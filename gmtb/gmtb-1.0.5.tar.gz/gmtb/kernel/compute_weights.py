import numpy as np


def median_weights_iter(n, kernel_matrix, start, normalize):
    # return values
    weights_median_set = np.full(n, np.inf)
    weights_median_set_new = start
    k_median_set = None
    k_median_set_new = np.zeros(n)
    k_median_median = None
    k_median_median_new = 0

    # stop conditions
    negative_stop = False
    threshold = 1e-15
    max_iter = 1000
    iter = 0

    while np.sum(np.power(weights_median_set - weights_median_set_new, 2)) > threshold and iter < max_iter:
        # if and ~isreal ...

        weights_median_set = weights_median_set_new
        k_median_median = k_median_median_new
        k_median_set = k_median_set_new

        # kernel between median and median
        k_median_median_new = np.sum(kernel_matrix * np.outer(weights_median_set, weights_median_set)) / \
                              np.power(np.sum(weights_median_set), 2)

        # kernel between objects and median
        for i in range(n):
            k_median_set_new[i] = np.sum(kernel_matrix[:, i] * weights_median_set) / np.sum(weights_median_set)

        # compute weights
        # prevent negative values
        tmp_weights = np.diag(kernel_matrix) - 2 * k_median_set_new + k_median_median_new
        tmp_weights[tmp_weights < 1e-10] = 1e-10

        weights_median_set_new = 1 / np.sqrt(tmp_weights)
        # weights_median_set_new[weights_median_set_new < 1e-5] = 1e-5
        # weights_median_set_new = np.sqrt(weights_median_set_new)

        if normalize:
            weights_median_set_new = weights_median_set_new / np.sum(weights_median_set_new)


        iter = iter + 1

    if np.any(np.isnan(weights_median_set_new)):
        negative_stop = True

    return weights_median_set_new, k_median_set_new, k_median_median_new, negative_stop


def compute_weights(kernel_matrix, normalize=True):
    n = np.shape(kernel_matrix)[0]

    start = np.sum(kernel_matrix) / np.power(n, 2) - (2 / n * np.sum(kernel_matrix, 1)) + np.diag(kernel_matrix)
    start[start < 1e-5] = 1e-5
    start = np.sqrt(start)
    start = start.astype(np.float128)

    max_iter = 5
    iter = 0
    weights_median_set = None
    k_median_set = None
    k_median_median = None
    negative_stop = True

    # as long as iteration not stopped and there was no stop because of negative values
    while iter < max_iter and negative_stop:
        weights_median_set, k_median_set, k_median_median, negative_stop = \
            median_weights_iter(n, kernel_matrix, start, normalize)

        start = np.random.rand(n) + 1
        start = start.astype(np.float128)
        iter = iter + 1

    return weights_median_set, k_median_set, k_median_median
