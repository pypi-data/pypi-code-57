import numpy as np


# This is an implementation of metricmap published in 'An Index Structure
# for Data Mining and Clustering' (2000) by Wang.
#   O:            list of cells which contains the items
#   d:            distance function (O x O -> R)
#   k:            destination dimension of the embedding
def metricmap(obj_set, dist_func, num_dim, dist_mat=None):
    n_items = len(obj_set)

    if num_dim > np.floor(n_items / 2):
        num_dim = np.floor(n_items / 2).astype(np.int64)

    # create subset with double number of elements than dimension
    m = 2 * num_dim
    subset_id = np.random.permutation(n_items)
    subset_id = subset_id[:m]
    subset = [obj_set[i] for i in subset_id]

    # set first item as orgin and remove it
    s0 = subset[0]
    s0_id = subset_id[0]
    subset.pop(0)
    subset_id = subset_id[1:]
    m = m-1

    # compute distances with respect to the origin
    m_mat = np.zeros((m, m))
    for i in range(m-1):
        for j in range(i+1, m):
            # compute distances in the reference set
            if dist_mat is None:
                m_mat[i, j] = (dist_func(subset[i], s0)**2 + dist_func(subset[j], s0)**2
                               - dist_func(subset[i], subset[j])**2) / 2
            else:
                m_mat[i, j] = (dist_mat[subset_id[i], s0_id] ** 2 + dist_mat[subset_id[j], s0_id] ** 2
                               - dist_mat[subset_id[i], subset_id[j]] ** 2) / 2
            m_mat[j, i] = m_mat[i, j]

    # calculate orthogonal basis of m_mat and the eigenvalues
    eig_val, eig_vec = np.linalg.eigh(m_mat)

    eig_val = np.flip(eig_val)
    eig_vec = np.flip(eig_vec, axis=1)
    eig_vec_inv = eig_vec.T

    # get a num_dim submatrix of eig_vec
    eig_vec_inv_dim = eig_vec_inv[:num_dim, :num_dim]

    # make a diagonal matrix with the square root of the corresponding eigenvalues
    c = np.sqrt(np.abs(eig_val[:num_dim]))
    c[c == 0] = 1
    c_mat = np.diag(c)

    # ********* project objects *********
    emb = np.zeros((n_items, num_dim))

    # current projection
    h_k = np.zeros(num_dim)

    for o in range(n_items):
        for d in range(num_dim):
            # compute projection of object_set[o] in dimension d
            if dist_mat is None:
                h_k[d] = (dist_func(s0, obj_set[o])**2 + dist_func(s0, subset[d])**2
                          - dist_func(obj_set[o], subset[d])**2) / 2
            else:
                h_k[d] = (dist_mat[s0_id, o]**2 + dist_mat[s0_id, subset_id[d]]**2
                          - dist_mat[o, subset_id[d]]**2) / 2

        # map object
        emb[o, :] = np.linalg.solve(c_mat, eig_vec_inv_dim) @ h_k

    return emb


if __name__ == '__main__':
    # create random points
    points = np.random.rand(10, 10)

    #compute distances
    from gmtb.util import pdist
    from gmtb.util.distance import euclidean_dist
    dist = pdist(points, euclidean_dist)

    res1 = metricmap(points, euclidean_dist, 5)
    res2 = metricmap(points, euclidean_dist, 5, dist_mat=dist)

    dist_res1 = pdist(res1,euclidean_dist)
    dist_res2 = pdist(res2,euclidean_dist)

    print("Difference:")

