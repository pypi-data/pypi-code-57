import pyximport

pyximport.install()

import sys
import tensorflow as tf
import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.custom.cust.apartmentlist.leads_filter_170 as lf

feature_file = 'bytegain/cust/apartmentlist/features/al_1.7.0.json'


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _byte_feature(value):
    return tf.train.Feature(byte_list=tf.train.BytesList(value=value))

def _float_array_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def create_records(filename_base, dataset):
    writer = None
    compression_type = tf.python_io.TFRecordCompressionType.GZIP
    options=tf.python_io.TFRecordOptions(compression_type=compression_type)

    for i in range(0, len(dataset._data)):
        if i % 10000 == 0:
            sys.stdout.write("writing %d    \r" % i)
            sys.stdout.flush()
            if writer:
                writer.close()
            writer = tf.python_io.TFRecordWriter(filename_base % (i/10000), options = options)

        if len(dataset._data[i]) != rh.width:
            raise Exception("Bad width: %d" % len(dataset._data[i]))
        feature = {'label': _int64_feature(int(dataset._labels[i])),
                   'id': _int64_feature(dataset._ids[i]),
                   'data': _float_array_feature(dataset._data[i])}

        example = tf.train.Example(features=tf.train.Features(feature=feature))

        # Serialize to string and write on the file
        writer.write(example.SerializeToString())
    writer.close()


rh, datasets = al_xgb.create_rh_and_dataset(feature_file, random_seed=2828712, filter = lf.filter2,
                                            downsample_negative=False)
print("Width: %d" % rh.width)
create_records('/data3/al_tensorflow/dataset_all_train_%04d.tfrecord', datasets.train)
create_records('/data3/al_tensorflow/dataset_all_test_%04d.tfrecord', datasets.test)
