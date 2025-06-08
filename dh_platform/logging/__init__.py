"""Пакет для логирования"""

__author__: str = "Старков Е.П."

from .formatter import CustomJsonFormatter
from .middleware import log_requests
from .setup import setup_logging
