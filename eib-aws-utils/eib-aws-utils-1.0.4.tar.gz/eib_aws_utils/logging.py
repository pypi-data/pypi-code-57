"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging
import logging.config
import os
from uuid import uuid4

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    context = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._context_id = None

    def _get_context_id(self):
        if self._context_id is None:
            if self.context and hasattr(self.context, 'aws_request_id'):
                self._context_id = self.context.aws_request_id
            else:
                self._context_id = str(uuid4())

        return self._context_id

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['aws_request_id'] = self._get_context_id()


def configure_logging(main_module_name, context):
    """
    Configure the standard logging package to use JSON format.
    It also add the aws_request_id to the log fields.
    And use the LOGGING_LEVEL environment variable to define the logging level for the main_module_name package.

    :param main_module_name: the main package name
    :type main_module_name: str
    :param context: the aws context of the lambda
    :type context: object
    """
    logging.config.dictConfig(_get_default_logging_config(main_module_name))
    CustomJsonFormatter.context = context


def _get_default_logging_config(main_module_name):
    return {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'DEBUG'
            },
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)s %(levelname)s %(lineno)s %(module)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z',
                'class': 'eib_aws_utils.logging.CustomJsonFormatter'
            }
        },
        'disable_existing_loggers': False,
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'loggers': {
            main_module_name: {
                'level': os.getenv('LOGGING_LEVEL', 'INFO')
            }
        }
    }
