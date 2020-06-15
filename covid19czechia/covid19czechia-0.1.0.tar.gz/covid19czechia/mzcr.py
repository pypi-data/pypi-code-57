
from datetime import datetime
from io import StringIO
import warnings

import pandas as pd
import requests

# change to have different age_groups
def _group5_to_range(group):
    return group * 5, group * 5 + 4
def _age_to_group5(age):
    group = age // 5
    group_range = _group5_to_range(group)
    return f"{group_range[0]}_{group_range[1]}"

age_to_group = _age_to_group5

def deaths_covid(level = 1):
    """Returns deaths for COVID-19 in Czechia.
    
    The deaths are aggregated by week, age group (by 5 years) and sex.
    Setting of parameter *level* sets granularity of administrative unit.
    
    Args:
        level (int, optional): Granularity of administrative unit.
            * by country (level = 1) = default
            * by region (level = 2)
            * by district (level = 3)
    """
    # fallback
    if level > 3 or level < 1:
        warnings.warn("invalid level")
        return None
    
    # download
    mzcr_deaths_url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv'
    mzcr_deaths_response = requests.get(mzcr_deaths_url)
    
    # read csv
    x = pd.read_csv( StringIO(mzcr_deaths_response.text) )
    x.columns = ["date","age","sex","region","district"]
    x["date"] = x["date"].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
    x["sex"] = x["sex"].apply(lambda s: {"M":"M", "Z":"F"}[s])
    # alter values
    x["age_group"] = x["age"].apply(age_to_group)
    x["week"] = x["date"].apply(lambda dt: dt.isocalendar()[1])
    
    # country level
    if level == 1:
        x = x.groupby(["week","age_group","sex"]).size().reset_index(name = 'deaths')
    # region level
    elif level == 2:
        x = x.groupby(["week","age_group","sex","region"]).size().reset_index(name = 'deaths')
    # district level
    elif level == 3:
        x = x.groupby(["week","age_group","sex","region","district"]).size().reset_index(name = 'deaths')
    
    return x

def set_age_groups(callback):
    global age_to_group
    age_to_group = callback

__all__ = ["deaths_covid","set_age_groups","age_to_group"]

    