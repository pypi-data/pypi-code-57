from pprint import pprint

import click
from gui_util import gui


@click.group()
def cli():
    pass


@cli.command()
def current_window():
    window = gui.get_current_window()
    print(window)
    return True


@cli.command()
@click.option('--exclude')
@click.option('--limit', type=int)
def recent_windows(exclude, limit):
    recent_windows_result = gui.get_recent_windows(exclude=exclude, limit=limit)
    pprint(recent_windows_result)
    return True


@cli.command()
@click.option('--exclude')
def recent_window(exclude):
    recent_window_result = gui.get_recent_window(exclude=exclude)
    print(recent_window_result)
    return True


@cli.command()
def focus_on_window():
    print('[START]')
    gui.focus_on_window('chrome')
    print('[END]')
    return True


if __name__ == "__main__":
    cli()
