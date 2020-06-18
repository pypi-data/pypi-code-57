# MSC: Multiplicative scatter correction
# https://nirpyresearch.com/two-scatter-correction-techniques-nir-spectroscopy-python/

import numpy as np

def MSC(input_data):
    ''' 
    MSC: Multiplicative scatter correction
    [X_msc,reference] = msc(X,reference)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_msc [n x k] 
        preprocessed spectra
    
    '''
    
    
    
    # mean centre correction
    for i in range(input_data.shape[0]):
        input_data[i,:] -= input_data[i,:].mean()
    
    # Get the reference spectrum : calculate mean
    ref = np.mean(input_data, axis=0)    
        
    # Define a new array and populate it with the corrected data    
    data_msc = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        # Run regression
        fit = np.polyfit(ref, input_data[i,:], 1, full=True)
        # Apply correction
        data_msc[i,:] = (input_data[i,:] - fit[0][1]) / fit[0][0] 
    
    ref = ref[np.newaxis]
    return (data_msc,ref) 
