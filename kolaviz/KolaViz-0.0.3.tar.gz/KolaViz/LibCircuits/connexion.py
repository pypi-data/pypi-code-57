# -*- coding: utf-8 -*-
"""Making the connexion in the graph"""
from graph_tool import Graph, Edge
from typing import Tuple, Any

from KolaViz.LibCircuits.utilsCircuits2 import (
    get_vertex4uid,
    update_data2vertex,
)


def connexion_temporelle(g, df, fenetre_tdelta, parallel=False):
    """
    Crée les liaisons entre les noeuds de g en se basant uniquement sur le temps des messages contenu dans df
    - fenetre_tdelta définie quels messages prendre en compte
    - parallel: si il faut autoriser des arcs parallèles (default False)
    """
    # tri les messages par date d'édition
    dfs = df.sort_values("msgMREd")

    # On défini une fenetre temporelle pour lier les messages
    # c'est un multiple du temps médian sur l'ensemble des données
    tdelta_median = (dfs.msgMREd - dfs.msgMREd.shift()).median()
    tdelta = tdelta_median * fenetre_tdelta

    for i, idx in enumerate(dfs.index):
        datum = dfs.loc[idx]
        uid, ts = datum.loc[["authorID", "msgMREd"]].values
        # ts = ts.timestamp()  # pd.ts -> float

        # récupère un noeud pour cet uid (noeud unique)
        vi = get_vertex4uid(g, uid)
        update_data2vertex(g, vi, datum)

        # compute the earliest ts node this user can connect too
        earliest_ts = ts - tdelta

        ts_mask = dfs.msgMREd.apply(lambda d: d < ts and d >= earliest_ts)
        TSwindowUsers = dfs[ts_mask].authorID
        etype = "temporal"

        for j, ujd in enumerate(TSwindowUsers):
            edit_connexion(
                g, datum, vi, ujd, etype, parallel, self_edge=False,
            )
            print(
                f"{etype} connexion update: {i}/{len(dfs)}, msg {j}/{len(TSwindowUsers)} de la fenetre",
                end="\r",
            )
    return g


def connexion_topique(g, df, method, wtext=True, parallel=False):
    """
    Adding links between users of the same tdf.
    - g is the graphe where the links are added
    - tdf is a group of messmsgsMREd from the same tdf
    - users are the users ids from the network
    - nb_groups is the number of tdfs in the network
    - parallel: (True)  if parallel edge should be created or not
    - how: (star), prec, prec1, all, specify how to link users. see create_or_udpate_edge_in_
    - wtext: should we put the true message content or not

    """
    # nombre de messmsgsMREds != nb d'utilisateurs dans cette discussion
    threadGs = df.groupby("threadID")
    # nb_groups = len(threadGs)
    # users = df.authorID.unique()
    etype = "topic"
    for k, (tid, tdf) in enumerate(threadGs):
        for i, uid in enumerate(tdf.authorID):
            vi = get_vertex4uid(g, uid)

            # maj les données du noeuds
            update_data2vertex(g, vi, tdf.iloc[i])

            g.vp["nb_thread_open"][vi] += 1 if i == 0 else 0

            for j, ujd in enumerate(tdf.authorID):
                # on ne considère que messages j venant après i
                if j > i:
                    edit_connexion(
                        g, tdf.iloc[j], vi, ujd, etype, parallel, self_edge=False,
                    )
                    print(
                        f"{etype} connexion update: {k}/{len(threadGs)}, msg {j}/{len(tdf.authorID)} de l'auteur",
                        end="\r",
                    )
    return g


def edit_connexion(g, data, vi, ujd, etype, *args, **kwargs):
    """
Créer la connexion entre le noeud vi et celui qui a pour auteur ujd.
    Crée un noeud de type etype
    dans kwargs ou args, parallel=False, self_edge_allowed=False
"""

    vj = get_vertex4uid(g, ujd)

    # decide if create or update and with what strength
    doCreation, seuil = is_edge_create_or_update(g, vi, vj, etype, *args, **kwargs)

    # préparing dico to update edge props

    if doCreation and seuil:
        propkeys = [
            "msgID",
            "threadID",
            "msgMREd",
            "wtext",
        ]  # this is where we decide what to store in graph
        propsval = {f"s_{etype}": seuil}
        propsval.update(data.loc[propkeys].items())

        if doCreation == "create":
            e = g.add_edge(vj, vi)
            edit_edge_props(g, e, propsval)

        elif doCreation == "update":
            e = g.edge(vj, vi)
            # update_edge_connexion(g, data, vi, vj, seuil, etype)
            edit_edge_props(g, e, propsval, update=True)


def is_edge_create_or_update(g, vi, vj, etype, parallel=False, self_edge=False):
    # sfunc = get_strength_func(etype)
    sfunc = eval(f"get_strength4{etype}")
    seuil = sfunc(g, vi, vj)  # get_temporal_edge_strength

    if not self_edge and vi == vj:
        return False, 0
    else:
        if parallel or not (vi in g.get_out_neighbours(vj)):
            return "create", seuil
        else:
            # dans voisinage et ne veux pas de liens parallels
            return "update", seuil


def edit_edge_props(
    g: Graph, edge: Edge, properties: Tuple(str, Any), update: bool = False,
) -> None:
    """
    Undate or create properties_ for the edge edge_
    """
    try:
        if update:
            for key, val in properties.items():
                g.ep[key][edge] += val
        else:
            for key, val in properties.items():
                g.ep[key][edge] = val
    except AttributeError as ex:
        raise (ex)

    return None


def get_strength_func(etype):
    return eval(f"get_strength4{etype}")


def get_strength4temporal(g, vi, vj):
    return 1


def get_strength4topic(g, vi, vj):
    return 1


def get_strength4author(g, vi, vj):
    return 1
