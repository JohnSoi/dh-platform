"""Пакет для схем данных миксинов"""

__author__: str = "Старков Е.П."

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EntityID(BaseModel):
    """
    Миксин схемы данных для числового идентификатора

    Examples:
        >>> from dh_platform.schemas import EntityID
        >>>
        >>> class UserData(EntityID):
        ...     ...
    """

    id: int


class EntityUUID(BaseModel):
    """
    Миксин схемы данных для идентификатора UUID

    Examples:
        >>> from dh_platform.schemas import EntityUUID
        >>>
        >>> class UserData(EntityUUID):
        ...     ...
    """

    uuid: UUID


class SoftDeletedDateTime(BaseModel):
    """
    Миксин для даты удаления записи

    Examples:
        >>> from dh_platform.schemas import SoftDeletedDateTime
        >>>
        >>> class UserData(SoftDeletedDateTime):
        ...     ...
    """

    deleted_at: datetime | None = None


class OperationDateTime(BaseModel):
    """
    Миксин для дат создания и удаления

    Examples:
        >>> from dh_platform.schemas import OperationDateTime
        >>>
        >>> class UserData(OperationDateTime):
        ...     ...
        >>>
    """

    created_at: datetime
    updated_at: datetime | None = None


__all__: list[str] = [
    "EntityID",
    "EntityUUID",
    "SoftDeletedDateTime",
    "OperationDateTime",
]
