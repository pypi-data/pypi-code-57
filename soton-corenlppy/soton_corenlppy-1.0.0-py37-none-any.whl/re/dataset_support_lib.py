# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	/////////////////////////////////////////////////////////////////////////
	//
	// (c) Copyright University of Southampton IT Innovation, 2019
	//
	// Copyright in this software belongs to IT Innovation Centre of
	// Gamma House, Enterprise Road, Southampton SO16 7NS, UK.
	//
	// This software may not be used, sold, licensed, transferred, copied
	// or reproduced in whole or in part in any manner or form or in or
	// on any media by any person other than in accordance with the terms
	// of the Licence Agreement supplied with the software, or otherwise
	// without the prior written consent of the copyright owners.
	//
	// This software is distributed WITHOUT ANY WARRANTY, without even the
	// implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
	// PURPOSE, except where stated in the Licence Agreement supplied with
	// the software.
	//
	// Created By : Stuart E. Middleton
	// Created Date : 2019/08/31
	// Created for Project: FLORAGUARD
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies: None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

Support lib for working with pretrained embedding datasets and other large NLP corpora

"""

import array,sys,codecs,os,re,copy,math,multiprocessing,threading,traceback,logging,time,tempfile,subprocess,datetime,signal
import soton_corenlppy, soton_corenlppy.re

#file_bert_vocab = '/projects/datasets/bert/wwm_cased_L-24_H-1024_A-16/vocab.txt'
#dir_propbank = '/projects/datasets/propbank-release-master'
#dir_ewt = '/projects/datasets/LDC/english web treebank/eng_web_tbk'
#training_file_limit = 20
#test_file_limit = 2
#bool_bert_vocab_lowercase = False

#file_bert_vocab = '/floraguard/bert-experiment/datasets/bert/wwm_cased_L-24_H-1024_A-16/vocab.txt'
#dir_propbank = '/floraguard/bert-experiment/datasets/propbank-release-master'
#dir_ewt = '/floraguard/bert-experiment/datasets/eng_web_tbk'

#
# propbank support functions
#

def read_propbank( propbank_dir = None, ewt_dir = None, max_files = None, dict_openie_config = None ) :
	"""
	read in the Propbank dataset and cross-index it with the English Web Treebank dataset to provide a set of SRL annotated sentences.

	:param unicode propbank_dir: location of Propbank dataset dir
	:param unicode ewt_dir: location of English Web Treebank dataset dir
	:param int max_files: max number of files to load (None for all files). this is useful for testing purposes.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: dict of Propbank file sent SRL annotations = { EWT_filename : { sent_index : ( [ word_token1, ... ], [ pos_token1, ... ], [ [ iob_token1, ... ], ... x N_clauses_in_sent ] ) } }
	:rtype: dict
	"""

	if not isinstance( propbank_dir, str ) :
		raise Exception( 'invalid propbank_dir' )
	if not isinstance( ewt_dir, str ) :
		raise Exception( 'invalid ewt_dir' )
	if not isinstance( max_files, (int,type(None)) ) :
		raise Exception( 'invalid max_files' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	dictFiles = {}

	#
	# read propbank data files (to get SRL and POS labels for words)
	#
	# e.g. \propbank-release-master\data\google\ewt\answers\00\20070404104007AAY1Chs_ans.xml.gold_skel

	listFilesToProcess = []
	if os.path.exists( propbank_dir ) == False :
		raise Exception( 'propbank dir does not exist : ' + repr(propbank_dir) ) 
	strEnglishWebTreebankDir = os.path.abspath( propbank_dir ) + os.sep + 'data' + os.sep + 'google' + os.sep + 'ewt'
	listFiles1 = os.listdir( strEnglishWebTreebankDir )
	for strFile1 in listFiles1 :

		if os.path.isdir( strEnglishWebTreebankDir + os.sep + strFile1 ) :
			listFiles2 = os.listdir( strEnglishWebTreebankDir + os.sep + strFile1 )

			for strFile2 in listFiles2 :

				if os.path.isdir( strEnglishWebTreebankDir + os.sep + strFile1 + os.sep + strFile2 ) :
					listFiles3 = os.listdir( strEnglishWebTreebankDir + os.sep + strFile1 + os.sep + strFile2 )

					for strFile3 in listFiles3 :
						if strFile3.endswith( '.gold_skel' ) == True :
							listFilesToProcess.append( ( strEnglishWebTreebankDir + os.sep + strFile1 + os.sep + strFile2 + os.sep + strFile3, strFile1, strFile3 ) )

	# set a limit on number of files to read (useful for testing prior to a full run)
	if max_files == None :
		nMaxFiles = 1000000
	else :
		nMaxFiles = max_files

	nCountFiles = 0
	while (nCountFiles < nMaxFiles) and (nCountFiles < len(listFilesToProcess)) :
		(strFileWithPath, strDataset, strFile) = listFilesToProcess[nCountFiles]

		readHandle = codecs.open( strFileWithPath, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		#
		# Propbank example
		#
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   0   [WORD]   WRB    (TOP(S(SBARQ(WHADVP*)                 -        -  (ARGM-LOC*)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   1   [WORD]    MD                    (SQ*                  -        -  (ARGM-MOD*)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   2   [WORD]   PRP                    (NP*)                 -        -      (ARG0*)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   3   [WORD]    VB                    (VP*                get   get.01         (V*)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   4   [WORD]   NNS                    (NP*)                 -        -      (ARG1*)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   5   [WORD]    IN                    (PP*                  -        -  (ARGM-LOC*            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   6   [WORD]   NNP                    (NP*                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   7   [WORD]   NNP                       *)))))             -        -           *)           *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   8   [WORD]     ,                       *                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0   9   [WORD]   PRP                (S(S(NP*)                 -        -           *       (ARG0*)           * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  10   [WORD]    MD                    (VP*                  -        -           *   (ARGM-MOD*)           * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  11   [WORD]    VB                    (VP*              liken  like.01           *          (V*)           * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  12   [WORD]    DT                    (NP*                  -        -           *       (ARG1*            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  13   [WORD]    JJ                       *                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  14   [WORD]    NN                       *))))              -        -           *            *)           * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  15   [WORD]     ,                       *                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  16   [WORD]    CC                       *                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  17   [WORD]   PRP                  (S(NP*)                 -        -           *            *       (ARG0*)
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  18   [WORD]    MD                    (VP*                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  19   [WORD]    TO                  (S(VP*                  -        -           *            *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  20   [WORD]    VB                    (VP*                try   try.01           *            *          (V*)
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  21   [WORD]   NNS                    (NP*)                 -        -           *            *       (ARG1*)
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  22   [WORD]    UH                  (INTJ*)))))))           -        -           *            *   (ARGM-DIS*)
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    0  23   [WORD]     .                       *))                -        -           *            *            * 
		#
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    1   0   [WORD]   PRP    (TOP(S(S(NP*)                       -          -  (ARG0*)           *          *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    1   1   [WORD]   VBD            (VP*                   search  search.01     (V*)           *          *            * 
		#google/ewt/answers/00/20070404104007AAY1Chs_ans.xml    1   2   [WORD]    RB            (PP*                        -          -  (ARG1*            *          *            * 

		dictSents = {}

		listWords = []
		listPOS = []
		listSRL = []
		listPredicateWordSense = []
		nSRLCount = 0
		nSentIndex = None
		for strLine in listLines :
			if len( strLine.strip() ) > 0 :

				# split by space and remove any empty strings (as there will be multiple spaces between values)
				listComponents = strLine.strip().split(' ')
				while listComponents.count('') :
					listComponents.remove('')

				if len(listComponents) < 7 :
					raise Exception('error parsing file (number of columns) ' + repr(strFileWithPath) + ' : ' + repr(strLine) )

				# send index
				if nSentIndex != None :
					if int( listComponents[1] ) != nSentIndex :
						raise Exception('error parsing file (sent index) ' + repr(strFileWithPath) + ' : ' + repr(strLine) )
				else :
					nSentIndex = int( listComponents[1] )

				# word will always be [WORD] in propbank as we need to cordd-ref it with EWT tokenized sentences
				listWords.append( listComponents[3] )
				listPOS.append( listComponents[4] )
				listSRL.append( listComponents[8:] )
				listPredicateWordSense.append( listComponents[7] )

				if nSRLCount == 0 :
					nSRLCount = len( listComponents[8:] )
				elif len( listComponents[8:] ) != nSRLCount :
					raise Exception('SRL count mismatch between words : ' + repr(strFileWithPath) + ' : ' + repr(strLine) )

			else :
				# newline is a sentence delimiter
				if len(listWords) > 0 :
					listSRLSets = []

					# no SRL? add sentence with all labels as 'O'
					if nSRLCount == 0 :
						listSRLSets.append( 'O'*len(listWords) )

					else :
						# for each SRL entry add a new fully annotated sentence (so we will get several copies of sent with different SRL if it has multiple relations)
						# a SRL entry is always terminates with a ) so no need to look after open fragments

						# debug - force 1 SRL entry per sent for testing pourposes
						# nSRLCount = 1
						# end debug

						for nIndexSRL in range(nSRLCount) :
							listSRLInstance = []
							strOpenRole = None
							strOpenPred = None

							for nTokenIndex in range(len(listSRL)) :
								entry = listSRL[nTokenIndex]
								strSRL = entry[nIndexSRL]

								if strSRL.startswith('(') :
									strOpenRole = strSRL.strip('()*')
									strIOB = 'B-' + strOpenRole
								elif strOpenRole != None :
									strIOB = 'I-' + strOpenRole
								else :
									strIOB = 'O'

								# append the predicate word sense to the verb IOB tag so it can be used to train
								# in SRL tasks the predicate location is provided but not the predicate wordsense
								if strSRL.startswith('(V*') :
									strOpenPred = listPredicateWordSense[nTokenIndex]
								
								if strOpenPred != None :
									strIOB = strIOB + '-' + strOpenPred

								if strSRL.endswith(')') :
									strOpenRole = None
									strOpenPred = None

								listSRLInstance.append( strIOB )

							listSRLSets.append( listSRLInstance )

							if strOpenRole != None :
								raise Exception('SRL parse error : ' + repr(strFileWithPath) + ' : ' + repr(strLine) )

					# { sent_index : ( list_words, list_pos, ( list_IOB, list_IOB, ... ) ) }
					dictSents[nSentIndex] = ( listWords, listPOS, listSRLSets )

				# reset sent and start again
				listWords = []
				listPOS = []
				listPredicateWordSense = []
				listSRL = []
				nSRLCount = 0
				nSentIndex = None

		# add propbank annotated sent data for this file
		# { ewt_source_filename : { sent_index : ( list_words, list_pos, ( list_IOB, list_IOB, ... ) ) } }
		strSourceFile = strFile[:-1*len('.xml.gold_skel')] + '.txt'
		strEWTSourceFile = ewt_dir + os.sep + 'data' + os.sep + strDataset + os.sep + 'source' + os.sep + 'source_text_ascii_tokenized' + os.sep + strSourceFile
		dictFiles[strEWTSourceFile] = dictSents

		# update file count
		nCountFiles = nCountFiles + 1

	#
	# read english web treebank data files (to get original words to replace placeholders in propbank)
	#
	# e.g. \eng_web_tbk\data\answers\source\source_text_ascii_tokenized\20070404104007AAY1Chs_ans.txt

	for strEWTSourceFile in dictFiles :
		# load source file
		readHandle = codecs.open( strEWTSourceFile, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		#
		# EWT example
		#
		#<en=1>where can I get morcillas in tampa bay , I will like the argentinian type , but I will to try anothers please ?
		#<en=2>I searched all over the internet , but I could not find one place in Tampa Bay that sells morcillas , also known as blood pudding , black pudding and blood sausages .
		#<en=3>I learned that morcillas are basically impossible to find all across the North American region .
		#<en=4>But I did find this website , www.igourmet.com , where they sell all types of sausages , including blood sausages !
		#<en=5>So follow the link at the bottom and buy some blood sausages .
		#<en=6>huh ?
		#<en=7>yuck !!
		#<en=8>I do n't know , and it is because I do n't like them , do you know that , morcillas is coagulated blood from animals , ewww

		nSentIndex = 0
		for strLine in listLines :

			if len( strLine.strip() ) > 0 :
				listComponents = strLine.strip().split(' ')
				if len(listComponents) < 1 :
					raise Exception('error parsing file (not enough tokens) ' + repr(strEWTSourceFile) + ' : ' + repr(strLine) )

				# remove sent index from first token
				if listComponents[0].count('>') > 0 :
					listComponents[0] = listComponents[0][ listComponents[0].index('>') + 1 : ]
				else :
					raise Exception('error parsing file (missing sent marker on first token) ' + repr(strEWTSourceFile) + ' : ' + repr(strLine) )
				
				# replace [WORD] propbank placeholders with the actual word from EWT source file
				( listWords, listPOS, listSRLSets ) = dictFiles[strEWTSourceFile][nSentIndex]
				if len(listWords) != len(listComponents) :
					raise Exception('error source file has different number of tokens to propbank file ' + repr(strEWTSourceFile) + ' : ' + repr(strLine) )
				for nIndexWord in range(len(listWords)) :
					listWords[nIndexWord] = listComponents[nIndexWord]

				# next sent
				nSentIndex = nSentIndex + 1

	# all done
	return dictFiles

#
# BERT support functions
#

def generate_vocab( list_word_sets = None, list_tag_sets = None, dict_openie_config = None ) :
	"""
	make a set of (word,tag) sequences for a sentence in BERT format.
	e.g. sent = [CLS] ... [SEP] ... [SEP] [PAD] [PAD] [PAD] ...

	:param list list_word_sets: list of words for each sent
	:param list list_tag_sets: list of tags for each sent
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: tuple = ( list_words_vocab, list_tags_vocab, list_predicates_vocab, dict_index_words, dict_index_tags, dict_index_predicates, index_pad_word, index_pad_tag, index_pad_predicate )
	:rtype: tuple
	"""

	if not isinstance( list_word_sets, list ) :
		raise Exception( 'invalid list_word_sets' )
	if not isinstance( list_tag_sets, list ) :
		raise Exception( 'invalid list_tag_sets' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if (list_tag_sets != None) and (len(list_tag_sets) != len(list_word_sets)) :
		raise Exception( 'mismatch num sets - word, tag' )

	setWords = set([])
	setTags = set([])
	setPredicates = set([])
	for nIndex in range(len(list_word_sets)) :
		listTaggedSent = []

		listTokens = list_word_sets[nIndex].split(' ')

		if list_tag_sets != None :
			listTags = list_tag_sets[nIndex].split(' ')
		else :
			# if no tags are provided assign 'O' to all tokens
			listTags = ['O'] * len(listTokens)
			listTags[0] = '[CLS]'
			listTags[-1] = '[SEP]'

		for nIndexWord in range(len(listTokens)) :
			setWords.add( listTokens[nIndexWord] )
			setTags.add( listTags[nIndexWord] )

			if listTags[nIndexWord].startswith('B-V-') == True :
				# extract wordsense of predicate
				strPredicate = listTags[nIndexWord][ len('B-V-') : ]
			elif listTags[nIndexWord].startswith('I-V-') == True :
				strPredicate = 'X'
			else :
				strPredicate = 'O'
			setPredicates.add( strPredicate )

	# make set into an index so we can lookup phrases later by index id
	listWords = list(setWords)
	listTags = list(setTags)
	listPredicates = list(setPredicates)

	# add token for unknown vocabulary (for test corpus which might have vocabulary not seen in training corpus) and padding
	listWords.append( '???' )
	if not '[PAD]' in listWords :
		listWords.append( '[PAD]' )
	if not '[PAD]' in listTags :
		listTags.append( '[PAD]' )
	if not '[PAD]' in listPredicates :
		listPredicates.append( '[PAD]' )

	# make an inverted index of words and tags
	dictIndexWord = {}
	for nIndexEntry in range(len(listWords)) :
		dictIndexWord[listWords[nIndexEntry]] = nIndexEntry

	# padding token for words is '[PAD]'
	nPaddingIndexWord = dictIndexWord['[PAD]']

	dictIndexTag = {}
	for nIndexEntry in range(len(listTags)) :
		dictIndexTag[listTags[nIndexEntry]] = nIndexEntry

	# padding token for tags is '[PAD]'
	nPaddingIndexTag = dictIndexTag['[PAD]']

	dictIndexPredicate = {}
	for nIndexEntry in range(len(listPredicates)) :
		dictIndexPredicate[listPredicates[nIndexEntry]] = nIndexEntry

	# padding token for predicates is '[PAD]'
	nPaddingIndexPredicate = dictIndexPredicate['[PAD]']

	print(( 'padding word index = ', repr(nPaddingIndexWord) ))
	print(( 'padding tag index = ', repr(nPaddingIndexTag) ))
	print(( 'word list size = ', repr(len(listWords)) ))
	print(( 'tag list size = ', repr(len(listTags)) ))
	print(( 'predicate list size = ', repr(len(listPredicates)) ))
	print(( 'word index size = ', repr(len(dictIndexWord)) ))
	print(( 'tag index size = ', repr(len(dictIndexTag)) ))
	print(( 'tag index size = ', repr(len(dictIndexPredicate)) ))

	return ( listWords, listTags, listPredicates, dictIndexWord, dictIndexTag, dictIndexPredicate, nPaddingIndexWord, nPaddingIndexTag, nPaddingIndexPredicate )

def generate_sequence( index_words = None, index_tags = None, index_predicates = None, padding_word_value = None, padding_tag_value = None, padding_predicate_value = None, sequence_length = None, list_word_sets = None, list_tag_sets = None, dict_openie_config = None ) :
	"""
	make a set of (word,tag) sequences for each sentence

	:param dict index_words: index of words from generate_vocab()
	:param dict index_tags: index of tags from generate_vocab()
	:param dict index_predicates: index of predicates from generate_vocab()
	:param int padding_word_value: value of pad word in the index
	:param int padding_tag_value: value of pad word in the index
	:param int padding_predicate_value: value of pad word in the index
	:param int sequence_length: max length of sequence (e.g. sentence length) - can be None for no limit. This is needed to limit sents to a fixed size for use in embeddings with BERT
	:param list list_word_sets: list of vocab words from generate_vocab()
	:param list list_tag_sets: list of vocab words from generate_vocab()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: tuple = ( list_seq_words, list_seq_tags_categorical, list_seq_predicates_categorical, max_seq_length )
	:rtype: tuple
	"""

	if not isinstance( index_words, dict ) :
		raise Exception( 'invalid index_words' )
	if not isinstance( index_tags, dict ) :
		raise Exception( 'invalid index_tags' )
	if not isinstance( index_predicates, dict ) :
		raise Exception( 'invalid index_predicates' )
	if not isinstance( padding_word_value, int ) :
		raise Exception( 'invalid padding_word_value' )
	if not isinstance( padding_predicate_value, int ) :
		raise Exception( 'invalid padding_predicate_value' )
	if not isinstance( sequence_length, int ) :
		raise Exception( 'invalid sequence_length' )
	if not isinstance( list_word_sets, list ) :
		raise Exception( 'invalid list_word_sets' )
	if not isinstance( list_tag_sets, list ) :
		raise Exception( 'invalid list_tag_sets' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if (list_tag_sets != None) and (len(list_tag_sets) != len(list_word_sets)) :
		raise Exception( 'mismatch num sets - word, tag' )

	if (sequence_length != None) and (sequence_length < 2) :
		raise Exception( 'sequence_length too small' )

	nMaxLen = 0
	listTaggedSentSet = []
	for nIndex in range(len(list_word_sets)) :
		listTaggedSent = []

		listTokens = list_word_sets[nIndex].split(' ')

		#print( 'sent = ', repr(listTokens) )

		if sequence_length != None :
			# truncate sentence if its too long
			if len(listTokens) > sequence_length :
				listTokens = listTokens[:sequence_length]

			# force padded sequence length to be of this predefined length
			nMaxLen = sequence_length
		else :
			# get the longest sentence and use this as padded sequence length
			nMaxLen = max( nMaxLen, len(listTokens) )

		if list_tag_sets != None :
			listTags = list_tag_sets[nIndex].split(' ')
		else :
			listTags = None

		#print( 'tags = ', repr(listTags) )

		for nIndexWord in range(len(listTokens)) :
			# token not in the vocab list? replace with '???' if so
			strToken = listTokens[nIndexWord]
			if not listTokens[nIndexWord] in index_words :
				strToken = '???'
			
			# do we have a tag? if not its 'O' in IOB tagging scheme
			if listTags != None :
				strTag = listTags[nIndexWord]
			else :
				if nIndexWord == 0 :
					strTag = '[CLS]'
				elif nIndexWord == len(listTokens)-1 :
					strTag = '[SEP]'
				else :
					strTag = 'O'

			if strTag.startswith('B-V-') == True :
				strPredicate = strTag[ len('B-V-'): ]
				if not strPredicate in index_predicates :
					strPredicate = '???'
			elif strTag.startswith('I-V-') == True :
				strPredicate = 'X'
			else :
				strPredicate = 'O'

			listTaggedSent.append( ( strToken, strTag, strPredicate ) )

		listTaggedSentSet.append( listTaggedSent )

		#print( 'tagged sent = ', repr(listTaggedSent) )

	print(( 'max token length = ', repr(nMaxLen) ))

	# generate sequences of words and tags for training
	# - sequence = [CLS] some words give me trouble [SEP] give [SEP]
	# note: sequences are padded to max_length of longest word sentence (including the predicates) so they have the same size allowing embedding token index values to be added later

	listSequenceSetWords = []
	listSequenceSetPredicates = []
	listSequenceSetTags = []
	for listTaggedSent in listTaggedSentSet :
		listSequenceWords = []
		listSequenceTags = []
		listSequencePredicates = []

		for (strWord,strTag,strPredicate) in listTaggedSent :

			listSequenceWords.append( index_words[strWord] )
			listSequenceTags.append( index_tags[strTag] )
			listSequencePredicates.append( index_predicates[strPredicate] )
		
		#if len(listSequenceWords) != sequence_length :
		#	raise Exception('word length incorrect : ' + repr(len(listSequenceWords)) )

		listSequenceSetWords.append( listSequenceWords )
		listSequenceSetPredicates.append( listSequencePredicates )
		listSequenceSetTags.append( listSequenceTags )

	# pad sequences so they all have the same length
	# use int16 to save memory. we need to represent word and tag indexes in the sequence so int16 allows 65,536‬ unique words to be represented in index (probbank has about 20,000 unique words, bert 30,000)

	if len(index_words) > 16*1024 :
		raise Exception('int16 too small for number of words')
	listSequenceSetWords = keras.preprocessing.sequence.pad_sequences(
		maxlen = nMaxLen,
		sequences = listSequenceSetWords,
		padding = 'post',
		value = padding_word_value,
		dtype='int16' )

	if len(index_tags) > 16*1024 :
		raise Exception('int16 too small for number of words')
	listSequenceSetPredicates = keras.preprocessing.sequence.pad_sequences(
		maxlen = nMaxLen,
		sequences = listSequenceSetPredicates,
		padding = 'post',
		value = padding_predicate_value,
		dtype='int16' )

	if len(index_predicates) > 16*1024 :
		raise Exception('int16 too small for number of words')
	listSequenceSetTags = keras.preprocessing.sequence.pad_sequences(
		maxlen = nMaxLen,
		sequences = listSequenceSetTags,
		padding = 'post',
		value = padding_tag_value,
		dtype='int16' )

	# convert tag values to keras 'categorical' type as we have a multi-class problem (each word can have a tag from a set of mutually exclusive labels)
	# later this means we will use the loss function "categorical_crossentropy".
	# use int16 to save memory as this will be converted into large array = Matrix[Nsent_length x Nsent_length] x Nsent
	listSequenceSetTagsCategorical = []
	for nIndexSequence in range(len(listSequenceSetTags)) :
		matrixObj = keras.utils.to_categorical(
			y = listSequenceSetTags[nIndexSequence],
			num_classes = len(index_tags),
			dtype='int16' )
		listSequenceSetTagsCategorical.append( matrixObj )

	# convert predicate values to keras 'categorical' type as we have a multi-class problem (each word can have a tag from a set of mutually exclusive labels)
	listSequenceSetPredicatesCategorical = []
	for nIndexSequence in range(len(listSequenceSetPredicates)) :
		matrixObj = keras.utils.to_categorical(
			y = listSequenceSetPredicates[nIndexSequence],
			num_classes = len(index_predicates),
			dtype='int16' )
		listSequenceSetPredicatesCategorical.append( matrixObj )

	# return the values
	return ( listSequenceSetWords, listSequenceSetTagsCategorical, listSequenceSetPredicatesCategorical, nMaxLen )

def create_corpus( dict_propbank = None, pad_to_size = None, test_fraction = 0.1, dict_openie_config = None ) :
	"""
	create a BERT style training corpus from propbank data.
	e.g. sent = [CLS] ... [SEP] ... [SEP] [PAD] [PAD] [PAD] ...

	:param dict dict_propbank: propbank data from read_propbank()
	:param int pad_to_size: size to pad sequences to (can be None)
	:param float test_fraction: fraction of corpus to use as test data
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: tuple = ( list_train_corpus_words, list_train_corpus_tags, list_test_corpus_words, list_test_corpus_tags )
	:rtype: tuple
	"""

	if not isinstance( dict_propbank, dict ) :
		raise Exception( 'invalid dict_propbank' )
	if not isinstance( pad_to_size, int ) :
		raise Exception( 'invalid pad_to_size' )
	if not isinstance( test_fraction, (float,type(None)) ) :
		raise Exception( 'invalid test_fraction' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listTrainingCorpusWords = []
	listTrainingCorpusTags = []

	for strFile in dictPropbankFiles :
		dictSents = dictPropbankFiles[strFile]

		for nSentIndex in dictSents :
			( listWords, listPOS, listSRLSets ) = dictSents[nSentIndex]

			# init tokenized structures
			listWordsTokenized = []
			listPOSTokenized = []
			listSRLSetsTokenized = []
			for listSRL in listSRLSets :
				listSRLSetsTokenized.append( [] )

			# apply WordPiece tokenization to each words and insert N pieces using original word/pos/srl tags
			for nIndexWord in range(len(listWords)) :
				strWord = listWords[nIndexWord]
				strPOS = listPOS[nIndexWord]

				# get word pieces for this word
				listWordPieces = wordpiece_tokenizer.tokenize( strWord )

				# insert pieces (words and pos)
				for strPiece in listWordPieces :
					listWordsTokenized.append( strPiece )
					listPOSTokenized.append( strPOS )

				# insert pieces (srl)
				for nIndexSRLSet in range(len(listSRLSets)) :
					listSRL = listSRLSets[nIndexSRLSet]
					if len(listSRL) != len(listWords) :
						raise Exception( 'Word len != SRL len' )

					bBegin = False
					for strPiece in listWordPieces :

						# ensure only first piece has the begin SRL label
						if (listSRL[nIndexWord].startswith('B-') == True) and (bBegin == True) :
							strSRL = 'I-' + listSRL[nIndexWord][2:]
						elif (listSRL[nIndexWord].startswith('B-') == True) and (bBegin == False) :
							strSRL = listSRL[nIndexWord]
							bBegin = True
						else :
							strSRL = listSRL[nIndexWord]

						listSRLSetsTokenized[nIndexSRLSet].append( strSRL )

			# create the training corpus words and tags
			for listSRL in listSRLSetsTokenized :
				# get the first predicate token (if any) to be added at the end of the training sent
				strPredicatePhrase = '[NONE]'
				strPredicateTagPhrase = '[NONE]'

				for nIndexToken in range(len(listSRL)) :
					strTag = listSRL[nIndexToken]
					if strTag.startswith( 'B-V-' ) == True :
						strPredicatePhrase = listWordsTokenized[nIndexToken]
						strPredicateTagPhrase = strTag[ len('B-V-') : ]

				'''
				listPredicateWords = []
				listPredicateTags = []

				for nIndexToken in range(len(listSRL)) :
					strTag = listSRL[nIndexToken]
					if (strTag.startswith( 'B-V' ) == True) or (strTag.startswith( 'I-V' ) == True) :
						strWord = listWordsTokenized[nIndexToken]
						listPredicateWords.append( strWord )
						listPredicateTags.append( strTag )

				if len(listPredicateWords) > 0 :
					strPredicatePhrase = ' '.join( listPredicateWords ) + ' '
					strPredicateTagPhrase = ' '.join( listPredicateTags ) + ' '
				else :
					strPredicatePhrase = '--- '
					strPredicateTagPhrase = '--- '
				'''

				# pad sentence (leaving 3 for [SEP] pred [SEP] at end)
				if (pad_to_size != None) and (len(listWordsTokenized) < pad_to_size) :
					for nPadIndex in range( pad_to_size - len(listWordsTokenized) - 3 ) :
						listWordsTokenized.append( '[PAD]' )
						listSRL.append( '[PAD]' )
				
				# add a copy of the sent for each different SRL annotation
				# this means the same sent will appear with its full variety of SRL annotations
				listTrainingCorpusWords.append( '[CLS] ' + ' '.join( listWordsTokenized ) + ' [SEP] ' + strPredicatePhrase + ' [SEP]' )
				listTrainingCorpusTags.append( '[CLS] ' + ' '.join( listSRL ) + ' [SEP] ' + strPredicateTagPhrase + ' [SEP]' )

	# for testing make the test corpus a fraction of the training set (should get really good SRL classification rates)
	if test_fraction == None :
		nNumTestFiles = 0
	else :
		nNumTestFiles = test_fraction * len(listTrainingCorpusWords)

	listTestCorpusWords = listTrainingCorpusWords[:nNumTestFiles]
	listTestCorpusTags = listTrainingCorpusTags[:nNumTestFiles]
	listTrainingCorpusWords = listTrainingCorpusWords[nNumTestFiles:]
	listTrainingCorpusTags = listTrainingCorpusTags[nNumTestFiles:]

	# all done
	return ( listTrainingCorpusWords, listTrainingCorpusTags, listTestCorpusWords, listTestCorpusTags )

#
# streusle support functions
#

def read_streusle( streusle_home = None, allowed_id_set = None, dict_config = None ) :
	"""
	read in streusle dataset. for information about the corpus see https://github.com/nert-nlp/streusle/blob/master/CONLLULEX.md

	:param unicode streusle_home: dir of streusle dataset
	:param list allowed_id_set: list of allowed IDs (None for no filter)
	:param dict dict_config: config object

	:return: dict = { sent_index : { 'sent_id' : <str>, 'text' : <str>, 'tokens' : <list>, 'phrases' : <dict>, 'phrases_addr' : <dict> }. 'tokens' will have a list of 19 columns with multi-word extraction address ranges converted from str to tuple(mwe_id,rel_position_in_mwe). 'phrases' is a dict with key verb|prep|noun and value of phrases. 'phrases_addr' is the same but with a list of token addresses for each phrase not a string.
	:rtype: dict
	"""

	if not isinstance( streusle_home, str ) :
		raise Exception( 'invalid streusle_home' )
	if not isinstance( allowed_id_set, (list,type(None)) ) :
		raise Exception( 'invalid allowed_id_set' )
	if not isinstance( dict_config, dict ) :
		raise Exception( 'invalid dict_config' )

	if not 'verb_phrase_lexcat' in dict_config :
		raise Exception( 'verb_phrase_lexcat missing from config' )
	if not 'prep_phrase_lexcat' in dict_config :
		raise Exception( 'prep_phrase_lexcat missing from config' )
	if not 'noun_phrase_lexcat' in dict_config :
		raise Exception( 'noun_phrase_lexcat missing from config' )

	dictClassPatterns = {
		'verb' : dict_config['verb_phrase_lexcat'],
		'prep' : dict_config['prep_phrase_lexcat'],
		'noun' : dict_config['noun_phrase_lexcat']
		}

	readHandle = None
	writeHandle = None

	#
	# load streusle data file 'streusle.conllulex' into memory as a dict indexed by streusle_sent_id
	#
	try :
		if os.path.exists( streusle_home ) == False :
			raise Exception( 'streusle home dir missing : ' + repr(streusle_home) )
		strInputFile = os.path.abspath( streusle_home ) + os.sep + 'streusle.conllulex'
		readHandle = codecs.open( strInputFile, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		# # newdoc id = reviews-001325
		# # sent_id = reviews-001325-0001
		# # text = Highly recommended
		# # streusle_sent_id = ewtb.r.001325.1
		# # mwe = Highly recommended
		# 1	Highly	highly	ADV	RB	_	2	advmod	2:advmod	_	_	ADV	highly	_	_	_	_	_	O-ADV
		# 2	recommended	recommend	VERB	VBN	Tense=Past|VerbForm=Part	0	root	0:root	_	_	V	recommend	v.communication	_	_	_	_	O-V-v.communication

		dictSentSet = {}

		listTokens = []
		strSentID = None
		dictSentTokens = {}
		nSentIndex = 0
		nTokenIndex = 0

		for strLine in listLines :
			strLineClean = strLine.strip()

			if strLineClean.startswith('# streusle_sent_id =') :
				strSentID = strLineClean[ len('# streusle_sent_id =') : ]
			
			elif len(strLineClean) == 0 :
				# compute text from tokens (not original untokenized text)

				# newline indicates the end of a sentence so add a new sent entry
				# note: make text by using tokens NOT the original text to preserve the token index for stuff like 'spot-on' == 'spot' '-' 'on'
				if (allowed_id_set == None) or (nSentIndex in allowed_id_set) :
					dictSentSet[ nSentIndex ] = {
						'sent_id' : strSentID,
						'text' : ' '.join( listTokens ),
						'tokens' : dictSentTokens
						}

				# reset sent data
				listTokens = []
				strSentID = None
				dictSentTokens = {}
				nTokenIndex = 0
				nSentIndex = nSentIndex + 1

			elif not strLineClean.startswith('#') :
				listParts = strLineClean.split('\t')
				if len(listParts) != 19 :
					raise Exception( 'token entry does not have 19 columns : ' + repr(strLineClean) )

				# strong multi-word extraction (SMWE) = [ mwe_id, relative_token_position_in_group ] e.g. [1,1] = mwe #1, 1st token
				if not listParts[10] == '_' :
					listParts2 = listParts[10].split(':')
					tupleMWE = ( int(listParts2[0]), int(listParts2[1]) )
				else :
					tupleMWE = None
				listParts[10] = tupleMWE

				# weak multi-word extraction (SMWE) = [ mwe_id, relative_token_position_in_group ] e.g. [1,1] = mwe #1, 1st token
				if not listParts[15] == '_' :
					listParts2 = listParts[15].split(':')
					tupleMWE = ( int(listParts2[0]), int(listParts2[1]) )
				else :
					tupleMWE = None
				listParts[15] = tupleMWE

				# add token details to the dict. tokens appear sequentially so use the sequence index NOT the 1st column index as sometimes there is a value of 6, 7, *7.1*, 8 ... 
				dictSentTokens[ nTokenIndex ] = listParts[1:]
				listTokens.append( listParts[1] )
				nTokenIndex = nTokenIndex + 1

		if strSentID != None :
			# add last sent entry if we have one left running
			if (allowed_id_set == None) or (nSentIndex in allowed_id_set) :
				dictSentSet[ nSentIndex ] = {
					'sent_id' : strSentID,
					'text' : ' '.join( listTokens ),
					'tokens' : dictSentTokens
					}

	finally :
		if readHandle != None :
			readHandle.close()
		readHandle = None

	dict_config['logger'].info('loaded ' + str(len(dictSentSet)) + ' streusle sents')

	#
	# construct verb, prep and noun phrase sets, using the MWE (multi-word extraction) annotations
	#

	for nSentID in dictSentSet :
		dictPhrase = {}
		nGroupIndexSingle = 1000

		# first pass get all single tokens and MWE that match a LEXCAT of interest
		for nTokenID in dictSentSet[nSentID]['tokens'] :
			# remember original index 0 was removed and became token_id
			strToken = dictSentSet[nSentID]['tokens'][nTokenID][0]
			strLexCat = dictSentSet[nSentID]['tokens'][nTokenID][10]

			# only bother with SMWE
			tupleMWE = dictSentSet[nSentID]['tokens'][nTokenID][9]

			for strType in dictClassPatterns :
				for strLexCatAllowed in dictClassPatterns[strType] :
					if strLexCatAllowed == strLexCat :

						if tupleMWE == None :
							# add single tokens in a unique new group ID
							dictPhrase[ nGroupIndexSingle ] = [ [ strToken ], [ nTokenID ], strType ]
							nGroupIndexSingle = nGroupIndexSingle + 1
						else :
							# add multi-word tokens in the group they are assigned to
							nGroup = tupleMWE[0]
							nTokenPosInGroup = tupleMWE[1] # 1 = first token in group

							if not nGroup in dictPhrase :
								dictPhrase[nGroup] = [ [], [], strType ]
							
							if len(dictPhrase[nGroup][0]) < nTokenPosInGroup :
								listExtend = [''] * ( nTokenPosInGroup - len(dictPhrase[nGroup][0]) )
								listExtendAddr = [-1] * ( nTokenPosInGroup - len(dictPhrase[nGroup][1]) )
								dictPhrase[nGroup][0].extend( listExtend )
								dictPhrase[nGroup][1].extend( listExtendAddr )

							dictPhrase[nGroup][0][nTokenPosInGroup-1] = strToken
							dictPhrase[nGroup][1][nTokenPosInGroup-1] = nTokenID

		# second pass fill in any group tokens that are missing (as they might have a LEXCAT of '_')
		for nTokenID in dictSentSet[nSentID]['tokens'] :
			# remember original index 0 was removed and became token_id
			strToken = dictSentSet[nSentID]['tokens'][nTokenID][0]

			# SMWE
			tupleMWE = dictSentSet[nSentID]['tokens'][nTokenID][9]

			if tupleMWE != None :
				nGroup = tupleMWE[0]
				nTokenPosInGroup = tupleMWE[1]

				# if group is in phrase list then it matched LEXCAT
				# so add this MWE token to fill in any gaps
				if nGroup in dictPhrase :
					if len(dictPhrase[nGroup][0]) < nTokenPosInGroup :
						listExtend = [''] * ( nTokenPosInGroup - len(dictPhrase[nGroup][0]) )
						listExtendAddr = [-1] * ( nTokenPosInGroup - len(dictPhrase[nGroup][1]) )
						dictPhrase[nGroup][0].extend( listExtend )
						dictPhrase[nGroup][1].extend( listExtendAddr )

					dictPhrase[nGroup][0][nTokenPosInGroup-1] = strToken
					dictPhrase[nGroup][1][nTokenPosInGroup-1] = nTokenID

		# convert the phrase dict so it has the type as the index
		dictTypeIndexedPhrases = {}
		dictTypeIndexedPhrasesAddr = {}
		for nGroup in dictPhrase :
			listPhrase = dictPhrase[nGroup][0]
			listPhraseAddr = dictPhrase[nGroup][1]
			strType = dictPhrase[nGroup][2]

			if not strType in dictTypeIndexedPhrases :
				dictTypeIndexedPhrases[strType] = []
				dictTypeIndexedPhrasesAddr[strType] = []

			dictTypeIndexedPhrases[strType].append( ' '.join( listPhrase ) )
			dictTypeIndexedPhrasesAddr[strType].append( listPhraseAddr )

		# add phrase dict to sent data
		dictSentSet[nSentID]['phrases'] = dictTypeIndexedPhrases
		dictSentSet[nSentID]['phrases_addr'] = dictTypeIndexedPhrasesAddr

	return dictSentSet

def streusle_to_IOB( dict_sent_set = None, max_processes = 1, dict_config = None ) :
	"""
	compute a set of IOB tags for [noun, verb, prep] from a sent set returned by read_streusle()

	:param dict dict_sent_set: dict returned by read_streusle()
	:param int max_processes: max number of processes to use for POS tagging
	:param dict dict_config: config object

	:return: list of sents, each a list of IOB annotated token entries = [ [ ( token, pos, IOB ), ... ], ... ]
	:rtype: list
	"""

	if not isinstance( dict_sent_set, dict ) :
		raise Exception( 'invalid dict_sent_set' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( dict_config, dict ) :
		raise Exception( 'invalid dict_config' )


	# IOB files have a line per token, and newline to indicate a new sentence
	# streusle IOB annotations have classes for noun, verb and prep
	#
	# e.g.
	#
	# I	PRP	B-noun
	# love	VRB	B-verb
	# New	NN	B-noun
	# York	NN	I-noun
	# !	-	O
	#
	# Its	PRP	b-noun
	# lovely	VRB	B-verb
	# 

	# POS tag all sentences (replacing the POS tags which are not stanford POS tags)

	dictSentTokenized = {}
	dictText = {}
	for nSentID in dict_sent_set :
		listTokens = []
		for nTokenID in dict_sent_set[nSentID]['tokens'] :
			strToken = dict_sent_set[nSentID]['tokens'][nTokenID][0]
			listTokens.append( strToken )
		
		# sent id's are strings
		strSentID = str(nSentID)
		dictSentTokenized[ strSentID ] = [ listTokens ]
		dictText[ strSentID ] = dict_sent_set[nSentID]['text']

	# run stanford coreNLP to do tokenize, pos
	# the tokenize is constrained to only split sents at EOL so the input sent count == output sent count
	# also only split using whitespace, so the original streusle tokenization is preserved (and hence the number of tokens remains the same)
	( dictStanfordTokens, dictStanfordPOS ) = soton_corenlppy.re.comp_sem_lib.exec_stanford_corenlp(
		dict_text = dictText,
		work_dir = os.path.abspath( '.' ),
		annotators = 'tokenize,ssplit,pos',
		option_list = ['-tokenizeOptions','americanize=false','-tokenize.whitespace','true','-ssplit.eolonly','true'],
		num_processes = max_processes,
		dict_openie_config = dict_config )

	'''
	# relic NLTK POS tagger use
	dictTaggedSents = soton_corenlppy.common_parse_lib.pos_tag_tokenset_batch( 
						document_token_set = dictSentTokenized,
						lang = 'en',
						dict_common_config = dict_config,
						max_processes = max_processes,
						timeout = 300 )
	'''

	# compute IOB tags
	listType = [ 'noun','verb','prep' ]
	listSentsIOB = []
	strLastClass = None
	listSortedSentID = sorted( list( dict_sent_set.keys() ) )
	for nSentID in listSortedSentID :

		strSentID = str(nSentID)

		dictTypeIndexedPhrasesAddr = dict_sent_set[nSentID]['phrases_addr']

		# stanford POS sent id's are strings
		treeObjPOS = dictStanfordPOS[strSentID]
		if len(dict_sent_set[nSentID]['tokens']) != len(treeObjPOS) :
			raise Exception( 'stanford CoreNLP tokenization != streusle tokenization (review stanford options this should not be possible with -tokenize.whitespace true' )
		listIOB = []

		for nTokenID in dict_sent_set[nSentID]['tokens'] :

			strToken = dict_sent_set[nSentID]['tokens'][nTokenID][0]
			#strPOS = dictTaggedSents[nSentID][0][nTokenID][1]
			strPOS = treeObjPOS[nTokenID].label()

			# look to see if the token address appears in a labelled phrase. if so thats its class
			strClass = None
			for strType in listType :
				if strType in dictTypeIndexedPhrasesAddr :
					for listPhraseAddr in dictTypeIndexedPhrasesAddr[strType] :
						for nAddr in listPhraseAddr :
							if nAddr == nTokenID :
								strClass = strType
								break
						if strClass != None :
							break
				if strClass != None :
					break

			if strClass == None :
				strIOBTag = 'O'
			elif strClass == strLastClass :
				strIOBTag = 'I-' + strClass
			else :
				strIOBTag = 'B-' + strClass

			strLastClass = strClass

			listIOB.append( ( strToken, strPOS, strIOBTag ) )

		# new sent
		listSentsIOB.append( listIOB )

	# all done
	return listSentsIOB

def sentences_to_IOB( sentences_file = None, allowed_id_set = None, tokenize_sents = True, max_processes = 1, dict_config = None ) :
	"""
	read in a sentence file, then do POS tagging and generate a IOB file with IOB tag set to default 'O'.
	if sentence file has no tabs its assumed sent index is the row number.
	if sentence file has tabs its assumed 1st column is sent index, second column is text.

	:param unicode sentences_file: sentences filename to read
	:param list allowed_id_set: list of allowed IDs (None for no filter)
	:param bool tokenize_sents: if True use Treebank to tokenize, otherwise split sent using spaces
	:param int max_processes: max number of processes to use for POS tagging
	:param dict dict_config: config object

	:return: sent_ID's, sent_IOB = list of sent ID's; list of sents, each a list of IOB annotated token entries = [ [ ( token, pos, IOB ), ... ], ... ]
	:rtype: list, list
	"""

	if not isinstance( sentences_file, str ) :
		raise Exception( 'invalid sentences_file' )
	if not isinstance( allowed_id_set, (list,type(None)) ) :
		raise Exception( 'invalid allowed_id_set' )
	if not isinstance( tokenize_sents, bool ) :
		raise Exception( 'invalid tokenize_sents' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( dict_config, dict ) :
		raise Exception( 'invalid dict_config' )

	# read in sentences text

	readHandle = None
	dictSentences = {}

	try :
		readHandle = codecs.open( sentences_file, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		nCount = 0
		for strLine in listLines :

			strLineClean = strLine.strip()
			if len(strLineClean) == 0 :
				continue

			listParts = strLineClean.split('\t')
			if len(listParts) > 1 :
				strSentID = str(listParts[0])
				if (allowed_id_set == None) or (strSentID in allowed_id_set) :
					dictSentences[strSentID] = listParts[1]
			else :
				strSentID = str(nCount)
				if (allowed_id_set == None) or (strSentID in allowed_id_set) :
					dictSentences[strSentID] = listParts[0]

			nCount = nCount + 1

	finally :
		if readHandle != None :
			readHandle.close()

	# tokenization and POS tagging

	dictSentTokenized = {}
	for strSentID in dictSentences :
		strUTF8Text = dictSentences[strSentID]

		if tokenize_sents == True :
			listTokens = soton_corenlppy.common_parse_lib.unigram_tokenize_text( text = strUTF8Text, dict_common_config = dict_config )
		else :
			listTokens = strUTF8Text.split(' ')

		dictSentTokenized[ strSentID ] = [ listTokens ]

	# POS tag document set

	# run stanford coreNLP to do tokenize, pos
	# the tokenize is constrained to only split sents at EOL so the input sent count == output sent count
	# also only split using whitespace, so the original streusle tokenization is preserved (and hence the number of tokens remains the same)
	( dictStanfordTokens, dictStanfordPOS ) = soton_corenlppy.re.comp_sem_lib.exec_stanford_corenlp(
		dict_text = dictSentences,
		work_dir = os.path.abspath( '.' ),
		annotators = 'tokenize,ssplit,pos',
		option_list = ['-tokenizeOptions','americanize=false','-tokenize.whitespace','true','-ssplit.eolonly','true'],
		num_processes = max_processes,
		dict_openie_config = dict_config )

	'''
	# relic NLTK POS tagging
	dictTaggedSents = soton_corenlppy.common_parse_lib.pos_tag_tokenset_batch( 
						document_token_set = dictSentTokenized,
						lang = 'en',
						dict_common_config = dict_config,
						max_processes = max_processes,
						timeout = 300 )
	'''

	# make IOB with 'O' tags
	listSentIOB = []
	listSortedSentID = sorted( list( dictSentences.keys() ) )
	for strSentID in listSortedSentID :
		treeObjPOS = dictStanfordPOS[strSentID]
		listIOB = []

		#for listPOS in dictTaggedSents[nSentIndex][0] :
		#	listIOB.append( ( listPOS[0], listPOS[1], 'O' ) )
		for nToken in range(len(treeObjPOS)) :
			strToken = ' '.join( treeObjPOS[nToken].leaves() )
			strPOS = treeObjPOS[nToken].label()
			listIOB.append( ( strToken, strPOS, 'O' ) )
		listSentIOB.append( listIOB )
	
	# all done
	return listSortedSentID, listSentIOB

