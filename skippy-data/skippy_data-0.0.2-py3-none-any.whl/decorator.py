import logging

from kubernetes import config, watch, client
from kubernetes.client import V1Pod
from minio import Minio
from minio.error import ResponseError

from data.minio import download_file, upload_file


def consume(urn):
    def wrapper(func):
        logging.info('Consume.wrapper(%s)' % func)

        def call(*args, **kwargs):
            logging.info('Consume.call(%s,%s,%s)' % (func, args, kwargs))
            content = download_file(urn)
            logging.info('Content Data(%s)' % content)
            kwargs['data'] = content
            return func(*args, **kwargs)

        logging.debug('Consume.wrapper over')
        return call

    return wrapper


def produce(urn):
    def wrapper(func):
        logging.info('Produce.wrapper(%s)' % func)

        def call(*args, **kwargs):
            logging.info('Produce.call(%s,%s,%s)' % (func, args, kwargs))
            response = func(*args, **kwargs)
            upload_file(urn,response)
            logging.info('Produce.store(%s)' % response)
            return response

        logging.debug('Produce.wrapper over')
        return call

    return wrapper
