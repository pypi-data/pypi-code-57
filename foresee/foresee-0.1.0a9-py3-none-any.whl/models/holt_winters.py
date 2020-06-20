"""
Holt-Winters from statsmodels
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from hyperopt import hp, fmin, tpe, Trials

# local module
from foresee.models import models_util
from foresee.models import param_optimizer
from foresee.scripts import fitter


def holt_winters_fit_forecast(ts, fcst_len, params=None, args=None):
    """[summary]

    Parameters
    ----------
    ts : [type]
        [description]
    fcst_len : [type]
        [description]
    freq : [type]
        [description]
    params : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    
    freq = args['FREQ']
    
    try:
        if params is None:
            hw_model = ExponentialSmoothing(
                                                endog = ts,
                                                seasonal_periods = freq
                                              ).fit(optimized=True)
        else:
            hw_model = ExponentialSmoothing(
                                                endog = ts,
                                                trend = params['trend'],
                                                seasonal = params['seasonal'],
                                                seasonal_periods = freq
                                              ).fit(optimized=True)
            
        hw_fittedvalues = hw_model.fittedvalues    

        hw_forecast = hw_model.predict(
                                            start = len(ts),
                                            end =   len(ts) + fcst_len - 1
                                        )
        err = None
        
    except Exception as e:
        hw_fittedvalues = None
        hw_forecast = None
        err = str(e)
    
    
    return hw_fittedvalues, hw_forecast, err


def holt_winters_tune(ts_train, ts_test, params=None, args=None):
    
    model = 'holt_winters'
    
    try:
        options = ['add', 'mul']
        space = {
                    'trend': hp.choice('trend', options),
                    'seasonal': hp.choice('seasonal', options)
                }
        
        f = fitter.model_loss(model)
        f_obj = lambda params: f.fit_loss(ts_train, ts_test, params, args)
        
        trials = Trials()
        best_raw = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=10, show_progressbar=False, verbose=False)
        best = {'trend': options[best_raw['trend']], 'seasonal': options[best_raw['seasonal']]}
        err = None
        
    except Exception as e:
        err = str(e)
        best = None
        
        
    return best, err


def holt_winters_main(data_dict, param_config, model_params):
    """[summary]

    Parameters
    ----------
    data_dict : [type]
        [description]
    freq : [type]
        [description]
    fcst_len : [type]
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

    model = 'holt_winters'
    fcst_len = param_config['FORECAST_LEN']
    output_format = param_config['OUTPUT_FORMAT']
    tune = param_config['TUNE']
    epsilon = param_config['EPSILON']  
    freq = param_config['FREQ']
    
    complete_fact = data_dict['complete_fact']
    
    # dataframe to hold fitted values
    fitted_fact = pd.DataFrame()
    fitted_fact['y'] = complete_fact['y']
    fitted_fact['data_split'] = complete_fact['data_split']
    
    # dataframe to hold forecast values
    forecast_fact = pd.DataFrame()
    forecast_fact['y'] = np.full(fcst_len, 0)
    forecast_fact['data_split'] = np.full(fcst_len, 'Forecast')
    
    fit_fcst_fact = pd.concat([fitted_fact, forecast_fact], ignore_index=True)
    
    args = dict()
    args['FREQ'] =  freq
    
    fit_args = dict()

    # no model competition    
    if output_format in ['all_models']:
        
        fitted_values, forecast, err = holt_winters_fit_forecast(
                                                                       ts = complete_fact['y'],
                                                                       fcst_len = fcst_len,
                                                                       params = None,
                                                                       args = args
                                                                  )
        if err is None:
            fit_fcst_fact['holt_winters_forecast'] = fitted_values.append(forecast).values
            
        else:
            fit_fcst_fact['holt_winters_forecast'] = 0
            
        fit_args['err'] = err
    
    
    # with model completition            
    if output_format in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            
            params, err = param_optimizer.tune(train_fact, test_fact, model, params=None, args=args)
            
            fit_args['tune_err'] = err
            
        else:
            params = None
            
        training_fitted_values, holdout_forecast, training_err = holt_winters_fit_forecast(
                                                                                                   ts = train_fact['y'],
                                                                                                   fcst_len = len(test_fact),
                                                                                                   params = params,
                                                                                                   args = args,
                                                                                         )
        
        complete_fitted_values, complete_forecast, complete_err = holt_winters_fit_forecast(
                                                                                                   ts = complete_fact['y'],
                                                                                                   fcst_len = fcst_len,
                                                                                                   params = params,
                                                                                                   args = args,
                                                                                         )
        
        if training_err is None and complete_err is None:
            hw_wfa = models_util.compute_wfa(
                                                y = test_fact['y'].values,
                                                yhat = holdout_forecast.values,
                                                epsilon = epsilon,
                                            )
            hw_fit_fcst = training_fitted_values.append(holdout_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['holt_winters_forecast'] = hw_fit_fcst.values
            fit_fcst_fact['holt_winters_wfa'] = hw_wfa
            
        else:
            hw_wfa = -1
            fit_fcst_fact['holt_winters_forecast'] = 0
            fit_fcst_fact['holt_winters_wfa'] = -1
            
        fit_args['err'] = (training_err, complete_err)
        fit_args['wfa'] = hw_wfa
        fit_args['params'] = params
        
        
    return fit_fcst_fact, fit_args




