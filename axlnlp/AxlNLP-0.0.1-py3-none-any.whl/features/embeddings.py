#basics
from tqdm import tqdm
import os

#torch
import torch
import numpy as np

#flair
import flair
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings, BertEmbeddings
from flair.data import Sentence

#axlnlp
from axlnlp import get_logger
import axlnlp.utils as u
from axlnlp.features.base import FeatureModel


logger = get_logger(__name__)

class Embeddings(FeatureModel):
    
    def __init__(self, dataset, emb_list:list, agg=None, gpu:int=None):

        if isinstance(gpu, int):
            flair.device = torch.device(f'cuda:{gpu}') 

        self._dataset = dataset
        self._name = "WordEmbModel"
        self.agg = agg
        self.emb_list = emb_list
        self._use_contex_embs = True if set(self.emb_list).intersection(set(["flair","bert","elmo"])) else False
        self.embedder = self.__get_embedder()
        self._feature_dim = self.embedder.embedding_length


    @property
    def dataset(self):
        return self._dataset


    def __get_embedder(self):

        embeddings = []
        for emb_name in self.emb_list:

            emb_name = emb_name.lower() 

            if emb_name in ["glove"]:
                embedding = WordEmbeddings("glove")

            elif emb_name == "bert":
                embedding = BertEmbeddings(	
                                            bert_model_or_path="bert-base-cased", 
                                            layers="-1,-2,-3,-4", 
                                            pooling_operation="first"
                                            )

            elif emb_name == "flair":
                flair_forward_embedding = FlairEmbeddings('mix-forward')
                flair_backward_embedding = FlairEmbeddings('mix-backward')
                embedding = StackedEmbeddings(embeddings=[flair_forward_embedding, flair_backward_embedding])
            else:
                raise KeyError(f'"{emb_name}" is not supported')

            embeddings.append(embedding)

        if len(embeddings) > 1:
            return StackedEmbeddings(embeddings=embeddings)
        else:
            return embeddings[-1]


    def __get_word_embs(self, output, item_list, pad, use_tqdm=True):
        
        if use_tqdm:
            item_list = tqdm(item_list, total=output.shape[0])

        for item_id, tok_item in item_list:
        #for i, tok_item in item_list:
                    
            item_string = " ".join(tok_item)
            flair_obj = Sentence(item_string)
            self.embedder.embed(flair_obj)

            nr_tokens = len(tok_item)
            tok_embs  = torch.stack([t.embedding for t in flair_obj])

            if pad:
                output[item_id][:nr_tokens] = tok_embs
            else:
                output.append(tok_embs)


    def __get_nested_word_embs(self, output, set_tok_sentences, pad, flat=True):
        
        for sample_id, tok_sentences in tqdm(set_tok_sentences, total=output.shape[0]):
        #for i,tok_sentences in tqdm(enumerate(set_tok_sentences), total=output.shape[0]):

            doc_emb = []
            self.__get_word_embs(tok_sentences, doc_emb, False, use_tqdm=False)
            nr_embs = len(doc_emb)
        
            if pad:
                output[sample_id][:nr_embs] = torch.stack(doc_emb)
            else:
                output.append(doc_emb)


    def __get_word_embeddings(self, sample_ids:list=None, pad:bool=True):

        """
        prediction level = feature level

        if prediction level == token  DONE
        if prediction level == sentence  we need some for of aggregation?
        if prediction level == document we need some from for aggregation, different axis than sentences
        if prediction level == span we need to 

        """

        sample_level  = self.dataset.sample_level

        if pad:
            if sample_ids:
                size = len(sample_ids)
            else:
                size = max(self.dataset.level_dfs[sample_level]["id"].to_numpy()) + 1 #.shape[0]
            
            shape = (size, self.dataset.max_words[sample_level], self.feature_dim)
            output = torch.zeros(shape)
        else:
            output = []
        
        # If we use context embeddings we need to extract embeddings per sentence
        middle_level = None
        if self._use_contex_embs:
            middle_level = "sentence"
        
        return_ids = True
        if sample_ids:
            return_ids = False

        tok_items = self.dataset.get_tokens(
                                            top_level=sample_level, 
                                            middle_level=middle_level,
                                            sample_ids=sample_ids, 
                                            return_ids=return_ids
                                            )
        
        # if we use sample ids, we dont want to pad rows and columns so we will reset the ids to == len(samples)
        if sample_ids:
            tok_items = list(enumerate(tok_items))

        if self._use_contex_embs and sample_level != "sentence":
            self.__get_nested_word_embs(output, tok_items, pad)
        else:
            self.__get_word_embs(output, tok_items, pad)

        if pad:
            return output.cpu().detach().numpy()
        else:
            return output


    def agg_embs(self,output):

        p_lvl = self.dataset.prediction_level
        s_lvl = self.dataset.sample_level
        p_lvl_id = f"{self.dataset.prediction_level}_id"
        s_lvl_id = f"{self.dataset.sample_level}_id"
        s_t_id = f"{s_lvl[0]}_token_id"

        if p_lvl == s_lvl or p_lvl == "token":
            return output        

        sample_groups = self.dataset.level_dfs["token"].groupby(s_lvl_id)

        #getting the ranges of each span for each sample group
        pred_item_ranges = {}
        for i,group in sample_groups:
            pred_groups = group.groupby(p_lvl_id)
            starts = pred_groups.first()[s_t_id].to_numpy()
            ends = pred_groups.last()[s_t_id].to_numpy()
            pred_item_ranges[i] = np.array([np.arange(*r) for r in zip(starts,ends)])


        if self.agg:
            new_output_matrix = np.zeros((
                                        output.shape[0], 
                                        self.dataset.max_sample_length,
                                        self.feature_dim
                                    ))
        else:
            new_output_matrix = np.zeros((
                                            output.shape[0], 
                                            self.dataset.max_sample_length,
                                            self.dataset.max_words[p_lvl],
                                            self.feature_dim
                                        ))

        for i in range(output.shape[0]):

            if i not in pred_item_ranges:
                continue

            idx_ranges = pred_item_ranges[i]
            
            # TODO: unable to solve how to slice and array into multiple indexes so
            # this loop will suffice for now
            # tried:
            # a[[range1,range2,range3 ...]]
            # a.take()
            # a.take_alonge_axis()
            for idx_id, idx_range in enumerate(idx_ranges):
                slice_ = output[i][idx_range] 

                if self.agg:

                    if self.agg == "mean":
                        agg_slice = np.mean(slice_, axis=0)
                    elif self.agg == "min":
                        agg_slice = np.min(slice_, axis=0)
                    elif self.agg == "max":
                        agg_slice = np.max(slice_, axis=0)
                    else:
                        raise NotImplementedError()
                    
                    new_output_matrix[i][idx_id] = agg_slice

                else:
                    slice_len = slice_.shape[0]
                    new_output_matrix[i][idx_id][:slice_len] = slice_
            
        return new_output_matrix
    

    def extract(self,sample_ids:list=None, pad:bool=True):

        # first we get word embeddings
        word_embs = self.__get_word_embeddings(sample_ids=sample_ids, pad=pad)
        output = self.agg_embs(word_embs)

        return output

