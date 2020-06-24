import logging
from colorlog import ColoredFormatter
from logging import Formatter


class Loggers(object):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self):
        self.__file_handler = None
        self.__console_handler = None
        self.__logger_map = {}
        self.__level = logging.DEBUG

    def __init(self, log_file_name: str) -> None:
        color_formatter = ColoredFormatter(
            "%(purple)s%(asctime)s%(reset)s\
 - %(log_color)s%(levelname)-8s%(reset)s\
 - %(white)s%(name)s[%(lineno)s]%(reset)s - %(white)s%(message)s%(reset)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        normal_formatter = Formatter(
            "%(asctime)s - %(levelname)-8s[%(lineno)s] \
- %(name)s - %(message)s")

        # 创建一个handler，用于写入日志文件
        if log_file_name:
            self.__file_handler = logging.FileHandler(log_file_name)
            self.__file_handler.setFormatter(normal_formatter)

        # 再创建一个handler，用于输出到控制台
        self.__console_handler = logging.StreamHandler()
        self.__console_handler.setFormatter(color_formatter)

    def set_level(self, level: int) -> None:
        for logger in self.__logger_map.values():
            logger.setLevel(level)
        self.__level = level

    def get(self, logger_name: str, use_file: bool = False) -> logging.Logger:
        if not self.__console_handler:
            self.__init(f"DobotRpc-{logger_name}.log" if use_file else None)
            # raise Exception("Logger had not inited.")

        logger = self.__logger_map.get(logger_name, None)

        if logger is None:
            logger = logging.getLogger(logger_name)
            # 给logger添加handler
            if self.__file_handler:
                logger.addHandler(self.__file_handler)
            logger.addHandler(self.__console_handler)
            logger.setLevel(self.__level)
            self.__logger_map[logger_name] = logger

        return logger
