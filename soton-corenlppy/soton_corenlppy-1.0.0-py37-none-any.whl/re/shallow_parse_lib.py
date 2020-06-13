# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
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
//    Created By :    Stuart E. Middleton
//    Created Date :    2019/05/30
//    Created for Project:    LPLP
//
/////////////////////////////////////////////////////////////////////////
//
// Dependencies: None
//
/////////////////////////////////////////////////////////////////////////
"""

import os, sys, logging, traceback, codecs, datetime, copy, time, ast, math, re, random, shutil, json, csv, multiprocessing, subprocess, warnings
import soton_corenlppy
import scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics
from sklearn.metrics import make_scorer
from nltk.util import ngrams

def train_shallow_parse_crf_plus_plus( file_IOB_training_corpus = None, list_IOB_training_corpus = None, training_filename = None, template = None, dict_openie_config = None ) :
	"""
	create a training IOB file from a set of JSON documents and run a chunker (CRF++) to create a model file.
	for CRF++ the IOB training corpus is a token list, with a ('',) tuple terminating a sentence

	:param str file_IOB_training_corpus: training corpus serialized as IOB text file (if None will use list_IOB_training_corpus)
	:param dict list_IOB_training_corpus: training corpus = [ (token,pos,iob_tag), ..., ('',), (token,pos,iob_tag), ... ]. (if None will use file_IOB_training_corpus)
	:param str training_filename: base filename for output files = training IOB (suffix .iob) and training model files (suffix .model)
	:param str template: filename of CRF template
	:param dict dict_openie_config: config object returned from openiepy.openie_lib.get_openie_config() 

	:return: name of model file created
	:rtype: str
	"""

	writeHandle = None
	readHandle = None

	try :
		# check args
		if not isinstance( dict_openie_config, dict ) :
			raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )
		if not isinstance( template, str ) :
			raise Exception('invalid template : ' + repr(template) )
		if not isinstance( training_filename, (str,type(None)) ) :
			raise Exception('invalid training_filename : ' + repr(training_filename) )
		if not isinstance( file_IOB_training_corpus, (str,type(None)) ) :
			raise Exception('invalid file_IOB_training_corpus : ' + repr(file_IOB_training_corpus) )
		if not isinstance( list_IOB_training_corpus, (list,type(None)) ) :
			raise Exception('invalid list_IOB_training_corpus : ' + repr(list_IOB_training_corpus) )

		# serialize POS and IOB labelled text to a single training file
		if list_IOB_training_corpus != None :
			writeHandle = codecs.open( training_filename + '.iob', 'w', 'utf-8', errors = 'replace' )
			for tupleIOB in list_IOB_training_corpus :
				writeHandle.write( '\t'.join( tupleIOB ) + '\n' )
			writeHandle.close()
			strTrainFile = training_filename + '.iob'
		else :
			strTrainFile = file_IOB_training_corpus

		strChunkerTrainingApp = dict_openie_config['crf_learn']
		strCRFTemplate = template
		strModelFile = strTrainFile + '.model'
		strLogFile = strTrainFile + '.model.log'
		strWorkingDir = '.'

		# dont bother processing files of size 0 (i.e. no data in section)
		if os.path.getsize( strTrainFile ) > 0 :

			# train chunker model
			listCMD = [
				strChunkerTrainingApp,
				strCRFTemplate,
				strTrainFile,
				strModelFile
				]

			writeHandle = codecs.open( strLogFile, 'w', 'utf-8', errors = 'replace' )

			p = subprocess.Popen(
				listCMD,
				cwd=strWorkingDir,
				shell=False,
				stdout = writeHandle,
				stderr = writeHandle )
			p.wait()
			if p.returncode < 0 :
				raise Exception( 'chunker failed (train) : code ' + repr( p.returncode ) )

			writeHandle.close()
		
		else :
			raise Exception( 'training file has no data' )

		# return the model file
		return strModelFile

	finally :
		if readHandle != None :
			readHandle.close()
		if writeHandle != None :
			writeHandle.close()

def word2features(sent, i, dict_config = None) :
	"""
	internal word2feature function for a default. called by train_shallow_parse_crf()

	:param list sent: sent = [ (token,pos,...,iob_tag), ... ]
	:param int i: index of token in sent to generate IOB features for
	:param dict dict_context: static context for feature generation (can be None)

	:return: crf feature dict for this token in this sent
	:rtype: dict
	"""

	# match lookahead_tokens to list_lookahead_vocab (in order they appear which is in TF-IDF order so most discriminating first)
	if dict_config != None :
		list_lookahead_vocab = dict_config['list_lookahead_vocab']
		# get all remaining tokens after this one (for lookahead vocabulary features)
		lookahead_tokens = [ tupleIOB[0] for tupleIOB in sent[i+1:] ]
	else :
		list_lookahead_vocab = []
		lookahead_tokens = []

	setLookAheadMatches = set([])
	if len(lookahead_tokens) > 0 :
		listPhrases = list( ngrams( lookahead_tokens, 2 ) )
		listPhrases.extend( lookahead_tokens )
		for tuplePhrase in listPhrases :
			strPhrase = ' '.join( tuplePhrase )
			strPhrase = strPhrase.lower()
			if strPhrase in list_lookahead_vocab :
				setLookAheadMatches.add( strPhrase )
	listLookAheadMatches = list( setLookAheadMatches )

	nFirstN = 5
	if len(listLookAheadMatches) > nFirstN :
		listLookAheadMatches = listLookAheadMatches[:nFirstN]
	else :
		for nExtra in range( nFirstN - len(listLookAheadMatches) ) :
			listLookAheadMatches.append( '' )

	features = {}

	for nPos in range(-3,4) :
		if (nPos + i >= 0) and (nPos + i < len(sent)) :
			token = sent[nPos + i][0]
			pos = sent[nPos + i][1]

			if len(token) < 4 :
				strLength = 'short'
			elif len(token) < 7 :
				strLength = 'normal'
			else :
				strLength = 'long'

			features[ 'word' + str(nPos) ] = token.lower()
			features[ 'pos' + str(nPos) ] = pos.lower()
			features[ 'digit' + str(nPos) ] = token.isdigit()
			features[ 'lower' + str(nPos) ] = token.islower()
			features[ 'upper' + str(nPos) ] = token.isupper()
			features[ 'title' + str(nPos) ] = token.istitle()
			features[ 'space' + str(nPos) ] = token.isspace()

			features[ 'length' + str(nPos) ] = strLength

			if nPos + i == 0 :
				features[ 'BOS' + str(nPos) ] = 'True'
			else :
				features[ 'BOS' + str(nPos) ] = 'False'

			if nPos + i == len(sent)-1 :
				features[ 'EOS' + str(nPos) ] = 'True'
			else :
				features[ 'EOS' + str(nPos) ] = 'False'
	
	# add look ahead matches (
	for nIndex in range(len(listLookAheadMatches)) :
		strPhrase = listLookAheadMatches[ nIndex ]
		features[ 'ahead' + str(nIndex) ] = strPhrase.replace(' ','_')

	return features

def train_shallow_parse_crf( list_IOB_training_corpus = None, word2features = word2features, word2featuresConfig = None, n_jobs = -1, log_eval = True, params_space = { 'c1': [0, 0.1, 1.0], 'c2': [0, 0.1, 1.0] }, num_folds = 3, all_possible_transitions  = True, dict_openie_config = None ) :
	"""
	train a scikit learn CRF model using an IOB training corpus.
	for scikit learn CRF the IOB corpus is a list of sentences, each sentence is a list of tokens (phrase, POS, ... other features, IOB tag).
	CRF trained model is returned as an object to allow efficient in-memory running (unlike CRF++ version of this function that serializes IOB training corpus and runs an EXE to classify).
	model params are optimised using sklearn.model_selection.GridSearchCV

	:param list list_IOB_training_corpus: training corpus = [ [ (token,pos,...,iob_tag), ... ], ... ]
	:param function word2features: function pointer to word2features(sent, i, dict_config) which will be called to generate a feature dict for each word in an IOB sentence.
	:param dict word2featuresConfig: dict of config for word2features(), can be None if not needed.
	:param int n_jobs: number of jobs to spawn for random param search (optimising CRF model training) (-1 uses all available processors)
	:param bool log_eval: if True eval data will be logged. if False micro_f1 is None
	:param bool all_possible_transitions: if True negative transitions will be considered, generating L**2 transitions from L. will improve accuracy but be very slow to compute for larger datasets.
	:param dict params_space: param space for GridSearchCV (default gives a basic search with 9 conbinations of c1 and c2 params total)
	:param int num_folds: number of folds for GridSearchCV
	:param dict dict_openie_config: config object returned from openiepy.openie_lib.get_openie_config() 

	:return: CRF model object trained, float
	:rtype: sklearn_crfsuite.CRF, macro_F1
	"""

	# input IOB corpus = list of sents, each a list of IOB tuples
	# e.g. [ [('Melbourne', 'NP', 'B-LOC'), ('(', 'Fpa', 'O'), ('Australia', 'NP', 'B-LOC'), (')', 'Fpt', 'O'), (',', 'Fc', 'O'), ('25', 'Z', 'O'), ('may', 'NC', 'O'), ('(', 'Fpa', 'O'), ('EFE', 'NC', 'B-ORG'), (')', 'Fpt', 'O'), ('.', 'Fp', 'O')], ... ]

	# check args
	if not isinstance( dict_openie_config, dict ) :
		raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )
	if not isinstance( word2features, type(train_shallow_parse_crf) ) :
		raise Exception('invalid word2features : ' + repr(word2features) )
	if not isinstance( word2featuresConfig, (dict,type(None)) ) :
		raise Exception('invalid word2features : ' + repr(word2featuresConfig) )
	if not isinstance( n_jobs, int ) :
		raise Exception('invalid n_jobs : ' + repr(n_jobs) )
	if not isinstance( list_IOB_training_corpus, list ) :
		raise Exception('invalid list_IOB_training_corpus : ' + repr(list_IOB_training_corpus) )
	if not isinstance( params_space, dict ) :
		raise Exception('invalid params_space : ' + repr(params_space) )
	if not isinstance( num_folds, int ) :
		raise Exception('invalid num_folds : ' + repr(num_folds) )
	if not isinstance( log_eval, bool ) :
		raise Exception('invalid log_eval : ' + repr(log_eval) )
	if not isinstance( all_possible_transitions, bool ) :
		raise Exception('invalid all_possible_transitions : ' + repr(all_possible_transitions) )

	def sent2features(sent):
		return [word2features(sent, i, word2featuresConfig) for i in range(len(sent))]

	def sent2labels(sent):
		return [list_IOB_tuples[-1] for list_IOB_tuples in sent]

	# prepare the test and training set
	X_train = [sent2features(s) for s in list_IOB_training_corpus]
	y_train = [sent2labels(s) for s in list_IOB_training_corpus]

	# get labels (cannot get from model yet as its not trained, so get from training data directly)
	labels = [ label for s in y_train for label in s ]
	labels = list( set( labels ) )
	labels.remove('O')

	# surpress all warnings (otherwise we get loads of FutureWarnings)
	if not sys.warnoptions:
		warnings.simplefilter("ignore")
		os.environ["PYTHONWARNINGS"] = "ignore" # Also affect subprocesses (important as GridSearchCV will spawn a lot)

	if num_folds > 1 :
		# do a grid search to discover best parameters for CRF model
		# define attributes we want to search on here, since GridSearchCV will dynamically look them up and throw warnings if they are missing
		crf = sklearn_crfsuite.CRF(
			algorithm='lbfgs',
			all_possible_transitions=all_possible_transitions,
		)

		f1_scorer = make_scorer( sklearn_crfsuite.metrics.flat_f1_score, average='macro', labels=labels, zero_division = 0 )

		dict_openie_config['logger'].info( 'training CRF model using a GridSearchCV of param space' )
		
		rs = sklearn.model_selection.GridSearchCV(
								estimator=crf,
								param_grid=params_space, 
								cv=num_folds, 
								verbose=1, 
								n_jobs=n_jobs,
								scoring=f1_scorer )

		rs.fit( X_train, y_train )

		# output the results
		macro_F1 = None
		if log_eval == True :
			dict_openie_config['logger'].info( 'best params: {}'.format( rs.best_params_ ) )
			dict_openie_config['logger'].info( 'best macro F1 score = {}'.format( rs.best_score_ ) )
			dict_openie_config['logger'].info( 'model size: {:0.2f}M'.format( rs.best_estimator_.size_ / 1000000 ) )
			macro_F1 = rs.best_score_

		# return the best CRF model
		crf = rs.best_estimator_
	else :
		# just train model with params given (using first combination in set)
		dictParams = {}
		for strParam in params_space :
			dictParams[strParam] = params_space[strParam][0]

		crf = sklearn_crfsuite.CRF(
			algorithm='lbfgs',
			all_possible_transitions=all_possible_transitions,
			**dictParams
		)
		crf.fit( X_train, y_train )
		macro_F1 = None

	return crf, macro_F1

def shallow_parse_crf_plus_plus( file_IOB_test_corpus = None, list_IOB_test_corpus = None, test_filename = None, model_file = None, template = None, dict_openie_config = None ) :
	"""
	run a trained CRF++ chunker on a set of test JSON files

	:param str file_IOB_test_corpus: test corpus serialized as IOB text file (if None will use list_IOB_test_corpus)
	:param dict list_IOB_test_corpus: test corpus = [ (token,pos,iob_tag), ..., ('',), (token,pos,iob_tag), ... ]. (if None will use file_IOB_test_corpus)
	:param str test_filename: base filename for output files = test IOB (suffix .iob) and classified IOB (suffix .iob.chunked)
	:param str model_file: model filename trained using train_shallow_parse_crf()
	:param str template: filename of CRF template
	:param dict dict_openie_config: config object returned from openiepy.openie_lib.get_openie_config() 

	:return: name of chunked file created
	:rtype: str
	"""

	writeHandle = None
	readHandle = None
	writeHandleEval = None

	try :
		# check args
		if not isinstance( dict_openie_config, dict ) :
			raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )
		if not isinstance( dict_openie_config, dict ) :
			raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )
		if not isinstance( template, str ) :
			raise Exception('invalid template : ' + repr(template) )
		if not isinstance( test_filename, (str,type(None)) ) :
			raise Exception('invalid test_filename : ' + repr(test_filename) )
		if not isinstance( model_file, str ) :
			raise Exception('invalid model_file : ' + repr(model_file) )
		if not isinstance( list_IOB_test_corpus, (list,type(None)) ) :
			raise Exception('invalid list_IOB_test_corpus : ' + repr(list_IOB_test_corpus) )
		if not isinstance( file_IOB_test_corpus, (str,type(None)) ) :
			raise Exception('invalid file_IOB_test_corpus : ' + repr(file_IOB_test_corpus) )

		# serialize POS (and IOB optionally for eval purposes) labelled text to a single training file
		if list_IOB_test_corpus != None :
			strTestFile = test_filename + '.iob'
			writeHandle = codecs.open( strTestFile, 'w', 'utf-8', errors = 'replace' )
			for tupleIOB in list_IOB_test_corpus :
				writeHandle.write( '\t'.join( tupleIOB ) + '\n' )
			writeHandle.close()
		else :
			strTestFile = file_IOB_test_corpus

		strChunkerTestApp = dict_openie_config['crf_test']
		strCRFTemplate = template
		strWorkingDir = '.'

		# run chunker with model on test data to label it
		if os.path.getsize( strTestFile ) > 0 :
			listCMD = [
				strChunkerTestApp,
				'-m',
				model_file,
				strTestFile
				]

			writeHandle = codecs.open( strTestFile + '.chunked', 'w', 'utf-8', errors = 'replace' )

			p = subprocess.Popen(
				listCMD,
				cwd=strWorkingDir,
				shell=False,
				stdout = writeHandle )
			p.wait()
			if p.returncode < 0 :
				raise Exception( 'chunker failed (test) : code ' + repr( p.returncode ) )

			writeHandle.close()

		else :
			raise Exception( 'test file has no data' )
		
		return strTestFile + '.chunked'

	finally :
		if readHandle != None :
			readHandle.close()
		if writeHandle != None :
			writeHandle.close()

def shallow_parse_crf( list_IOB_test_corpus = None, crf_model = None, word2features = word2features, word2featuresConfig = None, log_eval = True, dict_openie_config = None ) :
	"""
	run a trained scikit learn CRF model on a test IOB corpus
	for scikit learn CRF the IOB corpus is a list of sentences, each sentence is a list of tokens (phrase, POS, IOB tag).
	if this is unlabelled test data IOB tag should be 'O'

	:param list list_IOB_test_corpus: test corpus = [ [ (token,pos,iob_tag), ... ], ... ]
	:param sklearn_crfsuite.CRF crf_model: CRF model from train_shallow_parse_crf()
	:param function word2features: function pointer to word2features(sent, i) which will be called to generate a feature dict for each word in an IOB sentence.
	:param dict word2featuresConfig: dict of config for word2features(), can be None if not needed.
	:param bool log_eval: if True eval data will be logged (assuming IOB test corpus has gold tags provided). If False then returned macro_F1 + macro_scores are None
	:param dict dict_openie_config: config object returned from openiepy.openie_lib.get_openie_config() 

	:return: list of labelled sentences, each a list of the predicted IOB labels (one for each token in test IOB corpus) e.g. [ ['B-LOC', 'I-LOC', 'O', ... ], ...] + macro_F1 + macro_scores
	:rtype: list, float, dict
	"""

	# input IOB corpus = list of sents, each a list of IOB tuples
	# e.g. [ [('Melbourne', 'NP', 'B-LOC'), ('(', 'Fpa', 'O'), ('Australia', 'NP', 'B-LOC'), (')', 'Fpt', 'O'), (',', 'Fc', 'O'), ('25', 'Z', 'O'), ('may', 'NC', 'O'), ('(', 'Fpa', 'O'), ('EFE', 'NC', 'B-ORG'), (')', 'Fpt', 'O'), ('.', 'Fp', 'O')], ... ]

	# check args
	if not isinstance( dict_openie_config, dict ) :
		raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )
	if not isinstance( word2features, type(shallow_parse_crf) ) :
		raise Exception('invalid word2features : ' + repr(word2features) )
	if not isinstance( word2featuresConfig, (dict,type(None)) ) :
		raise Exception('invalid word2features : ' + repr(word2featuresConfig) )
	if not isinstance( crf_model, sklearn_crfsuite.CRF ) :
		raise Exception('invalid crf_model : ' + repr(crf_model) )
	if not isinstance( log_eval, bool ) :
		raise Exception('invalid log_eval : ' + repr(log_eval) )
	if not isinstance( list_IOB_test_corpus, list ) :
		raise Exception('invalid list_IOB_test_corpus : ' + repr(list_IOB_test_corpus) )

	def sent2features(sent):
		return [word2features(sent, i, word2featuresConfig) for i in range(len(sent))]

	def sent2labels(sent):
		return [list_IOB_tuples[-1] for list_IOB_tuples in sent]

	# prepare the test set
	X_test = [sent2features(s) for s in list_IOB_test_corpus]
	y_test = [sent2labels(s) for s in list_IOB_test_corpus]

	# run model
	y_pred = crf_model.predict(X_test)

	# eval result (only useful if gold label is provided with testset, otherwise F1 will always be 0.0)
	macro_scores = None
	macro_F1 = None
	if log_eval == True :
		labels = list( crf_model.classes_ )
		labels.remove('O')
		if len(labels) > 0 :
			macro_F1 = sklearn_crfsuite.metrics.flat_f1_score( y_test, y_pred, average='macro', labels=labels, zero_division = 0 )

			# compute the macro F1 score (F1 for instances of each label class averaged) in the test set
			if macro_F1 != 0.0 :
				sorted_labels = sorted(
					labels, 
					key=lambda name: (name[1:], name[0])
				)
				macro_scores = sklearn_crfsuite.metrics.flat_classification_report( y_test, y_pred, labels=sorted_labels, digits=3, output_dict = True )

	# return the predictions
	return y_pred, macro_F1, macro_scores

def label_sents_from_chunked_file( chunk_file = None, chunked_index = 3, gold_index = 2, dict_openie_config = None ) :
	"""
	load IOB chunked file and return a JSON structure with labelled sentences
	BILOU:
		B - 'beginning'
		I - 'inside'
		L - 'last'
		O - 'outside'
		U - 'unit' (singular occurance)

	:param str chunk_file: chunk file to load
	:param int chunked_index: index in IOB tuple with the chunked label. can be None.
	:param int gold_index: index in IOB tuple with the gold truth label (IOB prediction is always at end of tuple). can be None.
	:param dict dict_openie_config: config object

	:return: dict of sent labels = { sent_index : { 'sent' : '...', 'pos' : '...', 'chunk-labels' : [...], 'gold-labels' : [...] } }
	:rtype: dict
	"""

	readHandle = None

	try :
		# check args
		if not isinstance( chunk_file, str ) :
			raise Exception('invalid chunk_file : ' + repr(chunk_file) )
		if not isinstance( chunked_index, (int,type(None)) ) :
			raise Exception('invalid chunked_index : ' + repr(chunked_index) )
		if not isinstance( gold_index, (int,type(None)) ) :
			raise Exception('invalid gold_index : ' + repr(gold_index) )
		if not isinstance( dict_openie_config, dict ) :
			raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )

		dictLabelledSents = {}
		nSentIndex = 0
		listTokens = []
		listPOS = []
		setLabelsChunk = set([])
		setLabelsGold = set([])

		readHandle = codecs.open( chunk_file, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		for strLine in listLines :
			strLineClean = strLine.strip()

			if len(strLineClean) > 0 :
				listParts = strLineClean.split('\t')
				if len(listParts) < 4 :
					raise Exception('chunked file row does not have at least 4 parts : ' + chunk_file )

				strToken = listParts[0]
				strPOS = listParts[1]

				listTokens.append( strToken )
				listPOS.append( strPOS )

				# note any label except O (removing the IOB position marker prefix)
				if chunked_index != None :
					strIOBChunker = listParts[chunked_index]
					if len(strIOBChunker) > 1 :
						if strIOBChunker[:2] in ['B-', 'I-', 'L-', 'U-'] :
							strLabel = strIOBChunker[2:]
							setLabelsChunk.add( strLabel )

				if gold_index != None :
					strIOBGold = listParts[gold_index]
					# note any label except O (removing the IOB position marker prefix)
					if len(strIOBGold) > 1 :
						if strIOBGold[:2] in ['B-', 'I-', 'L-', 'U-'] :
							strLabel = strIOBGold[2:]
							setLabelsGold.add( strLabel )

			else :
				# add sent to dict
				dictLabelledSents[nSentIndex] = { 'sent' : ' '.join(listTokens), 'pos' : ' '.join(listPOS) }

				if chunked_index != None :
					dictLabelledSents[nSentIndex]['chunk-labels'] = setLabelsChunk

				if gold_index != None :
					dictLabelledSents[nSentIndex]['gold-labels'] = setLabelsGold

				# empty row is an end of sent marker
				nSentIndex += 1
				listTokens = []
				listPOS = []
				setLabelsChunk = set([])
				setLabelsGold = set([])

		# all done
		return dictLabelledSents

	finally :
		if readHandle != None :
			readHandle.close()

def label_sents_from_chunked( list_IOB_corpus = None, chunked_index = 3, gold_index = 2, dict_openie_config = None ) :
	"""
	process a IOB corpus chunked and return a JSON structure with labelled sentences

	BILOU:
		B - 'beginning'
		I - 'inside'
		L - 'last'
		O - 'outside'
		U - 'unit' (singular occurance)

	:param list list_IOB_corpus: corpus = [ [ (token,pos,...,iob_tag), ... ], ... ]
	:param int chunked_index: index of predicted IOB label. can be None.
	:param int gold_index: index of gold IOB label. can be None.
	:param dict dict_openie_config: config object

	:return: dict of sent labels = { sent_index : { 'sent' : '...', 'pos' : '...', 'chunk-labels' : [...], 'gold-labels' : [...] } }
	:rtype: dict
	"""

	# input IOB corpus = list of sents, each a list of IOB tuples (usually chunked label at end)
	# e.g. [ [('Melbourne', 'NP', 'B-LOC'), ('(', 'Fpa', 'O'), ('Australia', 'NP', 'B-LOC'), (')', 'Fpt', 'O'), (',', 'Fc', 'O'), ('25', 'Z', 'O'), ('may', 'NC', 'O'), ('(', 'Fpa', 'O'), ('EFE', 'NC', 'B-ORG'), (')', 'Fpt', 'O'), ('.', 'Fp', 'O')], ... ]

	# check args
	if not isinstance( list_IOB_corpus, list ) :
		raise Exception('invalid list_IOB_corpus : ' + repr(list_IOB_corpus) )
	if not isinstance( chunked_index, (int,type(None)) ) :
		raise Exception('invalid chunked_index : ' + repr(chunked_index) )
	if not isinstance( gold_index, (int,type(None)) ) :
		raise Exception('invalid gold_index : ' + repr(gold_index) )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )

	dictLabelledSents = {}
	nSentIndex = 0
	listTokens = []
	listPOS = []
	setLabelsChunk = set([])
	setLabelsGold = set([])

	for listSent in list_IOB_corpus :
		for tupleIOB in listSent :
			strToken = tupleIOB[0]
			strPOS = tupleIOB[1]

			listTokens.append( strToken )
			listPOS.append( strPOS )

			# note any label except O (removing the IOB position marker prefix)
			if chunked_index != None :
				strIOBChunker = tupleIOB[chunked_index]
				if len(strIOBChunker) > 1 :
					if strIOBChunker[:2] in ['B-', 'I-', 'L-', 'U-'] :
						strLabel = strIOBChunker[2:]
						setLabelsChunk.add( strLabel )

			if gold_index != None :
				strIOBGold = tupleIOB[gold_index]
				# note any label except O (removing the IOB position marker prefix)
				if len(strIOBGold) > 1 :
					if strIOBGold[:2] in ['B-', 'I-', 'L-', 'U-'] :
						strLabel = strIOBGold[2:]
						setLabelsGold.add( strLabel )

		# add sent to dict
		dictLabelledSents[nSentIndex] = { 'sent' : ' '.join(listTokens), 'pos' : ' '.join(listPOS) }

		if chunked_index != None :
			dictLabelledSents[nSentIndex]['chunk-labels'] = setLabelsChunk

		if gold_index != None :
			dictLabelledSents[nSentIndex]['gold-labels'] = setLabelsGold

		# empty row is an end of sent marker
		nSentIndex += 1
		listTokens = []
		listPOS = []
		setLabelsChunk = set([])
		setLabelsGold = set([])

	# all done
	return dictLabelledSents


def eval_shallow_parse( file_to_score = None, dict_scores = None, gold_index = 2, dict_openie_config = None ) :
	"""
	load chunked file and score it

	:param str file_to_score: file to load and score
	:param dict dict_scores: dict where scores will be recorded
	:param int gold_index: index in IOB tuple with the gold truth label (IOB prediction is always at end of tuple)
	:param dict dict_openie_config: config object
	"""

	readHandle = None

	try :
		# check args
		if not isinstance( file_to_score, str ) :
			raise Exception('invalid file_to_score : ' + repr(file_to_score) )
		if not isinstance( dict_scores, dict ) :
			raise Exception('invalid dict_scores : ' + repr(dict_scores) )
		if not isinstance( gold_index, int ) :
			raise Exception('invalid gold_index : ' + repr(gold_index) )
		if not isinstance( dict_openie_config, dict ) :
			raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )

		readHandle = codecs.open( file_to_score, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		if not 'fn_all' in dict_scores :
			dict_scores['fn_all'] = 0
		if not 'tn_all' in dict_scores :
			dict_scores['tn_all'] = 0
		if not 'tp_all' in dict_scores :
			dict_scores['tp_all'] = 0
		if not 'fp_all' in dict_scores :
			dict_scores['fp_all'] = 0

		for strLine in listLines :
			strLineClean = strLine.strip()
			if len(strLineClean) > 0 :
				listParts = strLineClean.split('\t')
				if len(listParts) < 4 :
					raise Exception('chunked file row does not have at least 4 parts : ' + file_to_score )
				
				strToken = listParts[0]
				strPOS = listParts[1]
				strIOBGold = listParts[gold_index]
				strIOBChunker = listParts[-1]

				if (strIOBChunker == 'O') and (strIOBGold != 'O') :
					dict_scores[ 'fn_all' ] = dict_scores[ 'fn_all' ] + 1

					strTag = 'fn_' + strIOBGold
					if not strTag in dict_scores :
						dict_scores[ strTag ] = 0
					dict_scores[ strTag ] = dict_scores[ strTag ] + 1

				elif (strIOBChunker == 'O') and (strIOBGold == 'O') :
					dict_scores[ 'tn_all' ] = dict_scores[ 'tn_all' ] + 1

				elif (strIOBChunker != 'O') and (strIOBGold == strIOBChunker) :
					dict_scores[ 'tp_all' ] = dict_scores[ 'tp_all' ] + 1

					strTag = 'tp_' + strIOBGold
					if not strTag in dict_scores :
						dict_scores[ strTag ] = 0
					dict_scores[ strTag ] = dict_scores[ strTag ] + 1

				elif (strIOBChunker != 'O') and (strIOBGold != strIOBChunker) :
					dict_scores[ 'fp_all' ] = dict_scores[ 'fp_all' ] + 1

					strTag = 'fp_' + strIOBChunker
					if not strTag in dict_scores :
						dict_scores[ strTag ] = 0
					dict_scores[ strTag ] = dict_scores[ strTag ] + 1

				else :
					raise Exception( 'code error, should be impossible : ' + repr( (strIOBChunker,strIOBGold) ) )

	finally :
		if readHandle != None :
			readHandle.close()

def eval_chunked_sents( dict_labelled_sents = None, dict_openie_config = None ) :
	"""
	score a set of labelled sents created using label_sents_from_chunked()

	:param dict dict_labelled_sents: sent labels created using label_sents_from_chunked()
	:param dict dict_openie_config: config object

	:return: dict of scores = { 'macro-averaged' : ..., 'micro-averaged' : ... }
	:rtype: dict
	"""

	# check args
	if not isinstance( dict_labelled_sents, dict ) :
		raise Exception('invalid dict_labelled_sents : ' + repr(dict_labelled_sents) )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception('invalid dict_openie_config : ' + repr(dict_openie_config) )

	# input expected
	# dict_labelled_sents = { sent_id : { 'sent' : ..., 'pos' : ..., 'chunk-labels' : [...], 'gold-labels' : [...] } }
	# labels should be sorted in confidence order (or left random if no confidence available)

	# metrics
	# (1) P@K and R@K macro-averaged
	#     P@K = ( 1 / num_docs ) * sum_for_all_docs( num correct labels in top K / K )
	#     R@K = ( 1 / num_docs ) * sum_for_all_docs( num correct labels in top K / num gold labels )
	#     ==> penalizes documents with fewer labels than K
	# (2) micro-averaged F1 (computed for both all labels and per label)
	#     P = TP/(TP+FP) = correct / ( correct + incorrect )
	#     R = TP/(TP+FN) = correct / ( correct + missing_gold_truth )
	#     F1 = 2 * P * R / ( P + R )
	# (3) nDCG@K macro-averaged
	#     nDCG@K = ( 1 / num_docs ) * sum_for_all_docs( sum_over_1..K( ( ( 2 ** num correct labels in top k ) - 1 ) / log( 1 + k ) ) )
	# (4) RP@K macro-averaged
	#     RP@K = ( 1 / num_docs ) * sum_for_all_docs( num correct labels in top K / min( K, num gold labels ) )
	#
	# doc = sentence for the problem of sentence classification


	# see paper Ilias Chalkidis, Manos Fergadiotis, Prodromos Malakasiotis, Ion Androutsopoulos:Large-Scale Multi-Label Text Classification on EU Legislation. ACL (1) 2019: 6314-6322
	# https://www.aclweb.org/anthology/P19-1636.pdf
	# all metrcis clearly defined and pro/con explained for each of them

	dictScores = { 'macro-averaged' : {}, 'micro-averaged' : {} }

	# P@K and R@K
	for K in range(1,11) :
		nDocs = len(dict_labelled_sents)
		nSum = [0.0, 0.0, 0.0, 0.0]
		for nSentIndex in dict_labelled_sents :
			listChunkLabels = dict_labelled_sents[nSentIndex]['chunk-labels']
			listGoldLabels = dict_labelled_sents[nSentIndex]['gold-labels']

			nCorrect = 0
			for k in range(1,K+1) :
				if len(listChunkLabels) > k-1 :
					if listChunkLabels[k-1] in listGoldLabels :
						nCorrect += 1

			nDCG = 0.0
			for k in range(1,K+1) :
				nCount2 = 0
				for k2 in range(1,k+1) :
					if len(listChunkLabels) > k2-1 :
						if listChunkLabels[k2-1] in listGoldLabels :
							nCount2 += 1
				nDCG += ( ( 2**nCount2 ) - 1 ) / math.log( 1+k )

			# P
			nSum[0] += nCorrect / (1.0 * K)

			# R
			if len(listGoldLabels) > 0 :
				nSum[1] += nCorrect / (1.0 * len(listGoldLabels))
			else :
				nSum[1] += 0

			# RP
			nVal = min( len(listGoldLabels), K )
			if nVal > 0 :
				nSum[2] += nCorrect / (1.0 * nVal)
			else :
				nSum[2] += 0

			# nDCG
			nSum[3] += nDCG

		if nDocs > 0 :
			nP_at_K = nSum[0] * (1.0 / nDocs)
		else :
			nP_at_K = 0.0

		if nDocs > 0 :
			nR_at_K = nSum[1] * (1.0 / nDocs)
		else :
			nR_at_K = 0.0

		if nDocs > 0 :
			nRP_at_K = nSum[2] * (1.0 / nDocs)
		else :
			nRP_at_K = 0.0

		if nDocs > 0 :
			nDCG_at_K = nSum[3] * (1.0 / nDocs)
		else :
			nDCG_at_K = 0.0

		dictScores['macro-averaged'][K] = { 'P@K' : nP_at_K, 'R@K' : nR_at_K, 'RP@K' : nRP_at_K, 'nDCP@K' : nDCG_at_K }

	# make a set of all possible labels
	setLabels = set([])
	for nSentIndex in dict_labelled_sents :
		listChunkLabels = dict_labelled_sents[nSentIndex]['chunk-labels']
		listGoldLabels = dict_labelled_sents[nSentIndex]['gold-labels']

		setLabels = setLabels.union( set(listChunkLabels) )
		setLabels = setLabels.union( set(listGoldLabels) )

	setLabels.add('ALL')

	# compute micro-averaged P/R/F1 for labels (and all labels)
	for strLabelTarget in setLabels :
		nTP = 0
		nFP = 0
		nFN = 0

		for nSentIndex in dict_labelled_sents :
			listChunkLabels = dict_labelled_sents[nSentIndex]['chunk-labels']
			listGoldLabels = dict_labelled_sents[nSentIndex]['gold-labels']

			# filter labels based on target
			if strLabelTarget != 'ALL' :
				if strLabelTarget in listChunkLabels :
					listChunkLabels = [ strLabelTarget ]
				else :
					listChunkLabels = []
				if strLabelTarget in listGoldLabels :
					listGoldLabels = [ strLabelTarget ]
				else :
					listGoldLabels = []

			# calc TP, FP, FN
			for strLabel in listChunkLabels :
				if strLabel in listGoldLabels :
					nTP += 1
				else :
					nFP += 1

			for strLabel in listGoldLabels :
				if not strLabel in listChunkLabels :
					nFN += 1

		# calc F1
		if nTP + nFP > 0 :
			nP = nTP / (1.0 * ( nTP + nFP ) )
		else :
			nP = 0.0

		if nTP + nFN > 0 :
			nR = nTP / (1.0 * ( nTP + nFN ) )
		else :
			nR = 0.0

		if nP + nR > 0 :
			nF1 = 2.0 * nP * nR / ( 1.0 * ( nP + nR ) )
		else :
			nF1 = 0.0

		dictScores['micro-averaged'][strLabelTarget] = { 'P' : nP, 'R' : nR, 'F1' : nF1 }

	# all done
	return dictScores
