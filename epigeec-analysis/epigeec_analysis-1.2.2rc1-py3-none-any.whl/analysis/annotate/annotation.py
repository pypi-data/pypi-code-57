import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

DESCRIPTION_CLUSTERING_ALGORITHM = 'clusteringAlgorithm={}'
DESCRIPTION_LINKAGE_METHOD = 'linkageMethod={}'

class Annotation:
    def __init__(self, matrix, metadata, comparison):
        self.matrix = matrix
        self.metadata = metadata
        self.comparison = comparison

        if not metadata.key_intersection(matrix.get_file_names()):
            logger.warning("There's no match between the matrix and the metadata.")

    @property
    def description(self):
        description_list = []

        matrix_description = self.matrix.description

        if matrix_description:
            description_list.append(matrix_description)

        description_list.extend(
            [
                DESCRIPTION_CLUSTERING_ALGORITHM.format(self.clustering_algorithm),
                DESCRIPTION_LINKAGE_METHOD.format(self.linkage_method)
            ]
        )

        return ', '.join(description_list)

    def obtain_size_of_tags_in_category(self, category_name):
        return self.comparison.obtain_size_of_tags_in_category(category_name)

    def obtain_file_names_with_tag_name(self, tag_name):
        return self.comparison.obtain_file_names_with_tag_name(tag_name)

    def obtain_cluster_name(self, cluster_id):
        return self.comparison.obtain_cluster_name(cluster_id)

    def obtain_size_of_tags_from_tag_names(self, cluster_id, category_name, tag_names):
        return self.comparison.obtain_size_of_tags_from_tag_names(cluster_id, category_name, tag_names)

    def obtain_file_names_tag_names(self, category_name):
        return self.comparison.obtain_file_names_tag_names(category_name)

    def obtain_ordered_tag_names(self, category_name):
        file_names_tag_names = self.comparison.obtain_file_names_tag_names(category_name)
        return [file_names_tag_names[file_name]
                for file_name in self.matrix.get_file_names()]

    def make_flat_clusters(self):
        return self.comparison.make_flat_clusters(self.matrix)

    def obtain_clusters(self):
        return self.comparison.clusters

    @property
    def linkage_method(self):
        return self.comparison.clusters.linkage_method

    @property
    def clustering_algorithm(self):
        return self.comparison.clusters.clustering_algorithm

    def get_nb_clusters(self):
        return self.comparison.clusters.count

    def get_matrix(self):
        return self.matrix

    def get_file_names(self):
        return self.matrix.get_file_names()

    def get_metadata(self):
        return self.metadata

    def __len__(self):
        return len(self.matrix)

    def annotation_datagrid_iter(self, categories_names):
        for file_name in self.matrix.get_file_names():
            yield ([file_name, self.comparison.obtain_cluster_name_by_file_name(file_name)] + 
                   self.metadata.obtain_formated_dataset(file_name, categories_names))

class Comparison:
    ALL = 0
    def __init__(self, clusters, categories):
        self._clusters = clusters
        self._categories = categories

    @property
    def clusters(self):
        return self._clusters

    @property
    def categories(self):
        return self._categories

    def obtain_file_names_with_tag_name(self, tag_name):
        return self.categories.obtain_file_names_with_tag_name(tag_name)

    def obtain_size_of_tags_in_category(self, category_name):
        return self.categories.obtain_size_of_tags_in_category(category_name)

    def obtain_cluster_name(self, cluster_id):
        if cluster_id == self.ALL:
            return 'All'
        else:
            return self.clusters[cluster_id].get_name()

    def obtain_size_of_tags_from_tag_names(self, cluster_id, category_name, tag_names):
        if cluster_id == self.ALL:
            file_names = self.clusters.get_file_names()
        else:
            file_names = self.clusters[cluster_id].get_file_names()
        return self.categories.obtain_size_of_tags_from_tag_names(category_name, tag_names, file_names)

    def obtain_file_names_tag_names(self, category_name):
        return self.categories.obtain_file_names_tag_names(category_name)

    def obtain_cluster_name_by_file_name(self, file_name):
        return self.clusters.obtain_cluster_name(file_name)

    def make_flat_clusters(self, matrix):
        return self._clusters.make_flat_clusters(matrix)
