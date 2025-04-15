from logging.config import dictConfig

from config import config


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if config.ENV == "dev" else 32,
                    "default_value": "-",
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "dateftm": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "dateftm": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | [%(correlation_id)s] %(name)s:%(lineno)d - %(message)s",
                },
                "file_json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "dateftm": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file_json",
                    "filename": "records.log",
                    "maxBytes": 1024 * 1024,  # 1MB
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id"],
                },
            },
            "loggers": {
                "waitress": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "gunicorn": {
                    "handlers": ["default", "rotating_file"],
                    "level": "WARNING",
                },
                "sqlalchemy": {
                    "handlers": ["default", "rotating_file"],
                    "level": "WARNING",
                },
                "chatbot": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if config.ENV == "dev" else "INFO",
                    "propagate": False,
                },
            },
        }
    )
