"""Константы модуля"""

__author__: str = "Старков Е.П."

# Конфиг логера
LOG_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "dh_platform.logging.CustomJsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "rename_fields": {"levelname": "level", "asctime": "timestamp"},
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "json_ensure_ascii": False,
        },
        "simple": {"format": "%(levelname)-8s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple", "level": "INFO"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "dh_logger": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
