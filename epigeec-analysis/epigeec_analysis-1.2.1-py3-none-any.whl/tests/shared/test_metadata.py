import unittest
from io import StringIO

from tests.context import analysis
from analysis.shared.metadata import Metadata, MetadataFormatError

METADATA_JSON_BAD_TYPE = u'{"potato": ["non-sense"]}'

METADATA_NON_JSON = u'I am just a text.'

METADATA_JSON_TYPE_LIST = u'''
{"count": 2,
"name": "test1",
"datasets": [
{"cell_type": "hindlimb bud", "assay": "H3K27ac", "file_name": "MS046901", "assay_category": "Histone Modifications", "md5sum": "f0fd84b5c0c7b0c56e165c8e0963e8c2", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "8"},
{"cell_type": "forelimb bud", "assay": "H3K27ac", "file_name": "MS046801", "assay_category": "Histone Modifications", "md5sum": "5600791b332ab4a88fade77ba50be26a", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "9"}
]}'''

METADATA_JSON_TYPE_DICT =  u'''
{"count": 2,
"name": "test1",
"datasets": {
"MS046901": {"cell_type": "hindlimb bud", "assay": "H3K27ac", "file_name": "MS046901", "assay_category": "Histone Modifications", "md5sum": "f0fd84b5c0c7b0c56e165c8e0963e8c2", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "8"},
"MS046801": {"cell_type": "forelimb bud", "assay": "H3K27ac", "file_name": "MS046801", "assay_category": "Histone Modifications", "md5sum": "5600791b332ab4a88fade77ba50be26a", "virtual": false, "publishing_group": "CEEHRC", "cell_type_category": "forelimb/hindlimb", "releasing_group": "McGill", "assembly": "mm10", "id": "9"}
}}'''

METADATA_JSON_A =  u'''
{"count": 1,
"name": "test2_A",
"datasets": [
{"file_name": "MS046901"}
]}'''

METADATA_JSON_B =  u'''
{"count": 1,
"name": "test2_B",
"datasets": [
{"file_name": "MS046801"}
]}'''

METADATA_JSON_C = u'''
{"count": 2,
"name": "test2_A;test2_B",
"datasets": [
{"file_name": "MS046901"}, {"file_name": "MS046801"}
]}'''

METADATA_JSON_TYPE_ERROR = u'''
{"count": 2,
["typeerror"]: "typeerror"
"name": "test2_A;test2_B",
"datasets": [
{"file_name": "MS046901"}, {"file_name": "MS046801"}
]}
'''

LIST_CATEGORIES_MD5SUM = ['f0fd84b5c0c7b0c56e165c8e0963e8c2', '5600791b332ab4a88fade77ba50be26a']

LIST_CATEGORIES_HEADERS_BAD = ['badddd132141aebaaddd3214j36jk253']

LIST_CATEGORIES_RESULT_ALL = ['cell_type', 'assay', 'file_name', 'assay_category', 'md5sum', 'virtual', 'publishing_group', 'cell_type_category', 'releasing_group', 'assembly', 'id']

class TestMetadata(unittest.TestCase):

    def test_load_from_different_types(self):
        json_file_list = StringIO(METADATA_JSON_TYPE_LIST)
        metadata_from_list = Metadata.load_from_file(json_file_list, 'file_name')

        json_file_dict = StringIO(METADATA_JSON_TYPE_DICT)
        metadata_from_dict = Metadata.load_from_file(json_file_dict, 'file_name')

        self.assertEqual(metadata_from_list, metadata_from_dict)

    def test_load_from_bad_json_file(self):
        json_bad_type = StringIO(METADATA_JSON_BAD_TYPE)
        with self.assertRaises(MetadataFormatError):
            Metadata.load_from_file(json_bad_type, 'file_name')

        json_type_error = StringIO(METADATA_JSON_TYPE_ERROR)
        with self.assertRaises(MetadataFormatError):
            Metadata.load_from_file(json_type_error, 'file_name')

    def test_load_from_non_json_file(self):
        non_json = StringIO(METADATA_NON_JSON)
        with self.assertRaises(MetadataFormatError):
            Metadata.load_from_file(non_json, 'file_name')

    def test_add(self):
        md_a = Metadata.load_from_file(StringIO(METADATA_JSON_A), 'file_name')
        md_b = Metadata.load_from_file(StringIO(METADATA_JSON_B), 'file_name')
        md_c = Metadata.load_from_file(StringIO(METADATA_JSON_C), 'file_name')

        self.assertNotEqual(md_a, md_c)
        self.assertNotEqual(md_b, md_c)
        self.assertNotEqual(md_a, md_b)

        self.assertEqual(md_a + md_b, md_c)

    def test_list_categories(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_DICT), 'file_name')

        list1 = data.list_categories(LIST_CATEGORIES_MD5SUM)
        self.assertEqual(len(set(list1).intersection(LIST_CATEGORIES_RESULT_ALL)), len(list1))

        list1 = data.list_categories(LIST_CATEGORIES_HEADERS_BAD)
        self.assertEqual(len(set(list1).intersection([])), 0)

    def test_find(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')
        patterns = ['MS046901', 'potato']

        m1 = data.find(patterns, False)
        m2 = data.find(patterns, True)

        self.assertNotEqual(m1, m2)

        self.assertEqual(len(m1), 1)
        self.assertNotEqual(len(m1), len(data))

        self.assertEqual(len(m2), 1)
        self.assertNotEqual(len(m2), len(data))

    def test_match(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')
        p1 = ['MS[0-9]+']
        p2 = ['^8$', 'potato']
        p3 = ['hind', 'fore']

        a1 = data.match(p1, False)
        a2 = data.match(p1, True)
        b1 = data.match(p2, False)
        b2 = data.match(p2, True)
        c1 = data.match(p3, False)
        c2 = data.match(p3, True)

        self.assertNotEqual(a1, a2)
        self.assertNotEqual(b1, b2)
        self.assertNotEqual(c1, c2)

        self.assertEqual(len(a1), 2)
        self.assertEqual(len(a2), 0)
        self.assertEqual(len(b1), 1)
        self.assertEqual(len(b2), 1)
        self.assertEqual(len(c1), 2)
        self.assertEqual(len(c2), 0)

    def test_extract(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')

        a_file_names = []
        b_file_names = ['MS046901']
        c_file_names = ['MS046901', 'MS046801']
        d_file_names = ['potato']
        e_file_names = ['potato', 'MS046801']

        a_md = data.extract(a_file_names)
        b_md = data.extract(b_file_names)
        c_md = data.extract(c_file_names)
        d_md = data.extract(d_file_names)
        e_md = data.extract(e_file_names)

        self.assertNotEqual(a_md, data)
        self.assertNotEqual(b_md, data)
        self.assertEqual(c_md, data)
        self.assertNotEqual(d_md, data)
        self.assertNotEqual(e_md, data)

        self.assertEqual(len(a_md), 0)
        self.assertEqual(len(b_md), 1)
        self.assertEqual(len(c_md), 2)
        self.assertEqual(len(d_md), 0)
        self.assertEqual(len(e_md), 1)

    @unittest.skip("demonstrating skipping")
    def test_make_usable_categories(self):
        self.fail("Not implemented yet!")

    def test_obtain_formated_dataset(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')
        file_name = 'MS046901'

        # good md5
        good_md5 = data.obtain_formated_dataset(file_name, ['assay'])
        self.assertEqual(len(good_md5), 1)

        # bad md5
        bad_md5 = data.obtain_formated_dataset('potato', ['assay'])
        self.assertEqual(len(bad_md5), 1)
        self.assertEqual(bad_md5, ['User'])

        # good categories
        good_categories = data.obtain_formated_dataset(file_name, ['assay', 'cell_type'])
        self.assertEqual(len(good_categories), 2)
        self.assertEqual(good_categories, ['H3K27ac', 'hindlimb bud'])

        # bad categories
        bad_categories = data.obtain_formated_dataset(file_name, ['potato'])
        self.assertEqual(len(bad_categories), 1)
        self.assertEqual(bad_categories, ['NA'])

        # empty categories
        empty_categories = data.obtain_formated_dataset(file_name, [])
        self.assertEqual(len(empty_categories), 0)

    def test_obtain_dataset_item(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')
        file_name = 'MS046901'

        # good md5
        good_md5 = data.obtain_dataset_item(file_name, 'assay')
        self.assertEqual(good_md5, 'H3K27ac')

        # bad md5
        bad_md5 = data.obtain_dataset_item('potato', 'assay')
        self.assertEqual(bad_md5, 'User')

        # good categories
        good_categories = data.obtain_dataset_item(file_name, 'cell_type')
        self.assertEqual(good_categories, 'hindlimb bud')

        # bad categories
        bad_categories = data.obtain_dataset_item(file_name, 'potato')
        self.assertEqual(bad_categories, 'NA')

    def test_extract_tag_names_file_names(self):
        data = Metadata.load_from_file(StringIO(METADATA_JSON_TYPE_LIST), 'file_name')
        file_names = ['MS046901', 'MS046801']
        cell_type = 'cell_type'
        assay = 'assay'

        # good md5s split
        good_md5s_split = data.extract_tag_names_file_names(file_names, cell_type)
        self.assertEqual(len(good_md5s_split), 2)
        for tag_name, md5 in zip(['hindlimb bud', 'forelimb bud'], file_names):
            self.assertEqual(good_md5s_split[tag_name], [md5])

        # good md5s fusion
        good_md5s_fusion = data.extract_tag_names_file_names(file_names, assay)
        self.assertEqual(len(good_md5s_fusion), 1)
        self.assertEqual(good_md5s_fusion['H3K27ac'], file_names)

        # bad md5
        bad_md5 = data.extract_tag_names_file_names(['patate'], assay)
        self.assertEqual(len(bad_md5), 1)
        self.assertEqual(bad_md5['User'], ['patate'])

        # empty md5
        empty_md5 = data.extract_tag_names_file_names([], assay)
        self.assertFalse(empty_md5)

        # bad category name
        bad_category_name = data.extract_tag_names_file_names(file_names, 'potato')
        self.assertEqual(len(bad_category_name), 1)
        self.assertEqual(bad_category_name['NA'], file_names)

if __name__ == '__main__':
    unittest.main()
