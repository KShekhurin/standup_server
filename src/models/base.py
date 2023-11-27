from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Uuid
import uuid


class Base(DeclarativeBase):
    pass


class BasicObject(Base):
    id: Mapped[Uuid] = mapped_column(primary_key=True, default=uuid.uuid4)
