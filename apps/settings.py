import os

class Config:
    ENV = 'development'
    DEBUG = True
    Threaded = True
    # URI需要修改成本地的数据库地址  格式：'数据库名+驱动名://用户名:密码@主机IP:端口号/数据库表名'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asdfghijklmn'  # session运行时的加密密钥
    #项目路径
    BASE_DIR = os.path.abspath(os.getcwd())
    #服务器IP地址:端口号
    SERVER_IP = "http://127.0.0.1:5000"
    if __name__=='__main__':
        print(BASE_DIR)