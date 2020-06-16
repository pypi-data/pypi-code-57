import unittest
import bytegain.custom.model_data.read_from_db as read_from_db
from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.model_data.buffered_dataset import BufferedDataset, BatchIterator
from bytegain.custom.model_data.bucket import ValueBucket
from bytegain.custom.model_data.extractor import LogNormedExtractor

def get_leased_array(row):
    leased = row["leased_at_notified_property"]
    if leased:
        return [0.0, 1.0]
    else:
        return [1.0, 0.0]

def get_interest_id_from_row(row):
    return row["interest_id"]

row_handler = RowHandler(label_function = get_leased_array, id_function = get_interest_id_from_row)
row_handler.add_bucket(ValueBucket("commute_distance", LogNormedExtractor("commute_distance", 2.15481928615808, 1.01514149898681, 0, 200)))

WHERE =  """
interest_created_at > timestamp '2016-06-30' and
interest_created_at < timestamp '2016-07-01'
"""

def create_queue(test_mod, is_test):
    selector = read_from_db.Selector("bytegain_leads", WHERE, "leased_at_notified_property", "interest_id")
    mod_selector = read_from_db.ModSelector(10, test_mod)
    return read_from_db.create_enqueue_operator(None, "apartmentlist", selector, row_handler, mod_selector, is_test = is_test)

class TestBatchIterator(unittest.TestCase):
    def test_batch_reader(self):
        batch_size = 7
        data = list(range(0, 1000))
        batch = BatchIterator(data.__iter__(), batch_size)
        iters = 1000 / batch_size
        for i in range (0, iters):
            expected = list(range(i * batch_size, (i +1) * batch_size))
            actual = next(batch)
            self.assertEqual(actual, expected)

        remainder = next(batch)
        expected = list(range(iters * batch_size, 1000))
        self.assertEqual(remainder, expected)

        try:
            next(batch)
            self.fail("This shouldn't happen")
        except StopIteration:
            pass

    def test_batch_reader_with_limit(self):
        batch_size = 7
        limit = 100
        data = list(range(0, 1000))
        batch = BatchIterator(data.__iter__(), batch_size, limit = limit)
        iters = limit / batch_size
        for i in range (0, iters):
            expected = list(range(i * batch_size, (i +1) * batch_size))
            actual = next(batch)
            self.assertEqual(actual, expected)

        remainder = next(batch)
        expected = list(range(limit / batch_size * batch_size, limit))
        self.assertEqual(remainder, expected)

        try:
            next(batch)
            self.fail("This shouldn't happen")
        except StopIteration:
            pass

class TestIterableDataset(unittest.TestCase):
    def test_iterable_test_mode(self):
        ids = set()
        id_array = []
        enqueued = create_queue(3, True)

        for data,label,id in enqueued:
            self.assertFalse(id in ids)
            ids.add(id)
            id_array.append(id)

        # Now re-read, ensure consistency
        enqueued = create_queue(3, True)
        for prev_id in id_array:
            data,label,id = next(enqueued)
            self.assertEqual(prev_id, id)

        # Now read different mod- no overlap
        enqueued = create_queue(4, True)

        for data,label,id in enqueued:
            self.assertFalse(id in ids)
            ids.add(id)

    def test_iterable_train_mode(self):
        ids = set()
        id_array = []
        enqueued = create_queue(3, False)
        for data,label,id in enqueued:
            if id in ids:
                print("End epoch after %d" % (len(ids)))
                break
            else:
                ids.add(id)
                id_array.append(id)

        # Go through again (skip first since already done above)
        for prev_id in id_array[1:]:
            data,label,id = next(enqueued)
            self.assertEqual(prev_id, id)

        # Once more, just for good measure
        for prev_id in id_array:
            data,label,id = next(enqueued)
            self.assertEqual(prev_id, id)

    def test_buffered_iterable_test_mode(self):
        ids = set()
        id_array = []
        buffered = BufferedDataset(100, create_queue(3, True))

        for data,label,id in buffered:
            self.assertFalse(id in ids)
            ids.add(id)
            id_array.append(id)

        # Now re-read, ensure consistency
        enqueued = create_queue(3, True)
        for prev_id in id_array:
            data,label,id = next(enqueued)
            self.assertEqual(prev_id, id)

        # Now read different mod- no overlap
        enqueued = BufferedDataset(100, create_queue(4, True))
        for data,label,id in enqueued:
            self.assertFalse(id in ids)
            ids.add(id)
