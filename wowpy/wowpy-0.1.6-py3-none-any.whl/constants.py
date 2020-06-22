import os
import json
import logging
from logging import Logger
from pkg_resources import resource_string

# Load config
wowza_config = resource_string(__name__, 'config.json')
wowza_settings = json.loads(wowza_config)['properties']

# Settings
WSC_API_VERSION = wowza_settings['WSC_API_VERSION']
WSC_API_PATH = wowza_settings['WSC_API_PATH']
WSC_API_ENDPOINT = WSC_API_PATH + WSC_API_VERSION + '/'
WSC_TARGET_NAME = wowza_settings['WSC_TARGET_NAME']

# Logger setup
loglevel = wowza_settings['LOG_LEVEL']
logger = Logger('')
logger.setLevel(loglevel)
ch = logging.StreamHandler()
ch.setLevel(loglevel)
logger.addHandler(ch)