#-*- encoding: utf8 -*-
import os
import logging
import getpass

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


logging.getLogger("requests.packages.urllib3").propagate = 0


def get_logger(name=None, format='[%(asctime)s %(funcName)s %(levelname)s] %(message)s', verbose=False):
    logging.basicConfig(
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
        
    logger = logging.getLogger(name)

    if verbose:
        logger.level = logging.DEBUG

    return logger


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
