"""
SARIMAX from statsmodels
"""


import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import statsmodels.api
from hyperopt import hp, fmin, tpe, Trials

# local module
from foresee.models import models_util
from foresee.models import param_optimizer
from foresee.scripts import fitter


def sarimax_fit_forecast(ts, fcst_len, params=None, args=None):
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

    try:
        if params is None:
            sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                        endog = ts,
                                                                        enforce_stationarity = False,
                                                                        enforce_invertibility = False,
                                                                   ).fit(disp=0)
        else:
            freq = args['FREQ']
            order = (params['p'], params['d'], params['q'])
            seasonal_order = (params['cp'], params['cd'], params['cq'], freq)
            
            sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                        endog = ts,
                                                                        order = order,
                                                                        seasonal_order = seasonal_order,
                                                                        enforce_stationarity = True,
                                                                        enforce_invertibility = True,
                                                                   ).fit(disp=0)
            
        
        sarimax_fittedvalues = sarimax_model.fittedvalues
        sarimax_forecast = sarimax_model.predict(
                                                    start = len(ts),
                                                    end = len(ts) + fcst_len - 1,
                                                 )
        err = None
        
    except Exception as e:
        
        sarimax_model = None
        sarimax_fittedvalues = None
        sarimax_forecast = None
        err = str(e)
        
    return sarimax_fittedvalues, sarimax_forecast, err

def sarimax_tune(ts_train, ts_test, params=None, args=None):
    
    model = 'sarimax'
    
    if params is None:
        space = {
                    'p': hp.randint('p', 5),
                    'd': hp.randint('d', 3),
                    'q': hp.randint('q', 5),
                    'cp': hp.randint('cp', 3),
                    'cd': hp.randint('cd', 2),
                    'cq': hp.randint('cq', 3),
                }
    else:
        try:
            max_p = params['p']
            max_d = params['d']
            max_q = params['q']
            max_cp = params['cp']
            max_cd = params['cd']
            max_cq = params['cq']
            
            space = {
                        'p': hp.randint('p', max_p),
                        'd': hp.randint('d', max_d),
                        'q': hp.randint('q', max_q),
                        'cp': hp.randint('cp', max_cp),
                        'cd': hp.randint('cd', max_cd),
                        'cq': hp.randint('cq', max_cq),
                    }
        except:
            space = {
                        'p': hp.randint('p', 5),
                        'd': hp.randint('d', 3),
                        'q': hp.randint('q', 5),
                        'cp': hp.randint('cp', 3),
                        'cd': hp.randint('cd', 2),
                        'cq': hp.randint('cq', 3),
                    }
        
    try:
        f = fitter.model_loss(model)
        f_obj = lambda params: f.fit_loss(ts_train, ts_test, params, args)
        
        trials = Trials()
        best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=100, show_progressbar=False, verbose=False)
        
        err = None
        
    except Exception as e:
        err = str(e)
        best = None
        print(err)
        
    return best, err


def sarimax_main(data_dict, param_config, model_params):
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
    """    

    model = 'sarimax'
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
    args['FREQ'] = freq
    
    fit_args = dict()
    
    # no model competition
    if output_format in ['all_models']:
        
        sarimax_fitted_values, sarimax_forecast, err = sarimax_fit_forecast(
                                                                            ts = complete_fact['y'],
                                                                            fcst_len = fcst_len,
                                                                            params = None,
                                                                            args = None,
                                                                        )
        
        if err is None:
            fit_fcst_fact['sarimax_forecast'] = sarimax_fitted_values.append(sarimax_forecast).values
            
        else:
            fit_fcst_fact['sarimax_forecast'] = 0
            
        fit_args['err'] = err
    
    # with model completition            
    elif output_format in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            param_space = model_params[model]
            params, err = param_optimizer.tune(train_fact, test_fact, model, params=param_space, args=args)
            fit_args['err'] = err
            
        else:
            # TODO: accept params set by user
            params = None
            
        training_fitted_values, training_forecast, training_err = sarimax_fit_forecast(
                                                                                        ts = train_fact['y'],
                                                                                        fcst_len = len(test_fact),
                                                                                        params = params,
                                                                                        args = args,
                                                                                    )
        
        complete_fitted_values, complete_forecast, complete_err = sarimax_fit_forecast(
                                                                                        ts = complete_fact['y'],
                                                                                        fcst_len = fcst_len,
                                                                                        params = params,
                                                                                        args = args,
                                                                                    )
        
#        if 'enforce_stationarity' in complete_err or '' in complete_err:
#            
#            # run without enforcement
#        
#        #TODO: if failed with 'enforce_stationarity' or 'enforce_invertibility' at complete fcst, set these to false
        
        if training_err is None and complete_err is None:
            sarimax_wfa = models_util.compute_wfa(
                                                    y = test_fact['y'].values,
                                                    yhat = training_forecast.values,
                                                    epsilon = epsilon,
                                                )
            sarimax_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['sarimax_forecast'] = sarimax_fit_fcst.values
            fit_fcst_fact['sarimax_wfa'] = sarimax_wfa
            
        else:
            sarimax_wfa = -1
            fit_fcst_fact['sarimax_forecast'] = 0
            fit_fcst_fact['sarimax_wfa'] = -1
            
        fit_args['err'] = (training_err, complete_err)
        fit_args['wfa'] = sarimax_wfa
        fit_args['params'] = params
            
            
    return fit_fcst_fact, fit_args
