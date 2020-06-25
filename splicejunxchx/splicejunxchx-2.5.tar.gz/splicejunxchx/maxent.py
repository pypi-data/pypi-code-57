#!usr/bin/python3
import pandas as pd
import numpy as np
import subprocess
from sys import argv

def calculate_maxEnt(jnc):
    ex_df = jnc
    if ex_df.empty:
        max_ent_series_5 = pd.DataFrame(columns = ["5bases_maxEnt", 'maxEnt_5'])
        max_ent_series_3 = pd.DataFrame(columns = ["3bases_maxEnt", 'maxEnt_3'])
    else:
        lt_5 = ex_df["5bases_maxEnt"].to_list()
        with open('data/fivemaxent.txt', mode='wt', encoding='utf-8') as fiveprfile:
            fiveprfile.write('\n'.join(lt_5))
        lt_3 = ex_df["3bases_maxEnt"].tolist()
        with open('data/threemaxent.txt', mode='wt', encoding='utf-8') as threeprfile:
            threeprfile.write('\n'.join(lt_3))
        bash_cmd_5 = "perl score5.pl data/fivemaxent.txt"
        process_5 = subprocess.Popen(bash_cmd_5.split(), stdout=subprocess.PIPE)
        output_5, error_5 = process_5.communicate()
        results_5 = output_5.decode("utf-8")
        results_in_list_5 = results_5.split('\n')
        max_ent_series_5 = pd.DataFrame([x.split('\t') for x in results_in_list_5], columns = ["5bases_maxEnt", 'maxEnt_5'])
        max_ent_series_5.drop(max_ent_series_5.tail(1).index, inplace = True)
        bash_cmd_3 = "perl score3.pl data/threemaxent.txt"
        process_3 = subprocess.Popen(bash_cmd_3.split(), stdout=subprocess.PIPE)
        output_3, error_3 = process_3.communicate()
        results_3 = output_3.decode("utf-8")
        results_in_list_3 = results_3.split('\n')
        max_ent_series_3 = pd.DataFrame([x.split('\t') for x in results_in_list_3], columns = ["3bases_maxEnt", 'maxEnt_3'])
        max_ent_series_3.drop(max_ent_series_3.tail(1).index, inplace = True)
    return max_ent_series_5, max_ent_series_3

if __name__ == '__main__':
    ex_df = pd.read_csv(argv[1])
    max_ent_series_5, max_ent_series_3 = calculate_maxEnt(ex_df)
