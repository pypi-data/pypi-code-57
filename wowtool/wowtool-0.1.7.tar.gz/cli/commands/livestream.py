import json
import click
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
    """Get data for a Live Stream"""
    wowza_auth()
    response = Livestream.get_livestream(id)
    click.echo(json.dumps(response, indent=4))

@live.command(name='start')
@click.option('--id', required=True, help='Live stream id')
@exception_handler
def start(id):
    """Start a Live Stream"""
    wowza_auth()
    Livestream.start_livestream(id)
    click.echo('Live Stream started')

@live.command(name='stop')
@click.option('--id', required=True, help='Live stream id')
@exception_handler
def stop(id):
    """Stop a Live Stream"""
    wowza_auth()
    Livestream.stop_livestream(id)
    click.echo('Live Stream stopped')

@live.command(name='state')
@click.option('--id', required=True, help='Live stream id')
@exception_handler
def state(id):
    """Get state for a Live Stream"""
    wowza_auth()
    state = Livestream.get_state(id)
    click.echo('Live Stream state is {0}'.format(state))
