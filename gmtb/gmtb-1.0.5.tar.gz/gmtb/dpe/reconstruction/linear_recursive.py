import numpy as np
from ..compute_alpha import compute_alpha
from ..best_weighted_mean import best_weighted_mean
import gmtb.util
import gmtb.util.distance


# implementation of the linear recursive reconstruction method
# returns:
#   rec_obj - reconstructed object
#   best_value - value of the reconstructed object (at the moment SOD)
def linear_recursive(object_vector, embedding, object_set, dist_func, weighted_mean_func):

    # return if only one object
    if len(object_set) == 1:
        return object_set[0], 0

    # save original set
    orig_set = object_set
    object_set = object_set.copy()

    # first best value: set median
    dist = gmtb.util.pdist(set1=embedding, set2=[object_vector], func=gmtb.util.distance.euclidean_dist)
    ind = np.argmin(dist)
    best_value = np.sum(gmtb.util.pdist(set1=object_set, set2=[object_set[ind]], func=dist_func))
    rec_obj = object_set[ind]

    while len(object_set) > 1:

        dist = gmtb.util.pdist(set1=embedding, set2=[object_vector], func=gmtb.util.distance.euclidean_dist)
        ind = np.argsort(dist)

        new_object_set = []
        new_embedding = []

        for i in range(0, len(object_set)-1,2):

            # compute new weighted mean
            alpha = compute_alpha(embedding[ind[i]], embedding[ind[i+1]], object_vector)

            nm, bv = best_weighted_mean(object_set[ind[i]], object_set[ind[i+1]], alpha, orig_set,
                                        dist_func, weighted_mean_func)

            new_object_set.append(nm)
            new_embedding.append(alpha*embedding[ind[i]] + (1-alpha)*embedding[ind[i+1]])

            # save best
            if bv < best_value:
                best_value = bv
                rec_obj = nm

        # if leftover objects: just copy
        if np.remainder(len(object_set), 2) == 1:
            new_object_set.append(object_set[ind[-1]])
            new_embedding.append(embedding[ind[-1]])

        # prepare next iteration
        object_set = new_object_set
        embedding = new_embedding

    # end: return best result
    return rec_obj, best_value

