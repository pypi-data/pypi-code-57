#-*- encoding: utf8 -*-
import os
import sys
import logging
import getpass

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


logging.getLogger("requests.packages.urllib3").propagate = 0


class User(object):
    def __init__(self, section='cms', username=None, password=None, configfile=None, **kwargs):
        self.username = username
        self.password = password
        self.configfile = configfile
        self.section = section
        self.conf = ConfigParser()

    def get_user_pass(self):

        if self.configfile:
            self.conf.read(self.configfile)

        if self.username and self.password:
            username, password = self.username, self.password
        elif self.configfile and os.path.exists(self.configfile):
            username, password = self.read()
        else:
            username, password = None, None

        if not all([username, password]):
            print('Please input your username and password [{}]'.format(self.section))
            username = raw_input('> username: ')
            password = getpass.getpass('> password: ')

        return username, password

    def read(self):
        username = password = None

        if self.conf.has_section(self.section):
            if self.username:
                if self.conf.has_option(self.section, self.username):
                    username = self.username
                    password = self.conf.get(self.section, self.username)
            elif len(self.conf.options(self.section)) == 1:
                username = self.conf.options(self.section)[0]
                password = self.conf.get(self.section, username)

        return username, password

    def save(self, username, password):
        if not self.conf.has_section(self.section):
            self.conf.add_section(self.section)
        self.conf.set(self.section, username, password)

        with open(self.configfile, 'w') as out:
            self.conf.write(out)


class MyLogger(logging.Logger):
    def __init__(self,
                 name=None,
                 level=logging.INFO,
                 fmt=None,
                 datefmt=None,
                 logfile=None,
                 filemode='w',
                 stream=sys.stderr,
                 verbose=True,
                 colored=False,
                 **kwargs):

        if verbose:
            level = logging.DEBUG

        super(MyLogger, self).__init__(name, level)

        self.fmt = fmt or '[%(asctime)s %(funcName)s %(levelname)s %(threadName)s] %(message)s'
        self.datefmt = datefmt or '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter(self.fmt, self.datefmt)

        if logfile:
            self._addFilehandler(logfile, filemode)
        else:
            self._addStreamHandler(stream)
            if colored:
                import coloredlogs
                coloredlogs.install(fmt=self.fmt, level=level, logger=self)

    def _addFilehandler(self, filename, filemode):

        file_hdlr = logging.FileHandler(filename, filemode)
        file_hdlr.setFormatter(self.formatter)
        self.addHandler(file_hdlr)

    def _addStreamHandler(self, stream):

        stream_hdlr = logging.StreamHandler(stream)
        stream_hdlr.setFormatter(self.formatter)
        self.addHandler(stream_hdlr)


if __name__ == '__main__':

    # logger = MyLogger(colored=False)
    logger = MyLogger(name='TEST1')
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')

    logger2 = MyLogger(name='TEST2', colored=False, logfile='out.log')
    logger2.warn('warn message')
    logger2.warn('warn message')
