import json
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from wowpy.livestreams import LiveStream
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
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def query(id, name):
    """Get data for a Live Stream"""
    wowza_auth()
    response = LiveStream.get_live_stream(id)
    click.echo(json.dumps(response, indent=4))

@live.command(name='start')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def start(id, name):
    """Start a Live Stream"""
    wowza_auth()
    LiveStream.start_live_stream(id)
    click.echo('Live Stream started')

@live.command(name='stop')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def stop(id, name):
    """Stop a Live Stream"""
    wowza_auth()
    LiveStream.stop_live_stream(id)
    click.echo('Live Stream stopped')

@live.command(name='state')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def state(id, name):
    """Get state for a Live Stream"""
    wowza_auth()
    state = LiveStream.get_state(id)
    click.echo('Live Stream state is {0}'.format(state))
