from flask import request, jsonify
from . import bp
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import select
import uuid

from ..models import User, Group, UserGroup
from app import Session


# json body user validation schema
class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    is_active = fields.Bool(load_default=True)
    contact_id = fields.String(required=True)
    name = fields.String(required=True)

    groups_ids = fields.List(fields.UUID(), load_only=True, required=False)


# json body group validation schema
class GroupSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    contact_id = fields.String(required=True)
    is_active = fields.Bool(load_default=True)

    users_id = fields.List(fields.UUID(), load_only=True, required=False)


def get_object_by_id(session, model, id: uuid.UUID):
    statement = select(model).where(model.id == id)
    return session.scalars(statement).one_or_none()


def template_delete_object(model, id: uuid.UUID):
    try:
        uuid_id = uuid.UUID(id)
        obj = None

        with Session.begin() as session:
            obj = get_object_by_id(session, model, uuid_id)

            if obj is None:
                return jsonify(
                        {"msg": "User with such UUID is not found"}), 404

            session.delete(obj)

        return "Ok", 200
    except ValueError:
        return jsonify({"msg": "Invalid UUID!"}), 400


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
    return template_delete_object(User, id)


@bp.route("/user/<string:id>", methods=["GET"])
def get_user_route(id: str):
    try:
        uuid_id = uuid.UUID(id)

        with Session.begin() as session:
            user = get_object_by_id(session, User, uuid_id)

            if user is None:
                return jsonify(
                        {"msg": "User with such UUID is not found"}), 404

            session.expunge(user)

        return UserSchema().dump(user), 200
    except ValueError:
        return jsonify({"msg": "Invalid UUID"}), 400


@bp.route("/group", methods=["POST"])
def add_group_route():
    try:
        body = request.get_json()
        group = GroupSchema().load(body)

        group_model = Group(
                group["name"], group["contact_id"], group["is_active"])
        group_id = ""

        with Session.begin() as session:
            session.add(group_model)
            session.flush()
            group_id = str(group_model.id)

        return jsonify({"id": group_id}), 200
    except ValidationError as err:
        return err.message, 400


@bp.route("/group/<string:group_id>/user/<string:user_id>", methods=["POST"])
def add_user_to_group(group_id: str, user_id: str):
    try:
        group_uuid = uuid.UUID(group_id)
        user_uuid = uuid.UUID(user_id)

        with Session.begin() as session:
            user = get_object_by_id(session, User, user_uuid)
            group = get_object_by_id(session, Group, group_uuid)

            if user is None:
                return jsonify({"err": "User not found"}), 404
            if group is None:
                return jsonify({"err": "Group not found"}), 404

            user.groups.append(group)

        return "Ok", 200
    except ValueError:
        return jsonify({"err": "UUID is incorrect"}), 400


@bp.route("/group/<string:group_id>/user/<string:user_id>", methods=["DELETE"])
def remove_user_from_group_route(group_id: str, user_id: str):
    try:
        group_uuid = uuid.UUID(group_id)
        user_uuid = uuid.UUID(user_id)

        with Session.begin() as session:
            user = get_object_by_id(session, User, user_uuid)
            group = get_object_by_id(session, Group, group_uuid)

            if user is None:
                return jsonify({"err": "User not found"}), 404
            if group is None:
                return jsonify({"err": "Group not found"}), 404

            group.users.remove(user)

        return "Ok", 200
    except ValueError:
        return jsonify({"err": "UUID is incorrect"}), 400


@bp.route("/group/<string:id>", methods=["DELETE"])
def delete_group_route(id: str):
    return template_delete_object(Group, id)
