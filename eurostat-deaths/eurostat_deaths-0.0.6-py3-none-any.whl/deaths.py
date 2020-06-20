
from datetime import datetime,timedelta
import gzip
from io import BytesIO
import logging
import os
import pickle
import warnings

import pandas as pd
import requests

# soft int parser
def tryInt(i):
    """Soft int parser. If not possible, bypasses input.
    
    Args:
        i (any): Value to parse int from.
    """
    try: return int(i)
    except: return i

def getDeaths(timestamp, cache = False, cache_age = timedelta(days = 7), chunksize = 1, output = None):
    from_cache = False
    if cache:
        newest_version = None
        for f in os.listdir("output/"):
            try:
                version = datetime.strptime(f, "%Y-%m-%d_raw.tsv.gz")
                if abs(version - timestamp) < cache_age:
                    newest_version = version if not newest_version or version > newest_version else newest_version
                else:
                    logging.info(f"found version {version} but older than cache_age tolerance")
            except: pass
            
        if newest_version:
            from_cache = True
            logging.info(f"using version from {newest_version}")
            # unzip tsv
            with gzip.open(f"output/{newest_version.strftime('%Y-%m-%d')}_raw.tsv.gz") as z:
                for chunk in pd.read_csv(z, sep=",|\t", engine = "python", chunksize = chunksize * 10**3):
                    yield chunk
        else:
            logging.info("not found any cached version")
     
    if not from_cache:
        # download zip
        logging.warning("input has over 200MB, processing will take a few minutes (for me 15 min)")
        url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mweek3.tsv.gz'
        zipinput = requests.get(url, stream=True)
        if output:
            logging.info("writing raw output to file")
            with open(f"output/{timestamp.strftime('%Y-%m-%d')}_raw.tsv.gz", "wb") as fd:
                for chunk in zipinput.iter_content(chunk_size = chunksize * 10**3):
                    fd.write(chunk)
            logging.info("written raw output to file")
            zipinput = requests.get(url, stream=True)
            
        # unzip tsv
        with gzip.GzipFile(fileobj = BytesIO(zipinput.content), mode = "r") as z:
            logging.info("parsing zip file")
        
            for chunk in pd.read_csv(z, sep=",|\t", engine = "python", chunksize = chunksize * 10**3):
                yield chunk

def check_cache(timestamp, cache_age):
    newest_version = None
    for f in os.listdir("output/"):
        try:
            version = datetime.strptime(f, "%Y-%m-%d.pickle")
            if abs(version - timestamp) < cache_age:
                newest_version = version if not newest_version or version > newest_version else newest_version
            else:
                logging.info(f"found version {version} but older than cache_age tolerance")
        except: pass
    return f"output/{newest_version.strftime('%Y-%m-%d')}.pickle" 
                
def deaths(countries = None, start = None, chunksize = 1,
           output = True, cache = True, cache_age = timedelta(days = 7)):
    """Reads data from Eurostat, filters and saves to CSV.
    
    Args:
        start (datetime, optional): Start time. Will be rounded to week. Endtime is always end of data.
                                    Default is all the data (no filtering).
        output (str, optional): Output file. If None, returns processed dataframe. Default is "output.csv".
        chunksize (int, optional): Size of chunk to process data by (in thousands). Default is 1 (1000 lines in chunk).
    """
    if output or cache:
        os.mkdir("output")
    now = datetime.now()
    if cache:
        x = check_cache(now, cache_age)
        if x:
            print(f"loading {x}")
            with open(x, "rb") as pf:
                return pickle.load(pf)
        print(x)
        
    
    data = None
    for i,chunk in enumerate(getDeaths(now, output = output, chunksize = chunksize, cache = cache, cache_age = cache_age)):
        # columns
        chunk.columns = [c.strip() for c in chunk.columns]
        data_columns = set(chunk.columns) - {'unit','sex','age','geo\\time'}
            
        # filter data
        if countries:
            f = None
            for pre in countries:
                matches = chunk['geo\\time'].str.startswith(pre)
                f = f | matches if f else matches
            chunk = chunk[f]
            # all chunk filtered out
            if len(chunk.index) == 0:
                logging.info(f"whole chunk filtered out")
                continue
                
        # parse data
        chunk[ list(data_columns) ] = chunk.loc[ :,list(data_columns) ]\
            .replace({r'\s*:\s*': None, r'[^0-9]*([0-9]+)[^0-9]*': r'\1'}, regex = True)\
            .apply(tryInt)
        chunk = chunk.loc[:,:]\
            .drop(['unit'], axis = 1)
        
        # parse age groups
        chunk['age'] = chunk.loc[:,'age']\
            .replace({'Y_LT5': 'Y0-4', 'Y_GE90': 'Y90', 'Y_GE85': 'Y85'})\
            .replace({r'(.*)-(.*)':r'\1_\2', r'Y(.*)':r'\1'}, regex = True)
        # filter weeks
        if start is not None and start > datetime(2000,1,1):
            year, week = start.year, start.isocalendar()[1]
            cols_to_remove = [f"{y}W{str(w).zfill(2)}" for y in range(2000,year + 1) for w in range(1,54) if y < year or w < week]
            for col in cols_to_remove:
                try:
                    chunk = chunk\
                        .drop(col, axis = 1)
                except: pass
        # output
        if output:
            output_file = f"output/{now.strftime('%Y-%m-%d')}.csv"
            if i == 0: chunk.to_csv(output_file, mode='w', header=True, index=False)
            else: chunk.to_csv(output_file, mode='a', header=False, index=False)
            
        if data is None: data = chunk
        else: data = data.append(chunk)
            
        logging.info(f"parsed {chunksize * (i + 1) * 10**3}/64000 lines")
    
    with open(f"output/{now.strftime('%Y-%m-%d')}.pickle", "wb") as pf:
        pickle.dump(data, pf)
    return data

__all__ = ["deaths"]