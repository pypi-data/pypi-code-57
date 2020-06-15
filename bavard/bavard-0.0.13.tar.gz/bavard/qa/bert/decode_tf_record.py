from typing import Dict

import tensorflow as tf


def decode_tf_record(record, input_len: int, is_training: bool) -> Dict[str, any]:
    read_features = {
        "input_word_ids": tf.io.FixedLenFeature([input_len], tf.int64),
        "input_mask": tf.io.FixedLenFeature([input_len], tf.int64),
        "input_type_ids": tf.io.FixedLenFeature([input_len], tf.int64),
    }

    if is_training:
        read_features["ans_start"] = tf.io.FixedLenFeature([], tf.int64)
        read_features["ans_end"] = tf.io.FixedLenFeature([], tf.int64)
        read_features["is_impossible"] = tf.io.FixedLenFeature([], tf.int64)

    example = tf.io.parse_single_example(record, read_features)

    # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
    # So cast all int64 to int32.
    for name in example.keys():
        t = example[name]
        if t.dtype == tf.int64:
            t = tf.cast(t, tf.int32)
        example[name] = t

    ans_start = example["ans_start"]
    ans_end = example["ans_end"]
    example["ans_start"] = tf.one_hot(ans_start, input_len)
    example["ans_end"] = tf.one_hot(ans_end, input_len)

    return example
