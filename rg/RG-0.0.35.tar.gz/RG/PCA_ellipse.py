# 95% Confidence Inerval Ellipse on PCA scores


import numpy as np
from scipy import stats


def PCA_ellipse(T):

    N = T.shape[0]
    nbPC = T.shape[1]
    Fdf1 = nbPC
    Fdf2 = N-nbPC
    T2_95 = nbPC*(N-1)/(N-nbPC)*stats.f.ppf(0.95,Fdf1,Fdf2)
    
    u = 0     #x-position of the center
    v = 0    #y-position of the center
    a = np.sqrt(np.var(T[:,0]) * T2_95)      #radius on the x-axis
    b = np.sqrt(np.var(T[:,1]) * T2_95)    #radius on the y-axis
    
    t = np.linspace(0, 2*np.pi, 100)
    H = u+a*np.cos(t)
    V = v+b*np.sin(t)
    
    H = H[np.newaxis].T
    V = V[np.newaxis].T
    
    Tellipse = np.concatenate((H,V),axis=1)
    
    return Tellipse
