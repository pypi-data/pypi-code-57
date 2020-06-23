from __future__ import absolute_import, unicode_literals

import os
import sentry_sdk
import logging

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corgy_erp.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")
# try:
#     from dotenv import load_dotenv, find_dotenv
#     from pathlib import Path
#     dotenv_path = find_dotenv(raise_error_if_not_found=True)
#     dotenv_result = load_dotenv(dotenv_path=dotenv_path)
#     print('dotenv[celery] configuration %s from "%s"' % ('loaded' if dotenv_result else 'not loaded', dotenv_path))
# except BaseException as e:
#     logging.error('dotenv[celery] configuration could not loaded')
#     logging.exception(e)
#
# finally:
#     os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('KRYNEGGER_CONFIGURATION').capitalize())

import configurations
configurations.setup()

from celery import Celery
app = Celery('corgy_erp')
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
