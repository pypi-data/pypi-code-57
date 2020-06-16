"""
Typical usage:

python s3_to_proto.py --config model_configs/al_1.0 --input /data3/al_join/split-apartmentlist.web_join2.????_part_??.gz-* --output /data3/al_join/protos --workers 32

"""

import pyximport
pyximport.install()

import argparse
import csv
import gzip
import itertools
import os
import tensorflow as tf
import time

from bytegain.custom.model_data.model_config import ModelConfig, ModelConfigRowHandler
from multiprocessing import Process, Queue

import bytegain.custom.model_data.row_handler as row_handler_module
row_handler_module.set_fast_mode(True)

parser = argparse.ArgumentParser(description='Write clickstream protos.')
parser.add_argument('--config', type=str, required=True, help='Path to model config')
parser.add_argument('--input', type=str, required=True, nargs='+', help='Path to input files')
parser.add_argument('--output', type=str, required=True, help='Output filebase')
parser.add_argument('--workers', type=int, default=8, help='Worker count')
parser.add_argument('--user_limit', type=int, default=None, help='Maximum number of users to process')
args = parser.parse_args()

config = ModelConfig.from_json_file(args.config)
row_handler = ModelConfigRowHandler(config, csv_input=True)

queue = Queue()

def run_worker(worker):
    for path_i, path in iter(queue.get, None):
        output_file = '%s-%s' % (args.output, os.path.basename(path))
        writer = tf.python_io.TFRecordWriter(output_file, options=tf.python_io.TFRecordOptions(compression_type=tf.python_io.TFRecordCompressionType.ZLIB))
        print("Reading from %s..." % (path))

        reader = csv.reader(gzip.open(path))
        header = next(reader)
        row_handler.replace_field_names_with_index_header(header)

        user_count = 0
        start_time = time.time()
        for row_id, row_id_iterator in itertools.groupby(reader, lambda x: row_handler.get_id_from_row(x)):
            row_handler.add_sequence_examples(row_id_iterator, writer)
            user_count += 1
            if args.user_limit and user_count >= args.user_limit:
                break
        print("(%d/%d) Finished %s in %d seconds." % (path_i+1, len(args.input), path, time.time() - start_time))
        writer.close()

processes = [Process(target=run_worker, args=(i,)) for i in range(args.workers)]

print("Starting workers...")
for process in processes:
    process.start()

print("Processing %d files..." % len(args.input))
for path_i, path in enumerate(args.input):
    queue.put((path_i, path,))

# Tell workers to quit.
for i in range(args.workers):
    queue.put(None)

# Wait for them to actually quit.
for process in processes:
    process.join()
