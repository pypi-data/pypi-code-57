import logging

import click

from .commands.init import init


@click.group()
def main():
    pass


def run():
    main.add_command(init)

    logging.getLogger().setLevel(logging.INFO)
    main()
