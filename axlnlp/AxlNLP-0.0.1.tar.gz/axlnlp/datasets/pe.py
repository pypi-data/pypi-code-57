#basic
import re
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
import sys
import random
import os
from urllib.request import urlopen
from zipfile import ZipFile
import time
from pathlib import Path


# axlnlp
from axlnlp import get_logger
import axlnlp.utils as u
from axlnlp import DataSet
from axlnlp.utils import RangeDict

#ntlk
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# string
from string import punctuation
punctuation += "’‘,`'" + '"'

# import spacy
# nlp = spacy.load("en")

logger = get_logger(__name__)

#data example
''' T1  MajorClaim 503 575  we should attach more importance to cooperation during primary education
T2  MajorClaim 2154 2231    a more cooperative attitudes towards life is more profitable in one's success
T3  Claim 591 714   through cooperation, children can learn about interpersonal skills which are significant in the future life of all students
A1  Stance T3 For
T4  Premise 716 851 What we acquired from team work is not only how to achieve the same goal with others but more importantly, how to get along with others
T5  Premise 853 1086    During the process of cooperation, children can learn about how to listen to opinions of others, how to communicate with others, how to think comprehensively, and even how to compromise with other team members when conflicts occurred
T6  Premise 1088 1191   All of these skills help them to get on well with other people and will benefit them for the whole life
R1  supports Arg1:T4 Arg2:T3    
R2  supports Arg1:T5 Arg2:T3    
R3  supports Arg1:T6 Arg2:T3    
T7  Claim 1332 1376 competition makes the society more effective
A2  Stance T7 Against
T8  Premise 1212 1301   the significance of competition is that how to become more excellence to gain the victory
T9  Premise 1387 1492   when we consider about the question that how to win the game, we always find that we need the cooperation
T10 Premise 1549 1846   Take Olympic games which is a form of competition for instance, it is hard to imagine how an athlete could win the game without the training of his or her coach, and the help of other professional staffs such as the people who take care of his diet, and those who are in charge of the medical care
T11 Claim 1927 1992 without the cooperation, there would be no victory of competition
A3  Stance T11 For
R4  supports Arg1:T10 Arg2:T11  
R5  supports Arg1:T9 Arg2:T11   
R6  supports Arg1:T8 Arg2:T7
''' 
# TODO: is this  the cleanest solution to avoid .load() ??
def PE(dump_path="/tmp/"):
    return PE_Dataset(dump_path=dump_path).load()

class PE_Dataset:

    def __init__(self, dump_path="/tmp/"):
        self.name = "pe"
        self.dump_path = dump_path
        #self._dataset_path = "datasets/pe/data"
        self.dataset_url = "https://www.informatik.tu-darmstadt.de/media/ukp/data/fileupload_2/argument_annotated_news_articles/ArgumentAnnotatedEssays-2.0.zip"
        self._dataset_path = self.__download_data()
        self.splits = self.__splits()


    def __download_data(self):
        
        data_path = os.path.join(self.dump_path,"ArgumentAnnotatedEssays-2.0")
        self.dump_path = data_path

        if os.path.exists(data_path):
            brat_zip_file = str(list(Path(data_path).rglob("brat-project-final.zip"))[0])
            final_data_dir = brat_zip_file.rsplit(".",1)[0]
            return final_data_dir

        logger.info(f"Downloading data for PE dataset from {self.dataset_url}. Saving to {data_path}")

        zip_resp = urlopen(self.dataset_url)
        zip_dump_path = "/tmp/pe_data.zip"
        with open(zip_dump_path, "wb") as f:
            f.write(zip_resp.read())

        # unzip dump main file
        zf = ZipFile(zip_dump_path)
        zf.extractall(path=data_path)
        zf.close()

        brat_zip_file = str(list(Path(data_path).rglob("brat-project-final.zip"))[0])
        final_data_dir = brat_zip_file.rsplit(".",1)[0]

        #second file
        zf = ZipFile(brat_zip_file)
        zf.extractall(path=os.path.join(data_path, "ArgumentAnnotatedEssays-2.0"))
        zf.close()

        return final_data_dir


    def __read_file(self,file):
        with open(file,"r", encoding="utf8") as f:
            text = f.read()
        return text


    def __get_ac(self, annotation_line):
        #e.g. "MajorClaim 238 307"
        AC, start_char, end_char = annotation_line.split()
        return AC, int(start_char), int(end_char)


    def __get_stance(self, annotation_line):
        #e.g. "Stance T8 For"
        _, AC_ID, stance = annotation_line.split()
        return stance, AC_ID


    def __get_relation(self, annotation_line):
        #e.g. supports Arg1:T10 Arg2:T11 
        stance, arg1, arg2 = annotation_line.split()

        arg1_AC_ID = arg1.split(":")[1]
        arg2_AC_ID = arg2.split(":")[1]

        #get difference in number of AC's
        diff_in_acs = int(arg2_AC_ID[1:]) - int(arg1_AC_ID[1:]) 

        return str(diff_in_acs), stance, arg1_AC_ID


    def __parse_ann_file(self,ann, text_len):

        ac_id2span = {}

        ac_id2ac = {}
        ac_id2stance = {}
        ac_id2relation = {}

        ann_lines = ann.split("\n")
        for ann_line in ann_lines:
            # There are 3 types of lines:
            #['T1', 'MajorClaim 238 307', 'both of studying hard and playing sports are part of life to children']
            #["R5", "supports Arg1:T9 Arg2:T11 "  ]
            #["A3", "Stance T11 For"]

            if not ann_line.strip():
                continue

            segment_ID, annotation_line, *_ = ann_line.split("\t")

            # for MajorClaim, Premise, Claim
            if segment_ID.startswith("T"):
                ac, start_idx, end_idx = self.__get_ac(annotation_line)
                ac_id2span[segment_ID] = (start_idx,end_idx)
                ac_id2ac[segment_ID] = ac

            #for Stance
            elif segment_ID.startswith("A"):
                stance, AC_ID = self.__get_stance(annotation_line)
                ac_id2stance[AC_ID] = stance

            # for relations + stance
            else:
                relation, stance, AC_ID = self.__get_relation(annotation_line)
                ac_id2stance[AC_ID] = stance
                ac_id2relation[AC_ID] = relation


        # sort the span
        ac_id2span_storted = sorted(ac_id2span.items(),key= lambda x:x[1][0])

        # fill in some spans
        prev_span_end = 0
        for (_, (start,end)) in ac_id2span_storted.copy():

            if start-1 != prev_span_end:
                ac_id2span_storted.append((f"None_{start-1}",(prev_span_end,start-1)))

            prev_span_end = end
        

        if prev_span_end != text_len:
            ac_id2span_storted.append(("None_LAST",(prev_span_end,999999)))


        # sort again when added the missing spans
        ac_id2span = dict(sorted(ac_id2span_storted,key=lambda x:x[1][0]))
        
        return ac_id2span, ac_id2ac, ac_id2stance, ac_id2relation

    
    def __get_label_dict(self, ac_id2span, ac_id2ac,ac_id2stance, ac_id2relation):

        span2label = RangeDict()
        for ac_id, span in ac_id2span.items():
            label = {   
                        "seg":"O",
                        "ac": ac_id2ac.get(ac_id,"None"), 
                        "stance": ac_id2stance.get(ac_id,"None"), 
                        "relation": ac_id2relation.get(ac_id,"None")
                        }
            
            span2label[span] = [label, ac_id]

        return span2label


    def __splits(self):

    	# NOTE! we are provided with a test and train split but not a dev split
    	# approach after the original paper:
    	# https://arxiv.org/pdf/1612.08994.pdf (section 4) - join pointer model
    	# https://www.aclweb.org/anthology/P19-1464.pdf (section 4.1 -Dataset) - LSTM-Dist
    	# report that they randomly select 10% from the train set as validation set
    	# there is no reference a dev or validation split in 
    	# https://arxiv.org/pdf/1704.06104.pdf - (LSTM-ER, LSTM-CNN-CRF)
    	# 
    	# For only segmentation:
    	# https://www.aclweb.org/anthology/W19-4501.pdf (LSTM-CRF + flair, bert etc),
    	# report that they use the following samples for dev set:
    	#
    	# 13, 38, 41, 115, 140, 152, 156, 159, 162, 164, 201, 257,291, 324, 343, 361, 369, 371, 387, 389, 400 
    	# 
    	# however 21/322 = 6%, thus using smaller dev set
    	#
    	# We will randomly select a 10% as dev set


       	train_set = []
       	test_set = []

        split_path = str(list(Path(self.dump_path).rglob("train-test-split.csv"))[0])
        print(split_path)

       	with open(split_path, "r") as f:
       		for i,line in enumerate(f):

       			if not i:
       				continue

       			essay, split = line.replace('"',"").strip().split(";")
       			essay_id = int(re.findall(r"(?!0)\d+", essay)[0])

       			if split == "TRAIN":
       				train_set.append(essay_id)
       			else:
       				test_set.append(essay_id)

       	dev_size = int(len(train_set)*0.1)
       	dev_set = []
       	while len(dev_set) != dev_size:
       		s = random.choice(train_set)
       		train_set.remove(s)
       		dev_set.append(s)

        random.shuffle(train_set)
        random.shuffle(dev_set)
        random.shuffle(test_set)

       	return {
                    0:{
                        "train":np.array(train_set), 
                        "dev":np.array(dev_set),
                        "test": np.array(test_set)
                    }
                }


    def load(self):
        
        dump_path = "/tmp/pe_dataset.pkl"
        dataset = DataSet(data_path=dump_path)
        dataset.add_splits(self.splits)

        if not hasattr(dataset, "level_dfs"):

            ann_files = sorted(glob(self._dataset_path+"/*.ann"))
            text_files = sorted(glob(self._dataset_path+"/*.txt"))
            number_files = len(ann_files) + len(text_files)
            logger.info("found {} files".format(number_files))

            samples = []
            sample_span_labels = []
            grouped_files = list(zip(ann_files, text_files))
            for ann_file,txt_file in tqdm(grouped_files, desc="reading and formating PE files"):

                # -1 one as we want index 0 to be sample 1
                file_id = int(re.sub(r'[^0-9]', "", ann_file.rsplit("/",1)[-1])) #-1

                text = self.__read_file(txt_file)
                ann = self.__read_file(ann_file)

                # extract annotation spans
                ac_id2span, ac_id2ac,ac_id2stance, ac_id2relation = self.__parse_ann_file(ann, len(text))

                span2label = self.__get_label_dict(ac_id2span, ac_id2ac,ac_id2stance, ac_id2relation)
                            
                samples.append({
                                "sample_id":file_id,
                                "text":text, 
                                "text_type":"document"
                                })
                sample_span_labels.append((file_id,span2label))
            
            dataset.add_samples(samples)
            dataset.label_spans(sample_span_labels, "ac")
            dataset.save(dump_path)

        return dataset
        