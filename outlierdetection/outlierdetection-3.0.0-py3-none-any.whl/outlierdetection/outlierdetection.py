# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
from scipy.signal import savgol_filter

def outlierdetection(data,method):
    """
    # outlierdetection detects outliers given data and method.
    # method = dictionary where good data is defined.
    # data = array of data
    # return a mask (i.e., boolean array parallel to data) with True for good data.
    #####
    # method = {'name': 'method_name',
    #           'rule': dictionary}
    #####
    # General rule description:
    #   initmask = array parallel to data with True for good data to initialize the process
    #              if not specified, set all data as good (True)
    #   keepneg = False for rejecting all negatives, True otherwise
    #   niter = integer for number of iterations
    #   noise = array parallel to data specifying noise
    #####
    # Global Median Clipping
    # method = {'name':'median',
    #           'rule': {'minp':minp, 'maxp':maxp, 'niter':niter, 'initmask':initmask}
    #          }
    # where [minp*median, maxp*median] defines good data (inclusive both sides) 
    # and median iteratively defined by good data
    # Note: global median clipping is good for global detection given some knowledge about global boundaries.
    # For example, you know that good data varied between 0.1*median and 10.*median.
    #####
    # Global Sigma Clipping
    # method = {'name': 'sigma',
    #           'rule': {'minp':minp, 'maxp':maxp, 'niter':niter, 'initmask':initmask} 
    #          }
    # where [median - minp*std, median + maxp*std] defines good data (inclusive both sides)
    # where, respectively, median and std are median and standard deviation defined by good data iteratively.
    # Note: global sigma clipping is good for examining outliers using global variation.
    #####
    # Local Sigma Clipping
    # method = {'name':'sigmalocal',
    #           'rule': {'sigma':sigma, 'noise':noise, 'keepneg':True, 'niter':niter, 'initmask':initmask, 'params':dictionary}
    #          }
    # where ratio <= sigma defines good data
    # where ratio = (data - median) / noise
    # and if 'keepneg':True, ratio = np.abs(ratio)
    # where median = savgol_filter(data,**params)
    #####
    # Signal-to-Noise Clipping
    # method = {'name': 'sn',
    #           'rule': {'minp':minp, 'noise':noise, 'keepneg':True}
    #          }
    # for calculating SN = data / noise
    # if 'keepneg':True, SN = np.abs(SN)
    # good data has SN >= minp
    # Note: SN clipping is examining individual variation, and data quality control.
    ##########
    """
    import numpy as np
    ##########
    # 0. Input
    data = np.array(data)
    methodname = method['name']
    rule = method['rule']
    try:
        mask = rule['initmask'].copy()
        if not mask:
            mask = np.full_like(data,True,dtype=bool)
            rule['initmask'] = mask.copy()
    except:
        mask = np.full_like(data,True,dtype=bool)
        rule['initmask'] = mask.copy()
    ##########
    # 1. Compute
    if methodname in {'median','sigma'}:
        minp,maxp = rule['minp'],rule['maxp']
        niter = rule['niter']
        for i in range(niter):
            gooddata = data[mask] # good data
            ### median or sigma
            if methodname=='median':
                median = np.median(gooddata)
                minbound = minp*median
                maxbound = maxp*median
            elif methodname=='sigma':
                std = np.std(gooddata)
                median = np.median(gooddata)
                minbound = median - minp*std
                maxbound = median + maxp*std
            ### update mask
            m = np.argwhere((data >= minbound) & (data <= maxbound)).flatten() # good data
            mask = np.full_like(data,False,dtype=bool)
            mask[m] = True
            print('{0} iter {1}'.format(methodname,i))
    elif methodname == 'sn':
        minp = rule['minp']
        noise = rule['noise']
        keepneg = rule['keepneg']
        sn = data / noise
        if keepneg:
            sn = np.abs(sn)
        m = np.argwhere(sn >= minp).flatten()
        mask = np.full_like(data,False,dtype=bool)
        mask[m] = True
        print('{0} complete'.format(methodname))
    elif methodname == 'sigmalocal':
        sigma = rule['sigma']
        noise = rule['noise']
        keepneg = rule['keepneg']
        niter = rule['niter']
        params = rule['params']
        for i in range(niter):
            tmpdata = data[mask]
            tmpmedian = savgol_filter(tmpdata,**params)
            tmpnoise = noise[mask]
            ratio = (tmpdata - tmpmedian)/tmpnoise
            if keepneg:
                ratio = np.abs(ratio)
            m = np.argwhere(ratio > sigma).flatten()
            mask[m] = False
            print('{0} iter {1}'.format(methodname,i))
    else:
        raise ValueError('method {0} does not support'.format(method))
    ##########
    # 2. Update with the initial mask and return
    return mask & rule['initmask']
