import logging
import os
from datetime import datetime
import re

LOGGING_LEVEL = logging.INFO
LOGS_DIR = "logs/"

# Check if the logs directory exists or not, if not create one
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Format the current date and time to the filename
current_time = datetime.now().strftime("%Y-%m-%d_%H")
log_filename = f"app_{current_time}.log"

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(message)s"},
    },
    "handlers": {
        "file": {
            "level": LOGGING_LEVEL,
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, log_filename),  # log filename
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
    },
}


class TrendLoggingAdapter(logging.LoggerAdapter):
    def __init__(self, logger, trend_name):
        super().__init__(logger, {})
        self.trend_name = trend_name

    def process(self, msg, kwargs):
        msg = clean_text(msg)
        return f"Trend '{self.trend_name}': {msg}", kwargs


def get_trend_logger(trend_name, logger_name="my_logger"):
    logger = logging.getLogger(logger_name)
    return TrendLoggingAdapter(logger, trend_name)


def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text
