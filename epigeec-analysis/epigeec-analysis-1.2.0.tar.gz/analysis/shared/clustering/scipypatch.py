import numpy as np
import scipy.cluster.hierarchy as sch

from analysis.shared.clustering.clusters import Clusters

class ScipyPatch(object):
    """
    The scipy dendrogram imposes an order for the matrix and the clusters.
    ScipyPatch fixes issues caused with incompatible naming and ordering.
    """

    @staticmethod
    def reorder_matrix(clusters, matrix):
        """
        This method reorder the matrix with the dendogram.
        """
        file_names = matrix.get_file_names()
        Z = ScipyPatch.make_dendrogram(clusters, matrix)
        return matrix.sub_matrix(reversed([file_names[leaf] for leaf in Z['leaves']]))

    @staticmethod
    def rename_clusters(clusters, matrix):
        Z = ScipyPatch.make_dendrogram(clusters, matrix)

        real_cluster_order = ScipyPatch._obtain_order(reversed(Z['ivl']))
        wanted_cluster_order = range(1, clusters.count + 1) # [1..n]

        remap_dict = {r:w for r, w in zip(real_cluster_order, wanted_cluster_order)}

        return clusters.remap_clusters_ids([remap_dict[x] for x in clusters.make_flat_clusters(matrix)], matrix)

    @staticmethod
    def make_dendrogram(clusters, matrix):
        """
        This method uniformize the way the dendrogram is made with this objects methods and the code.
        """
        return sch.dendrogram(clusters.linkage_matrix,
                              color_threshold=ScipyPatch._compute_color_threshold(clusters),
                              orientation='left',
                              distance_sort='descending',
                              labels=clusters.make_flat_clusters(matrix))

    @staticmethod
    def _compute_color_threshold(clusters):
        """
        Compute the color threshold for the dendrogram.
        
        Reference
        -----
        See color_threshold of scipy.cluster.hierarchy.dendrogram
        """
        return clusters.linkage_matrix[-(clusters.count-1),2]

    @staticmethod
    def _obtain_order(flat_cluster):
        """
        This function takes a flat_cluster and return the order of the ids.
        """
        inside = set()

        def add_if_not_inside(x):
            if x in inside:
                return False
            else:
                inside.add(x)
                return True

        return filter(add_if_not_inside, flat_cluster)