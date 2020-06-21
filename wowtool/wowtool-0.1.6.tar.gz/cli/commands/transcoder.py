import json
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from wowpy.transcoders import Transcoder
from cli.utils import exception_handler, wowza_auth

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def trans():
    """
    Transcoder commands.
    """
    pass


@trans.command(name='query')
@click.option('--id', required=True, help='Transcoder id.')
@exception_handler
def query(id):
    """Get data for a Transcoder"""
    wowza_auth()
    response = Transcoder.get_transcoder(id)
    click.echo(json.dumps(response, indent=4))

@trans.command(name='start')
@optgroup.group('Transcoder identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza transcoder')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def start(id, name):
    """Start a Transcoder"""
    print(id, name)