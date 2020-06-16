import argparse
import os
import sys
import json
import time
from datetime import datetime
from bytegain.iox import gcp_init

# Use cred file and private key to set google credentials
gcp_cred_file = os.environ.get("GCP_CRED_FILE")
gcp_private_key = os.environ.get("GCP_PRIVATE_KEY")
if gcp_cred_file and gcp_private_key:
    gcp_init.set_credentials_file(gcp_cred_file, gcp_private_key)

import googleapiclient.discovery

from bytegain.data_import.segment_utils import parse_s3_url
import configparser

PROJECT_ID = 'tough-hologram-156002'


def create_transfer_client():
    return googleapiclient.discovery.build('storagetransfer', 'v1')


parser = argparse.ArgumentParser()
parser.add_argument('--s3_url', required=True)
parser.add_argument('--gs_url', required=True)
args = parser.parse_args()

s3_bucket, s3_key, _ = parse_s3_url(args.s3_url)
gs_bucket, gs_key, _ = parse_s3_url(args.gs_url)

if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
    aws_access_key = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
else:
    try:
        config = configparser.ConfigParser()
        config.read([str(os.path.expanduser('~') + "/.aws/credentials")])
        aws_access_key = config.get('default', 'aws_access_key_id')
        aws_secret_key = config.get('default', 'aws_secret_access_key')
    except:
        aws_access_key = None
        aws_secret_key = None

if aws_access_key is None or aws_secret_key is None:
    print("Error: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set either in the environment or in ~/.aws/credentials")
    sys.exit(1)
else:
    print("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set")

now = datetime.now()
# Edit this template with desired parameters.
# Specify times below using US Pacific Time Zone.
transfer_job = {
    'description': "Transfer from %s to %s" % (args.s3_url, args.gs_url),
    'status': 'ENABLED',
    'projectId': PROJECT_ID,
    'schedule': {
        'scheduleStartDate': {
            'day': now.day,
            'month': now.month,
            'year': now.year
        },
        'scheduleEndDate': {
            'day': now.day,
            'month': now.month,
            'year': now.year
        },
    },
    'transferSpec': {
        'transferOptions': {
            'overwriteObjectsAlreadyExistingInSink': True
        },
        'objectConditions': {
            'includePrefixes': [s3_key]
        },
        'awsS3DataSource': {
            'bucketName': s3_bucket,
            'awsAccessKey': {
                'accessKeyId': aws_access_key,
                'secretAccessKey': aws_secret_key
            }
        },
        'gcsDataSink': {
            'bucketName': gs_bucket
        }
    }
}

client = create_transfer_client()
result = client.transferJobs().create(body=transfer_job).execute()
# print('Returned transferJob: {}'.format(
#     json.dumps(result, indent=4)))
job_name = result["name"]
op_filter = {
    'project_id': PROJECT_ID,
    'job_names': [job_name]
}
start_time = time.time()
# Wait for operation to be created
time.sleep(30)

print("Waiting for %s" % job_name)
while True:
    ops = client.transferOperations().list(name='transferOperations', filter=json.dumps(op_filter)).execute()
    if "operations" in ops:
        ops = ops["operations"]
        if len(ops) != 1:
            print("Bad ops returned: %s" % ops)
            break
        else:
            op = ops[0]
            # print json.dumps(op, indent=4)
            if "done" in op and op["done"]:
                total_time = time.time() - start_time
                data = int(op["metadata"]["counters"]["bytesCopiedToSink"])
                print(("Files Copied %5.3fG in %ds (%4.1fM/s)" % (
                    data / (1024.0 * 1024 * 1024), total_time, data / (1024 * 1024.0) / total_time)))
                break
            elif op["metadata"]["status"] == "IN_PROGRESS":
                total_time = time.time() - start_time
                if "bytesCopiedToSink" in op["metadata"]["counters"]:
                    data = int(op["metadata"]["counters"]["bytesCopiedToSink"])
                    sys.stdout.write("Data: %5.3fG in %ds (%4.1fM/s)    \r" % (
                        data / (1024.0 * 1024 * 1024), total_time, data / (1024 * 1024.0) / total_time))
                    sys.stdout.flush()

    time.sleep(10)
