"""
Fast Fourier Transformation
"""

import numpy as np
import pandas as pd
from hyperopt import hp, fmin, tpe, Trials

# local module
from foresee.models import models_util
from foresee.models import param_optimizer
from foresee.scripts import fitter


def _reconstruct_signal(
                         n_periods,
                         forecast_len,
                         fft_model,
                         ft_sample_frequencies,
                         fft_terms_for_reconstruction,
                         linear_trend
                      ):
    """[summary]

    Parameters
    ----------
    n_periods : [type]
        [description]
    forecast_len : [type]
        [description]
    fft_model : [type]
        [description]
    ft_sample_frequencies : [type]
        [description]
    fft_terms_for_reconstruction : [type]
        [description]
    linear_trend : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    pi = np.pi
    t = np.arange(0, n_periods+forecast_len)
    restored_sig = np.zeros(t.size)
    for i in fft_terms_for_reconstruction:
        ampli = np.absolute(fft_model[i]) / n_periods
        phase = np.angle(
                             fft_model[i],
                             deg = False
                           )
        restored_sig += ampli * np.cos(2 * pi * ft_sample_frequencies[i] * t + phase)
    return restored_sig + linear_trend[0] * t


def fft_fit_forecast(ts, fcst_len, params=None, args=None):
    """[summary]

    Parameters
    ----------
    ts : [type]
        [description]
    fcst_len : [type]
        [description]
    n_harmonics : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    
    
    try:
        ts_len = len(ts)
        n_harmonics = params['n_harmonics']
        
        t = np.arange(0, ts_len)
        linear_trend = np.polyfit(t, ts, 1)
        training_endog_detrend = ts - linear_trend[0] * t
        fft_model = np.fft.fft(training_endog_detrend)
        indexes = list(range(ts_len))
        
        # sort by amplitude
        indexes.sort(
                        key = lambda i: np.absolute(fft_model[i]) / ts_len,
                        reverse = True
                    )
        fft_terms_for_reconstruction = indexes[:1 + n_harmonics * 2]
        ft_sample_frequencies = np.fft.fftfreq(
                                                    n = ts_len,
                                                    d = 1
                                                 )
        
        fft_fit_forecast = _reconstruct_signal(
                                                 n_periods = ts_len,
                                                 forecast_len = fcst_len,
                                                 fft_model = fft_model,
                                                 ft_sample_frequencies = ft_sample_frequencies,
                                                 fft_terms_for_reconstruction = fft_terms_for_reconstruction,
                                                 linear_trend = linear_trend
                                              )
        
        fft_fit_forecast = pd.Series(fft_fit_forecast)
        
        
        fft_fittedvalues = fft_fit_forecast[:-(fcst_len)]
        
        fft_forecast = fft_fit_forecast[-(fcst_len):]
        
        err = None
        
        
    except Exception as e:
        fft_fittedvalues = None
        fft_forecast = None
        err = str(e)
        
    return fft_fittedvalues, fft_forecast, err


def fft_tune(ts_train, ts_test, params=None, args=None):
    
    model = 'fft'
    
    try:
        if params is None:
            space = hp.choice('n_harmonics', [nh for nh in range(2, 20)])
        else:
            nh_ub = params['n_harmonics']
            space = hp.choice('n_harmonics', [nh for nh in range(2, nh_ub)])
        
        f = fitter.model_loss(model)
        
        f_obj = lambda params: f.fit_loss(ts_train, ts_test, params, args)
        
        trials = Trials()
        
        best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=100, show_progressbar=False, verbose=False)
        
        err = None
        
    except Exception as e:
        err = str(e)
        best = None
        
    return best, err


def fft_main(data_dict, param_config, model_params):
    """[summary]

    Parameters
    ----------
    data_dict : [type]
        [description]
    model_params : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    model = 'fft'
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
    
    fit_args = dict()
    
    # no model competition
    if output_format in ['all_models']:
        
        params = {'n_harmonics': 5}
        fitted_values, forecast, err = fft_fit_forecast(
                                                                    ts = complete_fact['y'],
                                                                    fcst_len = fcst_len,
                                                                    params = params,
                                                                    args = None
                                                            )
        
        if err is None:
            fit_fcst_fact['fft_forecast'] = fitted_values.append(forecast).values
            
        else:
            fit_fcst_fact['fft_forecast'] = 0
            
        fit_args['err'] = err
        fit_args['n_harmonics'] = 5
            
    # with model completition            
    if output_format in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            model_params = model_params[model]
            params, err = param_optimizer.tune(train_fact, test_fact, model, params=model_params)
            fit_args['tune_err'] = err
            
        else:
            params = {'n_harmonics': 5}
            
        training_fitted_values, holdout_forecast, training_err = fft_fit_forecast(
                                                                                    ts = train_fact['y'],
                                                                                    fcst_len = len(test_fact),
                                                                                    params = params
                                                                                )
        
        complete_fitted_values, complete_forecast, complete_err = fft_fit_forecast(
                                                                                    ts = complete_fact['y'],
                                                                                    fcst_len = fcst_len,
                                                                                    params = params
                                                                                )
        
        if training_err is None and complete_err is None:
            fft_wfa = models_util.compute_wfa(
                                                y = test_fact['y'].values,
                                                yhat = holdout_forecast.values,
                                                epsilon = epsilon,
                                            )
            fft_fit_fcst = training_fitted_values.append(holdout_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['fft_forecast'] = fft_fit_fcst.values
            fit_fcst_fact['fft_wfa'] = fft_wfa
            
        else:
            fft_wfa = -1
            fit_fcst_fact['fft_forecast'] = 0
            fit_fcst_fact['fft_wfa'] = -1
            
        fit_args['err'] = (training_err, complete_err)
        fit_args['wfa'] = fft_wfa
        fit_args['n_harmonics'] = params['n_harmonics']
        
        
    return fit_fcst_fact, fit_args
