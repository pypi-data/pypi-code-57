#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:44:58 2020

@author: ryangosselin
"""

# LDA: linear discriminate analysis

import numpy as np

def LDA(nbPC, *args):
    ''' 
    
    LDA: linear discriminate analysis
    [T,P,SSX] = LDA(nbPC, X1, X2, Xi, ...)
    
    INPUT
    npPC [1 x 1] <numpy.ndarray>
        number of components in the LDA decomposition
    Xi [ni x k] <numpy.ndarray>
        spectra
        ni samples
        k variables
    
    OUTPUT
    T [(n1+n2+...) x nbPC] 
        scores
    P [nbPC x k] 
        loadings
    SSX [1 x nbPC] 
        Sum of squared variance explained by each component
        
    '''

    # Tuple containing n block matrices
    varargin = args
    n_block = len(varargin)
    
    # Number of columns in the data (dimensionality)
    k = varargin[0].shape[1]

    # Number of observation in each block
    N = np.zeros((n_block,1))
    for i in range(n_block):
        ni = varargin[i].shape[0]
        N[i] = ni

    # Means
    MU = np.zeros((n_block,k))
    for i in range(n_block):
        xi = varargin[i]
        mu = np.mean(xi,axis=0)
        MU[i,:] = mu
    
    # Overall mean
    MU_overall = np.mean(MU,axis=0)
    MU_overall = MU_overall[np.newaxis].T
    
    # Within-class scatter matrix
    Sw = np.zeros((k,k))
    for i in range(n_block):
        si = np.cov(varargin[i].T) # Class covariance matrices
        Sw = Sw + si
    
    # Between-class statter matrix
    Sb = np.zeros((k,k)) 
    for i in range(n_block):
        ni = N[i]
        mui = MU[i,:][np.newaxis].T
        sbi = ni * (mui-MU_overall)@(mui-MU_overall).T
        Sb = Sb + sbi
    Sb = Sb / np.sum(N)

    # Compute LDA projections
    Swinv = np.linalg.pinv(Sw) #Use pseudo-inverse to avoir rank issues
    SwinvSb = Swinv@Sb
    
    U,D,V = np.linalg.svd(SwinvSb)
    P = U[:,:nbPC]
    
    # Correct for rotational ambiguity
    for i in range(P.shape[1]):
        if P[:,i][np.newaxis]@np.ones((P.shape[0],1)) < 0:
            P[:,i] = -P[:,i]
    
    # Create overall X matrix containing n blocks    
    X = []
    for i in range(n_block):
        xi = varargin[i]
        if (i==0):
            X = xi
        else:
            X = np.append(X,xi,axis=0)
    
    T = X@P

    # Sum of squares -----------
    SSX = np.zeros((T.shape[1],1)) 
    for i in range(T.shape[1]):
        t = T[:,i][np.newaxis].T
        p = P[:,i][np.newaxis]
        Xhat = t@p
        #Xhat = T[:,i][np.newaxis].T@P[:,i][np.newaxis].T
        ssX0 = np.sum(np.sum(X * X)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
    # --------------------------

    
    # Sort by SSX   
    sort = np.argsort(SSX.T) 
    sort = np.fliplr(sort) # Decreasing order
    SSX = SSX[sort]
    T = np.squeeze(T[:,sort])
    P = np.squeeze(P[:,sort])

    return T,P,SSX