import gmtb.kernel
import numpy as np


def linear(object_set,weights,dist,kernel_func,weighted_mean_func,kernel_matrix,n_points):

    # get order of objects by distance
    ind = np.argsort(dist)

    n = len(object_set)
    iter = min(n,n_points)-1
    best_value_kernel_space = np.full(iter+1, np.inf)
    new_mean = [None] * (iter+1)
    new_mean[0] = object_set[ind[0]]

    k_mean_set = kernel_matrix[:, ind[0]]
    k_mean_mean = kernel_matrix[ind[0], ind[0]]
    best_value_kernel_space[0] = np.sum(np.sqrt(k_mean_mean - 2 * k_mean_set + np.diag(kernel_matrix)))

    for i in range(iter):
        # get next index
        b = ind[i+1]

        # compute alpha
        alpha = gmtb.kernel.compute_alpha(weights, k_mean_set, k_mean_mean, kernel_matrix[:, b], kernel_matrix[b, b], k_mean_set[b])

        # compute new weighted mean
        new_mean[i+1], k_mean_set, k_mean_mean, best_value_kernel_space[i+1] = \
            gmtb.kernel.best_weighted_mean(new_mean[i], object_set[b], alpha, object_set, kernel_matrix, kernel_func, weighted_mean_func)

    ind = np.argmin(best_value_kernel_space)
    return new_mean[ind], best_value_kernel_space[ind]