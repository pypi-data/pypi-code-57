import json
import logging.config, logging
import os


class RFUtilsLogger:

    @staticmethod
    def init_log(json_config: str = None):
        """
        Method for init log
        :param json_config:
        :return:
        """
        if json_config is None:
            json_config = {
                "version": 1,
                "formatters": {
                    "default": {
                        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                        "formatter": "default",
                        "level": "DEBUG"
                    }
                },
                "loggers": {
                    "console": {
                        "level": "DEBUG",
                        "handlers": [
                            "console"
                        ],
                        "propagate": "no"
                    }
                },
                "root": {
                    "level": "DEBUG",
                    "handlers": [
                        "console"
                    ]
                }
            }
        logging.config.dictConfig(json_config)

    @staticmethod
    def error(msg: str, *args, **kwargs):
        """
        Method to send error log
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        logging.error(msg, *args, **kwargs)

    @staticmethod
    def debug(msg: str, *args, **kwargs):
        """
        Method to send debug message
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        logging.debug(msg, *args, **kwargs)
