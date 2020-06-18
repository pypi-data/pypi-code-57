# Linear baseline removal (remove the mean of each spectrum)

import numpy as np

def baseline(spectra):
    '''
    
    Linear baseline removal (remove the mean of each spectrum)
    [X_baseline] = baseline(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_baseline [n x k] 
        preprocessed spectra       
    
    '''
    
    spectra = spectra.T
    spectra = spectra - np.mean(spectra, axis=0)
    spectra = spectra.T
    return spectra