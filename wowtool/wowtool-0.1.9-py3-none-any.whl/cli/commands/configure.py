import click
import json
import os
from pathlib import Path
from cli.utils import exception_handler, create_creds_file, credentials_file_exist, get_credentials_path

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group(invoke_without_command=True)
def configure():
    """
    Setup credentials file.
    """

    credentials_path = get_credentials_path()
    if credentials_file_exist(credentials_path):
        if click.confirm('Credentials file already exist, override?'):
            create_creds_file(credentials_path)
            click.echo('Credentials file successfully created!')
    else: 
        create_creds_file(credentials_path)
        click.echo('Credentials file successfully created!')
