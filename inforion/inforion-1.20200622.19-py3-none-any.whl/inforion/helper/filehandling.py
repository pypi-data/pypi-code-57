

import os
import sys

import pandas as pd

def checkfiletype(filepath):

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(filepath)[-1].lower()
    print (ext)
    # Now we can simply use == to check for equality, no need for wildcards.

    
    if ext == ".csv":
        print ("file is csv")
    elif ext == ".xlsx" or ext == ".xls":
        print ("file is excel")
    else:
        print ("Inputfile Type is not supported")
        sys.exit(0)
    
    return ext

def loadfile(ext,file):

    if ext == ".csv":
        df = pd.read_csv(file)
    elif ext == ".xlsx" or ext == ".xls":
        df = pd.read_excel(file)
    return df