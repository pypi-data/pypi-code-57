"""
Typical usage:

python clickstream_to_proto.py --config model_configs/al_1.0 --output /data3/al_data/clickstream-al_1.0

Testing:

python clickstream_to_proto.py --config model_configs/al_1.0  --output protos --shards 1 --workers 1 --row_limit 100

"""

import argparse
import os

from bytegain.custom.model_data.read_from_db import Selector, write_protos
from bytegain.custom.model_data.model_config import ModelConfig, ModelConfigRowHandler

parser = argparse.ArgumentParser(description='Write clickstream protos.')
parser.add_argument('--config', type=str, required=True, help='Path to model config')
parser.add_argument('--output', type=str, required=True, help='Output filebase')
parser.add_argument('--shards', type=int, default=1024, help='Output shard count')
parser.add_argument('--workers', type=int, default=8, help='Worker count')
parser.add_argument('--row_limit', type=int, default=None, help='Maximum number of rows to process per worker')
args = parser.parse_args()

config = ModelConfig.from_json_file(args.config)
row_handler = ModelConfigRowHandler(config)

for worker in range(args.workers):
    if args.workers == 1 or os.fork() == 0:
        # Apportion the shards sequentially among the workers.
        # This is going to be most efficient when args.workers divides evenly into shard_count.
        stride = args.shards / args.workers
        shard_range = [worker * stride, (worker + 1) * stride]

        where = "(%s) and strtol(right(md5(%s), 15), 16) %% %d >= %d and strtol(right(md5(%s), 15), 16) %% %d < %d" % (
                config.where, config.id_field, args.shards, shard_range[0], config.id_field, args.shards, shard_range[1])
        # TODO(chris): Upgrade to fully-qualified table name
        # TODO(chris): Stop peeking into row_handler
        selector = Selector(config.table, where, row_handler._label_extractor._field_name, config.id_field)
        write_protos(selector, row_handler, args.output, shard_range, args.shards, row_limit=args.row_limit)
        exit()

for worker in range(args.workers):
    os.wait()
