from logzero import logger

from ..tuner.atml_impl import AtmlOrchestrator
from .base_socket import SocketBase


class AutoLearningSocket(SocketBase):
    def __init__(self, with_default):
        super().__init__(with_default)
        logger.info('with_default: {0}'.format(with_default))
        self.tuner = AtmlOrchestrator(with_default=with_default)

    def register(self, instance, search_space):
        self.tuner.register_model_search(instance, search_space)

    def choose(self, instances):
        self.tuner.choose_models(instances)

    def config(self, instance, change_list):
        for key, value in change_list:
            self.tuner.set_model_search_param(instance, key, value)

    def tune(self, X, y):
        try:
            self.tuner.run(X, y)
        finally:
            self.best_model = self.tuner.get_best_model_details()['MODEL']

    def get_best_model(self):
        return self.best_model

    def predict(self, X):
        return self.best_model.predict(X)

    def score(self, X, y):
        return self.best_model.score(X, y)