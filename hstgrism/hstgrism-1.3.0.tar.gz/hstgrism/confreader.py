# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np

class ConfReader:
    '''
    ConfReader (using Python 3) reads aXe configuration files.
    obj = ConfReader(conffile) to assign the configuration file
    obj.conffile to see what file
    obj.readall() simply reads the whole file
    obj.getbeam(beam) extracts the beam info
    obj.beam to see the beam info
    obj.make_coef2d() re-constructs DYDX and DLDP
    obj.coef2d to see the coef re-construction
    NOTE: use np.astype(type) to convert after extraction
    NOTE: can feed coef2d into Polynomial2D package (pip install polynomial2d) for further analysis
        (i.e., given X1,X2 arrays and obj.coef2d, Polynomial2D().fit() can decompress from 2D coef to 1D coef)
    '''
    def __init__(self,conffile=None):
        self.conffile = conffile
        self.beam = None
        self.coef2d = None
    ##########
    ##########
    ##########
    def getbeam(self,beam='A'):
        #####
        # prepare keywords to read
        KEY = ['BEAM'+beam,'MMAG_EXTRACT_'+beam,'MMAG_MARK_'+beam,
               'DYDX_ORDER_'+beam,
               'XOFF_'+beam,'YOFF_'+beam,
               'DISP_ORDER_'+beam
              ]
        #####
        # open file and record value for each keyword
        f = open(self.conffile,'r')
        tmpp = {}
        tmpp['BEAM'] = beam
        for i,ii in enumerate(f.readlines()):
            tmp = ii.split(' ')[0]
            if tmp in KEY:
                tmppp = np.array(ii.split()[1:])
                tmpp[tmp] = tmppp
        f.close()
        #####
        # get DYDX_{beam}_{order} and DLDP_{beam}_{order}
        tmpkey = {'DYDX_ORDER_'+beam:'DYDX_{0}_'.format(beam),
                  'DISP_ORDER_'+beam:'DLDP_{0}_'.format(beam)
                 }
        for i in tmpkey:
            order = int(tmpp[i][0])
            for j in np.arange(order+1):
                string = tmpkey[i]+str(j)
                f = open(self.conffile,'r')
                for k,kk in enumerate(f.readlines()):
                    if string in kk.split(' '):
                        tmpp[string] = np.array(kk.split()[1:])
        #####
        # keep in self
        self.beam = tmpp
    ##########
    ##########
    ##########
    def readall(self):
        f = open(self.conffile,'r')
        for i,ii in enumerate(f.readlines()):
            print(i,ii.split())
    ##########
    ##########
    ##########
    def make_coef2d(self):
        beam = self.beam['BEAM']
        KEY = {'DYDX_ORDER_'+beam:'DYDX_{0}_'.format(beam),
               'DISP_ORDER_'+beam:'DLDP_{0}_'.format(beam)
              }
        tmpp = {}
        for i in KEY:
            order = int(self.beam[i][0])
            for j in np.arange(order+1):
                string = KEY[i]+str(j)
                tmp = self.beam[string]
                tmpp[string] = self._make_coef(tmp)
        self.coef2d = tmpp
    def _make_coef(self,coef):
        tmp = np.array(coef).astype(float)
        px1,px2,order = 0,0,0 # initialize
        out = {}
        out['NORDER'] = None
        out['COEF'] = {}
        for i in tmp:
            out['COEF'][(px1,px2)] = i
            px1-=1
            px2+=1
            if px1 < 0:
                order += 1
                px1 = order
                px2 = 0
        out['NORDER'] = order - 1
        return out
    
