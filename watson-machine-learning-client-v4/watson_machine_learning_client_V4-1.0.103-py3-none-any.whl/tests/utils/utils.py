import json
import os
from configparser import ConfigParser

__all__ = [
    "get_wml_credentials",
    "get_cos_credentials",
    "get_env",
    "is_cp4d",
    "bucket_exists",
    "bucket_name_gen"
]

if "ENV" in os.environ:
    environment = os.environ['ENV']
else:
    environment = "YP_QA"


timeouts = "TIMEOUTS"
credentials = "CREDENTIALS"
training_data = "TRAINING_DATA"
configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


def get_env():
    return environment


def get_wml_credentials(env=environment):
    return json.loads(config.get(env, 'wml_credentials'))


def get_cos_credentials(env=environment):
    return json.loads(config.get(env, 'cos_credentials'))


def is_cp4d():
    if "CP4D" in get_env():
        return True
    elif "ICP" in get_env():
        return True
    elif "OPEN_SHIFT" in get_env():
        return True
    elif "CPD" in get_env():
        return True

    return False

def bucket_exists(cos_resource, bucket_name):
    """
    Return True if bucket with `bucket_name` exists. Else False.
    """
    buckets = cos_resource.buckets.all()
    for bucket in buckets:
        if bucket.name == bucket_name:
            return True
    print("Bucket {0} not found".format(bucket_name))
    return False


def bucket_name_gen(prefix='bucket-tests', id_size=8):
    import random
    import string

    return prefix + "-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(id_size))




