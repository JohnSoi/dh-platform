"""Модуль для форматтера логирования"""

__author__: str = "Старков Е.П."

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    """Кастомный форматтер. Предназначен для правильной интерпретации русского языка"""

    def process_log_record(self, log_record):
        # Преобразуем все строки в UTF-8
        for key, value in log_record.items():
            if isinstance(value, str):
                log_record[key] = value.encode("utf-8").decode("utf-8")
        return super().process_log_record(log_record)
