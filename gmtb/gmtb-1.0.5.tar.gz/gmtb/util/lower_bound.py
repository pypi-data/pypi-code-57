import numpy as np
from scipy.optimize import linprog
from scipy.special import comb
import scipy.sparse
from .k_medians import k_medians

import networkx as nx

from gmtb.kernel.compute_weights import compute_weights
from gmtb.kernel.kernel_functions import dist_sub_batch


# linear programming based lower bound
def lp_lower_bound(dist_mat):
    n = np.size(dist_mat,1)

    index = 0
    c = np.ones(n)
    #a = np.zeros((3 * comb(n, 2, exact=True) + n, n))
    b = np.zeros((3 * comb(n, 2, exact=True) + n, 1))

    a = scipy.sparse.lil_matrix((3 * comb(n, 2, exact=True) + n, n))
    #b = scipy.sparse.lil_matrix((3 * comb(n, 2, exact=True) + n, 1))

    # for i < j
    # -x_i + -x_j <= -dist_mat_ij
    # -x_i +  x_j <=  dist_mat_ij
    #  x_i + -x_j <=  dist_mat_ij
    for j in range(1,n):
        for i in range(j):
            a[index:index+3, [i, j]] = [[-1, -1], [-1, 1], [1, -1]]
            b[index:index+3] = [[-dist_mat[i, j]], [dist_mat[i, j]], [dist_mat[i, j]]]
            index = index + 3

    # for i:
    # -x_j <= 0
    a[-n:, :] = -np.eye(n)
    for j in range(n):
        a[-n+j, j] = -1
    #b[-n:, :] = np.zeros((n ,1))

    # solve linprog. interior-point seems better in first tests
    result = linprog(c, a, b, options={'sparse': True})

    return np.sum(result.x)

def graph_lower_bound(dist_mat):
    # cost matrix: negative distance and Diagonal is infinity
    #cost_matrix = -dist_mat
    #np.fill_diagonal(cost_matrix, np.inf)

    # get pairs by graph matching
    g = nx.from_numpy_matrix(dist_mat)
    pairs = nx.max_weight_matching(g)

    # sum pair values
    sum = 0
    for (i,j) in pairs:
        sum = sum + dist_mat[i,j]

    return sum


# kernel based lower bound
def kernel_lower_bound(dist_mat,kernel_mat):

    # based on k_lin
    if kernel_mat is None:
        origin_idx = k_medians(dist_mat,1)
        kernel_mat = dist_sub_batch(dist_mat,"lin",origin_idx)
        # based on k_nd
        # kernel_mat = dist_sub_batch(dist_mat, "nd", param=2)


    # compute weights
    weights, k_median_set, k_median_median = compute_weights(kernel_mat, True)

    tmp_bound = k_median_median - 2 * k_median_set + np.diag(kernel_mat)

    # remove too small values
    tmp_bound[tmp_bound < 1e-10] = 1e-10

    return np.sum(np.sqrt(tmp_bound))


def lower_bound(dist_mat, method="lp", kernel_mat=None):
    if method == "lp":
        return lp_lower_bound(dist_mat)
    elif method == "graph":
        return graph_lower_bound(dist_mat)
    elif method == "kernel":
        return kernel_lower_bound(dist_mat,kernel_mat)
    else:
        raise ValueError("lower_bound: Wrong method")