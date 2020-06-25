import logging

import click

from .commands.init import init
from .commands.run import run as run_skill
from .commands.run import train as train_skill


@click.group()
def main():
    pass


def run():
    main.add_command(init)
    main.add_command(run_skill)
    main.add_command(train_skill)

    logging.getLogger().setLevel(logging.INFO)
    main()
