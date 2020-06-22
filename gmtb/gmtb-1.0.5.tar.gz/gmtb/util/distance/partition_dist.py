import numpy as np
from munkres import Munkres


# relabel clustering y to match the most amount of labels with x without changing clusterings themselves
def relabel(y, x):

    # compute cost matrix
    max_label = max(max(x), max(y))
    cost_matrix = np.zeros((max_label + 1, max_label + 1))
    for i in range(len(x)):
        cost_matrix[x[i], y[i]] = cost_matrix[x[i], y[i]] - 1

    # assignment
    assignment = Munkres().compute(cost_matrix)

    #assignment = munkres(cost_matrix).nonzero()

    # relabel
    y_tmp = np.copy(y)
    for i in range(1,max_label+1):
        y_tmp[y == assignment[i][1]] = assignment[i][0]

    return y_tmp


# computes the partition distance between two clusterings
def partition_dist(x, y):
    return np.sum(x != relabel(y, x))


# computes the weighted mean between two clusterings based on the partition distance
def partition_wm(x, y, alpha):
    y_tmp = relabel(y, x)

    # compute distance
    d = np.sum(x != y_tmp)

    # find labels that differ
    idx = (x != y_tmp)

    d_changed = 0
    i = 0
    mean = np.copy(x)

    while d_changed < round(alpha*d):
        # find next index
        while not idx[i]:
            i = i + 1
        # change it
        mean[i] = y_tmp[i]
        i = i + 1
        d_changed = d_changed + 1

    return mean
