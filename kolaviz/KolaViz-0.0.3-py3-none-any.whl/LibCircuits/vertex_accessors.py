# -*- coding: utf-8 -*-
"""A bunch of function to access easily vertex of a graph"""
import numpy as np
import operator
from numpy.random import choice, randint


def vx_with_indeg_eq(g, val, tri="in"):
    return vx_with_anyindeg(g, val=val, op="eq", tri=tri)


def vx_with_indeg_sup(g, val, tri="in"):
    return vx_with_anyindeg(g, val=val, op="gt", tri=tri)


def vx_with_anyindeg(g, val=0, op="gt", tri=""):
    return vx_with_anyspecdeg(g, "in", val=val, op=op, tri=tri)


def vx_with_outdeg_eq(g, val, tri="out"):
    return vx_with_anyoutdeg(g, val=val, op="eq", tri=tri)


def vx_with_outdeg_sup(g, val, tri="out"):
    return vx_with_anyoutdeg(g, val=val, op="gt", tri=tri)


def vx_with_anyoutdeg(g, val=0, op="gt", tri="out"):
    return vx_with_anyspecdeg(g, degtype="out", val=val, op=op, tri=tri)


def vx_with_deg_sup(g, val, tri=""):
    return vx_with_anydeg(g, val=val, op="gt", tri=tri)


def vx_with_deg_eq(g, val, tri=""):
    return vx_with_anydeg(g, val=val, op="eq", tri=tri)


def vx_with_anydeg(g, val=0, op="gt", tri=""):
    return vx_with_anyspecdeg(g, "in_out", val=val, op=op, tri=tri)


def vx_with_anyspecdeg(g, degtype, val=0, op="gt", tri=""):
    """degtype in 'in' or 'out.
    Returns a list of vertices with any in or out degree"""
    return vx_with_specdeg(g, degtype, val=val, op=op, tri=tri)


def vx_with_specdeg(g, degtype, val=0, op="gt", tri=""):
    """degtype in 'in' or 'out' or 'both'.
    tri  par 'in' 'out' or 'in_out' degree
    Returns a list of vertices with any in or out degree"""

    assert op is not None and isinstance(op, str), f"Check the op={op}."
    test = getattr(operator, op)
    vx = [v for v in g.vertices() if test(degfunc(v, degtype), val)]
    return sorted(vx, key=lambda v: degfunc(v, tri)) if tri else vx


def degfunc(v, degtype):
    """Renvois la fonction pour évaluer l degree d'un vertex. in_degree or out_degree or both
    degtype is 'in' 'out' or any combination"""
    assert (
        "in" in degtype or "out" in degtype
    ), f"One of 'in', 'out' should be in degtype but it is '{degtype}'"
    if "in" in degtype and "out" in degtype:
        return getattr(v, "in_degree")() + getattr(v, "out_degree")()
    elif "in" in degtype or "out" in degtype:
        return getattr(v, f"{degtype}_degree")()


def rnd_vx_with_specdeg(g, degtype="in_out", val=0, op="gt"):
    """Renvois un noeud aléatoire mais satisfaisant les condition degtype (in, out, in_out), et op et val"""
    rvx = vx_with_anyspecdeg(g, degtype, val=val, op=op)
    return np.random.choice(rvx)


def vs_with_specdeg_sup(g, spec1=("out", 1), spec2=("in", 1)):
    """Renvois un couple de vertex pas forcement connecté mais dont le premier à sont degtype (spec1[0]) sup val1 (spec1[1]) et le second degtype > val2"""
    degtype1, val1 = spec1
    degtype2, val2 = spec2
    vx1 = vx_with_specdeg(g, degtype1, val1)
    vx2 = vx_with_specdeg(g, degtype2, val2)
    return choice(vx1), choice(vx2)


def rnd_edge(g, asedge=True):
    """REturn a random edge from g"""
    rx = randint(g.num_edges())
    s, t = g.get_edges()[rx]
    return g.edge(s, t) if asedge else (s, t)
