#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Computes circuits for dynacol."""
import sys
import logging
import json
import argparse
from pandas import DataFrame, Series, Timestamp
from typing import Dict, List, Any, Optional, Sequence
from numpy.linalg import norm
from numpy import round, array

from graph_tool import Graph

from KolaViz.koNMF import main as mainNMF
from KolaViz.Lib.fnames import (
    create_dir,
    save_pickle,
    read_pickle,
    prepare_cir_dft_name,
)
from KolaViz.Lib.outilsKoNLP import coerce_string2number
from KolaViz.LibCircuits.circuit_detector import circuit_enumeration4
from KolaViz.Lib.model import (
    SAMETHREADID_DFT,
    SAMETOP_DFT,
    SIMTYPE_DFT,
    SIMFACTOR_DFT,
    CIR_STG_DFT,
    CIR_ACTION_DFT,
    CIR_DRAW_DFT,
    CIR_ENUMERATION_DFT,
    CIR_METHODS_DFT,
    CIR_OUTDIR_DFT,
    CIR_WTDELTAS_DFT,
    LANG_DFT,
    LOGLEVEL_DFT,
    TOK_PREFIX_DFT,
    TOK_FNAME_DFT,
    VEC_ALPHA_DFT,
    VEC_L1RATIO_DFT,
    VEC_REDUX_DFT,
    COURSE_DFT,
)
from KolaViz.LibCircuits.utilsCircuits2 import (
    graph_init,
    drawg,
)
from KolaViz.LibCircuits.network_utils import (
    ungroup_serie_of_sequence,
    get_strength_,
    get_msgid_author_circuit,
    author_network_init,
    circuit_strength,
    get_nodeID_from_autID,
    link_similar_autNodes,
    membership_attributions,
    msgIDs_4_authID,
    msg_connexion_temporelle,
    msg_connexion_topic,
    remove_self_edges,
    update_author_link,
    update_author_node,
)

"""Regroupe les fonctions pour générer les circuits des dynamiques collectives"""

# ### types
userID = int
aCircuit = List[userID]
desCircuits = List[aCircuit]
dic2Circuits = Dict[str, desCircuits]

circuitID = int
aMembership = List[
    circuitID
]  # un liste d'id de circuits auxquel appartient l'utilisateur
desMembership = List[aMembership]
dic2Membership = Dict[str, desMembership]

EPROPNAMES = ["s_topic", "s_temporal", "s_author"]


def circuits(
    action_: str,
    kwargsV,
    data_=None,
    course_: str = COURSE_DFT,
    circuitLen_: int = CIR_ENUMERATION_DFT,
    circuitStg_: int = CIR_STG_DFT,
    draw_: bool = CIR_DRAW_DFT,
    lang_: str = LANG_DFT,
    methods_: List[str] = CIR_METHODS_DFT,
    outdir_=CIR_OUTDIR_DFT,
    w_tdeltas_: List[Any] = CIR_WTDELTAS_DFT,
    simFactor_: float = SIMFACTOR_DFT,
    simType_: str = SIMTYPE_DFT,
    sameTop_: bool = SAMETOP_DFT,
    sameThreadID_: bool = SAMETHREADID_DFT,
) -> Dict[str, Any]:
    """
    Charge ou build les données et calcule le graphes des dynamiques
    collectives potentielles
    - nécessite un fichier tokenisés ou un dictionnaire pour récupérer les données
    à partir du fichiers vectorisés
    - methods = ["prec1", "prec2", "prec3", "prec5", "prec8", "starall", "all"]
    - action : readC (try to read circuit files else build it
    - circtuiStg_: limit the strenght of circuit.  if 0, no cond.
    -circuitLen_: limit the length of circuit. if 0 no cond.
    """

    # Création d'un nom de fichiers pour stocker ou lire le graphes
    # si read, une première lecture
    load, name, data = mainNMF(action_="read", **kwargsV)

    if data_ is None:
        data_ = data

    outdir, fname = prepare_cir_dft_name(outdir_=outdir_, **kwargsV)

    # deuxième lecture ici
    res: Dict[str, Any] = {"nothing": None}

    if "read" in action_:
        res = read_pickle(fname)

    elif "build" in action_:
        graphes, circuits = screen_circuits(
            data_,
            circuitLen_=circuitLen_,
            circuitStg_=circuitStg_,
            draw_=draw_,
            methods_=methods_,
            outdir_=outdir,
            outstem_=f"{course_}_{lang_}",
            w_tdeltas_=w_tdeltas_,
            simFactor_=simFactor_,
            simType_=simType_,
            sameThreadID_=sameThreadID_,
        )

        # on met le temps au bon format avant l'écriture
        # sur le disque et le retour fonction

        data_.loc[:, "msgMREd"] = data_.msgMREd.apply(lambda d: Timestamp(d * 10e8))
        if "save" in action_:

            # on coerce les Edges en couple d'int pour
            # d'eventuelle sauvegarde. Sinon pas picklable
            def to_id_list(circuit):
                return [(int(e.source()), int(e.target())) for e in circuit]

            # pour cela il les faut récupére dans chacun
            # des dictionnaires
            # en veillant à ne pas modifier la copie qui va
            # être retournée par# la fonction
            new_circuits: Dict[str, DataFrame] = dict()

            for idx, circuit in circuits.items():
                stg = circuit["stg"].copy()
                stg.loc[:, "edges"] = stg.edges.apply(to_id_list)
                new_circuits[idx] = {
                    "stg": stg,
                    "aut": circuit["aut"],
                    "msg": circuit["msg"],
                }

            res = {
                "graphes": graphes,
                "circuits": new_circuits,
                "data": data_,
            }

            save_pickle(res, fname)

        res = {
            "graphes": graphes,
            "circuits": circuits,
            "data": data_,
        }

    return res


def etendre_df(
    df_: DataFrame,
    colWithSeq_: str,
    title_: Optional[str] = None,
    dropPrevIndex_: Optional[str] = None,
):
    """
    - colWithSeq_ est le nom d'une colonne avec une sequence.
    pour chaque élément de la séquence créer une ligne dans la dataFrame.
    - dropPrevIndex_ pour supprimer la colonne de jonction
    Renvois la nouvelle dataFrame
    """
    res = ungroup_serie_of_sequence(
        df_.loc[:, colWithSeq_], names_=("prev_index", colWithSeq_), title_=title_,
    )
    res = df_.merge(res, how="right", left_index=True, right_on="prev_index")

    if dropPrevIndex_ is not None:
        res = res.drop("prev_index", axis=1)

    return res


# @arg_force_type_check(
#     args_types={
#         "data_": DataFrame,
#         "circuitLen_": int,
#         "circuitStg_": int,
#         "draw_": bool,
#         "methods_": List[str],
#         "outdir_": str,
#         "outstem_": str,
#         "w_tdeltas_": List[float],
#         "simFactor_": float,
#         "simType_": str,
#         "sameTop_": bool,
#         "sameThreadID_": bool,
#     }
# )
def screen_circuits(
    data_: DataFrame,
    circuitLen_: int = 4,
    circuitStg_: int = 3,
    draw_: bool = False,
    methods_: List[str] = ["all"],
    outdir_=".",
    outstem_: str = "ddl_c18_fr",
    w_tdeltas_: List[float] = [1],
    simFactor_: float = 1,
    simType_: str = "jaccard",
    sameTop_: bool = True,
    sameThreadID_: bool = True,
):
    """
    Loop the create_sociogram for several methods and window timedeltas.
    Returns dictionnaries of graphes and circuits if circuits_ > 0
    - outstem_ to build the file name if draw is True
    - w_tdeltas, a list of time windows to split the graph to draw temporal graphs
    exg 4W
    - circuitStg_:
    - circuitLen_:
    """

    # si il y avait un regoupement avant les messages et catégorie
    # pourrait faire en batch ??
    circuits: Dict["str", Dict[str, DataFrame]] = {}
    graphes = {}
    outdir = create_dir(outdir_)

    # crée des graphes en faisant varier la méthods de connexion
    # intra discussion

    for method in methods_:

        # et en faisant varier la méthode de connexion temporelle
        # wts = window temporelle,

        for wts in w_tdeltas_:
            idx = f"{outstem_}_{method}_{wts}ft"
            autNet, pos = create_sociogram(
                data_,
                method,
                wts,
                draw_=draw_,
                draw_fname_=outdir.joinpath(f"graph_{idx}.pdf"),
                simFactor_=simFactor_,
                simType_=simType_,
                sameTop_=sameTop_,
                sameThreadID_=sameThreadID_,
            )

        # save the graph
        graphes[idx] = autNet

        if circuitLen_ or circuitStg_:
            # on enumère les circuits (circuit == liste de uid)
            # puis on ajoute la réciproque (uid -> liste cirid)

            # dans un premier temps on crée un fichier où
            # sauvegarder les circuits, afin d'alléger la mémoire
            fname = outdir_.joinpath(f"circuits_{idx}.json")

            # on défini des conditions d'arrêt de la recherche de
            # cycles.  ie. une sur la force moyenne du cycle,
            # l'autre sur sa longeur
            stopcond: List = list()
            if circuitStg_:

                def _strength_cond(cir):
                    return strength_cond(cir, autNet, EPROPNAMES)

                stopcond.append((_strength_cond, "lt", circuitStg_,))

            if circuitLen_:
                stopcond.append((len, "lt", circuitLen_))

            # we stop for any of the above condition
            stopcond.append("any")

            # coeur de l'énumération
            logging.info("Starting Circuit enumeration")

            enumeration = enumerate_circuits(autNet, stopcond_=stopcond, fname_=fname)
            logging.info(
                f"\n{len(enumeration)} circuits with cond"
                f" {stopcond} computed and saved in {fname}"
            )

            # ainsi que la force de chaque circuit
            strength = circuit_strength(
                sociogram_=autNet, circuits_=Series(enumeration), concat_=True,
            )

            # on ajoute l'ensemble des messages qui ont participé au circuits.
            # il peut y avoir liens qui ne sont pas créés pars des messages
            # c'est le cas de ceux issue de la similarité entre les auteurs
            def get_circuit_messages(circuits_: Sequence, G_: Graph = graphes[idx]):

                return get_msgid_author_circuit(graphes[idx], circuits_)

            strength.loc[:, "msgIDs"] = strength.edges.apply(get_circuit_messages)
            strength = strength.reset_index()

            # puis on retourne aussi la liste de circuits associé aux userID
            autCirIDs = membership_attributions(net_=autNet, circuits_=enumeration)

            # on extrait les messages des circuits
            cirMsgIDs = ungroup_serie_of_sequence(
                strength.msgIDs, names_=("cirID", "msgID"), title_="cir&msgIDs",
            )

            circuits[idx] = {
                "stg": strength,
                "aut": autCirIDs,
                "msg": cirMsgIDs,
            }

            #    return graphes

    return graphes, circuits if circuits else dict()


def strength_cond(
    circuit_: List[int], sociogram_: Graph, propNames_: List[str] = EPROPNAMES,
):
    """
    Renvois la force d'un circuit_ du sociogram_.

    Fais la moyennes des trois forces.
    selon les propNames_
    """
    try:
        stgs = get_strength_(sociogram_, circuit_, propNames_)
        stg = array(list(stgs[0].values())).mean()
    except Exception as ex:
        import pdb

        pdb.set_trace()
        raise (ex)

    return stg


def enumerate_circuits(G: Graph, stopcond_, fname_) -> List[aCircuit]:
    """
    Enumerate the circuits in graph G limiting with the stopcond
    - stopcond default : (len, 'lt', circuit_)
    Save the circuit_enumeration4 will write them on the disk.
    at the end, we read the file and update the
    return a tuple idx and the enumeration ton the disk,
    the reload it reto circuits of length circuitLen_
    """
    E, V = len(G.get_edges()), len(G.get_vertices())
    # ! 12/19 run out of memory on machine with 256G Ram !!
    logging.debug(
        f"Starting circuits enumeration with (E+V) = {E}+{V}={E+V} à mulitplier par"
        " le nombre de circuits (existant) pour trouver la complexité."
        f"stopcond_={stopcond_}, fname_={fname_}"
    )

    # does the enumeration and write the result to the file fname
    circuit_enumeration4(G, stopcond_=stopcond_, fname_=fname_)

    circuits_idx: List[aCircuit] = list()
    # on reli ce qui a été écrit sur le disque.
    # c'est pour éviter de garder tout en mémoire
    with open(fname_, "r") as f:
        logging.debug("Loading circuits enumeration from file")
        ligne = f.readline()
        while ligne:
            circuits_idx += [json.loads(ligne.strip("\n"))]
            ligne = f.readline()

    return circuits_idx


def create_sociogram(
    data_: DataFrame,
    method_: str = "all",
    fenetre_tdelta_: float = 1,
    draw_: bool = False,
    draw_fname_=None,
    simFactor_: float = 1,
    simType_: str = "jaccard",
    sameTop_: bool = True,
    sameThreadID_: bool = True,
):
    """
    Main step to create all edges for all users in a course.

    - initialise the graph, make links and update properties
    - methode = "all" (ou prev1, prev2 ect...) façon de lier les messages d'une
    même discussion
    - fenetre_tdelta_:int (def 1). Durée en fenetre temporelle d'écart median entre
    les étiquettes temporelles de deux messages quelconques devant être liés.
    - draw_, Faut-il dessiner le graphe ou non?
    - draw_fname_: nom du fichier à écrire si draw_ is True
    """
    if draw_fname_ is not None:
        assert (
            draw_
        ), f"Confit des les options draw_={draw_} et draw_fname={draw_fname_}."
    # Création du réseau de messages

    msgNet = new_message_network(
        data_, fenetre_tdelta_, sameTop_=sameTop_, sameThreadID_=sameThreadID_,
    )

    # Création du réseau de auteurs
    msgAut = new_author_network(msgNet, data_, simFactor_=simFactor_, simType_=simType_)

    if draw_:
        pos = drawg(msgAut, fname=draw_fname_)
        return (msgAut, pos)
    else:
        return (msgAut, False)


def new_message_network(
    data: DataFrame,
    fenetre_tdelta_: float = 4,
    sameTop_: bool = True,
    sameThreadID_: bool = True,
) -> Graph:
    """
    crée le réseau des messages selon les deux dimensions
    - temporelle définie par fenêtre_tdelta_
    - et topique same topic, same thread id
    Renvois le network
    """
    ntw = graph_init(data)
    ntw = msg_connexion_temporelle(ntw, fenetre_tdelta_)
    ntw = msg_connexion_topic(ntw, sameTheme_=sameTop_, sameThreadID_=sameThreadID_)

    return ntw


def new_author_network(
    msgNet_: Graph,
    data_: DataFrame,
    noSelfEdge_: bool = True,
    simType_: str = "jaccard",
    simFactor_: float = 1,
) -> Graph:
    """
    Make the author-author network based on a message network.

    - msgNet_ :  un graphe basé sur les messages
    - data_ :
    - noSelfEdge_: Faut-il dessiner les self Edges
    - simType_:
    - simFactor_: set the minimun similitude factor to connect 2 authors.
    """
    authorIDs = data_.authorID.unique()

    # initialise le réseaux des auteurs
    autNet = author_network_init(authorIDs)

    for authID in authorIDs:
        # pour chaque id récupère l'auteur
        authNode = get_nodeID_from_autID(autNet, authID, asVertex_=True)
        # et les messages qui lui sont associés
        msgIDs = msgIDs_4_authID(msgNet_, authID)

        # on sauvegarde les données dans l'auteur dans le noeud
        autNet = update_author_node(msgNet_, autNet, authNode, msgIDs)

        # pour chaque message on met à jour les liens
        for msg in msgIDs:
            autNet = update_author_link(msgNet_, autNet, authNode, msgNet_.vertex(msg))

    # une fois la prise en compte des messages pour la construction du sociogramme
    # on lie les auteurs qui sont similaires dans la structure du réseau
    if simFactor_:
        link_similar_autNodes(
            autNet, epropName_="s_author", simFactor_=simFactor_, simType_=simType_,
        )
    else:
        logging.info(f"simFactor_={simFactor_} not linking similar users at all")

    if noSelfEdge_:
        autNet = remove_self_edges(autNet)

    # les forces des liens doivent avoir été toutes renseignées, on les normalise
    # dans le sens x / ||x||_2
    # pour chaque dim la valeur sera celle de la participation de cet edge dans la force
    # totale de cette dim ex.  0,001 % de la force totale temporelle du graphe est dans
    # l'edge n° 432 (dummy example)
    for epName in ["s_temporal", "s_topic", "s_author"]:
        # on normalise mais si le graphe finale n'a pas les même edges la somme ne
        # fera pas 1
        autNet.ep[epName].a = autNet.ep[epName].a / norm(autNet.ep[epName].a, 2)

        # on arrondi aussi pour faciliter le traitement ultérieur
        autNet.ep[epName].a = round(autNet.ep[epName].a, 6)
    return autNet


def get_course_lang(course="ddl_c18_fr"):
    """
    given a course such as ddl_c18_fr,
    return the course (ddl, c18) and the lang 'fr'
    """
    return course.split("_")[:2], course.split("_")[-1]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Charge ou recrée les données et calcule les circuits"
        "des dynamiques collectives"
    )
    action_hlp = f"Action.  Can be `read`, `Save`, `reload` (def. {CIR_ACTION_DFT})."

    course_hlp = (
        "Non du cours pour lequel calculer les circuits."
        "ufm_c18, pml_c17, pp_c17, va_c17 pour respectivement"
        " understanding Financial markes, "
        "python for machin learning, python plotting and villes africaines"
    )

    outDir_hlp = (
        f"Dossier de sortie pour les graphes et les circuits calculés"
        f" (def. {CIR_OUTDIR_DFT})."
    )
    tokfname_hlp = f"vectorized file (def. {TOK_FNAME_DFT})."
    logLevel_hlp = f"Log level (def. {LOGLEVEL_DFT})"
    lang_hlp = f"lang des données à garder pour le classement (def. {LANG_DFT})."
    draw_hlp = f"Should we draw and save the graph (def. {CIR_DRAW_DFT})."
    circuits_hlp = (
        f"Compute circuits.. ! Can take a long time in O((V+E)*(C+1))"
        f"(def. {CIR_ENUMERATION_DFT}). If set should be an int to limite"
        "the size of the circuits."
    )
    methods_hlp = (
        f"methods type when linking users in a thread. could"
        " be ['prec1', 'prec2', 'prec3', 'prec5', 'prec8', 'starall', 'all']"
        f"(def. {CIR_METHODS_DFT})."
    )

    w_tdeltas_hlp = (
        f"time window multiplier. The default is the median timedelta"
        "of all the course.  When linking edges based on time only,"
        " how old should be the message to consider for linking."
        f" (def. {CIR_WTDELTAS_DFT})."
    )
    alpha_hlp = f"Importance du terme de régulation (def. {VEC_ALPHA_DFT})"
    l1Ratio_hlp = f"Ratio de régularisation l1 (1) vs l2 (0), (def. {VEC_L1RATIO_DFT})"
    redux_hlp = f"The number of dimension de la troncation Default = {VEC_REDUX_DFT}"
    prefix_hlp = f" (def. {TOK_PREFIX_DFT})."
    simType_hlp = (
        f"La mesure de similarité des noeuds du " f"sociograme (def. {SIMTYPE_DFT})."
    )

    sameTop_hlp = (
        f"Should we link message with same topique exclusively or"
        f" can we link message in same thread (def. {SAMETOP_DFT})."
    )

    sameThreadID_hlp = (
        f"Should we link user in exactly the same thread or can time"
        f" linkage occur outside of same thread (def. {SAMETHREADID_DFT})."
    )

    simFactor_hlp = (
        f"set the strenght of the similarity factor to link user "
        f"in sociogram (def. {SIMFACTOR_DFT})."
    )

    parser.add_argument(
        "-f", "--simFactor", type=float, default=SIMFACTOR_DFT, help=simFactor_hlp,
    )
    parser.add_argument(
        "-s", "--sameThreadID", default=SAMETHREADID_DFT, help=sameThreadID_hlp,
    )
    parser.add_argument("-t", "--sameTop", default=SAMETOP_DFT, help=sameTop_hlp)

    parser.add_argument("-j", "--simType", default=SIMTYPE_DFT, help=simType_hlp)
    parser.add_argument("-O", "--OutDir", default=CIR_OUTDIR_DFT, help=outDir_hlp)
    parser.add_argument("-c", "--course", default=COURSE_DFT, help=course_hlp)
    parser.add_argument(
        "-T", "--tokfname", default=TOK_FNAME_DFT, help=tokfname_hlp,
    )
    parser.add_argument("-A", "--Action", default=CIR_ACTION_DFT, help=action_hlp)
    parser.add_argument(
        "-L", "--logLevel", default=LOGLEVEL_DFT, help=logLevel_hlp,
    )
    parser.add_argument("-l", "--lang", default=LANG_DFT, help=lang_hlp)
    parser.add_argument("-d", "--draw", action="store_true", help=draw_hlp)
    parser.add_argument(
        "-C", "--Circuits", type=int, default=CIR_ENUMERATION_DFT, help=circuits_hlp,
    )
    parser.add_argument(
        "-m", "--methods", nargs="*", default=CIR_METHODS_DFT, help=methods_hlp,
    )
    parser.add_argument(
        "-w", "--wTdeltas", nargs="*", default=CIR_WTDELTAS_DFT, help=w_tdeltas_hlp,
    )
    parser.add_argument(
        "-a", "--alpha", type=float, default=VEC_ALPHA_DFT, help=alpha_hlp,
    )
    parser.add_argument(
        "-r", "--l1Ratio", type=float, default=VEC_L1RATIO_DFT, help=l1Ratio_hlp,
    )
    parser.add_argument(
        "-x", "--redux", type=int, default=VEC_REDUX_DFT, help=redux_hlp,
    )
    parser.add_argument("-p", "--prefix", default=TOK_PREFIX_DFT, help=prefix_hlp)
    return parser.parse_args()


def main_prg():
    """Parse argument and run the main function."""
    args = parse_arguments()

    LOGFMT = "/%(filename)s@%(lineno)s@%(funcName)s/ %(message)s"
    logging.basicConfig(level=args.logLevel, format=LOGFMT)
    logging.info(f"sys.argv={sys.argv[0]}, main.__file__={__file__}")

    kwargsC = {
        "course_": args.course,
        "circuitLen_": args.Circuits,
        "draw_": args.draw,
        "lang_": args.lang,
        "methods_": args.methods,
        "outdir_": args.OutDir,
        "w_tdeltas_": args.wTdeltas,
        "simFactor_": args.simFactor,
        "simType_": args.simType,
        "sameTop_": args.sameTop,
        "sameThreadID_": args.sameThreadID,
    }

    kwargsV = {
        "alpha_": args.alpha,
        "course_": args.course,
        "fname_": coerce_string2number(args.tokfname),
        "l1ratio_": args.l1Ratio,
        "lang_": args.lang,
        "prefix_": args.prefix,
        "redux_": args.redux,
    }

    circuits(args.Action, kwargsV, data_=None, **kwargsC)


if __name__ == "__main__":
    main_prg()
