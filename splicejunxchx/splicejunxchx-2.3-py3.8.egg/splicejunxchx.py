#!/usr/bin/env python3
import pandas as pd
import numpy as np
import argparse
from sys import argv
import subprocess
import time
from splicejunxchx.func_file import *
from splicejunxchx.get_seq_splicesite import *
from splicejunxchx.extract_splice_junctions import *
from splicejunxchx.constitutive_exons import *
from splicejunxchx.maxent import *
import os
pd.options.mode.chained_assignment = None
''' The following code is able to take in a SJ.out.tab file with splice junctions
and a GTF file with genome info to parse specific information about the location
of the splice junctions

Importarnt requirements for this program to work:
Python 3.6 at least in order to utilze the gtf2csv function from github
Install pandas and numpy
Install bedtools
Install bigWigToBedGraph
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs = 2, help = 'A GTF file (gtf.gz or .csv) and a STAR file (.out.tab) with information about splice junctions')
    parser.add_argument('-seqs','--sequence_file', help = 'Fasta file (.fa) for sequences of GTF file')
    parser.add_argument('-supp', '--support_files', nargs = 2, help = 'Supply the splice junction file (.csv) and constitutive exon file (.csv)')
    parser.add_argument('-phyloP', '--phyloPscores', nargs = 2, help = 'phyloP score file (.bw) and the number of nucleotides around each splice site (must be even number and less than 200)')
    parser.add_argument('-maxEnt', '--maxEntscore', action = 'store_true',help = 'If maxEnt, perl files and splicemodel directory are included in root then you can calculate the maxEnt score by adding this optional flag')
    parser.add_argument('output_file', help = 'Name of output file (.csv) to save final dataframe')
    args = parser.parse_args()

    if (args.maxEntscore) and (args.sequence_file == None):
        sys.exit("Cannot calculate maxEnt without proper sequence file (-seqs)")
    if args.maxEntscore:
        if args.sequence_file == None:
            sys.exit("Cannot calculate maxEnt without proper sequence file (-seqs)")
        if not os.path.exists('score5.pl'):
            sys.exit("Cannot find score5.pl in the root directory, look at README to donwload")
        if not os.path.exists('score3.pl'):
            sys.exit("Cannot find score3.pl in the root directory, look at README to donwload")
        if not os.path.exists('me2x5'):
            sys.exit("Cannot find me2x5, look at README to donwload")
        if not os.path.exists('splicemodels'):
            sys.exit("Cannot find splicemodels in the root directory, look at README to donwload")

    if not os.path.exists('data'):
        os.makedirs('data')
    # Convert a GTF file to dataframe/CSV
    filename = str(args.inputs[0])
    if filename.endswith('.gtf.gz'): # if file is GTF then need to use gtf2csv in bash
        gtfcsvfile = filename[:-7] + '.csv'
        bash_cmd = "gtf2csv -f %s" % args.inputs[0]
        process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        temp = filename[:-7]
    elif filename.endswith('.gtf'): # if file is GTF then need to use gtf2csv in bash
        gtfcsvfile = filename[:-4] + '.csv'
        bash_cmd = "gtf2csv -f %s" % args.inputs[0]
        process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        temp = filename[:-4]
    elif filename.endswith('.csv'):# if file is already csv then just load into df
        gtfcsvfile = filename
        temp = filename[:-4]
    else:
        sys.exit("Need GTF file (.gtf.gz or .gtf) or CSV file for initial input")
    gtf_df = pd.read_csv(gtfcsvfile, dtype = {'seqname': str})

    # Convert SJ.out.tab file to dataframe

    jnc_filename= str(args.inputs[1])
    if jnc_filename.endswith('out.tab'): # Create dataframe for SJ.out.tab
        col_names = ['chr','first_base', 'last_base','strand','motif','STAR_annotation','uniq_reads', 'no_reads','overhang']
        jnc_df =  pd.read_csv(args.inputs[1], names = col_names, sep = '\t', dtype = {'chr': str})
        jnc_df['unidentified_strand'] = [1 if x == 0 else 0 for x in jnc_df['strand']]
        jncid_list = []
        for id in range(1,len(jnc_df.index)+1):
            jncid_list.append("JNC" + str(id))
        jnc_df['JNC_ID'] = jncid_list

    # Take splice junctions with unidentified strand and duplicate them to assume ones lies on the positive strand and the other on the negative strand

    no_strand_info = jnc_df[jnc_df['strand']==0]
    change_strand = set()
    for jncid in no_strand_info.itertuples():
        change_strand.add((jncid.JNC_ID + '.1', jncid.chr, jncid.first_base, jncid.last_base, 1, jncid.motif, jncid.STAR_annotation, jncid.uniq_reads, jncid.no_reads, jncid.overhang,jncid.unidentified_strand))
        change_strand.add((jncid.JNC_ID + '.2', jncid.chr, jncid.first_base, jncid.last_base, 2, jncid.motif, jncid.STAR_annotation, jncid.uniq_reads, jncid.no_reads, jncid.overhang, jncid.unidentified_strand))
    no_strand_df = pd.DataFrame(change_strand, columns = ['JNC_ID','chr','first_base', 'last_base','strand','motif','STAR_annotation','uniq_reads', 'no_reads','overhang','unidentified_strand'])
    jnc_df = jnc_df.append(no_strand_df, ignore_index=True)
    jnc_df.set_index(['JNC_ID'], inplace = True)

    # All Splice junction using extract_spl_junc file
    # All constitutive exons using cons_exons file
    if (args.support_files != None):
        all_spl_junc = pd.read_csv(args.support_files[0])
        cons_exons = pd.read_csv(args.support_files[1])
    else:
        all_spl_junc = all_spl_junctions(gtf_df)
        cons_exons = constitutive_exons(gtf_df)
        all_spl_junc.to_csv('data/all_spl_junc_%s.csv', index = False) % temp.rsplit('/',1)[-1]
        cons_exons.to_csv('data/cons_exons_%s.csv', index = False) % temp.rsplit('/',1)[-1]
    #  Final df to develop
    #final_df = jnc_df.iloc[0:100,0:6]
    final_df = jnc_df.iloc[:,np.r_[0:8,9]].copy()
    #final_df = jnc_df[col_names[0:6]]
    jnc_df = jnc_df.sort_values(by = ['chr','strand'])
    # add_cols is all the data we want to gather and have in our final datarame
    add_cols = ["5_in_gene","5_in_exon","5_in_constitutiveexon","5_in_intron", "5_in_constitutiveintron","5_in_fiveprimeutr","5_in_threeprimeutr","5_in_CDS","5_in_startcodon","5_in_stopcodon",  "5_in_strandofgene", "3_in_gene", "3_in_exon",  "3_in_constitutiveexon",
                "3_in_intron","3_in_constitutiveintron","3_in_fiveprimeutr","3_in_threeprimeutr","3_in_CDS","3_in_startcodon","3_in_stopcodon","3_in_strandofgene"]

    if args.sequence_file != None:
        seq_info = ["5ss_sequence_51bp", "3ss_sequence_51bp", "5ss_sequence_2bp","3ss_sequence_2bp","5bases_maxEnt","3bases_maxEnt", "5score_maxEnt","3score_maxEnt"]
    else:
        seq_info = []
    if args.phyloPscores != None:
        phyloP_cols = ["5phyloPscore", "3phyloPscore", "5phyloPlist", "3phyloPlist"]
    else:
        phyloP_cols = []

    splice_sites_nearby_cols = ["5annotated", "3annotated",
                "5ss_to_upstream5ss", "5ss_to_upstream3ss",
                "5ss_to_downstream5ss","5ss_to_downstream3ss",
                "3ss_to_upstream5ss", "3ss_to_upstream3ss",
                "3ss_to_downstream5ss","3ss_to_downstream3ss"]

    all_cols = add_cols +splice_sites_nearby_cols+seq_info+phyloP_cols
    for col in all_cols:
        final_df[col] = 'NA'  #np.nan
        if col in add_cols:
            final_df[col] = final_df[col].astype('object')
        elif col in ["5_in_specificregions","3_in_specificregions", "5phyloPlist", "3phyloPlist", "5_in_otherregions", "3_in_otherregions"]:
            final_df[col] = final_df[col].astype('object')
        elif col in seq_info:
            final_df[col] = final_df[col].astype('str')
    print(final_df.head(10))

    # Seperate GTF file into positive strand and negative strand data to make it easier to search through
    pos_strand = gtf_df['strand'] == '+'
    neg_strand = gtf_df['strand'] == '-'
    pos_gtf = gtf_df[pos_strand]
    neg_gtf = gtf_df[neg_strand]

    # Search each junction through GTF file

    five_prime_str = "5_"
    five_prime_cols = list(filter(lambda x: five_prime_str in x, final_df.columns))
    three_prime_str = "3_"
    three_prime_cols = list(filter(lambda x: three_prime_str in x, final_df.columns))
    '''
    jnc_df = jnc_df.iloc[0:100,:]
    for jnc, fb, lb, strand in zip(jnc_df.index, jnc_df['first_base'], jnc_df['last_base'], jnc_df['strand']):
         jnc_time = time.process_time()
         if strand== 1:
             gtf_search = pos_gtf
             five_dict, three_dict = extract_spljnc_alt(fb,lb, gtf_search, strand)
         elif strand == 2:
             gtf_search = neg_gtf
             five_dict, three_dict = extract_spljnc_alt(fb,lb, gtf_search, strand)
         else:
             continue
         for val in five_prime_cols:
             final_df.at[jnc,val] = five_dict[val.split('_')[-1]]
         for val in three_prime_cols:
             final_df.at[jnc,val] = three_dict[val.split('_')[-1]]
         jnc_time_fin = time.process_time()
         elapsed_time = jnc_time_fin - jnc_time
         print(elapsed_time)
    print(final_df.iloc[0:5,14:])
    '''
    start = time.process_time()
    if args.sequence_file != None:
        seqs = sequence_splice_site(final_df[~final_df.strand.isin([0])], args.sequence_file) # Sequence file
    gtfseqnamelist = set(gtf_df['seqname'].tolist())
    prev_jncrow_chr = np.nan # temp variable to compare previous iteration
    prev_jncrow_strand = np.nan # temp variable to compare previous iteration
    i = 0
    for jncrow in jnc_df.itertuples(): # iterate through each splice junction
        i+=1
        if (jncrow.strand == 1) & (jncrow.chr in gtfseqnamelist): # Determine if its on the + or - strand
            gtf_search = pos_gtf
            if (jncrow.strand == prev_jncrow_strand) and (jncrow.chr == prev_jncrow_chr): # Determine if its on the same strand/chr as the previous iteration to save time
                gtf_chr = prev_gtf_chr
                gtf_exons = prev_gtf_exons
                spl_junc_df = prev_spl_junc_df
            else: # Create 3 dataframes: 1. gtf_chr corresponding chr in gtf file 2. corresponding exons from gtf file 3. splice junctions found on that chromosome and strand
                gtf_chr = gtf_search[np.in1d(gtf_search['seqname'].values, [jncrow.chr])]
                gtf_exons = gtf_chr[np.in1d(gtf_chr['feature'].values, ['exon'])]
                spl_junc_df = all_spl_junc[np.in1d(all_spl_junc['seqname'].values,[jncrow.chr])]
                spl_junc_df = spl_junc_df[np.in1d(spl_junc_df['strand'].values, ['+'])]
            five_dict, three_dict = extract_spljnc(jncrow, gtf_chr, '+', cons_exons, gtf_exons) # outputs dictionary of 5' and 3' info to add to final dataframe
            #final_df.at[jncrow.Index,'alternative_splicing'] = alt_vs_cons_splicing(jncrow, gtf_chr)
            ss_nearby = closest_splice_sites(jncrow, spl_junc_df)

        elif (jncrow.strand == 2) & (jncrow.chr in gtfseqnamelist):
            gtf_search = neg_gtf
            if (jncrow.strand == prev_jncrow_strand) and (jncrow.chr == prev_jncrow_chr):
                gtf_chr = prev_gtf_chr
                gtf_exons = prev_gtf_exons
                spl_junc_df = prev_spl_junc_df
            else:
                gtf_chr = gtf_search[np.in1d(gtf_search['seqname'].values, [jncrow.chr])]
                gtf_exons = gtf_chr[np.in1d(gtf_chr['feature'].values, ['exon'])]
                spl_junc_df = all_spl_junc[np.in1d(all_spl_junc['seqname'].values,[jncrow.chr])]
                spl_junc_df = spl_junc_df[np.in1d(spl_junc_df['strand'].values, ['-'])]
            five_dict, three_dict = extract_spljnc(jncrow, gtf_chr, '-', cons_exons, gtf_exons) # outputs dictionary of 5' and 3' info to add to final dataframe
            #final_df.at[jncrow.Index,'alternative_splicing'] = alt_vs_cons_splicing(jncrow, gtf_chr)
            ss_nearby = closest_splice_sites(jncrow, spl_junc_df)

        else: # Do not analyze strands that have a unidentified strand
            continue

        # If phyloPscore is requested, then using the phyloP_func to get the average score and the arrays for specific values
        if args.phyloPscores != None:
            fb_phyloPval, fb_extract_phyloP, lb_phyloPval, lb_extract_phyloP = phyloP_func(jncrow,args.phyloPscores[0], args.phyloPscores[1])
            if jncrow.strand == 1:
                final_df.at[jncrow.Index, "5phyloPscore"] = np.around(fb_phyloPval,3)
                final_df.at[jncrow.Index, "5phyloPlist"] = ", ".join(map(str, fb_extract_phyloP))
                final_df.at[jncrow.Index, "3phyloPscore"] = np.around(lb_phyloPval,3)
                final_df.at[jncrow.Index, "3phyloPlist"] = ", ".join(map(str,lb_extract_phyloP))
            elif jncrow.strand == 2:
                final_df.at[jncrow.Index, "3phyloPscore"] = np.around(fb_phyloPval,3)
                final_df.at[jncrow.Index, "3phyloPlist"] = ", ".join(map(str,fb_extract_phyloP))
                final_df.at[jncrow.Index, "5phyloPscore"] = np.around(lb_phyloPval,3)
                final_df.at[jncrow.Index, "5phyloPlist"] = ", ".join(map(str,lb_extract_phyloP))

        for val in five_prime_cols: # Add all 5' info into the appropriate columns
            if val.split('_')[-1] not in five_dict:
                final_df.at[jncrow.Index,val] = 0
            else:
                final_df.at[jncrow.Index,val] = five_dict[val.split('_')[-1]]
        for val in three_prime_cols: # Add all 3' info into the appropriate columns
            if val.split('_')[-1] not in three_dict:
                final_df.at[jncrow.Index,val] = 0
            else:
                final_df.at[jncrow.Index,val] = three_dict[val.split('_')[-1]]
        for val in splice_sites_nearby_cols:
            final_df.at[jncrow.Index, val] = ss_nearby[val]

        # Creating temp variables of extracted dataframes to save time on re-extracting the information
        prev_jncrow_chr = jncrow.chr
        prev_jncrow_strand = jncrow.strand
        prev_gtf_chr = gtf_chr
        prev_gtf_exons= gtf_exons
        prev_spl_junc_df = spl_junc_df
        if i % 10000 == 0:
            print(time.process_time() - start, '%i of %i' % (i,len(jnc_df)))

    if args.sequence_file != None:
        seqs_site3 = seqs[seqs['site'].isin(['3',3])].set_index('JNC_ID') # get sequences for 3' end
        seqs_site5 = seqs[seqs['site'].isin(['5',5])].set_index('JNC_ID') # get sequences for 5' end
        seqs_site3 =  seqs_site3.reindex(index=seqs_site3.index.to_series().str.slice(start=3).astype(float).sort_values().index) # order sequences based on JNC_ID index values
        seqs_site5 = seqs_site5.reindex(index=seqs_site5.index.to_series().str.slice(start=3).astype(float).sort_values().index)
        final_df = final_df.reindex(index=final_df.index.to_series().str.slice(start=3).astype(float).sort_values().index) # order final_df based on JNC_ID index values
        final_df.loc[final_df.index.isin(seqs_site3.index.tolist()),"3ss_sequence_51bp"] = seqs_site3['seq'].tolist() # Attach list of sequences to series
        final_df.loc[final_df.index.isin(seqs_site5.index.tolist()),"5ss_sequence_51bp"] = seqs_site5['seq'].tolist() # Attach list of sequences to series

        # Extract sequences needed for maxEnt and the 2bp at the 5' and 3' end

        final_df.loc[~final_df["5ss_sequence_51bp"].isin([np.nan,'nan','NA']), "5ss_sequence_2bp"] = final_df.loc[~final_df["5ss_sequence_51bp"].isin([np.nan,'nan','NA'])]["5ss_sequence_51bp"].str.slice(start = 25, stop = 27)
        final_df.loc[~final_df["5ss_sequence_51bp"].isin([np.nan,'NA','nan']), "5bases_maxEnt"] = final_df.loc[~final_df["5ss_sequence_51bp"].isin([np.nan,'NA','nan'])]["5ss_sequence_51bp"].str.slice(start = 22, stop =31)
        final_df.loc[~final_df["3ss_sequence_51bp"].isin([np.nan,'NA','nan']), "3ss_sequence_2bp"] = final_df.loc[~final_df["3ss_sequence_51bp"].isin([np.nan,'NA','nan'])]["3ss_sequence_51bp"].str.slice(start = 24, stop =  26)
        final_df.loc[~final_df["3ss_sequence_51bp"].isin([np.nan,'NA','nan']), "3bases_maxEnt"] = final_df.loc[~final_df["3ss_sequence_51bp"].isin([np.nan,'NA','nan'])]["3ss_sequence_51bp"].str.slice(start = 6, stop = 29)
        if args.maxEntscore:
            max_ent_seq_info = final_df.loc[~final_df["5bases_maxEnt"].isin([np.nan,'','nan','NA']) & ~final_df["3bases_maxEnt"].isin([np.nan,'','nan','NA'])]
            max_ent_seq_info.to_csv('data/max_ent_seq.csv', header = True, index = True)
            max_ent_series_5, max_ent_series_3 = calculate_maxEnt(max_ent_seq_info)
            final_df.loc[~final_df["5bases_maxEnt"].isin([np.nan,'','nan','NA']) & ~final_df["3bases_maxEnt"].isin([np.nan,'','nan','NA']), "5score_maxEnt"] = max_ent_series_5["maxEnt_5"].tolist()
            final_df.loc[~final_df["5bases_maxEnt"].isin([np.nan,'','nan','NA']) & ~final_df["3bases_maxEnt"].isin([np.nan,'','nan','NA']), "3score_maxEnt"] = max_ent_series_3["maxEnt_3"].tolist()
    final_df['strand_label'] = final_df['strand'].apply(lambda x: '+' if x ==1 else ('-' if x==2 else 'NA'))
    final_df['5_splice_site'] = final_df.apply(lambda x: int(x.first_base) if x.strand ==1 else (int(x.last_base) if x.strand==2 else 'NA'), axis = 1)
    final_df['3_splice_site'] = final_df.apply(lambda x: int(x.last_base) if x.strand ==1 else (int(x.first_base) if x.strand==2 else 'NA'), axis = 1)
    final_df = final_df.iloc[:,np.r_[0,len(final_df.columns)-2,len(final_df.columns)-1,len(final_df.columns)-3,4:len(final_df.columns)-3]]


# Create output csv file
    output_path = str(args.output_file).rsplit('/',1)
    if os.path.exists(output_path[0]):
        output = final_df.to_csv(args.output_file,header = True)
    else:
        os.makedirs(output_path[0])
        output = final_df.to_csv(args.output_file,header = True)
if __name__ == "__main__":
    main()
