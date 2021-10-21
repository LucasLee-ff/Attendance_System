from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

teacher_bp = Blueprint('Teacher', __name__)
teacher_api = Api(teacher_bp)

# 需要进行权限验证的路由
required_login_list = ['/Teacher/get']

# 判断是否已经登录
@teacher_bp.before_app_request
def before_app_request():
    if request.path in required_login_list:  # 判断该路径是否需要权限验证
        if 'tid' in session:
            Tid = session['tid']
            g.teacher = Teacher.query.get(Tid)
            return {'msg_code': 1}  # 验证成功
        else:
            return {'msg_code': 2}  # 未登录

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
    if len(Ttel)!=11 or (not Ttel.isdigit()):
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


class Teacher(Resource):
    # 查询某个教师
    def get(self):
        parser = reqparse.RequestParser()
        #parser.add_argument('Tid', type=int)
        args = parser.parse_args()
        Tid = session['tid']

        teacher = Teacher.query.filter(Teacher.Tid == Tid).first()
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
            return {'msg_code': 7}, 404  # 查询的教师不存在

teacher_api.add_resource(Teacher, '/Teacher')