from omnipack import __version__
import click
from .aliased_group import AliasedGroup

from .os import (kill_multiprocess, kill_port, kill_process,
                 get_host, get_hostname, is_port_available)
from .fileio import csv2tsv, tsv2csv

__all__ = ['cli']

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help='Powerpack')
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(kill_multiprocess)
cli.add_command(kill_port)
cli.add_command(kill_process)
cli.add_command(get_host)
cli.add_command(get_hostname)
cli.add_command(is_port_available)
cli.add_command(csv2tsv)
cli.add_command(tsv2csv)

if __name__ == '__main__':
    cli()
