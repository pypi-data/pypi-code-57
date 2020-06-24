import getpass

import click

from tktl.commands import login as login_commands
from tktl.core.loggers import CliLogger

logger = CliLogger()


@click.command("login", help="Perform authenticated requests against the taktile api")
@click.option(
    "-u", "--user-name", "user_name", help="User name used to create Taktile account"
)
@click.option(
    "-p", "--password", "password", help="Password used to create Taktile account"
)
@click.option("-k", "--api-key", "api_key", help="Your api key")
def login(user_name: str, password: str, api_key: str):
    command = login_commands.LogInCommand()
    command.execute(user_name=user_name, password=password, api_key=api_key)


@click.command("logout", help="Log out / remove apiKey from config file")
def logout():
    command = login_commands.LogOutCommand()
    command.execute()


@click.command("api-key", help="Save your api key")
@click.argument(
    "api_key", required=False,
)
def save_api_key(api_key):
    if not api_key:
        api_key = getpass.getpass("Enter your API Key: ")

    command = login_commands.SetApiKeyCommand()
    api_key = api_key.strip()
    command.execute(api_key)
