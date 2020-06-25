# -*- coding: utf-8 -*-
import pandas as pd


def in_half_open(x, aBin=(0, 1), where="right"):
    """
    aBin is a half open interval [a, b),   return true if x in [a, b),
    false otherways. enter aBin as a interable default = (0,1)
    """

    if where == "right":
        ret = (x >= aBin[0]) and (x < aBin[1])
    elif where == "left":
        ret = (x > aBin[0]) and (x <= aBin[1])
    else:
        raise Exception("where=%s is invalid" % where)

    return ret


def in_closed(x, aBin=(0, 1)):
    """
    aBin is a half open interval [a, b),   return true if x in [a, b),
    false otherways. enter aBin as a interable default = (0,1)
    """

    return (x >= aBin[0]) and (x <= aBin[1])


def mark_age_in_aBin_(x, aBin, aBin_type="semi"):
    """
    return true if e.age in bin n° id

    """

    if aBin_type == "semi":
        ret = in_half_open(x, aBin)
    elif aBin_type == "closed":
        ret = in_closed(x, aBin)
    else:
        raise Exception("aBin_type=%s is invalid" % aBin_type)

    return ret


def draw_time_seq(g, pos, fname, df, freq="4W-SUN", timeProp="msgMREd", **kwargs):
    """
    Draw un graph coupé en séquence temporelles selon la frequence appliqué
    sur la timeProp
    """

    init_view = dict()
    init_view["X"] = [pos[v][0] for v in g.vertices() if pos[v] != []]
    init_view["Y"] = [pos[v][1] for v in g.vertices() if pos[v] != []]
    g.clear_filters()

    age_bins = sorted(bining_eprop(g, timeProp, freq=freq))

    for i, aBin in enumerate(age_bins):
        g.clear_filters()
        # on marque les edges en fonction de leur age par catégorie binid
        for e in g.edges():
            aBin_type = "semi" if i < len(age_bins) - 1 else "closed"
            # in case i = len(age_bins) - 1 c'est la dernière bin.
            g.ep.filtre[e] = mark_age_in_aBin_(g.ep[timeProp][e], aBin, aBin_type)

        g.set_edge_filter(g.ep.filtre)

        path, _, bname, ext = get_bname(fname)
        # mis à jour de filtre pour les noeuds
        if len(g.get_edges()):
            _ = updating_prop(g, df)
            name = path + bname + "_s%s" % str(i) + ext
            print("Drawing timeseq %s" % name, end="\r")
            dg.drawg(g, pos, fname=name, init_view=init_view, **kwargs)
            # print("Drawing %s/%s"  % (i,len(age_bins)), end="\r")

        # print("%s/%s"  % (i,len(age_bins)), end="\r")

    print("Draw %s graph of frequence %s !" % (len(age_bins), freq))
    # file_0 c'est la plus récente,

    # draw_time_seq(g, pos, )


def bining_prop(g, prop, freq="W-SUN", prop_type="v"):
    """
    returns, time intervals semi open [a,b( or bin covering the prop value space
    """

    #    np.histogram_bin_edges(a, bins=n, range=None, weights=None)[source]
    # voir pour 3.7
    prop = g.edge_properties[prop]
    min_p, max_p = min(prop), max(prop)
    min_p, max_p = map(lambda d: pd.Timestamp(d, unit="s"), (min_p, max_p))
    prop_range = pd.date_range(min_p, max_p, freq=freq)
    if min_p < prop_range[0]:
        prop_range = pd.date_range(
            min_p - (prop_range[1] - prop_range[0]), max_p, freq=freq
        )
    prop_bin_edges = list(map(lambda d: d.timestamp(), prop_range))
    prop_bin_edges = zip(prop_bin_edges[:-1], prop_bin_edges[1:])
    return list(prop_bin_edges)


def bining_eprop(g, prop, freq=None):
    """
    returns, n intervals semi open [a,b( or bin covering the prop value space
    """

    return bining_prop(g, prop, freq, prop_type="e")


def bining_vprop(g, prop, freq=None):
    """
    returns, n intervals semi open [a,b( or bin covering the prop value space
    """

    return bining_prop(g, prop, freq, prop_type="v")


def get_bname(fpath):
    """
    Returns a tuple (path, fname, bname, ext)
    """

    path = "/".join(fpath.split("/")[:-1])
    path = "./" if path == "" else path + "/"
    fname = fpath.split("/")[-1]
    bname = ".".join(fname.split(".")[:-1])
    ext = "." + fname.split(".")[-1]

    return path, fname, bname, ext
