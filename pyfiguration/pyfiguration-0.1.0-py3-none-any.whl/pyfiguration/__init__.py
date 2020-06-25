from .cli import cli
from .pyfiguration import PyFiguration


# Create an instance of PyFiguration
conf = PyFiguration()

__all__ = [
    "cli",
    "PyFiguration",
    "conf",
]
