"""Console script for hey_babe."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for hey_babe."""
    click.echo("Replace this message by putting your code into "
               "hey_babe.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
