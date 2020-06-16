import pyximport
pyximport.install()

import unittest
from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.custom.model_data.bucket import Bucket, ValueBucket, StringBucket, CategoricalBucket
from bytegain.custom.model_data.extractor import RowExtractor, NonNullExtractor, AutoNormedExtractor

entries = [
        {"field1" : -65, "field2" : None, "field3" : "c", "is_null" : "asda", "null_clamp" : -40, "str_cat": "cat1"},
        {"field1" : None, "field2" : -150, "field3" : "d", "is_null" : "asda", "null_clamp" : 400, "str_cat": "cat1"},
        {"field1" : 30, "field2" : 27, "field3" : "a", "is_null" : "", "null_clamp" : 0, "str_cat": "cat8"},
        {"field1" : 300, "field2" : 3000, "field3" : None, "is_null" : None, "null_clamp" : None, "str_cat": None},
]

field1_bucket = Bucket("test1", RowExtractor("field1", -27, 247), [-60, -23, 100.2, 200, 250])
field2_bucket = ValueBucket("test2", AutoNormedExtractor("field2",  -100, None, 10, 5), has_null = False)
field3_bucket = StringBucket("test3", RowExtractor("field3"), ["a", "b", "c"], has_none = False)
field4_bucket = ValueBucket("test4", NonNullExtractor("is_null"))
field5_bucket = ValueBucket("test5", AutoNormedExtractor("null_clamp", min_val = -11, max_val=121, mu = 0, sigma = 20))
field6_bucket = CategoricalBucket("test6", RowExtractor("str_cat", 0), 0, {"cat1" : 0, "cat2" : 1, "cat3" : 2})

class TestRowHandler(unittest.TestCase):
    def test_save_one_bucket(self):
        row_handler = RowHandler()
        row_handler.add_bucket(field5_bucket)
        filename = '/tmp/test_row_handler'
        row_handler.save(filename)

        loaded_handler = RowHandler(load_from=filename)
        self.compare_handlers(row_handler, loaded_handler)
        self.assertEqual(1, len(loaded_handler._buckets))


    def test_save_all_bucket(self):
        print("min max %s %s" % (str(field5_bucket._extractor._min_val), str(field5_bucket._extractor._max_val)))
        row_handler = RowHandler()
        row_handler.add_bucket(field1_bucket)
        row_handler.add_bucket(field2_bucket)
        row_handler.add_bucket(field3_bucket)
        row_handler.add_bucket(field4_bucket)
        row_handler.add_bucket(field5_bucket)
        row_handler.add_bucket(field6_bucket)
        for entry in entries:
            row_handler.get_data_from_row(entry)

        filename = '/tmp/test_row_handler'
        row_handler.save(filename)

        loaded_handler = RowHandler(load_from=filename)
        print("load: min max %s %s" % (str(loaded_handler._buckets[4]._extractor._min_val), str(loaded_handler._buckets[4]._extractor._max_val)))
        print("Loaded handler spec:")
        print(loaded_handler.print_spec());

        self.compare_handlers(row_handler, loaded_handler)

    def compare_handlers(self, expected, actual):
        for entry in entries:
            expected_data = expected.get_data_from_row(entry)
            actual_data = actual.get_data_from_row(entry)
            # actual_data[2] =923.2
            print("actual_data: " + str(actual_data))
            self.assertEqual(actual_data, expected_data)
