from sqlalchemy.orm import (
        Mapped,
        mapped_column, relationship
)
from sqlalchemy import String, Uuid, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from enum import Enum
from typing import List

from .base import BasicObject
from .user import User


class InputTypes(Enum):
    TEXT = 1
    NUMBER = 2


class Template(BasicObject):
    __tablename__ = "template"

    date: Mapped[DateTime] = mapped_column()
    name: Mapped[String] = mapped_column()

    questions: Mapped[List["Question"]] = relationship(
            back_populates="template")
    answers: Mapped[List["AnswerTemplate"]] = relationship(
            back_populates="template")


class Question(BasicObject):
    __tablename__ = "question"

    template_id: Mapped[Uuid] = mapped_column(
            ForeignKey("template.id")
    )
    template: Mapped["Template"] = relationship(back_populates="questions")

    text: Mapped[String] = mapped_column()
    input_type: Mapped[Integer] = mapped_column(default=InputTypes.TEXT)
    order: Mapped[Integer] = mapped_column(default=0)

    answers: Mapped[List["Answer"]] = relationship(back_populates="question")


class AnswerTemplate(BasicObject):
    __tablename__ = "answer_template"

    user_id: Mapped[Uuid] = mapped_column(
            ForeignKey("user.id")
    )
    sender: Mapped["User"] = relationship(back_populates="answer_templates")

    template_id: Mapped[Uuid] = mapped_column(ForeignKey("template.id"))
    template: Mapped["Template"] = relationship(back_populates="answers")

    date: Mapped[DateTime] = mapped_column(server_default=func.now)

    answers: Mapped[List["Answer"]] = relationship(
            back_populates="answer_template")


class Answer(BasicObject):
    __tablename__ = "answer"

    question_id: Mapped[Uuid] = mapped_column(ForeignKey("question.id"))
    question: Mapped["Question"] = relationship(back_populates="answer")

    answer_template_id: Mapped[Uuid] = mapped_column(
            ForeignKey("answer_template.id"))
    answer_template: Mapped["AnswerTemplate"] = relationship(
            back_populates="answers")

    data: Mapped[String] = mapped_column()
