#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Author: Li Fajin
@Date: 2019-08-19 14:15:05
@LastEditors: Li Fajin
@LastEditTime: 2020-06-09 10:20:52
@Description: This script is used for statistic ribosome density around a specific di-AA or tri-AA motifs.
input:
the input are just the same as MetageneAnalysis.py but with longest.transcripts.cds.sequence.fa file input also which could be generated by GetProteinCodingSequence.py
--type1 is a di-AA motif such as PP,KK,DD, et al.
--type2 is a tri-AA motif such as PPP, KKK,DDD, et al.
--motifList1 and --motifList2 is list with more than one AAA motifs,such as :
motifs
KKK
PPP
LLL
HHH
output:
a data frame with density around AA motifs and with a stretch equals to 50 nt. Namely the length of each density vector equals to 101 nt(-50 nt + 0 + 50 nt.)
'''



from .FunctionDefinition import *
from collections import defaultdict
import re
from itertools import groupby,chain

def find_motif(in_bamFile,in_selectTrans,in_transLengthDict,in_startCodonCoorDict,in_stopCodonCoorDict,in_readLengths,in_readOffset,inCDS_countsFilterParma,inCDS_lengthFilterParma,transcriptFasta,type1=None,type2=None,motifList1=None,motifList2=None,mode='counts',table=1):
	'''
	find a specific triplete AA motif (PPP) and its ribosome density or find a set of motifs provided by the motifList and get their ribosome densities.
	'''
	transcript_sequence=fastaIter(transcriptFasta)
	filter_1=0
	filter_2=0
	filter_3=0
	filter_4=0
	all_counts=0
	passTransSet=set()
	motifDensity_1=defaultdict(list)
	tmpMotifDensity_1=defaultdict(list)
	motifDensity_2=defaultdict(list)
	tmpMotifDensity_2=defaultdict(list)
	RecordList1=[]
	RecordList2=[]

	if type1:
		type1_AA=list(type1)
		if len(type1_AA) != 2:
			raise IOError("The type1 must be a string with lenght equaling to 2. e,g. 'PP' or 'KK' motifs")
		else:
			pass
	if type2:
		type2_AA=list(type2)
		if len(type2_AA) != 3:
			raise IOError("The type2 must be a string with lenght equaling to 3. e,g. 'PPP' or 'KKK' or 'PKK' motifs")
		else:
			pass
	if motifList1:
		motifList1_motif=pd.read_csv(motifList1,sep="\t")
		motifList1_motif=motifList1_motif.iloc[:,0].values
	if motifList2:
		motifList2_motif=pd.read_csv(motifList2,sep="\t")
		motifList2_motif=motifList2_motif.iloc[:,0].values

	if (type1 or type2) and (motifList1 or motifList2):
		raise IOError("The 'type' parameters and 'motifList' parameters are mutually exclusive. Please input one of them.")

	if (not type1 and not type2) and  (not motifList1 and not motifList2):
		raise IOError("There is at least one parameters among the 'typ1' 'type2' 'motifList1' and 'motifList2'.")

	## read sam files
	pysamFile=pysam.AlignmentFile(in_bamFile,"rb")
	pysamFile_trans=pysamFile.references
	in_selectTrans=set(pysamFile_trans).intersection(in_selectTrans)
	in_selectTrans=in_selectTrans.intersection(transcript_sequence.keys()).intersection(in_startCodonCoorDict.keys())
	for trans in in_startCodonCoorDict.keys():
		leftCoor =int(in_startCodonCoorDict[trans])-1
		rightCoor=int(in_stopCodonCoorDict[trans])-3
		(trans_counts,read_counts_frameSum,total_reads,cds_reads)=get_trans_frame_counts(pysamFile, trans, in_readLengths, in_readOffset, in_transLengthDict[trans], leftCoor, rightCoor)
		all_counts+=total_reads
	for trans in in_selectTrans:
		leftCoor =int(in_startCodonCoorDict[trans])-1 #the first base of start codon 0-base
		rightCoor=int(in_stopCodonCoorDict[trans])-3 #the first base of stop codon 0-base
		CDS_seq=transcript_sequence[trans]
		if len(CDS_seq) % 3 !=0:
			filter_1+=1
			continue
		if len(CDS_seq) < inCDS_lengthFilterParma:
			filter_2+=1
		AA_seq=translation(CDS_seq,table=table,cds=False)

		## read counts
		(read_counts,read_counts_frameSum,trans_reads,cds_reads)=get_trans_frame_counts(pysamFile, trans, in_readLengths, in_readOffset, in_transLengthDict[trans], leftCoor, rightCoor)
		cds_reads_normed = 10**9*(cds_reads/(all_counts*len(read_counts_frameSum)*3))
		if mode == "RPKM":
			if cds_reads_normed < inCDS_countsFilterParma:
				filter_3+=1
				continue
		if mode == 'counts':
			if cds_reads < inCDS_countsFilterParma:
				filter_3+=1
				continue
		## get read density in nt unit
		read_counts_frame=np.array(read_counts[leftCoor:rightCoor+3])
		sumValue=sum(read_counts_frame[20:(len(AA_seq)-20)]) ## count from the 20th, and stop at len(AA_seq)-20
		if sumValue==0:
			filter_4+=1
			continue
		## normalize the read_counts_frame by total density along the whole AA sequence
		densityPerTrans=read_counts_frame/sumValue
		tmpMotif2=np.zeros(101,dtype="float64")
		tmpMotif1=np.zeros(101,dtype="float64")
		passTransSet.add(trans)
		if (type1 and (not type2) and (not motifList1) and (not motifList2)):
			motif=type1_AA[0]+type1_AA[1]
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				if AA_seq[i]== type1_AA[0] and AA_seq[i+1]== type1_AA[1]:
					tmpMotif1+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_1[motif].append(tmpMotif1)
					record=trans+"\t"+motif+AA_seq[i+2]+"\t"+str(i)+"\t"+str(sum(densityPerTrans[i*3:(i*3+3)])) ## E-site
					#print(record,file=sys.stderr)
					RecordList1.append(record)
		elif (type2 and (not type1) and (not motifList1) and (not motifList2)):
			motif=type2_AA[0]+type2_AA[1]+type2_AA[2]
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				if AA_seq[i]== type2_AA[0] and AA_seq[i+1]== type2_AA[1] and AA_seq[i+2]==type2_AA[2]:
					tmpMotif2+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_2[motif].append(tmpMotif2)
					record=trans+"\t"+motif+"\t"+str(i)+"\t"+str(sum(densityPerTrans[(i*3+3):(i*3+6)])) ## P-site
					#print(record,file=sys.stderr)
					#print(trans,motif,i,file=sys.stderr)
					RecordList2.append(record)
		elif (type1 and type2 and (not motifList1) and (not motifList2)):
			motif1=type1_AA[0]+type1_AA[1]
			motif2=type2_AA[0]+type2_AA[1]+type2_AA[2]
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				if AA_seq[i]== type1_AA[0] and AA_seq[i+1]== type1_AA[1]:
					tmpMotif1+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_1[motif1].append(tmpMotif1)
					record=trans+"\t"+motif1+AA_seq[i+2]+"\t"+str(i)+"\t"+str(sum(densityPerTrans[i*3:(i*3+3)]))
					#print(record,file=sys.stderr)
					RecordList1.append(record)
				if AA_seq[i]== type2_AA[0] and AA_seq[i+1]== type2_AA[1] and AA_seq[i+2]==type2_AA[2]:
					tmpMotif2+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_2[motif2].append(tmpMotif2)
					record=trans+"\t"+motif2+"\t"+str(i)+"\t"+str(sum(densityPerTrans[(i*3+3):(i*3+6)]))
					#print(record,file=sys.stderr)
					RecordList2.append(record)
		elif ((not type1) and (not type2) and motifList1 and (not motifList2)):
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				motif=AA_seq[i]+AA_seq[i+1]+AA_seq[i+2]
				if motif in motifList1_motif:
					tmpMotif1+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_1[motif].append(tmpMotif1)
					record=trans+"\t"+motif+"\t"+str(i)+"\t"+str(sum(densityPerTrans[i*3:(i*3+3)]))
					#print(record,file=sys.stderr)
					RecordList1.append(record)
		elif ((not type1) and (not type2) and (not motifList1) and motifList2):
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				motif=AA_seq[i]+AA_seq[i+1]+AA_seq[i+2]
				if motif in motifList2_motif:
					tmpMotif2+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_2[motif].append(tmpMotif2)
					record=trans+"\t"+motif+"\t"+str(i)+"\t"+str(sum(densityPerTrans[(i*3+3):(i*3+6)]))
					#print(record,file=sys.stderr)
					RecordList2.append(record)
		elif ((not type1) and (not type2) and motifList1 and motifList2):
			for  i in np.arange(20,(len(AA_seq)-20)): # there is no AA on position len(AA_seq)+1,scan from the 21 codon and stop at 21 codon away from stop codon
				motif=AA_seq[i]+AA_seq[i+1]+AA_seq[i+2]
				if motif in motifList1_motif:
					tmpMotif1+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_1[motif].append(tmpMotif1)
					record=trans+"\t"+motif+"\t"+str(i)+"\t"+str(sum(densityPerTrans[i*3:(i*3+3)]))
					#print(record,file=sys.stderr)
					RecordList1.append(record)
				if motif in motifList2_motif:
					tmpMotif2+=densityPerTrans[(i*3-50):(i*3+50+1)]
					tmpMotifDensity_2[motif].append(tmpMotif2)
					record=trans+"\t"+motif+"\t"+str(i)+"\t"+str(sum(densityPerTrans[(i*3+3):(i*3+6)]))
					#print(record,file=sys.stderr)
					RecordList2.append(record)
		else:
			raise IOError("Please check your input!")

	pysamFile.close()
	print("The number of genes whose length of CDS could not divided by three: " + str(filter_1),file=sys.stderr)
	print("The number of genes whose length of CDS is less than the criteria: " + str(filter_2),file=sys.stderr)
	print("The number of genes whose read counts on CDS are less than the criteria: " + str(filter_3),file=sys.stderr)
	print("The number of genes whose total read counts after normalization are equal to zero: "+str(filter_4),file=sys.stderr)
	print("The final number of genes used for following analysis is: " + str(len(passTransSet)),file=sys.stderr)

	if tmpMotifDensity_1 and (not tmpMotifDensity_2):
		for k,v in tmpMotifDensity_1.items():
			tmpMotif1=k
			tmpDensity1=np.array(v)
			print("There are "+str(tmpDensity1.shape[0])+" positions used for plot",file=sys.stderr)
			for i in np.arange(101):
				motifDensity_1[tmpMotif1].append(np.mean(tmpDensity1[:,i]))
		print("This will return motifDensity_1",file=sys.stderr)
		#print(len(RecordList1),file=sys.stderr)
		return motifDensity_1,RecordList1
	if (not tmpMotifDensity_1) and tmpMotifDensity_2:
		for k,v in tmpMotifDensity_2.items():
			tmpMotif2=k
			tmpDensity2=np.array(v)
			print("There are "+ str(tmpDensity2.shape[0])+" positions used for plot",file=sys.stderr)
			for i in np.arange(101):
				motifDensity_2[tmpMotif2].append(np.mean(tmpDensity2[:,i]))
		print(len(RecordList2),file=sys.stderr)
		#print("This will return motifDensity_2",file=sys.stderr)
		return motifDensity_2,RecordList2
	if tmpMotifDensity_1 and tmpMotifDensity_2:
		for k,v in tmpMotifDensity_1.items():
			tmpMotif1=k
			tmpDensity1=np.array(v)
			print("There are "+str(tmpDensity1.shape[0])+" positions used for plot "+ str(tmpMotif1) ,file=sys.stderr)
			for i in np.arange(101):
				motifDensity_1[tmpMotif1].append(np.mean(tmpDensity1[:,i]))
		for k,v in tmpMotifDensity_2.items():
			tmpMotif2=k
			tmpDensity2=np.array(v)
			print("There are "+ str(tmpDensity2.shape[0])+" positions used for plot " + str(tmpMotif2),file=sys.stderr)
			for i in np.arange(101):
				motifDensity_2[tmpMotif2].append(np.mean(tmpDensity2[:,i]))
		if len(tmpMotifDensity_1.keys())>1 or len(tmpMotifDensity_2.keys())>1:
			motifDensity_1['sum_list1']=np.array(list(map(sum,zip(*motifDensity_1.values()))))
			motifDensity_2['sum_list2']=np.array(list(map(sum,zip(*motifDensity_2.values()))))
		print("This will return motifDensity_1 and motifDensity_2",file=sys.stderr)
		#print(len(RecordList1),len(RecordList2),file=sys.stderr)
		return motifDensity_1,motifDensity_2,RecordList1,RecordList2


def write_mofitDensity_dataframe_two_types(inBamAttr,outFile):
		data=[]
		data_columns=[]
		for bms in inBamAttr:
			tmpmotif1=list(chain(*[[i]*len(bms.motifDensity_1[i]) for i in bms.motifDensity_1.keys()]))
			tmpmotif2=list(chain(*[[i]*len(bms.motifDensity_2[i]) for i in bms.motifDensity_2.keys()]))
			tmpdensity1=list(chain(*[bms.motifDensity_1[i] for i in bms.motifDensity_1.keys()]))
			tmpdensity2=list(chain(*[bms.motifDensity_2[i] for i in bms.motifDensity_2.keys()]))
			density1=pd.DataFrame(tmpdensity1)
			density2=pd.DataFrame(tmpdensity2)
			sample=bms.bamLegend
			motif=pd.DataFrame(tmpmotif1+tmpmotif2)
			density=pd.concat((density1,density2),axis=0)
			data_columns.append(sample)
			data.append(density)
		temp=data[0]
		if len(data) < 1:
			raise EOFError("Empty file, there is nothing in the file.")
		if len(data) == 1:
			data_columns=["motif"]+data_columns
			temp=pd.DataFrame(pd.merge(motif,temp,how='left',left_index=True,right_index=True))
			temp.columns=data_columns
			temp.to_csv(outFile,sep="\t",index=0)
		if len(data) > 1:
			for i in np.arange(1,len(data)):
				temp=np.hstack((temp,data[i]))
			data_columns=["motif"]+data_columns
			temp=pd.DataFrame(temp)
			temp=pd.DataFrame(pd.merge(motif,temp,how='left',left_index=True,right_index=True))
			temp.columns=data_columns
			temp.to_csv(outFile,sep="\t",index=0)
def write_mofitDensity_dataframe_one_type(inBamAttr,outFile):
		data=[]
		data_columns=[]
		for bms in inBamAttr:
			tmpmotif=list(chain(*[[i]*len(bms.motifDensity[i]) for i in bms.motifDensity.keys()]))
			tmpdensity=list(chain(*[bms.motifDensity[i] for i in bms.motifDensity.keys()]))
			density=pd.DataFrame(tmpdensity)
			sample=bms.bamLegend
			motif=pd.DataFrame(tmpmotif)
			data_columns.append(sample)
			data.append(density)
		temp=data[0]
		if len(data) < 1:
			raise EOFError("Empty file, there is nothing in the file.")
		if len(data) == 1:
			data_columns=["motif"]+data_columns
			temp=pd.DataFrame(pd.merge(motif,temp,how='left',left_index=True,right_index=True))
			temp.columns=data_columns
			temp.to_csv(outFile,sep="\t",index=0)
		if len(data) > 1:
			for i in np.arange(1,len(data)):
				temp=np.hstack((temp,data[i]))
			data_columns=["motif"]+data_columns
			temp=pd.DataFrame(temp)
			temp=pd.DataFrame(pd.merge(motif,temp,how='left',left_index=True,right_index=True))
			temp.columns=data_columns
			temp.to_csv(outFile,sep="\t",index=0)

def write_motif_list(inBamAttr,outputprefix,Type):
	for bms in inBamAttr:
		if Type == 'di-AA':
			densityLabel="Density at E-site of the motif"
			with open(outputprefix+"_"+bms.bamLegend+"_type1"+".motifs",'w') as f:
				f.write("%s\t%s\t%s\t%s\n" %("transcript","motif","position",densityLabel))
				for record in bms.RecordList1:
					f.write("%s\n" %(record))
		if Type  == 'tri-AA':
			densityLabel="Density at P-site of the motif"
			with open(outputprefix+"_"+bms.bamLegend+"_type2"+".motifs",'w') as f:
				f.write("%s\t%s\t%s\t%s\n" %("transcript","motif","position",densityLabel))
				for record in bms.RecordList2:
					f.write("%s\n" %(record))
		if Type == 'both':
			label1='Density at E-site of the motif'
			label2='Density at P-site of the motif'
			with open(outputprefix+"_"+bms.bamLegend+"_type1"+".motifs",'w') as f:
				f.write("%s\t%s\t%s\t%s\n" %("transcript","motif","position",label1))
				for record in bms.RecordList1:
					f.write("%s\n" %(record))
			with open(outputprefix+"_"+bms.bamLegend+"_type2"+".motifs",'w') as f:
				f.write("%s\t%s\t%s\t%s\n" %("transcript","motif","position",label2))
				for record in bms.RecordList2:
					f.write("%s\n" %(record))


def parse_args_for_triplete_AA_motif():
	parsed=create_parser_for_triplete_AA_motif()
	(options,args)=parsed.parse_args()
	(type1,type2,motifList1,motifList2,min_cds_counts,min_cds_codon,transcript_fasta,mode,output_prefix,table)=(options.type1,options.type2,options.motifList1,options.motifList2,
	options.min_cds_counts,options.min_cds_codon,options.transcript_fasta,options.mode,options.output_prefix,options.geneticCode)
	if options.bamListFile and (options.bam_files or options.read_length or options.read_offset or options.bam_file_legend):
		raise IOError("'-f' parameter and '-i -r -s -t' are mutually exclusive.")
	if options.bamListFile:
		bamFiles,readLengths,Offsets,bamLegends=parse_bamListFile(options.bamListFile)
	elif options.bam_files:
		bamFiles,readLengths,Offsets,bamLegends=options.bam_files.split(","),options.read_length.split("_"),options.read_offset.split("_"),options.bam_file_legend.split(",")
	else:
		raise IOError("Please check you input files!")
	print("your input : "+ str(len(bamFiles))+" bam files",file=sys.stderr)
	bam_attr=[]
	for ii,jj,mm,nn in zip(bamFiles,readLengths,Offsets,bamLegends):
		bam=bam_file_attr(ii,jj,mm,nn)
		bam_attr.append(bam)
	selectTrans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,transID2geneID,transID2geneName,cdsLengthDict=reload_transcripts_information(options.coorFile)
	geneID2transID={v:k for k,v in transID2geneID.items()}
	geneName2transID={v:k for k,v in transID2geneName.items()}
	if options.in_selectTrans:
		select_trans=pd.read_csv(options.in_selectTrans,sep="\t")
		select_trans=set(select_trans.iloc[:,0].values)
		if options.id_type == 'transcript_id':
			select_trans=select_trans.intersection(selectTrans)
			print("There are " + str(len(select_trans)) + " transcripts from "+options.in_selectTrans+" used for following analysis.",file=sys.stderr)
		elif options.id_type == 'gene_id':
			tmp=[geneID2transID[gene_id] for gene_id in select_trans if gene_id in geneID2transID]
			select_trans=set(tmp)
			select_trans=select_trans.intersection(selectTrans)
			print("There are " + str(len(select_trans))+" gene id could be transformed into transcript id and used for following analysis.",file=sys.stderr)
		elif options.id_type == 'gene_name' or options.id_type=='gene_symbol':
			tmp=[geneName2transID[gene_name] for gene_name in select_trans if gene_name in geneName2transID]
			select_trans=set(tmp)
			select_trans=select_trans.intersection(selectTrans)
			print("There are " + str(len(select_trans))+" gene symbol could be transformed into transcript id and used for following analysis.",file=sys.stderr)
		else:
			raise IOError("Please input a approproate id_type parameters.[transcript_id/gene_id/gene_name/]")
	else:
		select_trans=selectTrans


	if (type1 and (not type2) and (not motifList1) and (not motifList2)):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			(bamfs.motifDensity,bamfs.RecordList1)=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,type1=type1,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'di-AA')
		write_mofitDensity_dataframe_one_type(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)

	if (type2 and (not type1) and (not motifList1) and (not motifList2)):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			bamfs.motifDensity,bamfs.RecordList2=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,type2=type2,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'tri-AA')
		write_mofitDensity_dataframe_one_type(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)

	if (type1 and type2 and (not motifList1) and (not motifList2)):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			(bamfs.motifDensity_1,bamfs.motifDensity_2,bamfs.RecordList1,bamfs.RecordList2)=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,type1=type1,type2=type2,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'both')
		write_mofitDensity_dataframe_two_types(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)

	if ((not type1) and (not type2) and motifList1 and (not motifList2)):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			bamfs.motifDensity,bamfs.RecordList1=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,motifList1=motifList1,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'di-AA')
		write_mofitDensity_dataframe_one_type(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)

	if ((not type1) and (not type2) and (not motifList1) and motifList2):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			bamfs.motifDensity,bamfs.RecordList2=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,motifList2=motifList2,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'tri-AA')
		write_mofitDensity_dataframe_one_type(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)

	if ((not type1) and (not type2) and motifList1 and motifList2):
		for bamfs in bam_attr:
			print("Start analyze the sample: "+str(bamfs.bamName),file=sys.stderr)
			(bamfs.motifDensity_1,bamfs.motifDensity_2,bamfs.RecordList1,bamfs.RecordList2)=find_motif(bamfs.bamName,select_trans,transLengthDict,startCodonCoorDict,stopCodonCoorDict,bamfs.bamLen,bamfs.bamOffset,min_cds_counts,min_cds_codon,
			transcript_fasta,motifList1=motifList1,motifList2=motifList2,mode=mode,table=table)
			print("Finish the step of calculate the motif density of genes",file=sys.stderr)
		## output density
		write_motif_list(bam_attr,output_prefix,'both')
		write_mofitDensity_dataframe_two_types(bam_attr,output_prefix+"_motifDensity_dataframe.txt")
		print("Finish the step of write motif density file!",file=sys.stderr)



def main():
	"""main program"""
	parse_args_for_triplete_AA_motif()

if __name__ == "__main__":
		main()













