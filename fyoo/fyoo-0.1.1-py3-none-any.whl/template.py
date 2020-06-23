import datetime
import os
import pytz

from jinja2.environment import Environment
from jinja2.ext import Extension

from fyoo.exception import FyooTemplateException


class FyooDatetimeExtension(Extension):

    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.globals['date'] = self.date
        environment.globals['dt'] = self.dt
        environment.globals['raw_datetime'] = datetime.datetime

    def parse(self, parser):
        pass

    @classmethod
    def date(cls, tz='UTC', fmt: str = r'%Y-%m-%d') -> str:
        """Get current time string

        Args:
            tz (str, optional): Timezone to use. Defaults to 'UTC'.
            fmt (str, optional): Datetime format. Defaults to r'%Y-%m-%d'.

        Returns:
            str: Formated datetime string
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
        """Same as ``os.getenv``
        """
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

        You would do this if you wanted to verify arguments
        at 'compile-time', before executing a subcommand.

        """
        raise FyooTemplateException(*args, **kwargs)
