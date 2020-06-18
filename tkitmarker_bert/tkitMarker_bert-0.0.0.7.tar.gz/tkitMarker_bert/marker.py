

import numpy as np
import torch
from transformers import AutoModelForTokenClassification,AutoTokenizer
import os
import re
import tkitFile
import regex
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# from elasticsearch_dsl import Q
# from config import *
from tqdm import tqdm
import time
import tkitText
# from memory_profiler import profile
import gc

class Marker:
    def __init__(self,model_path="../model",device='cpu'):
        self.model_path=model_path
        self.labels_file=os.path.join(model_path,"labels.txt")
        self.device=device
        pass
    def __del__(self):
        # self.release()
        pass

    def release(self):
        # print("释放显存")
        self.model.cpu()

        torch.cuda.empty_cache()
        pass
        # torch.cuda.empty_cache()
        del self.model
        del self.tokenizer
        del self.lablels_dict
        gc.collect()
    # @profile
    def load_model(self):
        # tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        # model.to(self.device)
        f2=open(self.labels_file,'r')
        lablels_dict={}
        for i,line in enumerate(f2):
            # l=line.split(" ")
            l=line.replace("\n",'')
            # print(l)
            lablels_dict[i]=l
        f2.close()
        self.lablels_dict=lablels_dict
        # self.model=model
        # self.tokenizer=tokenizer
        # self.model.eval()
        return self.model,self.tokenizer
    def cut_text(self,obj,sec):
        """
        分割固定长度字符串
        """
    #     textArr = re.findall('.{'+str(lenth)+'}', text)
    #     textArr.append(text[(len(textArr)*lenth):])
    #     return textArr
    # def cut(self,obj, sec):
        return [obj[i:i+sec] for i in range(0,len(obj),sec)]
    def clear_word(self,word):
        return word.replace("##", "")
    # @profile
    def filterPunctuation(self,x):
        x = regex.sub(r'[‘’]', "'", x)
        x = regex.sub(r'[“”]', '"', x)
        x = regex.sub(r'[…]', '...', x)
        x = regex.sub(r'[—]', '-', x)
        x = regex.sub(r"&nbsp", "", x)
        return x
    def pre(self,word,text):
        
        model=self.model
        # text=word+" [SEP] "+text
        lenth=500-len(word)
        all_ms=[]
        n=0
        h_i=2+len(word)
        with torch.no_grad():
            # model = AutoModelForTokenClassification.from_pretrained(self.model_path)
            # model.to(self.device)      
            text=self.filterPunctuation(text)
            for text_mini in self.cut_text(text,lenth):
                # text_mini=word+"[SEP]"+text_mini
                # print(word,"text_mini",text_mini)
                n=n+1
                ids=self.tokenizer.encode_plus(word,text_mini,max_length=512, add_special_tokens=True)
                # print(ids)
                input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
                labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
                outputs = model(input_ids, labels=labels)
                # print("outputs",outputs)
                tmp_eval_loss, logits  = outputs[:2]
                # ids=tokenizer.encode(text)
                # print(ids['token_type_ids'])

                # print("\n".join([i for i in self.lablels_dict.keys()]))
                words=[]
                for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                    # print(m)
                    # if i<h_i:
                    #     continue

                    # print(i,m,ids['input_ids'][i],self.tokenizer.convert_ids_to_tokens(ids['input_ids'][i]),self.lablels_dict[m])
                    # print(h_i)
                    word=self.tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                    # try:
                    #     word=text_mini[i-h_i]
                    # except:
                    #     continue
                    # print(word)


                    if m >=len(self.lablels_dict):
                        mark_lable="X"
                    else:
                        mark_lable=self.lablels_dict[m]

                    if mark_lable=="E-描述"  and len(words)>0:
                        
                        words.append(word)
                        # words.append(word+mark_lable)
                        # print(words)
                        
                        all_ms.append(self.clear_word("".join(words)))
                        words=[]
                    elif mark_lable=="S-描述":
                        words=[]
                        words.append(word)
                        # words.append(word+mark_lable)
                        all_ms.append(self.clear_word("".join(words)))
                        words=[]
                    elif mark_lable=="B-描述":
                        words=[]
                        words.append(word)
                        # words.append(word+mark_lable)
                    elif mark_lable=="M-描述" and len(words)>0:
                        words.append(word)
                        # words.append(word+mark_lable)
                    elif  mark_lable=="O" or mark_lable=="X":
                        words=[]
                        pass
        print("文章自动分段：",n)
        model.cpu()
        del model
        torch.cuda.empty_cache()
        gc.collect()
        return all_ms

    def pre_ner(self,text):
        model=self.model
        tokenizer=self.tokenizer
        model.eval()
        text=text
        lenth=128
        all_ms=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            words=[]
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                # print(word,self.lablels_dict[m])
                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-实体"  and len(words)>0:
                    
                    words.append(word)
                    # print(words)
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="S-实体":
                    words=[]
                    words.append(word)
                    all_ms.append(self.clear_word("".join(words)))
                    words=[]
                elif mark_lable=="B-实体":
                    words=[]
                    words.append(word)
                elif mark_lable=="M-实体"  and len(words)>0:
                    words.append(word)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms

