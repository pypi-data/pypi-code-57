
import torch 
import numpy as np
from transformers import BertTokenizer


class DatasetEncoder:

    def add_encoder(self, *args, **kwargs): # name, data, max_sample_length=None, pad_value=0):
        
        name = kwargs["name"]

        if name == "chars":
            encoder = self.CharEncoder
        elif name == "bert":
            encoder = self.BertTokEncoder
        else:
            encoder = self.SimpleEncoder

        self.encoders[name] = encoder(*args, **kwargs)
        
                                        # name=name, 
                                        # data=data, 
                                        # pad_value=pad_value,
                                        # max_sample_length=max_sample_length
                                        # )


    def decode(self, item:str, name:str):
        return self.encoders[name].decode(item)


    def encode(self, item:str, name:str):
        return self.encoders[name].encode(item)


    def decode_list(self, item:str, name:str, pad=False):
        return self.encoders[name].decode_list(item, pad=pad)


    def encode_list(self, item:str, name:str, pad=False):
        return self.encoders[name].encode_list(item, pad=pad)


    class Encoder:
        
        def __init__(self, name:str, data:list, max_sample_length:int=None, pad_value:int=None):
            self._name = name
                
            if pad_value == 0:
                start = 1
            else:
                start = 0

            self.id2item = dict(enumerate(sorted(self._get_unique(data)),start=start))
            self.item2id = {w:i for i,w in self.id2item.items()}

            if pad_value != None:
                #self.id2item[pad_value] = "PAD"
                #self.item2id["PAD"] = pad_value
                self.pad_value = pad_value

            if max_sample_length != None:
                self.max_sample_length = max_sample_length


        def __len__(self):
            return len(self.id2item)

        @property
        def name(self):
            return self._name
        

        def encode(self,item):
            return self.item2id[item]


        def decode(self,item):
            return self.id2item[item]


        def encode_list(self, item_list, pad=False):
            if pad:
                padded = np.zeros((self.max_sample_length,))
                padded.fill(self.pad_value)
                for i, item in enumerate(item_list):
                    padded[i] = self.encode(item)
                return padded
            else:
                return np.array([self.encode(item) for item in item_list])


        def decode_list(self, item_list, pad=False):
            return np.array([self.decode(item) for item in item_list])


    class SimpleEncoder(Encoder):

        def _get_unique(self,data):
            #return sorted(set([item for sublist in data for item in sublist]))
            return sorted(set(data))


    class CharEncoder(Encoder):


        def _get_unique(self,data):
            #words = sorted(set([item for sublist in data for item in sublist]))
            words = sorted(set(data))
            self.max_word_length = max(len(w) for w in words)
            characters = sorted(set([item for sublist in words for item in sublist]))
            return characters


        def encode(self,word, pad=False):

            if pad:
                padded = np.zeros((self.max_word_length,))
                padded.fill(self.pad_value)
                for i, c in enumerate(word):
                    padded[i] = self.item2id[c]
                return padded
            else:
                return np.array([self.item2id[c] for c in word])


        def decode(self,char_ids):
            return "_".join([self.id2item[c] for c in char_ids])


        def encode_list(self, item_list, pad=False):
            if pad:
                padded = np.zeros((self.max_sample_length, self.max_word_length))
                padded.fill(self.pad_value)
                for i, item in enumerate(item_list):
                    padded[i] = self.encode(item,pad=pad)
                return padded
            else:
                return np.array([self.encode(item) for item in item_list])
                #return torch.LongTensor([self.encode(item) for item in item_list])



    class BertTokEncoder:

        def __init__(self, name:str, data:list, max_sample_length:int=None, pad_value:int=None):
            self.name = name
            self.pad_value = pad_value
            self.max_sample_length = max_sample_length
            self.tokenizer = BertTokenizer.from_pretrained(
                                                        'bert-base-uncased',
                                                        )
        
        def encode(self, item, pad=False):
            enc_ids = self.tokenizer.encode(item, max_length=self.max_sample_length)
            return enc_ids


        def encode_list(self, item_list, pad=True):            
            item_string = " ".join(item_list)
            enc_ids = np.array(self.tokenizer.encode(   
                                                        item_string, 
                                                        add_special_tokens=True, 
                                                        max_length=self.max_sample_length, 
                                                        pad_to_max_length=True
                                                        ))
            return enc_ids