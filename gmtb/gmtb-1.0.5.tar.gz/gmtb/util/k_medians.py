from pyclustering.cluster.kmedoids import kmedoids
import numpy as np


def k_medians(dist_mat, subset_size):
    # create K-Medoids algorithm for processing distance matrix instead of points
    initial_medoids = range(subset_size)
    kmedoids_instance = kmedoids(dist_mat, initial_medoids, data_type='distance_matrix')

    # run cluster analysis and obtain results
    kmedoids_instance.process()

    #clusters = kmedoids_instance.get_clusters()
    medoids = np.asarray(kmedoids_instance.get_medoids(),dtype=np.int64)

    return medoids
