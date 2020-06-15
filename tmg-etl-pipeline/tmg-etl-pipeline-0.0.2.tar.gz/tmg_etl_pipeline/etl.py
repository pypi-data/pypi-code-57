import abc
import os

from tmg_etl_pipeline import conf
from tmg_etl_pipeline import logs
from tmg_etl_pipeline import secret_manager


class TMGETLPipeline(metaclass=abc.ABCMeta):

    def __init__(self, app_name, config_path):

        self.app_name = app_name

        self.config = conf.Client(config_path).config
        service_account = self.config.get('service_account', None)
        if service_account:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account

        self.logger = logs.Client(app_name).logger
        self.secrets = secret_manager.Client(self.config['project'], app_name).secrets

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):

        try:
            self.run(*args, **kwargs)
        finally:
            self.cleanup()

