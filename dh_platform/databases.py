"""Модуль для работы с БД"""

__author__: str = "Старков Е.П."

from functools import wraps
from typing import Any, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dh_platform.settings import (
    BaseAppSettings,
    DatabaseSettings,
    get_core_settings,
    get_db_settings,
)

db_config: DatabaseSettings = get_db_settings()
app_config: BaseAppSettings = get_core_settings()

# Создаем асинхронный движок SQLAlchemy
engine: AsyncEngine = create_async_engine(
    db_config.dsn,  # Используем свойство dsn
    echo=app_config.DEBUG,  # Логирование SQL-запросов (для разработки)
    pool_pre_ping=True,  # Проверка соединения перед использованием
)

# Создаем асинхронную сессию
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator:
    """Генератор сессий для Dependency Injection в FastAPI."""
    async with AsyncSessionLocal() as session:
        yield session


def add_session_db(method: Callable) -> Any:
    """
    Декоратор для добавления сессии подключения к БД в параметры.
    Управление откатом и закрытием производиться внутри

    Args:
        method: метод с запросом

    Returns:
        Результат метода

    Warnings:
        Параметр session обязательно должен идти после неименнованных параметров

    Examples:
        >>> @add_session_db
        >>> async def list(
        ...     cls, session: AsyncSession, filters: dict | None = None, navigation: dict | None = None
        ... ) -> Sequence[Row]:
        ...     ...
    """

    @wraps(method)
    async def wrapper(*args, **kwargs) -> Any:
        async with AsyncSessionLocal() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
