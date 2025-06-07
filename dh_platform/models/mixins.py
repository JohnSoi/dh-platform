# pylint: disable=not-callable
"""Модуль миксинов"""

__author__: str = "Старков Е.П."

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class IDMixin:
    """
    Миксин для добавления первичного ключа

    Examples:
        >>> from dh_platform.models import BaseModel, IDMixin
        >>>
        >>> class User(BaseModel, IDMixin):
        ...     ...
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class UUIDMixin:
    """
    Миксин для добавления UUID первичного ключа

    Examples:
        >>> from dh_platform.models import BaseModel, UUIDMixin
        >>>
        >>> class User(BaseModel, UUIDMixin):
        ...     ...
    """

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, index=True)


class SoftDeleteMixin:
    """
    Миксин для мягкого удаления записей

    Examples:
        >>> from dh_platform.models import BaseModel, SoftDeleteMixin
        >>>
        >>> class User(BaseModel, SoftDeleteMixin):
        ...     ...
    """

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        """
        Мягкое удаление - запись остается, но с признаком удаления

        Examples:
            >>> from dh_platform.models import BaseModel, SoftDeleteMixin
            >>>
            >>> class User(BaseModel, SoftDeleteMixin):
            ...     ...
            >>>
            >>> user: User = User()
            >>> user.soft_delete() # пометит запись на удаление
        """
        self.deleted_at = func.now()


class TimestampMixin:
    """
    Миксин для полей создания и обновления записи

    Examples:
        >>> from dh_platform.models import BaseModel, TimestampMixin
        >>>
        >>> class User(BaseModel, TimestampMixin):
        ...     ...
        >>>
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @property
    def last_updated(self) -> datetime:
        """
        Возвращает время последнего обновления или создания

        Examples:
            >>> from dh_platform.models import BaseModel, TimestampMixin
            >>>
            >>> class User(BaseModel, TimestampMixin):
            ...     ...
            >>>
            >>> user: User = User()
            >>> print(user.last_updated) # Выведет дату создания или обновления
        """
        return self.updated_at or self.created_at


__all__: list[str] = [
    "IDMixin",
    "UUIDMixin",
    "SoftDeleteMixin",
    "TimestampMixin",
]
