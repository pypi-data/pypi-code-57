import pathlib
import os
import sys
import pandas as pd


def read_csv(filename,index=False):
    cwd = os.getcwd()
    basepath = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
    filepath = basepath / "sample" / filename
    if index == True:index=0
    else:index = None
    data = pd.read_csv(filepath,header=0,index_col=index)
    os.chdir(cwd)
    return data
