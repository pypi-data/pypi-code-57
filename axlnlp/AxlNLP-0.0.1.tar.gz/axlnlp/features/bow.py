
#basic
import numpy as np
import os

#alxnlp
from axlnlp.features.base import TrainableFeatureModel
import axlnlp.utils as u

#sklearn
from sklearn.feature_extraction.text import CountVectorizer

class BOW(TrainableFeatureModel):

    def __init__(self,dataset, bow_type:str="word_count", dump_path:str="/tmp/bow_feature_model.pkl", **kwargs):
        self._name = "BOW"
        self._dataset = dataset
        self._trained = False
        self.bow_type = bow_type
        self.dump_path = dump_path

        # sampels are expected to be tokenized, so we will just join by spaces and then make the
        # model split by spaces
        tokenizer = lambda x: x.split(" ")
        self._params = kwargs
        self._params["tokenizer"] = tokenizer


        if os.path.exists(self.dump_path):
            self.load()


    def save(self):
        u.pickle_data([self.split_models, self._feature_dim], self.dump_path)


    def load(self):
        self.split_models, self._feature_dim = u.load_pickle_data(self.dump_path) 
        self._trained = True


    def _get_model_class(self):
        if self.bow_type=="word_count":
            return CountVectorizer
        else:
            raise KeyError(f'"{self.bow_type}" is not a supported BOW-type')

        
    def _train_model(self, model, train_ids):
        sample_level  = self.dataset.sample_level
        pred_level  = self.dataset.prediction_level
        top_level = sample_level if pred_level == "token" else pred_level
        samples = self.dataset.get_tokens(
                                            top_level=top_level, 
                                            sample_ids=train_ids, 
                                            join=True
                                            )
        model.fit(samples)
        self._feature_dim = len(model.get_feature_names())
        self.save()
        return model


    def extract(self, sample_ids:list=None, split_id:int=0):

        sample_level  = self.dataset.sample_level
        pred_level  = self.dataset.prediction_level

        middle_level = None if sample_level == pred_level or pred_level=="token" else pred_level

        samples = self.dataset.get_tokens(
                                top_level=sample_level,
                                middle_level=middle_level,
                                sample_ids=sample_ids,
                                join=True
                                )
        
        # NOTE! default model is the model of the firs split: 0
        model = self.split_models[split_id]

        if sample_ids is not None:
            size = len(sample_ids)
            assert len(samples) == size
        else:
            size = max(self.dataset.level_dfs[sample_level]["id"].to_numpy()) + 1

        if not middle_level:
            matrix = model.transform(samples).toarray()
        else:
            matrix = np.zeros((size, self.dataset.max_sample_length, self.feature_dim))
            for i,s in enumerate(samples):
                m = model.transform(s).toarray()
                m_len = m.shape[0]

                #assert matrix[i][:m.shape[0]].shape == m.shape
                matrix[i][:m_len] = model.transform(s).toarray()

        return matrix        