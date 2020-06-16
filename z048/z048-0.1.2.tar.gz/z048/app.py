import random
import click

from .utils import Play2048

@click.group()
def cli():
    pass

@cli.command()
@click.option('--dimension', '-d', 'd', help='choose how rows/cols will the board have assuming its a square', default=4)
def play(d):

    game = Play2048(d)
    game.print_board()
    game.playing()

if __name__ == '__main__':
    cli()
