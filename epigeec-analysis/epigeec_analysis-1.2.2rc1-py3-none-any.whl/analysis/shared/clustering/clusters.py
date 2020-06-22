from analysis.shared.util.labels import int_label_to_letter_label

class Clusters(dict):
    def __init__(self, clusters_dict, linkage_matrix, linkage_method, clustering_algorithm):
        super(Clusters, self).__init__(clusters_dict)
        self.clusters_ref = {file_name:cl
                             for cl in self.values()
                             for file_name in cl.get_file_names()}
        self._linkage_matrix = linkage_matrix
        self._linkage_method = linkage_method
        self._clustering_algorithm = clustering_algorithm

    def get_file_names(self):
        return self.clusters_ref.keys()

    def obtain_cluster_name(self, file_name):
        return self.clusters_ref[file_name].get_name()

    def make_flat_clusters(self, matrix):
        return [self.clusters_ref[fn].get_id() for fn in matrix.get_file_names()]

    @property
    def linkage_matrix(self):
        return self._linkage_matrix

    @property
    def linkage_method(self):
        return self._linkage_method

    @property
    def clustering_algorithm(self):
        return self._clustering_algorithm

    @property
    def count(self):
        return len(self)
    
    @staticmethod
    def make_clusters(cluster_ids, file_names, linkage_matrix, linkage_method, clustering_algorithm):
        if len(cluster_ids) != len(file_names):
            raise Exception('The length of the two list aren\'t matching!')

        clusters_file_names = {cluster_id:[] for cluster_id in set(cluster_ids)}

        for cluster_id, file_name in zip(cluster_ids, file_names):
            clusters_file_names[cluster_id].append(file_name)

        return Clusters({cls_id:Cluster.make_cluster(cls_id, md5s)
                         for cls_id, md5s in clusters_file_names.items()},
                        linkage_matrix,
                        linkage_method,
                        clustering_algorithm)

    def remap_clusters_ids(self, new_clusters_ids, matrix):
        return Clusters.make_clusters(new_clusters_ids, matrix.get_file_names(), self.linkage_matrix, self.linkage_method, self.clustering_algorithm)

class Cluster:
    def __init__(self, cluster_id, cluster_name, file_names):
        self.cluster_id = cluster_id
        self.name = cluster_name
        self.file_names = file_names

    def get_id(self):
        return self.cluster_id

    def get_name(self):
        return self.name

    def get_file_names(self):
        return self.file_names

    def __len__(self):
        return len(self.file_names)

    @staticmethod
    def make_cluster(cluster_id, file_names):
        return Cluster(cluster_id,
                       int_label_to_letter_label(cluster_id),
                       file_names)
