import click


@click.group()
@click.version_option()
def cli():
    "Demonstrating https://github.com/simonw/click-app"


@cli.command(name="command")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")
