from flask import request, jsonify
from . import bp
from marshmallow import Schema, fields, ValidationError

from ..models import User
from app import Session


# json body user validation schema
class UserSchema(Schema):
    is_active = fields.Bool(default=True, required=True)
    contact_id = fields.String(required=True)
    name = fields.String(required=True)


@bp.route("/user", methods=["POST"])
def add_user():
    body = request.get_json()

    try:
        user = UserSchema().load(body)
    except ValidationError as err:
        return err.messages, 400

    user_model = User(user["name"], user["contact_id"], user["is_active"])
    user_id = ""

    with Session.begin() as session:
        session.add(user_model)
        session.flush()
        user_id = str(user_model.id)

    return jsonify({"id": user_id}), 200
