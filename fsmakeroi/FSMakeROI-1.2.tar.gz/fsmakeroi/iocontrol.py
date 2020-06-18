"""
Control file input/output for FSMakeROI
"""

#---------------------------------------------------------------------
# Package Management
#---------------------------------------------------------------------
import os
import os.path as op
import numpy as np
import pandas as pd

#---------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------
def readlut(path):
    """
    Reads Freesurfer's LUT text file and loads them into an array
    
    Parameters
    ----------
    path : str
        Path to FS LUT text file
    
    Returns
    -------
    DataFrame
        A 2D Pandas DataFrame containing LUT information
    """
    if not op.exists(path):
        raise FileNotFoundError('Path to FS LUT {} not '
        'found'.format(path))
    lut = pd.read_csv(
        path,
        skip_blank_lines=True,
        skipinitialspace=True,
        sep=' '
    )
    return lut

def readroi(path):
    """
    Reads list of ROI text file
    
    Parameters
    ----------
    path : str
        Path to ROI list file
    
    Returns
    -------
    list of int
        List of ROIs in text file
    """
    if not op.exists(path):
        raise FileNotFoundError('Path to ROI file {} not '
        'found'.format(path))
    return [int(line.strip('\n')) for line in open(path, 'r')]


