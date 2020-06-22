import numpy as np


def pdist(set1, func, set2=None):

    if set2 is None:
        n = len(set1)
        p_matrix = np.zeros((n,n))

        for i in range(n):
            for j in range(i, n):
                p_matrix[i, j] = func(set1[i], set1[j])
                p_matrix[j, i] = p_matrix[i, j]

        return p_matrix

    else:
        n = len(set1)
        m = len(set2)

        p_matrix = np.zeros((n, m))

        for i in range(n):
            for j in range(m):
                p_matrix[i, j] = func(set1[i], set2[j])

        return p_matrix.squeeze()
