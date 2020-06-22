import numpy as np


def best_weighted_mean(oa, ob, alpha, object_set, kernel_matrix, kernel_func, weighted_mean_func):

    n = len(object_set)

    # compute weighted median
    new_mean1 = weighted_mean_func(oa, ob, alpha)
    new_mean2 = weighted_mean_func(ob, oa, 1-alpha)

    # compute sets
    k_mean_set1 = np.zeros(n)
    k_mean_set2 = np.zeros(n)

    for i in range(n):
        k_mean_set1[i] = kernel_func(object_set[i], new_mean1)
        k_mean_set2[i] = kernel_func(object_set[i], new_mean2)

    k_mean_mean1 = kernel_func(new_mean1, new_mean1)
    k_mean_mean2 = kernel_func(new_mean2, new_mean2)

    # compute best value, ignore negative values
    best_value1 = k_mean_mean1 - 2 * k_mean_set1 + np.diag(kernel_matrix)
    best_value2 = k_mean_mean2 - 2 * k_mean_set2 + np.diag(kernel_matrix)
    best_value1[best_value1 < 0] = 0
    best_value2[best_value2 < 0] = 0
    best_value1 = np.sum(np.sqrt(best_value1))
    best_value2 = np.sum(np.sqrt(best_value2))

    # return better result
    if best_value1 < best_value2:
        return new_mean1, k_mean_set1, k_mean_mean1, best_value1
    else:
        return new_mean2, k_mean_set2, k_mean_mean2, best_value2
