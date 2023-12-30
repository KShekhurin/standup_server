from flask import Blueprint

bp = Blueprint("client", __name__, static_folder="static", template_folder="pages")


from .routes import *
