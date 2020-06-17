# PCA: principal component analysis

import numpy as np

def PCA(X, nbPC):
    ''' 
    
    PCA: principal component analysis
    [T,P,SSX] = PCA(X, nbPC)
    
    INPUT
    npPC [1 x 1] <numpy.ndarray>
        number of components in the PCA decomposition
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    T [n x nbPC] 
        scores
    P [nbPC x k] 
        loadings
    SSX [1 x nbPC] 
        Sum of squared variance explained by each component
        
    '''
    
    s0, s1 = X.shape
    T = np.zeros((s0, nbPC))
    P = np.zeros((s1, nbPC))
    SSX = np.zeros((nbPC, 1))
    X0 = X # Save a copy
    
    for i in range(0,nbPC):
        error = 1
        t_temp = np.ones((s0, 1))
        t = np.ones((s0, 1))
            
        while error > 1E-10:
            p = (X.T@t)/(t.T@t)
            p = p/np.linalg.norm(p,2)

            # Fix rotational ambiguity
            onez = np.ones([len(p),1]) # Use as a reference
            if p.T@onez < 0:
                p = -p

            t = (X@p)/(p.T@p)
            # Check t convergence --------------------
            error = sum(np.power((t-t_temp),2),0) # Squared error
            t_temp = t
            # ----------------------------------------     
        P[:,i] = np.squeeze(p)
        T[:,i] = np.squeeze(t)
        X = X - t@p.T
        
        # Sum of squares -----------
        Xhat = t@p.T
        ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
        # --------------------------    
        
    return T, P, SSX
