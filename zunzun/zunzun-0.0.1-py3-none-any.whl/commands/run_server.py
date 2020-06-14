from injector import singleton, inject
from zunzun import Command
from zunzun import HttpKernel


@singleton
class RunServerCommand(Command):
    @inject
    def __init__(self, http_kernel: HttpKernel):
        super().__init__("runserver")
        self.http_kernel = http_kernel

    def handle(self):
        self.http_kernel.run()
