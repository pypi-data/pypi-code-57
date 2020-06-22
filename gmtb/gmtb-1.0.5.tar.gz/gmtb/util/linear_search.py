import numpy as np
import scipy.optimize
import gmtb.util


# implementation of the linear search method for improving of reconstructions.
# returns
#   rec_obj - the improved reconstructed object
#   best_value - value of the reconstructed object (ath the moment SOD)
def linear_search(median_obj,object_set,dist_func,weighted_mean_func,num_iterations=5):

    best_value = np.sum(gmtb.util.pdist(set1=object_set,set2=[median_obj],func=dist_func))
    rec_obj = median_obj
    best_obj = median_obj

    # for each iteration
    for iter in range(num_iterations):

        last_best_value = best_value

        # try each object
        for obj in range(len(object_set)):

            def search_crit(alpha):
                wm = weighted_mean_func(rec_obj, object_set[obj], alpha)
                return np.sum(gmtb.util.pdist(set1=object_set, set2=[wm], func=dist_func))

            alpha, new_best_value, ierr, numfunc = scipy.optimize.fminbound(search_crit, 0, 1, maxfun=15, full_output=True, disp=0)

            if new_best_value < best_value:
                best_value = new_best_value
                best_obj = weighted_mean_func(rec_obj, object_set[obj], alpha)

        # set new median
        rec_obj = best_obj

        if last_best_value == best_value:
            return rec_obj, best_value

    return rec_obj, best_value