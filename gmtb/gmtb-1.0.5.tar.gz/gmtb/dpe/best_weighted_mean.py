import gmtb.util as util
import numpy as np


def best_weighted_mean(oa, ob, alpha, object_set, dist_func, weighted_mean_func):
    mean1 = weighted_mean_func(oa, ob, alpha)
    mean2 = weighted_mean_func(ob, oa, 1-alpha)

    best_value1 = np.sum(util.pdist(set1=object_set, set2=[mean1], func=dist_func))
    best_value2 = np.sum(util.pdist(set1=object_set, set2=[mean2], func=dist_func))

    if best_value1 < best_value2:
        return mean1, best_value1
    else:
        return mean2, best_value2
