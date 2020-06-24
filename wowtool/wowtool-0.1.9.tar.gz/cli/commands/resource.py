import json
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from wowpy.resources import get_resource_info
from cli.utils import exception_handler, wowza_auth

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def resource():
    """
    Resource commands.
    """
    pass


@resource.command(name='query')
@optgroup.group('Resource identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for resource')
@optgroup.option('--id', help='Resource id')
@optgroup.option('--name', help='Resource name')
@exception_handler
def query(id, name):
    """Get data for resource"""
    wowza_auth()
    response = get_resource_info(id)
    click.echo(json.dumps(response, indent=4))