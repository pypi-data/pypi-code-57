import bytegain.custom.model_data.row_handler_proto.row_handler_pb2 as row_handler_pb2
import bytegain.custom.model_data.bucket as bucket_module

"""
MultiRowHandler converts a series of input rows with raw data into a set of examples for training.
Multiple rows of input can result in a single row of output.
"""

class MultiRowHandler(object):
    def __init__(self, label_bucket = None, id_extractor = None):
        self._label_bucket = label_bucket
        self._id_extractor = id_extractor
        self._buckets = []
        self._width = None
        self._last_id = None
        self._current_events = None

        # if load_from is not None:
        #       self._load_from_file(load_from)

    @property
    def buckets(self):
        return self._buckets

    @property
    def width(self):
        if self._width is None:
            self._width = 0
            for bucket in self._buckets:
                self._width += bucket._total_buckets
        return self._width

    def replace_field_names_with_index(self, cursor):
        # Instead of using a DictCursor, use a regular cursor,
        # and rewrite the extractor field names with array
        # offsets.  This speeds up data loading by about 20%.
        header = [x.name for x in cursor.description]
        for bucket in self._buckets:
            extractor = bucket._extractor
            extractor.update_fields_by_id(header)

        self._id_extractor.update_fields_by_id(header)
        self._label_bucket._extractor.update_fields_by_id(header)

    def _load_from_file(self, filename):
        with open(filename, "rb") as f:
            handler = row_handler_pb2.RowHandler()
            handler.ParseFromString(f.read())

        for bucket in handler.bucket:
            self._buckets.append(bucket_module.read_from_proto(bucket))

    def save(self, filename):
        handler = row_handler_pb2.RowHandler()
        for bucket in self._buckets:
            bucket_proto = handler.bucket.add()
            bucket.write_to_proto(bucket_proto)

        with open(filename, "wb") as f:
            f.write(handler.SerializeToString())

    def add_bucket(self, bucket):
        self._buckets.append(bucket)

    def get_id_from_row(self, row):
        if self._id_extractor == None:
            raise Exception("No ID function given")
        return self._id_extractor.extract(row)

    def get_label_from_row(self, row):
        if self._label_bucket == None:
            raise Exception("No Label function given")
        return self._label_bucket.bucketize(row)

    def _make_entry(self):
        return self._make_data_entry(), self.get_label_from_row(self._current_events[0]), self.get_id_from_row(self._current_events[0])

    def process_row(self, row):
        new_val = None
        row_id = self.get_id_from_row(row)
        if row_id != self._last_id:
            if self._last_id:
                new_val = self._make_entry()
            self._last_id = row_id
            self._current_events = []

        self._current_events.append(row)
        return new_val

    def get_fields(self):
        fields = []
        for bucket in self._buckets:
            fields.extend(bucket._extractor.get_fields())
        return fields
