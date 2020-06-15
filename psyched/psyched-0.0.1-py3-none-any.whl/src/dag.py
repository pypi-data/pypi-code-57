import networkx as nx
from matplotlib import pyplot as plt

from .image import Image
from .task import Task


class DAG (object):
    def __init__(self, max_parallel_workers: int = 1):
        self.tasks = {}
        self.max_parallel_tasks = max_parallel_workers
        return

    def add_task(self, task: Task):
        self.tasks[task.get_name()](task)
        return

    def new_task(self, name: str, image: Image, command: str) -> Task:
        t = Task(name, image, command)
        self.add_task(t)
        return t

    def draw(self, path: str = 'dag.png'):
        G = nx.DiGraph()
        for k in self.tasks:
            G.add_node(k)
        for k in self.tasks:
            for tp in self.tasks[k].get_downstream():
                G.add_edge(t.name, tp.get_name())
        plt.close()
        nx.draw(G, with_labels=True)
        plt.savefig(path)
        return

    def run(self):
        