import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from yqn_pytorch_framework.pytorch_initialize import prepare_pack_padded_sequence, init_embedding, init_linear
from booking_ner.data.pytorch_ner_data_utils import load_word2vec
import pickle

class BiLSTM(nn.Module):
    """
        BiLSTM
    """

    def __init__(self, **kwargs):
        super(BiLSTM, self).__init__()
        for k in kwargs:
            self.__setattr__(k, kwargs[k])

        V = self.embed_num
        D = self.embed_dim
        C = self.label_num
        padding_id = self.padding_id

        self.embed = nn.Embedding(V, D, padding_idx=padding_id)
        init_embedding(self.embed.weight)

        print("self.emb_file:", self.emb_file)
        with open(self.map_file, "rb") as f:
            char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
        self.pretrained_weight = load_word2vec(self.emb_file , id_to_char, self.embed_dim, self.embed)
        self.embed = self.pretrained_weight

        self.seg_embed = nn.Embedding(5, 20, padding_idx=padding_id)
        # if False:
        #     print("pretrained_weight:::",   self.pretrained_weight)
        #     self.embed.weight.data.copy_(torch.from_numpy(self.pretrained_weight))
        # else:
        #     init_embedding(self.embed.weight)

        self.dropout_embed = nn.Dropout(self.dropout_emb)
        self.dropout = nn.Dropout(self.dropout)

        self.bilstm = nn.LSTM(input_size=D+20,
                              hidden_size=self.lstm_hiddens,
                              num_layers=self.lstm_layers,
                              bidirectional=True, batch_first=True, bias=True)

        self.linear = nn.Linear(in_features=self.lstm_hiddens * 2, out_features=C, bias=True)
        init_linear(self.linear)

    def forward(self, word, sentence_length, seg):
        """
        :param word:
        :param sentence_length:
        :return:
        """

        # print("wordwordwordword", word)
        # print("sentence_length:", sentence_length)

        # word, sentence_length, sorted_indices = prepare_pack_padded_sequence(word,
        #                                                                      sentence_length,
        #                                                                      device=self.device)
        # # print("word22222", word)
        # # print("sentence_length:", sentence_length)
        # # print("sorted_indices:", sorted_indices)
        # x = self.embed(word)  # (N,W,D)
        # seg = self.seg_embed(seg)
        # x = self.dropout_embed(x)
        # seg = self.dropout_embed(seg)
        # seg = seg[sorted_indices]
        #
        # packed_embed = pack_padded_sequence(x, sentence_length, batch_first=True, enforce_sorted=True)
        # emb_token_seg = [x, seg]
        # x = torch.cat(emb_token_seg,-1)
        # x, _ = self.bilstm(x)
        # x, _ = pad_packed_sequence(x, batch_first=True)
        # x = x[sorted_indices]
        # x = self.dropout(x)
        # x = torch.tanh(x)
        # logits = self.linear(x)



        # segs = segs.to("cuda:0")
        segs = seg
        word, sentence_length, desorted_indices = prepare_pack_padded_sequence(word, sentence_length, device=self.device)
        # segs, sentence_length_segs, desorted_indices_segs = prepare_pack_padded_sequence(segs, sentence_length,device=self.device)

        # print("word_model:", word)
        # print("sentence_length:", sentence_length)
        # print("desorted_indices:", desorted_indices)
        x = self.embed(word)  # (N,W,D)

        segs_embed = self.seg_embed(segs)
        embed_list = [x,segs_embed]
        embed_list = torch.cat(embed_list,-1)
        x = self.dropout_embed(embed_list)

        packed_embed = pack_padded_sequence(x, sentence_length, batch_first=True)
        x, _ = self.bilstm(packed_embed)
        x, _ = pad_packed_sequence(x, batch_first=True)
        x = x[desorted_indices]
        x = self.dropout(x)
        x = torch.tanh(x)
        logit = self.linear(x)
        return logit
