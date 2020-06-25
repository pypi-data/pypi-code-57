# -*- coding: utf-8 -*-
"""
Making graphes from messages graphes
"""
from typing import (
    List,
    Dict,
    Any,
    Sequence,
    Set,
    Tuple,
    Optional,
    Union,
)
from itertools import chain

from pandas import DataFrame, Series, concat, Index
import numpy as np
from numpy.linalg import norm

from graph_tool import Graph, Vertex, Edge
from graph_tool import EdgePropertyMap, VertexPropertyMap

from graph_tool.topology import vertex_similarity

from KolaViz.LibCircuits.utilsCircuits2 import (
    get_nodeIDs4cond,
    graph_init,
)

PropertyMapT = Union[EdgePropertyMap, VertexPropertyMap]
EPROPNAMES = ["s_topic", "s_temporal", "s_author"]
VertexID = int  # éventuellemet créer un type (mais la comparaison doit être possible)


def main(df: DataFrame, fenetre_tdelta: int = 3) -> Tuple[Graph, Graph]:
    """
    Génère un graphe d'autor après avoir généré un graphe de message
    """
    msgNet = new_graph(df, fenetre_tdelta)

    authorIDs = df.authorID.unique()
    autNet = author_network_init(authorIDs)

    for authID in authorIDs:
        authNode = get_nodeID_from_autID(autNet, authID, asVertex_=True)
        msgIDs = msgIDs_4_authID(msgNet, authID)

        autNet = update_author_node(msgNet, autNet, authNode, msgIDs)

        for msgID in msgIDs:
            msgNode = msgNet.vertex(msgID)
            update_author_link(msgNet, autNet, authNode, msgNode)

    autNet = remove_self_edges(autNet)
    return msgNet, autNet


def new_graph(df, fenetre_tdelta=5):
    g = graph_init(df)
    g = msg_connexion_temporelle(g, fenetre_tdelta)
    g = msg_connexion_topic(g, sameTheme_=True, sameThreadID_=True)
    return g


def author_network_init(authorids: Sequence[Any]) -> Graph:
    """
    Initialise the author network
    """

    # ! authorID != vertex ID
    g = Graph()
    g.add_vertex(len(authorids))

    # ################ Vertex properties ################

    g.vp["authorID"] = g.new_vp("int")
    g.vp.authorID.a = authorids

    # to store the data associated with a user
    g.vp["load"] = g.new_vp("object")

    # ############### edges properties  ################

    g.ep["weight"] = g.new_ep("float")
    g.ep["s_temporal"] = g.new_ep("float")
    g.ep["s_topic"] = g.new_ep("float")
    g.ep["s_author"] = g.new_ep("float")

    g.ep["msgIDs"] = g.new_ep("object")

    # ### les filtres
    g.vp["filtre"] = g.new_vp("bool")
    g.ep["filtre"] = g.new_ep("bool")

    return g


def msgIDs_4_authID(g: Graph, x, filtrer=False):
    """
    filtre g based on authorID x.  return the filterd graph
    """
    g.clear_filters()
    mask = g.vp.authorID.a == x
    if filtrer:
        g.vp.filtre.a = mask
        g.set_vertex_filter(g.vp.filtre)
    return np.argwhere(mask).T[0]


def update_author_node(
    msgNet_: Graph, autNet_: Graph, authNode_: Vertex, msgIDs_, propNames_=None,
):
    """
    Update la propriété d'un noeud du deuxième graphe autNet_ à partir
    des propriétés des noeuds du 1er graphe msgNet_ désigné par propNames_.
    - msgNet_ : c'est le graph de base de message
    """
    if propNames_ is None:
        # suppose que les props de autNet_ sont toutes dans msgNet_
        propNames_ = set(msgNet_.vp.keys()) - {"filtre"}

    autNode: Dict["str", Any] = {}
    for propName in propNames_:
        # on rempli le dico
        for msgid in msgIDs_:
            msgNode = msgNet_.vertex(msgid)
            autNode[propName] = autNode.get(propName, []) + [
                msgNet_.vp[propName][msgNode]
            ]

    # attention modification de la variable passée entrée
    autNet_.vp["load"][authNode_] = autNode

    return autNet_


def update_author_link(
    msgNet_: Graph, autNet_: Graph, authNode_: Vertex, msgNode_: Vertex,
) -> Graph:
    """
    but: créer des liens pondérés entre le noeud auteur et chacun
    des auteurs des messages neighours
    - autNet_ author graph,
    - autNet_ msg graph,
    """

    # pour chaqun des messages du réseaux des message connectés au msgNode
    for msgNeigID in msgNet_.get_out_neighbours(msgNode_):

        # on récupère les ID des auteurs liés
        msgNeigNode = msgNet_.vertex(msgNeigID)
        msgNeigAutID = msgNet_.vp.authorID[msgNeigNode]
        msgNeigAutNodeID = get_nodeID_from_autID(autNet_, msgNeigAutID, asVertex_=True)

        # check if auth neighbour already in authNode_ neighbours
        if msgNeigAutNodeID in autNet_.get_out_neighbours(authNode_):

            # if so we get the edge
            autEdge = autNet_.edge(authNode_, msgNeigAutNodeID, all_edges=True)

            # vérif qu'il n'y en a bien qu'un
            if not isinstance(autEdge, Edge):
                assert (
                    len(autEdge) == 1
                ), f"len(autEdge)={len(autEdge)} pour {autEdge} but should be one."
                autEdge = autEdge[0]

        else:
            autEdge = autNet_.add_edge(authNode_, msgNeigAutNodeID)

        # on récupère le message et son message voisin
        msgEdges = msgNet_.edge(msgNode_, msgNeigNode, all_edges=True)

        # et on met à jour les propriété associé chez les noeuds auteur à partir du message
        autNet_ = update_autEdges_from_msgEdges(
            autNet_, autEdge, msgNet_, msgEdges, propNames_=["s_temporal", "s_topic"],
        )

        if autNet_.ep["msgIDs"][autEdge]:
            autNet_.ep["msgIDs"][autEdge] |= {msgNeigID}
        else:
            autNet_.ep["msgIDs"][autEdge] = {msgNeigID}

        # seul reste la mesure de sim dépendante uniquement du network auteur
        # faite plus haut dans le stack

    return autNet_


def link_similar_autNodes(
    autNet_: Graph,
    simFactor_: float = 1,
    simType_: str = "jaccard",
    epropName_: str = "s_author",
):
    """
    Connect similar nodes in the structural simtype way.
    
    - autNet_: the graph to rewrire
    - simFactor_: the minimal simFactor_ to allow connection
    - simType_: the way to measure similarity
    - epropName_: the name of the edge properties to update
    """
    # renvois un ..
    simiNodes = vertex_similarity(autNet_, simType_, eweight=autNet_.ep.weight)

    # on récupère la similarité médiane comme val de ref pour
    # définir ensuite notre seuil à partir du quel on connect les utilisateurs

    _medianSimilarity = similarity_scores(autNet_, simiNodes)
    medianSimilarity = _medianSimilarity.median()
    seuil2Similarity = medianSimilarity * simFactor_

    # on effectue les connexions
    for i, nodeID in enumerate(autNet_.get_vertices()):
        # on ignore les noeuds qui n'on aucune similarité ou qui sont identique à nodeID
        # value is a mask of bool same size as simiNodes, ie same as autNet_

        simiValues = mask_values(
            simiNodes.get_2d_array([nodeID])[0], values2Mask_=[0, 1],
        )

        candidateNodeIDs = element_set_in_sequence(np.argwhere(simiValues))

        for j, candidateNodeID in enumerate(candidateNodeIDs):
            # pour chaque candidat on connecte si sa similarité est plus grande
            # que le seuil
            if simiValues[j] >= seuil2Similarity:
                # creation ou update
                e = get_create_edge(autNet_, nodeID, candidateNodeID)
                autNet_.ep[epropName_][e] += simiValues[j]

    return autNet_


def update_autEdges_from_msgEdges(
    autNet_: Graph,
    autEdge_: Edge,
    msgNet_: Graph,
    msgEdges_: Sequence[Edge],
    propNames_=["s_temporal", "s_topic"],
) -> Graph:
    """
    Update the autor Edge properties propNames_ with the sum of those of the msgNet_ msgEdges_

    """
    for propName in propNames_:
        autNet_.ep[propName][autEdge_] += sum(
            [msgNet_.ep[propName][e] for e in msgEdges_]
        )

        autNet_.ep["weight"][autEdge_] += autNet_.ep[propName][autEdge_]
    return autNet_


def msg_connexion_temporelle(msgNet_: Graph, fenetre_tdelta: float = 1) -> Graph:
    """
    Connect les messages selon la fenetre tdelta sans tenir compte des thread ou autre
    """

    # On défini une fenetre temporelle pour lier les messages
    # On lie tout les message qui sont plus vieux que ts l'age du message en question
    # et ts - largeur fenetre.
    # La taille de la fenetre temporelle est un facteur de la fenetre mediane.
    # entre deux messages consécutifs.
    sorted_ts = np.array(sorted(msgNet_.vp.msgMREd.a))

    def _delta_ts(array_ts_=sorted_ts):
        return array_ts_[1:] - array_ts_[:-1]

    tdelta_median = np.median(_delta_ts())
    tdelta = tdelta_median * fenetre_tdelta

    # import ipdb; ipdb.set_trace()

    for i, v in enumerate(msgNet_.vertices()):

        # on récupère le temps d'édition de v
        msgts = msgNet_.vp.msgMREd[v]

        # on calcule la fenêtre
        window_ts = msgts - tdelta

        # on récupère messages qui sont dans la fenêtre temporelle
        omsgID = get_nodeIDs4cond(
            msgNet_,
            cond=(msgNet_.vp.msgMREd.a > window_ts) & (msgNet_.vp.msgMREd.a < msgts),
        )

        for j, msgID in enumerate(omsgID):
            print(
                f"{i, j} / {len(omsgID), msgNet_.num_vertices()}", end="\r",
            )
            # l'autre msg
            omsg = msgNet_.vertex(msgID)
            e = get_create_edge(msgNet_, v, omsg)

            # ajout d'une force à ce lien
            # on prend une fonction qui tend doucement vers 0 quand le tdelta s'accroit
            time_strength = 1 / np.log(np.e + msgts - msgNet_.vp.msgMREd[omsg])
            msgNet_.ep["s_temporal"][e] = time_strength

            # on garde le set des msgs Ids dans l'edge pour une compilation dans le sociogram
            if msgNet_.ep["msgIDs"][e]:
                msgNet_.ep["msgIDs"][e] |= {msgID}
            else:
                msgNet_.ep["msgIDs"][e] = {msgID}

    return msgNet_


def msg_connexion_topic(
    msgNet_: Graph, sameTheme_: bool = True, sameThreadID_: bool = True,
):

    for msgNode in msgNet_.vertices():
        # pour chaque noeud
        # récupérer les threadIDs
        threadID = msgNet_.vp.threadID[msgNode]

        # récupérer les autres noeuds ayant le même threadID
        # pour chaque noeud w avec le même threadID
        # vérifier qu'il a été écrit avant v et qu'il a la même nmf_ctg
        # les relier v -> w

        msgHasThreadID = msgNet_.vp.threadID.a == threadID
        if sameThreadID_:
            nodeIDs = get_nodeIDs4cond(msgNet_, cond=msgHasThreadID)
        else:
            nodeIDs = set([msgNet_.vertex_index[v] for v in msgNet_.vertices()])

        nodeIDs -= {msgNode}

        for v in nodeIDs:
            earlier = msgNet_.vp.msgMREd[v] < msgNet_.vp.msgMREd[msgNode]
            if sameTheme_:
                same_category = msgNet_.vp.nmf_ctg[v] == msgNet_.vp.nmf_ctg[msgNode]
            else:
                same_category = True
            if earlier and same_category:
                e = get_create_edge(msgNet_, msgNode, v)
                msgNet_.ep["s_topic"][e] = 1
    return msgNet_


def mask_values(
    ar: np.array,
    values2Mask_: List[Any] = [0],
    maskNaN_: bool = True,
    returnType_: str = "aronly",
):
    """
    Create a mask of ar.shape masking all values2Mask_ in values2Mask_ from ar
    is masknpnan, mask those too
    returnType_ can be aronly for array only, maskonly for mask only or both
    """
    msk = np.ones(ar.shape).astype(bool)

    for x in values2Mask_:
        msk &= ar != x
    if maskNaN_:
        msk &= np.invert(np.isnan(ar))

    if returnType_ == "aronly":
        return ar[msk]
    elif returnType_ == "maskonly":
        return msk
    else:
        return ar[msk], msk


def not_null_nor_one_values(propMap_: PropertyMapT, nodeID_: int):
    """
    Create a mask for a 2d propMap_, masking null and 1 value and np.nan
    """
    return mask_values(
        propMap_.get_2d_array([nodeID_])[0], values2Mask_=[0, 1], returnType_="aronly",
    )


def similarity_scores(autNet_: Graph, eProp: EdgePropertyMap):
    """
    Return all similarity mesure for the graph autNet_,
    - eprop = simiNodes
    enable distribution study and find median value to do the social linking
    """
    scores: List[Any] = []

    for autNodeID in autNet_.get_vertices():
        score = not_null_nor_one_values(eProp, autNodeID)

        if len(score):
            scores += list(score)

    return Series(scores)


def get_strength_(
    sociogram_: Graph, circuit_: List, propNames_: List[str] = EPROPNAMES,
) -> Tuple[Dict[str, float], Any]:
    """
    Calcule la force d'un circuit, ou d'un chemin selon 
    les dimensions dans propNames
    Si il n'y a pas de circuit renvois un dictionnaire avec
    les propnames et des 0
    """
    if len(circuit_) < 2:
        return (
            {pName: 0.0 for i, pName in enumerate(propNames_)},
            [],
        )

    edgeliste = edges_in_circuit(sociogram_, circuit_)

    # liste de weights pour cette liste d'edges.
    # shape len(edgeliste) x len(propNames_)
    propWeights = edge_props_in_circuit(sociogram_, edgeliste, propNames_)

    # on fait la moyenne des forces des edges du circuit selon chaque dimensions
    weight = np.average(propWeights, axis=0)

    # on renvois les forces et les edges pour ce circuits
    return (
        {pName: weight[i] for i, pName in enumerate(propNames_)},
        edgeliste,
    )


def circuit_strength(
    sociogram_: Graph, circuits_: Series, concat_: bool = True, propNames_=EPROPNAMES,
) -> DataFrame:
    """
    Renvois la force moyenne (normalisée 2) de chaque circtuit 
    dans circuits_
    On aura en sortie un DataFrame avec une colonnes, pour chaque
    epropname et une avec un liste d'edges représentant le circuit
    """
    _res: List[Dict[str, Any]] = []

    for circuit in circuits_:

        forces, edgeliste = get_strength_(sociogram_, circuit, propNames_)

        _res.append(forces)

        # on ajoute les edges au dernier dico ajouté à _res
        _res[-1]["edges"] = edgeliste

    res = DataFrame(_res)

    if concat_:
        res = concat([circuits_, res], axis=1)
        old_col = list(res.columns)
        old_col[0] = "autNodeID"
        res.columns = old_col

    # #### normalisation
    # on (re)normalise les strengths des edges qui reste

    res.loc[:, propNames_] /= norm(res.loc[:, propNames_].values, 2, axis=0)

    res.index.name = "cirID"
    return res


def edge_props_in_circuit(
    net_: Graph, edgelist_: List[Edge], propNames_: List[str] = EPROPNAMES,
) -> np.array:
    """
    Renvois les valeurs DES propriétes propNames_des edges de edgelist_
    utilisé pour les propriété des circtuis.

    return array of shape len(edgeliste) x len(propNames_)
    """
    assert None not in edgelist_, f"Need to filter None from edgelist_"

    n = len(edgelist_)
    p = len(propNames_)
    assert n > 0, f"edgelist_={edgelist_} check len"

    arr = np.empty((n, p))

    try:
        for i, e in enumerate(edgelist_):
            for j, pName in enumerate(propNames_):
                arr[i, j] = net_.ep[pName][e]
    except Exception as ex:
        import pdb

        pdb.set_trace()
        raise (ex)

    return arr


def edges_in_circuit(net_: Graph, circuit: List[Union[int, Vertex]]) -> List[Edge]:
    """
    renvois les edges qui compose le circuit c
    """
    circuit_ext = circuit + [circuit[0]]  # c extended

    edges = [net_.edge(s, t) for s, t in zip(circuit_ext[:-1], circuit_ext[1:])]

    # return the list without None
    return [e for e in edges if e is not None]


def edges_with_prop(net_: Graph, epropName_: str, asEdge_=True) -> List:
    """
    return a liste of  edges (Edges) in the Graphe for which epropName_ is not 0.
    If as edges is false return the id of the edges only
    """
    edgeIDs = np.argwhere(net_.ep[epropName_].a).T[0]

    def get_edgeID(edgeID: int) -> Edge:
        return get_edge(net_, edgeID)

    return list(map(get_edgeID, edgeIDs)) if asEdge_ else list(edgeIDs)


def element_set_in_sequence(sequence_: Sequence[Any] = []):
    """
    Return the set of edges in sequence_.  sequence_ can be a liste
    of edges or a liste of edge id
    usage exemple mc.element_set_in_sequence(net_, cs.edges.values)
    """
    return set(chain.from_iterable(sequence_))


def get_nodeID_from_autID(
    g: Graph, authorID_: int, asVertex_: bool = True
) -> Union[Vertex, int]:
    """
    given the author id, récupère l'id du noeud dans le graphe g
    Il y a une bijection entre node id et author id sinon erreur
    """
    mask = g.vp.authorID.a == authorID_
    nodeID = np.argwhere(mask)[0, 0]
    return g.vertex(nodeID) if asVertex_ else nodeID


def get_create_edge(
    G_: Graph, u: Union[Vertex, VertexID], v: Union[Vertex, VertexID],
) -> Edge:
    """
    Get or create an edge between u and v.
    suppose that the graph does note acept multi edges
    """
    e = G_.edge(u, v, all_edges=True)

    assert (
        len(e) < 2
    ), f"This methods is only for graph with no parallels edges. Check edges={e}"

    if not e:
        return G_.add_edge(u, v)

    return e[0]


def get_chaine_author_circuits(net, c):
    """
    Renvois la liste d'authorID correspondant au nodeID dans le circuit c
    """
    res = []
    for nodeID in c:
        res.append(net.vp.authorID[net.vertex(nodeID)])


def get_edge(net_: Graph, eid: int, asEdge_: bool = True):
    """
    return the edge with eid, as an edge or a tuple
    """
    s, t = net_.get_edges()[eid]
    return net_.edge(s, t) if asEdge_ else (s, t)


def get_author_in_circuit(net_: Graph, edgeList_, asVertex_: bool = True):
    """
    Soit une liste d'arrête, renvois le set des auteur (sommet) mentionné.
    if asVertex_=False renvois les ID
    """
    authors: Dict[str, Set[Any]] = {}
    for i, c in enumerate(edgeList_):
        for s, t in c:
            if not asVertex_:
                s, t = net_.vertex_index[s], net_.vertex_index[t]
            authors[f"g{i}"] = authors.get(f"g{i}", set([s, t])) | set([s, t])
    return authors


def get_self_edges(g):
    return [e for e in g.edges() if e.source() == e.target()]


def membership_attributions(net_: Graph, circuits_: Sequence) -> Series:
    """
    for chaque element of circuits_ which is a Serie of vertices,
    identifie les sommets (ie les auteurs) et leur attribue un groupe.
    renvois une pd.Serie auteur id et ensegroup set auquels il appartiennent
    """
    _memberShip: Dict[int, Set[Any]] = {}

    for cid, vertices in enumerate(circuits_):
        for nodeID in vertices:
            # met dans membership pour chaque auteur id (nodeID)
            # un set des circuit id nommé gc_id # group collectif_id

            _memberShip[nodeID] = _memberShip.get(nodeID, set()) | set([cid])

    memberShip = Series(_memberShip, name="group_attributions")
    memberShip.index.name = "autID"

    memberShip = ungroup_serie_of_sequence(
        memberShip, names_=("autID", "cirID"), title_="aut&cir"
    )

    return memberShip


def ungroup_serie_of_sequence(
    membership: Series,
    names_: Tuple[str, str] = ("col1", "col2"),
    title_: Optional[str] = None,
) -> DataFrame:
    """
    transforme une serie de sequence en dataframe avec deux colonnes
    ... un genre de unstack
    - nome le colonnes avecs names_ et l'index avec title_
    """

    _res: Dict[str, List] = {names_[0]: [], names_[1]: []}

    for autID, cirIDs in membership.items():
        _res[names_[0]] += [autID] * len(cirIDs)
        _res[names_[1]] += cirIDs

    index = Index(list(range(len(_res[names_[0]]))), name=title_)

    return DataFrame(_res, index)


def is_iterable(obj, raiseex=None):
    """
    test if the object is iterable using duck typing
    """
    try:
        iter(obj)
        if "notuniq" in raiseex:
            assert len(obj) == 1, f"len(obj)={len(obj)} should be one."
        elif "iter" in raiseex:
            raise Exception(f"obj={obj} should not be iterable")

        return True
    except TypeError as te:
        if "not iterable" in te.__str__():
            return False
        else:
            raise (te)


def remove_self_edges(g: Graph):
    """
    returns a copy of g where self edges are removed. use a filter for this
    """
    new_g = Graph(g, prune=True)
    # récupérer les self edges
    for se in get_self_edges(new_g):
        new_g.ep.filtre[se] = True
    new_g.set_edge_filter(new_g.ep.filtre, inverted=True)
    return Graph(new_g, prune=True)


# ############### not used yes ################


def edge_prop_in_circuit(
    net_: Graph, edgesList_: Sequence[Edge], pName_: str
) -> Sequence[Any]:
    """
    renvois les valeurs de la propriété pName_ des edges donnés dans edgesList_
    """
    return [net_.ep[pName_][e] for e in edgesList_]


def get_autID_from_nodeID(net_: Graph, nodeID_: int) -> Any:
    return net_.vp["authorID"][nodeID_]


def get_autIDs_from_nodeIDs(
    net_: Graph, sequence_: Sequence[Union[int, Vertex]]
) -> List[int]:
    return [get_autID_from_nodeID(net_, nodeID) for nodeID in sequence_]


def get_msgid_author_circuit(autNet_: Graph, circuits_: Sequence[Edge]) -> Set:
    """
    Renois l'ensemble des msgID qui on participé à la création du circuits
    """
    res: Set[int] = set()

    for e in circuits_:
        msgIDs = autNet_.ep.msgIDs[e]
        if msgIDs is not None:
            res |= set([m for m in msgIDs])

    return res
