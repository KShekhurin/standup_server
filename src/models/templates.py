from sqlalchemy.orm import (
        Mapped,
        mapped_column, relationship
)
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from enum import Enum
from typing import List
from datetime import datetime
from uuid import UUID

from .base import BasicObject, Base


class InputTypes(Enum):
    TEXT = 1
    NUMBER = 2


class Template(BasicObject, Base):
    __tablename__ = "template"

    date: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column()

    questions: Mapped[List["Question"]] = relationship(
            back_populates="template")
    answers: Mapped[List["AnswerTemplate"]] = relationship(
            back_populates="template")


class Question(BasicObject, Base):
    __tablename__ = "question"

    template_id: Mapped[UUID] = mapped_column(
            ForeignKey("template.id")
    )
    template: Mapped["Template"] = relationship(back_populates="questions")

    text: Mapped[str] = mapped_column()
    input_type: Mapped[int] = mapped_column(default=InputTypes.TEXT)
    order: Mapped[int] = mapped_column(default=0)

    answers: Mapped[List["Answer"]] = relationship(back_populates="question")


class AnswerTemplate(BasicObject, Base):
    __tablename__ = "answer_template"

    user_id: Mapped[UUID] = mapped_column(
            ForeignKey("user.id")
    )
    sender: Mapped["User"] = relationship(back_populates="answer_templates")

    template_id: Mapped[UUID] = mapped_column(ForeignKey("template.id"))
    template: Mapped["Template"] = relationship(back_populates="answers")

    date: Mapped[datetime] = mapped_column(server_default=func.now())

    answers: Mapped[List["Answer"]] = relationship(
            back_populates="answer_template")


class Answer(BasicObject, Base):
    __tablename__ = "answer"

    question_id: Mapped[UUID] = mapped_column(ForeignKey("question.id"))
    question: Mapped["Question"] = relationship(back_populates="answer")

    answer_template_id: Mapped[UUID] = mapped_column(
            ForeignKey("answer_template.id"))
    answer_template: Mapped["AnswerTemplate"] = relationship(
            back_populates="answers")

    data: Mapped[str] = mapped_column()


class User(BasicObject, Base):
    __tablename__ = "user"

    is_active: Mapped[bool] = mapped_column(default=True)

    answer_templates: Mapped[List["AnswerTemplate"]] = relationship(
            back_populates="sender")

    # many-to-many User -> UserGroup -> Group
    groups: Mapped[List["Group"]] = relationship(
            secondary="user_group", back_populates="users")
    # one-to-many User -> UserGroup
    user_groups: Mapped[List["UserGroup"]] = relationship(
            back_populates="user")


class Group(BasicObject, Base):
    __tablename__ = "group"

    name: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    # many-to-many Group -> UserGroup -> User
    users: Mapped[List["User"]] = relationship(
            secondary="user_group", back_populates="groups")
    # one-to-many Group -> UserGroup
    user_groups: Mapped[List["UserGroup"]] = relationship(
            back_populates="group")


class UserGroup(Base):
    __tablename__ = "user_group"

    user_id: Mapped[UUID] = mapped_column(
            ForeignKey("user.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(back_populates="user_groups")

    group_id: Mapped[UUID] = mapped_column(
            ForeignKey("group.id"), primary_key=True
    )
    group: Mapped["Group"] = relationship(back_populates="user_groups")

    is_active: Mapped[bool] = mapped_column(default=True)
