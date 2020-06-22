def hola_mundo(name="Mundo"):
    return "Librería creada e importada exitosamente. Hola, {name}".format(name = name)
   
def df_colored(pandas_df, cmap='RdYlGn', axis=None):
    """This function returns a styled dataframe with conditional foramting"""
    x = pandas_df.style.background_gradient(cmap=cmap,axis=axis)
    return x

def df_colored_perc(pandas_df, cmap='RdYlGn',axis=None):
    """This function returns a styled dataframe with conditional foramting and the numbers as a percentage"""
    return pandas_df.style.format('{:,.1%}'.format).background_gradient(cmap=cmap,axis=axis)

def distribution(x, hist=False):
    """This function draws the distribution of observations in a serie"""
    import seaborn as sns
    return sns.distplot(x, hist=hist)

def df_percentage(x):
    """This function calculates the percentage of columns"""

    return x.T.apply(lambda x: x / float(x.sum())) 

def df_join(a,b,join,left,right):
    """This function joins two pandas dataframes in a SQL-like way"""
    import pandas as pd
    return pd.merge(a, b,how=join, left_on=left, right_on = right)

# .format('{:,.1%}'.format)


def date_ranges(start = '2020-01-01', end = '2020-03-01', interval = 30):
    """This function returns a list of date ranges that have an interval and a range for the beginning date"""
    from datetime import date, timedelta

    sdate = date(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
    edate = date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))

    delta = edate - sdate       # as timedelta

    interval = interval

    dates = []
    for i in range(int(delta.days / interval) + 1):
       day1 = sdate + timedelta(days=i*interval)
       day2 = sdate + timedelta(days=i*interval +interval - 1)
       dates.append([str(day1) , str(day2)])
    return dates