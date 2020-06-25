#!/usr/bin/env python3
import pandas as pd
import numpy as np
import time
import subprocess
from collections import Counter
from sys import argv

'''
Inputs are a splice junction tuple, a gtf dataframe, +/- strand location of splice junction, and the exons nearby
Outputs a 5 prime dictinary and 3 prime dictionary that says if it is located in gene,transcript, exon, etc.
'''
def extract_spljnc(splice_jnc, gtf, strand, cons_exons, gtf_exons):
    #start = time.process_time()
    #Define strand and location of 5' and 3' ends
    if  strand == '+':
         five_ss = splice_jnc.first_base
         three_ss = splice_jnc.last_base
    elif strand == '-':
        five_ss = splice_jnc.last_base
        three_ss = splice_jnc.first_base
    # Extract the parts of GTF file that contain the 5' end
    extract_five_info = (gtf['start'] <= five_ss) & (gtf['end'] >= five_ss)
    five_info_df = gtf[extract_five_info]
    # What are the features of the strand that are found in this junction (gene,transcript, exon)?
    five_features = set(five_info_df['feature'].tolist())
    possible_elements = set(gtf['feature'].tolist())
    # Create a dictionary for the features of the 5' end and set it to 1 or 0
    dict_five_sam = {ft:1 for ft in possible_elements.intersection(five_features)}
    dict_five_dif = {ft:0 for ft in possible_elements.difference(five_features)}
    dict_five = {**dict_five_dif, **dict_five_sam}
    dict_five = {key.replace('_',''): val for key, val in dict_five.items()}
    #print(time.process_time()-start)
    #start = time.process_time()
    # Extract the parts of GTF file that contain the 3' end (look at 5' comments for role of each part of code)
    extract_three_info = (gtf['start'] <= three_ss) & (gtf['end'] >= three_ss)
    three_info_df = gtf[extract_three_info]
    three_features = set(three_info_df['feature'].tolist())
    dict_three_sam = {ft:1 for ft in possible_elements.intersection(three_features)}
    dict_three_dif = {ft:0 for ft in possible_elements.difference(three_features)}
    dict_three = {**dict_three_dif, **dict_three_sam}
    dict_three = {key.replace('_',''): val for key, val in dict_three.items()}
    #Seeing if it is in an intron by counting the number of transcripts that are in that region and comparing it to the number of exons
    if (five_info_df['feature'].tolist().count('transcript')!= 0):
        if (five_info_df['feature'].tolist().count('transcript')==five_info_df['feature'].tolist().count('exon')):
            five_intron= 0
        else:
            five_intron = 1
    else:
        five_intron = np.nan
    if (three_info_df['feature'].tolist().count('transcript')!= 0):
        if (three_info_df['feature'].tolist().count('transcript')==three_info_df['feature'].tolist().count('exon')):
            three_intron= 0
        else:
            three_intron = 1
    else:
        three_intron = np.nan # may need to change to np.nan


    # looking if it is in a constiutive or alternative exon/intron
    five_con_intron =[] # constitutive intron 5'
    five_con_exon = [] # constitutive exon 5'
    genes_three = three_info_df['gene_id'].unique().tolist() #genes on 3' end
    genes_five = five_info_df['gene_id'].unique().tolist() # genes on 5' end
    junctions_five = [] # name of region where 5' end is located when 5' end and 3' end share the same gene location
    #other_junctions_five = [] #name of region where 5' end is located when 5' end and 3' end DON'T share the same gene location
    #intersecting_genes = list(set(genes_five).intersection(genes_three)) # which genes are 5' end and 3' end found
    #start = time.process_time()
    for geneid in genes_five:
        five_info_df_gene = five_info_df[five_info_df['gene_id'].isin([geneid])]
        exonids_five = five_info_df_gene[five_info_df_gene['feature'].isin(['exon'])]['exon_id'].tolist()

        if five_info_df_gene[five_info_df_gene['feature'].isin(['transcript'])].empty: # if no transcripts then can't be constituve exon or intron
            five_con_intron.append(np.nan)
            five_con_exon.append(np.nan)
            continue

        elif (five_info_df_gene['feature'].tolist().count('transcript')==five_info_df_gene['feature'].tolist().count('exon')): # if number of exons found = number of transcripts found, we check the constitutive exon dataframe if that exon and corresponding geneid are present
            exon_type = cons_exons[cons_exons['exon_id'].isin(exonids_five) & cons_exons['gene_id'].isin([geneid])]
            if not exon_type.empty:
                five_con_exon.append(geneid + ':exon:' + str(exon_type.iloc[0]['start']) +'-'+ str(exon_type.iloc[0]['end']))
            else:
                five_con_exon.append(0)
            #print(time.process_time() - st,1)
            five_con_intron.append(np.nan)
            listofexons = five_info_df_gene[five_info_df_gene['feature'].isin(['exon'])]
            listofexons2 = listofexons.copy()
            listofexons2['string'] = geneid + ':chr' + listofexons['seqname'] +':exon:' + listofexons['start'].astype(str) + '-' + listofexons['end'].astype(str)
            junctions_five.extend(listofexons2['string'].tolist())
            '''
            if geneid in intersecting_genes:
                junctions_five.extend(listofexons2['string'].tolist())
            else:
                other_junctions_five.extend(listofexons2['string'].tolist())
            '''
        elif (five_info_df_gene['feature'].tolist().count('transcript')!=five_info_df_gene['feature'].tolist().count('exon')) and (five_info_df_gene['feature'].tolist().count('exon') > 0):
            # if number of trasncripts differs from number of exons then we need to look at each exon and intron
            five_con_exon.append(0)
            five_con_intron.append(0)
            listofexons = five_info_df_gene[five_info_df_gene['feature'].isin(['exon'])]
            listofexons2 = listofexons.copy()
            listofexons2['string'] = geneid + ':chr' + listofexons['seqname'] +':exon:' + listofexons['start'].astype(str) + '-' + listofexons['end'].astype(str)
            junctions_five.extend(listofexons2['string'].tolist())
            '''
            if geneid in intersecting_genes:
                junctions_five.extend(listofexons2['string'].tolist())
            else:
                other_junctions_five.extend(listofexons2['string'].tolist())
            '''
            cnt_transcripts = Counter(five_info_df_gene['transcript_id'].dropna().tolist())
            sing_trans =  [a for a, b in cnt_transcripts.items() if b == 1]
            #count number of transcripts that are only repeated once in five_info_df_gene then it is an intron
            for tran in sing_trans:
                nearbyexons = gtf_exons[gtf_exons['transcript_id'].isin([tran])]
                #print(time.process_time() - st,'c')
                five_near_end_exon = nearbyexons[nearbyexons['end'] < five_ss].end.max()
                five_near_start_exon = nearbyexons[nearbyexons['start'] > five_ss].start.min()
                junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon + 1) +'-' + str(five_near_start_exon-1)))
                '''
                if geneid in intersecting_genes:
                    junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon + 1) +'-' + str(five_near_start_exon-1)))
                else:
                    other_junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon + 1) +'-' + str(five_near_start_exon-1)))
                '''
        else: #Only transcripts and no exons
            # Look at closest exons left and right of the coordinate
            nearbyexons = gtf_exons[gtf_exons['gene_id'].isin([geneid])]
            five_near_end_exon = (nearbyexons['end']==(nearbyexons[nearbyexons['end'] < five_ss].end.max()))
            five_end = nearbyexons[five_near_end_exon]['exon_id'].tolist()
            five_near_start_exon = (nearbyexons['start'] == (nearbyexons[nearbyexons['start'] > five_ss].start.min()))
            five_start = nearbyexons[five_near_start_exon]['exon_id'].tolist()
            #five_start = nearbyexons[nearbyexons['start'] == (nearbyexons[nearbyexons['start'] > five_ss].start.min())]['exon_id'].unique.tolist()
            # if exons nearby are both constitutive exons then it must be in an constitutive intron
            five_start_df = cons_exons[cons_exons['exon_id'].isin(five_start) & cons_exons['gene_id'].isin([geneid])]
            five_end_df = cons_exons[cons_exons['exon_id'].isin(five_end) & cons_exons['gene_id'].isin([geneid])]
            if cons_exons[cons_exons['exon_id'].isin(five_start) & cons_exons['gene_id'].isin([geneid])].empty or cons_exons[cons_exons['exon_id'].isin(five_end) & cons_exons['gene_id'].isin([geneid])].empty:
                five_con_intron.append(0)
            else:
                five_con_intron.append(geneid + ':intron:' + str(five_end_df.iloc[0]['end'] +1) +'-'+  str(five_start_df.iloc[0]['start']-1))
            five_con_exon.append(np.nan)
            cnt_transcripts = Counter(five_info_df_gene['transcript_id'].dropna().tolist())
            sing_trans =  [a for a, b in cnt_transcripts.items() if b == 1]
            for tran in sing_trans:
                nearbyexons = gtf_exons[gtf_exons['transcript_id'].isin([tran])]
                five_near_end_exon = nearbyexons[nearbyexons['end'] < five_ss].end.max()
                five_near_start_exon = nearbyexons[nearbyexons['start'] > five_ss].start.min()
                junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon+1) +'-' + str(five_near_start_exon-1)))
                '''
                if geneid in intersecting_genes:
                    junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon+1) +'-' + str(five_near_start_exon-1)))
                else:
                    other_junctions_five.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(five_near_end_exon+1) +'-' + str(five_near_start_exon-1)))
                '''
    three_con_intron =[]
    three_con_exon = []
    junctions_three = []
    #other_junctions_three = []
    for geneid in genes_three:
        three_info_df_gene = three_info_df[three_info_df['gene_id'].isin([geneid])]
        exonids_three = three_info_df_gene[three_info_df_gene['feature'].isin(['exon'])]['exon_id'].tolist()
        if three_info_df_gene[three_info_df_gene['feature'].isin(['transcript'])].empty:
            three_con_intron.append(np.nan)
            three_con_exon.append(np.nan)
            continue
        elif (three_info_df_gene['feature'].tolist().count('transcript')==three_info_df_gene['feature'].tolist().count('exon')):
            #st = time.process_time()
            exon_type = cons_exons[cons_exons['exon_id'].isin(exonids_three) & cons_exons['gene_id'].isin([geneid])]
            if not exon_type.empty:
                three_con_exon.append(geneid + ':exon:' + str(exon_type.iloc[0]['start']) +'-'+ str(exon_type.iloc[0]['end']))
            else:
                three_con_exon.append(0)
            #print(time.process_time() - st,1)
            three_con_intron.append(np.nan)
            listofexons = three_info_df_gene[three_info_df_gene['feature'].isin(['exon'])]
            listofexons2 = listofexons.copy()
            listofexons2['string'] = geneid + ':chr' + listofexons['seqname'] +':exon:' + listofexons['start'].astype(str) + '-' + listofexons['end'].astype(str)
            junctions_three.extend(listofexons2['string'].tolist())
            '''
            if geneid in intersecting_genes:
                junctions_three.extend(listofexons2['string'].tolist())
            else:
                other_junctions_three.extend(listofexons2['string'].tolist())
            '''
        elif (three_info_df_gene['feature'].tolist().count('transcript')!=three_info_df_gene['feature'].tolist().count('exon')) and (three_info_df_gene['feature'].tolist().count('exon') > 0):
            three_con_exon.append(0)
            three_con_intron.append(0)
            listofexons = three_info_df_gene[three_info_df_gene['feature'].isin(['exon'])]
            listofexons2 = listofexons.copy()
            listofexons2['string'] = geneid + ':chr' + listofexons['seqname'] +':exon:' + listofexons['start'].astype(str) + '-' + listofexons['end'].astype(str)
            junctions_three.extend(listofexons2['string'].tolist())
            cnt_transcripts = Counter(three_info_df_gene['transcript_id'].dropna().tolist())
            sing_trans =  [a for a, b in cnt_transcripts.items() if b == 1]
            for tran in sing_trans:
                nearbyexons = gtf_exons[gtf_exons['transcript_id'].isin([tran])]
                three_near_end_exon = nearbyexons[nearbyexons['end'] < three_ss].end.max()
                three_near_start_exon = nearbyexons[nearbyexons['start'] > three_ss].start.min()
                junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon + 1) +'-' + str(three_near_start_exon-1)))
                '''
                if geneid in intersecting_genes:
                    junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon + 1) +'-' + str(three_near_start_exon-1)))
                else:
                    other_junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon + 1) +'-' + str(three_near_start_exon-1)))
                '''
        else:
            nearbyexons = gtf_exons[gtf_exons['gene_id'].isin([geneid])]
            three_near_end_exon = (nearbyexons['end']==(nearbyexons[nearbyexons['end'] < three_ss].end.max()))
            three_end = nearbyexons[three_near_end_exon]['exon_id'].tolist()
            three_near_start_exon = (nearbyexons['start'] == (nearbyexons[nearbyexons['start'] > three_ss].start.min()))
            three_start = nearbyexons[three_near_start_exon]['exon_id'].tolist()
            three_start_df = cons_exons[cons_exons['exon_id'].isin(three_start)& cons_exons['gene_id'].isin([geneid])]
            three_end_df = cons_exons[cons_exons['exon_id'].isin(three_end) & cons_exons['gene_id'].isin([geneid])]
            if cons_exons[cons_exons['exon_id'].isin(three_start)& cons_exons['gene_id'].isin([geneid])].empty or cons_exons[cons_exons['exon_id'].isin(three_end) & cons_exons['gene_id'].isin([geneid])].empty:
                three_con_intron.append(0)
            else:
                three_con_intron.append(geneid + ':intron:' + str(three_end_df.iloc[0]['end'] +1 ) +'-'+  str(three_start_df.iloc[0]['start']-1))
            three_con_exon.append(np.nan)
            #print(time.process_time() - st,3)
            cnt_transcripts = Counter(three_info_df_gene['transcript_id'].dropna().tolist())
            sing_trans =  [a for a, b in cnt_transcripts.items() if b == 1]
            for tran in sing_trans:
                nearbyexons = gtf_exons[gtf_exons['transcript_id'].isin([tran])]
                three_near_end_exon = nearbyexons[nearbyexons['end'] < three_ss].end.max()
                three_near_start_exon = nearbyexons[nearbyexons['start'] > three_ss].start.min()
                junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon+1) +'-' + str(three_near_start_exon-1)))
                '''
                if geneid in intersecting_genes:
                    junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon+1) +'-' + str(three_near_start_exon-1)))
                else:
                    other_junctions_three.append(str(geneid + ':chr'+ splice_jnc.chr + ':intron:'+ str(three_near_end_exon+1) +'-' + str(three_near_start_exon-1)))
                '''
    five_con_exon_val = [x for x in five_con_exon if x not in [0,np.nan]]
    five_con_intron_val = [x for x in five_con_intron if x not in [0,np.nan]]
    if five_con_exon_val:
        dict_five['constitutiveexon'] = ';'.join(five_con_exon_val)
    elif 0 in five_con_exon:
        dict_five['constitutiveexon'] = 0
    else:
        dict_five['constitutiveexon'] = 'NA'
    if five_con_intron_val:
        dict_five['constitutiveintron'] = ';'.join(five_con_intron_val)
    elif 0 in five_con_intron:
        dict_five['constitutiveintron'] = 0
    else:
        dict_five['constitutiveintron'] = 'NA'

    three_con_exon_val = [x for x in three_con_exon if x not in [0,np.nan]]
    three_con_intron_val = [x for x in three_con_intron if x not in [0,np.nan]]

    if three_con_exon_val:
        dict_three['constitutiveexon'] = ';'.join(three_con_exon_val)
    elif 0 in three_con_exon:
        dict_three['constitutiveexon'] = 0
    else:
        dict_three['constitutiveexon'] = 'NA'
    if three_con_intron_val:
        dict_three['constitutiveintron'] = ';'.join(three_con_intron_val)
    elif 0 in three_con_intron:
        dict_three['constitutiveintron'] = 0
    else:
        dict_three['constitutiveintron'] = 'NA'

    junctions_five = list(set(junctions_five))
    junctions_three = list(set(junctions_three))
    dict_five['intron'] = five_intron
    dict_three['intron'] = three_intron
    if  dict_five['gene'] == 1:
        dict_five['gene'] = ';'.join(list(set([itm.split(':',1)[0] for itm in junctions_five])))
    if dict_three['gene'] == 1:
        dict_three['gene'] = ';'.join(list(set([itm.split(':',1)[0] for itm in junctions_three])))
    if dict_five['exon'] == 1:
        dict_five['exon'] = ';'.join([(s.split(':')[0] +':'+ s.split(':')[-1]) for s in junctions_five if ':exon:' in s])
    if dict_three['exon'] == 1:
        dict_three['exon'] =';'.join([(s.split(':')[0] +':'+ s.split(':')[-1]) for s in junctions_three if ':exon:' in s])
    if dict_five['intron'] == 1:
        dict_five['intron'] = ';'.join([(s.split(':')[0] +':'+ s.split(':')[-1]) for s in junctions_five if ':intron:' in s])
    if dict_three['intron'] == 1:
        dict_three['intron'] = ';'.join([(s.split(':')[0] +':'+ s.split(':')[-1]) for s in junctions_three if ':intron:' in s])
    #dict_five['intron'] = five_intron
    #dict_three['intron'] = three_intron
    dict_five['strandofgene'] = strand
    dict_three['strandofgene'] = strand
    #dict_five['otherregions'] = set(other_junctions_five)
    #dict_three['otherregions'] = set(other_junctions_three)
    return (dict_five, dict_three)

def alt_vs_cons_splicing(splice_jnc, gtf):
    #start = time.process_time()
    # Define strand and location of 5' and 3' ends
    fb = splice_jnc.first_base
    lb = splice_jnc.last_base
    # Extract the parts of GTF file with the start or end site inside the splice junction
    extract_feat_in_spljnc = (((fb <= gtf['start']) & (lb >= gtf['start'])) |
                              ((fb <= gtf['end']) & (lb >= gtf['end'])))
    feat_in_spljnc = gtf[extract_feat_in_spljnc]
    # Is there an exon in this region?
    if 'exon' in feat_in_spljnc['feature'].tolist():
        feat_jnc_exon = 1
    else:
        feat_jnc_exon = 0
    #print(time.process_time()-start, 'alt/cons')
    return feat_jnc_exon

def closest_splice_sites(jnc, splice_list):
    gtf = splice_list
    fb = jnc.first_base
    lb = jnc.last_base
    gtf['dist_start_fb'] = gtf['start'] - fb
    gtf['dist_end_fb'] = gtf['end'] - fb
    gtf['dist_start_lb'] = gtf['start'] - lb
    gtf['dist_end_lb'] = gtf['end'] - lb
    ss_fb = (gtf["dist_start_fb"]== 0)
    ss_lb = (gtf["dist_end_lb"]== 0)
    if len(gtf[ss_fb].index) == 0:
        fb_annotation = 0
    else:
        fb_annotation = 1
    fb_left_start = gtf[gtf['dist_start_fb'] <= 0].dist_start_fb.max()
    fb_left_end = gtf[gtf['dist_end_fb'] <= 0].dist_end_fb.max()
    fb_right_start = gtf[gtf['dist_start_fb'] >= 0].dist_start_fb.min()
    fb_right_end = gtf[gtf['dist_end_fb'] >= 0].dist_end_fb.min()

    if len(gtf[ss_lb].index) == 0:
        lb_annotation = 0
    else:
        lb_annotation =1
    lb_left_start = gtf[gtf['dist_start_lb'] <= 0].dist_start_lb.max()
    lb_left_end = gtf[gtf['dist_end_lb'] <= 0].dist_end_lb.max()
    lb_right_start = gtf[gtf['dist_start_lb'] >= 0].dist_start_lb.min()
    lb_right_end = gtf[gtf['dist_end_lb'] >= 0].dist_end_lb.min()
    if jnc.strand == 1:
        splicesite_dict = {"5ss_to_upstream5ss": fb_left_start, "5ss_to_upstream3ss": fb_left_end,
                           "5ss_to_downstream5ss": fb_right_start,"5ss_to_downstream3ss": fb_right_end,
                           "3ss_to_upstream5ss": lb_left_start, "3ss_to_upstream3ss": lb_left_end,
                           "3ss_to_downstream5ss": lb_right_start,"3ss_to_downstream3ss": lb_right_end,
                           "5annotated": fb_annotation, "3annotated":lb_annotation}
    else:
        splicesite_dict = {"3ss_to_upstream5ss": fb_right_end, "3ss_to_upstream3ss": fb_right_start,
                            "3ss_to_downstream5ss": fb_left_end,"3ss_to_downstream3ss": fb_left_start,
                            "5ss_to_upstream5ss": lb_right_end, "5ss_to_upstream3ss": lb_right_start,
                            "5ss_to_downstream5ss": lb_left_end,"5ss_to_downstream3ss": lb_left_start,
                           "5annotated": lb_annotation, "3annotated":fb_annotation}
    return splicesite_dict

def phyloP_func(jnc, bigwig, rangeval):
    st = time.process_time()
    bash_cmd = "bigWigtoBedGraph -chrom=chr%s -start=%i -end=%i %s data/phyloPscores.bedGraph" % (jnc.chr, int(jnc.first_base - 100), int(jnc.last_base + 100), bigwig)
    process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    phyloPinfo = pd.read_csv('data/phyloPscores.bedGraph', sep = '\t', names = ['chr', 'start', 'end', 'score'])
    #print(time.process_time() -st,'1a')
    #phyloPinfo = phyloPinfo2[['chr', 'end', 'score']].copy()
    phyloPinfo['start'] = phyloPinfo['start'] + 1
    '''
    extract = (jnc.first_base <= phyloPinfo['end']) & (jnc.last_base >= phyloPinfo['start'])
    extract_phyloP = phyloPinfo[extract]
    extract_phyloP = extract_phyloP.sort_values(by = ['start'])
    extract_phyloP['length'] = extract_phyloP['end'] - extract_phyloP['start'] +1
    '''
    fb_extract = ((jnc.first_base + int(float(rangeval)/2)) >= phyloPinfo['start']) & ((jnc.first_base - int(float(rangeval)/2)) <= phyloPinfo['end'])
    fb_phyloP = phyloPinfo[fb_extract]
    fb_phyloP = fb_phyloP.sort_values(by = ['start'])
    fb_phyloP["pos"] = fb_phyloP["start"] - jnc.first_base
    fb_phyloP['length'] = fb_phyloP['end'] - fb_phyloP['start'] +1

    lb_extract = ((jnc.last_base + int(float(rangeval)/2)) >= phyloPinfo['start']) & ((jnc.last_base - int(float(rangeval)/2)) <= phyloPinfo['end'])
    lb_phyloP = phyloPinfo[lb_extract]
    lb_phyloP = lb_phyloP.sort_values(by = ['start'])
    lb_phyloP["pos"] = lb_phyloP["start"] - jnc.last_base
    lb_phyloP['length'] = lb_phyloP['end'] - lb_phyloP['start'] +1


    #print(time.process_time() -st, '2a')
    if fb_phyloP.empty:
        fb_score = 'NA'
        fb_list_fin = ['NA']
    else:
        if ((jnc.first_base - int(float(rangeval)/2)) > fb_phyloP['start'].iloc[0]):
            fb_phyloP['length'].iloc[0] = fb_phyloP['end'].iloc[0] - (jnc.first_base - int(float(rangeval)/2)) +1
            fb_phyloP["pos"].iloc[0] = int(float(rangeval)/2) *-1
        elif ((jnc.first_base - int(float(rangeval)/2)) < fb_phyloP['start'].iloc[0]):
            init_row = {'chr':fb_phyloP['chr'].iloc[0],'start':(jnc.first_base - int(float(rangeval)/2)), 'end':(fb_phyloP['start'].iloc[0]-1), 'pos':-1*int(float(rangeval)/2), 'length': fb_phyloP['start'].iloc[0]- (jnc.first_base - int(float(rangeval)/2))}
            fb_phyloP = fb_phyloP.append(init_row, ignore_index = True)
            fb_phyloP = fb_phyloP.sort_values(by = ['start'])
        if ((jnc.first_base + int(float(rangeval)/2)) < fb_phyloP['end'].iloc[-1]):
            fb_phyloP['length'].iloc[-1] = (jnc.first_base + int(float(rangeval)/2)) - fb_phyloP['start'].iloc[-1] +1
            fb_phyloP["pos"].iloc[-1] = int(float(rangeval)/2)
        elif ((jnc.first_base + int(float(rangeval)/2)) > fb_phyloP['end'].iloc[-1]):
            fin_row = {'chr':fb_phyloP['chr'].iloc[-1],'end':(jnc.first_base + int(float(rangeval)/2)), 'start':(fb_phyloP['end'].iloc[-1]+1), 'pos':int(float(rangeval)/2), 'length':(jnc.first_base + int(float(rangeval)/2) - (fb_phyloP['end'].iloc[-1]+1) + 1)}
            fb_phyloP = fb_phyloP.append(fin_row, ignore_index = True)
            fb_phyloP = fb_phyloP.sort_values(by = ['start'])
        #fb_score = np.average(fb_phyloP.score, weights = fb_phyloP.length)
        fb_list_fin = [np.around(fb_phyloP['score'].iloc[0],3)] * fb_phyloP['length'].iloc[0]
        #fb_phyloP_fin = fb_phyloP[[ 'start','pos','score']]
        for i in range(1, len(fb_phyloP)):
            if fb_phyloP['start'].iloc[i] - fb_phyloP['end'].iloc[i-1] == 1:
                fb_list_fin.extend([np.around(fb_phyloP['score'].iloc[i],3)]*fb_phyloP['length'].iloc[i])
            else:
                fb_list_fin.extend(['NA']*(fb_phyloP['start'].iloc[i] - fb_phyloP['end'].iloc[i-1] - 1))
                fb_list_fin.extend([np.around(fb_phyloP['score'].iloc[i],3)]*fb_phyloP['length'].iloc[i])

        fb_score = np.average([val for val in fb_list_fin if (val not in [np.nan, 'NA']) and (not np.isnan(val))])
        fb_score = np.around(fb_score,3)
        #fb_phyloP_fin = fb_phyloP_fin.set_index('start')
        #fb_list = fb_phyloP_fin.values.tolist()

    if lb_phyloP.empty:
        lb_score = 'NA'
        lb_list_fin = ['NA']
    else:
        if ((jnc.last_base - int(float(rangeval)/2)) > lb_phyloP['start'].iloc[0]):
            lb_phyloP['length'].iloc[0] = lb_phyloP['end'].iloc[0] - (jnc.last_base - int(float(rangeval)/2)) +1
            lb_phyloP["pos"].iloc[0] = int(float(rangeval)/2) *-1
        elif ((jnc.last_base - int(float(rangeval)/2)) < lb_phyloP['start'].iloc[0]):
            init_row = {'chr':lb_phyloP['chr'].iloc[0],'start':(jnc.last_base - int(float(rangeval)/2)), 'end':(lb_phyloP['start'].iloc[0]-1), 'pos':-1*int(float(rangeval)/2),'length':lb_phyloP['start'].iloc[0]- (jnc.last_base - int(float(rangeval)/2))}
            lb_phyloP = lb_phyloP.append(init_row, ignore_index = True)
            lb_phyloP = lb_phyloP.sort_values(by = ['start'])
        if ((jnc.last_base + int(float(rangeval)/2)) < lb_phyloP['end'].iloc[-1]):
            lb_phyloP['length'].iloc[-1] = (jnc.last_base + int(float(rangeval)/2)) - lb_phyloP['start'].iloc[-1] +1
            lb_phyloP["pos"].iloc[-1] = int(float(rangeval)/2)

        elif ((jnc.last_base + int(float(rangeval)/2)) > lb_phyloP['end'].iloc[-1]):
            fin_row = {'chr':lb_phyloP['chr'].iloc[-1],'end':(jnc.last_base + int(float(rangeval)/2)), 'start':(lb_phyloP['end'].iloc[-1]+1), 'pos':int(float(rangeval)/2), 'length':(jnc.last_base + int(float(rangeval)/2) - (lb_phyloP['end'].iloc[-1]+1) + 1)}
            lb_phyloP = lb_phyloP.append(fin_row, ignore_index = True)
            lb_phyloP = lb_phyloP.sort_values(by = ['start'])
        #lb_score = np.average(lb_phyloP.score, weights = lb_phyloP.length)
        lb_list_fin = [np.around(lb_phyloP['score'].iloc[0],3)] * lb_phyloP['length'].iloc[0]
        #lb_phyloP_fin = lb_phyloP[[ 'start','pos','score']]
        #lb_phyloP_fin =  lb_phyloP_fin.set_index('start')
        #lb_list = lb_phyloP_fin.values.tolist()
        for i in range(1, len(lb_phyloP)):
            if lb_phyloP['start'].iloc[i] - lb_phyloP['end'].iloc[i-1] == 1:
                lb_list_fin.extend([np.around(lb_phyloP['score'].iloc[i],3)]*lb_phyloP['length'].iloc[i])
            else:
                lb_list_fin.extend(['NA']*(lb_phyloP['start'].iloc[i] - lb_phyloP['end'].iloc[i-1] - 1))
                lb_list_fin.extend([np.around(lb_phyloP['score'].iloc[i],3)]*lb_phyloP['length'].iloc[i])
        lb_score = np.average([val for val in lb_list_fin if (val not in [np.nan, 'NA']) and (not np.isnan(val))])
        lb_score = np.around(lb_score,3)
    #print(time.process_time() -st, '3a')
    return fb_score, fb_list_fin, lb_score, lb_list_fin


