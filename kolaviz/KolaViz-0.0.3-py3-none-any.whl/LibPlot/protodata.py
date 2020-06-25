# -*- coding: utf-8 -*-

"""
 Outils pour générer les visualisations d3 via vega-lite et Altair
"""
from pandas import (
    DataFrame,
    Series,
    Timestamp,
    MultiIndex,
    to_datetime,
)
from itertools import zip_longest
from operator import itemgetter
from numpy import random as rnd
import numpy as np


class DummyDataGen:
    def __init__(
        self,
        nbmsg=9460,
        nbauth=4609,
        nbdis=1318,
        startts="2019-07-08",
        endts="2019-09-01",
        nbtop=8,
        maxgpsize=50,
    ):
        """
        Générateur de données aléatoires mais suivant cependant certaines lois de probabilité pour la distribution des messages et des appartenances au groupes
Renvois un dataframe avec les colonnes msgID, authID, groupID, goupe_strenght.
group_strength est un tuple repésentant la force d'appartenance d'un auteur à un groupe collectif.
        Par défaut les nombres sont ceux du cours de l'UNIGE UFM
        Keyword Arguments:
        nbmsg  -- (default 9460) nombre de message
        nbAuth -- (default 4609) nombre d'auteur
        nbDis  -- (default 1318) nombre de discussions
        startsts -- (defaut 2019-07-08)  le temps du premier message
        endts -- (defaut 2019-09-01)  le temps du dernier message

        """
        listetype = zip(["msg", "auth", "disc"], [nbmsg, nbauth, nbdis])
        msgID, authID, disID = base_data_gen(listetype)

        # les times stamp
        msgTS = gen_ts(startts, endts, nbmsg)

        # group_attribution
        df = msg_repartition(disID, msgID, authID, msgTS, nbmsg)

        # topics generations and attribution to messages
        df = topique_attribution(df, nbtop)

        # 2 ) Authors and groups
        dfAutGp = group_attribution(authID, maxgpsize, N=30)
        self.df = df.merge(
            right=dfAutGp, how="left", left_on="authID", right_on="auth",
        ).drop("auth", axis=1)

    def null_group_lt_(self, num=10):
        """
        remove groups smaller than num, but keepos the df.
         ie: "group_force", 'group_name', 'group_size' will be None.
        """
        largest_groups = idx_largest("group_name", self.df, num)
        mask = ~self.df.group_name.isin(largest_groups)
        self.df.loc[mask, ["group_force", "group_name", "group_size"]] = None
        return self.df


def group_attribution(authid, maxgpsize, N=50):
    """
    Attribute users to N groupes of maximun size maxgpsize. N le nombre de groupes
    """
    # l'appartenance à un group dépend d'un triplet (prox semantique, prox temporelle, prox quantitative)

    G = {}
    for gp in range(N):
        G[gp] = rnd.choice(authid, size=gen_group_size(maxgpsize), replace=False)

    A = []
    for g, auths in G.items():
        for k, auth in enumerate(auths):
            A += [
                {
                    "auth": auth,
                    "group_force": get_uni_rnd(),
                    "group_name": f"gp{k}",
                    "group_size": len(auths),
                }
            ]

    return DataFrame(A)


def base_data_gen(listetype):
    """
    for each type returns a liste of associated size
    """

    def gen_list(name, nb):
        return [f"{name}{i}" for i in range(nb)]

    return [gen_list(name, nb) for name, nb in listetype]


def topique_attribution(df, nbtop):
    """
    Attribute topics to messages         # using some beta distribution over each disID
    """
    T = []
    for name, g in df.groupby("disID"):
        T += list(zip(g.index, get_rnd_topics(len(g), nbtop)))

    topics = DataFrame(T, columns=["idx", "msgTop"]).set_index("idx")

    return df.merge(right=topics, left_index=True, right_index=True)


def msg_repartition(disid, msgid, authid, msgts, nbmsg):
    """
    Attribute msgID to authors and discussion
    """
    # Note: ne gère pas le cas des doublons temporels pour un même auteur et discussion
    beta = rnd.beta(0.5, 10, size=len(disid))
    p = beta / sum(beta)
    disChoice = rnd.choice(disid, nbmsg, replace=True, p=p)
    df = DataFrame(
        data=np.array([msgts, msgid, rnd.choice(authid, nbmsg), disChoice]).T,
        columns=["msgTS", "msgID", "authID", "disID"],
    )
    return df.sort_values("msgTS")


def gen_ts(startts, endts, nbmsg):
    startTs = Timestamp(startts).timestamp()
    endTs = Timestamp(endts).timestamp()

    C = 10e6
    ts = rnd.choice(
        np.linspace(startTs, endTs, num=C, dtype=int), size=nbmsg, replace=False,
    )
    return to_datetime(ts * 10e8)


def gen_group_size(maxgpsize):
    """
    Renvois la taille d'un groupe entre  3 et maxgpsize
    """
    return int(rnd.beta(1, 9) * (maxgpsize - 3)) + 3


def get_rnd_topics(nbmsg, maxtopdis):
    """
    Each discussion wil have a major topic
    """
    # set a number of topics for the discussion
    nbDisTop = int(rnd.beta(2, 7) * maxtopdis) + 1

    # generate a beta distribution for that number
    beta = rnd.beta(1, 5, size=nbDisTop)
    p = beta / sum(beta)

    # sample nbmsg Topics from a restricted subset of topics
    restrictedSubset = rnd.choice(range(maxtopdis), size=nbDisTop, replace=False)
    return rnd.choice(restrictedSubset, nbmsg, replace=True, p=p)


def get_uni_rnd(size=3, prec=2, norme="l1"):
    """
    Generate a random point in normed l1 for unit cube, l2 for boule
    """
    # à vérifier
    X = rnd.uniform(size=size)
    if norme == "l2":
        X = list(map(lambda x: round(x, prec), X ** 2 / sum(X ** 2)))
    elif norme == "l1":
        X = list(map(lambda x: round(x, prec), X / sum(X)))

    X[-1] = round(1 - sum(X[:-1]), prec)
    return X


def get_uni_rnd_vect(longueur=1, innersize=3, prec=2, norme="l1"):
    """
    May not be necessary
    """
    return [
        get_uni_rnd(size=innersize, prec=prec, norme=norme) for i in range(longueur)
    ]


def get_by_len_(what, df, num=None):
    """
    group the dataFrame df by col what, sort by group len and return the first num rows index, id, cols.
    if num is None, renvois tout, sinon les plus petit quand num > 0 et le plus grand quand num < 0
    """
    sorted_data = df.groupby(what).agg(len).sort_values(by="msgID").index
    if not num:
        return sorted_data

    return sorted_data[:num] if num > 0 else sorted_data[num:]


def get_group_name_by_len(df, num=None):
    """
    Return the group_name ordered by group lenght
    """
    return get_by_len_("group_name", df, num=num)


def idx_largest(what, df, num=3):
    """
    Return the what column and order by largest's group
    """
    assert num > 0
    return get_by_len_(what, df, num=num * -1)


def largest_dis(df, num=3):
    """
    Returns the largest discussions index
    """
    return idx_largest("disID", df, num=num)


def keep_largest_(what, df, num=3):
    """
    returns the df with only the largest, of what cols kept.  by default the 3 largest.
    """
    return df[df.loc[:, what].isin(idx_largest(what, df, num))]


def keep_largest_dis(df, num=3):
    """
    returns the df with the num largest discussions only
    """
    return keep_largest_("disID", df, num)


def keep_largest_group(df, num=3):
    """
    returns the df with the num largest discussions only
    """
    return keep_largest_("group_name", df, num)


def keep_what_with_criteria(df, what, op="gt", num=10):
    """
    Returns the df where rows of what groups not satisfying op num are filtered out
    """
    gb = df.groupby(what).count().iloc[:, 0]
    crit = what_criteria(df, what, op, num)
    mask = df.loc[:, what].isin(crit.index)
    return df[mask]


def what_criteria(df, what, op="gt", num=10):
    """
    Returns mask that should be used to filter out df base don criteria
    """
    gb = df.groupby(what).count().iloc[:, 0]
    crit = gb
    if op == "gt":
        crit = gb > num
    elif op == "lt":
        crit = gb < num
    elif op == "ge":
        crit = gb >= num
    elif op == "le":
        crit = gb <= num
    else:
        raise Exception(f"op={op} is invalid")

    return gb[crit]


def get_topique_msg_resume(df):
    """
    renvois des statistiques résumant l'ensemble des messages
    dans msgList_
    critère pour sortes
    state général: count,
    sur wtext: min, max, mean , mead phrases, tokens
    sur msgMREd: min , max, mean , med ts
    sur authorID: # de différent, # msg/autor
    sur nmf_ctg:

    """

    def avg_msg_per_auth(s):
        return len(s.unique())

    res = dict()
    for n, gp in df.groupby("topique"):
        res[(n, "general")] = {"len": len(gp)}

        col = "msgMREd"
        func2apply = [min, max, np.mean, np.median]
        val = gp.loc[:, [col]].apply(func2apply, axis=0).values
        idx = gp.loc[:, [col]].apply(func2apply, axis=0).index
        res[(n, col)] = dict(zip(idx, val.T[0]))

        col = "authorID"
        val = len(gp) / gp.loc[:, [col]].apply(avg_msg_per_auth).values[0]
        res[(n, col)] = {"msg_per_author": val}

        col = "msgID"
        val = gp.loc[:, [col]].apply(len).values[0]
        res[(n, col)] = {"nbMsg": val}

    # pd.DataFrame(res)
    resdf = DataFrame.from_dict(res).T.unstack().dropna(axis=1, how="all")
    resdf = DataFrame(
        data=resdf.values, index=resdf.index, columns=resdf.columns.swaplevel(),
    )
    return resdf


def get_topique_data(df):
    df.loc[:, "topique"] = df.iTokens.apply(itemgetter(0))
    gbTopiques = df.topique.groupby("topique")

    res = {}

    topiques = Series(gbTopiques.groups).apply(list)
    topiques.index.name = "topiques"
    topiques.name = "msgID"

    mcols = MultiIndex.from_tuples(
        list(zip_longest(topiques.index, ["raw"], fillvalue="raw"))
    )
    import ipdb

    ipdb.set_trace()

    topiques = DataFrame(data=topiques.values, index=topiques.index, columns=mcols)
    # topiques = topiques.drop(["threadID", "msgIDto_drop", "authorID"], axis=1)

    topiques = topiques.merge(
        get_topique_msg_resume(gbTopiques), left_index=True, right_index=True,
    ).sort_index(axis=1)

    return topiques


def get_data_temporal_filter(df_, Cs_, asTimestamp_=True):
    """
    Renvois les données pour le filtre temporelle
    prend le retour de cuiruit.py
    -asTimestamp_ : should we return the time stamp as Timestamp

    return un dataFrame avec les colonnes
    """

    cirPerMsg = Cs_["msg"].groupby("msgID").count()
    if df_.index.name in df_.columns:
        df_.index.name = f"Orij_{df_.index.name}"
    res = (
        df_.loc[:, ["msgID", "msgMREd"]]
        .merge(
            cirPerMsg.reset_index(),
            how="left",
            left_on="msgID",
            right_on="msgID",
            suffixes=("", "_drop"),
        )
        .set_index("msgID", drop=True)
    )
    res.loc[:, "inCircuit"] = res.cirID.notna().apply(lambda x: int(x))
    res = res.drop("cirID", axis=1)

    if asTimestamp_:
        res.loc[:, "msgMREd"] = res.msgMREd.apply(lambda x: Timestamp(x * 10e8))

    res.loc[:, "inCircuit"] = res.inCircuit.apply(bool)

    return res


def build_data_for_threadID(df_):
    """
    Some stats for sort and filter of the thread visu
    """
    # T = df_.reset_index().loc[:, ['tTitle', 'Orij_msgID', 'msgID', 'authorID']]
    # T = T.merge(R_, right_index=True, left_index=True).drop('msgID', axis=1)

    _res: Dict[str, Dict[str, Any]] = {}

    for n, gp in df_.groupby("tTitle"):

        _res[n] = {}

        for c in gp.columns:

            if c in ["msgMREd"]:

                _res[n][(f"{c}_min")] = min(gp[c])
                _res[n][(f"{c}_max")] = max(gp[c])
                _res[n][(f"{c}_mean")] = np.mean(gp[c]).round("s")
                _res[n][(f"{c}_tdelta")] = max(gp[c]) - min(gp[c])

            if c in ["Orij_msgID", "authorID"]:

                _res[n][(f"{c}_nb")] = len(gp[c].unique())

            if c == "inCircuit":

                _res[n][f"{c}"] = sum(gp[c])

    res = DataFrame(_res).T
    res.index.name = "tTitles"
    return res.reset_index().sort_values("authorID_nb")
