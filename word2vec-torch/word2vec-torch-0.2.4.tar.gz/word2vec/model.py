import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init

"""
    u_embedding: Embedding for center word.
    v_embedding: Embedding for neighbor words.
"""


class SkipGramModel(nn.Module):

    def __init__(self, emb_size, emb_dimension):
        super(SkipGramModel, self).__init__()
        self.emb_size = emb_size
        self.emb_dimension = emb_dimension
        self.u_embeddings = []
        self.v_embeddings = []
        initrange = 1.0 / self.emb_dimension / len(emb_size)
        self.u_embeddings = nn.ModuleList([nn.Embedding(emb_size[i], emb_dimension, sparse=True) for i in range(len(emb_size))])
        self.v_embeddings = nn.ModuleList([nn.Embedding(emb_size[i], emb_dimension, sparse=True) for i in range(len(emb_size))])

        for i in range(len(emb_size)):
            init.uniform_(self.u_embeddings[i].weight.data, -initrange, initrange)
            init.constant_(self.v_embeddings[i].weight.data, 0)

    def forward(self, pos_u, pos_v, neg_v):
        emb_u = []
        for i in range(len(self.emb_size)):
            emb_u.append(self.u_embeddings[i](pos_u[:,i]))
        emb_u = torch.stack(emb_u, dim=1)

        score_all = []
        neg_score_all = []

        for i in range(len(self.emb_size)):
            emb_v = self.v_embeddings[i](pos_v[:,i])
            emb_neg_v = self.v_embeddings[i](neg_v[:,:,i])

            score = torch.bmm(emb_u,emb_v.unsqueeze(2))
            score = torch.clamp(score, max=10, min=-10)
            score_all.append(-torch.sum(F.logsigmoid(-score), dim=1).squeeze())

            neg_score = torch.bmm(emb_neg_v, torch.transpose(emb_u, 1, 2))
            neg_score = torch.clamp(neg_score, max=10, min=-10)
            neg_score_all.append(-torch.sum(F.logsigmoid(-neg_score), dim=1).squeeze())

        score_all = torch.stack(score_all, dim=1)
        neg_score_all = torch.stack(neg_score_all, dim=1)

        return torch.mean(score_all + neg_score_all)

    def save_embedding(self, file_name):
        for i in range(len(self.emb_size)):
            embedding = self.u_embeddings[i].weight.cpu().data.numpy()
            with open(file_name+'_'+str(i), 'w') as f:
                for j in range(len(embedding)):
                    f.write('%s %s\n' % (j, ' '.join(list(map(str,embedding[j])))))
