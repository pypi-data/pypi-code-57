import graph_tool.topology as gtt
import numpy as np
import logging


def compute_seuils(g, tdf, vi, i, vj, j, how, lcd):
    """Compute the strength between the ith an jth repliers in tdf tid.  this is where content evaluation (or topiques) should by taken in account
    - how: prec: link to all preceding node in the tdf, with strength depending on distance from linker
    prec1 link to the last preceding node in the tdf,
    prec3: link to the last three preceding node in the tdf
    star: link only to the tdf starter
    all: link all previous user,
    - prec1"""

    # il manque la prise en compte de la position déjà existante des sommets i et j dans le réseaux

    # les fonctions ici sont arbitraires...et devraient être justifiées par la littérature
    seuilTS = compute_seuilTS(i, j, how)
    seuil_auteur = compute_seuil_auteur(g, vi, vj, lcd)
    seuil_topic = compute_seuil_topic(tdf, vi, i, vj, j)  # attention pas implémenté

    # plus que de renvoyer une seule force il faut en renvoyer trois (temps, auteurs et topiques)
    return float(seuilTS), float(seuil_auteur), float(seuil_topic)


def compute_seuil_auteur(g, vi, vj, lcd):
    """return a number to mark the strength of previous relation between the two users vi, and vj"""
    # 2147483647 < 1e9 false biggest distance (infinty)
    distance = gtt.shortest_distance(g, source=vi, target=vj)
    return lcd / distance if distance and distance < 100 else 0


def compute_seuil_topic(tdf, i, j, how):
    """return a number to mark that message of the two user are on the same topic"""
    topi = tdf.iloc[i].nmf_ctg
    topj = tdf.iloc[j].nmf_ctg
    return int(topi == topj)


def compute_seuilTS(i, j, how):
    """ Calcule la dimention temporelle de la force """
    # j est > i,
    if how == "precall":
        return gaussian(j - i, sig=6)  # 6 dumbar's number
    elif how == "prec1":
        return 1 if j - i == 1 else 0
    elif how == "starall":
        return 1 if i == 0 else 0
    elif how == "all":
        return 1
    elif "prec" in how:
        try:
            n = int(how.replace("prec", ""))
            return gaussian(j - i, sig=n / 2) if j - i <= n else 0
        except ValueError as ve:
            logging.error(
                "Check the rest of how=%s.  It shoulde be coercible to int." % how
            )
            raise (ve)
    else:
        raise Exception("Choisissez un type de connexion valide")

    return 0


def gaussian(x, mu=0, sig=1):
    # A = 1 / (2 * np.pi * sig ** (1 / 2))
    return np.exp(-((x - mu) ** 2) / (2 * sig ** 2))


# #### helper
