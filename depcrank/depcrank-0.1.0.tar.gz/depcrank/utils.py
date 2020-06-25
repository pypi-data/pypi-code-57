"""
FIXME: insert program metadata
"""

import networkx as nx


def make_graph(input_data):
    graph = nx.DiGraph()

    for required_package in input_data:
        graph.add_node(required_package)
        for consuming_package in input_data.get(required_package):
            graph.add_node(consuming_package)
            graph.add_edge(consuming_package, required_package)
    
    return graph


def make_makedepends_graph(input_data):
    graph = nx.DiGraph()

    for required_package in input_data:
        graph.add_node(required_package)
        for makedepend in data.get(required_package):
            graph.add_node(makedepend)
            graph.add_edge(required_package, makedepend)

    return graph


def write_gexf(graph, output_path):
    nx.write_gexf(graph, output_path)
