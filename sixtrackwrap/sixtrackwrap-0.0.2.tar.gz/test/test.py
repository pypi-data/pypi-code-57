from numba import jit, njit, prange
import numpy as np
import sixtracklib as st
import warnings
import os
import time


def accumulate_and_return(r, alpha, th1, th2, n_sectors):
    tmp_1 = ((th1 + np.pi) / (np.pi * 2)) * n_sectors
    tmp_2 = ((th2 + np.pi) / (np.pi * 2)) * n_sectors

    i_1 = np.empty(tmp_1.shape, dtype=np.int32)
    i_2 = np.empty(tmp_2.shape, dtype=np.int32)

    for i in prange(i_1.shape[0]):
        for j in range(i_1.shape[1]):
            i_1[i, j] = int(tmp_1[i, j])
            i_2[i, j] = int(tmp_2[i, j])

    result = np.empty(r.shape[0])
    matrices = np.empty((r.shape[0], n_sectors, n_sectors))
    count = np.zeros((r.shape[0], n_sectors, n_sectors), dtype=np.int32)

    for j in prange(r.shape[0]):
        matrix = np.zeros((n_sectors, n_sectors)) * np.nan

        for k in range(r.shape[1]):
            if count[j, i_1[j, k], i_2[j, k]] == 0:
                matrix[i_1[j, k], i_2[j, k]] = r[j, k]
            else:
                matrix[i_1[j, k], i_2[j, k]] = (
                    (matrix[i_1[j, k], i_2[j, k]] * count[j, i_1[j, k],
                                                          i_2[j, k]] + r[j, k]) / (count[j, i_1[j, k], i_2[j, k]] + 1)
                )
            count[j, i_1[j, k], i_2[j, k]] += 1

        for a in range(matrix.shape[0]):
            for b in range(matrix.shape[1]):
                if matrix[a, b] == 0:
                    matrix[a, b] = np.nan

        result[j] = np.power(np.nanmean(np.power(matrix, 4)), 1/4)
        matrices[j, :, :] = matrix

    return count, matrices, result


def recursive_accumulation(count, matrices):
    n_sectors = count.shape[1]
    c = []
    m = []
    r = []
    validity = []
    c.append(count.copy())
    m.append(matrices.copy())
    r.append(np.nanmean(np.power(matrices, 4), axis=(1, 2)))
    validity.append(np.logical_not(
        np.any(np.isnan(matrices), axis=(1, 2))))
    while n_sectors >= 2 and n_sectors % 2 == 0:
        matrices *= count
        count = np.nansum(count.reshape(
            (count.shape[0], n_sectors//2, 2, n_sectors//2, 2)), axis=(2, 4))
        matrices = np.nansum(matrices.reshape(
            (matrices.shape[0], n_sectors//2, 2, n_sectors//2, 2)), axis=(2, 4)) / count
        result = np.nanmean(np.power(matrices, 4), axis=(1, 2))
        c.append(count.copy())
        m.append(matrices.copy())
        r.append(result.copy())
        validity.append(np.logical_not(
            np.any(np.isnan(matrices), axis=(1, 2))))
        n_sectors = n_sectors // 2
    return c, m, r, np.asarray(validity, dtype=np.bool)


coso1, coso2, _ = accumulate_and_return(np.ones((2,10)) * 2, np.ones((2,10)), np.ones((2,10)), np.ones((2,10)),4)

c, m, r, v = recursive_accumulation(coso1, coso2)

print(m, r, v)
