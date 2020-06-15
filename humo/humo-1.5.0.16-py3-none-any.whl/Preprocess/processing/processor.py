import numpy as np
import pandas as pd
from collections import namedtuple


def getdataflags(df):
    """
    getdataflags
    """
    targets = ["Devices","Model Outputs","Trajectories"]
    num = []
    for flag in targets:
        try:
            num.append(df[df[0].str.contains(flag) == True].index[0])
        except:
            print("Error")
    Ntuple = namedtuple("flags",["device","model","marker"])
    return Ntuple(*num)

def getNanflags(df):
    """
    getNanflags
    """
    nanlist = df.isnull().values
    return np.array(df[nanlist].index)

def getDataIndex(dkind, dataflags, nanflags):
    """
    getDataIndex
    """
    if dkind == "Device":
        return np.abs(nanflags - dataflags.device).argmin(), nanflags
    elif dkind == "Model":
        _nanflags = nanflags[nanflags > dataflags.model]
        return np.abs(_nanflags - dataflags.model).argmin(), _nanflags
    elif dkind == "Marker":
        _nanflags = nanflags[nanflags > dataflags.marker]
        return np.abs(_nanflags - dataflags.marker).argmin(), _nanflags
    else:
        pass

def getColLength(df,dkind,dataflags,nanflags,p):
    """
    getDataIndex
    """
    dIndex,nanflags = getDataIndex(dkind, dataflags, nanflags)
    data = pd.read_csv(
        p,
        header = nanflags[dIndex]+1,
        nrows = 1,
        dtype = object
    )
    cols = []
    for i in data.columns:
        if "Unnamed" in i:
            pass
        else:
            cols.append(i)
    return len(cols)

def getData(df,dkind, dataflags, nanflags, p):
    """
    getDataIndex
    """
    dIndex,nanflags = getDataIndex(dkind, dataflags, nanflags)
    colLen = getColLength(df, dkind, dataflags, nanflags, p)
    if dkind == "Device":
        data = pd.read_csv(
                    p,
                    header = nanflags[dIndex],
                    nrows = nanflags[dIndex + 2]-3,
                    index_col = 0,
                    usecols=np.arange(colLen),
                    dtype=object
                    )[62:-60]
    elif dkind == "Model":
        data = pd.read_csv(
                    p,
                    header = nanflags[dIndex],
                    nrows = nanflags[dIndex + 2] - nanflags[dIndex + 1] + 1,
                    index_col = 0,
                    usecols = np.arange(colLen),
                    dtype = object
                    )[8:-6]
    elif dkind == "Marker":
        data = pd.read_csv(
                    p,
                    header = nanflags[dIndex],
                    index_col = 0,
                    usecols = np.arange(colLen),
                    dtype = object
                    )[8:-6]
    else:
        pass
    return data

def getData2(df, dkind, dataflags, nanflags, p):
    dIndex,nanflags = getDataIndex(dkind, dataflags, nanflags)
    colLen = getColLength(df, dkind, dataflags, nanflags, p)
    if dkind == "Device":
        data = pd.read_csv(
                    p,
                    header = nanflags[dIndex] + 2,
                    nrows = 5,
                    index_col = 0,
                    usecols=np.arange(colLen),
                    dtype=object
                    )
        return data
    else:
        pass


