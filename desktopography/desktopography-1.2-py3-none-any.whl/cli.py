import logging

import click
import daiquiri

from . import __version__
from . import desktops
from . import selector


@click.group()
@click.version_option(version=__version__)
def main():
    daiquiri.setup(level=logging.INFO)


@main.command()
@click.option('--size')
def shuffle(size=None):
    wallpaper = selector.select_random_wallpaper(size)
    print(wallpaper)  # noqa


@main.command()
@click.option('--size')
@click.argument('desktop', type=click.Choice(desktops.DESKTOPS))
def gsettings(desktop=None, size=None):
    wallpaper = desktops.set_wallpaper(desktop, size)
    logging.info("Set wallpaper to %s", wallpaper)


if __name__ == '__main__':
    main()
