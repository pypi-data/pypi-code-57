import os

from boto3.session import Session
from configurations import Configuration, values
import requests

class EC2Configuration(Configuration):
    AWS_CLOUDWATCH_ENABLED = values.BooleanValue(True)
    AWS_ACCESS_KEY_ID = values.Value(environ_required=True)
    AWS_SECRET_ACCESS_KEY = values.Value(environ_required=True)
    AWS_REGION_NAME = values.Value(environ_required=True)
    AWS_LOG_GROUP = values.Value(environ_required=True)
    AWS_STREAM_NAME = values.Value(environ_required=True)


    @classmethod
    def setup(cls):
        super(EC2Configuration, cls).setup()
        url = 'http://169.254.169.254/latest/meta-data/local-ipv4'
        EC2_PRIVATE_IP = requests.get(url,timeout=1).text
        cls.ALLOWED_HOSTS+=[EC2_PRIVATE_IP]
        if not cls.AWS_CLOUDWATCH_ENABLED:
            return
        boto3_session = Session(
            aws_access_key_id=cls.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cls.AWS_SECRET_ACCESS_KEY,
            region_name=cls.AWS_REGION_NAME
        )
        if not hasattr(cls,'LOGGING') or not cls.LOGGING:
            cls.LOGGING = {}
        cls.LOGGING['version'] = cls.LOGGING.get('version',1)
        cls.LOGGING['disable_existing_loggers'] = cls.LOGGING.get('disable_existing_loggers',False)
        cls.LOGGING['formatters'] = cls.LOGGING.get('formatters',{})
        cls.LOGGING['handlers'] = cls.LOGGING.get('handlers',{})
        cls.LOGGING['loggers'] = cls.LOGGING.get('loggers',{})
        cls.LOGGING['formatters']['aws'] = {
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
        cls.LOGGING['handlers']['watchtower'] = {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_session': boto3_session,
            'log_group': cls.AWS_LOG_GROUP,
            'stream_name': cls.AWS_STREAM_NAME,
            'formatter': 'aws',
        }
        cls.LOGGING['loggers']['django'] = {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        }
