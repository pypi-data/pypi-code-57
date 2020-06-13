
# basic
import numpy as np
from abc import ABC, abstractmethod
import os

# axl nlp
import axlnlp.utils as u
from axlnlp import get_logger

logger = get_logger(__name__)



class FeatureModel(ABC):
    

    @property
    def name(self):
        return self._name


    @property
    def trainable(self):
        return False


    @property
    def dataset(self):
        return self._dataset


    @property
    def feature_dim(self):
        return self._feature_dim

    
    @abstractmethod
    def extract(self):
        pass



class TrainableFeatureModel(FeatureModel):

    @property
    def trainable(self):
        return True

    @property
    def params(self):
        return self._params

    @property
    def trained(self):
        return self._trained

    def _init_model(self):
        return self._get_model_class()(**self.params)


    def _get_model_class(self):
        raise NotImplementedError()


    def _train_model(self, model):
        raise NotImplementedError


    def fit(self):
        logger.info(f"Training {self.name} ..")
        self.split_models = {}
        for i, split_set in self.dataset.splits.items():
            model = self._init_model()
            train_ids = split_set["train"]
            self.split_models[i] = self._train_model(model, train_ids)
        
        self._trained = True
