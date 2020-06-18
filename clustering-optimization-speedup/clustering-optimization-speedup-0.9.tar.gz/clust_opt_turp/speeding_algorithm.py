import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage

from recalculation import recalculate_data, recalculate_returns
from .optimizer import optimize_port


def optimize_use_clustering(data, value, t, dist, returns, crit="return_bound"):
    """
    :param data: data on stock assets prices for clustering, format: each array row is
        data on prices changes in period at percents from the beginning of the beginning of the period
        (e.g. first value in row = 1.0)
    :param t: threshold value for clustering
    :param dist: 'single', 'complete', 'average' - clustering distance
    :param value: optimization criterion value:
        risk if crit="risk_bound"
        return if crit="return_bound",
        gamma if crit="risk_return"
    :param returns: vector of assets returns
    :param crit: optimization method - by risk bound ("risk_bound"), value bound ("return_bound")
        or RAPOC ("risk_return")
    :return: vector of assets weights in optimal portfolio
    """
    clusters = form_clusters(data, t, dist)
    clustered_data = recalculate_data(data, clusters)
    clustered_returns = recalculate_returns(returns, clusters)
    w = optimize_port(clustered_data, value, clustered_returns, crit)
    x = clusters_weights(w, clusters)
    return x


def form_clusters(x, t, dist, return_count=False):
    link = linkage(x, metric='correlation', method=dist)
    res = fcluster(Z=link, t=t, criterion='distance')
    if return_count:
        res = res, np.unique(res).max()
    return res


def clusters_weights(W, clusters):
    _, clusters_sizes = np.unique(clusters, return_counts=True)
    function = np.vectorize(lambda x: (W / clusters_sizes)[x - 1])
    return function(clusters)


def calc_risk(w: np.ndarray, cv: np.ndarray) -> float:
    if len(w.shape) == 1:
        w = w.reshape(1, w.shape[0])
    return (w.T.dot(w) * cv).sum()


def calc_revenue(w: np.ndarray, d: np.ndarray) -> float:
    return w.dot(d)
