import click
from cli.__version__ import VERSION
from cli.commands.live import live


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass


# breakpoint()
cli.add_command(live)