import logging
import os

LOG_LEVEL = logging.DEBUG

if os.getenv('DAGGER_LOG_LEVEL', None) is not None:
    LOG_LEVEL = getattr(logging, os.getenv('DAGGER_LOG_LEVEL'))

DAGGER_URL = 'https://api.getdagger.com/v1/tasks/status'
# DAGGER_URL = 'http://localhost:3001/v1/tasks/status'
