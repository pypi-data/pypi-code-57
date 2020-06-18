import unittest
from mock import MagicMock
from io import StringIO

from tests.context import analysis
from analysis.shared.clustering.clusters import Clusters, Cluster

METADATA_JSON = '''
{"count": 2,
"name": "test1",
"datasets": [
{"cell_type": "hindlimb bud", "assay": "H3K27ac", "file_name": "MS046901", "assay_category": "Histone Modifications", "md5sum": "f0fd84b5c0c7b0c56e165c8e0963e8c2", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "8"},
{"cell_type": "forelimb bud", "assay": "H3K27ac", "file_name": "MS046801", "assay_category": "Histone Modifications", "md5sum": "5600791b332ab4a88fade77ba50be26a", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "9"}
]}
'''
FILE_NAMES = ['MS046901', 'MS046801']

class TestClusters(unittest.TestCase):
    def setUp(self):
        self.linkage_matrix = None
        self.linkage_method = None
        self.clustering_algorithm = None

    def tearDown(self):
        self.linkage_matrix = None
        self.linkage_method = None
        self.clustering_algorithm = None

    def test_obtain_cluster_name(self):
        two_clusters = Clusters.make_clusters([1, 2], FILE_NAMES, self.linkage_matrix, self.linkage_method, self.clustering_algorithm)
        for name, fn in zip(['A', 'B'], FILE_NAMES):
            self.assertEqual(two_clusters.obtain_cluster_name(fn), name)

        with self.assertRaises(KeyError):
            two_clusters.obtain_cluster_name('potato')

    def test_make_clusters(self):
        # Two clusters
        two_clusters = Clusters.make_clusters([1, 2], FILE_NAMES, self.linkage_matrix, self.linkage_method, self.clustering_algorithm)
        self.assertEqual(len(two_clusters), 2)
        for cl_id, fn in zip([1, 2], FILE_NAMES):
            self.assertEqual(two_clusters[cl_id].get_file_names(), [fn])

        # One cluster
        one_clusters = Clusters.make_clusters([1, 1], FILE_NAMES, self.linkage_matrix, self.linkage_method, self.clustering_algorithm)
        self.assertEqual(len(one_clusters), 1)
        self.assertEqual(one_clusters[1].get_file_names(), FILE_NAMES)

        # Unmatching len
        with self.assertRaises(Exception):
            Clusters.make_clusters([1], FILE_NAMES, self.linkage_matrix, self.linkage_method, self.clustering_algorithm)

        with self.assertRaises(Exception):
            Clusters.make_clusters([1, 2], ['f0fd84b5c0c7b0c56e165c8e0963e8c2'], self.linkage_matrix, self.linkage_method, self.clustering_algorithm)

        # empty
        empty = Clusters.make_clusters([], [], self.linkage_matrix, self.linkage_method, self.clustering_algorithm)
        self.assertFalse(empty)

    def test_remap_clusters_ids(self):
        matrix = MagicMock()
        matrix.get_file_names = MagicMock(return_value=FILE_NAMES)
        two_clusters = Clusters.make_clusters([1, 2], FILE_NAMES, self.linkage_matrix, self.linkage_method, self.clustering_algorithm)

        remmapped = two_clusters.remap_clusters_ids([2, 1], matrix)

        for cl_id, fn, cl_name in zip([2, 1], FILE_NAMES, ['B', 'A']):
            self.assertEqual(remmapped[cl_id].get_file_names(), [fn])
            self.assertEqual(remmapped[cl_id].get_name(), cl_name)