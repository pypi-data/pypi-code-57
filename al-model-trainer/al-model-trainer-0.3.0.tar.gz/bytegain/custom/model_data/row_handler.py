import bytegain.custom.model_data.row_handler_proto.row_handler_pb2 as row_handler_pb2
import bytegain.custom.model_data.bucket as bucket_module
import bytegain.custom.model_data.extractor as extractor_module
import numpy

"""
RowHandler converts an input row with raw data into an array of floats suitable for sending to a model.
RowHandlers consistent primarily of "buckets" which convert the input data into floats.
The "label_function" converts the input row into the "label" that the model is trying to guess.
The "id_function" converts the input row into an id suitable for tracking the row in future steps.

Buckets in RowHandlers are serialized as protos.  The buckets can be saved & written to disk, but the id & label functions
must be specified in th constructor (if desired).  ID & label functions aren't needed for serving.
"""

def set_fast_mode(fast_mode = True):
    bucket_module.FAST_MODE = fast_mode
    extractor_module.FAST_MODE = fast_mode

class RowHandler(object):
    def __init__(self, preprocess = None, label_bucket = None, id_extractor = None, weight_extractor = None,
                 control_extractor = None,
                 load_from=None, extra_fields=[]):
        self._preprocess = preprocess
        self._label_bucket = label_bucket
        self._id_extractor = id_extractor
        self._weight_extractor = weight_extractor
        self._control_extractor = control_extractor
        self._buckets = []
        self._width = None
        self._extra_fields = extra_fields
        if load_from is not None:
            self._load_from_file(load_from)

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

    def extra_fields(self):
        return self._extra_fields

    def get_categorical_indicies(self):
        categorical = []
        index = 0
        for bucket in self._buckets:
            if isinstance(bucket, bucket_module.CategoricalBucket):
                print("Categorical bucket name %s"%(bucket._name))
                categorical.append(index)
            else:
                print("Not categorical bucket name %s" % bucket._name)
            index += bucket._total_buckets
        return categorical


    def replace_field_names_with_index(self, cursor):
        # Instead of using a DictCursor, use a regular cursor,
        # and rewrite the extractor field names with array
        # offsets.  This speeds up data loading by about 20%.
        header = [x[0].lower() for x in cursor.description]
        for bucket in self._buckets:
            extractor = bucket._extractor
            extractor.update_fields_by_id(header)

        self._id_extractor.update_fields_by_id(header)
        if self._weight_extractor:
            self._weight_extractor.update_fields_by_id(header)
        if self._control_extractor:
            self._control_extractor.update_fields_by_id(header)

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

    def get_weight_from_row(self, row):
        if self._weight_extractor:
            return self._weight_extractor.extract(row)
        return 1.0

    def get_label_from_row(self, row):
        if self._label_bucket == None:
            raise Exception("No Label function given")
        return self._label_bucket.bucketize(row)


    def is_control_from_row(self, row):
        if self._control_extractor == None:
            return False
        return self._control_extractor.extract(row)

    def get_data_from_row(self, row):
        val = []
        if self._preprocess:
            row = self._preprocess(row)
        for bucket in self._buckets:
            val.extend(bucket.bucketize(row))

        # Convert to compact Numpy array
        return numpy.array(val, dtype = numpy.float32)

    def get_feature_spec(self):
        features = []
        for bucket in self._buckets:
            extractor = bucket._extractor

            feature_dict = {'name' : extractor._field_name, 'datatype' : extractor.data_type_string(), 'null_fraction' : int(extractor._null_fraction * 100) / 100.0 }

            # output = "%-24s %s is_null=%3d%%" % (extractor._field_name + ":", extractor.data_type_string(), extractor._null_fraction * 100)
            if not isinstance(bucket, bucket_module.CategoricalBucket) and hasattr(extractor, "_has_mu") and extractor._has_mu:
                feature_dict["mean"] = extractor._mu
                feature_dict["std"] = extractor._sigma

            if isinstance(bucket, bucket_module.CategoricalBucket):
                values = [{"value" : bucket._category_dict[x], "key" : x} for x in bucket._category_dict]
                values.sort(key=lambda val: val['value'])
                values = [{"key" : "None"}, {"key" : "Other"}] + values
                for fraction, value in zip(bucket._distro, values):
                    value["fraction"] = int(fraction * 100) / 100.0
                feature_dict["categorical_values"] = values

            features.append(feature_dict)
        return {"features" : features}

    def print_summary(self):
        for bucket in self._buckets:
            print("%20s: %s" % (bucket._name, bucket.get_distro()))

    def value_header(self):
        header = ""
        for bucket in self._buckets:
            header += bucket.get_short_label()
        return header

    def get_fields(self):
        fields = []
        if self._control_extractor:
            fields.extend(self._control_extractor.get_fields())
        print("Fields: %s" % fields)
        for bucket in self._buckets:
            fields.extend(bucket._extractor.get_fields())
        return fields
