# Stdlib
import logging

# Django
from django.conf import settings

# Pipy: pika
import pika

# Project
from .config import get_config
from .job import JobServer, job_methods

logger = logging.getLogger(__name__)


def register_tasks():
    for apps in settings.INSTALLED_APPS:
        try:
            __import__(apps + '.tasks')
            __import__(apps + '.models')
        except ModuleNotFoundError:
            pass


def start():
    register_tasks()
    connection = pika.BlockingConnection(get_config())
    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)
    job_server = JobServer(channel, job_methods)
    job_server.job_register()
    job_server.start()
