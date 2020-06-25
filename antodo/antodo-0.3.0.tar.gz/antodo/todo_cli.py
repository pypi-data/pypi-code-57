import contextlib
from typing import List

import click

from .todo import Todos


@click.group()
def todo_cli():
    """simple another todo CLI app"""


@todo_cli.command(help="show current todos")
def show():
    todos = Todos()
    print_todos(todos)


@todo_cli.command(help="add todo")
@click.argument("content", nargs=-1, type=click.STRING)
@click.option("--urgent", "-u", is_flag=True, help="set todo as urgent")
def add(content: List[str], urgent: bool):
    content_str: str = " ".join(content)
    with todos_operation() as todos:
        todos.add_todo(content_str, urgent)


@todo_cli.command(help="removes todo")
@click.argument("indexes", nargs=-1, type=click.INT)
def remove(indexes: List[int]):
    with todos_operation() as todos:
        indexes_to_remove = []
        for index in indexes:
            index_to_remove = index - 1
            if index_to_remove < len(todos):
                indexes_to_remove.append(index_to_remove)
            else:
                click.echo(f"no todo with index {index}")

        todos.remove_todos(indexes_to_remove)
        click.echo(f"deleted todos: {[i+1 for i in indexes_to_remove]}")


@todo_cli.command(help="set todo as urgent")
@click.argument("indexes", nargs=-1, type=click.INT)
def urgent(indexes: List[int]):
    with todos_operation() as todos:
        indexes_to_set = [i-1 for i in indexes if i-1 < len(todos)]
        for index in indexes_to_set:
            todos[index].urgent = True


@contextlib.contextmanager
def todos_operation():
    todos = Todos()
    yield todos
    todos.save()
    print_todos(todos)


def print_todos(todos: Todos):
    if todos:
        for index, todo in enumerate(todos, 1):
            if todo.urgent:
                click.secho(f"{index}. {todo.content}", fg="red")
            else:
                click.echo(f"{index}. {todo.content}")
    else:
        click.echo("No todos found")
