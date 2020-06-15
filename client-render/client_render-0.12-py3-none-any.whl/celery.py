import logging
import time

from celery import Celery

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)


@celery.task(name="run")
def run(*files):
    print(files)
    logger.info(files)
    time.sleep(int(100))
