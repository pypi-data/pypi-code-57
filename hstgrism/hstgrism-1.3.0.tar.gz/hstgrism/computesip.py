# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from polynomial2d.polynomial2d import Polynomial2D

class ComputeSIP:
    '''
    ComputeSIP (using Python 3) chains from ConfReader to compute SIP using Polynomial2D package (pip install polynomial2d).
    conf = ConfReader() with conf.coef2d corrently constructed.
    obj = ComputeSIP(conf.coef2d,x1=xref,x2=yref) to instantiate (NOTE: x1 is the leading term in SIP).
    obj.coef2d contains the same conf.coef2d
    obj.x1,obj.x2 contains xref,yref
    obj.compress() to compress to 1D coef
    self.coef1d to see the 1D coef
    '''
    def __init__(self,coef2d=None,x1=None,x2=None):
        self.coef2d = coef2d
        self.x1 = x1
        self.x2 = x2
    def compress(self):
        out = {}
        for i in self.coef2d:
            tmp = self.coef2d[i]   
            obj = Polynomial2D()
            obj.model['NORDER'] = tmp['NORDER']
            obj.model['COEF'] = tmp['COEF']
            obj.data['X1'] = self.x1
            obj.data['X2'] = self.x2
            obj.compute()
            out[i] = obj.model['YFIT']
        self.coef1d = out           
