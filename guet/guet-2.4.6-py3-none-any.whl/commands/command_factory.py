from typing import List

from guet.commands.command import Command
from guet.context.context import Context
from guet.settings.settings import Settings


class CommandFactoryMethod:
    def __init__(self):
        self.context = Context.instance()

    def build(self, args: List[str], settings: Settings) -> Command:
        raise NotImplementedError
