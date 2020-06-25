# -*- coding: utf-8 -*-
"""Make dummy bgraph"""

import logging

from graph_tool import Graph
from graph_tool.generation import random_graph
from numpy.random import exponential, beta

from KolaViz.LibCircuits.utilsCircuits2 import drawg


def deg(mean=None):
    # mean (scale) based on table from my article
    # mean = round(np.log(N) + 1)
    return round(exponential(mean))


def deg_sampler():
    return dispatch_deg(deg())


def make_dummyg(N=10, gtype="random", draw=True, **kwargs):
    g = Graph()
    g.add_vertex(N)

    if isinstance(gtype, list):
        # assert len(gtype) == N, f"pb de taille entre N={N} et len(gtype)={len(gtype)}. Doivent être égaux."
        logging.info(f"Setting N={len(gtype)}")
        g = Graph()
        g.add_vertex(len(gtype))
        for i, vs in enumerate(gtype):
            for v in vs:
                g.add_edge(i, v)
    elif gtype == "fixed":
        logging.info("Generating a fixed graph")
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(3, 4)
        g.add_edge(3, 5)
        g.add_edge(5, 6)
    elif gtype == "circuit":
        logging.info("Generating a fixed graph with circuit")
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(3, 4)
        g.add_edge(3, 5)
        g.add_edge(5, 6)
        g.add_edge(6, 1)
    else:
        logging.info("Generating a random graph")

        g = random_graph(N, deg_sampler)

    if draw:
        pos = drawg(g, vertex_text=g.vertex_index, **kwargs)
        return g, pos
    else:
        return g, None


def dispatch_deg(deg, dist=None):
    """dispatch a general degree as in and out degree folowing the distribution dist (defautl beta(7,2)), in = dist et out = geg - dist"""
    # avece le beta créer un déséquilibre entre in et out degrees avec les noeuds qui recoive plus qu'ils n'émettent
    if dist is None:
        dist = beta(5, 2)

    return round(dist * deg), round(deg - dist * deg)
