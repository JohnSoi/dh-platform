# pylint: disable=unused-argument
"""Модуль для базового сервиса"""

__author__: str = "Старков Е.П."

from datetime import datetime
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Result, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from dh_platform.databases import add_session_db
from dh_platform.models import BaseModel
from dh_platform.types import DictOrNone
from dh_platform.exceptions import EntityNotFound, UpdateAllowedById

M = TypeVar("M", bound=BaseModel)


class BaseService(Generic[M]):
    """
    Базовый сервис

    Generic:
        M: Модель сущности

    Examples:
        >>> from dh_platform.services import BaseService
        >>> from dh_platform.models import BaseModel
        >>>
        >>>
        >>> class UserModel(BaseModel):
        ...     ...
        >>>
        >>>
        >>> class UserService(BaseService):
        ...     _MODEL = UserModel
        >>>
    """

    _MODEL: Type[M]
    _PRIMARY_KEY: str = "id"

    @classmethod
    @add_session_db
    async def create(cls, data: PydanticBaseModel, session: AsyncSession) -> M: # type: ignore[call-arg]
        """
        Создание сущности и запись ее в БД

        Args:
            data (dict): Данные о сущности
            session (AsyncSession): Сессия подключения к БД

        Returns:
            (M): Данные модели

        Examples:
            >>> from dh_platform.services import BaseService
            >>>
            >>> class UserModel(BaseModel):
            ...     ...
            >>>
            >>> class UserService(BaseService):
            >>>     _MODEL = UserModel
            >>>
            >>> await UserService.create({})
        """
        data_dict: dict = data.model_dump()
        await cls._before_create(data_dict)

        new_entity: M = cls._get_new_entity(data_dict)

        session.add(new_entity)
        await session.commit()
        await cls._after_create(new_entity, data_dict)

        return new_entity

    @classmethod
    @add_session_db
    async def update(cls, new_data: PydanticBaseModel, session: AsyncSession):
        data_dict: dict = new_data.model_dump()

        if data_dict.get(cls._PRIMARY_KEY) is None:
            raise UpdateAllowedById()

        old_data: M = await cls.read(entity_id=data_dict.get(cls._PRIMARY_KEY))

        await cls._before_update(data_dict, old_data)

        for key, value in data_dict.items():
            if hasattr(old_data, key):
                setattr(old_data, key, value)

        if hasattr(old_data, "updated_at"):
            old_data.updated_at = datetime.now()

        session.add(old_data)
        await session.commit()
        await cls._after_update(old_data)

        return old_data

    @classmethod
    @add_session_db
    async def read(cls, entity_id: int, session: AsyncSession) -> M:
        data: M = await cls.get_one_by_filter(id=entity_id)

        if not data:
            raise EntityNotFound()

        await cls._after_read(data)

        return data

    @classmethod
    @add_session_db
    async def delete(cls, entity_id: int, force_delete: bool = False, session: AsyncSession = None) -> bool:
        data: M = await cls.read(entity_id)

        if hasattr(data, "deleted_at"):
            if data.deleted_at:
                force_delete = True
        else:
            force_delete = True

        await cls._before_delete(data, force_delete)

        if force_delete:
            await session.delete(data)
        else:
            data.deleted_at = datetime.now()
            session.add(data)
            await session.commit()

        await cls._after_delete(data)

    @classmethod
    @add_session_db
    async def list(
            cls, filters: DictOrNone = None, navigation: DictOrNone = None, session: AsyncSession = None # type: ignore[call-arg]
    ) -> List[M]:
        """
        Запрос списка по сущности с фильтрацией и навигацией

        Args:
            session (AsyncSession): Сессия подключения к БД
            filters (dict | None): Фильтр метода
            navigation (dict | None): Навигация метода

        Returns:
            (List[M]): результаты запроса

        Examples:
            >>> async def get_users(session: AsyncSession) -> List[UserModel]:
            ...     return UserService.list(session)
            >>>
            >>> async def get_active_users(session: AsyncSession) -> List[UserModel]:
            ...     return UserService.list(session, {"is_active": True}, {"page": 0, "limit": 30})
        """
        query: Select = select(cls._MODEL)
        query = await cls._before_list(query, filters, navigation)
        query_result: Result[tuple[M]] = await session.execute(query)
        result: List[M] = list(query_result.scalars().all())
        await cls._after_list(result, filters, navigation)

        return result

    @classmethod
    @add_session_db
    async def get_one_by_filter(cls, session: AsyncSession, **filters) -> M | None:
        query: Select = select(cls._MODEL).filter_by(**filters)
        data: Result[tuple[M]] = await session.execute(query)

        return data.scalar_one_or_none()

    @classmethod
    def _get_new_entity(cls, data_dict: dict) -> M:
        """
        Получение модели с данными

        Args:
            data_dict (dict): Данные для создания

        Returns:
            (M): Модель с данными
        """
        entity_data: dict = {}

        for key, value in data_dict.items():
            if hasattr(cls._MODEL, key):
                entity_data[key] = value

        new_entity: M = cls._MODEL(**entity_data)

        return new_entity

    @classmethod
    async def _before_list(cls, query: Select, filters: DictOrNone, navigation: DictOrNone) -> None:
        if filters:
            for key, value in filters.items():
                if hasattr(cls._MODEL, key):
                    query = query.where(key == value)

        return query

    @classmethod
    async def _after_list(cls, result: List[M], filters: DictOrNone, navigation: DictOrNone) -> None: ...

    @classmethod
    async def _before_create(cls, create_data: dict) -> None: ...

    @classmethod
    async def _after_create(cls, entity_data: M, create_data: dict) -> None: ...

    @classmethod
    async def _after_read(cls, entity_data: M) -> None:
        ...

    @classmethod
    async def _before_update(cls, data_dict: dict, old_data: M) -> None:
        ...

    @classmethod
    async def _after_update(cls, old_data: M) -> None:
        ...

    @classmethod
    async def _before_delete(cls, entity_data: M, force_delete: bool) -> None:
        ...

    @classmethod
    async def _after_delete(cls, entity_data: M) -> None:
        ...
