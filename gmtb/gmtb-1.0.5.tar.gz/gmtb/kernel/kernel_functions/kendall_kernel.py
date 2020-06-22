import numpy as np

import scipy.special

# Source:
# Jiao, Yunlong, and Jean-Philippe Vert. "The Kendall and Mallows kernels for permutations."
# IEEE transactions on pattern analysis and machine intelligence 40.7 (2017): 1755-1769.
#
# Based on the mapping:
# phi(r)_ij =  1/sqrt(comb(n,2)) , if r[i] > r[j]
#              0                 , if r[i] == r[j]
#             -1/sqrt(comb(n,2)) , if r[i] < r[j]
# with i < j
def kendall_tau_kernel(r1, r2):
    nc = 0
    nd = 0

    for i in range(len(r1)-1):
        for j in range(i, len(r2)):
            # skip comparing to itself
            if i == j:
                continue

            # sum errors
            if r1[i] < r1[j] and r2[i] < r2[j] or r1[i] > r1[j] and r2[i] > r2[j]:
                nc = nc + 1
            elif r1[i] < r1[j] and r2[i] > r2[j] or r1[i] > r1[j] and r2[i] < r2[j]:
                nd = nd + 1

    return (nc - nd) / scipy.special.comb(len(r1), 2)