import unittest
from io import StringIO

from tests.context import analysis
from analysis.shared.matrix import Matrix
from analysis.shared.metadata import Metadata
from analysis.ari.breakdowns import Breakdowns, Breakdown, SubBreakdowns, SubBreakdown

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

class TestBreakdowns(unittest.TestCase):
    def setUp(self):
        self.metadata = Metadata.load_from_file(StringIO(METADATA_JSON), 'file_name')
        self.matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC))

    def tearDown(self):
        self.metadata = None
        self.matrix = None

    def test_make_breakdowns_full_full(self):
        breakdown_categories = ['one', 'two', 'three', 'six']
        restriction_categories = ['one', 'two', 'three', 'six']
        breakdowns_names = ['all', 'breakdown:one:1', 'breakdown:two:1', 'breakdown:two:2', 'breakdown:three:1', 'breakdown:three:2', 'breakdown:three:3', 'breakdown:six:1', 'breakdown:six:2', 'breakdown:six:3', 'breakdown:six:4', 'breakdown:six:5', 'breakdown:six:6']
        breakdowns_dataset_size = [6, 6, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1]
        breakdowns_nbs_clusters = [[1, 2, 3, 6], [1, 2, 3, 6], [1, 1, 2, 3], [1, 1, 2, 3], [1, 1, 1, 2], [1, 2, 1, 2], [1, 1, 1, 2], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
        # full_full
        full_full = Breakdowns.make_breakdowns(self.matrix, self.metadata, breakdown_categories, restriction_categories, LINKAGE_METHOD)
        self.assertEqual(len(full_full), 13)
        self.assertEqual([b.get_name() for b in full_full], breakdowns_names)
        self.assertEqual([b.get_dataset_size() for b in full_full], breakdowns_dataset_size)
        self.assertEqual([b.get_nbs_clusters() for b in full_full], breakdowns_nbs_clusters)

    def test_make_breakdowns_empty_full(self):
        breakdown_categories = []
        restriction_categories = ['one', 'two', 'three', 'six']
        breakdowns_names = set(['all'])
        breakdowns_dataset_size = [6]
        breakdowns_nbs_clusters = [[1, 2, 3, 6]]
        # empty_full
        empty_full = Breakdowns.make_breakdowns(self.matrix, self.metadata, breakdown_categories, restriction_categories, LINKAGE_METHOD)
        self.assertEqual(len(empty_full), 1)
        self.assertEqual(set([b.get_name() for b in empty_full]), breakdowns_names)
        self.assertEqual([b.get_dataset_size() for b in empty_full], breakdowns_dataset_size)
        self.assertEqual([b.get_nbs_clusters() for b in empty_full], breakdowns_nbs_clusters)

    def test_make_breakdowns_full_empty(self):
        breakdown_categories = ['one', 'two', 'three', 'six']
        restriction_categories = []
        breakdowns_names = set(['all', 'breakdown:one:1', 'breakdown:two:1', 'breakdown:two:2', 'breakdown:three:1', 'breakdown:three:3', 'breakdown:three:2', 'breakdown:six:1', 'breakdown:six:3', 'breakdown:six:2', 'breakdown:six:5', 'breakdown:six:4', 'breakdown:six:6'])
        breakdowns_dataset_size = [6, 6, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1]
        breakdowns_nbs_clusters = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        # full_empty
        full_empty = Breakdowns.make_breakdowns(self.matrix, self.metadata, breakdown_categories, restriction_categories, LINKAGE_METHOD)
        self.assertEqual(len(full_empty), 13)
        self.assertEqual(set([b.get_name() for b in full_empty]), breakdowns_names)
        self.assertEqual([b.get_dataset_size() for b in full_empty], breakdowns_dataset_size)
        self.assertEqual([b.get_nbs_clusters() for b in full_empty], breakdowns_nbs_clusters)

    def test_make_breakdowns_empty_empty(self):
        breakdown_categories = []
        restriction_categories = []
        breakdowns_names = set(['all'])
        breakdowns_dataset_size = [6]
        breakdowns_nbs_clusters = [[]]
        # empty_empty
        empty_empty = Breakdowns.make_breakdowns(self.matrix, self.metadata, breakdown_categories, restriction_categories, LINKAGE_METHOD)
        self.assertEqual(len(empty_empty), 1)
        self.assertEqual(set([b.get_name() for b in empty_empty]), breakdowns_names)
        self.assertEqual([b.get_dataset_size() for b in empty_empty], breakdowns_dataset_size)
        self.assertEqual([b.get_nbs_clusters() for b in empty_empty], breakdowns_nbs_clusters)
