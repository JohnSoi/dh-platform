from pydantic_settings import BaseSettings
from functools import lru_cache


class BaseAppSettings(BaseSettings):
    """
    Базовые настройки всех приложений экосистемы

    Attributes:
        APP_ENV (str): Текущее окружение
        DEBUG (bool): Режим отладки
    """
    APP_ENV: str = "production"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "CORE_"


@lru_cache
def get_core_settings() -> BaseAppSettings:
    return BaseAppSettings()
