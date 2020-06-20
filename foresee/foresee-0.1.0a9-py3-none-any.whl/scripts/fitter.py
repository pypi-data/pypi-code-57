# -*- coding: utf-8 -*-
"""
fitter class
"""

import os
import sys
from sklearn.metrics import mean_absolute_error, mean_squared_error

# import local modules

from foresee.models.ewm import ewm_main, ewm_fit_forecast, ewm_tune
from foresee.models.fft import fft_main, fft_fit_forecast, fft_tune
from foresee.models.holt_winters import holt_winters_main, holt_winters_fit_forecast, holt_winters_tune
from foresee.models.prophet import prophet_main, prophet_fit_forecast, prophet_tune
from foresee.models.sarimax import sarimax_main, sarimax_fit_forecast, sarimax_tune

class fitter:
    """[summary]

    Returns
    -------
    [type]
        [description]
    """    
    FIT_MODELS = {
                    'ewm_model':        ewm_main,
                    'fft':              fft_main,
                    'holt_winters':     holt_winters_main,
                    'prophet':          prophet_main,
                    'sarimax':          sarimax_main,
                 }
    
    
    def __init__(self, model):
         self.model = model
         
    
    def fit(self, data_dict, param_config, model_params):
        """[summary]

        Parameters
        ----------
        data_dict : [type]
            [description]
        freq : [type]
            [description]
        forecast_len : [type]
            [description]
        model_params : [type]
            [description]
        run_type : [type]
            [description]
        tune : [type]
            [description]
        epsilon : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """        
        fit_model = self.FIT_MODELS[self.model]
        
        return fit_model(data_dict, param_config, model_params)
    
class tuner:
    
    TUNE_MODELS = {
                        'ewm_model':        ewm_tune,
                        'fft':              fft_tune,
                        'holt_winters':     holt_winters_tune,
                        'prophet':          prophet_tune,
                        'sarimax':          sarimax_tune,           
                    }
    
    def __init__(self, model):
        self.model = model
        
    def tune(self, ts_train, ts_test, params, args):
        
        tune_model = self.TUNE_MODELS[self.model]
        
        return tune_model(ts_train, ts_test, params, args)
    
    
    
class model_loss:
    
    FIT_MODELS = {
                        'ewm_model':        ewm_fit_forecast,
                        'fft':              fft_fit_forecast,
                        'holt_winters':     holt_winters_fit_forecast,
                        'prophet':          prophet_fit_forecast,           
                        'sarimax':          sarimax_fit_forecast,           
                    }
    
    def __init__(self, model):
        self.model = model
        
    def fit_loss(self, ts_train, ts_test, params=None, args=None):
        
        fit_model = self.FIT_MODELS[self.model]
        
        fcst_len = len(ts_test)
        
        fitted_values, yhat, err = fit_model(ts_train, fcst_len, params, args)
        
        if err is None:
            loss = mean_absolute_error(ts_test.values, yhat.values)
        else:
            loss = ts_test.abs().mean()
        
        
        return loss


    