import pandas as pd
import numpy as np
from statsmodels.stats.stattools import jarque_bera, durbin_watson

''' 
The utils methods can be used without an instance of a class over a DataFrame
'''
def filter_by_list(
    self,
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered by a list passed as argument.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        dim: str, default None
            Is the feature with which want to work
        list_to_filter: list, default None
            The attributes which want to filter into a list

    :return: A DataFrame filtered by the attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.filter_by_list(object,df,"COLUMN",["list","of","attributes"])
    ''' 

    try:
        df_res = df[df[dim].isin(list_to_filter)]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}")
        raise 
    return df_res    

def antifilter_by_list(
    self,
    df,
    dim=None,
    list_to_filter=None
):
    r'''
    Return a dataframe filtered with a different attributes listed as argument.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        dim: str, default None
            Is the feature with which want to work
        list_to_filter: list, default None
            The attributes which want to not filter into a list

    :return: A DataFrame filtered by the differents attributes in a list
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.antifilter_by_list(object,df,"COLUMN",["list","of","attributes"])
    ''' 
    try:        
        df_res = df[~df[dim].isin(list_to_filter)]
    except IOError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise 
    return df_res

def reorder_columns(
    self,
    df,
    columns
):
    r'''
    Return a dataframe ordered by the columns passed.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        columns: list
            It is the list of columns for order

    :return: A DataFrame ordered by the columns passed
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.reorder_columns(object,df,["list","of","columns"])
    '''

    try:
        dims = df.columns.tolist()
        for col in reversed(columns):             
            dims.remove(col)
            dims.insert(0, col)
            df = df[dims]
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return df

def check_data_format(self,df):
    '''
    Return a dataframe of dimensions and its formats, e.g. int, float or string
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: A DataFrame of dimensions and its formats, e.g. int, float or string
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.check_data_format(object,df)
    '''

    try:
        dataformats = df.dtypes
        dims = list(dataformats.index.astype('str'))
        formats = list(dataformats.values.astype('str'))
        formats = list(zip(dims, formats))
        df_format = pd.DataFrame(formats, columns=['Dimension', 'Format']) 
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df_format

def count_na(self,df):
    '''
    Return a dataframe counting NaNs per dataframe columns
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: A DataFrame counting NaNs per column
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.count_na(object,df)    
    '''
    
    try:
        num_obs = df.shape[0]
        nan_list = []
        for dim in df.columns:
            nan_cnt = df[dim].isna().sum()
            nan_pct = nan_cnt/num_obs*100
            nan_list.append([dim, nan_cnt, nan_pct])
        df_nan = pd.DataFrame(nan_list, columns=['Dimension', 'Qty_NaNs', 'Pct_NaNs'])
        df_nan = df_nan.sort_values(by=['Pct_NaNs'], ascending=False)
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df_nan

def cast_datetime(
    self,
    df,
    date_dims,
    date_format='%Y/%m/%d',
    errors="coerce"
):
    """
    Return a dataframe casting datetime dimensions to datetime datatype
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        date_dims: List
            It is the list of dimensions or features with datetime type for casting
        date_format: Datetime, default '%Y/%m/%d'
            It is the format of datetime to cast the date_dims features
        errors: str, default 'coerce'
            Took it from Pandas read_csv parse_dates description
            * If ‘raise’, then invalid parsing will raise an exception.
            * If ‘coerce’, then invalid parsing will be set as NaT.
            * If ‘ignore’, then invalid parsing will return the input.

    :return: A DataFrame with datetimes dimensions casted
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.cast_datetime(object,df,date_dims=["list","of","dims"])  
    """
    try:
        for dim in date_dims:
            df[dim] = pd.to_datetime(df[dim], format=date_format, errors=errors)
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
    return df

def parse_months(
    self,
    df,
    month_dim,
    language='spanish'
):
    """
    Convert string month names to numeric
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        month_dim: Serie
            It is the Serie with months in string for mapping
        language: str, default 'spanish'
            Is the language of the month_dim 

    :return: A Serie with months mapped to int numbers
    :rtype: Serie

    Examples
    --------
    >>> import datup as dt
    >>> dt.parse_months(object,df,month_dim="month_dim")
    """
    try:
        df[month_dim] = df[month_dim].str.upper()
        if language=='spanish':            
            months = {'ENERO':1, 'FEBRERO':2, 'MARZO':3, 'ABRIL':4, 'MAYO':5, 'JUNIO':6, 
                    'JULIO':7, 'AGOSTO':8, 'SEPTIEMBRE':9, 'OCTUBRE':10, 'NOVIEMBRE':11, 'DICIEMBRE':12} 
            df[month_dim] = df[month_dim].map(months)
        else:
            months = {'JANUARY':1, 'FEBRUARY':2, 'MARCH':3, 'APRIL':4, 'MAY':5, 'JUNE':6, 
                    'JULY':7, 'AUGUST':8, 'SEPTEMBER':9, 'OCTOBER':10, 'NOVEMBER':11, 'DECEMBER':12} 
            df[month_dim] = df[month_dim].map(months)
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return df

def transform_positive_timeseries(
    self,
    df,
    positive_fix=0.001
):
    """
    Return a dataframe with values strictly positive. 0s and negative replaced with the value specified
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        positive_fix: float, default 0.001
            Is the to replace negative and 0s values 

    :return: A Serie with values strictly positive
    :rtype: Serie

    Examples
    --------
    >>> import datup as dt
    >>> dt.transform_positive_timeseries(object,df)
    """
    try:
        df[df<=0] = positive_fix
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return df

def transform_log_plus_one(
    self,
    df
):
    """
    Return a dataframe with log(x+1)
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: Return a dataframe with log(x+1)
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.transform_log_plus_one(object,df)    
    """
    try:
        for dim in df.columns:
            df[dim] = df[dim].map(lambda x: np.log(x+1))
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return df

def test_gaussianity(
    self,
    residuals
):
    """
    Return a boolean informing guassianity (true) or non-gaussianity (false) of the timeseries residuals
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        residuals: Serie
            It is the Serie with which want to work

    :return: Return a boolean informing guassianity (true) or non-gaussianity (false)
    :rtype: Bool

    Examples
    --------
    >>> import datup as dt
    >>> dt.test_gaussianity(object,residuals)     
    """
    try:
        gauss_test = jarque_bera(residuals)
        if gauss_test[1] < 0.1: 
            gaussianity_flag = False
            self.logger.debug('Residuals not Gaussian (p-value={pv:.3f})'.format(pv=gauss_test[1]))    
        else:
            gaussianity_flag = True
            self.logger.debug('Residuals Gaussian (p-value={pv:.3f})'.format(pv=gauss_test[1]))
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return gaussianity_flag

def test_acorr(
    self,
    residuals
):
    """
    Return a boolean informing autocorrelation of the timeseries residuals
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        residuals: Serie
            It is the Serie with which want to work

    :return: Return a boolean informing autocorrelation
    :rtype: Bool

    Examples
    --------
    >>> import datup as dt
    >>> dt.test_acorr(object,residuals)
    """
    try:
        dw_test = durbin_watson(residuals)
        if dw_test == 2:
            acorr_flag = False
            self.logger.debug('Residuals not autocorrelated (t={test:.3f})'.format(test=dw_test))
        elif dw_test > 0 and dw_test < 2:
            acorr_flag = True
            self.logger.debug('Residuals positive correlated (t={test:.3f})'.format(test=dw_test))
        elif dw_test > 2 and dw_test <4:
            acorr_flag = True
            self.logger.debug('Residuals negative correlated (t={test:.3f})'.format(test=dw_test))
        else:
            acorr_flag = True
            self.logger.debug('Residuals are really bad for autocorrelation (t={test:.3f})...'.format(test=dw_test))
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise
    return acorr_flag