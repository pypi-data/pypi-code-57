#!/usr/bin/python3
import pandas as pd
import numpy as np
from sys import argv
import time
import os
from collections import Counter

def constitutive_exons(df):
    gtf = df
    gtf_transcripts = gtf[gtf['feature'] == 'transcript']
    cnt_genes = Counter(gtf_transcripts['gene_id'].tolist())
    sing_trans =  [a for a, b in cnt_genes.items() if b == 1]
    gtf_exons = gtf[gtf['feature']== 'exon']
    gtf_exons_in_transcripts = gtf_exons[gtf_exons['gene_id'].isin(sing_trans)][['seqname', 'start','end','strand','exon_id', 'gene_id']]
    multi_trans = [h for h, j in cnt_genes.items() if j > 1]
    gtf_exons_in_multi_transcripts = gtf_exons[gtf_exons['gene_id'].isin(multi_trans)][['seqname', 'start','end','strand','gene_id', 'transcript_id', 'exon_id']]
    final_exon_list = set()
    start = time.process_time()
    for gene in multi_trans:
        gene_of_interest= gtf_exons_in_multi_transcripts[gtf_exons_in_multi_transcripts['gene_id'].isin([gene])]
        total_transcripts  = len(gene_of_interest['transcript_id'].unique())
        cnt_exons = Counter(gene_of_interest['exon_id'].tolist())
        cons_exons = [m for m, n in cnt_exons.items() if n == total_transcripts]
        df_cons_exons = gene_of_interest[gene_of_interest['exon_id'].isin(cons_exons)]
        for item in df_cons_exons.itertuples():
            final_exon_list.add((item.seqname, item.start,item.end,item.strand,item.exon_id, gene))
    df = pd.DataFrame(final_exon_list, columns = ['seqname', 'start','end','strand', 'exon_id', 'gene_id'])
    fin_df = pd.concat([df,gtf_exons_in_transcripts])
    convert_type = {'seqname': str, 'strand': str}
    fin_df.astype(convert_type)
    return fin_df
'''
cnt = Counter(gtf_exons['exon_id'].tolist())
multi_exons = [k for k, v in cnt.items() if v > 1]
final_exon_list = set()
start = time.process_time()
i =0
for exn in multi_exons:
    i+=1
    exn_labels = gtf_exons[gtf_exons['exon_id'].isin([exn])]
    #exn_labels = gtf_exons[np.in1d(gtf_exons['exon_id'].values,[exn])]
    #for item in set(exn_labels['gene_id'].tolist()):
    known_genes = exn_labels['gene_id'].unique().tolist()
    for gene in known_genes:
        transcripts = gtf_transcripts[gtf_transcripts['gene_id'].isin([gene])]['transcript_id'].unique().tolist()
        #transcripts = gtf[gtf['gene_id'].isin(exn_labels['gene_id'].unique().tolist())]['transcript_id'].dropna().unique().tolist()
        #geneid = gtf[np.in1d(gtf['gene_id'].values, exn_labels['gene_id'].unique().tolist())]
        #transcripts = geneid['transcript_id'].dropna().unique().tolist()
        trans_id = set(transcripts)
        if i % 10000 == 0:
            print(time.process_time() - start)
        if trans_id == set(exn_labels[exn_labels['gene_id'].isin([gene])]['transcript_id'].tolist()):
            final_exon_list.add((exn_labels.iloc[0]['seqname'], exn_labels.iloc[0]['start'],exn_labels.iloc[0]['end'],exn_labels.iloc[0]['strand'],exn, gene))
df = pd.DataFrame(final_exon_list, columns = ['seqname', 'start','end','strand', 'exon_id', 'gene_id'])
fin_df = pd.concat([df,gtf_exons_in_transcripts])
convert_type = {'seqname': str, 'strand': str}
fin_df.astype(convert_type)
'''
if __name__ == '__main__':
    gtf = pd.read_csv(argv[1], dtype = {'seqname': str})
    fin_df = constitutive_exons(gtf)
    output_path = str(argv[-1]).rsplit('/',1)
    if os.path.exists(output_path[0]):
        output = fin_df.to_csv(argv[-1],header = True, index = False)
    else:
        os.makedirs(output_path[0])
        output = fin_df.to_csv(argv[-1],header = True, index = False)
