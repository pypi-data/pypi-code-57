import click
import click_completion
import requests

from tktl.cli import common
from tktl.cli.auth import logout, login, save_api_key
from tktl.cli.deployments import deployments
from tktl.cli.init import init
from tktl.cli.validate import validate
from tktl.commands.version import get_version
from tktl.core.config import settings
from tktl.core.exceptions import TaktileSdkError, ApplicationError
from tktl.core.loggers import CliLogger

click_completion.init()


class TaktileGroup(common.ClickGroup):
    def main(self, *args, **kwargs):
        try:
            super(TaktileGroup, self).main(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            msg = (
                "Can't connect to Taktile API. "
                "Please check https://status.tktl.io/ for more information."
            )
            CliLogger().error(msg)
        except (ApplicationError, TaktileSdkError) as e:
            if settings.DEBUG:
                raise

            CliLogger().error(e)


@click.group(cls=TaktileGroup, **settings.HELP_COLORS_DICT)
def cli():
    pass


cli.add_command(get_version)
cli.add_command(logout)
cli.add_command(login)
cli.add_command(save_api_key)
cli.add_command(init)
cli.add_command(deployments)
cli.add_command(validate)
