import click
from cli.__version__ import VERSION
from cli.commands.live import live
from cli.commands.configure import configure


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass

cli.add_command(live)
cli.add_command(configure)