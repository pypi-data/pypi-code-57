import click


@click.command()
@click.argument('name', nargs=1)
def blocks(name):
    """
    Simple command that says hello
    """
    click.echo(f'Hello {name}')
