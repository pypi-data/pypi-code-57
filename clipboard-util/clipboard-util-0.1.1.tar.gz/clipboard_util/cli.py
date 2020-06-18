
import click
import clipboard_util


@click.group()
def cli():
    pass


@cli.command()
@click.argument('args', nargs=-1)
def copy(args):
    combined_args = ' '.join(args)
    clipboard_util.copy(combined_args)
    print(f'Copied "{combined_args}" to clipboard.')


@cli.command()
def paste():
    text = clipboard_util.paste()
    print(text)