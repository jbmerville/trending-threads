from datetime import datetime
import logging

LOGGING_LEVEL = logging.INFO

# Format the current date and time to the filename
current_time = datetime.now().strftime("%Y-%m-%d_%H")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {  # root logger
            "level": LOGGING_LEVEL,
            "handlers": ["console"],
        },
    },
}


class TrendLoggingAdapter(logging.LoggerAdapter):
    def __init__(self, logger, trend_name):
        super().__init__(logger, {})
        self.trend_name = trend_name

    def process(self, msg, kwargs):
        return f"Thread '{self.trend_name}': {msg}", kwargs


def get_thread_logger(trend_name, logger_name="my_logger"):
    logger = logging.getLogger(logger_name)
    return TrendLoggingAdapter(logger, trend_name)
