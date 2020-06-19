import pandas as pd
from six.moves import urllib
import os
import tempfile
import shutil
import zipfile


# Download twi_data from github
def download(directory, filename):
    url = 'https://github.com/corvid-ai/data-repo/raw/feature/compressed-data/src/compressed/sample.zip'
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        return filepath
    else:
        _, zipped_filepath = tempfile.mkstemp(suffix='.zip')
        print('Downloading %s to %s' % (url, filepath))
        urllib.request.urlretrieve(url, zipped_filepath)  
        with zipfile.ZipFile(zipped_filepath, 'r') as zip_ref:
            zip_ref.extractall('../data/')
        os.remove(zipped_filepath)
        filepath = '../data/twi-wikipedia.csv'
        return filepath

directory = '../data/'
filename = 'twi-wikipedia.csv'

def dataset():
    filepath = download(directory,filename)
    twi_dataset = pd.read_csv(filepath)
    return twi_dataset