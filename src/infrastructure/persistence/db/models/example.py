from uuid import UUID, uuid4
from typing import Any, ClassVar

from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class Example(TimedBaseModel):
    __tablename__ = "example"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}  # type: ignore

    id: Mapped[UUID] = mapped_column(nullable=False, primary_key=True, default=uuid4)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
