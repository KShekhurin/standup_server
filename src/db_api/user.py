from flask import request, jsonify
from . import bp
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import select
import uuid

from ..models import User
from app import Session


# json body user validation schema
class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    is_active = fields.Bool(default=True, required=True)
    contact_id = fields.String(required=True)
    name = fields.String(required=True)


def get_user_by_id(session, id: uuid.UUID) -> User | None:
    statement = select(User).where(User.id == id)
    return session.scalars(statement).one_or_none()


@bp.route("/user", methods=["POST"])
def add_user_route():
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


@bp.route("/user/<string:id>", methods=["DELETE"])
def delete_user_route(id: str):
    try:
        uuid_id = uuid.UUID(id)
        user = None

        with Session.begin() as session:
            user = get_user_by_id(session, uuid_id)

            if user is None:
                return jsonify(
                        {"msg": "User with such UUID is not found"}), 404

            session.delete(user)

        return "Ok", 200
    except ValueError:
        return jsonify({"msg": "Invalid UUID!"}), 400


@bp.route("/user/<string:id>", methods=["GET"])
def get_user_route(id: str):
    try:
        uuid_id = uuid.UUID(id)

        with Session.begin() as session:
            user = get_user_by_id(session, uuid_id)

            if user is None:
                return jsonify(
                        {"msg": "User with such UUID is not found"}), 404

            session.expunge(user)

        return UserSchema().dump(user), 200
    except ValueError:
        return jsonify({"msg": "Invalid UUID"}), 400
