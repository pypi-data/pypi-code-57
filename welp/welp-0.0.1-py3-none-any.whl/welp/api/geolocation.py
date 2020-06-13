from __future__ import print_function

import argparse
import json
import pprint
import uuid
import sys
import urllib
import os
import requests

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_KEY= os.environ['GOOGLE_API_KEY'] 

# API constants, you shouldn't have to change these.
API_HOST = 'https://www.googleapis.com'
SEARCH_PATH = '/geolocation/v1/geolocate'

def geolocate():
    url_params = {
        'key': API_KEY,
    }

    body = {
        'macAddress': ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]),
    }

    url_params = url_params or {}
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))

    response = requests.request('POST', url, params=url_params, data=body)

    return response.json()
