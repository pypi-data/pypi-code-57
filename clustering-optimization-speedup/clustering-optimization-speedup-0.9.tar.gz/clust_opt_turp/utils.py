import numpy as np

from .speeding_algorithm import optimize_use_clustering, form_clusters, calc_risk, calc_revenue
from .optimizer import optimize_port


def prepare_data(raw_data: np.ndarray) -> np.ndarray:
    return np.apply_along_axis(lambda x: x / x[0], axis=1, arr=raw_data)


def calc_loss(data, return_value, clust_thresold, clust_dist):
    returns = data[:, -1]
    w_clust = optimize_use_clustering(data, return_value, clust_thresold, clust_dist, returns, 'return_bound')
    _, n_of_clusts = form_clusters(data, clust_thresold, clust_dist, return_count=True)
    w_non = optimize_port(data, calc_risk(w_clust, np.cov(data)), returns, 'risk_bound')
    return calc_revenue(w_non, returns) - calc_revenue(w_clust, returns), data.shape[0] / n_of_clusts
