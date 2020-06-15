import json
import os

import click

_CONTEXT_ENV_NAME = "KAISTACK_CONTEXT_PATH"
_DEFAULT_CONTEXT_PATH = "~/.kaistack/context.json"


def get_file_path():
    path = os.environ.get(_CONTEXT_ENV_NAME)
    if path is None:
        path = _DEFAULT_CONTEXT_PATH
    return path


def load_context():
    context_file = get_file_path()
    context_file = os.path.expanduser(context_file) if context_file.startswith("~") else context_file
    with open(context_file, 'r') as f:
        config = f.read()
        return json.loads(config)


@click.command(name="get-context")
def get_context():
    context = load_context()
    click.echo(context)


@click.command(name="set-context")
def set_context():
    click.echo("set config")
