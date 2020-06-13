#basic
import numpy as np
from tqdm import tqdm
import os
import pandas as pd

#axlnlp
import axlnlp.utils as u
from axlnlp import get_logger
from axlnlp.dataset.encoders import DatasetEncoder
from axlnlp.dataset.preprocessor import Preprocessor
#from am.modules.split_utils import SplitUtils

#sklearn 
from sklearn.model_selection import KFold

logger = get_logger("DATASET")


import warnings

class DataSet(DatasetEncoder, Preprocessor): #, SplitUtils):


    """"

    TODO: might need to add global ids to each level_df
    when creating the level dfs one could create global ids as well.
    however these would need to be stored for each sub-level as  well

    """

    def __init__(self, data_path:str=""): # dump_path:str="/tmp/dataset.pkl"
        super().__init__()

        if os.path.exists(data_path):
            self.load(data_path)

        self.level2parents = {
                                "token": ["sentence", "paragraph", "document"],
                                "sentence": ["paragraph", "document"],
                                "paragraph": ["document"],
                                "document": []
                                }

        self.parent2children = {
                                "document": ["paragraph","sentence", "token"],
                                "paragraph": ["sentence", "token"],
                                "sentence": ["token"],
                                "token": []
                                }
        self.encoders = {}


        #self.max_words_per_doc
        #self.max_words_per_sent


    def __getitem__(self,key):
        
        if isinstance(key, int):
            return self.exp_df.loc[key, :]
        if isinstance(key, (list,np.ndarray)):
            return self.exp_df.loc[key, :]
        elif isinstance(key, str):
            return self.exp_df[key].to_numpy()
        else:
            raise IndexError()


    def get_tokens(self, top_level, middle_level:str=None, sample_ids=None, join=False, return_ids=False):


        def __get_nested(df, top_level, middle_level, join, sample_ids):

            groups = df.groupby(top_level,sort=False)

            items = []
            ids = []
            for i,group in groups:
                ids.append(i)
                subitems = []
                subgroups = group.groupby(middle_level,sort=False)
                
                for i,subgroup in subgroups:

                    item = subgroup["text"].to_numpy()

                    if join:
                        item = " ".join(item)
                    
                    subitems.append(item)
                
                items.append(subitems)

            return items, ids


        def __get_flat(df, top_level, join):

            groups = df.groupby(top_level,sort=False)
            items = []
            ids = []
            for i,group in groups:
                ids.append(i)
                item = group["text"].to_numpy()
                if join:
                    item = " ".join(item)
                items.append(item)

            return items, ids


        #TODO: This needs to be made faster        
        t_lvl_id = f"{top_level}_id"
        m_lvl_id = f"{middle_level}_id"

        df = self.level_dfs["token"]

        # if sample ids are given we filter out all other rows
        if sample_ids is not None:
            filter_cond = df[t_lvl_id].isin(sample_ids)
            df = df[filter_cond]
        
        # if we lets say want sentences, we might not care about getting sentences per document,
        # but just all sentences in the dataset.
        # if we want e.g. sentence per document, we just put flat=False, and we wont flatten.
        if middle_level:
            items, ids = __get_nested(df, t_lvl_id, m_lvl_id, join, sample_ids)
        else:
            items,ids = __get_flat(df, t_lvl_id, join)

        if return_ids:
            return list(zip(ids,items))
        else:
            return items


    @property
    def name(self):
        return self._name

    @property
    def vocab(self):
        return sorted(set(self.token_df["text"].values))


    def print(self):

        if not hasattr(self, "level_dfs"):
            raise RuntimeError("Dataset contain no data. Use add_sample() or add_samples() to populate dataset")


        for level, df in self.level_dfs.items():
            #df.reset_index(drop=True, inplace=True)
            logger.info(f'DataFrame of level {level}- \n{df.head(8)}')


        if hasattr(self, "exp_df"):
            logger.info(f'DataFrame of EXP DF - \n{self.exp_df.head(8)}')


    def __create_encoders(self):
        

        self.task2padvalue = {}
        self.feature2padvalue = {}

        logger.info("Creating Encoders ...")
        for feat_type in self.feature_types:

            if feat_type in ["words", "chars"]:
                data = self.level_dfs["token"]["text"].to_numpy()
            elif feat_type == "pos":
                data = self.level_dfs["token"]["pos"].to_numpy()
            elif feat_type == "bert":
                data = None
            else:
                raise KeyError(f'"{feat_type}" is not a supported feature')
            
            self.add_encoder(name=feat_type, data=data, max_sample_length=self.max_sample_length, pad_value=0)
            self.feature2padvalue[feat_type] = 0

        for label in self.labels:
            data = self.level_dfs[self.prediction_level][label]
            self.add_encoder(name=label, data=data, max_sample_length=self.max_sample_length, pad_value=777)
            self.task2padvalue[label] = 777



    def __construct_exp_df(self, pad=False):


        if self.prediction_level != "token" and self.feature_types:
            raise ValueError(f"No support for token level feature types for {self.prediction_level} yet")

        top_level_id = f"{self.dataset_level}_id"
        sample_id = f"{self.sample_level}_id"
        #p_id = f"{self.prediction_level}_id"


        if self.prediction_level != self.sample_level:
            pdf =  self.level_dfs[self.prediction_level]

            sample_groups = pdf.groupby(sample_id,sort=False)

            #TODO: MOVE THIS TO MAX OVER LENGTHS instead as we are doing this twice
            self.max_sample_length = max(g.shape[0] for i,g in sample_groups)

            # creating encoders for each of given feature types
            self.__create_encoders()

            new_columns = []
            for i, group in sample_groups:
                row = {}
                row["id"] = i

                # print(group)
                # TODO: not sure if this make sense for labeled spans as joining them
                # creates an incoherent text with missing parts.
                # will this work for duplicate checking?
                #row["text"] = " ".join(group["text"])
                # print(lol)

                row["lengths"] = group.shape[0]

                if sample_id != top_level_id:
                    row[top_level_id] = group[top_level_id].to_numpy()[0]

                for label in self.labels:
                    row[label] = self.encode_list(group[label].to_numpy(), label, pad=pad)


                if self.prediction_level == "token":
                    for f in self.feature_types:
                        #TODO: create a mapping for features to column instead of this:
                        data_type = "text" if f != "pos" else "pos"
                        
                        row[f] = self.encode_list(group[data_type].to_numpy(), f, pad=pad) 
                
                new_columns.append(row)

            exp_df = pd.DataFrame(new_columns)

        else:
            #TODO: THIS ALTERNATIVE IS YET NOT IMPLEMENTED
            raise NotImplementedError("Prediction on sample level is not implemented yet.")

            pdf = self.level_dfs[self.prediction_level]

            exp_df = pd.DataFrame()
            exp_df["id"] = pdf["id"]

            #self.max_sample_length = max(len(ids) for ids in self.exp_df["pred_level"].values)
            
            for label in self.labels:
                exp_df[label] = self.encode_list(pdf["label"].values, label)

            # if self.prediction_level == "token":
            #     for f in self.feature_types:
            #         exp_df[f] = pdf[f].values


        #return exp_df
        self.exp_df = exp_df


    def __change_split_level(self):
        
        #we get the set of split ids and compare it to a level to find witch it matches
        split_sets = set()
        for split_id, splits in self.splits.items():
            split_sets.update(splits["train"].tolist())
            split_sets.update(splits["dev"].tolist())
            split_sets.update(splits["test"].tolist())

        split_size = len(split_sets)

        # if split_size is the same as the exp_df shape it means that the split are on the exp level
        # so no need to change the split level
        if self.exp_df.shape[0] == split_size:
            return


        #lets find the level given splits are of
        # TODO: make this more exhaustive by making sure all ids exist in the level df
        split_id_level = False
        for level, df in self.level_dfs.items():
            
            level_size = df.shape[0]
            if level_size == split_size:
                split_id_level = f"{level}_id"
                break
                
        if not split_id_level:
            raise RuntimeError("No matching level found for given splits. Given splits need to match level else chaning level is not doable.")

        self.original_splits = self.splits
        for split_id, splits in self.splits.copy().items():
            for split_type, split in splits.copy().items(): 
                cond = self.level_dfs[self.sample_level][split_id_level].isin(split)
                new_split = self.level_dfs[self.sample_level]["id"][cond].to_numpy()
                self.splits[split_id][split_type] = new_split


    def __create_splits(self):
        raise NotImplementedError("No support for that splitting alternative yet")
    

    def __fix_labels(self):

        self.subtasks = []
        labels = set()
        labels.update(self.tasks)

        for t_label in self.tasks:
            
            t_labels = t_label.split("_")

            if len(t_labels) < 1:
                break
            
            labels.update(t_labels)
        
            self.level_dfs[self.prediction_level][t_label] = self.level_dfs[self.prediction_level][t_labels].apply(lambda x: '_'.join(x), axis=1)
        
        self.labels = sorted(list(labels))


    def remove_duplicates(self):

        def __get_duplicate_set(df):

            # TODO: solve this with groupby isntead???
            duplicate_mask_all = df.duplicated(subset="text",  keep=False).to_frame(name="bool")
            duplicate_ids_all = duplicate_mask_all[duplicate_mask_all["bool"]==True].index.values

            dup_ids = df.loc[duplicate_ids_all]["id"]
            dup_items = df.loc[duplicate_ids_all]["text"]
            dup_dict = dict(enumerate(set(dup_items)))
            dup_pairs = {i:[] for i in range(len(dup_dict))}
            for i, item in dup_dict.items():
                for ID, item_q in zip(dup_ids, dup_items):
                    if item == item_q:
                        dup_pairs[i].append(ID)

            return list(dup_pairs.values())

        target_level = self.dataset_level
        df = self.level_dfs[target_level]
        duplicate_sets = __get_duplicate_set(df)
        duplicate_ids = np.array([i for duplicate_ids in duplicate_sets for i in  duplicate_ids[1:]])

        df = df[~df["id"].isin(duplicate_ids)]
        df.reset_index(drop=True, inplace=True)
        self.level_dfs[target_level] = df


        for level, df in self.level_dfs.items():

            if level == target_level:
                continue

            df = df[~df[f"{target_level}_id"].isin(duplicate_ids)]
            df.reset_index(drop=True, inplace=True)
            self.level_dfs[level] = df

        
        self.duplicate_ids = duplicate_ids

        if hasattr(self, "splits"):
            self.update_splits()

        logger.info(f"Removed {len(duplicate_ids)} duplicates from dataset. Duplicates: {duplicate_sets}")


    def update_splits(self):
        #then we need to update the splits and remove duplicate ids
        for split_id, splits in self.splits.copy().items():
            #splits = self.splits[split_id]["splits"].copy()
            for split_type, split in splits.copy().items():
                self.splits[split_id][split_type] = split[~np.isin(split,self.duplicate_ids)]


    def save(self, pkl_path):
        u.pickle_data([self.level_dfs, self.dataset_level], pkl_path)


    def load(self, pkl_path):
        if hasattr(self, "level_dfs"):
            raise RuntimeError("data already exist. Overwriting is currently, unsupported with load()")

        self.level_dfs, self.dataset_level = u.load_pickle_data(pkl_path)
        self.stack_level_data = {l:[] for l in self.level_dfs.keys()}


    def add_splits(self, splits:list):
        assert len(splits)
        assert isinstance(splits,dict)
        self.splits = splits


    def prep_experiment(self, 
                        sample_level:str, 
                        prediction_level:str, 
                        task_labels:list, 
                        #subtasks:list, 
                        feature_types:list,
                        splits=None,
                        data_path:str=None,
                        remove_duplicates:bool=True,
                        pad:bool=True
                        ):

        # if (sample_level != prediction_level) and (step_level != prediction_level) and step_level != None:
        #     raise NotImplementedError("There is yet no support to predict on a sub-level of sample while step_level is not the same as predction level.")

        self.tasks = task_labels
        self.feature_types = feature_types
        self.sample_level = sample_level
        self.prediction_level = prediction_level

        self.__fix_labels()

        if remove_duplicates:
            self.remove_duplicates()

        self.__construct_exp_df(pad=pad)

        #CONVERTING SPLITSwa
        if not hasattr(self, "splits"):
            if not splits:
                self.__create_splits()
            else:
                self.add_splits(splits)

        if self.duplicate_ids.any():
            self.update_splits()

        self.__change_split_level()


        self.max_words = {}
        for level in self.level_dfs.keys():

            if level == "token":
                continue

            self.max_words[level] = int(np.nanmax(self.level_dfs["token"][f"{level[0]}_token_id"].to_numpy()))+1

        self.itersplits = iter(self.splits.items())


    def get_subtask_postions(self, subtask):
        return self._subtasks.index(subtask)

        

    
    
    



    # def load_data(self, samples, save_path:str=None):

    #     level_dfs = {}
    #     #global_indexes = {}
    #     self.dataset_level = samples[0].type
    #     sample_rows = []
    #     for sample in samples:

    #         sample_rows.append({
    #                                 "id":sample.id, 
    #                                 "text": sample.text, 
    #                                 "label": sample.label
    #                             })

    #         for level, df in sample.level_dfs.items():
                
    #             if level not in level_dfs:
    #                 level_dfs[level] = []

    #             #     global_indexes[level] = 0
    #             # df_len = df.shape[0]
    #             # df[f"g_{level}_id"] = range(global_indexes[level],global_indexes[level]+df.shape[0])
    #             # global_indexes[level] += df.shape[0]
                    
 
    #             level_dfs[level].append(df)

    #     combined_level_dfs = {level:pd.concat(df_list) for level, df_list in level_dfs.items()}
    #     combined_level_dfs[self.dataset_level] = pd.DataFrame(sample_rows)
        
    #     # #if we have more than
    #     # if len(combined_level_dfs.keys()) > 2:
    #     #     self.__add_global_ids(combined_level_dfs)

    #     for level, df in combined_level_dfs.items():
    #         #df.reset_index(drop=True, inplace=True)
    #         logger.info(f'DataFrame of level {level}- \n{df.head()}')

    #     self.level_dfs = combined_level_dfs

    #     if save_path:
    #         self.save(save_path)




    #logger.info(samples.print())
    # logger.info('DataFrame - \n{}'.format(df.head()))
    # assert isinstance(df, pd.DataFrame), "_worker needs to return a DataFrame"
    # assert not set(df.columns).difference(set(["ids","words", "pos_tags", "tok_sents", "labels", "lengths"])), "incorrect columns"
    # assert df["ids"][0] == 0, "ids need to start on 0"
    # assert isinstance(df["words"][0], tuple) # important for duplicate removal
    # assert "".join(["".join(doc) for doc in df["words"].values]).islower(),"words are not lowercased"
    # assert "".join(["".join(["".join(sent) for sent in doc]) for doc in df["tok_sents"]]).islower(),"tok_sents are not lowercased"

    # if self._level == "sentence":
    #     logger.info("Converting DataFrame to sentence level")
    #     df = self.__convert_to_sentence_lvl(df)
    #     logger.info('DataFrame  Sentences - \n{}'.format(df.head()))

    #return samples


    # if split_level != self.sample_level:
    #     self.splits = self.__change_split_level(split_data, split_level)
    # else:
    #     self.splits = split_data
    #self._iter_splits = iter(split_data)

    # def __convert_splits_to_sentence_lvl(self):

    #     new_splits = []
    #     for sent_sample in self.samples:

    #         for split_set in self._split_ids:

    #             ID, train, dev, test = split_set
    #             new_train, new_dev, new_test = [],[],[]

    #             if sent_sample.doc_id in train:
    #                 new_train.append(sent_sample.id)
    #             elif sent_sample.doc_id in dev:
    #                 new_dev.append(sent_sample.id)
    #             else:
    #                 new_test.append(sent_sample.id)

    #             new_splits.append([  
    #                                 ID,
    #                                 np.array(new_train),
    #                                 np.array(new_dev), 
    #                                 np.array(new_test)
    #                                 ])
    #     return new_splits


    # def __convert_to_sentence_lvl(self):
    #     sentences = []
    #     new_id = 0
    #     for sample in self.samples:
    #         for sent_sample in sample.sentences:
    #             sent_sample.reset(new_id=new_id)
    #             sentences.append(sent_sample)
    #             new_id += 1
        
    #     print("SENTENCES", len(sentences))
    #     return sentences


    # def __print(self):
    #     #print some stats
    #     logger.info(f"Found {len(self)} samples")
    #     logger.info(f"Example of sample (first 15 words): \n {self.samples[0][:15]} \n")

    #     if self._level != "sentence":
    #         logger.info(f"Example of sample sentence (first sentence in first sample): \n {self.samples[0].sentences[0]} \n")

    #     label_exp = [t.label for t in self.sample[1].tokens[:10]]
    #     logger.info(f"Example of labels (first 10 labels): \n {label_exp} \n")
    #     logger.info(f"Longest document (word count): {self.max_sample_length}")




    # def get_splits(self):
    #     return next(self._iter_splits)


    # def override_test_preds(self, pkl_file):


    #     test_preds = u.load_pickle_data(pkl_file)

    #     # TODO:
    #     # get the rows of test samples 
    #     # overrite the subtask label in the token dict
    #     # overrite the rows
    #     # NOTE!
    #     # as we are not evaulating the subtask we are overwriting
    #     # we dont need to perserve the original test labels for that subtask
    #     # 


    # def encode_dataset(self, tasks:list, subtasks:list, feature_types:list, level=str):

        # self._tasks = tasks
        # self._subtasks = subtasks
        # label_list = sorted(set(tasks+subtasks))

        # # creating encoders for each of given feature types
        # self.__create_encoders(feature_types, label_list)
        
        # for sample in tqdm(self.samples):
        #     sample.apply()


        #     logger.info("Encoding and padding  samples (samples are overwritten) ... ")
        #     rows = []
        #     for i,sample in tqdm(self._dataset_df.iterrows(), total=len(self)):

        #         row = [sample["ids"]]

        #         # add feature_type encodigns
        #         for feat_type in feature_types:
        #             data = sample[feat_type] if feat_type != "chars" else sample["words"]
        #             row.append(self.encode_list(data,feat_type, pad=True))

        #         # add label encodings
        #         for label in label_list:
        #             row.append(self.encode_list(sample["labels"],label,pad=True))

        #         # add sample length 
        #         row.append(len(sample["words"]))


        #         if self._level == "sentence":
        #             row.append(sample["doc_ids"])


        #         rows.append(tuple(row))


        #     df = pd.DataFrame(rows)

        #     #label the rows
        #     columns = ["ids"]
        #     columns.extend(feature_types)
        #     columns.extend(label_list)
        #     columns.append("lengths")

        #     if level=="sentence":
        #         columns.append("doc_ids")

        #     df.columns = columns

        #     logger.info('Encoded DataFrame- \n{}'.format(df.head()))

        # self._dataset_df = df