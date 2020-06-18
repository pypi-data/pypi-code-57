from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional

# import copy
import collections
import json
import multiprocessing as mp
import networkx as nx
import queue
import threading

from .actions import ActionSignal

__all__ = ["Workflow", "WorkflowResults"]


class WorkflowResults:
    def __init__(self, tasks: Iterable[materia.Task], results: Dict[int, Any]) -> None:
        self.tasks = tasks
        self.results = results

    def __getitem__(self, key: str) -> Any:
        return self.results[
            self.tasks.index(next(t for t in self.tasks if t.name == key))
        ]

    def __str__(self) -> str:
        results = {f"{str(self.tasks[k])} ({k})": v for k, v in self.results.items()}
        # FIXME: figure out how to sort by self.results' keys and not results' keys (i.e. by node numbers not task names?)
        return json.dumps(results, sort_keys=True, indent=2, default=str)


class Workflow:
    def __init__(self, *tasks: materia.Task) -> None:
        self.tasks = tuple(set(self._discover_tasks(*tasks)))
        self.links = collections.defaultdict(list)

        for i, t in enumerate(self.tasks):
            for r in t.requirements:
                self.links[i].append((None, self.tasks.index(r)))
            for k, r in t.named_requirements.items():
                self.links[i].append((k, self.tasks.index(r)))

    def _discover_tasks(self, *tasks: Iterable[materia.Task]) -> List[materia.Task]:
        discovered = list(tasks)

        for t in tasks:
            requirements = list(t.requirements) + list(t.named_requirements.values())
            discovered.extend(requirements + self._discover_tasks(*requirements))

        return discovered

    def run(
        self,
        available_cores: int,
        num_consumers: Optional[int] = 1,
        thread: Optional[bool] = True,
    ) -> WorkflowResults:
        if thread:
            tasks = list(self.tasks)
            links = self.links

            # NOTE: holds nodes corresponding to tasks waiting to be run by a process
            task_queue = queue.Queue()
            # NOTE: record task outputs for handler checking and passing to successor tasks
            results = {}
            # NOTE: lookup table to track which tasks have been completed
            done = {node: False for node in range(len(tasks))}
            # NOTE: holds nodes corresponding to tasks waiting to be recognized as done by the producer
            done_queue = queue.Queue()
            # NOTE: holds nodes corresponding to tasks currently being held by a consumer
            tracker = []
            available_cores = available_cores

            producer_kwargs = {
                "tasks": tasks,
                "links": links,
                "task_queue": task_queue,
                "done": done,
                "done_queue": done_queue,
                "tracker": tracker,
                "available_cores": available_cores,
            }
            producer = threading.Thread(target=_produce, kwargs=producer_kwargs)

            consumer_kwargs = {
                "tasks": tasks,
                "links": links,
                "task_queue": task_queue,
                "results": results,
                "done_queue": done_queue,
            }
            consumers = tuple(
                threading.Thread(target=_consume, kwargs=consumer_kwargs, daemon=True)
                for _ in range(num_consumers)
            )
        else:
            # NOTE: for freeze support on Windows - does nothing if not in frozen application or if not on Windows
            mp.freeze_support()
            m = mp.Manager()
            tasks = m.list(self.tasks)
            links = m.dict(self.links)

            # NOTE: holds nodes corresponding to tasks waiting to be run by a process
            task_queue = m.Queue()
            # NOTE: records task outputs for handler checking and passing to successor tasks
            results = m.dict()
            # NOTE: lookup table to track which tasks have been completed
            done = m.dict({node: False for node in range(len(tasks))})
            # NOTE: holds nodes corresponding to tasks waiting to be recognized as done by the producer
            done_queue = m.Queue()
            # NOTE: holds nodes corresponding to tasks currently being held by a consumer
            tracker = m.list()
            available_cores = mp.Value("i", available_cores)

            producer_kwargs = {
                "tasks": tasks,
                "links": links,
                "task_queue": task_queue,
                "done": done,
                "done_queue": done_queue,
                "tracker": tracker,
                "available_cores": available_cores,
            }
            producer = mp.Process(target=_produce, kwargs=producer_kwargs)

            # start consumers
            consumer_kwargs = {
                "tasks": tasks,
                "links": links,
                "task_queue": task_queue,
                "results": results,
                "done_queue": done_queue,
            }
            consumers = tuple(
                mp.Process(target=_consume, kwargs=consumer_kwargs, daemon=True)
                for _ in range(num_consumers)
            )

        # start producer
        producer.start()

        # start consumers
        for c in consumers:
            c.start()

        # synchronize - wait until producer is done (i.e. all tasks are done)
        producer.join()

        # signal consumers to finish
        for _ in range(num_consumers):
            task_queue.put(None)

        return WorkflowResults(tasks, dict(results))


def _produce(
    tasks: Union[List[Task], mp.managers.ListProxy[Task]],
    links: Union[Dict[str, Task], mp.managers.DictProxy[str, Task]],
    task_queue,
    done,
    done_queue,
    tracker,
    available_cores,
) -> None:
    available_cores = _queue_tasks(
        tasks, links, task_queue, done, tracker, available_cores
    )
    while not all(done.values()):
        try:
            node, actions = done_queue.get(block=False)
            if isinstance(node, Exception):
                raise node
        except queue.Empty:
            continue

        # run rest of loop only if a job was marked as done

        # NOTE: nothing bad can happen in between the try block and now,
        # since only _queue_tasks cares about done_queue, done, or tracker,
        # and _queue_tasks cannot possibly be running here since there is
        # only one producer process

        done[node] = True
        for action in actions:
            action.run(node=node, tasks=tasks, links=links, done=done)

        tracker.remove(node)
        available_cores += tasks[node].num_cores
        available_cores = _queue_tasks(
            tasks, links, task_queue, done, tracker, available_cores
        )


def _consume(
    tasks: Union[List[Task], mp.managers.ListProxy[Task]],
    links: Union[Dict[str, Task], mp.managers.DictProxy[str, Task]],
    task_queue,
    results,
    done_queue,
) -> None:
    while True:
        try:
            try:
                node = task_queue.get()
            except queue.Empty:
                continue

            # NOTE: node = None signals consumer to stop
            if node is None:
                break

            # NOTE: this is safe because the node assigned to a task never changes while the workflow runs
            task = tasks[node]
            # NOTE: this is safe because 1.) the dependencies of each task can only be changed by tasks which precede it, i.e. by the time a task is running, no actions can alter its dependencies, and 2.) only one consumer will write to results[node] at a time because only one consumer is running a particular task at a time
            result = task.run(
                *(results[v] for k, v in links[node] if k is None),
                **{k: results[v] for k, v in links[node] if k is not None},
            )

            try:
                for h in task.handlers:
                    h.run(result=result, task=task)

                results[node] = result
                actions = []
            except ActionSignal as a:
                results[node] = a.result
                actions = a.actions

            done_queue.put((node, actions))
        except Exception as e:
            done_queue.put((e, None))


# _PRODUCE HELPER FUNCTIONS


def _queue_tasks(
    tasks: Union[List[Task], mp.managers.ListProxy[Task]],
    links: Union[Dict[str, Task], mp.managers.DictProxy[str, Task]],
    task_queue,
    done,
    tracker,
    available_cores,
) -> None:
    dag = _build_dag(tasks, links)
    for node in dag.nodes:
        if (
            _task_is_ready(node, done, dag, tracker)
            and available_cores >= tasks[node].num_cores
        ):
            available_cores -= tasks[node].num_cores
            tracker.append(node)
            task_queue.put(node)

    return available_cores


def _build_dag(
    tasks: Union[List[Task], mp.managers.ListProxy[Task]],
    links: Union[Dict[str, Task], mp.managers.DictProxy[str, Task]],
) -> nx.DiGraph:
    # convert tasks and links into a NetworkX directed graph
    dag = nx.DiGraph()
    dag.add_nodes_from(range(len(tasks)))
    dag.add_edges_from((head, tail) for tail, v in links.items() for _, head in v)

    # a cyclic dependency graph can't be run - something must have gone wrong, so raise an error
    if not nx.is_directed_acyclic_graph(dag):
        raise ValueError("Workflow does not form a directed acyclic graph.")

    return dag


def _task_is_ready(node, done, dag: nx.DiGraph, tracker) -> bool:
    return (
        (not done[node])
        and all(done[ancestor] for ancestor in nx.ancestors(dag, node))
        and (node not in tracker)
    )
