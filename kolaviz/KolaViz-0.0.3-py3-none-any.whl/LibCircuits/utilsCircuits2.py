# -*-coding:utf-8-*-

import logging
import pandas as pd
from pathlib import Path
from itertools import chain
from pandas import Series
from typing import Set, Sequence


from graph_tool import Graph
from graph_tool.draw import graph_draw, sfdp_layout, prop_to_size
from graph_tool.topology import shortest_distance, label_components
from matplotlib.pyplot import get_cmap
import numpy as np
from numpy.random import choice


from KolaViz.LibCircuits.compute_seuil import compute_seuils, compute_seuil_topic


def graph_init(df: pd.DataFrame):
    """
    initialise un graph de messages à partir de df
    """
    g = Graph()
    g.clear_filters()

    # ############### vertices ################

    g.add_vertex(len(df))
    g.vp["filtre"] = g.new_vertex_property("bool")

    vpkeys = {
        "int": ["threadID", "msgID", "authorID", "nmf_ctg"],
        "float": ["msgMREd"],
        "string": ["wtext", "author"],
    }
    create_props(g, "vertex", vpkeys)

    # récupère les noms en une liste
    vdefname = list(chain.from_iterable(vpkeys.values()))

    # créer un dico avec les valeurs
    vdefault = dict(zip(vdefname, df.loc[:, vdefname].T.values))

    # on copie les données par defaut de df dans les noeuds du graphes
    set_default_vprop(g, propdef=vdefault)

    # ############### edges ################

    dims = ["temporal", "topic", "author"]
    epkeys = {"float": ["weight", *[f"s_{d}" for d in dims]]}
    epkeys["object"] = ["msgIDs"]

    _ = create_props(g, "edge", epkeys)

    return g


def get_nodeIDs4cond(g: Graph, cond) -> Set[Sequence]:
    """
    Given a condition as a boolean area over all the graph vertices.
    return the index of the non False vertices ???
    """
    return set(chain.from_iterable(np.argwhere(cond)))


def set_default_vprop(g, propdef: dict):
    """
    used to fill the graph properties with value from a df
    """
    for propname, propvalues in propdef.items():

        if is_number(propvalues[0]):
            g.vp[propname].a = propvalues
        else:
            for (i, val) in enumerate(propvalues):
                g.vp[propname][g.vertex(i)] = val
    return g


def get_edges4msgID(g, tid):
    return [e for e in g.edges() if g.ep["msgID"][e] == tid]


def get_weight_from(seuil):
    """
    Seuil peut être un triplet de valeurs positives. Renvois un float
    qui symbolise la force combiné du lien.
    """
    # la plus simple des fonctions.  Pourrait être min, max, average
    # ou un truc normé sur une bool
    return sum(seuil)


def get_vertex4uid(g, uid):
    """
    return the vertex for specific uid. IT should already existe
    """
    vid = filtre_vid_with_propval(g, "uid", uid)
    assert len(vid) == 1, (
        f"vid={vid} pour uid={uid}  Il doit y avoir exactement une vertex "
        "id pour un author ID"
    )
    return g.vertex(vid[0])


def filtre_vid_with_propval(g, prop, val):
    """
    Return vertices with prop equal to val
    """
    # nor working because vertex_index cannot be access as .a
    # filtre = g.vp[prop].a == val
    # return g.vertex_index.a[filtre]  # 12.8 µs ± 416 ns
    return [v for v in g.vertices() if g.vp[prop][v] == val]  # slow 238 µs ± 6.9


def create_props(G_: Graph, ptype: str, epkeys: Sequence) -> Graph:
    """
    given a graph G_, a ptype (edge or vertex and a dict of type values)
    create ptype property maps for the graphe
    """
    new_prop = getattr(G_, f"new_{ptype}_property")
    prop_dic = getattr(G_, f"{ptype}_properties")
    for proptype, propnames in epkeys.items():
        for name in propnames:
            prop_dic[name] = new_prop(proptype)
    return G_


def cree_liens_pour_group(
    g, tdf, users, rank, nb_groups, parallel=True, how="star", wtext=True
):
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
    nb_msg = len(tdf)
    # on loop sur les participants du group dans l'ordre du group
    # lCompoDiam = largest_component_diameter(g)

    for (i, uid) in enumerate(tdf.authorID):
        vi = get_vertex4uid(g, uid)

        g.vp["msgsMREd"][vi] = max([g.vp["msgsMREd"][vi], tdf.msgMREd.iloc[i]])

        # tdf starteur que si i == 0, pour ce group
        g.vp["nb_thread_open"][vi] += 1 if i == 0 else 0

        for (j, ujd) in enumerate(tdf.authorID):
            if j < i:
                # on ne considère que messages j venant après i
                break
            vj = get_vertex4uid(g, ujd)

            edge_creation, seuils = create_or_update_edge_in_(
                tdf, g, vi, i, vj, j, parallel, how=how, lcd=1
            )

            if edge_creation and get_weight_from(seuils):
                tdfj = tdf.iloc[j]

                if edge_creation == "create":
                    # de j vers i (dans le sens de l'action) 'h' donne une info à 'i'..?
                    # c'est plutot i qui a donnée l'info mais bon.. sens fixé.
                    e = g.add_edge(vj, vi)
                    g.ep["weight"][e] = get_weight_from(seuils)
                    g.ep["seuils"][e] = seuils
                    g.ep["msgID"][e] = tdfj.msgID
                    g.ep["threadID"][e] = tdfj.threadID
                    g.ep["msgMREd"][e] = tdfj.msgMREd
                    if wtext:
                        g.ep["wtext"][e] = tdfj.wtext
                    else:
                        # dummy text for annonymisation
                        g.ep["wtext"][e] = choice(
                            [
                                "Vous avez le choix,",
                                "entre noix de coco,",
                                " ananas et goyave.",
                                "  Que des fruits exotiques.",
                                "  Je ne raconte pas de salade de fruit,",
                                " jolie jolie.",
                            ]
                        )

                elif edge_creation == "update":
                    e = g.edge(vj, vi)
                    g.ep["weight"][e] += get_weight_from(seuils)
                    g.ep["seuils"][e] += np.array(seuils)
                    g.ep["msgMREd"][e] = max([tdfj.msgMREd, g.ep["msgMREd"][e]])

        print(
            f"Grouping methode {how}: {rank}/{nb_groups}, lien ({i}, {j})/{nb_msg}",
            end="\r",
        )


def create_or_update_edge_in_(tdf, g, vi, i, vj, j, parallel, how, lcd):
    """
    Dit si il faut créer un lien ou non entre deux sommets et renvois la force de ce lien.
    - tdf: un ensemble de messages d'un même thread
    - g le graph
    - vi, vj, le sommet source, le sommet cible
    - i, j les indices des sommet dans la list des messages du thread
    - parallel: faut-il créer des lien parallèle
    - how: la façon de créer les lien (voir compute_seuils)
    -lcd : largest component diameter. for seuils_authors

    """
    # vi = g.vertex(get_vertex4uid(g, tdf.authorID.iloc[i]))
    # vj = g.vertex(get_vertex4uid(g, tdf.authorID.iloc[j]))

    time_direction = i < j
    no_self_edge = vi != vj

    if time_direction and no_self_edge:
        seuils = compute_seuils(g, tdf, vi, i, vj, j, how, lcd)
        if parallel or not (vi in g.get_out_neighbours(vj)):
            return ("create", seuils)
        else:
            # dans voisinage et ne veux pas de liens parallels
            return ("update", seuils)

    return (False, 0)


def largest_component_diameter(g):
    """
    A pseudo-diameter existe but it does not return what I except
    """
    distSet: Set[float] = set()
    for v in g.vertices():
        distSet |= set(shortest_distance(g)[v])

    distL = list(distSet)
    return distL[-2] if len(distL) > 1 else distL[-1]


def create_or_update_topic_edge_in_(tdf, g, vi, i, vj, j, parallel, how, lcd):
    """
    Dit si il faut créer un lien ou non entre deux sommets et renvois la force de ce lien.
    - tdf: un ensemble de messages d'un même thread
    - g le graph
    - vi, vj, le sommet source, le sommet cible
    - i, j les indices des sommet dans la list des messages du thread
    - parallel: faut-il créer des lien parallèle
    - how: la façon de créer les lien (voir compute_seuils)
    -lcd : largest component diameter. for seuils_authors

    """
    time_direction = i < j
    no_self_edge = vi != vj

    if time_direction and no_self_edge:
        seuil = compute_seuil_topic(tdf, i, j, how)
        if parallel or not (vi in g.get_out_neighbours(vj)):
            return ("create", seuil)
        else:
            # dans voisinage et ne veux pas de liens parallels
            return ("update", seuil)

    return (False, 0)


def update_data2vertex(g: Graph, vi, new_data: Series) -> None:
    """
    Ajoute les données new_data d'un message à un noeud vi du graph g
    """
    prev_data = g.vp["data"][vi]  # previous data

    if prev_data is None:
        g.vp["data"][vi] = new_data

    else:
        if has_dim_one(prev_data):
            # prev_data is then a pd.Serie, we want it as a df..
            prev_data = prev_data.T

        g.vp["data"][vi] = prev_data.append(new_data)

    # on met à jour la date de dernière action du noeud
    maj_mrc_user_edit_time(g, vi, new_data.msgMREd)
    return None


def maj_mrc_user_edit_time(g, vi, ts) -> None:
    """
    met à jour le temps d'édition d'un auteur.  On ne garde que le plus récent
    """
    # import ipdb; ipdb.set_trace()

    g.vp["mrcuEdts"][vi] = max([g.vp["mrcuEdts"][vi], ts])
    return None


def drawg(
    g,
    opt="big",
    pos=None,
    fname=None,
    init_view=None,
    bg_color=None,
    ecmap=None,
    eorder=None,
    edge_color=None,
    edge_pen_width=None,
    output=None,
    output_size=None,
    vcmap=None,
    vertex_fill_color=None,
    vertex_size=None,
    vertex_text=None,
    vertex_text_position=None,
    vertex_font_size=None,
    vertex_shape=None,
    vweight=None,
    eweight=None,
    **kwargs,
):
    """
    Set some sensibl default to draw a graph

    """
    # edge_size = prop_to_size(g.ep.weight, mi=0, ma=1, log=False, power=4)
    if pos is None:
        pos = set_vertex_position(g, vweight=vweight, eweight=eweight)

    #    la taille du canvas
    # if init_view is None:
    #     X = [pos[v][0] for v in g.vertices()]
    #     Y = [pos[v][1] for v in g.vertices()]
    # else:
    #     X = init_view["X"]
    #     Y = init_view["Y"]

    # marge = {'x': 5, 'y': 5}
    # dx = max(X) - min(X) + marge['x']
    # dy = max(Y) - min(Y) + marge['y']
    # fit_view = (2*dx/5, 2*dy/5, dx, dy)
    fit_view = True

    # la sortie
    if fname is None:
        output = None
        output_size = (800, 400)
    else:
        output = fname
        output_size = (2054, 2054)

    # les noeuds
    if bg_color is None:
        bg_color = [1, 1, 1, 1]  # white

    if vertex_shape is not None and vertex_shape != "none":
        if vertex_fill_color is None:
            vertex_fill_color = "red"
        if vertex_size is None:
            vertex_size = prop_to_size(
                g.degree_property_map("out"), mi=2, ma=30, log=False, power=0.5
            )

    if opt == "big":
        vertex_shape = None
        vertex_size = 5
        vertex_fill_color = "blue"
        vertex_text = g.vertex_index
        vertex_text_position = 1
        vertex_font_size = 9

    # vertex_text = g.vertex_index
    # vertex_text_position = 2
    # vertex_text_offset=[50,0]
    # vertex_font_size = 10
    # ecmap = get_cmap('viridis')
    if edge_color is None:
        edge_color = [0, 0, 0, 0.5]

    if edge_pen_width is None:
        edge_pen_width = 3


    return graph_draw(
        g,
        pos,
        bg_color=bg_color,
        fit_view=fit_view,
        output=output.as_posix() if isinstance(output, Path) else output,
        output_size=output_size,
        vcmap=vcmap,
        vertex_fill_color=vertex_fill_color,
        vertex_size=vertex_size,
        vertex_text=vertex_text,
        vertex_text_position=vertex_text_position,
        vertex_font_size=vertex_font_size,
        ecmap=ecmap,
        eorder=eorder,
        edge_color=edge_color,
        edge_pen_width=edge_pen_width,
        vertex_shape=vertex_shape,
        **kwargs,
    )


def set_vertex_position(g, vweight=None, eweight=None):
    return sfdp_layout(
        g,
        vweight=vweight,
        eweight=eweight,
        K=1,  # optimal lenght edges (5)
        C=10,  # relative repulsive force
    )


def print_scc(g, minsize=5, fname="scc.pdf"):
    """
    separate the graph g in strongly connected components.
    Only keep those with more than minsize element
    Label them in the vpropertie scc.
    print to the filename fname{i} the com
    """
    # strongly connected components
    g.vertex_properties["scc"] = g.new_vertex_property("int")
    scc, hist = label_components(g, vprop=g.vp.scc, directed=True)
    # import ipdb; ipdb.set_trace()
    bname = Path("Images").joinpath(fname)
    sccL = pd.Series(scc.a)
    i = 0
    for gp, frame in sccL.groupby(scc.a):
        i += 1
        print(f"i={i}/{len(sccL.groupby(scc.a))}", end="\r")
        g.vp.filtre.a = False
        for v in list(frame.index):
            g.vp.filtre[v] = True
            g.set_vertex_filter(g.vp.filtre)
        if sum(g.vp.filtre.a) > 5:
            fname = bname.parent.joinpath(f"{bname.stem}{i}{bname.suffix}")
            logging.info(f"wrote={fname}")
            _ = drawg(
                g,
                vertex_shape=None,
                vertex_size=5,
                # vertex_fill_color=g.vp.color,
                vertex_text=g.vertex_index,
                vertex_text_position=1,
                vertex_font_size=9,
                fname=fname.as_posix(),
            )


def get_path_from_vertex(vlist, g):
    """
    return a list of edge from a list of vertex
"""
    edgeIdx = zip(vlist[:-1], vlist[1:])
    return [g.edge(s, t) for s, t in edgeIdx]


def keep_rankiest_component(g, rank=1):
    """
    Set a graph filter on the rankiest biggest component
    """
    g.clear_filters()
    # filtering to keep bigest component
    scc, hist = label_components(g, directed=False)
    sidx = np.argsort(hist)
    # set true only for the rankist bigest component
    g.vp.filtre.a = scc.a == sidx[-1 * rank]
    g.set_vertex_filter(g.vp.filtre)
    return g


def get_component(rank, g):
    return keep_rankiest_component(g, rank)


def has_dim_one(pdO):
    """
check if one of the dim of the pd object is one
"""
    return 1 in pdO.shape


def is_number(elt):
    try:
        float(elt)
        return True
    except ValueError:
        return False


def updating_prop(g, df):
    """
    updateing properties of the network's edges and vertices
    """

    P = {}
    try:
        # #### Filtres
        g.edge_properties["filtre"] = g.new_edge_property("bool")
        g.vertex_properties["filtre"] = g.new_vertex_property("bool")
        # on suprime les noeuds sans attaches
        deg = g.degree_property_map("total")

        def is_deg_null(v):
            return deg[v] != 0

        g.vp.filtre.a = list(map(is_deg_null, g.vertices()))

        g.set_vertex_filter(g.vp.filtre)

        # #### Vertices prep
        # ### degre related props
        P["vmrcuEdts"] = prop_to_size(g.vp.mrcuEdts, mi=0, ma=1, log=False, power=1)
        P["vdegall"] = prop_to_size(
            g.degree_property_map("total"), mi=2, ma=10, log=False, power=2
        )
        P["vdegin"] = prop_to_size(
            g.degree_property_map("in"), mi=2, ma=20, log=False, power=2
        )
        P["vdegout"] = prop_to_size(
            g.degree_property_map("out"), mi=2, ma=10, log=False, power=2
        )
        P["vdegoutin"] = g.new_vertex_property("float")
        P["vdeginout"] = g.new_vertex_property("float")
        P["vdegoutin"].a = (P["vdegout"].a + 1) / (P["vdegin"].a + 1)
        msk = P["vdegoutin"].a < 1
        P["vdegoutin"].a[msk] = 0.1
        P["vdeginout"].a = (P["vdegin"].a + 1) / (P["vdegout"].a + 1)
        msk = P["vdeginout"].a < 1
        P["vdeginout"].a[msk] = 0.1
        P["vmsgMREd"] = prop_to_size(g.vp.mrcuEdts, mi=1, ma=10, log=False, power=1)

        # #### Edges prep
        P["eweight"] = prop_to_size(g.ep.weight, mi=1, ma=20, log=False, power=2)
    except ValueError as ve:
        if "zero-size array" in ve.__repr__():
            # c'est que le graph est vide
            le = len(g.get_edges())
            lv = len(g.get_vertices())
            logging.error(f"Graph with edges {le} et vertices {lv}, {g}")

    # #### COLORS
    vcmap = get_cmap("viridis")
    # ecmap = get_cmap("plasma")

    # create a color mapping of even spaced colors orders by tid ages
    # une interpolation est mieux ici
    for v in g.vertices():
        #    g.vp.color[v] = vcmap(line_interpolation(g.vp['msgMREd'][v]))
        g.vp.color[v] = vcmap(P["vmrcuEdts"][v])

    return P


# ################ a revoir
# def update_edge_connexion(g, data, vi, vj):
#     e = g.edge(vj, vi)
#     propsval = {f"s_{etype}": seuil}
#     for key in propskeys:
#         propsval[key] = data.loc[key]

#     g.ep[seuil_prop][e] += seuil
#     #    g.ep["msgMREd"][e] = max([data.msgMREd, g.ep["msgMREd"][e]])
#     # idéalement chaque edge garde un historique de ses modifications
#     return None


# def add_edge_connexion(g, data, vi, vj, seuil, etype):
#     """add an edge and its properties to the graphes"""
#     e = g.add_edge(vj, vi)

#     propsval = {f"s_{etype}": seuil}
#     for key in ["msgID", "threadID", "msgMREd", "wtext"]:
#         propsval[key] = data.loc[key]

#     add_edge_props(g, e, propsval)
#     return None
