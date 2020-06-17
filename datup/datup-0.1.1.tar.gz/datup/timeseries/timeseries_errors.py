import numpy as np

''' 
The timeseries_errors methods can be used without an instance of a class over a timeseries
'''

def compute_rmse(
    self,
    timeseries,
    forecast
):
    r'''
    Return the root mean square error (RMSE) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A RMSE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_rmse(object,timeseries, forecast)
    '''
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        rmse = np.sqrt((e**2).mean())
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return rmse

def compute_mae(
    self,
    timeseries,
    forecast
):
    r'''
    Return the mean average error (MAE) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A MAE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mae(object,timeseries, forecast)
    '''
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        mae = np.mean(abs(e))
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return mae

def compute_maep(
    self,
    timeseries,
    forecast
):
    r'''
    Return the mean average error (MAEP) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A MAEP error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_maep(object,timeseries, forecast)
    '''    
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        maep = 100*np.mean(abs(e))/np.mean(timeseries.iloc[:,0])
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return maep

def compute_mape(
    self,
    timeseries,
    forecast
):
    r'''
    Return the mean average percentage error (MAPE) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A MAPE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mape(object,timeseries, forecast)
    '''
    try:
        e = (timeseries.iloc[:,0]-forecast.iloc[:,0])/timeseries.iloc[:,0]
        mape = 100*np.mean(abs(e))
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return mape

def compute_mase(
    self,
    timeseries,
    forecast
):
    r'''
    Return mean absolute scaled error (MASE) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A MASE error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mape(object,timeseries, forecast)
    '''
    try:
        ts_values = timeseries.iloc[:,0]
        e = (ts_values - forecast.iloc[:,0])
        denominator = (1/len(ts_values)-1)*sum(abs((ts_values-ts_values.shift(1)).fillna(0)))
        mase = np.mean(abs(e/denominator))        
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return mase

def compute_rmsep(self, timeseries, forecast):
    r'''
    Return root mean squared error percentage (RMSEP) between actual and forecast points.
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        timeseries: DataFrame, Serie
            It is the DataFrame with which want to work
        forecast: DataFrame, Serie
            It is the forecasted DataFrame which want to compare the points
    
    :return: A RMSEP error
    :rtype: float

    Examples
    --------
    >>> import datup as dt
    >>> dt.compute_mape(object,timeseries, forecast)
    '''
    try:
        e = timeseries.iloc[:,0]-forecast.iloc[:,0]
        rmsep = 100*np.sqrt((e**2).mean())/np.mean(timeseries.iloc[:,0])
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return rmsep