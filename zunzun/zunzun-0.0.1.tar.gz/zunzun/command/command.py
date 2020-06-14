import click
from .exceptions import CommandException


class Command(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = self._handle

    def _handle(self, **kwargs):
        try:
            self.handle(**kwargs)
        except CommandException as e:
            click.echo(str(e), err=True)

    def handle(self, **kwargs):
        raise NotImplementedError

    def add_option(self, *args, **kwargs):
        self.params.append(click.Option(args, **kwargs))

    def add_argument(self, *args, **kwargs):
        self.params.append(click.Argument(args, **kwargs))
