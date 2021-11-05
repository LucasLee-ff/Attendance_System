from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

student_bp = Blueprint('Student', __name__)
student_api = Api(student_bp)

student_curriculum_fields = {
    'Cid': fields.Integer(attribute='Cid'),
    'Cnum': fields.Integer(attribute='Cnum'),
    'Cname': fields.String(attribute='Cname'),
    'Cterm': fields.String(attribute='Cterm'),
    'Tid': fields.Integer(attribute='Tid')
}

# 需要进行权限验证的路由
required_login_list = ['/Student/alterinformation/', '/student_curriculum/', '/student_attendance/']


# 判断是否已经登录
@student_bp.before_app_request
def before_app_request():
    if request.path in required_login_list:  # 判断该路径是否需要权限验证
        if 'sid' in session:
            Sid = session['sid']
            g.student = Student.query.get(Sid)
        else:
            return {'msg_code': 7}  # 未登录


# 学生登录
@student_bp.route('/Student/login/',methods=['POST'])
def student_login():
    Stel = request.form.get('Stel')
    Spwd = request.form.get('Spwd')
    student = Student.query.filter_by(Stel=Stel).first()
    if student:
        if student.Spwd == Spwd:
            session['sid'] = student.Sid
            session['spwd'] = student.Spwd
            return {'msg_code': 1}  # 登录成功
        return {'msg_code': 2}  # 用户名或密码错误
    return {'msg_code': 3}  # 用户名不存在


# 学生注册
@student_bp.route('/Student/register/',methods=['POST'])
def student_register():
    Stel = request.form.get('Stel')
    Spwd = request.form.get('Spwd')
    Sname = request.form.get('Sname')
    Snum = request.form.get('Snum')
    Sschool = request.form.get('Sschool')
    if len(Stel) != 11 or (not Stel.isdigit()):
        return {'msg_code': 2}  # 手机号不正确
    student = Student.query.filter_by(Stel=Stel).first()
    if student:
        return {'msg_code': 3}  # 手机号已注册
    student = Student.query.filter_by(Snum=Snum).first()
    if student and student.Sschool == Sschool:
        return {'msg code': 4}  # 学生已注册
    newStudent = Student(Snum, Sname, Spwd, Stel, Sschool)
    db.session.add(newStudent)
    db.session.commit()  # 写入数据库中
    return {'msg_code': 1}  # 注册成功


# 学生修改信息
@student_bp.route('/Student/alterinformation/',methods=['POST'])
def student_alterinformation():
    new_Spwd = request.form.get('new_Spwd')
    new_Sname = request.form.get('new_Sname')
    new_Snum = request.form.get('new_Snum')
    new_Sschool = request.form.get('new_Sschool')
    student = Student.query.get(g.student.Sid)
    if student:
        student.Tpwd = new_Spwd
        student.Tname = new_Sname
        student.Tnum = new_Snum
        student.Tschool = new_Sschool
        db.session.commit()
        return {'msg_code': 1}  # 修改成功
    return {'mag_code': 2}  # 修改失败


# 学生选课相关
class student_curriculum(Resource):
    # 获取学生的所有选课
    def get(self):
        Sid = session['sid']
        student = Student.query.filter_by(Sid=Sid).first()
        curriculums = student.CurriculumList
        if curriculums:
            return {'msg_code': 1, 'curriculums': marshal(curriculums, student_curriculum_fields)}  # 查询成功
        else:
            return {'msg_code': 2}  # 未查询到课程

    # 学生增加选课
    def post(self):
        Sid = session['sid']
        Cid = request.form.get('Cid')
        curriculum = Curriculum.query.filter_by(Cid=Cid).first()
        if not curriculum:
            return {'msg_code': 2}  # 课程不存在
        student = Student.query.filter_by(Sid=Sid).first()
        curriculums = student.CurriculumList
        for c in curriculums:
            if c.Cid == int(Cid):
                return {'msg_code': 3}  # 重复选课
        newStudent_Curriculum = Student_Curriculum(Sid, Cid)
        db.session.add(newStudent_Curriculum)
        db.session.commit()
        return {'msg_code': 1}  # 增加成功

    def delete(self):
        Sid = session['sid']
        Cid = request.form.get('Cid')
        student_curriculum = Student_Curriculum.query.filter_by(Cid=Cid, Sid=Sid).first()
        if not student_curriculum:
            return {'msg_code': 2}  # 未选该课程
        db.session.delete(student_curriculum)
        db.session.commit()
        return {'msg_code': 1}  # 删除成功


# 学生签到相关
class student_attendance(Resource):
    def get(self):
        Sid = session['sid']
        Cid = request.form.get('Cid')
        attendances = Attendance.query.filter(Attendance.Cid == Cid).all()
        student_attendances = []
        for a in attendances:
            if Student_Attendance.query.filter_by(Sid=Sid, Aid=a.Aid).first():
                student_attendances.append(Student_Attendance.query.filter_by(Sid=Sid, Aid=a.Aid).first())
        if student_attendances:
            return_msg = []
            for sa in student_attendances:
                attendance = Attendance.query.filter_by(Aid=sa.Aid).first()
                return_msg.append({'Atime': attendance.Atime, 'Datetime': str(sa.Datetime)})
            return {'msg_code': 1, 'student_attendances': return_msg}  # 查询成功
        else:
            return {'msg_code': 2}  # 未查询到签到记录

    def post(self):
        Sid = session['sid']
        Cid = request.form.get('Cid')
        Atime = request.form.get('Atime')
        isSuccess = request.form.get('isSuccess')
        student_curriculum = Student_Curriculum.query.filter_by(Sid=Sid, Cid=Cid).first()
        if not student_curriculum:
            return {'msg_code': 2}  # 未选课
        attendance = Attendance.query.filter_by(Cid=Cid, Atime=Atime).first()
        if not attendance:
            return {'msg_code': 3}  # 未发起签到
        student_attendance = Student_Attendance.query.filter_by(Sid=Sid, Aid=attendance.Aid).first()
        if student_attendance:
            return {'msg_code': 4}  # 已成功签到
        if int(isSuccess) == 0:
            return {'msg_code': 5}  # 签到失败
        newStudent_Attendance = Student_Attendance(Sid, attendance.Aid)
        db.session.add(newStudent_Attendance)
        db.session.commit()
        return {'msg_code': 1}  # 签到成功


student_api.add_resource(student_curriculum, '/student_curriculum/')
student_api.add_resource(student_attendance, '/student_attendance/')