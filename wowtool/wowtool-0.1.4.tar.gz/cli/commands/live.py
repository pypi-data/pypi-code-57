import click
import json
from wowpy.livestreams import Livestream
from cli.utils import exception_handler, wowza_auth

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def live():
    """
    Live Stream commands.
    """
    pass


@live.command(name='query')
@click.option('--id', required=True, help='Live Stream id.')
@exception_handler
def query(id):
    """Get data for a Livestream"""
    wowza_auth()
    response = Livestream.get_livestream(id)
    click.echo(json.dumps(response, indent=4))
