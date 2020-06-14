import os
import json
import logging
from logging import Logger
from pkg_resources import resource_string
from pathlib import Path

# Load config
wowza_config = resource_string(__name__, 'config.json')
wowza_settings = json.loads(wowza_config)['properties']

# Settings
WSC_API_VERSION = wowza_settings['WSC_API_VERSION']
WSC_API_PATH = wowza_settings['WSC_API_PATH']
WSC_API_ENDPOINT = WSC_API_PATH + WSC_API_VERSION + '/'
WSC_TARGET_NAME = wowza_settings['WSC_TARGET_NAME']

# Secrets envars
# WSC_ACCESS_KEY = os.environ.get('WSC_ACCESS_KEY')
# WSC_API_KEY = os.environ.get('WSC_API_KEY')

# Secrets file
home_path = str(Path.home())
credentials_path = home_path + '/.wowza/credentials.json'
if os.path.exists(credentials_path):
  with open(credentials_path) as json_file:
    credentials_data = json.load(json_file)
    WSC_ACCESS_KEY = credentials_data['WSC_ACCESS_KEY']
    WSC_API_KEY = credentials_data['WSC_API_KEY']
    
# Query headers
WSC_HEADERS = {
  'headers': {
    'Content-Type': 'application/json',
    'cache-control': 'no-cache',
    'wsc-access-key': WSC_ACCESS_KEY,
    'wsc-api-key': WSC_API_KEY
  }
}

# Logger setup
loglevel = wowza_settings['LOG_LEVEL']
logger = Logger('')
logger.setLevel(loglevel)
ch = logging.StreamHandler()
ch.setLevel(loglevel)
logger.addHandler(ch)