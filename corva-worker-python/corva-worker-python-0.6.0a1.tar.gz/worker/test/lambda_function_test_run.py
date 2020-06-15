"""
This file is used to trigger lambda functions locally and test
the results of the app on actual data to make sure of the results.
An example to use this functionality is like the one shows on
'app_test.py' and then that file can run in command line.

Note: make sure you run your tests on QA environment.

== app_test.py file
# added the main directory as the first path
from os.path import dirname
import sys
parent = dirname(dirname(__file__))
sys.path.insert(0, parent)

if __name__ == '__main__':
    collections = ['collection_to_delete']
    app = AppTestRun(lambda_function.lambda_handler, collections)
    app.run()

> python app_test -a 16886 -d True
"""

import argparse
from distutils.util import strtobool
from tqdm import tqdm

from worker import constants
from worker.data.operations import delete_collection_data_of_asset_id, get_one_wits_record, gather_wits_for_period
from worker.framework.mixins import RedisMixin
from worker.test.utils import get_last_processed_timestamp, create_scheduler_events


def generate_parser():
    """
    Creating the supporting arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Run your tests locally on an asset.")
    parser.add_argument("-a", "--asset_id", "--id", type=int, required=True, help="set asset_id")
    parser.add_argument("-s", "--start_timestamp", "--start", type=int, required=False, default=None, help="start timestamp")
    parser.add_argument("-e", "--end_timestamp", "--end", type=int, required=False, default=None, help="end timestamp")
    parser.add_argument("-i", "--timestep", "--step", type=int, required=False, default=60, help="trigger the lambda function once every step")
    parser.add_argument("-t", "--event_type", "--event", type=str, required=False, default="scheduler", help="type of event, scheduler or wits_stream")
    parser.add_argument("-d", "--to_delete", "--delete", type=strtobool, required=False, default=False, help="to delete the state and data")
    return parser


class AppTestRun:
    def __init__(self, lambda_handler, collections, args=None):
        self.lambda_handler = lambda_handler
        self.collections = collections

        self.event_type = None
        self.progress = None

        if args is None:
            parser = generate_parser()
            args = parser.parse_args()

        self.initialize(args)

    def initialize(self, args):
        asset_id = args.asset_id
        start_timestamp = args.start_timestamp
        end_timestamp = args.end_timestamp
        step = args.timestep
        self.event_type = args.event_type
        to_delete = args.to_delete

        app_redis = "corva/{0}.{1}".format(asset_id, constants.get("global.app-key"))

        if not start_timestamp:
            start_timestamp = get_one_wits_record(asset_id, timestamp_sort=+1).get('timestamp')
        if not end_timestamp:
            end_timestamp = get_one_wits_record(asset_id, timestamp_sort=-1).get('timestamp')
        if to_delete:
            RedisMixin.delete_states(pattern=f"{app_redis}*")
            delete_collection_data_of_asset_id(asset_id, self.collections)
            print("Deleted relevant states and collections for this asset!")

        start_timestamp = get_last_processed_timestamp(app_redis) or start_timestamp
        print(f"asset_id: {asset_id}, timestamp interval: [{start_timestamp}, {end_timestamp}]")

        events = create_scheduler_events(asset_id, start_timestamp, end_timestamp, step)

        self.progress = tqdm(events, ncols=150)

    def run(self):
        for e in self.progress:
            schedule_time = str(int(e[0][0]['schedule_start'] / 1000))
            if self.event_type == "wits_stream":
                wits = gather_wits_for_period(
                    int(e[0][0]['asset_id']),
                    int(e[0][0]['schedule_start'] / 1000),
                    int(e[0][0]['schedule_end'] / 1000)
                )
                if not wits:
                    continue
                e = [wits]
            self.lambda_handler(e, None)
            self.progress.set_description(schedule_time)
