
import nltk
import re
from colorama import Back, Style
from string import punctuation
import warnings
punctuation += "’‘,`'" + '"'


from tqdm import tqdm
from collections import namedtuple
import numpy as np

import pandas as pd

from functools import partial
import multiprocessing as mp

from axlnlp.utils import timer


#from unidecode import unidecode
#import swifter


nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')


"""
HOW DO WE PERSERVE THE ORIGINAL TEXT and CHARACTER INDEXES?

for each tokenized items we:

1) using find()
2 ) apply a quick vicinity search in the close area?




"""


strange_characters = {
                        '``':'"',
                        "''":'"'
                    }

class Preprocessor:


    def __paragraph_tokenize(self, doc):
        """
        Paragraph tokenization includes title in the first paragraph
        """
        # def clean(string):
        #     patterns = [
        #                 (r"\t|\n", " "),
        #                 (r"\s{2,999}", " "),
        #                 (r'"', "'"),
        #                 ]

        #     cleaned_string = string
        #     for p,r in patterns:
        #         cleaned_string = re.sub(p, r, cleaned_string)
        #     return string
    
        paras = []
        stack = ""
        chars_added = 0
        for i, para in enumerate(doc.split("\n")):
            #print([para])
            #para =  para.strip()

            if not para:
                stack += "\n"
                continue

            #to add title to first paragraph
            if i == 0:
                if len(re.findall(r"[\.?!]", para)) <= 2:

                    #if para[-1] not in punctuation:
                        #para += "."

                    stack += para
                    continue
                
            if stack:
                para = stack  + "\n" + para
                stack = ""

            paras.append(para)

        return paras


    def __get_global_id(self,level):
        try:
            return self.stack_level_data[level][-1]["id"] +1
        except IndexError as e:
            return 0


    def __get_parent_text(self, level):
        parents = self.level2parents[level]
        text = self.stack_level_data[parents[0]][-1]["text"]
        doc = self.stack_level_data[parents[-1]][-1]["text"]
        return doc, text


    def __get_char_idx(self, level):
        
        parents = self.level2parents[level]
        top_parent_row = self.stack_level_data[parents[-1]][-1]

        if not self.stack_level_data[level]:
            return  0

        level_row = self.stack_level_data[level][-1]

        if level_row[f"{self.dataset_level}_id"] != top_parent_row["id"]:
            current_idx = 0
        else:
            current_idx = level_row["char_end"]

        return current_idx


    def __get_structure_ids(self,level):

        parents = self.level2parents[level]
        first_parent = parents[0]
        upper_parents = parents[1:]
        last_parent_row = self.stack_level_data[first_parent][-1]

        #inherent all the ids of the closest parent
        ids ={k:v for k,v in last_parent_row.items() if "id" in k}
        ids[f"{first_parent}_id"] = ids.pop("id")


        # we can only inherent the ids fo the closes parent
        # so if we want to know which token we are at in the document or paragraph
        # we need to add this as it cannot be inherented from sentence ids
        first = True
        current_id_in_parent = 0
        if self.stack_level_data[level]:
            last_level_row = self.stack_level_data[level][-1]
            first = False

        for parent in upper_parents:
            parent_level_id = f"{parent[0]}_{level}_id"
            parent_id = f"{parent}_id"

            if not first:

                #if parent id is last row  != last id parent id in parent row
                if last_level_row[parent_id] != ids[parent_id]:
                    current_id_in_parent = -1
                else:
                    current_id_in_parent = last_level_row[parent_level_id]
            
            ids[parent_level_id] = current_id_in_parent


        return ids


    def __infer_text_type(self):
        if "\n" in self.text.strip():
            t =  "doc"
        elif self.text.count(".") >= 2:
            t = "paragraph"
        elif " " in self.text.strip():
            t = "sentence"
        else:
            t = "token"
        
        warnings.warn(f"No text_type was passed. text_type infered to '{t}'")
        return t


    def __build_tokens(self):

        parent_ids = self.__get_structure_ids("token")
        doc, sentence = self.__get_parent_text("token")
        current_token_idx = self.__get_char_idx("token")

        tokens = nltk.word_tokenize(sentence)
        token_pos = nltk.pos_tag(tokens)
        
        for i, (token,pos) in enumerate(token_pos):
            token_len = len(token)

            token = strange_characters.get(token, token)

            if current_token_idx == 0:
                start = 0
            else:
                start = doc.find(token, max(0, current_token_idx-2))

            end = start + token_len

            row =  {
                    "id": self.__get_global_id("token"),
                    "s_token_id": i,
                    "char_start": start,
                    "char_end": end,
                    "text": token.lower(),
                    "label": None,
                    "pos": pos,
                    }

            for parent in self.level2parents["token"][1:]:
                parent_ids[f"{parent[0]}_token_id"] += 1

            row.update(parent_ids)

            self.stack_level_data["token"].append(row)
            current_token_idx = end


    def __build_sentences(self):

        parent_ids = self.__get_structure_ids("sentence")
        doc, paragraph = self.__get_parent_text("sentence")
        current_sent_idx = self.__get_char_idx("sentence")
        #paragraph, current_sent_id,  current_sent_idx = self.__get_text_id_idx("sentence")
        sentences = nltk.sent_tokenize(paragraph)

        for i, sent in enumerate(sentences):
            sent_len = len(sent)
            
            if current_sent_idx == 0:
                start = 0
            else:
                start = doc.find(sent, current_sent_idx) #, current_sent_idx)

            end = start + sent_len
      
            row =  {
                    "id": self.__get_global_id("sentence"),
                    "p_sentence_id": i,
                    "text":sent,
                    "char_start": start,
                    "char_end": end,
                    "label": None
                    }

            for parent in self.level2parents["sentence"][1:]:
                parent_ids[f"{parent[0]}_sentence_id"] += 1

            row.update(parent_ids)

            self.stack_level_data["sentence"].append(row)

            current_sent_idx = end #sent_len + 1

            self.__build_tokens()


    def __build_paragraphs(self):

        parent_ids = self.__get_structure_ids("paragraph")
        doc, _ = self.__get_parent_text("paragraph")
        current_para_idx = self.__get_char_idx("paragraph")

        paras = self.__paragraph_tokenize(doc)

        for i,para in enumerate(paras):
            para_len = len(para)

            if i == 0:
                start = 0
            else:
                start = doc.find(para, current_para_idx)
            end = start + para_len
 
            para_len = len(para)
            row =  {
                    "id": self.__get_global_id("paragraph"),
                    "d_paragraph_id": i,
                    "text": para,
                    "char_start": start,
                    "char_end": end,
                    "label": None,
                    }

            for parent in self.level2parents["paragraph"][1:]:
                parent_ids[f"{parent[0]}_paragraph_id"] += 1

            row.update(parent_ids)

            self.stack_level_data["paragraph"].append(row)

            current_para_idx = end #+= para_len + 1

            self.__build_sentences()


    def __build_level_dfs(self, string, text_type, text_id, label):

        self.stack_level_data[text_type].append({
                                            "id":text_id,
                                            "text":string,
                                            "label":label
                                            })
        
        if text_type == "document":
            self.__build_paragraphs()
        elif text_type == "paragraph":
            self.__build_sentences()      
        elif text_type == "sentence":
            self.__build_tokens()   
        else:
            raise NotImplementedError(f'"{text_type}" is not a understood type')


    def __prune_hiers(self):

        new_level2parents = {self.dataset_level:[]}
        for k, v in self.level2parents.items():

            if k in self.parent2children[self.dataset_level]:
                new_level2parents[k] = v[:v.index(self.dataset_level)+1]
        
        self.level2parents = new_level2parents


    def __init_setup(self, level):
        self.dataset_level = level
        self.stack_level_data = {level:[]}
        self.stack_level_data.update({l:[] for l in self.parent2children[level]})
        self.level_dfs = {l:pd.DataFrame() for l in self.stack_level_data.keys()}
        self.__prune_hiers()

        #self.level_dfs = {level:pd.DataFrame(columns=["id", "text","label"])}
        # parents = [level]
        # for child_level in self.parent2children[level]:
        #     base_columns  = ["id","l_id", "text", "char_start", "char_end","label"]

        #     if child_level == "token":
        #         base_columns.append("pos")

        #     for p_level in parents:
        #         base_columns.append(f"{p_level}_id")

        #         if p_level != "document":
        #             base_columns.append(f"l_{p_level}_id")

        #     parents.append(child_level)
        #     self.level_dfs[child_level] = pd.DataFrame(columns=base_columns)


    def add_samples(self, data):


        """
        TODO: multiprocessing
        problem: 
        as we are infering global ids from the order of processing
        we cannot just pass the data to multiprocessing and add to
        a shared stacked dict.
        Instead we need to make sure the data storing is NOT shared 
        across the processes, then when combining the processed data
        we need to know which split/batch was first and update
        the next split ids appropriately.

        e.g. if we have 2 splits of 1000 samples
        both ids will range from 1-1000, hence for the 2nd split
        we just need to append 1000 to all of the global ids.

        """
        # if not hasattr(self, "dataset_level"):
        #     self.__init_setup(data[0]["text_type"])

        # manager = mp.Manager()
        # stack = manager.dict()
        # pool = mp.Pool(processes=8)
        # for k,v in self.stack_level_data.items():
        #     stack[k] = v
        # self.stack_level_data = stack

        # pool.map(self.add_sample,data)
        # pool.close()
        # pool.join()p

        for sample in tqdm(data, desc="preprocessing data"):
            self.add_sample(**sample, _Preprocessor__single=False)

        self._clear_stack()
    

    def _clear_stack(self):
        for level, stack in self.stack_level_data.items():
            self.level_dfs[level] = self.level_dfs[level].append(pd.DataFrame(stack))
        self.stack_level_data = {l:[] for l in self.stack_level_data.keys()}
 

    def add_sample(self, text:str, text_type:str, sample_id:int, label=None, __single:bool=True): #sample_dict):
        
        # text = sample_dict.get("text", None)
        # text_type = sample_dict.get("text_type", None)
        # sample_id = sample_dict.get("sample_id", None)
        # label = sample_dict.get("label", None)

        text_type = text_type if text_type else self.__infer_text_type()

        if not hasattr(self, "dataset_level"):
            self.__init_setup(text_type)
        
        # if isinstance(text_id,int):
        #     if text_id in self.stack_level_data[text_type]:
        #         raise ValueError("that id already exists")
        # else:
        #     text_id = self.stack_level_data[text_type.shape[0]

        self.__build_level_dfs(text, text_type, sample_id, label)

        if __single:
            self._clear_stack()


    def _label(self, row, char_spans):

        current_doc = row["document_id"]
        if self.__prev_doc != current_doc:
            self.__prev_BIO = "O"
            self.__d_span_id = -1
            self.__p_span_id = -1
        
        current_para = row["d_paragraph_id"]
        if self.__prev_para != current_para:
            self.__p_span_id = -1

        char_span = char_spans[row["document_id"]]
        label, label_id = char_span[row["char_end"]]
        label = label.copy() # make a seperate obj for each particular token


        if "None" in label_id:

            if self.__prev_BIO == "I":
                self.__prev_BIO = "O"

            label["span_id"] = None
            label["d_span_id"] = None
            label["p_span_id"] = None
            label["span_token_id"] = None
        
        else:


            if self.__prev_label_id != label_id and self.__prev_BIO != "B":
                
                #print("OKOKOKOK")
                label["seg"] = "B"
                self.__prev_BIO = "B"

                self.__span_token_id = 0
                self.__span_id += 1
                self.__d_span_id += 1
                self.__p_span_id += 1

            else:
                label["seg"] = "I"
                self.__prev_BIO = "I"


            label["span_id"] = self.__span_id
            label["d_span_id"] = self.__d_span_id
            label["p_span_id"] = self.__p_span_id
            label["span_token_id"] = self.__span_token_id

            
            self.__span_token_id += 1
        
        
        self.__prev_label_id = label_id
        self.__prev_para = current_para
        self.__prev_doc = current_doc

        return label


    @timer
    def label_spans(self, sample_labels:list, span_name:str):# sample_id, label_name:str, mapping:dict, text_items:str="tokens", method="in_span"):
        
        char_spans = dict(sample_labels)
        args = [char_spans]
        self.__prev_BIO = "O"
        self.__prev_doc = 0
        self.__prev_para = 0
        self.__span_id = -1 #global
        self.__d_span_id = -1 # span in doc
        self.__p_span_id = -1 # span in paragraph
        self.__span_token_id = 0 # token per span id
        self.__prev_label_id = None

        #label tokens
        t_df = self.level_dfs["token"]
        #token_labels = t_df.swifter.apply(self._label, axis=1,  args=args)
        token_labels = t_df.apply(self._label, axis=1,  args=args)
        token_labels_df = pd.DataFrame(list(token_labels.to_numpy()))
        self.level_dfs["token"] = pd.concat([t_df,token_labels_df], sort=False, axis=1)

        #create a level_df for the labled spans
        filtered_tokens = self.level_dfs["token"][~self.level_dfs["token"]["span_id"].isna()]

        groups = filtered_tokens.groupby("span_id", axis=0, sort=False)
        texts = [" ".join(g["text"]) for i,g in groups]

        from_first = ["d_span_id","p_span_id","ac", "stance", "relation", "document_id","d_paragraph_id","char_start"]
        from_last = ["char_end"]
        span_df = pd.concat(
                            [
                            groups.first().loc[:,from_first],
                            groups.last().loc[:,from_last]
                            ], 
                            sort=False, 
                            axis=1
                            )

        span_df.reset_index(drop=True, inplace=True)
        span_df["id"] = groups.first().index
        span_df["id"] = span_df["id"].astype(int)
        span_df["d_span_id"] = span_df["d_span_id"].astype(int)
        span_df.rename({
                        "d_span_id":f"d_{span_name}_id", 
                        "p_span_id":f"p_{span_name}_id",
                        }
                        ,axis="columns", inplace=True)

        span_df["text"] = texts

        self.level_dfs["token"].rename({
                                        "span_token_id": f"{span_name[0]}_token_id",
                                        "d_span_id":f"d_{span_name}_id", 
                                        "p_span_id":f"p_{span_name}_id",
                                        "span_id":f"{span_name}_id",
                                        },
                                        axis="columns", inplace=True)


        #TODO MAKE THIS INTO A FUNCTION
        for column in self.level_dfs["token"].columns:
            try:
                self.level_dfs["token"][column] = self.level_dfs["token"][column].astype(int)
            except:
                pass


        for column in span_df.columns:

            try:
                span_df[column] = span_df[column].astype(int)
            except:
                pass
        
        self.level_dfs[span_name] = span_df