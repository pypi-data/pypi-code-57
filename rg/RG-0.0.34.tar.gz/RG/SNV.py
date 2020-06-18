# Standard Normal Variate

import numpy as np
from numpy import matlib as mb

def SNV(x):
    ''' 
    
    SNV: standard normal variate
    [X_snv] = snv(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_snv [n x k] 
        preprocessed spectra
    
    '''
    
    [m,n]=x.shape
    rmean=np.mean(x,1)
    rmean = (rmean[np.newaxis]).T
    dr=x-mb.repmat(rmean,1,n)
    drsum = np.sqrt(np.sum(dr**2,1)/(n-1))
    drsum = (drsum[np.newaxis]).T
    x_snv=dr/np.matlib.repmat(drsum,1,n)
    
    return x_snv