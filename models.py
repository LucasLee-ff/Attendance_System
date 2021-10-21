# 数据库模型
from apps.ext import db
from datetime import datetime
'''
数据库初始化方法: 
1.在命令行输入python3 app.py db migrate
2.上一条命令执行后再输入python3 app.py db upgrade
'''

#教师
class Teacher(db.Model):
    __tablename__ = 'teacher'
    Tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Tnum = db.Column(db.Integer)
    Tname = db.Column(db.String(20), nullable=False)
    Tpwd = db.Column(db.String(30))
    Ttel = db.Column(db.Integer)
    #isDelete = db.Column(db.Boolean,default=False)
    Tschool = db.Column(db.String(40))
    CurriculumList = db.relationship('Curriculum', backref='Teacher', cascade='all, delete-orphan', passive_deletes=True)
    Attendancelist = db.relationship('Attendance', backref='Teacher', cascade='all, delete-orphan', passive_deletes=True)
    
    def __init__(self, Tnum, Tname, Tpwd, Ttel, Tschool):
        self.Tnum = Tnum
        self.Tname = Tname
        self.Tpwd = Tpwd
        self.Ttel = Ttel
        self.Tschool = Tschool

    def __repr__(self):
        return '<Teacher %r>' % self.Tname


#学生
class Student(db.Model):
    __tablename__ = 'student'
    Sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Snum = db.Column(db.Integer)
    Sname = db.Column(db.String(30), nullable=False)
    Stel = db.Column(db.Integer)
    Spwd = db.Column(db.String(30), nullable=False)
    Sschool = db.Column(db.String(40))
    CurriculumList = db.relationship('Curriculum', backref='Student', cascade='all, delete-orphan', passive_deletes=True)
    Attendancelist = db.relationship('Attendance', backref='Student', cascade='all, delete-orphan', passive_deletes=True)

    def __init__(self, Snum, Sname, Spwd, Stel, Sschool):
        self.Snum = Snum
        self.Sname = Sname
        self.Spwd = Spwd
        self.Stel = Stel
        self.Sschool = Sschool

    def __repr__(self):
        return '<Student %r>' % self.Sname


#课程
class Curriculum(db.Model):
    __tablename__ = 'curriculum'
    Cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cnum = db.Column(db.Integer)
    Cname = db.Column(db.String(30), nullable=True)
    Cterm = db.Column(db.String(30), nullable=True)
    #Kvalue = db.Column(db.String(50), nullable=True) # 密钥值
    #Kdate = db.Column(db.Date, nullable=True)  # 密钥过期日期
    #outofdate = db.Column(db.Boolean, nullable=True)
    Tid = db.Column(db.Integer, db.ForeignKey('teacher.Tid'),nullable=False)
    StudentList = db.relationship('Student', backref='Curriculum', cascade='all, delete-orphan', passive_deletes=True)
    Attendancelist = db.relationship('Attendance', backref='Curriculum', cascade='all, delete-orphan', passive_deletes=True)

    def __init__(self, Cum, Cname, Cterm, Tid):
        self.Cum = Cum
        self.Cname = Cname
        self.Cterm = Cterm
        self.Tid = Tid

    def __repr__(self):
        return '<Curriculum %r>' % self.Cname

#考勤
class Attendance(db.Model):
    __tablename__ = 'attendance'
    Aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cid = db.Column(db.Integer, db.ForeignKey('curriculum.Cid'), nullable=False)  # 签到课程id
    Tid = db.Column(db.Integer,db.ForeignKey('teacher.Tid'),nullable=False)  # 签到教师id
    Sid = db.Column(db.Integer, db.ForeignKey('student.Sid'), nullable=False)  # 签到学生id
    isSuceess = db.Column(db.Boolean, nullable=False)  # 是否签到成功
    ADatetime = db.Column(db.DateTime, default=datetime.now)  # 签到时间
    Atime = db.Column(db.Integer)  #签到次数

    def __init__(self, Cid, Tid, Sid , Atime, isSuccess):
        self.Cid = Cid
        self.Tid = Tid
        self.Sid = Sid
        self.Atime = Atime
        self.isSuceess = isSuccess

    def __repr__(self):
        return '<Record %r>' % self.Apid

# 系统数据
class System(db.Model):
    __tablename__ = 'system'
    id = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.Date,nullable=False)
    notice = db.Column(db.String(200))
    version = db.Column(db.String(20))