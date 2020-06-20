# -*- coding: utf-8 -*-
"""
Joins user input with parameters configuration and stat models configuration
and combines forecast results
"""

import os
import pandas as pd
import numpy as np
import datetime

from foresee.scripts import utils
from foresee.scripts import compose
from foresee.params import constants

# default model params
model_params = utils.read_json('model_params.json')

epsilon = constants.Constants().epsilon



def prepare_fit_report(
                        ts_df,
                        endog_colname = None,
                        ds_colname = None, 
                        gbkey = None,
                        freq = 1, 
                        fcst_length = 10, 
                        output_format = 'all_models', 
                        holdout_length = 5,
                        model_list = None,
                        processing_method = 'non_parallel',
                        tune = False,
                    ):
    """[summary]

    Parameters
    ----------
    raw_fact : [type]
        [description]
    endog_colname : [type]
        [description]
    gbkey : [type]
        [description]
    ds_column : [type]
        [description]
    freq : [type]
        [description]
    fcst_length : [type]
        [description]
    run_type : [type]
        [description]
    holdout_length : [type]
        [description]
    model_list : [type]
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
    
    param_config = dict()
    
    param_config['Y'] = endog_colname
    param_config['DATE_STAMP'] = ds_colname
    param_config['GBKEY'] = gbkey
    param_config['FREQ'] = freq
    param_config['FORECAST_LEN'] = fcst_length
    param_config['HOLDOUT_LEN'] = holdout_length
    param_config['MODEL_LIST'] = model_list
    param_config['OUTPUT_FORMAT'] = output_format
    param_config['MODEL_LIST'] = model_list
    param_config['TUNE'] = tune
    param_config['PROCESSING_METHOD'] = processing_method
    param_config['EPSILON'] = epsilon
    
    raw_fact = ts_df.copy()
    
    pre_processed_dict = _pre_process_user_inputs(
                                                            raw_fact,
                                                            param_config,
                                                    )
    
    result, fit_result_list = compose.compose_fit(
                                                        pre_processed_dict,
                                                        model_params,
                                                        param_config,
                                                )
    
    return result, fit_result_list


def _pre_process_user_inputs(
                                    raw_fact,
                                    param_config,
                            ):
    
    endog_colname = param_config['Y']
    ds_colname = param_config['DATE_STAMP']
    output_format = param_config['OUTPUT_FORMAT']
    gbkey = param_config['GBKEY']
    holdout_length = param_config['HOLDOUT_LEN']
        
    # replace endog column name with 'y'
    
    if len(raw_fact.columns) == 1:
        raw_fact.columns = ['y']
    else:
        if endog_colname in raw_fact.columns:
            raw_fact.rename(columns={endog_colname: 'y'}, inplace=True)
        else:
            #TODO: display this error to user
            raise ValueError('time series column name not found!!!')

    
    # add or rename date-time column
    
    if ds_colname not in raw_fact.columns:
        raw_fact['date_stamp'] = pd.date_range(end=datetime.datetime.now(), periods=len(raw_fact), freq='D')
        
    else:
        raw_fact.rename(columns={ds_colname: 'date_stamp'}, inplace=True)
        raw_fact['date_stamp'] = pd.to_datetime(raw_fact['date_stamp'])
#        raw_fact['date_stamp'] = raw_fact['date_stamp'].astype('datetime64[ns]')
        
    #TODO: if user chose to compare models, then create train-holdout sets
    #TODO: missing data interpolation, needs user input!
    
    pre_processed_dict = dict()    
        
    if output_format in ['best_model', 'all_best']:
        
        if gbkey in raw_fact.columns:
            for k,v in raw_fact.groupby(gbkey):
                train_fact = v.iloc[:-holdout_length]
                test_fact = v.iloc[-holdout_length:]
                v['data_split'] = np.concatenate([np.full(len(train_fact), 'Train'), np.full(len(test_fact), 'Test')])

                pre_processed_dict[k] = {'complete_fact': v, 'train_fact': train_fact, 'test_fact': test_fact}
                
        else:
            train_fact = raw_fact.iloc[:-holdout_length]
            test_fact = raw_fact.iloc[-holdout_length:]
            raw_fact['data_split'] = np.concatenate([np.full(len(train_fact), 'Train'), np.full(len(test_fact), 'Test')])
            
            pre_processed_dict[1] = {'complete_fact': raw_fact, 'train_fact': train_fact, 'test_fact': test_fact}
            
            
    else:
        if gbkey in raw_fact.columns:
            for k,v in raw_fact.groupby(gbkey):
                v['data_split'] = 'Train'
                pre_processed_dict[k] = {'complete_fact': v}
                
        else:
            raw_fact['data_split'] = 'Train'
            pre_processed_dict[1] = {'complete_fact': raw_fact}
            
    
    return pre_processed_dict
  



