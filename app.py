from flask import *
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from flask_script import Manager
from models import *

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def test():
    return '服务器正常运行'


if __name__ == '__main__':
    #app.run()
    manager.run()  # python3 app.py runserver