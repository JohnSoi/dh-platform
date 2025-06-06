"""Модуль для работы с БД"""

__author__: str = "Старков Е.П."

from typing import AsyncGenerator

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
