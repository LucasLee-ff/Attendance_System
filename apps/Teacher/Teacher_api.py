from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

teacher_bp = Blueprint('Teacher', __name__)
teacher_api = Api(teacher_bp)

teacher_curriculum_fields = {
    'Cid': fields.Integer(attribute='Cid'),
    'Cnum': fields.Integer(attribute='Cnum'),
    'Cname': fields.String(attribute='Cname'),
    'Cterm': fields.String(attribute='Cterm')
}

teacher_attendance_fields = {
    'Atime': fields.String(attribute='Atime'),
    'ADatetime': fields.String(attribute='ADatetime')
}

# 需要进行权限验证的路由
required_login_list = ['/teacher_restful/', '/Teacher/alterinformation/', '/teacher_curriculum/', '/teacher_attendance/'
    , '/attendance_situation/']


# 判断是否已经登录
@teacher_bp.before_app_request
def before_app_request():
    if request.path in required_login_list:  # 判断该路径是否需要权限验证
        if 'tid' in session:
            Tid = session['tid']
            g.teacher = Teacher.query.get(Tid)  # 验证成功
        else:
            return {'msg_code': 7}  # 未登录


# 教师登录
@teacher_bp.route('/Teacher/login/',methods=['POST'])
def teacher_login():
    Ttel = request.form.get('Ttel')
    Tpwd = request.form.get('Tpwd')
    teacher = Teacher.query.filter_by(Ttel=Ttel).first()
    if teacher:
        if teacher.Tpwd == Tpwd:
            session['tid'] = teacher.Tid
            return {'msg_code': 1}  # 登录成功
        return {'msg_code': 2}  # 用户名或密码错误
    return {'msg_code': 3}  # 用户名不存在


# 教师注册
@teacher_bp.route('/Teacher/register/',methods=['POST'])
def teacher_register():
    Ttel = request.form.get('Ttel')
    Tpwd = request.form.get('Tpwd')
    Tname = request.form.get('Tname')
    Tnum = request.form.get('Tnum')
    Tschool = request.form.get('Tschool')
    if len(Ttel) != 11 or (not Ttel.isdigit()):
        return {'msg_code': 2}  # 手机号不正确
    teacher = Teacher.query.filter_by(Ttel=Ttel).first()
    if teacher:
        return {'msg_code': 3}  # 手机号已注册
    teacher = Teacher.query.filter_by(Tnum=Tnum).first()
    if teacher and teacher.Tschool == Tschool:
        return {'msg code': 4}  # 教师已注册
    newTeacher = Teacher(Tnum, Tname, Tpwd, Ttel, Tschool)
    db.session.add(newTeacher)
    db.session.commit()  # 写入数据库中
    return {'msg_code': 1} # 注册成功


# 教师修改信息
@teacher_bp.route('/Teacher/alterinformation/',methods=['POST'])
def teacher_alterinformation():
    new_Tpwd = request.form.get('new_Tpwd')
    new_Tname = request.form.get('new_Tname')
    new_Tnum = request.form.get('new_Tnum')
    new_Tschool = request.form.get('new_Tschool')
    teacher = Teacher.query.get(g.teacher.Tid)
    if teacher:
        teacher.Tpwd = new_Tpwd
        teacher.Tname = new_Tname
        teacher.Tnum = new_Tnum
        teacher.Tschool = new_Tschool
        db.session.commit()
        return {'msg_code': 1}  # 修改成功
    return {'mag_code': 2}  # 修改失败


class teacher_curriculum(Resource):
    # 获取教师的所有课程
    def get(self):
        Tid = session['tid']
        curriculums = Curriculum.query.filter(Curriculum.Tid == Tid).all()
        if curriculums:
            return {'msg_code': 1, 'curriculums': marshal(curriculums, teacher_curriculum_fields)}  # 查询成功
        else:
            return {'msg_code': 2}  # 未查询到课程

    # 教师增加课程
    def post(self):
        Tid = session['tid']
        Cnum = request.form.get('Cnum')
        Cname = request.form.get('Cname')
        Cterm = request.form.get('Cterm')
        curriculums = Curriculum.query.filter(Curriculum.Tid == Tid).all()
        for c in curriculums:
            if c.Cnum == Cnum:
                return {'msg_code': 2}  # 重复创建课程
        newCurriculum = Curriculum(Cnum, Cname, Cterm, Tid)
        db.session.add(newCurriculum)
        db.session.commit()
        return {'msg_code': 1}  # 增加成功

    # 教师删除课程
    def delete(self):
        Tid = session['tid']
        Cid = request.form.get('Cid')
        curriculum = Curriculum.query.filter_by(Tid=Tid, Cid=Cid).first()
        if curriculum:
            student_curriculums = Student_Curriculum.query.filter(Student_Curriculum.Cid == Cid).all()
            for sc in student_curriculums:
                db.session.delete(sc)
                db.session.commit()
            attendances = Attendance.query.filter(Attendance.Cid == Cid).all()
            for a in attendances:
                student_attendances = Student_Attendance.query.filter(Student_Attendance.Aid == a.Aid).all()
                for sa in student_attendances:
                    db.session.delete(sa)
                    db.session.commit()
                db.session.delete(a)
                db.session.commit()
            for a in attendances:
                db.session.delete(a)
                db.session.commit()
            db.session.delete(curriculum)
            db.session.commit()
            return {'msg_code': 1}  # 删除成功
        return {'msg_code': 2}  # 课程不存在


class teacher_attendance(Resource):
    # 查询签到情况
    def get(self):
        Tid = session['tid']
        Cid = request.form.get('Cid')
        attendances = Attendance.query.filter(Attendance.Cid == Cid, Attendance.Tid == Tid).all()
        if attendances:
            return {'msg_code': 1, 'teacher_attendances': marshal(attendances, teacher_attendance_fields)}  # 查询成功
        else:
            return {'msg_code': 2}  # 未发起过签到

    # 发起签到
    def post(self):
        Tid = session['tid']
        Cid = request.form.get('Cid')
        Atime = request.form.get('Atime')
        attendance = Attendance.query.filter_by(Tid=Tid, Cid=Cid, Atime=Atime).first()
        if attendance:
            return {'msg_code': 2}  # 重复发起签到
        newAttendance = Attendance(Cid, Tid, Atime)
        db.session.add(newAttendance)
        db.session.commit()
        return {'msg_code': 1}  # 发起成功


class attendance_situation(Resource):
    def get(self):
        Tid = session['tid']
        Cid = request.form.get('Cid')
        Atime = request.form.get('Atime')
        attendance = Attendance.query.filter_by(Tid=Tid, Cid=Cid, Atime=Atime).first()
        student_attendances = Student_Attendance.query.filter(Student_Attendance.Aid == attendance.Aid).all()
        if student_attendances:
            return_msg = []
            for sa in student_attendances:
                student = Student.query.filter_by(Sid=sa.Sid).first()
                return_msg.append({'Snum': student.Snum, 'Sname': student.Sname, 'Datetime': str(sa.Datetime)})
            return {'msg_code': 1, 'attendance_situation': return_msg}  # 查询成功
        else:
            return {'msg_code': 2}  # 未查询到签到记录


class teacher_restful(Resource):
    # 查询某个教师
    def get(self):
        Tid = session['tid']
        teacher = Teacher.query.filter_by(Tid=Tid).first()
        if teacher:
            return_msg = {
                'msg_code': 1,
                'Tid': teacher.Tid,
                'Tnum': teacher.Tnum,
                'Tname': teacher.Tname,
                'Ttel': teacher.Ttel,
                'Tschool': teacher.Tschool
            }
            return return_msg
        else:
            return {'msg_code': 2}  # 查询的教师不存在


teacher_api.add_resource(teacher_curriculum, '/teacher_curriculum/')
teacher_api.add_resource(teacher_attendance, '/teacher_attendance/')
teacher_api.add_resource(teacher_restful, '/teacher_restful/')
teacher_api.add_resource(attendance_situation, '/attendance_situation/')
