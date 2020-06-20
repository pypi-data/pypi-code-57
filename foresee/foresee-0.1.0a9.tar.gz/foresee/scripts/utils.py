# -*- coding: utf-8 -*-
"""
Local utility functions 
"""

import os
import json
import pandas as pd
import numpy as np
from io import StringIO
from importlib_resources import files

def read_json(file_name):
    """[summary]

    Parameters
    ----------
    file_name : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    
    json_string = files('foresee.params').joinpath(file_name).read_text()
    
    return json.loads(json_string.replace('\n', ' ').replace('\t', ' '))


def read_csv(file_name):
    """[summary]

    Parameters
    ----------
    file_name : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    
    
    data_txt = files('foresee.data').joinpath(file_name).read_text()
    
    return pd.read_csv(StringIO(data_txt))
