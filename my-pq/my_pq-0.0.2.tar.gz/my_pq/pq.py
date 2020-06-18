# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:44:39 2020

@author: huzhen
"""
import numpy as np
from scipy.cluster.vq import vq,kmeans2


class PQ:
    def __init__(self,M,Ks=256,verbose=True):
        """
        M:分区个数
        Ks:分区内聚类中心点个数
        codebooks:shape=(M,Ks,Ds)
        """
        self.M = M
        self.Ks = Ks
        self.verbose = verbose
        self.code_type = np.uint8 if self.Ks <= 2**8 else (np.uint16 if self.Ks <= 2**16 else np.uint32)
        self.codebooks = None
        self.Ds = None
        
        if self.verbose:
            print('M:{}, Ks:{}, code_type:{}'.format(self.M,self.Ks,self.code_type))
            
    
    def fit(self,vecs,iterations=20,seed=123):
        """
        主要是为了获得：code_word
        """
        N,D = vecs.shape
        self.Ds = D // self.M
        np.random.seed(seed)
        
        if self.verbose:
            print('iterations:{}, seed:{}'.format(iterations,seed))
        
        self.codebooks = np.zeros(shape=(self.M,self.Ks,self.Ds),dtype=np.float32)
        
        for m in range(self.M):
            if self.verbose:
                print('Traning subspace: {} / {}'.format(m+1,self.M))
            
            sub_vecs = vecs[:,m*self.Ds:(m+1)*self.Ds]
            self.codebooks[m],_ = kmeans2(sub_vecs,self.Ks,iter=iterations,minit='points')
    
    def encode(self,vecs):
        """
        数据压缩前:
            vecs.shape = (N,D)
        数据压缩后:
            vecs.shape = (N,M)
        """
        N,D = vecs.shape
        codes = np.empty(shape=(N,self.M),dtype=self.code_type)
        for m in range(self.M):
            if self.verbose:
                print('encoding subspace: {} / {}'.format(m+1,self.M))
            sub_vecs = vecs[:,m*self.Ds:(m+1)*self.Ds]
            codes[:,m],_ = vq(sub_vecs,self.codebooks[m])
        return codes
    
    
    def dtable(self,query):
        """
        dtable.shape = (M,ks)
        """
        D, = query.shape
        dtable = np.empty(shape=(self.M,self.Ks),dtype=np.float32)
        for m in range(self.M):
            sub_query = query[m*self.Ds:(m+1)*self.Ds]
            dtable[m,:] = np.linalg.norm(self.codebooks[m] - sub_query,axis=1)**2
        return DistanceTable(dtable)
    
class DistanceTable:
    def __init__(self,dtable):
        self.dtable = dtable
        
    def adist(self,codes):
        N,M = codes.shape
        dists = np.sum(self.dtable[range(M), codes], axis=1)
        return dists

