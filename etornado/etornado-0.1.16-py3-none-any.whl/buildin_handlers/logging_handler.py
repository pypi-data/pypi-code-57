import json
import logging
from etornado.error_code_manager import ErrorCode
from etornado.buildin_handlers.base_handler import BaseHandler
from etornado.error_code_manager import ErrorCode


class LoggingHandler(BaseHandler):
    NAME = "name"
    LEVEL = "level"
    NAME_TO_LEVEL = {
        "NOTSET": logging.NOTSET,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    LEVEL_TO_NAME = None
    UNKNOWN = "UNKNOWN"

    def do_get(self):
        if LoggingHandler.LEVEL_TO_NAME is None:
            LoggingHandler.LEVEL_TO_NAME = \
                {v: k for k, v in LoggingHandler.NAME_TO_LEVEL.items()}
        logger = logging.getLogger(self.url_args[0])
        level = LoggingHandler.LEVEL_TO_NAME.get(logger.level)
        if level is None:
            level = self.UNKNOWN
        return level

    def do_post(self):
        data = json.loads(self.request.body)
        name = self.url_args[0]
        level_name = data.get(self.LEVEL)
        if level_name is None:
            return ErrorCode.LACK_OF_FIELD, {"field": self.LEVEL}
        level = self.NAME_TO_LEVEL.get(level_name.upper())
        if level is None:
            return ErrorCode.UNSUPPORTED_LOGGING_LEVEL, {"level": level_name}
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return ErrorCode.NONE, "success"
