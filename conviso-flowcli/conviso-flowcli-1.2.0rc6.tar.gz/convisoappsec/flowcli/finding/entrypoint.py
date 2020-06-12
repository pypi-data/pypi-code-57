import click

from convisoappsec.flowcli import help_option
from .create import create

@click.group()
@help_option
def finding():
    pass


finding.add_command(create)
