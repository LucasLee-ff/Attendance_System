from flask import Blueprint, request, session, g
from flask_restful import Api, Resource, fields, marshal_with, reqparse, marshal, abort
from models import *

attendance_bp = Blueprint('Attendance', __name__)
attendance_api = Api(attendance_bp)