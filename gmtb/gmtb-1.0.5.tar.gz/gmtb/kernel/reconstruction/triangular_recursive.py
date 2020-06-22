import numpy as np
from ..compute_alpha import compute_alpha
from ..best_weighted_mean import best_weighted_mean


# implementation of the triangular recursive reconstruction method
# returns:
#   rec_obj - reconstructed object
#   best_value - value of the reconstructed object (at the moment SOD)
def triangular_recursive(object_set,weights,dist,kernel_func,weighted_mean_func,kernel_matrix):

    # return if only one or two objects
    if len(object_set) == 1:
        return object_set[0], 0

    # save original set
    orig_set = object_set.copy()
    object_set = object_set.copy()

    # arrays for intermediate kernel values
    k_mean_set = kernel_matrix
    k_mean_mean = np.diag(kernel_matrix)

    # first best value: set median
    ind = np.argsort(dist)
    best_value = np.sum(np.sqrt(k_mean_mean[ind[0]] - 2 * k_mean_set[ind[0], :] + np.diag(kernel_matrix)))
    new_mean = object_set[ind[0]]

    # precompute k_median (kernel of the true median with itself)
    k_median_vec = np.sum(np.outer(weights,weights) * kernel_matrix) / np.sum(weights)**2

    while len(object_set) > 1:

        ind = np.argsort(dist)

        new_object_set = []
        new_k_mean_set = []
        new_k_mean_mean = []
        new_dist = []

        # for every three objects
        for i in range(0, len(object_set)-2, 3):

            # compute median between first two
            alpha = compute_alpha(weights, k_mean_set[ind[i]], k_mean_mean[ind[i]], k_mean_set[ind[i+1]], k_mean_mean[ind[i+1]],
                                  kernel_func(object_set[ind[i]],object_set[ind[i+1]]))
            nm, kms, kmm, bv = \
                best_weighted_mean(object_set[ind[i]], object_set[ind[i+1]], alpha, orig_set, kernel_matrix, kernel_func,
                                   weighted_mean_func)

            # compute median between result and third
            alpha = compute_alpha(weights, kms, kmm, k_mean_set[ind[i + 2]], k_mean_mean[ind[i + 2]],
                                  kernel_func(nm, object_set[ind[i + 2]]))
            nm, kms, kmm, bv = \
                best_weighted_mean(nm, object_set[ind[i + 2]], alpha, orig_set, kernel_matrix, kernel_func,
                                   weighted_mean_func)

            new_object_set.append(nm)
            new_k_mean_set.append(kms)
            new_k_mean_mean.append(kmm)
            tmp_dist = (k_median_vec
                                    - 2 * np.sum(weights * kms) / np.sum(weights)
                                    + kmm)
            if tmp_dist < 0:
                tmp_dist = (dist[ind[i]] + dist[ind[i+1]] + dist[ind[i+2]])/3
            else:
                tmp_dist = np.sqrt(tmp_dist)
            new_dist.append(tmp_dist)

            # save best
            if bv < best_value:
                best_value = bv
                new_mean = nm



        # if only one leftover object: just copy
        if np.remainder(len(object_set), 3) == 1:
            new_object_set.append(object_set[-1])
            new_k_mean_mean.append(k_mean_mean[-1])
            new_k_mean_set.append(k_mean_set[-1])
            new_dist.append(dist[-1])

        # else: linear
        elif np.remainder(len(object_set), 3) == 2:
            alpha = compute_alpha(weights, k_mean_set[ind[-2]], k_mean_mean[ind[-2]], k_mean_set[ind[-1]],
                                  k_mean_mean[ind[-1]],
                                  kernel_func(object_set[ind[-2]], object_set[ind[-1]]))

            nm, kms, kmm, bv = \
                best_weighted_mean(object_set[ind[-2]], object_set[ind[-1]], alpha, orig_set, kernel_matrix,
                                   kernel_func,
                                   weighted_mean_func)

            new_object_set.append(nm)
            new_k_mean_set.append(kms)
            new_k_mean_mean.append(kmm)
            tmp_dist = (k_median_vec
                - 2 * np.sum(weights * kms) / np.sum(weights)
                + kmm)
            if tmp_dist < 0:
                tmp_dist = (dist[ind[-2]] + dist[ind[-1]]) / 2
            else:
                tmp_dist = np.sqrt(tmp_dist)
            new_dist.append(tmp_dist)

            if bv < best_value:
                best_value = bv
                new_mean = nm

        # prepare next iteration
        object_set = new_object_set
        k_mean_set = new_k_mean_set
        k_mean_mean = new_k_mean_mean
        dist = new_dist

    # end: return best result
    return new_mean, best_value

