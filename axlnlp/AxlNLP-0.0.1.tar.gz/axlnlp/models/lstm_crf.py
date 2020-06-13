
#basics
import numpy as np
import time

#pytroch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence


#am
from axlnlp.models.base import PyToBase
import axlnlp.utils as u

# use a torch implementation of CRF
from torchcrf import CRF


'''
###MODEL DESCRIPTION### 
#######################

'''

class LSTM_CRF(PyToBase):

    def __init__(self,dataset:None, features:dict, hyperparams:dict):
        super().__init__(dataset=dataset, features=features, hyperparams=hyperparams)

        self.BATCH_SIZE = hyperparams["batch_size"]
        self.OPT = hyperparams["optimizer"]
        self.LR = hyperparams["lr"]
        self.HIDDEN_DIM = hyperparams["hidden_dim"]
        self.WORD_EMB_DIM = features.feature_dim
        self.NUM_RNN = hyperparams["num_rnn"]
        self.retrain_embs = False #params["retrain_embs"]

        #dropout
        self.use_dropout = False
        if hyperparams["dropout"]:
            self.dropout = nn.Dropout(hyperparams["dropout"])
            self.use_dropout = True


        # model is a reimplementation of Flairs.SequenceTagger (LINK).
        # Model is implemented to replicate the scores from ().
        # Why finetuning of embeddings is done like this is, i assume, because
        # the finetuning of multiple models, ELMO BERT FLAIR GLOVE, etc... in cases of concatenated 
        # embeddigns would be very difficult and not very usefull. Hence a small remapping at least 
        # produces some sort of finetuning of the combination of embeddings used.
        #
        # https://github.com/flairNLP/flair/issues/1433
        # https://github.com/flairNLP/flair/commit/0056b2613ee9c169cb9c23e5e84fbcca180dde77#r31462803
        if self.retrain_embs:
            self.emb2emb = torch.nn.Linear(self.WORD_EMB_DIM, self.WORD_EMB_DIM)

        #lstm for words
        self.lstm = nn.LSTM(    
                                input_size=self.WORD_EMB_DIM, 
                                hidden_size=self.HIDDEN_DIM, 
                                num_layers=self.NUM_RNN, 
                                bidirectional=True,  
                                batch_first=True
                            )

        #output layers. One for each task
        self.output_layers = nn.ModuleDict()

        #Crf layers, one for each task
        self.crf_layers = nn.ModuleDict()

        for task in self.dataset.tasks:

            #adding for padding tag = <ENDTAG> 
            output_dim = len(dataset.encoders[task])

            self.output_layers[task] = nn.Linear(self.HIDDEN_DIM*2, output_dim)
            self.crf_layers[task] = CRF(    
                                            num_tags=output_dim,
                                            batch_first=True
                                        )


    def forward(self, batch):

        lengths = batch["lengths"]
        mask = batch.mask
        word_embs = batch["embs"]

        if self.use_dropout:
            word_embs = self.dropout(word_embs)

        if self.retrain_embs:
            #see line 48, definition of layer, for info why
            word_embs = self.emb2emb(word_embs)


        #print(word_embs.shape)
        #print(lengths)
        packed_embs = pack_padded_sequence(word_embs, lengths, batch_first=True)
        lstm_out,_ = self.lstm(packed_embs)
        #lstm_out.data = F.leaky_relu(lstm_out.data)
        unpacked, lengths = pad_packed_sequence(lstm_out, batch_first=True, padding_value=0.0)
        
        if self.use_dropout:
            unpacked = self.dropout(unpacked)
 
        tasks_preds = {}
        tasks_loss = {}
        for task, output_layer in self.output_layers.items():

            dense_out = output_layer(unpacked)

            crf = self.crf_layers[task]

            target_tags = batch[task]
      
            # for CRF we need to treat our padding as an actual padding label
            # hence 666 will be out of bounce and we will replace it with OUTSIDE (O), label
            target_tags[target_tags == self.dataset.task2padvalue[task]] = 2

            loss = -crf(    
                            emissions=dense_out, #score for each tag, (batch_size, seq_length, num_tags) as we have batch first
                            tags=target_tags, #preds_lstm?, #predicted tags from LSTM?
                            mask=mask,
                            reduction='mean'
                            )


            #returns preds with no padding (padding values removed)
            preds = crf.decode( emissions=dense_out, 
                                mask=mask)


            #flatten the list
            preds = np.array([i for sublist in preds for i in sublist])

            tasks_preds[task] = preds
            tasks_loss[task] = loss


        return tasks_loss, tasks_preds