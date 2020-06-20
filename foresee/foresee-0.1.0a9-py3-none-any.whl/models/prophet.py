"""
Prophet from fbprophet
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import os
from fbprophet import Prophet
from hyperopt import hp, fmin, tpe, Trials

# local module
from foresee.models import models_util
from foresee.models import param_optimizer
from foresee.scripts import fitter


class suppress_stdout_stderr(object):
    """[summary]

    Parameters
    ----------
    object : [type]
        [description]
    """

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

            
def prophet_fit_forecast(df, fcst_len, params=None, args=None):
    """[summary]

    Parameters
    ----------
    df : [type]
        [description]
    fcst_len : [type]
        [description]
    freq : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    df = df[['date_stamp','y']].reset_index(drop=True)
    df.columns = ['ds', 'y']
    
    freq = args['FREQ']
    
    if freq == 12:
        prophet_freq = 'M'
    elif freq == 52:
        prophet_freq = 'W'
    else:
        prophet_freq = None
    
    try:
        
        prophet_model = Prophet()
        
        with suppress_stdout_stderr():
            prophet_model.fit(df)
            
        future = prophet_model.make_future_dataframe(periods=fcst_len, freq=prophet_freq, include_history=True)
        
        prophet_model_predictions = prophet_model.predict(future)['yhat']
        
        prophet_fittedvalues = prophet_model_predictions.head(len(df))                
        
        prophet_forecast = prophet_model_predictions.tail(fcst_len)
        
        err = None
        
    except Exception as e:
        
        prophet_fittedvalues = None
        prophet_forecast = None
        err = str(e)
        
    return prophet_fittedvalues, prophet_forecast, err


def prophet_tune(ts_train, ts_test, params=None, args=None):
    return None

def prophet_main(data_dict, param_config, model_params):
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

    model = 'prophet'
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
    
    if output_format in ['all_models']:
    
        prophet_fitted_values, prophet_forecast, err = prophet_fit_forecast(
                                                                                df = complete_fact,
                                                                                fcst_len = fcst_len,
                                                                                args = args
                                                                            )
        if err is None:
            fit_fcst_fact['prophet_forecast'] = prophet_fitted_values.append(prophet_forecast).values
            
        else:
            fit_fcst_fact['prophet_forecast'] = 0
            
        fit_args['err'] = err
            
            
    if output_format in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        training_fitted_values, training_forecast, training_err = prophet_fit_forecast(
                                                                                            df = train_fact,
                                                                                            fcst_len = len(test_fact),
                                                                                            args = args
                                                                                    )
        
        complete_fitted_values, complete_forecast, complete_err = prophet_fit_forecast(
                                                                                            df = complete_fact,
                                                                                            fcst_len = fcst_len,
                                                                                            args = args,
                                                                                    )
        
        if training_err is None and complete_err is None:
            prophet_wfa = models_util.compute_wfa(
                                                    y = test_fact['y'].values,
                                                    yhat = training_forecast.values,
                                                    epsilon = epsilon
                                                )
            
            prophet_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['prophet_forecast'] = prophet_fit_fcst.values
            fit_fcst_fact['prophet_wfa'] = prophet_wfa
            
        else:
            prophet_wfa = -1
            fit_fcst_fact['prophet_forecast'] = 0
            fit_fcst_fact['prophet_wfa'] = prophet_wfa
            
        fit_args['err'] = (training_err, complete_err)
        fit_args['wfa'] = prophet_wfa
            
            
    return fit_fcst_fact, fit_args

