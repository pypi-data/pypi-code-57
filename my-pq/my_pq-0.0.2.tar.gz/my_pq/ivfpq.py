# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:01:16 2020

@author: huzhen
"""
from .pq import PQ
from scipy.cluster.vq import kmeans2,vq
import numpy as np


"""
1.IVF: 用kmeans给数据集划分区间。保存各个中心点,此步骤不必保存中心点下面的数据。可在步骤4中保存。
2.Residual:每个分区中：原始数据减去中心点。并存储Residual数据集。此时可抛弃原始数据集。

3.在Residual步骤结果的数据集上进行PQ学习，得到cookbooks:(M,Ks,Ds)。

以下是计算部分
4.对vecs数据集进行压缩（此数据集可能是训练数据集也可能是跟训练数据集分布一直的新数据集）
  得到codes:(N,M)，对压缩后的vecs，计算所属类别，并保存：centroid2vecindex
5.查询第一步:1)首先得到要在哪几个分区上进行查询。
            2) 计算query在筛选的各个分区上进行残差操作，得到不同的query_k。
            3) 在筛选的各个分区上，获取不同的dtable:(M,Ks)。
6.查询第二步，在各个分区上，根据各个分区的dtable进行检索。如果要找出前K个，那么假如筛选了H个分区，那么每个分区
  取前K//H向上取整个值。
"""

class IVFPQ:
    def __init__(self,K,M,Ks=256):
        self.K = K
        self.M = M
        self.Ks = Ks
        self.vecs = None
        self.codebooks = None
        self.pq = PQ(M,Ks)
        
        
    def ivf(self,vecs,iterations):
        print('vecs: ss',len(vecs))
        centroids,labels = kmeans2(data=vecs,k=self.K,iter=iterations,minit='points')
        return centroids,labels
    
    def residual(self,vecs,centroids,labels):
        vecs = vecs - centroids[labels]
        return vecs
        
    def fit(self,vecs,iterations=20,seed=123):
        """
        获取codebooks.shape=(M,Ks,Ds)
        """
        """
        聚类
        """
        self.centroids,self.labels = self.ivf(vecs,iterations)
        """
        残差
        """
        vecs = self.residual(vecs,self.centroids,self.labels)
        self.pq.fit(vecs=vecs,iterations=iterations,seed=seed)
        
    def encode(self,vecs):
        """
        对数据进行压缩，并保存压缩有的向量vecs:(N,M)
        centroid2vec:{centroid:[v1_index,v2_index,,,,]}
        """
        centroid_ids,_ = vq(vecs,self.centroids)
        vecs = vecs - self.centroids[centroid_ids]
        centroid2vec = {}
        for i,c_id in enumerate(centroid_ids):
            if c_id not in centroid2vec:
                centroid2vec[c_id] = []
            centroid2vec[c_id].append(i)
        vecs = self.pq.encode(vecs)
        self.vecs = vecs
        self.centroid2vec = centroid2vec
    
       
    def get_topH_partitions(self,query,H):
        """
        此时的query是原始query
        其实返回的就是前H个centroids的索引
        """
        _ = np.linalg.norm(self.centroids - query,axis=1)**2
        topH_ids = np.array([iid for iid in np.argsort(_) if iid in self.centroid2vec][:H])
        return topH_ids
    
        
    def dtable(self,query,topH_centroids):
        """
        根据query，获取dtables
        此时query是原始query
        """
#        topH_centroids = self.get_topH_partitions(query,H)
        dtables = []
        for i,pid in enumerate(topH_centroids):
            query = query - self.centroids[pid]
            dtables.append(self.pq.dtable(query))
            
        return dtables

    def find_topK(self,query,K,H):
        topH_centroids = self.get_topH_partitions(query,H)
        dtables = self.dtable(query,topH_centroids)
        ret = []
        total_dists = []
        for i in range(H):
            sub_vecs_ids = np.array(self.centroid2vec[topH_centroids[i]])
            sub_vecs = self.vecs[sub_vecs_ids]
            dists = dtables[i].adist(sub_vecs)
            topNum_ids = np.argsort(dists)[:K]
            total_dists += list(dists[topNum_ids])
            ret += list(sub_vecs_ids[topNum_ids])
        _ = sorted(zip(ret,total_dists),key=lambda x:x[1])[:K]
        return _
    


            
            
        
        
        
        


