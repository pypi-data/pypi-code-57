
from datetime import datetime
import gzip
from io import BytesIO
import logging
import os

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

def populations(output = False, chunksize = 10):
    now = datetime.now()
    if output:
        os.mkdir("output")
        output_file = f"output/{now.strftime('%Y-%m-%d')}_population.csv"
    # download zip
    url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_pjangrp3.tsv.gz'
    zipinput = requests.get(url, stream = True)
    
    # unzip tsv
    data = None
    with gzip.GzipFile(fileobj = BytesIO(zipinput.content), mode = "r") as z:
        logging.info("parsing zip file")
        
        for i,chunk in enumerate(pd.read_csv(z, sep=",|\t", engine = "python", chunksize = chunksize * 10**3)):
            # columns
            chunk.columns = [c.strip() for c in chunk.columns]
            data_columns = set(chunk.columns) - {'unit','sex','age','geo\\time'}
            
            # parse data
            chunk[ list(data_columns) ] = chunk[ list(data_columns) ]\
                .replace({r'\s*:\s*': None, r'[^0-9]*([0-9]+)[^0-9]*': r'\1'}, regex = True)\
                .applymap(tryInt)
            chunk = chunk\
                .drop(['unit'], axis = 1)
            
            # parse age groups
            chunk['age'] = chunk['age']\
                .replace({'Y_LT5': 'Y0-4', 'Y_GE90': 'Y90', 'Y_GE85': 'Y85'})\
                .replace({r'(.*)-(.*)':r'\1_\2', r'Y(.*)':r'\1'}, regex = True)
            # output
            if output:
                if i == 0: chunk.to_csv(output_file, mode='w', header=True, index=False)
                else: chunk.to_csv(output_file, mode='a', header=False, index=False)
            
            if data is None: data = chunk
            else: data = data.append(chunk)
            
            logging.info(f"parsed {chunksize*i*10**3 + min(chunksize*10**3, chunk.shape[0])}/131880 lines")
    
    return data
        
__all__ = ["populations"]

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    data = populations()
    print(data.age.unique())