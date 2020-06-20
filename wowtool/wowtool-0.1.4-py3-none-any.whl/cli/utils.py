import functools
import click
import datetime
import json
import os
from pathlib import Path

def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = 'There was an error in the CLI: {}'.format(str(e))
            click.echo(message, err=True)
            exit(1)

    return wrapper

def wowza_auth():
    credentials_path = get_credentials_path()
    if credentials_exist():
        set_credentials_envars(credentials_path)
    else:
        create_creds_file(credentials_path)
        set_credentials_envars(credentials_path)

def get_credentials_path():
    home_path = str(Path.home())
    credentials_path = home_path + '/.wow/config.json'
    return credentials_path

def credentials_exist():
    credentials_path = get_credentials_path()
    if os.path.exists(credentials_path):
        return True
    else:
        return False

def set_credentials_envars(credentials_path):
    with open(credentials_path) as json_file:
        credentials_data = json.load(json_file)
        os.environ["WSC_ACCESS_KEY"] = credentials_data['WSC_ACCESS_KEY']
        os.environ["WSC_API_KEY"] = credentials_data['WSC_API_KEY']

def create_creds_file(credentials_path):
    wsc_access_key = click.prompt('Please enter wowza access key')
    wsc_api_key = click.prompt('Please enter wowza api key')
    keys = {
            'WSC_ACCESS_KEY': wsc_access_key,
            'WSC_API_KEY': wsc_api_key
            }
    with open(credentials_path, 'w') as json_file:
        json_file.write(json.dumps(keys, indent=4))