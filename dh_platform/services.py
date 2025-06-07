# pylint: disable=unused-argument
"""Модуль для базового сервиса"""

__author__: str = "Старков Е.П."

from typing import Type, TypeVar, Generic, List

from sqlalchemy import Result, Row, Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from dh_platform.databases import add_session_db
from dh_platform.models import BaseModel
from dh_platform.types import DictOrNone


M = TypeVar('M', bound=BaseModel)


class BaseService(Generic[M]):
    """
    Базовый сервис

    Generic:
        M: Модель сущности

    Examples:
        Создание сервиса:
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
    async def create(cls, data: dict, session: AsyncSession) -> BaseModel:
        """
        Создание сущности и запись ее в БД

        Args:
            data (dict): Данные о сущности
            session (AsyncSession): Сессия подключения к БД

        Returns:
            (BaseModel): Данные модели
        """
        await cls._before_create(data)
        new_entity: BaseModel = cls._MODEL(**data)
        session.add(new_entity)
        await session.commit()
        await cls._after_create(new_entity)

        return new_entity

    @classmethod
    @add_session_db
    async def list(
        cls, filters: DictOrNone = None, navigation: DictOrNone = None, *, session: AsyncSession
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
            Получение полного списка:
            >>> async def get_users(session: AsyncSession) -> List[UserModel]:
            ...     return UserService.list(session)
            Получение списка с фильтрацией и навигацией:
            >>> async def get_active_users(session: AsyncSession) -> List[UserModel]:
            ...     return UserService.list(session, {"is_active": True}, {"page": 0, "limit": 30})
        """
        await cls._before_read(filters, navigation)
        query_result: Result[tuple[M]] = await session.execute(select(cls._MODEL))
        result: List[M] = list(query_result.scalars().all())
        await cls._after_read(result, filters, navigation)

        return result

    @classmethod
    async def _before_read(cls, filters: DictOrNone, navigation: DictOrNone) -> None: ...

    @classmethod
    async def _after_read(cls, result: List[M], filters: DictOrNone, navigation: DictOrNone) -> None: ...

    @classmethod
    def _before_create(cls, create_data: dict) -> None: ...

    @classmethod
    def _after_create(cls, entity_data: dict) -> None: ...
