#  © Copyright IBM Corporation 2020.

import logging
import sys
import traceback
import datetime
import json


class CPDStatusHandler:
    _instance = None
    logger = None
    log_source = None
    start_ts = None
    path = None
    operation = None

    def __new__(cls, path, op="export"):
        if cls._instance is None:
            cls._instance = super(CPDStatusHandler, cls).__new__(cls)
            cls.logger = cls.get_logger(path=path, op=op, logger_name=None)
            cls.log_source = None
            cls.start_ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
            cls.path = path
            cls.operation = op
        return cls._instance

    @staticmethod
    def get_logger(path, op, logger_name=None):
        """
        Retrieve logger object

        :param logger_name: Name of the logger
        :return: Logger object
        """
        logger = None
        try:
            file_handler = logging.FileHandler('{}/{}-status.json'.format(path, op))
            file_formatter = logging.Formatter("%(message)s")
            file_handler.setFormatter(file_formatter)

            if logger_name is None:
                logger_name = "__cpdtool logger__"
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.handlers = [file_handler]
        except:
            print(sys.exc_info()[0])
            pass
        return logger

    @staticmethod
    def msg_to_log(attributes, msg):
        """
        Covert message to proper log string

        :param attributes: Attributes of log line
        :param msg: Log message
        :return: Formatted log string
        """

        if "completion_ts" in attributes:
            message = dict(
                startTime=attributes['start_ts'],
                completionTime=attributes['completion_ts'],
                status=attributes['status'],
                message=msg,
                percentageCompleted=attributes['completed_percent']
            )
            return json.dumps(message)
        else:
            message = dict(
                startTime=attributes['start_ts'],
                status=attributes['status'],
                message=msg,
                percentageCompleted=attributes['completed_percent']
            )
            return json.dumps(message)

    @classmethod
    def log_status(cls, msg, status="running", percentage=0, completed=False):
        """
        Log status message

        :param msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on INFO level
        """
        attributes = dict(
            start_ts=cls.start_ts,
            status=status,
            message=msg,
            completed_percent=percentage
        )
        if completed:
            completion_ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
            attributes['completion_ts'] = completion_ts
        open('{}/{}-status.json'.format(cls.path, cls.operation), 'w').close()
        cls.logger.info(cls.msg_to_log(attributes, msg))
