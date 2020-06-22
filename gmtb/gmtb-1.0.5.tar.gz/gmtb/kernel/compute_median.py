import numpy as np

import gmtb.kernel
import gmtb.kernel.reconstruction
import gmtb.util


# computes median using kernel functions.
# paramter dist_func is only needed in case of linear search
def compute_median(object_set, weights, kernel_func, weighted_mean_func, rec_type, kernel_matrix=None, dist_func=None):
    n = len(object_set)

    # compute kernels
    if kernel_matrix is None:
        kernel_matrix = gmtb.util.pdist(object_set, kernel_func)

    if type(weights) is str:
        if weights == "mean":
            weights = np.ones(n)
            dist = np.sqrt(np.sum(kernel_matrix) / np.power(n, 2) - 2/n * np.sum(kernel_matrix, 0) + np.diag(kernel_matrix))
        elif weights == "median":
            weights = gmtb.kernel.compute_weights(kernel_matrix, True)[0]
            dist = 1 / weights
        else:
            raise ValueError("compute_median: only median and mean allowed as string values for weights")
    else:
        #TODO test this
        dist = np.sqrt(np.sum(weights @ np.transpose(weights) * kernel_matrix) / np.power(np.sum(weights, axis=0), 2)
                       - 2 * np.sum(weights * kernel_matrix, axis=0).T / np.sum(weights, axis=0) + np.diag(kernel_matrix))

    # reconstruction
    if rec_type == "linear":
        return gmtb.kernel.reconstruction.linear(object_set, weights, dist, kernel_func, weighted_mean_func, kernel_matrix, 2)
    elif rec_type == "triangular":
        return gmtb.kernel.reconstruction.linear(object_set, weights, dist, kernel_func, weighted_mean_func, kernel_matrix, 3)
    elif rec_type == "linear_recursive":
        return gmtb.kernel.reconstruction.linear_recursive(object_set, weights, dist, kernel_func, weighted_mean_func,
                                               kernel_matrix)
    elif rec_type == "triangular_recursive":
        return gmtb.kernel.reconstruction.triangular_recursive(object_set, weights, dist, kernel_func, weighted_mean_func,
                                                   kernel_matrix)
    elif rec_type == "linear_search_linear_recursive":
        obj, bv = gmtb.kernel.reconstruction.linear_recursive(object_set, weights, dist, kernel_func, weighted_mean_func,
                                                  kernel_matrix)
        return gmtb.util.linear_search(obj, object_set, dist_func, weighted_mean_func)
    else:
        raise NotImplementedError("kernel.compute_median: reconstruction method not found")


