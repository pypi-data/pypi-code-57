import click

from roboself.client import Client
from roboself.config import RawConfig
from roboself.runtime import Runtime


@click.command()
def run():
    """Runs the current skill.

    Loads the local configuration and sends it to the runtime. Then it waits for calls
    to execute actions.
    """
    click.echo("Loading configuration ...")

    # TODO: fetch the skill name from env
    raw_config = RawConfig(name="noname")
    raw_config.load()

    click.echo("Connecting to the roboself runtime ...")
    # TODO: fetch the API Key from env
    client = Client("NgsfFzGfWUdYJQi2beuYcgDe")
    runtime = Runtime(client=client, raw_config=raw_config)

    click.echo("Connecting the skill runtime ...")
    runtime.connect()

    click.echo("Waiting for action requests ...")

