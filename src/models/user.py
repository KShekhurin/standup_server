from sqlalchemy.orm import (
        Mapped,
        mapped_column, relationship
)
from sqlalchemy import String, Uuid, Boolean, ForeignKey
from typing import List

from .base import BasicObject, Base
from .templates import AnswerTemplate


class User(BasicObject):
    __tablename__ = "user"
    is_active: Mapped[Boolean] = mapped_column(default=True)

    answer_templates: Mapped[List["AnswerTemplate"]] = relationship(
            back_populates="sender")


class Group(BasicObject):
    __tablename__ = "group"

    name: Mapped[String] = mapped_column()
    is_active: Mapped[Boolean] = mapped_column(default=True)


class UserGroup(Base):
    user_id: Mapped[Uuid] = mapped_column(
            ForeignKey("user.id"), primary_key=True
    )
    group_id: Mapped[Uuid] = mapped_column(
            ForeignKey("group.id"), primary_key=True
    )
    is_active: Mapped[Boolean] = mapped_column(default=True)
