
# basic
import numpy as np
from abc import ABC, abstractmethod
import os

# axl nlp
import axlnlp.utils as u
from axlnlp import get_logger

logger = get_logger(__name__)


class FeatureSet:

    def __init__(self, dataset, features:list, dump_path:str="/tmp/TEST_FEATURE.pkl"):
        self.dataset = dataset
        self.dump_path = dump_path

        self.__fm_params = features # if isinstance(features, dict) else dict(features)

        self.__init_fms()

        if self.train:
            self.__fit()

        if os.path.exists(dump_path):
            self.load()
        else:
            self.__process_dataset()

        self.active = False
    

    def save(self):
        logger.info(f"Dumping matrix and init params to {self.dump_path}")
        u.pickle_data([self.feature_matrixes, self.__fm_params, self.feature_dim], self.dump_path)


    def load(self):
        logger.info(f"Loading matrix and init params from {self.dump_path}")
        self.feature_matrixes, self.__fm_params, self.feature_dim = u.load_pickle_data(self.dump_path)


    def __init_fms(self):
        self.feature_models = []
        
        are_trained = []
        for fm, *params in self.__fm_params:
            
            logger.info(f"Init {fm} ...")
            if not params:
                m = fm(self.dataset)
            elif isinstance(params[0], dict):
                m = fm(self.dataset,**params[0])
            elif isinstance(params, list):
                m = fm(self.dataset,*params[0])
            else:
                raise RuntimeError("Feature Model init failed ...")

            if m.trainable:
                are_trained.append(m.trained)

            self.feature_models.append(m)
        
        self.train = False in are_trained
        self.feature_names = [m.name for m in self.feature_models]


    def __fit(self):
        for fm in self.feature_models:
            if fm.trainable:
                fm.fit()


    def __process_dataset(self):

        feature_matrixes = {}
        feature_dim = 0
        for fm in self.feature_models:
            feature_dim += fm.feature_dim

            if fm.trainable:

                split_matrixes = {}
                for i, split_set in self.dataset.splits.items():
                    
                    size = max(self.dataset.level_dfs[self.dataset.sample_level]["id"].to_numpy()) + 1
                    matrix = np.zeros((size, self.dataset.max_sample_length, fm.feature_dim))

                    for split_type, split_ids in split_set.items():
                        feature_matrix = fm.extract(
                                                    sample_ids=split_ids,
                                                    split_id=i
                                                    )
                        
                        matrix[split_ids] = feature_matrix
                
                    split_matrixes[i] = matrix
                feature_matrixes[fm.name]  = split_matrixes

            else:
                feature_matrixes[fm.name] = fm.extract()


        self.feature_dim = feature_dim

        self.feature_matrixes = feature_matrixes
        self.save()
        self.deactivate()


    def deactivate(self):
        self.feature_models = []


    def activate(self):
        self.__init_fms()
        
        for fm in self.feature_models:
            if fm.trainable:
                fm.load()

        self.active = True

    
    @u.timer
    def get(self,split_id, sample_ids=None):
        matrixes = []
        for feature in self.feature_names:

            feature_matrix = self.feature_matrixes[feature]

            if isinstance(feature_matrix, dict):
                feature_matrix = feature_matrix[split_id]
            
            #print(feature, feature_matrix.shape)
            matrixes.append(feature_matrix)

        matrix = np.concatenate(matrixes, axis=2)

        #print("CONCAT", matrix.shape)
        #if sample_ids is not None:
            #matrix = matrix[self.sample_id2position[sample_ids]]

        return matrix


    def extract(self):

        if not self.active:
            raise RuntimeError("Feature Models are not active. Call .activate() on FeatureSet to load feature models.")


        # check if id is in dataset?
        # if not run add sample
        # then get it?


        raise NotImplementedError()