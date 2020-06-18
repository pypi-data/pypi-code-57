# cPCA: consensus PCA

import numpy as np

def cPCA(nbPC, *args):
    ''' 
    
    cPCA: consensus PCA
    [Tt, T_all, W, P_all, SSX, SSX_all] = cPCA(nbPC, X1, X2, Xi, ...)
    
    INPUT
    nbPC [1 x 1] <numpy.ndarray>
        number of components in the PCA decomposition
    Xi [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    
    Tt [n x nbPC] <numpy.ndarray>
        Super scores
    T_all [nbPC] <list>
        Scores for each block (corresponding to Xi)
    W [m x nbPC] <numpy.ndarray>
        Weights of each block (ie block loadings)
        m blocks
    P_all [nbPC] <list>
        Loadings for each block (corresponding to Xi)
    SSX [nbPC x 1] <numpy.ndarray>
        Sum of squared variance explained by each component
    SSX_all [nbPC x m] <list>
        Sum of squared variance explained by each component for each block
        m blocks
        
    '''
     
#%% Load data
    # Tuple containing n block matrices
    varargin = args
    n_block = len(varargin)
    
    # Creation of matrix X containing n blocks  
    X = []
    X_all = []
    for i in range(n_block):
        xi = varargin[i]
        if (i==0):
            X = xi
        else:
            X = np.append(X,xi,axis=1)

    
    n,k = X.shape

    # Save copy
    varargin0 = varargin
    X0 = X
    
    #%% Initialization 
    T = np.zeros((n, n_block))
    Tt = np.zeros((n,nbPC))
    W = np.zeros((n_block,nbPC))

    X_all = []

    # For creation of tuple containing T for each block
    T_all = []
    T_all_temp = []
    for i in range(n_block):
        Ti = np.zeros((n,nbPC))
        T_all.append(Ti)
    
    # Creation of tuple containing P for each block
    P_all = []
    P_all_temp = []
    for i in range(n_block): 
        Xi = varargin[i]
        n, ki = Xi.shape
        Pi = np.zeros((ki, nbPC))
        P_all.append(Pi)

    # Sum of squares
    SSXi = np.zeros((nbPC,n_block)) 
    
    #%% PCA
    
    for a in range(nbPC):
        tt = np.ones((n,1))
        tt_temp = np.ones((n,1))
        error_tt = 1
    
        while (error_tt > 1E-20):
        
            for i in range(n_block):
                Xi = varargin[i]
                pi = (Xi.T@tt)/(tt.T@tt)
                pi = pi/np.linalg.norm(pi)
                ti = Xi@pi
            
                T[:,i] = np.squeeze(ti)
        
            wt = (T.T@tt)/(tt.T@tt)
            wt = wt/np.linalg.norm(wt)
            tt = T@wt
        
            error_tt = sum(np.power((tt - tt_temp),2))
            tt_temp = tt
        
        for i in range(n_block):
            # Deflation 
            Xi = varargin[i]
            pi = (Xi.T@tt)/(tt.T@tt) 
            Xi = Xi - tt@pi.T
            X_all.append(Xi)
                         
            # Sum of squares of X
            Xi_hat = tt@pi.T
            Xi_0 = varargin0[i]
            ssXi_0 = np.sum(np.sum(Xi_0*Xi_0))
            ssXi = np.sum(np.sum(Xi_hat*Xi_hat))
            ssXi = ssXi/ssXi_0
            
            SSXi[a,i] = ssXi
            
            # Save pi 
            Pi = P_all[i]
            Pi[:,a] = np.squeeze(pi)
            P_all_temp.append(Pi)
        P_all = P_all_temp
        P_all_temp = []
        
    
        # Update of deflated blocks
        varargin = X_all
        X_all = []                         
    
        # Save
        Tt[:,a] = np.squeeze(tt)
        W[:,a] = np.squeeze(wt)
    
        for i in range(n_block):
            Ti = T_all[i]
            Ti[:,a] = T[:,i]
            T_all_temp.append(Ti)
        T_all = T_all_temp
        T_all_temp = []  
    
    SSX = np.sum(SSXi,axis=1)/n_block  
    
    SSX_all = SSXi
    
    return Tt, T_all, W, P_all, SSX, SSX_all
