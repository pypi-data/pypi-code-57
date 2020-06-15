import logging

import click

from .commands.init import init
from .commands.run import run as run_skill


@click.group()
def main():
    pass


def run():
    main.add_command(init)
    main.add_command(run_skill)

    logging.getLogger().setLevel(logging.INFO)
    main()
