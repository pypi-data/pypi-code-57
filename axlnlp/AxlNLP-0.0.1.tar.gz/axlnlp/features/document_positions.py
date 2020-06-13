
from axlnlp.features.base import FeatureModel
import pandas as pd
import numpy as np


class DocPos(FeatureModel):

    """
    Creates a vector representing a sentences position in the text.

    inital_texts are needed to create this feature


    feature is specifically implemented for replication of Joint Pointer NN from :
    https://arxiv.org/pdf/1612.08994.pdf

    "(3) Structural features:  Whether or not the AC is the first AC in a paragraph, 
    and Whether the AC  is  in  an  opening,  body,  or  closing  paragraph."
    """

    def __init__(self, dataset):
        self._dataset = dataset
        self._name = "DocPos"
        self._feature_dim = 2



    @property
    def dataset(self):
        return self._dataset


    # @property
    # def trainable(self):
    #     return False


    def __doc_pos(self, row, doc2paralen, step_level):

        vec = [0]*2
        doc_id = row["document_id"]
        row_id = row["id"]

        if row[f"p_{step_level}_id"] == 0:
            vec[0]= 1
        
        if row[f"d_paragraph_id"]== 0:
            pass
        elif row[f"d_paragraph_id"] == doc2paralen[doc_id]-1:
            vec[1] = 2
        else:
            vec[1] = 1
        
        return {"vec":np.array(vec),"document_id":doc_id, f"{step_level}_id":row_id}


    def extract(self, sample_ids:list=None, pad=True):

        """
        # 1) is the first AC in a paragaraph
        # 2) is is in first, body, or last paragraph
        
        FUNC()
        # We can get 1 by checking the local id of each ac and its paragraph_id, if both
        # we just need to know hte nr of paragaraphs in each document,
        # then we can make conditions
        #               ac_para_id == 0 == FIRST
        #               ac_para_id == nr_para == LAST
        #               else: BODY

        # feature representation
        
        alt 1:

        one hot encodig where dimN == {0,1}, dim size = 4
        dim0 = 1 if item is first in sample 0 if not
        dim1 = 1 if item is in first paragraph if not
        dim2 = 1 if item is in body 0 if not
        dim3 = 1 if item is in last paragraph 0 if not


        alt 2:
        one hot encodig where dim0 == {0,1}
        dim0 = 1 if item is first in sample 0 if not

        and dim1 = {0,1,2}
        dim1 = 0 if item in first paragrap, 1 if in body, 2 if in last paragraph

        """

        step_level = self.dataset.prediction_level
        sample_level = self.dataset.sample_level
        

        if sample_level != "document":
            raise ValueError("Sample level needs to be 'document' for this feature")


        # we will look at the position of the prediction level items
        df = self.dataset.level_dfs[step_level]

        # filtering if we are given sample ids else we take everything on sample level
        if sample_ids:
            sample_level_id = f"{sample_level}_id"
            df = df[df[sample_level_id].isin(sample_ids)]
            nr_ids = len(sample_ids)
        
            nr_ids = len(sample_ids)
            if nr_ids > 1:
                pad = True
        else:
            nr_ids = max(self.dataset.level_dfs[sample_level]["id"].to_numpy()) + 1


        if pad:
            max_sample_len = self.dataset.max_sample_length
            output = np.zeros((nr_ids, max_sample_len, 2))

        #create a dict of document 2 number of paragraphs
        para_groups = self.dataset.level_dfs["paragraph"].groupby("document_id", sort=False)
        doc2paralen = {i:g.shape[0] for i,g in para_groups}


        args = [doc2paralen, step_level]
        vec_rows = list(df.apply(self.__doc_pos, axis=1, args=args).to_numpy())
        new_df = pd.DataFrame(vec_rows)

        f = lambda x: x["vec"]
        test = new_df.groupby("document_id")["vec"] #.apply(f)

        for i, (doc_i,g) in enumerate(test):
            output[i][:g.shape[0]] = np.stack(g.to_numpy())

        return output