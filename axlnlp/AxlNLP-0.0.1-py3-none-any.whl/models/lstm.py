import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from axlnlp.models.base import PyToBase
import numpy as np


class LSTM(PyToBase):

    def __init__(self, dataset:None, features:dict, hyperparams:dict):
        super().__init__(dataset=dataset, features=features, hyperparams=hyperparams)

        self.BATCH_SIZE = hyperparams["batch_size"]
        self.OPT = hyperparams["optimizer"]
        self.LR = hyperparams["hidden_dim"]
        self.DROPOUT = hyperparams["dropout"]
        self.HIDDEN_DIM = hyperparams["hidden_dim"]
        
        # embedding layer to get features
        #self.emb_layer = nn.Embedding.from_pretrained(torch.tensor(feature_dict["glove"]),  freeze=True, padding_idx=0)
        #EMB_DIM = self.emb_layer.embedding_dim
        EMB_DIM = features.feature_dim

        #lstm
        self.lstm = nn.LSTM(    
                                EMB_DIM, 
                                self.HIDDEN_DIM, 
                                num_layers=1, 
                                bidirectional=False,  
                                batch_first=True
                            )

        if self.DROPOUT:
            self.dropout = nn.Dropout(self.DROPOUT)

        #output layers. One for each subtask
        self.output_layers = nn.ModuleDict()
        for task in dataset.tasks:
            output_dim = len(dataset.encoders[task])
            self.output_layers[task] = nn.Linear(self.HIDDEN_DIM, output_dim)


    def loss(self, output, target):
        #print("LOSS INPUT", F.log_softmax(output,dim=-1))
        return F.nll_loss(F.log_softmax(output,dim=-1), target, reduction="mean")


    def forward(self, batch):

        # x shape is (batch_size, seq_length)
        word_embs = batch["embs"]

        #embs_do = self.dropout(embs)

        packed_embs = nn.utils.rnn.pack_padded_sequence(word_embs, batch["lengths"], batch_first=True)

        lstm_packed, _ = self.lstm(packed_embs)
        lstm_out = F.leaky_relu(lstm_packed.data)

        tasks_pred = {}
        tasks_loss = {}
        for task, output_layer in self.output_layers.items():

            #input shape: (batch, seq_length, label_size)
            #output shape: (batch, seq_length, label_size)
            outputs = F.leaky_relu(output_layer(lstm_out))

            tasks_pred[task] = torch.argmax(F.softmax(outputs,dim=-1),dim=-1).cpu().detach().numpy()
            tasks_loss[task] = self.loss(outputs, batch.get_flat(task, remove=777))
        
        return tasks_loss, tasks_pred

