
#basics
import numpy as np

#pytroch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#wrapper class
from axlnlp.models.base import PyToBase

# use a torch implementation of CRF
from torchcrf import CRF

#am
#from am.modules.datasets.base import AMDataset


class BiLSTM_CNN_CRF(PyToBase):

    def __init__(self,dataset:None, features:dict, params:dict):
        super().__init__(dataset=dataset, features=features, params=params)

        self.BATCH_SIZE = params["hyperparams"]["batch_size"]
        self.OPT = params["hyperparams"]["optimizer"]
        self.LR = params["hyperparams"]["lr"]
        self.DROPOUT = params["hyperparams"]["dropout"]
        self.HIDDEN_DIM = params["hyperparams"]["hidden_dim"]


        NUM_FILTER = 4
        KERNEL_SIZE = 3
        C_EMB_DIM = 100
        W_EMB_DIM = 100


        self.dropout = nn.Dropout(self.DROPOUT)
        
        self.char_emb_layer = nn.Embedding( 
                                            num_embeddings=len(dataset._encoders["chars"]), 
                                            embedding_dim=C_EMB_DIM, 
                                            padding_idx=0
                                            )
        #nn.init.uniform_(self.char_emb_layer.weight, -0.5, 0.5) # Option: Ma, 2016

        self.char_cnn = nn.Conv1d(  
                                    in_channels=C_EMB_DIM, 
                                    out_channels=C_EMB_DIM, 
                                    kernel_size=KERNEL_SIZE, 
                                    groups=C_EMB_DIM,
                                    )

        #generate the word embedding based on char embeddings
        self.max_pool = nn.MaxPool1d(KERNEL_SIZE)


        #lstm for words
        self.lstm = nn.LSTM(    
                                input_size=W_EMB_DIM+C_EMB_DIM, 
                                hidden_size=self.HIDDEN_DIM, 
                                num_layers=1, 
                                bidirectional=True,  
                                batch_first=True
                                )



        #output layers. One for each task
        self.output_layers = nn.ModuleDict()

        #Crf layers, one for each task
        self.crf_layers = nn.ModuleDict()

        for task in params["tasks"]:
            output_dim = len(self.dataset._encoders[task])
            self.output_layers[task] = nn.Linear(self.HIDDEN_DIM, output_dim)
            self.crf_layers[task] = CRF(num_tags=output_dim, batch_first=True)


    def forward(self, batch):

        word_embs = batch["glove"]
        chars = batch["chars"]
        mask = batch.mask
    
        # get character embeddings
        # MIGHT NEED TO ADD PADDING TO WORDS?
        print("CHAR", chars.shape)
        batch_size = chars.shape[0]
        seq_length = chars.shape[1]
        char_length = chars.shape[2]

        char_embs = self.char_emb_layer(batch["chars"])


        emb_size = char_embs.shape[-1]

        print("CHAR EMB", char_embs.shape)
        char_embs = char_embs.view(-1, char_length, emb_size).transpose(1, 2)

        #c2 = char_embs.view(-1, char_size[2], char_size[3]).transpose(1, 2)
        print("CHAR EMBS 2", char_embs.shape)

        # create word embeddings from character embeddings
        cnn_out = self.char_cnn(char_embs)


        print("CNN OUT", cnn_out.shape)

        word_char_embs = cnn_out.max(dim=2)[0] #self.max_pool(cnn_out)

        print("MAXPOOL; WORD CHAR EMBS", word_char_embs.shape)

        word_char_embs = word_char_embs.view(batch_size, seq_length, -1)

        print("MAXPOOL; WORD CHAR EMBS 2", word_char_embs.shape)

        print("WORD EMB", word_embs.shape)

        # concatenate the embeddings
        cat_emb = torch.cat((word_embs, word_char_embs), dim=2)

        # pack padded sequences
        packed_embs = nn.utils.rnn.pack_padded_sequence(cat_emb, seq_lens, batch_first=True)

        # feed packed to lstm
        lstm_out, _ = self.lstm(packed_embs)

        tasks_preds = {}
        tasks_loss = {}
        for task, output_layer in self.output_layers.items():

            #linear layer
            dense_out = output_layer(lstm_out)

            target_tags = batch[task]

            # CRF
            crf = self.crf_layers[task]
            loss = crf( 
                        emissions=dense_out, #score for each tag, (batch_size, seq_length, num_tags) as we have batch first
                        tags=target_tags,
                        mask=mask,
                        reduction='sum'
                        )

            preds = crf.decode( 
                                emissions=dense_out, 
                                mask=mask
                                )

            tasks_preds[task] = preds
            tasks_loss[task] = output


        return tasks_loss, tasks_preds