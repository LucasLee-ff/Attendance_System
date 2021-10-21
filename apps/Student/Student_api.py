from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

student_bp = Blueprint('Student', __name__)
student_api = Api(student_bp)

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
    if len(Stel)!=11 or (not Stel.isdigit()):
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
