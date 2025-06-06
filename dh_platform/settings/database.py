"""Модуль настроек подключения к БД"""

__author__: str = "Старков Е.П."

from functools import lru_cache

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Настройки подключения к БД

    Attributes:
        HOST (str): Хост БД
        PORT (str): Порт БД
        USER (str): Пользователь БД
        PASSWORD (str): Пароль БД
        NAME (str): Название БД
        DRIVER (str): Драйвер БД
    Warnings:
        Данные переменные должны быть описаны в файле .env
    """

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str
    DRIVER: str = "postgresql+asyncpg"

    class Config:
        """Класс конфигурации настроек"""

        env_prefix = "DB_"
        env_file = ".env"
        extra = "ignore"

    @property
    def dsn(self) -> str:
        """Формирует DSN (Data Source Name) для подключения."""
        return (
            f"{self.DRIVER}://"
            f"{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}"
            f"/{self.NAME}"
        )


@lru_cache
def get_db_settings() -> DatabaseSettings:
    """
    Получение объекта базовых настроек

    Returns:
        BaseAppSettings: Экземпляр класса базовых настроек
    Examples:
        Пример использования в конфиге приложений:

        >>> from pydantic import Field
        >>> from pydantic_settings import BaseSettings
        >>> from dh_platform.settings import *
        >>>
        >>> class AllSettings(BaseSettings):
        ...     core: BaseAppSettings = Field(default_factory=get_core_settings)
        ...     db: DatabaseSettings = Field(default_factory=get_db_settings)
        ...
        ...     class Config:
        ...         env_nested_delimiter = "__"
        >>>
        >>> @lru_cache
        >>> def get_all_settings() -> AllSettings:
        ...    return AllSettings()
    """
    return DatabaseSettings() # type: ignore[call-arg]
