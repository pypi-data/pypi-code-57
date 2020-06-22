import datetime
import os
import pytz

from jinja2.environment import Environment
from jinja2.ext import Extension

from fyoo.exception import FyooTemplateException


class FyooDatetimeExtension(Extension):
    """
    Add a few functions or arguments to the global variables.
    """

    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.globals['date'] = self.date
        environment.globals['dt'] = self.dt
        environment.globals['raw_datetime'] = datetime.datetime

    def parse(self, parser):
        pass

    @classmethod
    def date(cls, tz='UTC', fmt=r'%Y-%m-%d') -> str:
        """Print now with specified timezone and format
        """
        return datetime.datetime.now(tz=pytz.timezone(tz)).strftime(fmt)

    @classmethod
    def dt(cls, *args, **kwargs) -> str:
        """Same as date()
        """
        return cls.date(*args, **kwargs)


class FyooEnvExtension(Extension):

    """
    Provide environment variable global functions
    """

    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.globals['getenv'] = self.getenv

    def parse(self, parser):
        pass

    @classmethod
    def getenv(cls, *args, **kwargs):
        return os.getenv(*args, **kwargs)


class FyooThrowExtension(Extension):

    """
    Provide ability to raise exceptions from within a template.
    """

    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.globals['throw'] = self.throw

    def parse(self, parser):
        pass

    @classmethod
    def throw(cls, *args, **kwargs):
        """Raise a FyooTemplateException
        """
        raise FyooTemplateException(*args, **kwargs)
