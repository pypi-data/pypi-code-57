#!/usr/bin/env python3
# coding: utf-8

import sys
import loguru
from b_i.config.setting import LOG_INFO

class logHandle(object):

    '''
    Super performance： opt to reload logging, logger.opt.debug.
    '''

    def __init__(self):
        self.logger = loguru.logger
        self._format = '{{"time":<green>"{time:YYYY-MM-DD HH:mm:ss}"</green>,"level":<level>"{level}"</level>,"pos":<cyan>"{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}"</cyan>,"msg":<level>"{message}"</level>}}'
        self._level = LOG_INFO.get("LEVEL")
        self._path = LOG_INFO.get("PATH")
        self._console = {
            'sink': sys.stderr,
            'format': self._format,
            'level': self._level
        }
        self._file = {
            'sink': self._path,
            'format': self._format,
            'level': self._level,
            'rotation': "128 MB",
            "compression": "tar.gz",
            "enqueue": False,
            "encoding": "utf-8"
        }
        if self._level == "DEBUG":
            self.logger.configure(handlers=[self._console, self._file])
        else:
            self.logger.configure(handlers=[self._file])

    def setLevel(self, level="INFO"):
        '''
        custom logger level by yourself, recommend: info
        :param level: "INFO", "ERROR", "WARNING", "DEBUG", "SUCCESS"
        :return:
        '''
        if self._level is not level:
            self._level = level
            self._console["level"] = self._level
            self._file["level"] = self._level
            self.logger.configure(handlers=[self._console, self._file])

    def setPath(self, path=LOG_INFO.get("PATH")):
        '''
        custom path by yourself, linux recommend: /var/log/
        :param path: custom log path.
        :return:
        '''
        if self._path is not path:
            self._path = path
            self._file["sink"] = self._path
            self.logger.configure(handlers=[self._console, self._file])

    def info(self, *args, **kwargs):
        '''
        this is logger info level, compatible
        :param args:
        :param kwargs:
        :return:
        '''
        self.logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        '''
        this is logger error level, compatible
        :param args:
        :param kwargs:
        :return:
        '''
        self.logger.error(*args, **kwargs)

    def debug(self, *args, **kwargs):
        '''
        this is logger debug level, compatible
        :param args:
        :param kwargs:
        :return:
        '''
        self.logger.debug(*args, **kwargs)

    def warning(self, *args, **kwargs):
        '''
        this is logger warning level, compatible
        :param args:
        :param kwargs:
        :return:
        '''
        self.logger.warning(*args, **kwargs)

    def success(self, *args, **kwargs):
        '''
        this is logger success level, compatible
        :param args:
        :param kwargs:
        :return:
        '''
        self.logger.success(*args, **kwargs)

    @property
    def catch(self):
        '''
        Return a decorator to automatically log possibly caught error in wrapped function.
        catch Exception , then must throw raise
        beta, 20190815
        :return:
        '''
        return self.logger.catch(reraise=True)

if __name__ == "__main__":
    pass