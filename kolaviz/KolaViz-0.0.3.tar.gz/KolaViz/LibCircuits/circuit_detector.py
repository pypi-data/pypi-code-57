# -*- coding: utf-8 -*-
# inspiration from
# https://eli.thegreenplace.net/2015/directed-graph-traversal-orderings-and-applications-to-data-flow-analysis/
import logging
import operator
import json
import pickle
from pathlib import Path
from collections import OrderedDict
from typing import List, IO, Optional, Any

import numpy.random as rnd

from graph_tool.topology import all_circuits as gtt_all_circuits
from graph_tool import Graph

from KolaViz.LibCircuits.vertex_accessors import (
    vx_with_indeg_eq,
    vx_with_outdeg_sup,
)


def conds_on_search_path(stack_: List[int], conds_, G_=None):
    """
    Test each conds on stack
    Applique la fonction qui est dans cond au stack

    exemple de cond [(len, 'lt', 4), "any"]

    return the value type of their truevalue
    """

    _res = []
    _popedTruthOp = conds_.pop()

    if isinstance(_popedTruthOp, str):
        _truthOp = globals()["__builtins__"][_popedTruthOp]
    elif callable(_popedTruthOp):
        _truthOp = _popedTruthOp
    else:
        msg = (
            "Truthop should be a truthOp builtin."
            f" It is {_popedTruthOp, type(_popedTruthOp)}."
        )
        raise Exception(msg)

    for _cond in conds_:
        assert len(_cond) == 3, f"_cond={_cond} in conds_={conds_}"
        _func, _op, _val = _cond
        _test_op = getattr(operator, _op)
        _res.append(_test_op(_func(stack_), _val))

    # conds_ is mutable we restore it to its original size
    conds_.append(_popedTruthOp)

    # we apply the truth operator to the list of test results
    return _truthOp(_res)


def update_circuits(circuits, newCircuits, fout, neigh, root):
    """
    add to circuits the same rooted circuits
    """

    if isinstance(newCircuits[0], list):
        # cas de plusieurs circuits
        logmsg = (
            f"neigh({neigh}) == root({root}), circuits={circuits},"
            f" updateting #newCircuits={newCircuits}"
        )

        for c in newCircuits:
            circuits.append(c)
    else:
        logmsg = (
            f"Circuits update for neigh({neigh}) == root({root}), circuits={circuits},"
            f" newCircuit={newCircuits}"
        )
        circuits.append(newCircuits)

    logging.debug(logmsg)
    if fout is not None:
        fout.write(str(pickle.dumps(newCircuits)) + "\n")

    return circuits, True


def in_same_root_circuit(root, marked_stack, neigh, circuits):
    """
    should return the whole circuits from the marked_stack
    and neigh when neigh is in an existing circuits
    """

    root = marked_stack[0]
    logging.debug(
        f"root={root}, marked_stack={marked_stack}, neigh={neigh}, circuits={circuits}"
    )
    try:
        container_circuits = [c for c in circuits if c[0] == root and neigh in c[1:]]
        end_circuits = [cc[cc.index(neigh) :] for cc in container_circuits]
        new_circuits = [marked_stack + ec for ec in end_circuits]
        logging.debug(f"new_circuits={new_circuits}")
        return new_circuits
    except TypeError as te:
        # import ipdb; ipdb.set_trace()
        logging.debug(f"circuits={circuits}")
        raise (te)

def circuit_enumeration4(G_: Graph, stopcond_=[(len, "lt", 5), "any"], fname_=None):
    """
    Enumère les circuits du graphe G_.

    - cond: is a list triplet (func, op_name, val) is to be applied
    on marked_stack to stop but the last element is the truth funtion to apply
    - fname_:  is the name of the file to write into.
    if None, will send result to memory
    """
    N = G_.num_vertices()
    G_.clear_filters()

    points: List[int] = list()
    circuits: List[List[int]] = list()
    marked_stack: List[int] = list()
    G_.vertex_properties["marked"] = G_.new_vertex_property("bool")
    G_.edge_properties["blocked"] = G_.new_edge_property("bool")

    # à voir
    global gFlag
    gFlag = None

    cpt = circuit_compteur(0, end=10e10)

    def tarjan(
        root: int, vertex: int, flag: bool, fout: Optional[IO] = None,
    ):

        print(
            f"cpt={next(cpt):7}, len(marked_stack)={len(marked_stack):3}, "
            f"vertex={vertex:4}, root={root:3}",
            end="\r",
        )

        global gFlag
        points.append(vertex)
        marked_stack.append(vertex)
        G_.vp["marked"][vertex] = True

        if conds_on_search_path(marked_stack, stopcond_, G_):

            for edge in G_.vertex(vertex).out_edges():
                neigh = G_.vertex_index[edge.target()]

                #            for neigh in Ga[vertex][:]:
                if neigh < root:
                    # Ga[vertex].pop(Ga[vertex].index(neigh))
                    G_.ep.blocked[edge] = True
                    #  logging.debug(f"neigh({neigh}) < root({root}), {Ga}")
                elif neigh == root:
                    newCircuit = points[:]
                    # logmsg = f"neigh({neigh}) == root({root}), newCircuit={newCircuit}
                    if fout is None:
                        circuits.append(newCircuit)
                        #  logging.debug(f"{logmsg} in memory only")
                    else:
                        fout.write(json.dumps(newCircuit) + "\n")
                        #  logging.debug(f"{logmsg} in file")
                    flag = True

                elif not G_.vp["marked"][neigh]:
                    if flag == gFlag and not flag:
                        flag = False
                    else:
                        flag = True
                    # #  logging.debug(f"#call={next(cpt)} tarjan({root}, neigh={neigh},
                    # {gFlag}), marked_stack={marked_stack}")
                    tarjan(root, neigh, gFlag, fout=fout)

        gFlag = flag
        if flag:
            u = marked_stack.pop()
            while u != vertex:
                G_.vp["marked"][u] = False
                u = marked_stack.pop()
            # vertex is now deleted from mark stacked, and has been called u
            # unmark vertex
            G_.vp["marked"][u] = False
        # #  logging.debug(f"vertex ({vertex}): backed to marked_stack={marked_stack},
        # marked={G_.vp['marked'].a}")
        # points.pop(points.index(vertex))
        points.pop()

    G_.vp["marked"].a = False
    if fname_ is not None:
        with open(fname_, "w") as f:
            for i in range(0, N):
                # print(f"Call # {i+1}/{N}", end="\n")
                points = []
                tarjan(i, i, False, fout=f)
                # on revient en arrière ici
                while len(marked_stack) > 0:
                    u = marked_stack.pop()
                    G_.vp["marked"][u] = False
    else:
        for i in range(0, N):
            # print(f"Call # {i+1}/{N}", end="\n")
            points = []
            tarjan(i, i, False)
            # on revient en arrière ici
            while len(marked_stack) > 0:
                u = marked_stack.pop()
                G_.vp["marked"][u] = False

    return circuits


def init(g, root, props, start_strat=None):
    """
    Initialise start of graph search
    """

    def out_degree(v):
        return g.degree_property_map("out")[v]

    N = g.num_vertices()
    for prop in props:
        g.vertex_properties[prop[0]] = g.new_vertex_property(prop[1])

    # how to select the root ?
    if root is None:

        if start_strat is None:
            root = g.vertex(rnd.randint(N))
        else:
            if start_strat == "most_in_out":
                # from nodes with 0 in degree select the one with most out degree
                potential_roots = vx_with_indeg_eq(g, 0, "in")
                potential_roots = sorted(potential_roots, key=out_degree)
            elif start_strat == "most_out":
                # ou simplement le plus de out
                potential_roots = vx_with_outdeg_sup(g, 1, "")

            root = potential_roots.pop()

    elif isinstance(root, int):
        root = g.vertex(root)

    return OrderedDict({"g": g, "root": root, "N": N})


def dfs(graph, root=None, visitor=None):
    """
    Depth First search over a graph g
    Start with vertice 'root', calling 'visitor' for every visited vertices
    .
    """

    if visitor is None:
        visitor = does_nothing

    g, root, N = init(graph, root, "visited").values()

    def dfs_walk(node):
        g.vp["visited"][node] = True
        visitor(node)
        for succ in g.get_out_neighbours(node):
            if not g.vp["visited"][succ]:
                dfs_walk(g.vertex(succ))

    dfs_walk(root)
    return g


def trajan(graph, root=None, visitor=None, start_strat="most_out"):
    """
    Return a post-order ordering of nodes in the graph.

    - start_stat is the startety to choose the starting node (most_out), most_in_out
    ,
    """

    if visitor is None:
        visitor = does_nothing

    g, root, N = init(graph, root, [("color", "string")], start_strat).values()
    order = []
    res = []

    # choisir un noeud de départ avec lien sortant
    def dfs_walk(node):
        # import ipdb; ipdb.set_trace()
        g.vp["color"][node] = "grey"
        for succ in g.get_out_neighbours(node):
            succ_color = g.vp["color"][succ]
            if "grey" in succ_color:
                # visitor(node, g.vertex(succ))
                # print(f'CIRCUIT: {node}-->{succ}')
                circuit = [
                    g.vertex_index[v]
                    for v in g.vertices()
                    if "grey" in g.vp["color"][v]
                ]
                res.append(circuit)
                g.vp["color"][node] = "grey_red"
            elif not succ_color:
                dfs_walk(g.vertex(succ))

        if "red" in g.vp["color"][node]:
            g.vp["color"][node] = "red"
        else:
            g.vp["color"][node] = "black"
            order.append(g.vertex_index[node])

    dfs_walk(root)

    return {"order": order, "circuit links": res}


def adjacent(g):
    """
    Given small g, returns the adjancent matrice in form of list of list of indices

    """

    A = []
    for v in g.vertices():
        A.append([g.vertex_index[u] for u in g.get_out_neighbours(v)])
    return A


def circuit_compteur(start=0, end=100):
    """
    Un compteur pour suivre les appels dans les applys
    """

    i = start
    while True:
        i += 1
        yield i


def all_circuits(
    g, asliste: bool = False, fname_=Path("all_circuit.pkl"), maxiter=10e4,
):
    """
    utiliser l'implémentation de graph_toolpour trouver les circuits.
    par défaut écrit le résultats dans un fichier binaire sur le disque.
    et ce limite à 10e4 iteration.  si aslist renvois le résultat comme une liste.
    """

    # ! Ce truc à tendance à planter souvent
    i = 0

    res: List[Any] = list()

    with open(fname_, "bw") as f:
        for c in gtt_all_circuits(g):
            i += 1
            print(f"i={i}", end="\r")
            if asliste:
                res.append(c)
            f.write(pickle.dumps(f"{c}\n"))
            if i > 10e4:
                break

    return res


def does_nothing(v):
    return None
