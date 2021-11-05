from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

curriculum_bp = Blueprint('Curriculum', __name__)
curriculum_api = Api(curriculum_bp)


class curriculum_restful(Resource):
    # 查询某个课程
    def get(self):
        Cid = request.form.get('Cid')
        curriculum = Curriculum.query.filter_by(Cid=Cid).first()
        if curriculum:
            teacher = Teacher.query.filter_by(Tid=curriculum.Tid).first()
            return_msg = {
                'msg_code': 1,
                'Cid': curriculum.Cid,
                'Cnum': curriculum.Cnum,
                'Cname': curriculum.Cname,
                'Cterm': curriculum.Cterm,
                'Tname': teacher.Tname
            }
            return return_msg
        else:
            return {'msg_code': 2}  # 查询的课程不存在


curriculum_api.add_resource(curriculum_restful, '/curriculum_restful/')