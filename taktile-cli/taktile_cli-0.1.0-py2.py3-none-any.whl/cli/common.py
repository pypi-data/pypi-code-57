import functools
import re

import click
import termcolor
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from tktl.core.config import settings

OPTIONS_FILE_OPTION_NAME = "optionsFile"
OPTIONS_FILE_PARAMETER_NAME = "options_file"
OPTIONS_DUMP_FILE_OPTION_NAME = "createOptionsFile"


class ClickGroup(DYMMixin, HelpColorsGroup):
    pass


def deprecated(msg):
    deprecated_invoke_notice = (
        msg
        + """\nFor more information, please see:

https://docs.taktile.com
If you depend on functionality not listed there, please file an issue."""
    )

    def new_invoke(self, ctx):
        click.echo(click.style(deprecated_invoke_notice, fg="red"), err=True)
        super(type(self), self).invoke(ctx)

    def decorator(f):
        f.invoke = functools.partial(new_invoke, f)

    return decorator


class ColorExtrasInCommandHelpMixin(object):  # noqa
    def get_help_record(self, *args, **kwargs):
        rv = super(ColorExtrasInCommandHelpMixin, self).get_help_record(*args, **kwargs)
        if not settings.USE_CONSOLE_COLORS:
            return rv

        try:
            help_str = rv[1]
        except (IndexError, TypeError):
            return rv

        if help_str:  # noqa
            help_str = self._color_extras(help_str)
            rv = rv[0], help_str
        return rv

    def _color_extras(self, s):
        pattern = re.compile(r"^.*(\[.*\])$")
        found = re.findall(pattern, s)
        if found:
            extras_str = found[-1]
            coloured_extras_str = self._color_str(extras_str)
            s = s.replace(extras_str, coloured_extras_str)

        return s

    def _color_str(self, s):
        s = termcolor.colored(s, settings.HELP_HEADERS_COLOR)
        return s
