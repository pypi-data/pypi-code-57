import numpy as np


# base scalar product of the edit kernel
def edit_prod(x,y,dist_func,origin):
    return -1/2 * (np.power(dist_func(x,y),2) - np.power(dist_func(x,origin),2) - np.power(dist_func(y,origin),2))


# base scalar product of the batch version of the edit kernel
def edit_prod_batch(dist_mat, origin_idx):
    return 1 / 2 * (np.add.outer(np.squeeze(dist_mat[:, origin_idx] * dist_mat[:, origin_idx]),
                                 np.squeeze(dist_mat[origin_idx,:] * dist_mat[origin_idx,:]))
                    - dist_mat * dist_mat)


# normal version of the distance substitution kernel
def edit_kernel(x, y, dist_func, origin_set):
    kernels = np.zeros(len(origin_set));

    for i in range(len(origin_set)):
        kernels[i] = edit_prod(x,y,dist_func,origin_set[i])

    return np.sum(kernels)


def edit_kernel_batch(dist_mat, origin_set_ind):
    kernel_mat = np.zeros((np.shape(dist_mat)[0], np.shape(dist_mat)[1], len(origin_set_ind)))

    for i in range(len(origin_set_ind)):
        kernel_mat[:,:,i] = edit_prod_batch(dist_mat,origin_set_ind[i])

    return np.sum(kernel_mat, axis=2)
