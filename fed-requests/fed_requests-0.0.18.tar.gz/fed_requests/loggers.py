import sys
import os
import logging

from .settings import TEMP_DIR


class Logger:
    def __init__(self, name=None, path=None):
        name = __name__ if not name else name
        path = TEMP_DIR if not path else path

        self.logger = logging.getLogger(name)
        self.file_path = os.path.join(path, f'{name}.log')

        self._setup_logger()

    def _setup_logger(self):
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add File Handler
        file_handler = logging.FileHandler(self.file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Add sysout handler (prints to console)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def __str__(self):
        return f'Logger object. Log file: {self.file_path}'

