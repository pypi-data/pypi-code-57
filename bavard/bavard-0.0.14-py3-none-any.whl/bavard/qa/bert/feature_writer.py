import collections

import tensorflow as tf

from bavard.qa.bert.input_features import InputFeatures


class FeatureWriter(object):
    """Writes InputFeature to TF example file."""

    def __init__(self, filename, is_training):
        self.filename = filename
        self.is_training = is_training
        self.num_features = 0
        self._writer = tf.io.TFRecordWriter(filename)

    def process_feature(self, feature: InputFeatures):
        """Write a InputFeature to the TFRecordWriter as a tf.train.Example."""
        self.num_features += 1

        def create_int_feature(values):
            feature = tf.train.Feature(
                int64_list=tf.train.Int64List(value=list(values)))
            return feature

        features = collections.OrderedDict()
        features["input_word_ids"] = create_int_feature(feature.input_ids)
        features["input_mask"] = create_int_feature(feature.input_mask)
        features["input_type_ids"] = create_int_feature(feature.segment_ids)

        if self.is_training:
            features["ans_start"] = create_int_feature([feature.ans_start_idx])
            features["ans_end"] = create_int_feature([feature.ans_end_idx])
            impossible = 0
            if feature.is_impossible:
                impossible = 1
            features["is_impossible"] = create_int_feature([impossible])

        tf_example = tf.train.Example(features=tf.train.Features(feature=features))
        self._writer.write(tf_example.SerializeToString())

    def close(self):
        self._writer.close()
