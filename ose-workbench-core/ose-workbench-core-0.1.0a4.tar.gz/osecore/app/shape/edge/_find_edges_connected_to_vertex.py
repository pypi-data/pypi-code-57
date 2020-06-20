from typing import List

import Part


def find_edges_connected_to_vertex(vertex: Part.Vertex,
                                   edges: List[Part.Edge]) -> List[Part.Edge]:
    """Find the edges connected to a vertex.

    :param vertex: A vertex to find the edges connected to.
    :type vertex: Part.Vertex
    :param edges: List of edges to search for the vertex.
    :type edges: List[Part.Edge]
    :return: A new filtered list of edges that are connected to the vertex.
    :rtype: List[Part.Edge]
    """
    vertex_edges = []
    for e in edges:
        for v in e.Vertexes:
            if v.isSame(vertex):
                vertex_edges.append(e)
    return vertex_edges
