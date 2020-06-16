import boto3
import argparse
import bytegain.data_import.segment_utils as segment_utils
import tempfile
import gzip
import shutil
import os
import datetime
import threading
import json

from multiprocessing import Process, Queue
from collections import defaultdict

class WorkerThread(Process):
    def __init__(self, queue, s3_dest, overwrite):
        super(WorkerThread, self).__init__()
        self._queue = queue
        self._s3_dest = s3_dest
        self._overwrite = overwrite
        self._resource = boto3.resource('s3')
        dest_bucket_name, self._dest_key, _ = segment_utils.parse_s3_url(self._s3_dest)
        self._dest_bucket = self._resource.Bucket(dest_bucket_name)

    def run(self):
        ended = False
        while not ended:
            item = self._queue.get()
            if not item:
                ended = True
            else:
                # print ("Got day: %s" % item[1])
                self.create_day(item[0], item[1], item[2])

    def create_day(self, bucket, day, file_list):
        millis = int(day)
        day_timestamp = datetime.datetime.fromtimestamp(millis / 1000.0)

        dest_file = "%s/%s-joined.gz" % (self._dest_key, day_timestamp.strftime("%Y-%m-%d"))
        if not self._overwrite:
            response = self._dest_bucket.objects.filter(Prefix=dest_file)
            count = 0
            for item in response:
                # print "item: %s" % str(item)
                count += 1
            if count > 0:
                print("Skipping %s" % dest_file)
                return

        my_bucket = self._resource.Bucket(bucket)
        tfiles = []
        for key in file_list:
            tfile = tempfile.NamedTemporaryFile(delete = False)
            tfile.close()
            my_bucket.download_file(key, tfile.name)
            tfiles.append(tfile.name)

        output_file = tempfile.NamedTemporaryFile(delete = False, suffix = ".gz")
        output_file.close()
        with gzip.open(output_file.name, 'wb') as output_gzip:
            for file in tfiles:
                with gzip.open(file, 'rb') as f:
                    shutil.copyfileobj(f, output_gzip)
                    os.remove(file)

        print("Uploading %s to %s" % (output_file.name, dest_file))
        self._dest_bucket.upload_file(output_file.name, dest_file)
        os.remove(output_file.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copies and Joins S3 data files to Bytegain S3 storage')
    parser.add_argument('--s3_input', type=str, help='S3 input directory', required=True)
    parser.add_argument('--s3_output', type=str, help='S3 output directory', required=True)
    parser.add_argument('--s3_profile', type=str, help='s3 profile to use for data access', default = "s3_data_user")
    parser.add_argument('--threads', type=int, help='number of parallel S3 threads', default = 4)
    parser.add_argument('--overwrite', help='If set, then overwrite destination files, otherwise skip existing days', action='store_true')

    args = parser.parse_args()
    boto3.setup_default_session(profile_name=args.s3_profile)
    session = boto3.Session()
    s3 = session.client('s3')

    bucket, key, _ = segment_utils.parse_s3_url(args.s3_input)
    start_key = ""
    day_files = defaultdict(lambda: [])
    files = 0
    while (True):
        response = s3.list_objects_v2(Bucket=bucket, Prefix=key, StartAfter = start_key)
        if "Contents" not in response:
            break

        contents = response["Contents"]
        for file in contents:
            start_key = file["Key"]
            if ".gz" in start_key:
                files += 1
                dirs = start_key.split('/')
                day = dirs[-2]
                day_list = day_files[day]
                day_list.append(start_key)

    print("%d files in %d days" % (files, len(day_files)))

    file_queue = Queue(20)
    processes = []
    for i in range(args.threads):
        thread = WorkerThread(file_queue, args.s3_output, args.overwrite)
        thread.start()
        processes.append(thread)

    for day in sorted(day_files.keys()):
        file_queue.put([bucket, day, day_files[day]])

    for process in processes:
        process.join()
