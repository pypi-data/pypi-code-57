# Kornpob Bhirombhakdi 20200331
# This is a very specific helper for aXe to go with a new version of sextractor.

import pandas as pd
import copy
import numpy as np

def read_catalog(catalog):
    x = open(catalog,'r')
    colname = []
    values = []
    for i in x.readlines():
        if i[0]=='#':
            colname.append(i)
        else:
            x2 = np.array(i.split(),dtype=np.double)
            values.append(x2)
    x.close()
    x3 = pd.DataFrame(values,columns=colname)
    x3 = x3.astype({colname[2]:'int64'})
    return copy.deepcopy(x3)

def change_magiso2magwavelength(catalog,wavelength):
    x = read_catalog(catalog)
    y = x.columns[11].split()
    y[2] = 'MAG_F'+str(int(wavelength))
    z = ' '.join(y) + '\n'
    x.rename(columns={x.columns[11]:z},inplace=True)
    write_catalog(catalog,x)
    
def write_catalog(catalog,dataframe):
    x = open(catalog,'w')
    for i in dataframe.columns:
        x.writelines(i)
    for i in dataframe.values:
        string = ' '.join(i[0:2].astype(str))
        string = string + ' ' + str(i[2].astype(int))
        string = string + ' ' + ' '.join(i[3:].astype(str)) + '\n'
        x.writelines(string)
    x.close()

def change_catalog_order(catalog):
    x = read_catalog(catalog)
    y = x.T.iloc[0:14].copy()
    z = y.copy()
    z1,z11 = z.iloc[11].name,z.iloc[12].name
    zz,zz2 = z1.split(),z11.split()
    zz[1],zz2[1] = '13','12'
    z2 = ' '.join(zz) + '\n'
    z22 = ' '.join(zz2) + '\n'
    z.rename(index={z1:z2,z11:z22}, inplace = True)
    tmp = z.iloc[0:11]
    tmp = tmp.append(z.iloc[12])
    tmp = tmp.append(z.iloc[11])
    tmp = tmp.append(z.iloc[13])
    tmpp = tmp.T.copy()
    write_catalog(catalog,tmpp)
    
def remove_bad_entry(catalog,maglimit=27.):
    x = read_catalog(catalog)
    for i in x.columns:
        for j in i.split():
            if j.split('_')[0] == 'MAG':
                xx = i
                break
    tmp = x[x[xx]<maglimit].copy()
    write_catalog(catalog,tmp)

def one_source(catalog,ID):
    x = read_catalog(catalog)
    for i in x.columns:
        for j in i.split():
            if j == 'NUMBER':
                xx = i
                break
    df = x[x[xx]==ID].copy()
    return df
    
def select_source(v1,v2,catalog,method='RADEC'):
    # check variables
    if method in {'RADEC','XY'}:
        if not v2:
            raise ValueError('v2 must be specified given method.')
    if method=='RADEC':
        CATALOG = read_catalog(catalog)
        x0 = CATALOG.iloc[:,3].values
        y0 = CATALOG.iloc[:,4].values
        dx,dy = x0-v1,y0-v2
        dd = np.sqrt(dx**2 + dy**2)
        index = np.argmin(dd)
    elif method=='XY':
        CATALOG = read_catalog(catalog)
        x0 = CATALOG.iloc[:,0].values
        y0 = CATALOG.iloc[:,1].values
        dx,dy = x0-v1,y0-v2
        dd = np.sqrt(dx**2 + dy**2)
        index = np.argmin(dd)
    elif method=='ID':
        CATALOG = read_catalog(catalog)
        x0 = CATALOG.iloc[:,2].values
        dx = x0-v1
        dd = np.sqrt(dx**2)
        index = np.argmin(dd)
    else:
        raise ValueError('select_source(method) is not allowed.')
    return CATALOG.iloc[index,:]
