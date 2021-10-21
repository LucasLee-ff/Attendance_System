from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

curriculum_bp = Blueprint('Curriculum', __name__)
curriculum_api = Api(curriculum_bp)