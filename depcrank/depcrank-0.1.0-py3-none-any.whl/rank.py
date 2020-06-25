"""
FIXME: insert program metadata
"""

import networkx as nx
from depcrank.utils import make_graph


def calculate_pagerank(input_data, personalization):
    graph = make_graph(input_data)

    pagerank_scores = nx.pagerank(graph, personalization=personalization)

    return pagerank_scores


def calculate_transitive_indegree(input_data):
    transitive_count = {}
    for package in input_data:
        for transitive_dependency in \
            set(input_data[package]['transitive_dependencies']):
            if transitive_dependency not in transitive_count:
                transitive_count[transitive_dependency] = 1
            else:
                transitive_count[transitive_dependency] += 1
    return transitive_count
