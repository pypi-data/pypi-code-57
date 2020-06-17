#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os

def test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(__file__)
    return ("hello am here at coname_stopwords")

def gno_inconame_stopwords():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "coname_stopwords_gno.csv")
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    CoNameStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return CoNameStopWords
    

