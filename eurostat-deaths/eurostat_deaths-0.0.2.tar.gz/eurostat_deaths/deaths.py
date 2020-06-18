
from datetime import datetime
import gzip
from io import BytesIO
import logging
import pandas as pd
import requests
import warnings

# soft int parser
def tryInt(i):
    """Soft int parser. If not possible, bypasses input.
    
    Args:
        i (any): Value to parse int from.
    """
    try: return int(i)
    except: return i

def deaths(start = None, output = None, chunksize = 1):
    """Reads data from Eurostat, filters and saves to CSV.
    
    Args:
        start (datetime, optional): Start time. Will be rounded to week. Endtime is always end of data.
                                    Default is all the data (no filtering).
        output (str, optional): Output file. If None, returns processed dataframe. Default is "output.csv".
        chunksize (int, optional): Size of chunk to process data by (in thousands). Default is 1 (1000 lines in chunk).
    """
    # download zip
    logging.warning("input has over 200MB, processing will take a few minutes (for me 15 min)")
    logging.info("downloading zip file")
    url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mweek3.tsv.gz'
    zipinput = requests.get(url, stream=True)
    
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
                .apply(tryInt)
            chunk = chunk\
                .drop(['unit'], axis = 1)
        
            # parse age groups
            chunk['age'] = chunk['age']\
                .replace({'Y_LT5': 'Y0-4', 'Y_GE90': 'Y90'})\
                .replace({'-':'_'})\
                .apply(lambda i: i[1:])
        
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
            if output is not None:
                if i == 0: chunk.to_csv(output, mode='w', header=True, index=False)
                else: chunk.to_csv(output, mode='a', header=False, index=False)
            else:
                if data is None: data = data.append(chunk)
                else: data = data.concat(chunk)
            
            logging.info(f"parsed {chunksize * (i + 1) * 10**3}/64000 lines")


def _parse_args():
    """Parses arguments for direct module execution."""
    # parse arguments
    import argparse        
    def check_positive(value):
        ivalue = int(value)
        if ivalue <= 0: raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return ivalue
    def check_date(value):
        # dates
        try: return datetime.strptime(f"{value}-01-01", "%Y-%m-%d")
        except: pass
        try: return datetime.strptime(value, "%Y-%m-%d")
        except: pass
        # datetime
        try: return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except: pass
        # week of year
        try: return datetime.strptime(f"{value}-1", "%Y-W%W-%w")
        except: pass
        
        raise argparse.ArgumentTypeError(f"{value} is an invalid date/week value")
    
    # create argument records
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Directs the output to a name of your choice.")
    parser.add_argument("-n", "--chunksize", type=check_positive, help="Number of lines in chunk (in thousands).")
    parser.add_argument("-s", "--start", type=check_date, help="Start date.")
    parser.add_argument("-v", "--verbose", action='count', default=0, help="Sets verbose log (logging level INFO).")
    args = parser.parse_args()
    # parse arguments
    return {'--output': args.output if args.output else "output.csv",
            '--chunksize': args.chunksize if args.chunksize else 1,
            '--start': args.start if args.start else None,
            '--verbose': bool(args.verbose) if args.verbose else False}

if __name__ == "__main__":
    # parse arguments
    args = _parse_args()
    # set verbose
    if args['--verbose']:
        logging.basicConfig(level = logging.INFO)
    
    # call main function
    deaths(start = args['--start'], output = args['--output'], chunksize = args['--chunksize'])

__all__ = ["deaths"]