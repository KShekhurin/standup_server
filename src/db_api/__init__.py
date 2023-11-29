from flask import Blueprint

bp = Blueprint("db_api", __name__)


from .user import *
