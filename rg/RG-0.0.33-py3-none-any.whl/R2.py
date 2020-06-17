# Calculate R2 for MLR model

import numpy as np

def R2(y,yhat):
    # R2 in calibration
    n = y.shape[0]
    ym = np.ones((n,1))*np.mean(y) # Vector form
    SSr = np.sum((yhat-ym)**2)
    SSe = np.sum((y-yhat)**2)
    SSt = sum((y-ym)**2)
    
    R2 = 1 - SSe / SSt
    
    return R2