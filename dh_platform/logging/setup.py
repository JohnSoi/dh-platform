"""Модуль для настройки логгера"""

__author__: str = "Старков Е.П."

from logging.config import dictConfig
from pathlib import Path

from dh_platform.logging.consts import LOG_CONFIG


def setup_logging() -> None:
    """
    Настройка логирования

    Examples:
        >>> @asynccontextmanager
        >>> async def lifespan(_: FastAPI):
        ...     setup_logging()
        ...     yield
        >>>
        >>> app: FastAPI = FastAPI(
        ...     title=settings.core.PROJECT_NAME,
        ...     version=settings.core.VERSION,
        ...     debug=settings.core.DEBUG,
        ...     lifespan=lifespan,
        ... )
    """
    # Создаем директорию для логов если ее нет
    Path("logs").mkdir(exist_ok=True)

    dictConfig(LOG_CONFIG)
