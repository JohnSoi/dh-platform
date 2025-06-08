"""Модуль для middleware логгера"""

__author__: str = "Старков Е.П."

import logging
from typing import Callable

from fastapi import Request

logger = logging.getLogger("dh_logger")


async def log_requests(request: Request, call_next: Callable) -> None:
    """
    Middleware для логирования запросов в FastAPI

    Args:
        request: запрос
        call_next: вызываемая функция

    Examples:
        >>> from dh_platform.logging import log_requests
        >>> ...
        >>> app.middleware("http")(log_requests)
    """
    logger.info("%s запрос на %s", request.method, request.url)
    try:
        response = await call_next(request)
        logger.info("Статус ответа: %d", response.status_code)
        return response
    except Exception as ex:
        logger.exception("Исключение: %s", ex)
        raise
