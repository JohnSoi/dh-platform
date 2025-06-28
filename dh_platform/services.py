# pylint: disable=unused-argument
"""Модуль для базового сервиса"""

__author__: str = "Старков Е.П."

from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Result, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from dh_platform.databases import add_session_db
from dh_platform.models import BaseModel
from dh_platform.types import DictOrNone

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

    @classmethod
    @add_session_db
    async def create(cls, data: PydanticBaseModel, session: AsyncSession = None) -> BaseModel: # type: ignore[call-arg]
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
        await cls._before_read(filters, navigation)
        query_result: Result[tuple[M]] = await session.execute(select(cls._MODEL))
        result: List[M] = list(query_result.scalars().all())
        await cls._after_read(result, filters, navigation)

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
    async def _before_read(cls, filters: DictOrNone, navigation: DictOrNone) -> None: ...

    @classmethod
    async def _after_read(cls, result: List[M], filters: DictOrNone, navigation: DictOrNone) -> None: ...

    @classmethod
    async def _before_create(cls, create_data: dict) -> None: ...

    @classmethod
    async def _after_create(cls, entity_data: M, create_data: dict) -> None: ...
