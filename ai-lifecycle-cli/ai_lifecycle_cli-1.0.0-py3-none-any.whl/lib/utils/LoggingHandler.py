#  © Copyright IBM Corporation 2020.

import logging
import sys
import traceback
import datetime


class LoggingHandler:

    def __init__(self):
        self.logger = self.get_logger()
        self.log_source = None

    @staticmethod
    def get_logger(logger_name=None):
        """
        Retrieve logger object

        :param logger_name: Name of the logger
        :return: Logger object
        """
        logger = None
        try:
            stream_handler = logging.StreamHandler()
            stream_formatter = logging.Formatter("%(message)s")
            stream_handler.setFormatter(stream_formatter)

            if logger_name is None:
                logger_name = "__AI_Lifecycle_CLI__"
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.handlers = [stream_handler]
        except:
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
        if not attributes.get("exception"):
            return "{ts} {level:10} - {msg}"\
                .format(ts=attributes['timestamp'],
                        level='[' + attributes['log_level'] + ']',
                        msg=msg)
        else:
            return "{ts} {level:10} - {msg} \n {ex}" \
                .format(ts=attributes['timestamp'],
                        level='[' + attributes['log_level'] + ']',
                        msg=msg,
                        ex=attributes["exception"])

    @staticmethod
    def get_logging_attributes(level, **kwargs):
        """
        Set attributes for log formatting

        :param level: Desired level format of the log
        :param kwargs: Keyword arguments
        :return: Dict of log format attributes
        """
        attributes = dict(
            log_level=level,
            timestamp=datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        )
        for key, val in kwargs.items():
            attributes[key] = val
        return attributes

    def log_info(self, msg, **kwargs):
        """
        Log message on INFO level

        :param msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on INFO level
        """
        attributes = self.get_logging_attributes("INFO", **kwargs)
        attributes["message_details"] = msg
        self.logger.info(self.msg_to_log(attributes, msg))

    def log_error(self, err_msg, **kwargs):
        """
        Log message on ERROR level

        :param err_msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on ERROR level
        """
        attributes = self.get_logging_attributes("ERROR", **kwargs)
        attributes["message_details"] = err_msg
        self.logger.error(self.msg_to_log(attributes, err_msg))

    def log_exception(self, exc_msg, **kwargs):
        """
        Log exception with message on ERROR level

        :param exc_msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged exception with message on ERROR level
        """
        attributes = self.get_logging_attributes("ERROR", **kwargs)
        attributes["message_details"] = exc_msg
        exc_info = kwargs.get("exc_info", False)
        if exc_info is True:
            type_, value_, traceback_ = sys.exc_info()
            attributes["exception"] = "".join(traceback.format_exception(
                type_, value_, traceback_))
        self.logger.error(self.msg_to_log(attributes, exc_msg))

    def log_warning(self, msg, **kwargs):
        """
        Log message on WARNING level

        :param msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on WARNING level
        """
        attributes = self.get_logging_attributes("WARNING", **kwargs)
        attributes["message_details"] = msg
        exc_info = kwargs.get("exc_info", False)
        if exc_info is True:
            type_, value_, traceback_ = sys.exc_info()
            attributes["exception"] = "".join(traceback.format_exception(
                type_, value_, traceback_))
        self.logger.warning(self.msg_to_log(attributes, msg))

    def log_debug(self, msg, **kwargs):
        """
        Log message on DEBUG level

        :param msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on DEBUG level
        """
        attributes = self.get_logging_attributes("DEBUG", **kwargs)
        attributes["message_details"] = msg
        self.logger.debug(self.msg_to_log(attributes, msg))

    def log_critical(self, msg, **kwargs):
        """
        Log message on CRITICAL level

        :param msg: Message to log
        :param kwargs: Keyword arguments
        :return: Logged message on CRITICAL level
        """
        attributes = self.get_logging_attributes("CRITICAL", **kwargs)
        attributes["message_details"] = msg
        self.logger.critical(self.msg_to_log(attributes, msg))
