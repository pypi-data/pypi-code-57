from dataclasses import asdict
from dataclasses import dataclass
import os
import json
from typing import List

import antodo.config as c


@dataclass
class Todo:
    content: str
    urgent: bool

    def __str__(self) -> str:
        return self.content


class Todos:
    def __init__(self):
        self._loader = TodosLoader()
        self._todos: list = self._loader.load_todos()

    def add_todo(self, content: str, urgent: bool):
        self._todos.append(Todo(content, urgent))

    def remove_todos(self, indexes_to_remove):
        self._todos = [todo for index, todo in enumerate(self._todos) if index not in indexes_to_remove]

    def save(self):
        self._loader.save_todos(self._todos)

    def __getitem__(self, index):
        return self._todos[index]

    def __bool__(self):
        return bool(self._todos)

    def __len__(self):
        return len(self._todos)

    def __iter__(self):
        return iter(self._todos)


class TodosLoader:
    DEFAULT_TODOS: dict = {"todos": []}

    def load_todos(self) -> List[Todo]:
        todos_json = self._get_or_create_todos()
        todos = list(map(lambda todo: Todo(**todo), todos_json["todos"]))
        return todos

    def _get_or_create_todos(self) -> dict:
        if os.path.exists(c.TODOS_JSON_PATH):
            with open(c.TODOS_JSON_PATH) as file:
                return json.load(file)

        os.makedirs(c.TODOS_DIR, exist_ok=True)
        with open(c.TODOS_JSON_PATH, "w") as file:
            json.dump(self.DEFAULT_TODOS, file)

        return self.DEFAULT_TODOS

    def save_todos(self, todos: Todos):
        todos_to_save = list(map(lambda todo: asdict(todo), todos))
        with open(c.TODOS_JSON_PATH, "w") as file:
            json.dump({"todos": todos_to_save}, file)
