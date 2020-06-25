__version__ = "0.3.0"
__all__ = ["main"]

from .todo_cli import todo_cli


def main():
    todo_cli()
