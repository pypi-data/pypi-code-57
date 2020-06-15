import logging
import logging.config

default_logging_dict = \
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "{app_name} %(levelname)9s %(asctime)3s Module: %(module)s - Line: %(lineno)s %(message)s"
            }
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "errors": {
                "level": "ERROR",
                "formatter": "default",
                "class": "logging.StreamHandler"
            }
        },
        "loggers": {
            "default": {
                "handlers": [
                    "default"
                ],
                "level": "INFO",
                "propagate": "no"
            }
        }
    }


class Client:

    def __init__(self, app_name):
        self._logger = self._load_logger(app_name)

    @property
    def logger(self):
        return self._logger

    @staticmethod
    def _load_logger(app_name):
        formatter = default_logging_dict['formatters']['default']['format']
        default_logging_dict['formatters']['default']['format'] = formatter.format(app_name=app_name)
        logging.config.dictConfig(default_logging_dict)
        return logging.getLogger('default')

