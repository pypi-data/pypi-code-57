import unittest
from mock import MagicMock, Mock
from io import BytesIO

from tests.context import analysis
from analysis.annotate.annotation import Annotation
from analysis.annotate.report.annotate_tsv import AnnotateTsv

CATEGORIES_NAMES = ['one', 'two', 'three', 'six']
ACTUAL_NB_CLUSTERS = 3

TSV_FILE_ANNOTATION_DATAGRID_ITER = [
    ['a773fa2c902e52ed2e0cf3fb3f4394df','A','1',u'\xe7','2','3'],
    ['4fe8dec76ed3d303e0dcc68e38c96f6f','B','1',u'\xe7','1','2'],
    ['6ed513f3a5e97687b04cd10c1ed619a7','B','1','2','3','5'],
    ['3847bb31fbec071306b5c2ce502458c4','C','1',u'\xe7','1','1'],
    ['0b04a1ffef60af4e5802c1038f902eb0','C','1','2','2','4'],
    ['0f87a2acadf34fee74c5de9c1f33ebb2','C','1','2','3','6']
]

TSV_FILE = u'''# description
file_name\tcluster(3)\tone\ttwo\tthree\tsix
a773fa2c902e52ed2e0cf3fb3f4394df\tA\t1\t\xe7\t2\t3
4fe8dec76ed3d303e0dcc68e38c96f6f\tB\t1\t\xe7\t1\t2
6ed513f3a5e97687b04cd10c1ed619a7\tB\t1\t2\t3\t5
3847bb31fbec071306b5c2ce502458c4\tC\t1\t\xe7\t1\t1
0b04a1ffef60af4e5802c1038f902eb0\tC\t1\t2\t2\t4
0f87a2acadf34fee74c5de9c1f33ebb2\tC\t1\t2\t3\t6'''.encode('utf-8')

TSV_FILE_NO_MATCH = u'''file_name\tcluster(3)
a773fa2c902e52ed2e0cf3fb3f4394df\tA
4fe8dec76ed3d303e0dcc68e38c96f6f\tB
6ed513f3a5e97687b04cd10c1ed619a7\tB
3847bb31fbec071306b5c2ce502458c4\tC
0b04a1ffef60af4e5802c1038f902eb0\tC
0f87a2acadf34fee74c5de9c1f33ebb2\tC'''.encode('utf-8')

TSV_FILE_COUNT_DONT_MATCH = u'''file_name\tcluster(4)
a773fa2c902e52ed2e0cf3fb3f4394df\tA
4fe8dec76ed3d303e0dcc68e38c96f6f\tB
6ed513f3a5e97687b04cd10c1ed619a7\tB
3847bb31fbec071306b5c2ce502458c4\tC
0b04a1ffef60af4e5802c1038f902eb0\tC
0f87a2acadf34fee74c5de9c1f33ebb2\tC'''.encode('utf-8')

TSV_FILE_EMPTY = u''.encode('utf-8')

class TestAnnotateTsv(unittest.TestCase):
    def setUp(self):
        self.annotate_tsv = AnnotateTsv.load_annotate_tsv_file(BytesIO(TSV_FILE))

    def tearDown(self):
        self.annotate_tsv = None

    def test_list_headers(self):
        headers = self.annotate_tsv.list_headers()
        self.assertEqual(set(headers), set(['file_name', 'cluster(3)', 'one', 'two', 'three', 'six']))

    def test_make_filter(self):
        names = ['A', 'C']
        header_name = 'cluster(3)'
        clusters = ['A', 'B', 'B', 'C', 'C', 'C']
        headers = [header_name]
        matrix = MagicMock()
        matrix.__len__ = MagicMock(return_value=len(clusters))
        matrix.__getitem__ = MagicMock(side_effect=clusters)

        sut = AnnotateTsv(headers, matrix)
        tsv_filter = sut.make_filter(header_name, lambda x: x in names)

        self.assertEqual(set(tsv_filter), set([0, 3, 4, 5]))

    def test_list_items(self):
        items = self.annotate_tsv.list_items('six', [0, 3, 4, 5])
        self.assertEqual(items, [3, 1, 4, 6])

    def test_annotation_to_tsv(self):
        tsv_file = BytesIO()

        metadata_mock = Mock()
        metadata_mock.unique_identifier = 'file_name'
        annotation_mock = Mock()
        annotation_mock.description = 'description'
        annotation_mock.get_nb_clusters = MagicMock(return_value=ACTUAL_NB_CLUSTERS)
        annotation_mock.get_metadata = MagicMock(return_value=metadata_mock)
        annotation_mock.annotation_datagrid_iter = MagicMock(return_value=TSV_FILE_ANNOTATION_DATAGRID_ITER)

        AnnotateTsv.annotation_to_tsv(annotation_mock, CATEGORIES_NAMES, tsv_file)

        self.assertEqual(tsv_file.getvalue(), TSV_FILE)

    @unittest.skip("If slice tool became usefull, code this test!")
    def test_load_annotate_tsv_file(self):
        self.fail("Not implemented yet!")

        '''Valid but should throw a warning'''
        self.assertIsNotNone(AnnotateTsv.load_annotate_tsv_file(BytesIO(TSV_FILE_NO_MATCH)))

        '''Should throw a custom exception'''
        with self.assertRaises(Exception):
            AnnotateTsv.load_annotate_tsv_file(BytesIO(TSV_FILE_COUNT_DONT_MATCH))

        '''Should throw a custom exception'''
        with self.assertRaises(Exception):
            AnnotateTsv.load_annotate_tsv_file(BytesIO(TSV_FILE_EMPTY))
