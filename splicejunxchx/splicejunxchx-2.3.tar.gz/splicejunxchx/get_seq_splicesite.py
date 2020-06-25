#!usr/local/bin
import pandas as pd
import numpy as np
from sys import argv
import subprocess


def sequence_splice_site(sp_junc, fasta_file):
    part = sp_junc
    part = part[['chr','first_base','last_base','motif','STAR_annotation','strand']]
    part['first_base'] = part['first_base']
    #part['chr'] = 'chr' + part['chr'].astype(str)
    part['strand'] = part['strand'].apply(lambda x: '+' if x ==1 else ('-' if x==2 else np.nan))

    cat1 = pd.DataFrame(columns = ['chr','start','end','def','ss','strand'])
    cat2 = pd.DataFrame(columns = ['chr','start','end','def','ss','strand'])
    cat1['chr'] = part['chr']
    cat1['start'] = part['first_base'] - 26
    cat1['end'] = part['first_base'] +25
    cat1['strand'] = part['strand']
    cat1['ss'] = part['strand'].apply(lambda x: 3 if x =='-' else 5)
    cat1['def'] = part.index +',' + cat1['ss'].astype(str)

    cat2['chr'] = part['chr']
    cat2['start'] = part['last_base'] -26
    cat2['end'] = part['last_base'] +25
    cat2['strand'] = part['strand']
    cat2['ss'] = part['strand'].apply(lambda x: 5 if x =='-' else 3)
    cat2['def'] = part.index +',' + cat2['ss'].astype(str)

    fin = pd.concat([cat1,cat2])

    fin.to_csv('data/bedfileex2.bed', sep ='\t', header = False, index = False)
    bash_cmd = "bedtools getfasta -fi %s -bed data/bedfileex2.bed -s -name -tab" % fasta_file
    process= subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    results = output.decode("utf-8")
    results_in_list= results.split('\n')
    seqs = pd.DataFrame([x.split('\t') for x in results_in_list], columns = ["names", 'seq'])
    seqs['id_jnc'] = seqs['names'].str.split(':', n=1, expand = True)[0]
    seqs[['JNC_ID', 'site']] = seqs.id_jnc.apply(lambda x: pd.Series(str(x).split(',')))
    five_pr_seq = seqs.loc[seqs.site.isin(['5']), 'seq']
    three_pr_seq = seqs.loc[seqs.site.isin(['3']), 'seq']
    return seqs
if __name__ == '__main__':
    col_names = ['chr','first_base', 'last_base','strand','motif','STAR_annotation','uniq_reads', 'no_reads','overhang']
    jnc_df =  pd.read_csv(argv[1], names = col_names, sep = '\t', dtype = {'chr': str})
    jncid_list = []
    for id in range(1,len(jnc_df.index)+1):
        jncid_list.append("JNC" + str(id))
    jnc_df['JNC_ID'] = jncid_list
    jnc_df.set_index(['JNC_ID'], inplace = True)
    seq = sequence_splice_site(part, argv[2])
