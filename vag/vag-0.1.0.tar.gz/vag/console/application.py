import click
from vag import __version__


@click.group()
def main():
    pass


@main.command()
def version():
    """Prints version"""
    
    print(__version__)


main.add_command(version)


if __name__ == '__main__':
    main()