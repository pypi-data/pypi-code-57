import argparse
import sys
import tensorflow as tf

parser = argparse.ArgumentParser(description='Dump tensorflow training records.')
parser.add_argument('path', nargs='+')
args = parser.parse_args()

record = tf.train.SequenceExample()
for path in args.path:
    if path[-3:] == '.gz':
        compression_type = tf.python_io.TFRecordCompressionType.GZIP
    else:
        compression_type = tf.python_io.TFRecordCompressionType.ZLIB
    record_iterator = tf.python_io.tf_record_iterator(path, options=tf.python_io.TFRecordOptions(compression_type=compression_type))
    for raw in record_iterator:
        record.ParseFromString(raw)
        print(record)
