import os
import sys

import click

from roboself.client import Client
from roboself.config import RawConfig
from roboself.runtime import Runtime


def _get_runtime():
    """Helper to initialise the skill runtime"""
    click.echo("Loading configuration ...")

    # TODO: fetch the skill name from env
    raw_config = RawConfig(name="noname")
    raw_config.load()

    click.echo("Connecting to the roboself runtime ...")
    # TODO: fetch the API Key from env
    api_key = os.environ.get("ROBOSELF_API_KEY")
    if not api_key:
        print("No environment ROBOSELF_API_KEY variable found ")
        exit(1)
        return

    client = Client(api_key)
    runtime = Runtime(client=client, raw_config=raw_config)

    return runtime


@click.command()
def run():
    """Runs the current skill.

    Loads the local configuration and sends it to the runtime. Then it waits for calls
    to execute actions.
    """
    runtime = _get_runtime()

    click.echo("Connecting the skill runtime ...")
    runtime.connect()

    click.echo("Waiting for action requests ...")


@click.command()
def train():
    """Trains the model for the current skill.

    Loads the local configuration and sends it to the runtime.
    Then it starts the training.
    """

    runtime = _get_runtime()

    click.echo("Connecting the skill runtime ...")
    runtime.connect()

    click.echo("Sending training request ...")
    runtime.train()

    click.echo("Quitting")
