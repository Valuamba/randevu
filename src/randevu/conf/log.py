import logging
import os
from django.utils.log import DEFAULT_LOGGING

from randevu.conf.boilerplate import BASE_DIR


# log_path = os.path.join(BASE_DIR, 'logs')
# isExist = os.path.exists(log_path)
# if not isExist:
#     os.makedirs(log_path)


logger = logging.getLogger(__name__)

LOG_LEVEL = "INFO"

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        },
        # "file": {
        #     "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        # },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"]
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console"
        },
        # "file": {
        #     "level": "INFO",
        #     "class": "logging.handlers.TimedRotatingFileHandler",
        #     "formatter": "file",
        #     "filename": os.path.join(BASE_DIR, "logs/randevu-admin.log"),
        #     'when': 'midnight',
        #     'backupCount': 10,
        # },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"]
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": [
                "console",
                # "file"
            ],
            "propagate": False
        },
        "apps": {
            "level": "INFO",
            "handlers": [
                "console"
            ],
            "propagate": False
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"]
    }
})
