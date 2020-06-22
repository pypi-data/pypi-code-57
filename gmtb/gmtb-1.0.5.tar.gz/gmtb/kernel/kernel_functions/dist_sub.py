import numpy as np

# for testing
import gmtb.util
import gmtb.util.distance


# base scalar product of the distance substitution kernel
def dist_sub_prod(x,y,dist_func,origin):
    return -1/2 * (np.power(dist_func(x,y),2) - np.power(dist_func(x,origin),2) - np.power(dist_func(y,origin),2))


# normal version of the distance substitution kernel
def dist_sub(x, y, dist_func, kernel_type, origin=None, param=None):
    if kernel_type == "lin":
        return dist_sub_prod(x,y,dist_func,origin)

    if kernel_type == "nd":
        return -np.power(dist_func(x, y), param)

    if kernel_type == "pol":
        return np.power(1 + param[0] * dist_sub_prod(x,y,dist_func,origin), param[1])

    if kernel_type == "rbf":
        return np.exp(-param * np.power(dist_func(x,y),2))
    else:
        raise ValueError("kernel_type not found")


# base scalar product of the batch version of the distance substitution kernel
def dist_sub_batch_prod(dist_mat, origin_idx):
    return 1 / 2 * (np.add.outer(np.squeeze(dist_mat[:, origin_idx] * dist_mat[:, origin_idx]),
                                 np.squeeze(dist_mat[origin_idx,:] * dist_mat[origin_idx,:]))
                    - dist_mat * dist_mat)


# batch version of the distance substitution kernels
def dist_sub_batch(dist_mat, kernel_type, origin_idx=None, param=None):
    if kernel_type == "lin":
        return dist_sub_batch_prod(dist_mat, origin_idx)
    if kernel_type == "nd":
        return -np.power(dist_mat, param)
    if kernel_type == "pol":
        return np.power(1 + param[0] * dist_sub_batch_prod(dist_mat,origin_idx), param[1])
    if kernel_type == "rbf":
        return np.exp(-param * dist_mat * dist_mat)
    else:
        raise ValueError("kernel_type not found")



if __name__ == "__main__":


    points = np.random.rand(10,5)

    def kernel(x,y):
        return dist_sub(x,y,gmtb.util.distance.euclidean_dist,"lin",origin=points[0])

    dist_mat = gmtb.util.pdist(points, gmtb.util.distance.euclidean_dist)
    kernel_mat = gmtb.util.pdist(points,kernel)
    kernel_mat_batch = dist_sub_batch(dist_mat, "lin", origin_idx=0)

    print("Max diff: %f" % np.max(np.abs(kernel_mat - kernel_mat_batch)))