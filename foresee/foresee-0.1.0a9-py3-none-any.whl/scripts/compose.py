# -*- coding: utf-8 -*-
"""
Controls input and output of forecasting process
"""

import pandas as pd
import numpy as np
import datetime
import dask
dask.config.set(scheduler='processes')

from foresee.scripts import fitter

def generate_fit_forecast(dict_key, dict_values, param_config, model_params):
    """[summary]

    Parameters
    ----------
    dict_key : [type]
        [description]
    dict_values : [type]
        [description]
    model_list : [type]
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
    
    model_list = param_config['MODEL_LIST']
    
    fit_result = dict()
    fit_result['ts_id'] = dict_key
    
    for m in model_list:

        f = fitter.fitter(m)

        (
         fit_result[m+'_fit_fcst_df'],
         fit_result[m+'_args']
         ) = f.fit(dict_values, param_config, model_params)
    
    return fit_result


def compose_fit(pre_processed_dict, model_params, param_config):
    """[summary]

    Parameters
    ----------
    pre_processed_dict : [type]
        [description]
    model_params : [type]
        [description]
    param_config : [type]
        [description]
    gbkey : [type]
        [description]
    run_type : [type]
        [description]
    processing_method : [type]
        [description]
    tune : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

#    freq = param_config['FREQ']
#    forecast_len = param_config['FORECAST_LEN']
#    model_list = param_config['MODEL_LIST']
#    epsilon = param_config['EPSILON']

    processing_method = param_config['PROCESSING_METHOD']
    model_list = param_config['MODEL_LIST']
    output_format = param_config['OUTPUT_FORMAT']
    
    # non-parallel fit
    
    if processing_method == 'parallel':
        task_list = list()
        
        for dict_key, dict_values in pre_processed_dict.items():
            fit_task = dask.delayed(generate_fit_forecast)(
                                                               dict_key,
                                                               dict_values,
                                                               param_config,
                                                               model_params,
                                                          )
            task_list.append(fit_task)

        fit_result_list = dask.compute(task_list)[0]
        
    else:
        fit_result_list = list()

        for dict_key, dict_values  in pre_processed_dict.items():
            fit_result = generate_fit_forecast(
                                                    dict_key,
                                                    dict_values,
                                                    param_config,
                                                    model_params,
                                            )
            fit_result_list.append(fit_result)
        
    result = combine_to_dataframe(fit_result_list, model_list, output_format)
        
    return result, fit_result_list


def combine_to_dataframe(fit_result_list, model_list, output_format):
    """[summary]

    Parameters
    ----------
    fit_result_list : [type]
        [description]
    model_list : [type]
        [description]
    run_type : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    if output_format == 'best_model':

        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:

            bm = result_dict['best_model']
            df = result_dict[bm+'_fit_fcst_df']
            
            df['best_model'] = bm
            df['ts_id'] = result_dict['ts_id']
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
        
    elif output_format == 'all_best':
        
        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:
            bm = result_dict['best_model']
            df = result_dict[bm+'_fit_fcst_df']
            
            for m in model_list:
                mdf = result_dict[m+'_fit_fcst_df']
                df[m+'_forecast'] = mdf[m+'_forecast'].values
                df[m+'_wfa'] = mdf[m+'_wfa'].values

            df['ts_id'] = result_dict['ts_id']
            df['best_model'] = bm
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
                
        
    else:
        df_list = list()
        
        for result_dict in fit_result_list:
            m1 = model_list[0]
            df = result_dict[m1+'_fit_fcst_df']
            
            for m in model_list[1:]:
                mdf = result_dict[m+'_fit_fcst_df']
                df[m+'_forecast'] = mdf[m+'_forecast'].values
                
            df['ts_id'] = result_dict['ts_id']
            df_list.append(df)
        
        result = pd.concat(df_list, axis=0, ignore_index=True) 
    
    return result


def _find_best_model(fit_result_list, model_list):
    """[summary]

    Parameters
    ----------
    fit_result_list : [type]
        [description]
    model_list : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    for result_dict in fit_result_list:
        model_wfa_dict = dict()
        
        for m in model_list:
            model_wfa_dict[m] = result_dict[m+'_args']['wfa']
            
        result_dict['best_model'] = [k for k,v in model_wfa_dict.items() if v == max(model_wfa_dict.values())][0]
    
    return fit_result_list


# not in use
def _transform_dataframe_to_dict(raw_fact, gbkey):
    """[summary]

    Parameters
    ----------
    raw_fact : [type]
        [description]
    gbkey : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    data_param_list = list()
    
    if gbkey is None:
        
        data_param_list.append({'ts_id':1, 'df':raw_fact})
    
    else:
        for k,v in raw_fact.groupby(gbkey):
            data_param_list.append({'ts_id':k, 'df':v})
    
    return data_param_list


