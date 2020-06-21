"""Clean users' inputs, send api requests, and clean the results.

To ensure consistent results from api requests, user inputs need to be cleaned.
Right now, the input is loose. 
No regex check to force two letter inputs for country and state codes.
"""

import json

import pandas as pd
import requests

def clean_user_inputs(queries):
    """
    Convert user inputs to match the api request input.

    Args:
        queries (string): country/us state codes

    Returns:
        string: lowercase codes and replace underscore to dash
    """
    queries = queries.lower()
    queries = queries.replace('_', '-')
    return queries

def search_cases(url):
    """
    Send queries to api and store json return. 
    The function will check for request status during the process.

    Args:
        url (string): full api query url.

    Returns:
        json: results from api.
    """
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return data

def get_url_usa_cases(states, daily):
    """    
    Build full url to send request to the covid tracking api.

    Args:
        states (string): states code to build full url.
        daily (string): show current data or daily data from first cases

    Returns:
        string: a full url to send api requests
    """
    link = 'https://covidtracking.com/api/v1/states/'
    if daily:
        extension = '/daily.json'
    else:
        extension = '/current.json'
    if states != 'all':
        url = link + states + extension
        return url
    else:
        url = link + extension
        return url

def change_number_formats(tables):
    """    
    Change number format to thousand separators.

    Args:
        tables (int/float): a pandas table.

    Returns:
        a thousand separated pandas table.
    """
    for column in tables.columns:
        tables[column] = tables[column].apply(lambda x: f'{x:,}')
    return tables

def clean_usa_results(results):
    """Function to clean pandas results and add thousand separator.

    Args:
        results : pandas table
    Returns:
        Cleaner table with numeric data formats change to thousand separators.
    """
    string_results = results.filter(['date','state'])
    number_results = results.drop(['date','state'], axis=1)
    #The api provided some data in float that display .0 in the value.
    #Change nan to 0 will allow the method to convert the data to integer. 
    #But, we can't tell the different between 0 cases vs no value provided.
    #Retain the value as it is to prevent misinterpretation.
    #number_results = number_results.fillna(0).astype('Int64')
    try:
        number_results = change_number_formats(number_results)
    except:
        pass
    final_results = pd.concat([string_results, number_results], axis=1)
    return final_results

def get_state_names(state_code):
    """
    match state codes with the state name.

    Args:
        state_code (string): two letter state codes to convert to state name.
    Returns:

    """
    #Dicts were copied from: 
    #http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
    #Change variable name for readability.
    usa_state_territories = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    state_code = state_code.upper()
    state_name = usa_state_territories.get(state_code)
    return state_name