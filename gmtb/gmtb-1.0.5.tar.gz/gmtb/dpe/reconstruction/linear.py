import numpy as np
import gmtb.util as util
import gmtb.util.distance as distance
from gmtb.dpe import compute_alpha,best_weighted_mean


# implementation of linear and triangular reconstruction
# returns:
#   rec_obj - the reconstructed object
#   best_value - SOD of the reconstructed object
def linear(object_vector, embedding, object_set, dist_func, weighted_mean_func, n_points):

    # get order of objects by distance
    dist = util.pdist(set1=embedding, set2=[object_vector], func=distance.euclidean_dist)
    ind = np.argsort(dist)

    n = len(object_set)
    iter = min(n, n_points)-1
    best_value = np.full(iter+1, np.inf)
    rec_obj = [None] * (iter+1)
    rec_obj[0] = object_set[ind[0]]
    mean_vec = embedding[ind[0]]

    best_value[0] = np.sum(util.pdist(set1=object_set, set2=[rec_obj[0]], func=dist_func))

    for i in range(iter):
        # get next index

        b = ind[i+1]

        # compute alpha
        alpha = compute_alpha(mean_vec, embedding[b,:], object_vector)

        # compute new weighted mean
        rec_obj[i+1], best_value[i+1] = best_weighted_mean(rec_obj[i], object_set[b], alpha, object_set, dist_func, weighted_mean_func)

    ind = np.argmin(best_value)
    return rec_obj[ind], best_value[ind]