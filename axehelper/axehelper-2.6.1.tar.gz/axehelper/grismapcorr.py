# Kornpob Bhirombhakdi 20200331

import numpy as np
from scipy.interpolate import interp2d
import copy

class GrismApCorr:
    """
    GrismApCorr is a class containing tables for aperture correction (i.e., apcorr = f(wavelength, apsize)) in aXe reduction. These tables are from ISRs. Interpolaton model is also prepared.
    x = GrismApCorr()
    x.table = show apcorr tables with keys as intrument codes. Use x.instrument to check which instrument is available.
    x.instrument = show available instrument codes
    x.table[instrument]['model'](wave,apsize) = calculate apcorr given a model corresponding to its instrument, wavelength, and aperture size.
    """    
    def __init__(self):
        ##########
        # Tables from ISRs
        TABLE = {'HST-WFC3-IR-G102': 
                 {'ref': 'ISR WFC3-2011-05'
                  ,'filter': 'G102'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.128,0.385,0.641
                                       ,0.898,1.154,1.411
                                       ,1.667,1.924,3.719
                                       ,7.567,12.954,25.779
                                      ))
                  ,'waveunit': 'A'
                  ,'wave': np.array((8850.,9350.,9850.,10350.,10850.,11350.))
                  ,'value' : np.array(((0.459,0.391,0.414,0.464,0.416,0.369)
                                      ,(0.825,0.809,0.808,0.811,0.794,0.792)
                                      ,(0.890,0.889,0.887,0.880,0.875,0.888)
                                      ,(0.920,0.917,0.916,0.909,0.904,0.916)
                                      ,(0.939,0.937,0.936,0.930,0.925,0.936)
                                      ,(0.952,0.950,0.950,0.943,0.940,0.949)
                                      ,(0.962,0.961,0.961,0.954,0.951,0.958)
                                      ,(0.969,0.968,0.969,0.962,0.959,0.965)
                                      ,(0.985,0.984,0.986,0.982,0.980,0.983)
                                      ,(0.995,0.995,0.996,0.991,0.990,0.992)
                                      ,(0.999,0.999,0.999,0.997,0.996,0.995)
                                      ,(1.000,1.000,1.000,1.000,1.000,1.000)
                                     ))
                  ,'model': None
                 }
                 ,'HST-WFC3-IR-G141':
                 {'ref': 'ISR WFC3-2011-05'
                  ,'filter': 'G141'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.128,0.385,0.641
                                       ,0.898,1.154,1.411
                                       ,1.667,1.924,3.719
                                       ,7.567,12.954,25.779
                                      ))   
                  ,'waveunit': 'A'
                  ,'wave': np.array((11300.,12300.,13300.,14300.,15300.,16300.))
                  ,'value': np.array(((0.442,0.444,0.395,0.344,0.342,0.376)
                                     ,(0.805,0.792,0.764,0.747,0.732,0.732)
                                     ,(0.866,0.877,0.865,0.863,0.850,0.859)
                                     ,(0.912,0.901,0.893,0.894,0.884,0.898)
                                     ,(0.933,0.924,0.914,0.913,0.903,0.913)
                                     ,(0.947,0.940,0.931,0.932,0.921,0.932)
                                     ,(0.958,0.950,0.942,0.944,0.934,0.945)
                                     ,(0.966,0.959,0.951,0.953,0.944,0.954)
                                     ,(0.985,0.984,0.981,0.985,0.980,0.985)
                                     ,(0.993,0.995,0.992,0.997,0.992,0.996)
                                     ,(0.996,0.998,0.997,1.000,0.997,1.000)
                                     ,(1.000,1.000,1.000,1.000,1.000,1.000)
                                    ))
                  ,'model': None
                 }
                 ,'HST-WFC3-UVIS1-G280':
                 {'ref': 'ISR WFC3-2009-01'
                  ,'filter': 'G280'
                  ,'scale': 0.04
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.04,0.12,0.20,
                                       0.28,0.36,0.44,
                                       0.52,0.60,1.16,
                                       2.36,4.04,8.04
                                      ))   
                  ,'waveunit': 'A'
                  ,'wave': np.array((2275.,2825.,3375.,3925.,4475.,5025.))
                  ,'value': np.array(((0.312,0.312,0.276,0.258,0.261,0.241)
                                     ,(0.720,0.706,0.676,0.642,0.600,0.589)
                                     ,(0.856,0.848,0.839,0.815,0.767,0.769)
                                     ,(0.903,0.899,0.897,0.882,0.840,0.855)
                                     ,(0.926,0.926,0.926,0.913,0.875,0.895)
                                     ,(0.939,0.942,0.944,0.933,0.898,0.916)
                                     ,(0.947,0.951,0.956,0.947,0.915,0.931)
                                     ,(0.953,0.957,0.963,0.956,0.928,0.944)
                                     ,(0.974,0.978,0.983,0.978,0.960,0.973)
                                     ,(0.990,0.992,0.994,0.991,0.983,0.989)
                                     ,(0.995,0.997,0.998,0.997,0.994,0.996)
                                     ,(1.000,1.000,1.000,1.000,1.000,1.000)
                                    ))
                  ,'model': None
                 }
                 ,'HST-ACS-WFC-G800L':
                 {'ref': 'ISR WFC3-2011-05'
                  ,'filter': 'G102'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'diameter'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.128,0.385,0.641
                                       ,0.898,1.154,1.411
                                       ,1.667,1.924,3.719
                                       ,7.567,12.954,25.779
                                      ))
                  ,'waveunit': 'A'
                  ,'wave': np.array((8850.,9350.,9850.,10350.,10850.,11350.))
                  ,'value' : np.array(((0.459,0.391,0.414,0.464,0.416,0.369)
                                      ,(0.825,0.809,0.808,0.811,0.794,0.792)
                                      ,(0.890,0.889,0.887,0.880,0.875,0.888)
                                      ,(0.920,0.917,0.916,0.909,0.904,0.916)
                                      ,(0.939,0.937,0.936,0.930,0.925,0.936)
                                      ,(0.952,0.950,0.950,0.943,0.940,0.949)
                                      ,(0.962,0.961,0.961,0.954,0.951,0.958)
                                      ,(0.969,0.968,0.969,0.962,0.959,0.965)
                                      ,(0.985,0.984,0.986,0.982,0.980,0.983)
                                      ,(0.995,0.995,0.996,0.991,0.990,0.992)
                                      ,(0.999,0.999,0.999,0.997,0.996,0.995)
                                      ,(1.000,1.000,1.000,1.000,1.000,1.000)
                                     ))
                  ,'model': None
                 }
                }
        ##########
        self.table = TABLE
        self.instrument = list(TABLE.keys())
        self.make_model()
##########
##########
##########

    def make_model(self):
        for i in self.instrument:
            apsize = 0.5 * np.copy(self.table[i]['apsize'])
            wave = np.copy(self.table[i]['wave'])
            value = np.copy(self.table[i]['value'])
            model = interp2d(wave,apsize,value,kind='linear',copy=True
                             ,bounds_error=False,fill_value=np.nan
                            )
            self.table[i]['model'] = copy.deepcopy(model)
    def make_apcorr(self,instrument,wave,apsize,apunit='pix'
                    ,replace='median'
                   ):
        apunittab = self.table[instrument]['apunit']
        model = self.table[instrument]['model']
        apsize2 = None
        value = None
        if (apunittab=='arcsec') & (apunit=='pix'):
            apsize2 = self.pix2arcsec(instrument,apsize)
        elif (apunittab=='pix') & (apunit=='arcsec'):
            apsize2 = self.arcsec2pix(instrument,apsize)
        value = model(wave,apsize2)
        if replace=='median':
            median = np.median(value[np.where(np.isfinite(value))])
            value[np.where(~np.isfinite(value))] = median
        value[np.where(value <= 0.)] = 0.
        value[np.where(value >= 1.)] = 1.        
        return value
    def pix2arcsec(self,instrument=None,pixsize=None):
        out = None
        if not instrument:
            print('Error: instrument is required. Set to None')
            return
        if not pixsize:
            print('Error: pixsize is required. Set to None')
            return
        scale = self.table[instrument]['scale']
        scaleunit = self.table[instrument]['scaleunit']
        if scaleunit=='arcsec/pix':
            out = pixsize * scale
        elif scaleunit=='pix/arcsec':
            out = pixsize.astype(float) / scaleunit
        else:
            print('Error: invalid scaleunit. Set to None')
        return out
    def arcsec2pix(self,instrument=None,arcsec=None):
        out = None
        if not instrument:
            print('Error: instrument is required. Set to None')
            return
        if not arcsec:
            print('Error: arcsec is required. Set to None')
        scale = self.table[instrument]['scale']
        scaleunit = self.table[instrument]['scaleunit']
        if scaleunit=='arcsec/pix':
            out = arcsec.astype(float) / scale
        elif scaleunit=='pix/arcsec':
            out = arcsec.astype(float) * scale
        else:
            print('Error: invalid scaleunit. Set to None')
        return out
