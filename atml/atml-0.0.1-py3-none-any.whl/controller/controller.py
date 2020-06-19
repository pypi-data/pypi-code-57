import json
import pickle
import requests
import os
import yaml

import logzero
from logzero import logger

from .auto_feature_socket import AutoFeatureSocket
from .auto_learning_socket import AutoLearningSocket
from .auto_deploy_socket import AutoDeploySocket

logzero.logfile(os.path.join(os.path.dirname(__file__), "..", "..", "atml.log"))

class AtmlController(yaml.YAMLObject):
    def __init__(self, with_default=True):
        self.auto_feature_socket = AutoFeatureSocket(with_default)
        self.auto_learning_socket = AutoLearningSocket(with_default)
        self.auto_deploy_socket = AutoDeploySocket(with_default)
    
    def build(self, X, y):
        logger.info('**Start running Auto Feature Socket**')
        self.auto_feature_socket.fit(X)
        X_transform = self.auto_feature_socket.transform(X)
        logger.info('**End of Auto Feature Socket**')
        
        logger.info('**Start running Auto Learning Socket**')
        self.auto_learning_socket.tune(X_transform, y)
        logger.info('**End of Auto Learning Socket**')

        logger.info('**Start running Auto Deploying Socket**')
        self.endpoints = list(self.auto_deploy_socket.deploy(self.auto_feature_socket.pipe, self.auto_learning_socket.best_model)) 
        logger.info('**End of Auto Deploying Socket with Endpoint: {0}**'.format(self.endpoints))

    def predict(self, X):
        X_transform = self.auto_feature_socket.transform(X)
        return self.auto_learning_socket.predict(X_transform)

    def predict_with_endpoint(self, X):
        api_ep = self.endpoints[0] +'/atml/api/v1/predict'
        logger.info('Endpoint: {0}'.format(api_ep))

        data = pickle.dumps(X, protocol=2)
        r = requests.post(api_ep, data=data)
        return json.loads(r.content)

    def score(self, X, y):
        X_transform = self.auto_feature_socket.transform(X)
        return self.auto_learning_socket.score(X_transform, y)
        
    def score_with_endpoint(self, X, y):
        api_ep = self.endpoints[0] +'/atml/api/v1/score'
        logger.info('Endpoint: {0}'.format(api_ep))
                
        X = pickle.dumps(X, protocol=2)
        y = pickle.dumps(y, protocol=2)
        data = pickle.dumps({'X': X, 'y': y}, protocol=2)

        r = requests.post(api_ep, data=data)
        return json.loads(r.content)

    def register_numeric_feature_plug(self, plug):
        self.auto_feature_socket.numeric_socket.register(plug)

    def unregister_numeric_feature_plug(self, plug):
        self.auto_feature_socket.numeric_socket.unregister(plug)

    def register_categorical_feature_plug(self, plug):
        self.auto_feature_socket.categorical_socket.register(plug)

    def unregister_categorical_feature_plug(self, plug):
        self.auto_feature_socket.categorical_socket.register(plug)

    def register_learning_plug(self, plug, space):
        self.auto_learning_socket.register(plug, space)

    def unregister_learning_plug(self, plug):
        self.auto_learning_socket.unregister(plug)

    def choose_learning_plug(self, plugs):
        self.auto_learning_socket.choose(plugs)

    def configure_learning_plug(self, plug, changes):
        self.auto_learning_socket.config(plug, changes)

    def register_deployment_plug(self, plug):
        self.auto_deploy_socket.register(plug)

    def unregister_deployment_plug(self, plug):
        self.auto_deploy_socket.unregister(plug)