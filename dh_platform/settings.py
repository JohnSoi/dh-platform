"""Модуль базовых настроек"""

__author__: str = "Старков Е.П."

from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Базовые настройки приложений

    Attributes:
        APP_ENV (str): Тип окружения
        DEBUG (bool): Режим отладки
    Warnings:
        Данные переменные должны быть описаны в файле .env
    """

    APP_ENV: str = "production"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "CORE_"


@lru_cache
def get_core_settings() -> BaseAppSettings:
    """Получение объекта базовых настроек

    Returns:
        BaseAppSettings: Экземпляр класса базовых настроек
    Examples:
        Пример использования в конфиге приложений:

        >>> from pydantic import Field
        >>> from pydantic_settings import BaseSettings
        >>> from dh_platform.settings import get_core_settings
        >>>
        >>> class AllSettings(BaseSettings):
        ...     core: BaseAppSettings = Field(default_factory=get_core_settings)
        ...
        ...     class Config:
        ...         env_nested_delimiter = "__"
        >>>
        >>> @lru_cache
        >>> def get_all_settings() -> AllSettings:
        ...    return AllSettings()
    """
    return BaseAppSettings()
