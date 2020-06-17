# Kornpob Bhirombhakdi 20200331

import numpy as np
import pandas as pd

def axeapcorr(aXeSPCdata,apcorrmod,outputpath=None):
    """
    Input:
      aXeSPCdata = data from SPC or opt.SPC output files from aXe reduction. 
      apcorrmod = model for aperture correction (i.e., apcorr = f(wavelength, apsize)). 
      outputpath = filepath to save output from axeapcorr.
    Output: csv file saved to outputpath. Output is aperture-size corrected.
    ##########
    axeapcorr performs aperture correction of the SPC or opt.SPC outputs from aXe reduction, and saves the results to a specified path. Aperture corrections for aXe are tables presented in ISRs. These tables are wrapped in grismapcorr.py.
    """
    # set up variables
    x = aXeSPCdata
    lamb = x['LAMBDA']
    flux = x['FLUX']
    eflux = x['FERROR']
    tcount = x['TCOUNT']
    weight = x['WEIGHT']
    dlambda = x['DLAMBDA']
    apsize = (weight/2.) * 0.13 # 0.13 is pixel scale of WFC3/IR
    
    # calculate aperture correction
    APCORR = []
    for i,ii in enumerate(lamb):
        tmp = apcorrmod(lamb[i],apsize[i])
        APCORR.append(tmp[0])
    APCORR = np.array(APCORR)
    
    # perform correction
    tmpp,etmpp = flux/APCORR,eflux/APCORR
    tmppp = tcount/APCORR/dlambda
    
    # prepare output
    out =  {'APCORR': APCORR,
            'FLUX': tmpp,
            'FLUX_ORIG': flux,
            'FERROR': etmpp,
            'TCOUNT': tmppp,
            'TCOUNT_ORIG': tcount,
            'TERROR': None,
            'U_TCALIB': 'count_unit / A',
            'U_TORIG': 'count_unit / pix',
            'DLAMBDA': dlambda,
            'U_DLAMBDA': 'A / pix',
            'LAMBDA': lamb}
    
    # save output
    _axeapcorrsave(out,outputpath)
    return out

def _axeapcorrsave(out,outputpath):
    if not outputpath:
        outputpath = 'axeapcorrsave.csv'
    pd.DataFrame(out).to_csv(outputpath)
