from cleo import Application  # type: ignore

from .view import ViewCommand

__slots__ = ("application",)

application = Application()
application.add(ViewCommand())
