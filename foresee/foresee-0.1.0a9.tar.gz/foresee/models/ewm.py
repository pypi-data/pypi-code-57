"""
Exponentially Weighted Mean
"""

import numpy as np
import pandas as pd
from hyperopt import hp, fmin, tpe, Trials

# local module
from foresee.models import models_util
from foresee.models import param_optimizer
from foresee.scripts import fitter


def ewm_fit_forecast(ts, fcst_len, params=None, args=None):
    """[summary]

    Parameters
    ----------
    ts : [type]
        [description]
    fcst_len : [type]
        [description]
    span : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    try:
        alpha = params['alpha']
        
        ewm_model = ts.ewm(alpha=alpha)
        ewm_fittedvalues = ewm_model.mean()
        
        ewm_forecast = np.full(fcst_len, ewm_fittedvalues.iloc[-1])
        ewm_forecast = pd.Series(ewm_forecast)
        err = None

    except Exception as e:
        
        ewm_fittedvalues = None
        ewm_forecast = None
        err = str(e)
        
    return ewm_fittedvalues, ewm_forecast, err


def ewm_tune(ts_train, ts_test, params=None, args=None):
    
    model = 'ewm_model'
    
    try:
        
        space = hp.uniform('alpha', 0, 1)
        
        f = fitter.model_loss(model)
        
        f_obj = lambda params: f.fit_loss(ts_train, ts_test, params=None, args=None)
        
        trials = Trials()
        
        best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=100, show_progressbar=False, verbose=False)
        
        err = None
        
    except Exception as e:
        err = str(e)
        best = None
        
    return best, err
    


def ewm_main(data_dict, param_config, model_params):
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

    model = 'ewm_model'
    fcst_len = param_config['FORECAST_LEN']
    output_format = param_config['OUTPUT_FORMAT']
    tune = param_config['TUNE']
    epsilon = param_config['EPSILON']
    
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
    
    # no model competition
    if output_format in ['all_models']:
        
        params = {'alpha': 0.5}
        ewm_fitted_values, ewm_forecast, err = ewm_fit_forecast(
                                                                    ts = complete_fact['y'],
                                                                    fcst_len = fcst_len,
                                                                    params = params,
                                                                )
        
        if err is None:
            fit_fcst_fact['ewm_model_forecast'] = ewm_fitted_values.append(ewm_forecast).values
            
        else:
            fit_fcst_fact['ewm_model_forecast'] = 0
            
        args['err'] = err
        args['alpha'] = params['alpha']
            
            
    # with model completition            
    if output_format in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            opt_params, err = param_optimizer.tune(train_fact, test_fact, model)
            args['err'] = err
            
        else:
            opt_params = {'alpha': 0.5}
            
        training_fitted_values, training_forecast, training_err = ewm_fit_forecast(
                                                                                    ts = train_fact['y'],
                                                                                    fcst_len = len(test_fact) ,
                                                                                    params = opt_params
                                                                                )
        
        complete_fitted_values, complete_forecast, complete_err = ewm_fit_forecast(
                                                                                    ts = complete_fact['y'],
                                                                                    fcst_len = fcst_len,
                                                                                    params = opt_params
                                                                                )
        
        if training_err is None and complete_err is None:
            ewm_wfa = models_util.compute_wfa(
                                                y = test_fact['y'].values,
                                                yhat = training_forecast.values,
                                                epsilon = epsilon,
                                            )
            ewm_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['ewm_model_forecast'] = ewm_fit_fcst.values
            fit_fcst_fact['ewm_model_wfa'] = ewm_wfa
            
        else:
            ewm_wfa = -1
            fit_fcst_fact['ewm_model_forecast'] = 0
            fit_fcst_fact['ewm_model_wfa'] = ewm_wfa
            
        args['err'] = (training_err, complete_err)
        args['wfa'] = ewm_wfa
        
        try:
            args['alpha'] = opt_params['alpha']
        except:
            args['alpha'] = None
            
            
    return fit_fcst_fact, args
