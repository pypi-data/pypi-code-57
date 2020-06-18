#%% Center 

import numpy as np

def center(X):
    '''
    
    Center: center data
    [X_auto, mX] = center(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_auto [n x k] 
        preprocessed spectra
    mX [1 x k] 
        mean of all variables     
    
    '''
    
    m,n = X.shape
    mx = np.nanmean(X, axis=0)
    ax = (X - mx)
    
    mx = mx[np.newaxis]
    
    return ax, mx