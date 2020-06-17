# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
from scipy.integrate import quad

class ComputeTraceNWavelength:
    '''
    ComputeTraceNWavelength (using Python 3) computes trace and wavelength in HST/aXe definition.
    This class can be easily used following ComputeSIP.
    Given obj = ComputeSIP(conf.coef2d,xref,yref), simply call
        newobj = ComputeTraceNWavelength(obj.coef1d,obj.x1,obj.x2,nax1,nax2)
        where nax1,nax2 = dimension of a grism image.
    newobj.data to see input parameters.
    newobj.compute() to compute trace and wavelength.
    newobj.trace to see trace
    newobj.wavelength to see wavelength (in A)
    '''
    def __init__(self,coef1d=None,x1ref=None,x2ref=None,
                 nax1=None,nax2=None
                ):
        self.data = {'COEF1D':coef1d,
                     'X1REF':x1ref,
                     'X2REF':x2ref,
                     'NX1':nax1,
                     'NX2':nax2,
                    }
        self.trace = None
        self.wavelength = None
    ##########
    ##########
    ##########
    def compute(self):
        # trace
        xg = np.arange(self.data['NX1'])
        delx = xg - self.data['X1REF']
        dydx = self._get_coef('DYDX')
        tmp = 0.
        for i,ii in enumerate(dydx):
            tmp += ii * np.power(delx,i)
        self.trace = {'XG':xg,
                      'YG':tmp.copy() + self.data['X2REF']
                     }
        # wavelength
        dydx = self._get_coef('DYDX')
        dldp = self._get_coef('DLDP')
        varclength = np.vectorize(self._arclength)
        arc,earc = np.array(varclength(delx,*dydx))
        tmp = 0.
        for i,ii in enumerate(dldp):
            tmp += ii * np.power(arc,i)
        self.wavelength = {'XG':xg,
                           'WW':tmp.copy()
                          }
    def _get_coef(self,key):
        coef1d = self.data['COEF1D']
        tmp = {}
        for i in coef1d:
            if i.split('_')[0] == key:
                tmp[int(i.split('_')[2])] = coef1d[i]
        n = len(tmp)
        dydx = []
        for i in range(n):
            dydx.append(tmp[i])
        return dydx
    def _arclength_integrand(self,Fa,*coef):
        # compute np.sqrt(1 + np.power(dydx,2))
        # dy = sum(i=0,i=n,DYDX_A_i*np.power(dx,i))
        # dydx = (dy/dx) = sum(i=0,i=n,i*DYDX_A_i*np.power(dx,i-1))
        # Fa = dx
        # coef = [DYDX_A_0,DYDX_A_1,...]
        s = 0
        for i,ii in enumerate(coef):
            if i==0:
                continue
            s += i * ii * np.power(Fa,i-1)
        return np.sqrt(1. + np.power(s,2))
    def _arclength(self,Fa,*coef):
        # compute integrate(from 0,to Fa,integrand np.sqrt(1 + np.power(dydx,2)))
        integral,err = quad(self._arclength_integrand, 0., Fa, args=coef)
        return integral,err 
