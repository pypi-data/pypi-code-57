import click

from tktl.commands import login as login_commands


@click.command("version", help="Show the version and exit")
def get_version():
    command = login_commands.ShowVersionCommand()
    command.execute()
