import unittest
from io import StringIO

from tests.context import analysis
from analysis.shared.matrix import Matrix
from analysis.shared.metadata import Metadata
from analysis.shared.clustering.hierarchical_clustering import HierarchicalClustering
from analysis.annotate.annotation import Annotation, Comparison
from analysis.shared.categories import Categories
from analysis.shared.clustering.scipypatch import ScipyPatch

MATRIX_BASIC = u'''\t3847bb31fbec071306b5c2ce502458c4\t4fe8dec76ed3d303e0dcc68e38c96f6f\ta773fa2c902e52ed2e0cf3fb3f4394df\t0b04a1ffef60af4e5802c1038f902eb0\t6ed513f3a5e97687b04cd10c1ed619a7\t0f87a2acadf34fee74c5de9c1f33ebb2
3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0'''
METADATA_JSON = u'''
{"count": 6,
"name": "test_breakdown",
"datasets": [
{"file_name": "3847bb31fbec071306b5c2ce502458c4", "one": "1", "two": "1", "three": "1", "six": "1"},
{"file_name": "4fe8dec76ed3d303e0dcc68e38c96f6f", "one": "1", "two": "1", "three": "1", "six": "2"},
{"file_name": "a773fa2c902e52ed2e0cf3fb3f4394df", "one": "1", "two": "1", "three": "2", "six": "3"},
{"file_name": "0b04a1ffef60af4e5802c1038f902eb0", "one": "1", "two": "2", "three": "2", "six": "4"},
{"file_name": "6ed513f3a5e97687b04cd10c1ed619a7", "one": "1", "two": "2", "three": "3", "six": "5"},
{"file_name": "0f87a2acadf34fee74c5de9c1f33ebb2", "one": "1", "two": "2", "three": "3", "six": "6"}
]}
'''
LINKAGE_METHOD = 'average'
CATEGORIES_NAMES = ['one', 'two', 'three', 'six']
DESIRED_NB_CLUSTERS = 3

class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.metadata = Metadata.load_from_file(StringIO(METADATA_JSON), 'file_name')
        self.matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC))
        self.clusters = HierarchicalClustering.make_clusters(self.matrix, LINKAGE_METHOD, DESIRED_NB_CLUSTERS)
        self.categories = Categories.make_categories(self.metadata, self.matrix.get_file_names(), CATEGORIES_NAMES)

        remapped_clusters = ScipyPatch.rename_clusters(self.clusters, self.matrix)
        self.comparison = Comparison(remapped_clusters, self.categories)
        self.clusters = remapped_clusters

        self.annotation = Annotation(self.matrix, self.metadata, self.comparison)

    def tearDown(self):
        self.metadata = None
        self.matrix = None
        self.clusters = None
        self.categories = None
        self.comparison = None
        self.annotation = None

    @unittest.skip("Not Implemented")
    def test_description(self):
        self.fail("Not Implemented")

    @unittest.skip("Not Implemented")
    def test_obtain_size_of_tags_in_category(self):
        self.fail("Not Implemented")

    @unittest.skip("Not Implemented")
    def test_obtain_file_names_with_tag_names(self):
        self.fail("Not Implemented")

    def test_obtain_cluster_name(self):
        # good_normal
        good_normal = self.annotation.obtain_cluster_name(1)
        self.assertEqual(good_normal, 'A')

        # good_all
        good_all = self.annotation.obtain_cluster_name(0)
        self.assertEqual(good_all, 'All')

        # bad
        with self.assertRaises(KeyError):
            self.annotation.obtain_cluster_name(-1)

    @unittest.skip('mock it!')
    def test_obtain_size_of_tags_from_tag_names(self):
        good_normal = self.annotation.obtain_size_of_tags_from_tag_names(1, 'one', ['1'])
        self.assertEqual(good_normal, 1)

        # good_all
        good_all = self.annotation.obtain_size_of_tags_from_tag_names(0, 'one', ['1'])
        self.assertEqual(good_all, 6)

        # bad
        with self.assertRaises(KeyError):
            self.annotation.obtain_size_of_tags_from_tag_names(-1, 'one', ['1'])

    @unittest.skip("Not Implemented")
    def test_obtain_file_names_tag_names(self):
        self.fail("Not Implemented")

    def test_obtain_ordered_tag_names(self):
        # good_normal
        good_normal = self.annotation.obtain_ordered_tag_names('three')
        self.assertEqual(good_normal, ['1', '1', '2', '2', '3', '3'])

        # bad
        with self.assertRaises(KeyError):
            self.annotation.obtain_ordered_tag_names('potato')

    @unittest.skip("Not Implemented")
    def test_annotation_datagrid_iter(self):
        self.fail("Not Implemented")

@unittest.skip("Not Implemented")
class TestComparison(unittest.TestCase):
    def test_obtain_file_names_with_tag_name(self):
        self.fail("Not Implemented")

    def test_obtain_size_of_tags_in_category(self):
        self.fail("Not Implemented")

    def test_obtain_cluster_name(self):
        self.fail("Not Implemented")

    def test_obtain_size_of_tags_from_tag_names(self):
        self.fail("Not Implemented")

    def test_obtain_file_names_tag_names(self):
        self.fail("Not Implemented")

    def test_obtain_cluster_name_by_file_name(self):
        self.fail("Not Implemented")
