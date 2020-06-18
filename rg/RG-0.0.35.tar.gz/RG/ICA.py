# ICA: independent component analysis

import numpy as np

def ICA(X):
    
    # X must be centered

    [D, E] = np.linalg.eig(X.T@X)
    D = D*np.eye(len(D))
    Dinv = np.linalg.pinv(D)
    P = E@np.sqrt(Dinv)@E.T
    T = X@P 
    
    return T,P