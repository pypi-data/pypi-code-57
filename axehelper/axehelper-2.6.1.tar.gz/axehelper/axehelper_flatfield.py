# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from astropy.io import fits
import copy
import numpy as np

class AXEhelper_FlatField:
    '''
    AXEhelper_FlatField (using Python 3) computes a flatfield image in aXe definition.
    This can easily be implemented following the use of AXEhelper_computeTraceNWavelength.
    Given obj = AXEhelper_computeTraceNWavelength(...), and obj.compute() is called,
        a user can start with flat = AXEhelper_FlatField(flatfile,obj.wavelength['WW'])
    flat.flatfile to see the path to flatfile.
    flat.data to see inputs for the computation.
    flat.compute() to compute the flatfield image.
    flat.flatfield to see the flatfield image.
    '''
    def __init__(self,flatfile,ww):
        self.flatfile = flatfile
        self.data = {'WMIN':None,
                     'WMAX':None,
                     'FLAT':None,
                     'NAX1':None,
                     'NAX2':None,
                     'WW':ww
                    }
        self.flatfield = None
        try:
            self._get()
        except:
            pass
    def _get(self):
        tmp = fits.open(self.flatfile)
        wmin,wmax = tmp[0].header['WMIN'],tmp[0].header['WMAX']
        nax1,nax2 = tmp[0].header['NAXIS1'],tmp[0].header['NAXIS2']
        self.data['WMIN'] = wmin
        self.data['WMAX'] = wmax
        self.data['NAX1'] = nax1
        self.data['NAX2'] = nax2
        n = len(tmp)
        tmpp = {}
        for i in range(n):
            tmpp[i] = tmp[i].data.copy()
        self.data['FLAT'] = copy.deepcopy(tmpp)
    ##########
    ##########
    ##########
    def compute(self):
        # dimension test
        if self.data['WW'].shape[0] != self.data['NAX1']:
            raise ValueError('Dimension of WW != NAX1')
        # set parametric wavelength [0,1]
        wmin,wmax,ww = self.data['WMIN'],self.data['WMAX'],self.data['WW']
        paramww = (ww-wmin)/(wmax-wmin)
        paramww[paramww<0.] = 0.
        paramww[paramww>1.] = 1.
        paramww,tmp = np.meshgrid(paramww,np.arange(0,self.data['NAX2']))
        # compute
        tmp = self.data['FLAT']
        tmpp = np.full_like(paramww,0.,dtype=float)
        for i in tmp:
            tmpp += tmp[i] * np.power(paramww,i)
        self.flatfield = tmpp.copy()
    