# Detrend: Perform spectral detrending to remove linear trend from data

import scipy

def detrend(spectra):
    '''
    
    Detrend: Perform spectral detrending to remove linear trend from data
    [X_detrend] = detrend(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_detrend [n x k] 
        preprocessed spectra      
    
    '''
    
    return scipy.signal.detrend(spectra, bp=0)