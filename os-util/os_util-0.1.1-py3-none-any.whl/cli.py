import click
import os_util


@click.group()
def cli():
    pass


@cli.command()
@click.argument("arg")
def which(arg):
    # print("[START]")
    result = os_util.which(arg)
    print(result)
    # print("[END]")


if __name__ == "__main__":
    cli()
