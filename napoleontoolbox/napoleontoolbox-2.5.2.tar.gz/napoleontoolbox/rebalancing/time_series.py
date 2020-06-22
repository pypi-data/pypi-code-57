from napoleontoolbox.rebalancing import rolling

from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from napoleontoolbox.signal import signal_utility


import pandas as pd
import numpy as np


from napoleontoolbox.utility import metrics
from scipy.optimize import Bounds, minimize


def discretize_two_states(y_pred, splitting_quantile_threshold=0.5):
    y_pred_discrete = np.zeros(y_pred.shape)
    threshold = np.nan
    try:
        threshold = np.quantile(y_pred, splitting_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")
    if np.isnan(threshold) :
        threshold = 0.5
    y_pred_discrete[y_pred > threshold] = 1.
    y_pred_discrete[y_pred < threshold] = -1.
    return y_pred_discrete

def discretize_two_states_lo(y_pred, splitting_quantile_threshold=0.5):
    y_pred_discrete = np.zeros(y_pred.shape)
    threshold = np.nan
    try:
        threshold = np.quantile(y_pred, splitting_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")
    if np.isnan(threshold) :
        threshold = 0.5
    y_pred_discrete[y_pred > threshold] = 1.
    y_pred_discrete[y_pred < threshold] = 0.
    return y_pred_discrete

def discretize_three_states(y_pred, upper_quantile_threshold=0.8, lower_quantile_threshold = 0.2):
    y_pred_discrete = np.zeros(y_pred.shape)

    lower_threshold = np.nan
    try:
        lower_threshold = np.quantile(y_pred, lower_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")

    upper_threshold = np.nan
    try:
        upper_threshold = np.quantile(y_pred, upper_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")

    if np.isnan(upper_threshold):
        upper_threshold = 0.8
    if np.isnan(lower_threshold):
        lower_threshold = 0.2

    y_pred_discrete[y_pred > upper_threshold] = 1.
    y_pred_discrete[y_pred < lower_threshold] = -1.
    return y_pred_discrete

def discretize_three_states_lo(y_pred, upper_quantile_threshold=0.8, lower_quantile_threshold = 0.2):
    y_pred_discrete = np.ones(y_pred.shape)/2

    lower_threshold = np.nan
    try:
        lower_threshold = np.quantile(y_pred, lower_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")

    upper_threshold = np.nan
    try:
        upper_threshold = np.quantile(y_pred, upper_quantile_threshold)
    except Exception as e:
        print(e)
        print("the quantile could not get computed")

    if np.isnan(upper_threshold):
        upper_threshold = 0.8
    if np.isnan(lower_threshold):
        lower_threshold = 0.2

    y_pred_discrete[y_pred > upper_threshold] = 1.
    y_pred_discrete[y_pred < lower_threshold] = 0.
    return y_pred_discrete

def find_best_two_states_discretization(y_pred, y, seed = 42, number_per_year = 252):
    N_ = 1
    w0 = np.array([0.5])
    # Set constraints
    #const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound_ = 1.
    low_bound_ = 0.
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))
    def f_to_optimize(w):
        y_pred_discrete = discretize_two_states(y_pred, splitting_quantile_threshold=w[0])
        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                              transaction_cost=False,
                                                              print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
        return sharpe_strat

    np.random.seed(seed)
    # Optimize f
    w__ = minimize(
        f_to_optimize,
        w0,
        method='SLSQP',
        #constraints=[const_sum],
        bounds=const_ind
    ).x

    splitting_quantile_threshold = w__[0]
    y_pred_discrete = discretize_two_states(y_pred, splitting_quantile_threshold=splitting_quantile_threshold)
    perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                          transaction_cost=False,
                                                          print_turnover=False)
    sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
    sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period=number_per_year, from_ret=True)
    return splitting_quantile_threshold, sharpe_strat, sharpe_under

def find_best_two_states_discretization_lo(y_pred, y, seed = 42, number_per_year = 252):
    N_ = 1
    w0 = np.array([0.5])
    # Set constraints
    #const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound_ = 1.
    low_bound_ = 0.
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))
    def f_to_optimize(w):
        y_pred_discrete = discretize_two_states_lo(y_pred, splitting_quantile_threshold=w[0])
        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                              transaction_cost=False,
                                                              print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
        return sharpe_strat

    np.random.seed(seed)
    # Optimize f
    w__ = minimize(
        f_to_optimize,
        w0,
        method='SLSQP',
        #constraints=[const_sum],
        bounds=const_ind
    ).x

    splitting_quantile_threshold = w__[0]
    y_pred_discrete = discretize_two_states_lo(y_pred, splitting_quantile_threshold=splitting_quantile_threshold)
    perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                          transaction_cost=False,
                                                          print_turnover=False)
    sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
    sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period=number_per_year, from_ret=True)
    return splitting_quantile_threshold, sharpe_strat, sharpe_under

def find_best_three_states_discretization(y_pred, y, seed = 42, number_per_year=252):
    N_ = 2
    w0 = np.array([0.3,0.7])
    # Set constraints
    #const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound_ = 1.
    low_bound_ = 0.
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))

    def f_to_optimize(w):
        lower_quantile_threshold = w[0]
        upper_quantile_threshold = w[1]

        y_pred_discrete = discretize_three_states(y_pred, upper_quantile_threshold=upper_quantile_threshold, lower_quantile_threshold=lower_quantile_threshold)
        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                              transaction_cost=False,
                                                              print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
        return sharpe_strat

    np.random.seed(seed)
    # Optimize f
    w__ = minimize(
        f_to_optimize,
        w0,
        method='SLSQP',
        #constraints=[const_sum],
        bounds=const_ind
    ).x

    lower_quantile_threshold = w__[0]
    upper_quantile_threshold = w__[1]
    y_pred_discrete = discretize_three_states(y_pred, upper_quantile_threshold=upper_quantile_threshold,
                                 lower_quantile_threshold=lower_quantile_threshold)
    perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                          transaction_cost=False,
                                                          print_turnover=False)
    sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
    sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period=number_per_year, from_ret=True)
    return lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under

def find_best_three_states_discretization_lo(y_pred, y, seed = 42, number_per_year=252):
    N_ = 2
    w0 = np.array([0.3,0.7])
    # Set constraints
    #const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
    up_bound_ = 1.
    low_bound_ = 0.
    const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))

    def f_to_optimize(w):
        lower_quantile_threshold = w[0]
        upper_quantile_threshold = w[1]

        y_pred_discrete = discretize_three_states_lo(y_pred, upper_quantile_threshold=upper_quantile_threshold, lower_quantile_threshold=lower_quantile_threshold)
        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                              transaction_cost=False,
                                                              print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
        return sharpe_strat

    np.random.seed(seed)
    # Optimize f
    w__ = minimize(
        f_to_optimize,
        w0,
        method='SLSQP',
        #constraints=[const_sum],
        bounds=const_ind
    ).x

    lower_quantile_threshold = w__[0]
    upper_quantile_threshold = w__[1]
    y_pred_discrete = discretize_three_states_lo(y_pred, upper_quantile_threshold=upper_quantile_threshold,
                                 lower_quantile_threshold=lower_quantile_threshold)
    perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                          transaction_cost=False,
                                                          print_turnover=False)
    sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
    sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period=number_per_year, from_ret=True)
    return lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under


def rolling_mixing(forecasting_model, X, y, n=252, s=63, s_eval= None, calibration_step=None, display = False, **kwargs):
    assert X.shape[0] == y.shape[0]
    idx = X.index
    forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_three_states_forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_three_states_forecasting_series_lo = pd.Series(index=idx, name='prediction')
    discrete_two_states_forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_two_states_forecasting_series_lo = pd.Series(index=idx, name='prediction')

    if n is None and s_eval is None:
        roll = rolling._ExpandingRollingMechanism(idx, s=s)
    if n is None and s_eval is not None:
        roll = rolling._ExpandingEvalRollingMechanism(idx, s=s, s_eval = s_eval)
    if n is not None and s_eval is None :
        roll = rolling._RollingMechanism(idx, n=n, s=s)
    if n is not None and s_eval is not None:
        roll = rolling._EvalRollingMechanism(idx, n=n, s=s, s_eval = s_eval)
    features_names = list(X.columns)
    features_importances = []
    iteration_counter = 0
    for slice_n, slice_s, slice_s_eval in roll():
        # Select X
        X_train = X.loc[slice_n].copy()
        y_train = y.loc[slice_n].copy()

        X_test = X.loc[slice_s].copy()
        y_test = y.loc[slice_s].copy()
        if calibration_step >0:
            if (iteration_counter>0 and iteration_counter%calibration_step == 0):
                # print('launching calibration '+str(iteration_counter))
                forecasting_model.calibrate(X_train, y_train)
                # print('endiing calibration ' + str(iteration_counter))

        if slice_s_eval is not None:
            X_eval = X.loc[slice_s_eval].copy()
            y_eval = y.loc[slice_s_eval].copy()
            forecasting_model.fit(X_train, y_train, X_eval, y_eval)
        else :
            forecasting_model.fit(X_train, y_train, X_train, y_train)

        y_pred = forecasting_model.predict(X_test)
        y_train_pred = forecasting_model.predict(X_train)

        #### three states discretization
        lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under = find_best_three_states_discretization(y_train, y_train_pred)
        # print('best sharpe training period '+str(sharpe_strat))
        # print('lower quantile '+str(lower_quantile_threshold))
        # print('upper quantile '+str(upper_quantile_threshold))
        y_pred_three_space_discrete = discretize_three_states(y_pred, upper_quantile_threshold,lower_quantile_threshold)
        y_test_three_space_discrete = discretize_three_states(y_test, upper_quantile_threshold,lower_quantile_threshold)

        #### three states discretization long only
        lower_quantile_threshold_lo, upper_quantile_threshold_lo, sharpe_strat_lo, sharpe_under_lo = find_best_three_states_discretization_lo(
            y_train, y_train_pred)
        # print('best sharpe training period '+str(sharpe_strat))
        # print('lower quantile '+str(lower_quantile_threshold))
        # print('upper quantile '+str(upper_quantile_threshold))
        y_pred_three_space_discrete_lo = discretize_three_states_lo(y_pred, upper_quantile_threshold_lo,
                                                              lower_quantile_threshold_lo)
        y_test_three_space_discrete_lo = discretize_three_states_lo(y_test, upper_quantile_threshold_lo,
                                                              lower_quantile_threshold_lo)


        #### two states discretization
        splitting_quantile_threshold, sharpe_strat, sharpe_under = find_best_two_states_discretization(y_train,
                                                                                                       y_train_pred)
        y_pred_two_space_discrete = discretize_two_states(y_pred, splitting_quantile_threshold)
        y_test_two_space_discrete = discretize_two_states(y_test, splitting_quantile_threshold)

        #### two states discretization long only
        splitting_quantile_threshold_lo, sharpe_strat_lo, sharpe_under_lo = find_best_two_states_discretization(y_train,
                                                                                                       y_train_pred)
        y_pred_two_space_discrete_lo = discretize_two_states_lo(y_pred, splitting_quantile_threshold_lo)
        y_test_two_space_discrete_lo = discretize_two_states_lo(y_test, splitting_quantile_threshold_lo)

        run_importances=forecasting_model.get_features_importance(features_names)
        features_importances.append(run_importances)
        # no leverage for the moment
        forecasting_series.loc[slice_s] = y_pred.ravel()
        discrete_three_states_forecasting_series.loc[slice_s] = y_pred_three_space_discrete.ravel()
        discrete_two_states_forecasting_series.loc[slice_s] = y_pred_two_space_discrete.ravel()
        discrete_three_states_forecasting_series_lo.loc[slice_s] = y_pred_three_space_discrete_lo.ravel()
        discrete_two_states_forecasting_series_lo.loc[slice_s] = y_pred_two_space_discrete_lo.ravel()

        rmse = mean_squared_error(y_test, y_pred)
        matrix_three = confusion_matrix(y_test_three_space_discrete, y_pred_three_space_discrete)
        accuracy_three = accuracy_score(y_test_three_space_discrete, y_pred_three_space_discrete)
        # matrix_three_lo = confusion_matrix(y_test_three_space_discrete_lo, y_pred_three_space_discrete_lo)
        # accuracy_three_lo = accuracy_score(y_test_three_space_discrete_lo, y_pred_three_space_discrete_lo)
        matrix_two = confusion_matrix(y_test_two_space_discrete, y_pred_two_space_discrete)
        accuracy_two = accuracy_score(y_test_two_space_discrete, y_pred_two_space_discrete)
        matrix_two_lo = confusion_matrix(y_test_two_space_discrete_lo, y_pred_two_space_discrete_lo)
        accuracy_two_lo = accuracy_score(y_test_two_space_discrete_lo, y_pred_two_space_discrete_lo)

        if display:
            print('training slice ' + str(slice_n))
            print('testing slice ' + str(slice_s))
            print('rmse for slice : '+str(rmse))
            print('accuracy three states')
            print(accuracy_three)
            print('confusion matrix three states')
            print(matrix_three  )
            print('accuracy two states')
            print(accuracy_two)
            print('confusion matrix two states')
            print(matrix_two)
        iteration_counter = iteration_counter+1

    features_importances = pd.DataFrame(features_importances)
    return forecasting_series, features_importances, discrete_two_states_forecasting_series, discrete_two_states_forecasting_series_lo, discrete_three_states_forecasting_series, discrete_three_states_forecasting_series_lo


def rolling_forecasting(forecasting_model, X, y, n=252, s=63, s_eval= None, calibration_step=None, display = False, min_signal = -1., max_signal = 1., **kwargs):
    assert X.shape[0] == y.shape[0]
    idx = X.index
    forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_three_states_forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_three_states_forecasting_series_lo = pd.Series(index=idx, name='prediction')
    discrete_two_states_forecasting_series = pd.Series(index=idx, name='prediction')
    discrete_two_states_forecasting_series_lo = pd.Series(index=idx, name='prediction')

    if n is None and s_eval is None:
        roll = rolling._ExpandingRollingMechanism(idx, s=s)
    if n is None and s_eval is not None:
        roll = rolling._ExpandingEvalRollingMechanism(idx, s=s, s_eval = s_eval)
    if n is not None and s_eval is None :
        roll = rolling._RollingMechanism(idx, n=n, s=s)
    if n is not None and s_eval is not None:
        roll = rolling._EvalRollingMechanism(idx, n=n, s=s, s_eval = s_eval)
    features_names = list(X.columns)
    features_importances = []
    iteration_counter = 0
    for slice_n, slice_s, slice_s_eval in roll():
        # Select X
        X_train = X.loc[slice_n].copy()
        y_train = y.loc[slice_n].copy()

        X_test = X.loc[slice_s].copy()
        y_test = y.loc[slice_s].copy()
        if calibration_step >0:
            if (iteration_counter>0 and iteration_counter%calibration_step == 0):
                # print('launching calibration '+str(iteration_counter))
                forecasting_model.calibrate(X_train, y_train)
                # print('endiing calibration ' + str(iteration_counter))

        if slice_s_eval is not None:
            X_eval = X.loc[slice_s_eval].copy()
            y_eval = y.loc[slice_s_eval].copy()
            forecasting_model.fit(X_train, y_train, X_eval, y_eval)
        else :
            forecasting_model.fit(X_train, y_train, X_train, y_train)

        y_pred = forecasting_model.predict(X_test)
        y_train_pred = forecasting_model.predict(X_train)

        #### three states discretization
        lower_quantile_threshold, upper_quantile_threshold, sharpe_strat, sharpe_under = find_best_three_states_discretization(y_train, y_train_pred)
        # print('best sharpe training period '+str(sharpe_strat))
        # print('lower quantile '+str(lower_quantile_threshold))
        # print('upper quantile '+str(upper_quantile_threshold))
        y_pred_three_space_discrete = discretize_three_states(y_pred, upper_quantile_threshold,lower_quantile_threshold)
        y_test_three_space_discrete = discretize_three_states(y_test, upper_quantile_threshold,lower_quantile_threshold)

        #### three states discretization long only
        lower_quantile_threshold_lo, upper_quantile_threshold_lo, sharpe_strat_lo, sharpe_under_lo = find_best_three_states_discretization_lo(
            y_train, y_train_pred)
        # print('best sharpe training period '+str(sharpe_strat))
        # print('lower quantile '+str(lower_quantile_threshold))
        # print('upper quantile '+str(upper_quantile_threshold))
        y_pred_three_space_discrete_lo = discretize_three_states_lo(y_pred, upper_quantile_threshold_lo,
                                                              lower_quantile_threshold_lo)
        y_test_three_space_discrete_lo = discretize_three_states_lo(y_test, upper_quantile_threshold_lo,
                                                              lower_quantile_threshold_lo)


        #### two states discretization
        splitting_quantile_threshold, sharpe_strat, sharpe_under = find_best_two_states_discretization(y_train,
                                                                                                       y_train_pred)
        y_pred_two_space_discrete = discretize_two_states(y_pred, splitting_quantile_threshold)
        y_test_two_space_discrete = discretize_two_states(y_test, splitting_quantile_threshold)

        #### two states discretization long only
        splitting_quantile_threshold_lo, sharpe_strat_lo, sharpe_under_lo = find_best_two_states_discretization(y_train,
                                                                                                       y_train_pred)
        y_pred_two_space_discrete_lo = discretize_two_states_lo(y_pred, splitting_quantile_threshold_lo)
        y_test_two_space_discrete_lo = discretize_two_states_lo(y_test, splitting_quantile_threshold_lo)

        run_importances=forecasting_model.get_features_importance(features_names)
        features_importances.append(run_importances)
        # no leverage for the moment
        y_pred = np.clip(y_pred, a_min=min_signal, a_max=max_signal)
        forecasting_series.loc[slice_s] = y_pred.ravel()
        discrete_three_states_forecasting_series.loc[slice_s] = y_pred_three_space_discrete.ravel()
        discrete_two_states_forecasting_series.loc[slice_s] = y_pred_two_space_discrete.ravel()
        discrete_three_states_forecasting_series_lo.loc[slice_s] = y_pred_three_space_discrete_lo.ravel()
        discrete_two_states_forecasting_series_lo.loc[slice_s] = y_pred_two_space_discrete_lo.ravel()

        rmse = mean_squared_error(y_test, y_pred)
        matrix_three = confusion_matrix(y_test_three_space_discrete, y_pred_three_space_discrete)
        accuracy_three = accuracy_score(y_test_three_space_discrete, y_pred_three_space_discrete)
        # matrix_three_lo = confusion_matrix(y_test_three_space_discrete_lo, y_pred_three_space_discrete_lo)
        # accuracy_three_lo = accuracy_score(y_test_three_space_discrete_lo, y_pred_three_space_discrete_lo)
        matrix_two = confusion_matrix(y_test_two_space_discrete, y_pred_two_space_discrete)
        accuracy_two = accuracy_score(y_test_two_space_discrete, y_pred_two_space_discrete)
        matrix_two_lo = confusion_matrix(y_test_two_space_discrete_lo, y_pred_two_space_discrete_lo)
        accuracy_two_lo = accuracy_score(y_test_two_space_discrete_lo, y_pred_two_space_discrete_lo)

        if display:
            print('training slice ' + str(slice_n))
            print('testing slice ' + str(slice_s))
            print('rmse for slice : '+str(rmse))
            print('accuracy three states')
            print(accuracy_three)
            print('confusion matrix three states')
            print(matrix_three  )
            print('accuracy two states')
            print(accuracy_two)
            print('confusion matrix two states')
            print(matrix_two)
        iteration_counter = iteration_counter+1

    features_importances = pd.DataFrame(features_importances)
    return forecasting_series, features_importances, discrete_two_states_forecasting_series, discrete_two_states_forecasting_series_lo, discrete_three_states_forecasting_series, discrete_three_states_forecasting_series_lo

