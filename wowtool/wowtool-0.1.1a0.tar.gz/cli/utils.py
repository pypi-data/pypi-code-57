import functools
import click
import datetime

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