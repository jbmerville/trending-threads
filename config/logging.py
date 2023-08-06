import logging
import os

LOGGING_LEVEL = logging.INFO
LOGS_DIR = 'logs/'

# Check if the logs directory exists or not, if not create one
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'app.log'),  # log filename
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
    }
}
