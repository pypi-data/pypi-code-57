# mbPLS: multiblock PLS

import numpy as np

def mbPLS(nbPC, Y, *args):
    '''
    
    HELP NOT FINISHED!!!!!
    
    mbPLS: multiblock PLS
    [X_auto, mX, sX] = mbPLS(nbPC, Y, X1, X2, Xi, ...)
    
    INPUT
    npPC [1 x 1] <numpy.ndarray>
        number of components in the mbPLS decomposition
    Y [n x m] <numpy.ndarray>
        responses
        n samples
        m variables
    Xi [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_auto [n x k] 
        preprocessed spectra
    mX [1 x k] 
        mean of all variables
    sX [1 x k] 
        standard deviation of all variables        
    
    '''
    
    
    
    
    
    
#%% Load data
    # Tuple containing n block matrices
    varargin = args
    n_block = len(varargin)
    
    # Creation matrix X containing n blocks    
    X = []
    for i in range(n_block):
        xi = varargin[i]
        if (i==0):
            X = xi
        else:
            X = np.append(X,xi,axis=1)

    n,k = X.shape
    n,l = Y.shape
    
    # Save copy
    varargin0 = varargin
    X0 = X
    Y0 = Y
    
    #%%  Initialization
    T = np.zeros((n,n_block))
    Tt = np.zeros((n,nbPC))
    U = np.zeros((n,nbPC))
    W = np.zeros((n_block,nbPC))
    
    X_all = []
    
    # For creation of tuple containing T for each block
    T_all = []
    T_all_temp = []
    for i in range(n_block):
        Ti = np.zeros((n,nbPC))
        T_all.append(Ti)
        
    # For creation of tuple containing W for each block
    Wi_all = []
    Wi_all_temp = []
    for i in range(n_block):
        Xi = varargin[i]
        n,ki = Xi.shape
        Wi = np.zeros((ki,nbPC))
        Wi_all.append(Wi)
           
   # Sum of squares
    SSXi = np.zeros((nbPC,n_block))
    SSY = np.zeros((nbPC,1))

    
    # %% PLS
    for a in range(nbPC):
        u = np.ones((n,1))
        u_temp = np.ones((n,1))
        tt_temp = np.ones((n,1))
        error_u = 1
        error_tt = 1
        
        while (error_u > 1E-20) and (error_tt > 1E-20):
            
                    for i in range(n_block):
                        Xi = varargin[i]
                        wi = (Xi.T@u)/(u.T@u)
                        wi = wi / np.linalg.norm(wi)
                        ti = Xi@wi
                        
                        T[:,i] = np.squeeze(ti)
                      
                        Wi = Wi_all[i]
                        Wi[:,a] = np.squeeze(wi)
                        Wi_all_temp.append(Wi)
                    Wi_all = Wi_all_temp
                    Wi_all_temp = []
                    
                    wt = (T.T@u)/(u.T@u)
                    wt = wt/np.linalg.norm(wt)
                    tt = (T@wt)/(wt.T@wt)
        
                    q = (Y.T@tt) / (tt.T@tt)
                    u = (Y@q) / (q.T@q)
        
                    error_tt = sum(np.power((tt-tt_temp),2),0) 
                    tt_temp = tt
        
                    error_u = sum(np.power((u-u_temp),2),0) 
                    u_temp = u
                                       
                    
        for i in range(n_block):
            # Deflation 
            Xi = varargin[i]
            pi = (Xi.T@tt)/(tt.T@tt) 
            Xi = Xi - tt@pi.T
            X_all.append(Xi)
            
            # Sum of squares for X
            Xi_hat = tt@pi.T
            Xi_0 = varargin0[i]
            ssXi_0 = np.sum(np.sum(Xi_0*Xi_0))
            ssXi = np.sum(np.sum(Xi_hat*Xi_hat))
            ssXi = ssXi/ssXi_0
            
            SSXi[a,i] = ssXi
            
            
        # Update of deflated blocks
        varargin = X_all
        X_all = []
        
        pt = (X.T@tt)/(tt.T@tt)
    
        # Scaling based on PLS Toolbox
#        tt = tt*np.linalg.norm(pt)  
#        wt = wt*np.linalg.norm(pt)
#        pt = pt/np.linalg.norm(pt)
            
        b = (u.T@tt)/(tt.T@tt)
        Y = Y - b*tt@q.T 
        
        # Sum of squares for Y
        Yhat = b*tt@q.T
        ssY0 = np.sum(np.sum(Y0*Y0))
        ssY = np.sum(np.sum(Yhat*Yhat))
        ssY = ssY / ssY0;
        SSY[a] = ssY
            
        
        # Save 
        Tt[:,a] = np.squeeze(tt)
        U[:,a] = np.squeeze(u)
        W[:,a] = np.squeeze(wt)
        
        for i in range(n_block):
            Ti = T_all[i]
            Ti[:,a] = T[:,i]
            T_all_temp.append(Ti)
        T_all = T_all_temp
        T_all_temp = []
    
                          
    SSX = np.sum(SSXi,axis=1)/n_block
 
    return Tt, T_all, W, Wi_all, SSX, SSY, SSXi
    
        