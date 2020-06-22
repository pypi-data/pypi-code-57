from gmtb.util.distance.partition_dist import relabel

import numpy as np

def partition_kernel(x,y):
    y = relabel(y,x)

    # compute number of disagreements
    return len(x) - np.sum(x != y)
