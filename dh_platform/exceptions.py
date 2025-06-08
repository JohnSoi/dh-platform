"""Модуль для базового исключения"""

__author__: str = "Старков Е.П."

import logging

from fastapi import HTTPException, status

from .types import DictOrNone

logger = logging.getLogger("dh_logger")


class BaseAppException(HTTPException):
    """
    Базовый класс исключений.
    Используется для расширения конкретным исключением приложения

    Attributes:
        _DETAIL (str): Текст сообщения ошибки
        _CODE (int): HTTP код ошибки. По-умолчанию - HTTP_500_INTERNAL_SERVER_ERROR
    Examples:
        >>> from fastapi import status
        >>> from dh_platform.exceptions import BaseAppException
        >>>
        >>>
        >>> class EntityNotFound(BaseAppException):
        ...     _DETAIL = "Сущность не найдена"
        ...     _CODE = status.HTTP_404_NOT_FOUND
    """

    _DETAIL: str
    _CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str | None = None, status_code: int | None = None, headers: DictOrNone = None) -> None:
        """
        Инициализация исключения

        Args:
            detail (str | None): сообщение
            status_code (int | None): код статуса
            headers (dict | None): заголовки
        """
        super().__init__(status_code or self._CODE, detail or self._DETAIL, headers)
        logger.exception("Исключение DH: %s [%d]", (detail or self._DETAIL), (status_code or self._CODE))
