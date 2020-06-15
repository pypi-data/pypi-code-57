""" network module.

"""

import warnings
from abc import ABC
from collections import Hashable


def connected_from(node, edges) -> list:
    return [b for a, b in edges if a == node]


def connect_nodes(nodes: dict, edges) -> dict:
    connected_nodes = {}
    for key, node in nodes.items():
        if not isinstance(node, Node):
            raise TypeError
        children = connected_from(key, edges)
        node.add_nodes(children)
        connected_nodes[key] = node
    return connected_nodes


class Node(object):
    """ node class.

    """

    def __init__(self):
        self.children = []

    def add_node(self, node):
        self.children.append(node)

    def pop_node(self, node):
        return self.children.pop(self.children.index(node))

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)


class Network(ABC):
    """ network abstract base class.

    """

    def __init__(self, nodes: dict, edges: list, start=None, end=None):
        self.nodes = connect_nodes(nodes, edges)
        self.start = start
        self.end = end
        self.setup()

    def merge_network(self, network, new_edges=None):
        if self.end is None:
            raise NotImplementedError("The end of this network must be defined before merging with another network.")
        if not isinstance(network, Network):
            raise TypeError("Object to append must be a network.")
        if len(set(self.nodes.keys()).union(set(network.nodes.keys()))) > 0:
            warnings.warn("There are some node naming conflicts between the two networks.")
        self.nodes.update(network.nodes)
        self.add_edge(self.end, network.start)
        if new_edges is not None:
            self.add_edges(new_edges)

    def setup(self):
        pass

    def add_edge(self, _from: Hashable, to: Hashable):
        self.nodes[_from].add_node(to)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)

    def remove_edge(self, _from: Hashable, to: Hashable):
        self.nodes[_from].pop_node(to)

    def add_node(self, key: Hashable, node: Node):
        self.nodes[key] = node

    def remove_node(self, key: Hashable):
        del self.nodes[key]
