from bytegain.data_import.segment_utils import parse_s3_url
from bytegain.beam.beam_util import download_from_gs
import tempfile
import pickle


def read_tableinfo_from_gs(filename):
    temp = tempfile.NamedTemporaryFile()
    download_from_gs(filename, temp.name)
    return pickle.load(temp)


# Get table schema from .pickle file. One pickle file per folder is assumed
def get_schema(filespec, subdirs):
    tables_info = {}
    if filespec.startswith('gs://'):
        # Read from cloud
        from google.cloud import storage
        client = storage.Client()
        bucket_name, key, _ = parse_s3_url(filespec)
        bucket = client.get_bucket(bucket_name)
        for k, v in list(subdirs.items()):
            path = key + v
            blobs = bucket.list_blobs(prefix=path)
            for blob in blobs:
                # There should be only one pickle file per directory
                if blob.name.endswith('.pickle'):
                    pickle_string = blob.download_as_string()
                    table_info = pickle.loads(pickle_string)
                    tables_info[k] = table_info
                    break
    else:
        # Read locally
        import os
        for k, v in list(subdirs.items()):
            for file in os.listdir(filespec+v):
                if file.endswith(".pickle"):
                    tables_info[k] = pickle.load(open(filespec + v + file))
                    break
    return tables_info
