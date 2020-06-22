import gmtb.util as util


# implementation of prototype embedding with the condition that dist_mat is already computed
def prototype(dist_mat, n_dim):

    prototype_index = util.k_medians(dist_mat, n_dim)

    return dist_mat[:, prototype_index]
