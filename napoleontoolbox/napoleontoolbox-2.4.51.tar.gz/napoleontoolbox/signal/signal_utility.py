#!/usr/bin/env python
# coding: utf-8

from numpy.lib.stride_tricks import as_strided as stride
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize
from napoleontoolbox.utility import metrics
import numpy as np
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.connector import napoleon_connector
import json

from napoleontoolbox.parallel_run import signal_result_analyzer

from functools import partial


def unjsonize_list_run_results(local_root_directory, list_pkl_file_name):
    signals_list = napoleon_connector.load_pickled_list(local_root_directory=local_root_directory,
                                                             list_pkl_file_name=list_pkl_file_name)
    print('signals list size '+str(len(signals_list)))
    params_list = []
    for me_signal in signals_list:
        ## idiosyncratic run itself
        run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
        params = json.loads(run_json_string)
        params_list.append(params)
    return params_list

def unjsonize_list_run_results_list(signals_list):
    print('signals list size '+str(len(signals_list)))
    params_list = []
    for me_signal in signals_list:
        ## idiosyncratic run itself
        run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
        params = json.loads(run_json_string)
        params_list.append(params)
    return params_list

def convert_to_sql_column_format(run):
    run = run.replace('[', 'ccg')
    run = run.replace(']', 'ccd')
    run = run.replace(',', 'comma')
    run = run.replace(' ', 'space')
    run = run.replace('.', 'dot')
    run = run.replace('-', 'minus')
    run = run.replace('"', 'dqq')
    run = run.replace("'", 'sqq')
    run = run.replace('{', 'aag')
    run = run.replace('}', 'aad')
    run = run.replace(':', 'dodo')
    return run

def recover_to_sql_column_format(run):
    run = run.replace('ccg','[')
    run = run.replace('ccd',']')
    run = run.replace('comma',',')
    run = run.replace('space',' ')
    run = run.replace('dot','.')
    run = run.replace('minus','-')
    run = run.replace('dqq','"')
    run = run.replace('sqq',"'")
    run = run.replace('aag','{')
    run = run.replace('aad','}')
    run = run.replace('dodo',':')
    return run


def compute_last_signal(rolled_df, lookback_window, function_to_apply):
    last_rolling_df = rolled_df.iloc[-lookback_window:]
    last_rolling_bis_df = rolled_df.tail(lookback_window)
    last_signal = function_to_apply(last_rolling_df)
    return last_signal

def roll_wrapper(rolled_df, lookback_window, skipping_size, function_to_apply, trigger):
    signal_df = roll(rolled_df, lookback_window).apply(function_to_apply)
    signal_df = signal_df.to_frame()
    signal_df.columns = ['signal_gen']
    signal_df['signal'] = signal_df['signal_gen'].shift()
    if trigger:
        signal_df['signal'] =  signal_df['signal'].fillna(method='ffill')

    signal_df = signal_df.fillna(0.)
    rolled_df = pd.merge(rolled_df, signal_df, how='left', left_index=True, right_index= True)
    rolled_df = rolled_df.iloc[skipping_size:]
    return rolled_df

def roll(df, w):
    v = df.values
    d0, d1 = v.shape
    s0, s1 = v.strides
    restricted_length = d0 - (w - 1)
    a = stride(v, (restricted_length, w, d1), (s0, s0, s1))
    rolled_df = pd.concat({
        row: pd.DataFrame(values, columns=df.columns)
        for row, values in zip(df.index[-restricted_length:], a)
    })
    return rolled_df.groupby(level=0)

def f_sharpe_signals_optim_mix(signal_data, returns, w, display_threshold = 0.99, period = 252, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True, print_turnover = False):
    N_ = signal_data.shape[1]
    w = w.reshape([1,N_])
    data = pd.DataFrame(signal_data.values * w, columns=signal_data.columns, index=signal_data.index)
    data['signal'] = data.sum(axis=1)
    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    average_turn_over = data['turn_over'].sum() / len(data)
    if print_turnover:
        print('average freqly turn over')
        print(average_turn_over)
    data['close_return'] = returns.values
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    if transaction_cost :
        data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
    else :
        data['perf_return'] = data['non_adjusted_perf_return']
    data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
    sharpe_strat = metrics.sharpe(data['perf_return'].dropna(), period= period, from_ret=True)
    if np.random.rand()>display_threshold:
        print(w)
        print('signals mix sharpe')
        print(sharpe_strat)
    return -sharpe_strat

def f_sharpe_signals_mix(data, w, display_threshold = 0.99, period = 252):
    all_signals = [col for col in data.columns if 'signal' in col]
    N_ = len(all_signals)
    w = w.reshape([1,N_])
    temp_df = data[['close']].copy()
    #temp_df = temp_df.rename(columns={"signal0": "signal"}, errors="raise")
    tt = pd.DataFrame(data[all_signals].values * w, columns=all_signals, index=data.index)
    temp_df['signal'] = tt.sum(axis=1)
    freqly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=True, print_turnover=False)
    sharpe_strat = metrics.sharpe(freqly_df['perf_return'].dropna(), period= period, from_ret=True)
    if np.random.rand()>display_threshold:
        print(w)
        print('signals mix sharpe')
        print(sharpe_strat)
    return -sharpe_strat

def expanding_zscore(signal_np_array=None, skipping_point = 5, signal_continuum_threshold = 10):
    u = np.unique(signal_np_array)
    nb_distinct_signals = len(u)
    if nb_distinct_signals >= signal_continuum_threshold:
        me_zscore_expanding_array = np.zeros(signal_np_array.shape)
        for i in range(len(signal_np_array)):
            if i <= skipping_point:
                me_zscore_expanding_array[i] = signal_np_array[i]
            else :
                std_dev = max(signal_np_array[:i].std(), 1e-6)
                me_zscore_expanding_array[i] = (signal_np_array[i] - signal_np_array[:i].mean())/std_dev
        return me_zscore_expanding_array
    else:
        raise Exception('zscoring a non continuous signal '+str(nb_distinct_signals))


def compute_signal_perf_ind(data=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True):

    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    average_turn_over = data['turn_over'].sum() / len(data)

    data['close_return'] = data['close'].pct_change()
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)

    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    data['adjusted°perf_return'] = data['non_adjusted_perf_return'] - data['turn_over'] * average_execution_cost

    data['non_adjusted_reconstituted_perf'] = metrics.from_ret_to_price(data['non_adjusted_perf_return'],initial_price=initial_price)
    perf_under = (data['reconstituted_close'].iloc[-1] - 1.) / 1.
    perf_strat = (data['non_adjusted_reconstituted_perf'].iloc[-1] - 1.) / 1.
    return average_turn_over, perf_under, perf_strat

def compute_signals_kpi(data=None, mapping_data=None, print_turnover = False, keep_only_one_per_signal_family = False, number_per_year = 252):
    hr_dic, json_dic = signal_result_analyzer.unjsonize_mapping_dataframe(mapping_data)
    all_signals = [col for col in data.columns if 'signal' in col]
    results_dic = {}
    results_dic_df = {}
    results_dic_without = {}
    results_dic_without_df = {}
    kpis = []
    for sig in all_signals:
        for transac_cost in [True, False]:
            temp_df = data[['close', sig]].copy()
            temp_df = temp_df.rename(columns={sig: "signal"})
            freqly_df, average_turn_over = signal_utility.reconstitute_signal_perf(data=temp_df, transaction_cost=transac_cost,print_turnover=print_turnover)
            sharpe_strat = metrics.sharpe(freqly_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
            sharpe_under = metrics.sharpe(freqly_df['close_return'].dropna(), period=number_per_year, from_ret=True)
            kpis.append(
                {
                    'sharpe_under': sharpe_under,
                    'sharpe_strat': sharpe_strat,
                    'signal': sig,
                    'average_turn_over':average_turn_over,
                    'transaction_cost': transac_cost,
                    'parameters_hash': hr_dic[sig]
                }
            )
            results_dic[sig + str(transac_cost)] = sharpe_strat
            results_dic_df[sig + str(transac_cost)] = [sharpe_strat]
            if not transac_cost:
                results_dic_without[sig] = sharpe_strat
                results_dic_without_df[sig] = [sharpe_strat]
    kpis_df = pd.DataFrame(kpis)
    single_kpis_df = kpis_df[['sharpe_under','sharpe_strat','transaction_cost']].copy().drop_duplicates()
    kpis_df = kpis_df[kpis_df.index.isin(list(single_kpis_df.index))]
    if keep_only_one_per_signal_family:
        results_dic_df = pd.DataFrame(results_dic_df)
        results_dic_without_df = pd.DataFrame(results_dic_without_df).T
        results_dic_without_df.columns = ['sharpe']
        results_dic_without_df = results_dic_without_df.sort_values(by=['sharpe'], ascending=False)
        results_dic_without_df = results_dic_without_df.reset_index()

        selected_algos = set()
        signals_to_keep = []
        for index, row in results_dic_without_df.iterrows():
            me_signal = row['index']
            print(me_signal)
            print(row['sharpe'])
            print(hr_dic[me_signal])
            params = json_dic[me_signal]
            if params['signal_type'] in selected_algos:
                continue
            else:
                selected_algos.add(params['signal_type'])
            signals_to_keep.append(me_signal)

        me_signals_to_keep = results_dic_without_df['index'].apply(lambda x: x in signals_to_keep)
        results_dic_without_df = results_dic_without_df.loc[me_signals_to_keep]
        kpis_df =kpis_df[kpis_df.signal.isin(list(results_dic_without_df['index'] ))]

    data = data[[col for col in data.columns if col in set(kpis_df.signal) or col == 'close']]
    return kpis_df, data, hr_dic, json_dic


def reconstitute_signal_perf(data=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True, print_turnover = False, normalization = False, recompute_return=True):
    if normalization:
        #data.signal = (data.signal - data.signal.mean())/data.signal.std(ddof=0)
        data.signal = expanding_zscore(signal_np_array=data.signal.values)
    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    average_turn_over = data['turn_over'].sum() / len(data)
    if print_turnover:
        print('average freqly turn over')
        print(average_turn_over)
    if recompute_return:
        data['close_return'] = data['close'].pct_change()
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    if transaction_cost :
        data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
    else :
        data['perf_return'] = data['non_adjusted_perf_return']
    data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
    return data, average_turn_over

def reconstitute_prediction_perf(y_pred=None, y_true=None, initial_price = 1. , average_execution_cost = 7.5e-4 , transaction_cost = True, print_turnover = False):
    if not isinstance(y_pred, pd.DataFrame):
        y_pred=pd.DataFrame(y_pred)
    data = y_pred
    data.columns = ['signal']
    if not isinstance(y_true, np.ndarray):
        y_true = y_true.values

    data['close_return']=y_true
    data['turn_over'] = abs(data['signal'] - data['signal'].shift(-1).fillna(0.))
    if print_turnover:
        print('average hourly turn over')
        print(data['turn_over'].sum() / len(data))
    data['reconstituted_close'] = metrics.from_ret_to_price(data['close_return'],initial_price=initial_price)
    data['non_adjusted_perf_return'] = data['close_return'] * data['signal']
    if transaction_cost :
        data['perf_return'] = data['non_adjusted_perf_return']- data['turn_over']*average_execution_cost
    else :
        data['perf_return'] = data['non_adjusted_perf_return']
    data['reconstituted_perf'] = metrics.from_ret_to_price(data['perf_return'],initial_price=initial_price)
    return data

def compute_turn_over(data=None):
    return abs((data.signal - data.signal.shift(-1).fillna(0.))).mean()

def deterministic_optim_sharpe(signal_data=None, returns=None, display_params = True):
    T_ = signal_data.shape[0]
    N_ = signal_data.shape[1]
    w0 = np.ones([N_]) / N_

    const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound = 1.
    low_bound = 0.
    up_bound_ = max(up_bound, 1 / N_)
    low_bound_ = min(low_bound, 1 / N_)
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))

    if display_params:
        print(max(signal_data.index))
        print(min(signal_data.index))
        print(N_)
        print(T_)
       # def f_sharpe_signals_optim_mix(signal_data, returns, w, display_threshold=0.99, period=252, initial_price=1.,average_execution_cost=7.5e-4, transaction_cost=True, print_turnover=False):

    #func_to_optimize = partial(signal_utility.f_sharpe_signals_optim_mix(signal_data, returns))
    func_to_optimize = lambda x : signal_utility.f_sharpe_signals_optim_mix(signal_data, returns, x)
    w__ = minimize(
        func_to_optimize,
        w0,
        method='SLSQP',
        constraints=[const_sum],
        bounds=const_ind
    ).x
    print('optimal weights')
    print(w__)
    return w__

def optimize_weights(data = None, starting_date = None, ending_date = None):
    #T = data.index.size
    print(max(data.index))
    print(min(data.index))
    data = data[data.index >= starting_date]
    data = data[data.index <= ending_date]
    print(max(data.index))
    print(min(data.index))
    all_sigs = [col for col in data.columns if 'signal' in col]
    N_ = len(all_sigs)
    w0 = np.ones([N_]) / N_

    const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound = 1.
    low_bound = 0.
    up_bound_ = max(up_bound, 1 / N_)
    low_bound_ = min(low_bound, 1 / N_)
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))
    to_optimize = lambda x : signal_utility.f_sharpe_signals_mix(data, x)
    w__ = minimize(
        to_optimize,
        w0,
        method='SLSQP',
        constraints=[const_sum],
        bounds=const_ind
    ).x
    print('optimal weights')
    print(w__)
    return w__

def compute_signals_weights_perf(data = None, optimal_weights = None, starting_date = None, ending_date = None, normalization = False, period = 252):
    print(max(data.index))
    print(min(data.index))
    data = data[data.index >= starting_date]
    data = data[data.index <= ending_date]
    print(max(data.index))
    print(min(data.index))
    all_sigs = [col for col in data.columns if 'signal' in col]
    temp_df = data[['close']].copy()
    if optimal_weights is None:
        N_ = len(all_sigs)
        optimal_weights = np.ones([N_]) / N_
    #temp_df = temp_df.rename(columns={"signal0": "signal"}, errors="raise")
    optimal_signal = pd.DataFrame(data[all_sigs].values * optimal_weights, columns=all_sigs, index=data.index)
    temp_df['signal'] = optimal_signal.sum(axis=1)
    hourly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=False, normalization=normalization)
    sharpe_strat_without = metrics.sharpe(hourly_df['perf_return'].dropna(), period=period, from_ret=True)
    sharpe_under = metrics.sharpe(hourly_df['close_return'].dropna(), period=period, from_ret=True)

    hourly_df = reconstitute_signal_perf(data=temp_df, transaction_cost=True, normalization=normalization)
    sharpe_strat = metrics.sharpe(hourly_df['perf_return'].dropna(), period=period, from_ret=True)
    return hourly_df, sharpe_strat, sharpe_strat_without, sharpe_under


def recompute_perf_returns(signals_df, close_df, transac_cost=True, print_turnover = False):
    results_df = pd.concat([signals_df, close_df], axis=1).reindex(signals_df.index)
    signals_returns_df = None
    for sig in results_df.columns:
        if 'signal' in sig:
            temp_df = results_df[['close_return', sig]].copy()
            temp_df = temp_df.rename(columns={sig: "signal"}, errors="raise")
            freqly_df, _ = signal_utility.reconstitute_signal_perf(data=temp_df, transaction_cost=transac_cost,
                                                                   print_turnover=print_turnover, recompute_return=False)
            if signals_returns_df is None:
                signals_returns_df = freqly_df[['perf_return']].rename(columns={'perf_return': sig})
            else:
                signals_returns_df[sig] = freqly_df.perf_return
    return signals_returns_df