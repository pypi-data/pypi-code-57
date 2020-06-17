# Autoscale: center and scale to unit variance

import numpy as np

def autoscale(X):
    '''
    
    Autoscale: center and scale to unit variance
    [X_auto, mX, sX] = autoscale(X)
    
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
    sX [1 x k] 
        standard deviation of all variables        
    
    '''
    
    m,n = X.shape
    mx = np.nanmean(X, axis=0)
    stdx = np.nanstd(X, axis=0)
    ax = (X - mx)/stdx
    
    # Remove NaN values occuring when std = 0
    for i in range(1,m):
        for j in range(1,n):
            if np.isnan(ax[i,j]) == 1:
                ax[i,j] = 0
    
    mx = mx[np.newaxis]
    stdx = stdx[np.newaxis]
    
    return ax, mx, stdx