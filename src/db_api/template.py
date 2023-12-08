from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from flask import request, jsonify

from . import bp
from ..models import Template, Question, InputTypes
from app import Session


class QuestionSchema(Schema):
    text = fields.String(default="")
    input_type = EnumField(InputTypes, by_value=True)


class TemplateSchema(Schema):
    name = fields.String(required=True)
    questions = fields.List(fields.Nested(QuestionSchema),
                            required=True, on_load=True)


@bp.route("/template", methods=["POST"])
def add_template_route():
    try:
        body = request.get_json()
        template = TemplateSchema().load(body)
        template_id = None

        with Session.begin() as session:
            template_model = Template.from_dict(template)
            session.add(template_model)
            questions = template["questions"]

            for i, question in enumerate(questions):
                question_model = Question(question["text"],
                                          question["input_type"], i)
                session.add(question_model)
                template_model.questions.append(question_model)

            session.flush()
            template_id = template_model.id

        return jsonify({"id": str(template_id)}), 200

    except ValidationError as err:
        return err.messages, 400
