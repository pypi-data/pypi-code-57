from injector import singleton, inject
from zunzun import Command
from ..engine import Engine
from ..base import BaseModel


@singleton
class shema_createCommand(Command):
    @inject
    def __init__(self, engine: Engine):
        super().__init__("shema_create")
        self.engine = engine

    def handle(self):
        BaseModel.metadata.create_all(self.engine())
