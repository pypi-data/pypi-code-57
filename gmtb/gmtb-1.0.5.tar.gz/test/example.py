import gmtb

# distance functions
from gmtb.util.distance import string_edit_dist,string_edit_wm
from gmtb.util import pdist

# kernel functions
from gmtb.kernel.kernel_functions import dist_sub, dist_sub_batch

# dpe
from gmtb.dpe import embed, compute_median_vector, reconstruct

# ewm
from gmtb.ewm import ewm

# kernel
from gmtb.kernel import compute_median as kernel_compute_median



# load dataset, a list of objects
dataset = list()
dataset.append("Hello World!")
dataset.append("Helo Woorld!")
dataset.append("Hallo Welt!")
dataset.append("Hella Wald")


# embedding dimension
dim = 3

# set distance function, any function or lambda with
# func(o1,o2) where o1, o2 are objects in list
# func(o1,o2) returns one scalar: the distance value
dist_func = string_edit_dist

# weighted mean function, any function or lambda with
# func(o1,o2,alpha) where o1,o2 are input objects, alpha is a scalar between 0 and 1
# func(o1,o2,alpha) returns a new object o, the weighted mean between these objects
weighted_mean_func = string_edit_wm


# precompute distance and kernel matrix. not neccessary, but removes repetition in case of several embeddings/reconstructions
D = pdist(dataset,dist_func)
K = dist_sub_batch(D,"nd",param=2)

####  Distance Preserving Embedding method #####
emb_matrix = embed(dataset,"cca",dim,dist_func,dist_mat=D)
med_vec = compute_median_vector(emb_matrix)
median, sod_result = reconstruct(med_vec,emb_matrix,dataset,dist_func,weighted_mean_func,"linear_recursive")
print("DPE Median = %s, SOD (object-space) = %d" % (median,sod_result))

# Evolutionary Weighted Mean
median, sod_result = ewm(dataset,dist_func,weighted_mean_func)
print("EWM Median = %s, SOD (object-space) = %d" % (median,sod_result))

# Kernel-based Median computation
kernel_function = lambda o1, o2: gmtb.kernel.kernel_functions.dist_sub(o1, o2, dist_func, "nd", param=2)
median, sod_result = kernel_compute_median(dataset, "median", kernel_function, weighted_mean_func, "linear_recursive",
                                                kernel_matrix=K, dist_func=dist_func)
print("Kernel Median = %s, SOD (kernel-space) = %d" % (median,sod_result))

