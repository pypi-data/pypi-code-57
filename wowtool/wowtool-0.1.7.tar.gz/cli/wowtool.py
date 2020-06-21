import click
from cli.__version__ import VERSION
from cli.commands.livestream import live
from cli.commands.transcoder import trans
from cli.commands.configure import configure


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass

cli.add_command(live)
cli.add_command(configure)
cli.add_command(trans)