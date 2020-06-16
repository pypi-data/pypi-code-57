"""
Reads filenames, one per line, from a file.
Calls s3api head_object on each one to determine whether it is being restored.
"""

import argparse
import boto3
import queue
import threading

class WorkerThread(threading.Thread):
    def __init__(self, task_queue):
        super(WorkerThread, self).__init__()
        self._task_queue = task_queue
        # Create a client for the S3 API.  Optional profile_name identifies
        # which profile to use from the ~/.aws/config file.
        session = boto3.Session(profile_name='al-s3')
        self._s3_client = session.client('s3')

    def run(self):
        """Pulls items off the task queue, calling _process for each one.
        Exits once a False item is pulled."""
        ended = False
        while not ended:
            fname = self._task_queue.get()
            if not fname:
                ended = True
                print('worker exiting')
            else:
                try:
                    self._process(fname)
                except Exception as e:
                    print('unexpected exception: ' + str(e))
            self._task_queue.task_done()

    def _process(self, fname):
        # See http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.head_object
        response = self._s3_client.head_object(Bucket='al-events', Key=fname)
        if 'Restore' not in response:
            print('%s lacks Restore' % fname)
        else:
            if response['Restore'] == 'ongoing-request="true"':
                print('%s ongoing Restore' % fname)
            else:
                print('%s completed Restore' % fname)
        # print('ho %s' % str(ho))

parser = argparse.ArgumentParser()
parser.add_argument('--fnames', type=str, required=True, help='filename containing filenames, one per line')
parser.add_argument('--num_threads', type=int, default=1, help='Number of threads')
known_args, _ = parser.parse_known_args()
task_queue = queue.Queue(1000)

# Start workers.
for _ in range(known_args.num_threads):
    thread = WorkerThread(task_queue)
    thread.daemon = True
    thread.start()

# Fill task_queue with file names to process.
with open(known_args.fnames, 'r') as fnames:
    for fname in fnames:
        fname = fname.strip()  # get rid of trailing newline
        task_queue.put(fname)

# Tell workers to exit.
for _ in range(known_args.num_threads):
    task_queue.put(False)
task_queue.join()
