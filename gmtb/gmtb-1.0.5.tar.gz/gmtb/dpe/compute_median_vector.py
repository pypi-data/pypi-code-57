import numpy as np


def compute_median_vector(vector_matrix, threshold=1e-10, max_iter=1000, max_iter_restart=3):

    dim = np.shape(vector_matrix)[1]
    y_old = np.zeros(dim)
    y_new = np.sum(vector_matrix, axis=0)/dim

    iter_restart = 0
    iter = 0

    # change initialization slightly as long as it lies on one of the points
    diff = np.sum(np.power(vector_matrix - y_new[np.newaxis, :], 2), axis=1)
    while np.any(diff == 0):
        y_new = y_new + 0.001
        diff = np.sum(vector_matrix - y_new[np.newaxis, :])

    while np.sum(np.abs(y_new - y_old)) > threshold and iter < max_iter:
        iter = iter + 1
        y_old = y_new

        # stop when the iteration coincidents with one point
        diff = np.sum(np.power(vector_matrix - y_old[np.newaxis, :], 2),axis=1)
        if np.any(diff == 0):
            return y_old

        eukl_dist = np.sqrt(diff)
        numerator = np.sum(vector_matrix / eukl_dist[:, np.newaxis], axis=0)
        denominator = np.sum(1 / eukl_dist)
        y_new = numerator / denominator

    return y_new
