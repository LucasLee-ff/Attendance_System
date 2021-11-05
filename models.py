# 数据库模型
from apps.ext import db
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey

'''
数据库初始化方法: 
1.在命令行输入python3 app.py db migrate
2.上一条命令执行后再输入python3 app.py db upgrade
'''


# 教师
class Teacher(db.Model):
    __tablename__ = 'teacher'
    Tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Tnum = db.Column(db.Integer, nullable=True)
    Tname = db.Column(db.String(20), nullable=False)
    Tpwd = db.Column(db.String(30), nullable=True)
    Ttel = db.Column(db.Integer, nullable=True)
    # isDelete = db.Column(db.Boolean,default=False)
    Tschool = db.Column(db.String(40))
    CurriculumList = db.relationship('Curriculum', backref='Teacher', cascade='all, delete-orphan',
                                     passive_deletes=True)
    Attendancelist = db.relationship('Attendance', backref='Teacher', cascade='all, delete-orphan',
                                     passive_deletes=True)

    def __init__(self, Tnum, Tname, Tpwd, Ttel, Tschool):
        self.Tnum = Tnum
        self.Tname = Tname
        self.Tpwd = Tpwd
        self.Ttel = Ttel
        self.Tschool = Tschool

    def __repr__(self):
        return '<Teacher %r>' % self.Tname


# 学生
class Student(db.Model):
    __tablename__ = 'student'
    Sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Snum = db.Column(db.Integer, nullable=True)
    Sname = db.Column(db.String(30), nullable=False)
    Stel = db.Column(db.Integer, nullable=True)
    Spwd = db.Column(db.String(30), nullable=True)
    Sschool = db.Column(db.String(40))
    CurriculumList = db.relationship('Curriculum', secondary="student_curriculum", backref='Student')
    Attendancelist = db.relationship('Attendance', secondary="student_attendance", backref='Student')

    def __init__(self, Snum, Sname, Spwd, Stel, Sschool):
        self.Snum = Snum
        self.Sname = Sname
        self.Spwd = Spwd
        self.Stel = Stel
        self.Sschool = Sschool

    def __repr__(self):
        return '<Student %r>' % self.Sname


# 课程
class Curriculum(db.Model):
    __tablename__ = 'curriculum'
    Cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cnum = db.Column(db.String(20), nullable=True)
    Cname = db.Column(db.String(30), nullable=True)
    Cterm = db.Column(db.String(30))
    # Kvalue = db.Column(db.String(50), nullable=True) # 密钥值
    # Kdate = db.Column(db.Date, nullable=True)  # 密钥过期日期
    # outofdate = db.Column(db.Boolean, nullable=True)
    Tid = db.Column(db.Integer, db.ForeignKey('teacher.Tid'), nullable=False)
    StudentList = db.relationship('Student', secondary="student_curriculum", backref='Curriculum')
    Attendancelist = db.relationship('Attendance', backref='Curriculum', cascade='all, delete-orphan',
                                     passive_deletes=True)

    def __init__(self, Cnum, Cname, Cterm, Tid):
        self.Cnum = Cnum
        self.Cname = Cname
        self.Cterm = Cterm
        self.Tid = Tid

    def __repr__(self):
        return '<Curriculum %r>' % self.Cname


# 考勤
class Attendance(db.Model):
    __tablename__ = 'attendance'
    Aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cid = db.Column(db.Integer, db.ForeignKey('curriculum.Cid'), nullable=False)  # 签到课程id
    Tid = db.Column(db.Integer, db.ForeignKey('teacher.Tid'), nullable=False)  # 签到教师id
    Studentlist = db.relationship('Student', secondary="student_attendance", backref='Attendance')  # 签到学生
    ADatetime = db.Column(db.DateTime, default=datetime.now)  # 发起签到时间
    Atime = db.Column(db.Integer)  # 签到次数

    def __init__(self, Cid, Tid, Atime):
        self.Cid = Cid
        self.Tid = Tid
        self.Atime = Atime

    def __repr__(self):
        return '<Attendance %r>' % self.Aid


# 多对多
class Student_Curriculum(db.Model):
    __tablename__ = 'student_curriculum'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Sid = Column(Integer, ForeignKey("student.Sid"), nullable=False)
    Cid = Column(Integer, ForeignKey("curriculum.Cid"), nullable=False)

    def __init__(self, Sid, Cid):
        self.Sid = Sid
        self.Cid = Cid

    def __repr__(self):
        return '<Student_Curriculum %r>' % self.id


# 签到情况
class Student_Attendance(db.Model):
    __tablename__ = 'student_attendance'
    id = Column(Integer, primary_key=True)
    Sid = Column(Integer, ForeignKey("student.Sid"), autoincrement=True)
    Aid = Column(Integer, ForeignKey("attendance.Aid"), autoincrement=True)
    Datetime = db.Column(db.DateTime, default=datetime.now)  # 签到时间

    def __init__(self, Sid, Aid):
        self.Sid = Sid
        self.Aid = Aid

    def __repr__(self):
        return '<Student_Attendance %r>' % self.id


# 系统数据
class System(db.Model):
    __tablename__ = 'system'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)
    notice = db.Column(db.String(200))
    version = db.Column(db.String(20))