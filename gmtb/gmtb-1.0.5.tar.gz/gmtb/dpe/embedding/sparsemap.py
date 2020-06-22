import numpy as np

from gmtb.util import pdist
from gmtb.util.distance import euclidean_dist


# greedy resampling to be used by sparsemap
def greedy_resampling(obj_set, dist_func, emb, p_res, num_dim):

    # if the embedding is already small enough
    if emb.shape[1] <= num_dim:
        return emb

    n_items = len(obj_set)

    # choose random subset
    subset = np.random.permutation(n_items).astype(np.int64)
    subset = subset[:round(n_items * p_res)]
    obj_subset = [obj_set[i] for i in subset]

    # calculate distances of items to the subset
    dist_subset_obj = pdist(obj_subset, dist_func)

    # create finished embedding
    emb_out = np.zeros((n_items,num_dim))

    for d in range(num_dim):

        n_features = emb.shape[1]
        k_stress = np.zeros(n_features)

        # prepare array to attach values
        ft = np.zeros((n_items, d+1))
        ft[:,:d] = emb_out[:,:d]

        #for each possible dimension in the original embedding
        for f in range(n_features):
            # try attaching this dimension to the final embedding
            ft[:,d] = emb[:,f]

            # calculate distance
            ft_dist = pdist(ft[subset,:], euclidean_dist)
            k_stress[f] = np.sum((ft_dist - dist_subset_obj)**2)

        # get the best feature combination
        f_best = np.argmin(k_stress)

        # attach best feature
        emb_out[:, d] = emb[:, f_best]

        # remove from full embedding
        np.delete(emb, f_best, axis=1)

    return emb_out


# this is an implementation of sparsemap published in 'cluster-preserving embedding of
# proteins' (1999) by Hristescu and Farach-Colton.
def sparsemap(obj_set, dist_func, num_dim, dist_mat=None, p_sigma=0.2, p_res=0.2):

    n_items = len(obj_set)

    # number of rows and columns for the reference matrix
    n_sets_rows = np.floor(np.log2(n_items)).astype(np.int64)
    n_sets_cols = np.floor(np.log2(n_items)).astype(np.int64)

    # number of reference sets
    n_sets = n_sets_cols * n_sets_rows

    # reference sets as row vector
    ref_sets = [None] * n_sets

    # create matrix of reference sets R. Every cell contains a set
    x_index = 0

    for i in range(n_sets_rows):
        for j in range(n_sets_cols):
            # create random subset
            x = np.random.permutation(n_items)
            ref_sets[x_index] = x[:2**i]

            # if  the stored set contains all avaliable items
            if len(ref_sets[x_index]) == n_items:
                ref_sets[x_index+1:] = []
                n_sets = x_index+1
                break

            x_index = x_index + 1

    # matrix for lipschitz-embedding
    emb = np.zeros((n_items,n_sets))

    for i in range(n_sets):
        # get current reference set and its length
        x = ref_sets[i]

        # for every item with index p of 0
        for p in range(n_items):
            # for every item q in the reference set, compute the approximated distance
            approx_dist_x = np.zeros(len(x))

            for q in range(len(x)):
                # if  there are embedded features avaliable, the approximated distance will be computed
                if i > 0:
                    approx_dist_x[q] = np.sum((emb[p,:i-1] - emb[x[q],:i-1]) ** 2)
                else:
                    if dist_mat is None:
                        approx_dist_x[q] = dist_func(obj_set[p], obj_set[q])
                    else:
                        approx_dist_x[q] = dist_mat[p,q]

            # if there are embedded features avaliable, the current distances are approximated
            # and a subset of true distances will be calculated
            if i > 0:

                # calcualte order
                approx_dist_x_order = np.argsort(approx_dist_x)

                # choose number of items in current subset for which the true distances will be calculated
                n_true_dist_x_sub = np.ceil(len(approx_dist_x)*p_sigma).astype(np.int64)

                # calculate true distances
                true_dist_x_sub = np.zeros(n_true_dist_x_sub)
                for q in range(n_true_dist_x_sub):
                    if dist_mat is None:
                        true_dist_x_sub[q] = dist_func(obj_set[p],obj_set[x[approx_dist_x_order[q]]])
                    else:
                        true_dist_x_sub[q] = dist_mat[p, x[approx_dist_x_order[q]]]
            else:
                true_dist_x_sub = approx_dist_x

            # the minimum distance is the k-th feature for p
            emb[p,i] = np.min(true_dist_x_sub)

    # perform greedy resampling to reduce dimensions
    return greedy_resampling(obj_set, dist_func, emb, p_res, num_dim)


if __name__ == '__main__':
    # create random points
    points = np.random.rand(10, 10)

    #compute distances
    dist = pdist(points, euclidean_dist)

    res1 = sparsemap(points, euclidean_dist, 5)
    res2 =  sparsemap(points, euclidean_dist, 5, dist_mat=dist)

    dist_res1 = pdist(res1,euclidean_dist)
    dist_res2 = pdist(res2,euclidean_dist)

    print("Difference:")


