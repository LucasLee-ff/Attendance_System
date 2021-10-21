from flask import Flask
from apps.settings import Config
from apps.ext import db
from flask_ckeditor import CKEditor
from apps.Student.Student_api import student_bp
from apps.Teacher.Teacher_api import teacher_bp
from apps.Attendance.Attendance_api import attendance_bp
from apps.Curriculum.Curriculum_api import curriculum_bp

ckeditor = CKEditor()

def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)  # 修改配置属性
        db.init_app(app)
        ckeditor.init_app(app)

        # 注册蓝图
        app.register_blueprint(student_bp)
        app.register_blueprint(teacher_bp)
        app.register_blueprint(attendance_bp)
        app.register_blueprint(curriculum_bp)
        return app
