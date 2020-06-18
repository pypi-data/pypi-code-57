from __future__ import annotations
from typing import Dict, Optional

import copy

from .action import Action

__all__ = ["InsertTasks", "Modify", "Rerun"]


class InsertTasks(Action):
    def __init__(self, *tasks, requires_kw=None) -> None:
        # NOTE: the first task in tasks must be the head, and the last task in tasks must be the tail!
        self.tasks = copy.deepcopy(tasks)
        self.requires_kw = requires_kw

    def run(self, node, tasks, links, done: Dict[int, bool]) -> None:
        head_task_node = len(tasks)
        # this value is safe to use in the scope of this method because only the producer runs actions, and there is only one producer at a time
        tail_task_node = head_task_node + len(self.tasks) - 1
        # this value is safe to use in the scope of this method because only the producer runs actions, and there is only one producer at a time
        tasks.extend(self.tasks)
        for k, v in links.items():
            links[k] = [(kw, x) if x != node else (kw, tail_task_node) for kw, x in v]
        links[head_task_node] = [(self.requires_kw, node)]
        for i in range(head_task_node, tail_task_node + 1):
            done[i] = False


class Modify(Action):
    def modify(self, task: materia.Task) -> materia.Task:
        # NOTE: this should return the modified task - this can be a copy or it can modify task in place and return it, either way
        raise NotImplementedError

    def run(self, node, tasks, links, done: Dict[int, bool]) -> None:
        tasks[node] = self.modify(task=tasks[node])


class Rerun(Action):
    def run(self, node, tasks, links, done: Dict[int, bool]) -> None:
        done[node] = False
