import os
import asyncio
from pathlib import Path
from datetime import datetime, timezone
from basic_logtools.filelog import LogFile



class GeneralData:

    def __init__(self, *args, **kwargs):
        self.session = None
        self.address = kwargs.get('address')  # (host,port)
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 28015)
        if self.address in {'', None, False}:
            self.address = (self.host, self.port)
        self.code = kwargs.get('code', 'NONE')
        self.hostname = kwargs.get('hostname', 'atlas')
        log_path = kwargs.get('log_path','~/data_log')
        log_level = kwargs.get('log_level', 'INFO')
        self.logger = LogFile(self.class_name,
                              self.code,
                              self.hostname,
                              path=log_path,
                              base_level=log_level)

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def log_filename(self):
        return "%s_%s_%s_%s.log" % (self.class_name, self.hostname, self.code, self.init_datetime)

    @property
    def log_filepath(self):
        return './logs/%s' % self.log_filename

    def save_log(self, msg, level):
        digit2level = {
            0: "LOG",
            10: "DEBUG",
            20: "INFO",
            30: "WARNING",
            40: "ERROR",
            50: "CRITICAL"
        }
        if type(level) == int:
            if level in digit2level:
                level = digit2level[level]
            else:
                level = digit2level[0]
        levels = dict(
            LOG=self.logger.log,
            DEBUG=self.logger.debug,
            INFO=self.logger.info,
            WARNING=self.logger.warning,
            ERROR=self.logger.error,
            CRITICAL=self.logger.critical)
        if level in levels:
            logfn = levels[level]
        else:
            logfn = levels['INFO']
        logfn(msg)

    def manage_data(self, data):
        # print(data)
        return data

    def connect(self, *args, **kwargs):
        pass

    async def async_connect(self, value):
        return None

    def set_source(self, value, *args, **kwargs):
        """
        Define source where data is saved
        """
        pass

    def save_data(self, data, is_header, *args, **kwargs):
        """
        Save data on place
        """
        # print(data)
        pass

    def check_data(self, *args, **kwargs):
        """
        load data from buffer
        """
        pass

    def show_data(self, time, columns, *args, **kwargs):
        """
        Select data filtered by time and columns
        """
        pass

    def show_info(self, *args, **kwargs):
        """
        Show info from settings [source, logs, etc]
        """
        pass

    def plot(self, data, dtype, *args, **kwargs):
        """
        Plot data in a dtype type
        """
        print("No plot fn yet defined")
        pass

    def get_data(self, delta, *args, **kwargs):
        pass

    def stop(self):
        pass
