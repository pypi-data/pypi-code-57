import click
import json
import os
from pathlib import Path
from time import sleep
from wowpy.livestreams import Livestream
from cli.utils import exception_handler

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.yml
"""


@click.group()
def live():
    """
    Livestream commands.
    """
    pass


@live.command(name='query')
@click.option('--id', required=True, help='Livestream id.')
@exception_handler
def query(id):
    """Get data for a Livestream"""

    # Load wowza api keys
    home_path = str(Path.home())
    credentials_path = home_path + '/.wow/credentials.json'
    if os.path.exists(credentials_path):
        with open(credentials_path) as json_file:
            credentials_data = json.load(json_file)
            os.environ["WSC_ACCESS_KEY"] = credentials_data['WSC_ACCESS_KEY']
            os.environ["WSC_API_KEY"] = credentials_data['WSC_API_KEY']

    response = Livestream.get_livestream(id)
    click.echo(json.dumps(response))
