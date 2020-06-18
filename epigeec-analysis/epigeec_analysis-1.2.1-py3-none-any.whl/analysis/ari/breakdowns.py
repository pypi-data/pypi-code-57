from analysis.shared.clustering.hierarchical_clustering import HierarchicalClustering
from analysis.shared.clustering.clusters import Clusters, Cluster
from analysis.shared.categories import Categories, Category, Tags, Tag
from sklearn.metrics import adjusted_rand_score

class Breakdowns(list):
    def __init__(self, restriction_categories, *args):
        super(Breakdowns, self).__init__(*args)
        self.restriction_categories = restriction_categories

    def get_restriction_categories(self):
        return self.restriction_categories

    @staticmethod
    def make_breakdowns(matrix, metadata, breakdown_categories, restriction_categories, linkage_method):
        categories = Categories.make_categories(metadata,
                                                matrix.get_file_names(),
                                                set(breakdown_categories + restriction_categories))

        return Breakdowns(restriction_categories,
                          [Breakdown.make_breakdown_of_all(matrix,
                                                           categories,
                                                           restriction_categories,
                                                           linkage_method)] +
                          [Breakdown.make_breakdown(matrix,
                                                    metadata,
                                                    br_cat,
                                                    restriction_categories,
                                                    br_tag,
                                                    linkage_method)
                           for br_cat in breakdown_categories
                           for br_tag in categories.obtain_sorted_tags(br_cat)])

class Breakdown:
    def __init__(self, breakdown_name, dataset_size, sub_breakdowns):
        self.breakdown_name = breakdown_name
        self.dataset_size = dataset_size
        self.sub_breakdowns = sub_breakdowns

    def get_name(self):
        return self.breakdown_name

    def get_dataset_size(self):
        return self.dataset_size

    def get_aris(self):
        return self.sub_breakdowns.get_aris()

    def get_nbs_clusters(self):
        return self.sub_breakdowns.get_nbs_clusters()

    @staticmethod
    def make_breakdown(matrix, metadata, breakdown_category, restriction_categories, tag, linkage_method):
        breakdown_name = 'breakdown:{}:{}'.format(breakdown_category, tag.get_name())
        sub_matrix = matrix.sub_matrix(tag.get_file_names())
        sub_categories = Categories.make_categories(metadata,
                                                    tag.get_file_names(),
                                                    restriction_categories)
        cluster_maker = HierarchicalClustering(sub_matrix, linkage_method)

        return Breakdown(breakdown_name,
                         len(sub_matrix),
                         SubBreakdowns.make_sub_breakdowns(sub_matrix,
                                                           sub_categories,
                                                           restriction_categories,
                                                           cluster_maker))

    @staticmethod
    def make_breakdown_of_all(matrix, categories, restriction_categories, linkage_method):
        cluster_maker = HierarchicalClustering(matrix, linkage_method)
        return Breakdown('all',
                         len(matrix),
                         SubBreakdowns.make_sub_breakdowns(matrix,
                                                           categories,
                                                           restriction_categories,
                                                           cluster_maker))

class SubBreakdowns(list):
    def __init__(self, *args):
        super(SubBreakdowns, self).__init__(*args)

    def get_aris(self):
        return [sb.get_ari() for sb in self]

    def get_nbs_clusters(self):
        return [sb.get_nb_clusters() for sb in self]

    @staticmethod
    def make_sub_breakdowns(matrix, categories, restriction_categories, cluster_maker):
        return SubBreakdowns([SubBreakdown.make_sub_breakdown(matrix,
                                                              categories[category_name],
                                                              cluster_maker)
                              for category_name in restriction_categories])

class SubBreakdown:
    def __init__(self, ari_value, nb_clusters):
        self.ari_value = ari_value
        self.nb_clusters = nb_clusters

    def get_ari(self):
        return self.ari_value

    def get_nb_clusters(self):
        return self.nb_clusters

    @staticmethod
    def make_sub_breakdown(matrix, category, cluster_maker):
        flat_clusters = cluster_maker \
                        .run(len(category)) \
                        .make_flat_clusters(matrix)
        cat_flat_clusters = category.make_flat_clusters(matrix)

        # The data sources needs to be align
        # In our case we use the matrix order
        return SubBreakdown(adjusted_rand_score(flat_clusters, cat_flat_clusters),
                            len(category))
