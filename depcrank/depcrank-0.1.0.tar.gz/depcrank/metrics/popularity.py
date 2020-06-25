"""
FIXME: insert program metadata
"""

import requests
import time
import os

PKGSTATS_ENDPOINT = "https://pkgstats.archlinux.de/api/packages/{}"
PKGSTATS_ENDPOINT_FAILURE = []
PKGSTATS_DEFAULT_VALUE = 0.001
DEFAULT_LOG_COUNT = 75


def _get_popularity(package):
    response = requests.get(PKGSTATS_ENDPOINT.format(package))
    try:
        value = json.loads(response.content)["popularity"]
    except json.decoder.JSONDecodeError:
        PKGSTATS_ENDPOINT_FAILURE.append(package)
        value = PKGSTATS_DEFAULT_VALUE
    return value


def _dump_stats(popularity, output_path):
    # FIXME: DRY?
    with open(output_path, "w") as fp:
        json.dump(popularity, fp)


def get_popularity(input_data, output_path, fresh=False):
    if fresh and os.path.exists(output_path):
        with open(output_path) as fp:
            popularity = json.load(fp)
    else:
        popularity = {}

    i = 0
    for package in input_data:
        if package in popularity:
            continue

        print('Fetching popularity of {}...'.format(package), end='',
            flush=True)
        popularity[package] = _get_popularity(package)
        i += 1
        if i % DEFAULT_LOG_COUNT == 0:
            _dump_stats(popularity, output_path)
            time.sleep(1)
    
    _dump_stats(popularity, output_path)
    
    if len(PKGSTATS_ENDPOINT_FAILURE) != 0:
        print("The endpoint failed for:")
        print(PKGSTATS_ENDPOINT_FAILURE)