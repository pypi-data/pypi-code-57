# Kornpob Bhirombhakdi 20200331

from astropy.io import fits
import numpy as np

def order_flist(flist,key=None):
    """
    Input:
      flist = flt.fits file list
      key = keyword from PRIMARY hdu for ordering
    Output: a list of filenames ordered by using key
    ##########
    If not key, key = 'EXPSTART' by default
    """
    if not key:
        key = 'EXPSTART'
    tmp = []
    for i,ii in enumerate(flist):
        x = fits.open(ii)
        tmpp = x[0].header[key]
        tmp.append(tmpp)
    order = np.argsort(tmp)
    return np.array(flist)[order]
