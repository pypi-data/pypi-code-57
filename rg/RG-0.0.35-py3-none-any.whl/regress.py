# MLR regression

import numpy as np
import statsmodels.api as sm
import pandas as pd

def regress(y, X):

    model = sm.OLS(y, X).fit()
    b = model.params
    b_int = model.conf_int(0.05)

    print('betas and confidence intervals')
        
    #out = pd.DataFrame({'low': b_int[:,0], 'b': b, 'high': b_int[:,1]})
    #print(out)
    
    b = (b[np.newaxis]).T # Vector format for output
    
    R2 = model.rsquared
    F = model.fvalue
    p = model.f_pvalue
    
    return b, b_int, model, R2, F, p