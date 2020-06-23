import click
from kaistack.config.context import get_context, set_context
from kaistack.auth.token import get_token
from kaistack.tools.component_importer import upload_component

@click.group()
def cli():
    pass


cli.add_command(get_context)
cli.add_command(set_context)
cli.add_command(get_token)
cli.add_command(upload_component)

def main():
    cli()
