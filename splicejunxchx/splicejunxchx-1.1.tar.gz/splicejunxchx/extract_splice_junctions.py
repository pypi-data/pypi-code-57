#!/usr/bin/python3
import pandas as pd
import numpy as np
from sys import argv
import time
import os
import itertools

def all_spl_junctions(df):
    gtf = df
    gtf  = gtf[~gtf['transcript_id'].isin([np.nan])]
    transcripts = set(gtf['transcript_id'].tolist())
    gtf = gtf.set_index('transcript_id')
    gtf = gtf[(gtf['feature'].isin(['exon']))]
    gtf = gtf[['seqname', 'source', 'feature', 'start', 'end','strand','exon_id']]
    junctions = set()
    start = time.process_time()
    ind = 0
    for tran in transcripts:
        extract_trans = gtf.loc[gtf.index.isin([tran])]
        #extract_trans = gtf[np.in1d(gtf['transcript_id'].values, [tran])]
        #exons_of_transcript = extract_trans[np.in1d(extract_trans['feature'].values, 'exon')]
        #exons_of_transcript = extract_trans[extract_trans['feature']=='exon']
        exon_list = extract_trans[['seqname', 'start','end','strand']].to_numpy().tolist()
        exon_list.sort()
        tmp_exons = [exon_list[0]]
        for i in range(1, len(exon_list)):
            if exon_list[i][1] - tmp_exons[-1][2] < 1:
                tmp_exons[-1][2] = exon_list[i][1]
            else:
                tmp_exons.append(exon_list[i])
        for i in range(1,len(tmp_exons)):
            junctions.add((tmp_exons[0][0],tmp_exons[i-1][2]+1,tmp_exons[i][1]-1, tmp_exons[0][3]))
        if ind % 10000 == 0:
            print(time.process_time() - start, '%i of %i' % (ind,len(transcripts)))
        ind+=1
    df = pd.DataFrame(junctions, columns = ['seqname', 'start','end','strand'])
    convert_type = {'seqname': str, 'strand': str}
    df.astype(convert_type)
    return df

if __name__ == '__main__':
    gtf = pd.read_csv(argv[1], dtype = {'seqname': str})
    df = all_spl_junctions(gtf)
    # Create output csv file
    output_path = str(argv[-1]).rsplit('/',1)
    if os.path.exists(output_path[0]):
        output = df.to_csv(argv[-1],header = True, index = False)
    else:
        os.makedirs(output_path[0])
        output = df.to_csv(argv[-1],header = True, index = False)
