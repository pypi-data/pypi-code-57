# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	/////////////////////////////////////////////////////////////////////////
	//
	// (c) Copyright University of Southampton IT Innovation, 2017
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
	// Created Date : 2016/08/12
	// Created for Project: GRAVITATE
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies: None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

Compositional semantics library

"""

import array,sys,codecs,os,re,copy,math,multiprocessing,threading,queue,traceback,logging,time,tempfile,subprocess,datetime,signal
import nltk.corpus, bs4
from nltk.parse import stanford
import soton_corenlppy
from soton_corenlppy.re import openie_lib

import warnings
warnings.simplefilter( 'ignore', UserWarning )

# global process handle for dep_parse. as we are using multiprocessing to run exec_dep_parse() we know only one thread is using p_global at a time
p_global = None

#
# StanfordDependancyParser and StanfordPOSTagger have a GPL license (OK if its installed as a standalone product)
# note: need NLTK 3.2.4 NOT 3.2.2 as older version had a UTF-8 bug with StanfordDependancyParser
# https://nlp.stanford.edu/software/lex-parser.shtml
# https://nlp.stanford.edu/software/tagger.shtml
# Dependancy = https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/parser/lexparser/LexicalizedParser.html
# POS Tagger = https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/tagger/maxent/MaxentTagger.html
# Tokenizer = https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/process/PTBTokenizer.html
# USD dependancy tags = http://nlp.stanford.edu/pubs/USD_LREC14_paper_camera_ready.pdf
#                     = http://universaldependencies.org/u/dep/index.html
# upenn POS tags = https://www.eecis.udel.edu/~vijay/cis889/ie/pos-set.pdf
#                = https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# POS to USD mappings = http://universaldependencies.org/tagset-conversion/en-penn-uposf.html
# stanford parser 2016 oct outputs USD v1.0 (PDF is v1.0, online is v2.0)
# 

# regex for parsing open template variables (lex/pos terms escaped so no {}). note use ; to delimit pos and lex as : is a POS tag
# e.g. {arg1_12:S:pos=NN;lex=}
#      {rel1_13:-:pos=VBN|VBZ;lex=hello|world}
regexVariableOpenTemplate = re.compile( r'\A\{(?P<TYPE>[a-zA-z]+)(?P<INDEX>[0-9]+)_(?P<SEEDTOKEN>[0-9]+)\:(?P<POS_MARK>[\-SE])\:(pos\=(?P<POS>[^;\}]+)){0,1}[;]?(lex\=(?P<LEX>[^\}]+)){0,1}\}\Z', re.IGNORECASE | re.UNICODE )

# regex for parsing immediate child move. note use ; to delimit pos and lex as : is a POS tag
# e.g. @nmod,rel1:pos=VBN|VBZ;lex=going|went,rel@
# e.g. @compound:prt,arg3:pos=DT;lex=a,arg@
regexEncodedExtractionImmediateChild = re.compile( r'\A\@(?P<DEP_TYPE>[a-zA-z:]+)\,(?P<VAR_BASE>[a-zA-z0-9]+)\:(pos\=(?P<POS>[^;]+)){0,1}[;]?(lex\=(?P<LEX>[^\}]+)){0,1}\,(?P<VAR_TYPE>[a-zA-z]+)\@\Z', re.IGNORECASE | re.UNICODE )

# regex for parsing encoded extraction variables (tokens escaped so no {})
regexEncodedExtraction = re.compile( r'\A\{(?P<VAR>[a-zA-z0-9]+) (?P<HEAD>\[head\=[^\]]+\] ){0,1}(?P<ADDR>\[addr\=[^\]]+\] ){0,1}(?P<PATTERN_INDEX>\[pindex\=[^\]]+\] ){0,1}(?P<CONNECTION>\[([a-zA-z:]+\>[a-zA-z0-9\>]+;){1,20}\] ){0,1}(?P<PHRASE>[^\}]+)\}\Z', re.IGNORECASE | re.UNICODE )

# default negation assertion vocabulary
dict_assertion_true = {
	'en' : [ 'true', 'genuine', 'real', 'confirmed', 'verified' ]
	}
dict_assertion_false = {
	'en' : [ 'false', 'fake', 'hoax', 'joke', 'trick', 'debunked' ]
	}

# pretty print allowing informative dependencies to allow simple lexicon matching
dict_pretty_print_var_dep_rels_default = {
	'any' : ['compound', 'amod', 'nummod', 'advmod', 'cop', 'appos', 'dep', 'conj', 'nmod', 'xcomp'],
	'before_head' :  [],
	'after_head' : ['case', 'case:of', 'case:by']
}

# set of prefixes to prevent appearing in a proposition set. default is based on a stoplist for {arg,rel,arg} proposition pattern
# case specific - we do not add 'In ...' to the stoplist for example, as its OK when a preposition starts a sentence. we want to prevent truncated forms.
dict_index_stoplist_prefix_default = {
	0 : ['and ','or ', 'of ', 'to ', 'in ', 'into ', 'for ', 'at ', "'s ", 'by ', 'on ', 'him '],
	1 : ['and ','or '],
	2 : ['and ','or ']
}
dict_index_stoplist_suffix_default = {
	0 : [' and',' or'],
	1 : [' and',' or'],
	2 : [' and',' or', ' those', ' he', ' she', ' they', ' the', ' a', ' would'],
}

# defaults for proposition extraction
list_proposition_pattern_default = [ 'arg', 'rel', 'arg' ]
dict_displaced_context_default = {
	'arg' : [],
	'rel' : [
		# for minimal rel set displace everything
		# except ccomp (which is important for rel meaning - so we collapse it rel later)
		# core dependents of clausal predicates
		'nsubj','nsubjpass','dobj','iobj','csubj','csubjpass','xcomp',

		# non-core dependents of clausal predicates
		# 'nmod', 'nmod:*', 'advcl', 'advcl:*', 'neg', 'nfincl', 'nfincl:*', 'ncmod', 'ncmod:*', 'advmod', 'acl', 'acl:*',
		'nmod', 'nmod:*', 'advcl', 'advcl:*', 'neg', 'nfincl', 'nfincl:*', 'ncmod', 'ncmod:*', 'acl', 'acl:*',

		# special clausal dependents
		'vocative', 'discourse', 'expl', 'aux', 'auxpass', 'cop', 'mark', 'punct',

		# noun dependents
		# 'nummod', 'appos', 'nmod', 'nmod:*', 'relcl', 'nfincl', 'nfincl:*', 'ncmod', 'ncmod:*', 'amod', 'advmod', 'det', 'neg',
		'nummod', 'appos', 'nmod', 'nmod:*', 'relcl', 'nfincl', 'nfincl:*', 'ncmod', 'ncmod:*', 'amod', 'det', 'neg',

		# compounding and unanalyzed
		'compound', 'compound:*', 'name', 'mwe', 'foreign','goeswith',
		# 'compound', 'name', 'mwe', 'foreign','goeswith',

		# coordination
		'conj', 'cc',

		# case-marking, prepositions, possessive
		#'case', 'case:*',

		# other
		'dep',

		]
}

# default semantic drift for index_cross_variable_connections()
dict_semantic_drift_default = {
	'conj' : 2,
	'cc' : 2,
	'appos' : 2,
	'parataxis' : 2,
	'list' : 2,
	'punct' : 2,
	'dislocated' : 2,
	'remnant' : 2,
	'dep' : 0
}

# aggressive generalization strategy for normalize_open_extraction_templates()
dict_generalize_strategy_default = {
	'relax_lex' : ['arg','rel'],
	'relax_pos' : [],
	'relax_pos_number_aware' : ['ctxt']
}

#
# POS tagged sent tree annotation functions
#

def annotate_phrase_sequences( list_sent_tree = None, dict_inverted_index_pos_phrase_patterns = None, dict_openie_config = None ) :
	"""
	calc n-gram phrases from sequences of tokens with the same POS tag

	:param list list_sent_tree: list of nltk.Tree representing the sents in a doc = [ nltk.Tree( '(S (IN For) (NN handle) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' ), ... ]
	:param dict dict_inverted_index_pos_phrase_patterns: inverted index from soton_corenlppy.re.openie_lib.calc_inverted_index_pos_phrase_patterns()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of nltk.Tree representing the sents in that doc after phrase sequencing
	:rtype: list
	"""

	if not isinstance( list_sent_tree, list ) :
		raise Exception( 'invalid list_sent_tree' )
	if not isinstance( dict_inverted_index_pos_phrase_patterns, dict ) :
		raise Exception( 'invalid dict_inverted_index_pos_phrase_patterns' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listSentSet = []

	# create n-gram phrases from POS pattern groups
	# - sequential POS tags are concatenated into phrases
	# - trees are groups already parsed in sent so represent phrases
	for treeSent in list_sent_tree :

		if not isinstance( treeSent, nltk.tree.Tree ) :
			raise Exception( 'non tree found in list_sent_tree_sets' )

		strLastPOSPattern = None
		nLastStart = 0
		listPhraseSet = []
		treePhraseSequence = nltk.Tree( 'S',[] )

		# loop on each leaf node in root sent tree
		# and generate phrases out of sequences of POS pattern types
		for nIndex in range(len(treeSent)) :

			leaf = treeSent[nIndex]
			if not isinstance( leaf, nltk.tree.Tree ) :
				raise Exception( 'non tree found in leaf : ' + repr(leaf) )

			strPOS = leaf.label()

			#strToken = unicode( ' '.join( leaf.leaves() ) )
			#dict_openie_config['logger'].info( repr( [strPOS, strToken] ) )

			if strPOS in dict_inverted_index_pos_phrase_patterns :
				strPOSPattern = dict_inverted_index_pos_phrase_patterns[ strPOS ]
			else :
				strPOSPattern = strPOS

			if strLastPOSPattern == None :

				# start POS pattern
				strLastPOSPattern = strPOSPattern
				nLastStart = nIndex

			elif strLastPOSPattern != strPOSPattern :

				# make phrase
				listPhrase = []
				for nIndexPhrase in range( nLastStart, nIndex ) :
					listPhrase.append( str( ' '.join( treeSent[nIndexPhrase].leaves() ) ) )
				strPhrase = ' '.join( listPhrase )

				treePhraseSequence.append( nltk.Tree( strLastPOSPattern, [strPhrase] ) )

				# start new pattern
				strLastPOSPattern = strPOSPattern
				nLastStart = nIndex

			else :

				# continue POS pattern
				continue

		# use whatever is left to make final phrase
		if strLastPOSPattern != None :
			# make phrase
			listPhrase = []
			for nIndexPhrase in range( nLastStart, len(treeSent) ) :
				listPhrase.append( str( ' '.join( treeSent[nIndexPhrase].leaves() ) ) )
			strPhrase = ' '.join( listPhrase )

			treePhraseSequence.append( nltk.Tree( strLastPOSPattern, [strPhrase] ) )

		# add sent tree containing phrases
		listSentSet.append( treePhraseSequence )

	# all done
	return listSentPhraseSet


#def annotate_using_pos_patterns( list_sent_trees = None, list_phrase_sequence_patterns_exec_order = soton_corenlppy.re.openie_lib.list_phrase_sequence_patterns_exec_order_default, dict_phrase_sequence_patterns = soton_corenlppy.re.openie_lib.dict_phrase_sequence_patterns_default, dict_openie_config = None ) :
def annotate_using_pos_patterns( list_sent_trees = None, list_phrase_sequence_patterns_exec_order = openie_lib.list_phrase_sequence_patterns_exec_order_default, dict_phrase_sequence_patterns = openie_lib.dict_phrase_sequence_patterns_default, dict_openie_config = None ) :
	"""
	Apply on a set of tagged sent trees a set of pos patterns (e.g. for ReVerb arguments and relations or CH entities, lists of entities, attributes and relations).
	The result is a sent with POS pattern annotations represented as nltk.Tree elements.

	:param list list_sent_trees: list of nltk.Tree representing the sents in a doc
	:param list list_phrase_sequence_patterns_exec_order: order that phrase sequence patterns should be executed (usually most permissive last). see openie.list_phrase_sequence_patterns_exec_order_default
	:param dict dict_phrase_sequence_patterns: phrase sequence patterns of compiled regex extracted groups with same name as pattern = { pattern : [ regex, regex, ... ] }. see openie.dict_phrase_sequence_patterns_default for example
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of documents, each containing a list of nltk.Tree objects representing an extracted lexico-pos pattern for entity, attribute and relation phrases
	:rtype: list
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'invalid list_sent_trees' )
	if not isinstance( list_phrase_sequence_patterns_exec_order, list ) :
		raise Exception( 'invalid list_phrase_sequence_patterns_exec_order' )
	if not isinstance( dict_phrase_sequence_patterns, dict ) :
		raise Exception( 'invalid dict_phrase_sequence_patterns' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listAnnotatedTrees = []

	for nTreeIndex in range(len(list_sent_trees)) :
		treeSent = list_sent_trees[nTreeIndex]

		# serialize tree ensuring tokens are safely escaped etc
		strTree = soton_corenlppy.common_parse_lib.serialize_tagged_tree( tree_sent = treeSent, dict_common_config = dict_openie_config )
		# strTree = treeSent.pformat( margin=100000 )

		# create a version of the serialized tree that blanks out all deep structures just for matching
		# this allows regex matches to be a lot simpler and not sorry about n-deep () structures
		# the size is identical to the original sent so we can use the match character positions later
		# e.g.
		# original = (S (ATTRIBUTE (NOUN_P handle plates) (PREPOSITION_P of) (NOUN_P column kraters)) (VERB_P attributed) ...)
		# blanked =  (S (ATTRIBUTE                                                                  ) (VERB_P           ) ...)
		strTreePOSOnly = blank_serialized_tree( tree_sent = treeSent, dict_openie_config = dict_openie_config )

		#dict_openie_config['logger'].info( strTree )
		#dict_openie_config['logger'].info( strTreePOSOnly )

		# extract patterns in the order specified
		for strPatternName in list_phrase_sequence_patterns_exec_order :

			# execute regex in sequential order
			for rePattern in dict_phrase_sequence_patterns[ strPatternName ] :

				# keep executing regex to get matches until there are no more matches
				bOK = True
				while bOK == True :

					matchObj = rePattern.match( strTreePOSOnly )
					if matchObj == None :
						bOK = False
					else :
						# get all named matches from this pattern
						# if a named match is optional it might have a None value
						for strGroupName in matchObj.groupdict() :

							strMatch = matchObj.group( strGroupName )
							if strMatch != None :

								nPosMatchStart = matchObj.start( strGroupName )
								nPosMatchEnd = matchObj.end( strGroupName )

								# create a tree entry for this matched pattern
								strMatchFragment = '(' + strGroupName + r' ' + strTree[nPosMatchStart:nPosMatchEnd] + ')'
								#dict_openie_config['logger'].info( strMatchFragment )

								# create a new sent tree with the fragment tree replacing the old text
								strTree = strTree[:nPosMatchStart] + strMatchFragment + strTree[nPosMatchEnd:]

								# parse it again so we can blank it also
								try :
									treeSent = soton_corenlppy.common_parse_lib.parse_serialized_tagged_tree( strTree, dict_common_config = dict_openie_config )
								except Exception :
									dict_openie_config['logger'].info( 'parse_serialized_tagged_tree() failed for tree : ' + repr(strTree) )
									raise

								strTreePOSOnly = blank_serialized_tree( tree_sent = treeSent, dict_openie_config = dict_openie_config )

								# there should only be a single named match so break and check for new tree for another other matches
								# later in the text (e.g. two relations in a sent)
								break

			#dict_openie_config['logger'].info( '>>' + strTreePOSOnly )

		# return the final sent tree with the matches inserted as patterns
		treeSent = soton_corenlppy.common_parse_lib.parse_serialized_tagged_tree( strTree, dict_common_config = dict_openie_config )
		listAnnotatedTrees.append( treeSent )

	# all done
	return listAnnotatedTrees


def blank_serialized_tree( tree_sent = None, dict_openie_config = None ) :
	"""
	create a version of the serialized tree that blanks out all deep structures just for matching
	this allows regex matches to be a lot simpler and not sorry about n-deep () structures
	the size is identical to the original sent so we can use the match character positions later
	e.g.
	original = (S (ATTRIBUTE (NOUN_P handle plates) (PREPOSITION_P of) (NOUN_P column kraters)) (VERB_P attributed) ...)
	blanked =  (S (ATTRIBUTE                                                                  ) (VERB_P           ) ...)

	:param nltk.Tree treeSent: nltk.Tree representing a sent = nltk.Tree( '(S (IN For) (NN handle) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' )
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: serialized tree blanked
	:rtype: unicode
	"""
	listBlanked = []
	for leaf in tree_sent :
		strLeaf = soton_corenlppy.common_parse_lib.serialize_tagged_tree( tree_sent = leaf, dict_common_config = dict_openie_config )
		#strLeaf = leaf.pformat( margin=100000 )
		strBlanked = '(' + leaf.label() + ' '*(len( strLeaf ) - len(leaf.label()) - 2) + ')'
		listBlanked.append( strBlanked )
	strTreePOSOnly = '(S ' + ' '.join( listBlanked ) + ')'

	return strTreePOSOnly



def extract_annotations_from_sents( list_sent_trees = None, set_annotations = set([]), pos_tags = False, include_start_and_end_annotations = False, dict_openie_config = None ) :
	"""
	extract a set of annotations from a list of sent trees. for example extracting argument and relation annotations from ReVerb style annotated sent trees.

	:param list list_sent_trees: list of nltk.Tree representing the sents in that doc = [ nltk.Tree( '(S (IN For) (NN handle) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' ), ... ]
	:param set set_annotations: set of allowed annotation labels e.g. set( ['RELATION','ARGUMENT'] )
	:param bool pos_tags: if True use nltk.Tree.pos() to return tuples ('token','pos') not just strings 'token' after the node label
	:param bool include_start_and_end_annotations: if True add START and END annotations if the sent start and end immediately preceeds or suffixes a matching annotation
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of sent extractions, each a list of annotation tuples (type,token) extracted in the order they appear in the sent e.g. [ [ ('ARGUMENT','John'), ('RELATION','come','from'), ('ARGUMENT','Paris') ], ... ]
	:rtype: list
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'invalid list_sent_trees' )
	if not isinstance( set_annotations, set ) :
		raise Exception( 'invalid set_annotations' )
	if not isinstance( pos_tags, bool ) :
		raise Exception( 'invalid pos_tags' )
	if not isinstance( include_start_and_end_annotations, bool ) :
		raise Exception( 'invalid include_start_and_end_annotations' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listSentExtractions = []

	for treeSent in list_sent_trees :

		listExtraction = []

		if not isinstance( treeSent, nltk.tree.Tree ) :
			raise Exception( 'nltk.Tree not found in list_sent_trees : ' + repr(type(treeSent)) )

		# match each leaf node to the set of annotations
		for nIndex in range(len(treeSent)) :

			leaf = treeSent[nIndex]
			if not isinstance( leaf, nltk.tree.Tree ) :
				raise Exception( 'nltk.Tree not found in leaf : ' + repr(leaf) )

			if leaf.label() in set_annotations :
				# is this the START?
				if (include_start_and_end_annotations == True) and (nIndex == 0) :
					listExtraction.append( tuple( [ 'START', '' ] ) )

				# get the collapsed tokens for this leaf
				listMatch = [ leaf.label() ]

				if pos_tags == False :
					listMatch.extend( leaf.leaves() )
				else :
					listMatch.extend( leaf.pos() )

				# record the extraction
				listExtraction.append( tuple( listMatch ) )

				# is this the END?
				if (include_start_and_end_annotations == True) and (nIndex == len(treeSent)-1) :
					listExtraction.append( tuple( [ 'END', '' ] ) )

		listSentExtractions.append( listExtraction )

	# all done
	return listSentExtractions


def generate_seed_tuples( list_sent_trees = None, generation_strategy = 'contiguous_tuple', set_annotations = None, dict_annotation_phrase_patterns = {}, list_sequences = None, prevent_sequential_instances = None, lower_case = False, stemmer = None, dict_openie_config = None ) :
	"""
	generate seed tuples and var candidates ready for generate_open_extraction_templates() using a number of strategies.
	a seed tuple is a sequence of annotations suitable for graph walk targets. e.g. [ ('ARGUMENT','London','bridge'), ('RELATION','is', 'burning'), ('ARGUMENT','down') ]
	a var candidate is a sub-phrase (noun, verb or pronoun phrase) appearing in an annotation e.g. { 'ARGUMENT' : ['London', ...] }

	generation strategies:
		* predefined_sequences - explicitly allowed sent annotation sequences e.g. (arg rel arg), (arg rel arg rel arg)
		* contiguous_tuple - all possible sent annotation tuple (up to quad) contiguous sequence combinations e.g. (arg, rel, arg)
		* contiguous_tuple_candidates - all possible var candidate tuple (up to quad) contiguous sequence combinations e.g. (arg, rel, arg)
		* contiguous_tuple_with_seq_groups - all possible sent annotation tuple (up to quad), which meet both a contiguous and sequence group criteria e.g. (arg, (rel,arg))

	var candidate generation strategy:
		* allow any pronoun, noun and verb phrase appearing within an annotation

	returns a set of seed tuples that a later dependency graph walk can use as target var's.
	returns a set of phrases for possible intermediate var candidates, so context var types can be replaced with known var types.
	note that ,:; characters are removed from generated seed tuples as they do not appear in a dep graph (so a tuple with them would never match)
	note that START and END are special labels indicating the start or end of the sent should be matched

	:param list list_sent_trees: list of nltk.Tree representing the sents in that doc = [ nltk.Tree( '(S (DT the) (ARGUMENT (NN handle)) (RELATION (VBZ missing)) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' ), ... ]
	:param str generation_strategy: name of generation strategy = predefined_sequences|contiguous_tuple|contiguous_tuple_candidates
	:param set set_annotations: filter set of annotation labels to create sequences for e.g. set( ['RELATION','ARGUMENT'] ) - [predefined_sequences, contiguous_triples]
	:param dict dict_annotation_phrase_patterns: allowed phrase patterns for each variable type e.g. { 'ARGUMENT' : ['noun_phrase','pronoun'], 'RELATION' : [verb_phrase'] }
	:param list list_sequences: list of sequences to allow as seed_tuples, including special START and END labels. for predefined_sequences its the set of predefined sequences  e.g. [ ('ARGUMENT','RELATION','ARGUMENT'), ('ARGUMENT','RELATION') ]). for contiguous_tuple its the tuple pattern (up to quad) to generate e.g. [ 'ARGUMENT','RELATION','ARGUMENT' ] - [predefined_sequences, contiguous_triples]
	:param list prevent_sequential_instances: list of seed types to prevent sequencial instance matching e.g. ['PREPOSITION'] - [predefined_sequences]
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: tuple of (list_seed_tuples, var_candidates). list_seed_tuples = [ ( ('ARGUMENT','John'), ('RELATION','come','from'), ('ARGUMENT','Paris') ), ... ]. var_candidates = { 'ARGUMENT' : [ ('John','Barnes'), ('Pele',) ] }
	:rtype: tuple
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'invalid list_sent_trees' )
	if not isinstance( generation_strategy, str ) :
		raise Exception( 'invalid generation_strategy' )
	if not isinstance( set_annotations, (set,type(None)) ) :
		raise Exception( 'invalid set_annotations' )
	if not isinstance( dict_annotation_phrase_patterns, dict ) :
		raise Exception( 'invalid dict_annotation_phrase_patterns' )
	if not isinstance( list_sequences, (list,type(None)) ) :
		raise Exception( 'invalid list_sequences' )
	if not isinstance( prevent_sequential_instances, (list,type(None)) ) :
		raise Exception( 'invalid prevent_sequential_instances' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )

	listSeedTuples = []
	dictVarCandidates = {}
	listSentExtractions = None
	listSentVarCandidates = []
	listFilterPhrases = [ ';', ':', ',', '.' ]

	#
	# var candidate generation (any pronoun, lexicon matched noun phrases)
	#

	if set_annotations == None :
		raise Exception( 'set_annotations is None (required)' )

	# get from sent annotation a sequence of annotations (with START and END)
	# listSentExtractions = [ [ ('START',''), ('ARGUMENT','John'), ('RELATION','come from'), ('ARGUMENT','Paris'), ... ], ... ]
	listSentExtractions = extract_annotations_from_sents(
		list_sent_trees = list_sent_trees,
		set_annotations = set_annotations,
		pos_tags = False,
		include_start_and_end_annotations = True,
		dict_openie_config = dict_openie_config )

	# listSentExtractionsPosTagged = [ [ ('ARGUMENT',('John','NN'), ...), ... ], ... ]
	listSentExtractionsPosTagged = extract_annotations_from_sents(
		list_sent_trees = list_sent_trees,
		set_annotations = set_annotations,
		pos_tags = True,
		include_start_and_end_annotations = True,
		dict_openie_config = dict_openie_config )

	# debug
	#for entry in listSentExtractions :
	#	dict_openie_config['logger'].info( 'seed gen extracts = ' + repr(entry) )

	# loop on each extracted annotation and get var candidates
	for nSentIndex in range(len(listSentExtractionsPosTagged)) :
		listExtractionPosTagged = listSentExtractionsPosTagged[nSentIndex]
		listExtraction = listSentExtractions[nSentIndex]
		listVarCandidates = []

		for nExtractionPos in range(len(listExtractionPosTagged)) :
			# loop on post tag list
			# - lookup any continuous noun sequence as a noun phrase => lexicon match == var candidate
			# - any pronoun == var candidate
			listPhraseTokens = []
			nTokenIndex = 0
			nPhraseIndex = None
			strPhraseType = None
			strLastPhraseType = None

			# var type (e.g. ARGUMENT)
			strVar = listExtractionPosTagged[nExtractionPos][0]
			if strVar in [ 'START','END' ] :
				listPhrasePatterns = []
			else :
				listPhrasePatterns = dict_annotation_phrase_patterns[strVar]

			for nTokenIndex in range( 1,len(listExtractionPosTagged[nExtractionPos]) ) :
				tuplePOS = listExtractionPosTagged[nExtractionPos][nTokenIndex]

				if ('pronoun' in listPhrasePatterns) and (tuplePOS[1] in ['PRP','PRP$','WP','WP$','WDT']) :
					strPhraseType = 'pronoun'
				elif ('noun_phrase' in listPhrasePatterns) and (tuplePOS[1] in ['NNP','NNPS','NN','NNS','INITIAL','TITLE']) :
					strPhraseType = 'noun_phrase'
				elif ('verb_phrase' in listPhrasePatterns) and (tuplePOS[1] in ['VB','VBD','VBG','VBN','VBP','VBZ','MD']) :
					strPhraseType = 'verb_phrase'
				else :
					strPhraseType = None

				if (strLastPhraseType != strPhraseType) and (len(listPhraseTokens) > 0) :

					# check previous phrase for a var candidate
					# dict_openie_config['logger'].info( 'T1 = ' + repr(listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)]) )
					if not strVar in dictVarCandidates :
						dictVarCandidates[strVar] = []
					dictVarCandidates[strVar].append( listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)] )
					listVarCandidates.append( ( strVar, nExtractionPos, listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)] ) )

					# reset phrase
					listPhraseTokens = []
					nPhraseIndex = None

				if strPhraseType != None :
					# set phrase start point if needed
					if len(listPhraseTokens) == 0 :
						nPhraseIndex = nTokenIndex
					
					# add token to phrase
					if lower_case == True :
						listPhraseTokens.append( tuplePOS[0].lower() )
					else :
						listPhraseTokens.append( tuplePOS[0] )
					#dict_openie_config['logger'].info( 'T4 = ' + repr(tuplePOS[0]) )
				
				# remember last phrase type so we know if its a sequence or not
				strLastPhraseType = strPhraseType

			# check final phrase (if any)
			if len(listPhraseTokens) > 0 :

				# check previous phrase for a var candidate
				# dict_openie_config['logger'].info( 'T1 = ' + repr(listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)]) )
				if not strVar in dictVarCandidates :
					dictVarCandidates[strVar] = []
				dictVarCandidates[strVar].append( listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)] )
				listVarCandidates.append( ( strVar, nExtractionPos, listExtraction[nExtractionPos][nPhraseIndex : nPhraseIndex + len(listPhraseTokens)] ) )

		# remember var candidates for each sent (needed for contiguous_triples)
		listSentVarCandidates.append( listVarCandidates )

	# debug
	#for entry in listSentVarCandidates :
	#	dict_openie_config['logger'].info( 'sent_var_can = ' + repr(entry) )

	#
	# seed generation
	#

	if generation_strategy == 'predefined_sequences' :

		# match pre-defined sequences of annotations
		# allow multiple instances of the same annotation type to be matched to a single annotation (e.g. arg arg rel arg == arg rel arg)

		if list_sequences == None :
			raise Exception( 'list_sequences is None (required)' )
		if prevent_sequential_instances == None :
			raise Exception( 'prevent_sequential_instances is None (required)' )

		# loop on the extracted annotations and try to match each allowed sequence
		for nSentIndex in range(len(listSentExtractions)) :
			listExtraction = listSentExtractions[nSentIndex]
			for tupleSequence in list_sequences :

				# try at each start position to match the target sequence
				# allow multiple targets to count as one in the sequence (e.g. RELATION means 2 x RELATION OK, ARGUMENT means 3 x ARGUMENT OK)
				for nExtractionPosStart in range(len(listExtraction)) :

					nSeqPos = 0
					nLastSeqPos = None
					nExtractionPos = nExtractionPosStart
					listSeed = []

					# loop until one past end of list, so we get all sequence instances of the last item
					while( nSeqPos <= len(tupleSequence) ) :

						if (nSeqPos < len(tupleSequence) ) and (listExtraction[nExtractionPos][0] == tupleSequence[nSeqPos]) :
							# annotation matches next in sequence

							# add extraction to seed list
							listSeed.append( tuple( listExtraction[nExtractionPos] ) )

							# move to next in sequence
							nLastSeqPos = nSeqPos
							nSeqPos = nSeqPos + 1

							# move to next in extraction
							nExtractionPos = nExtractionPos + 1

							# last tuple populated? add all variants as we make them with variable last tuple sequence instance length
							if nSeqPos == len(tupleSequence) :
								listSeedTuples.append( tuple( listSeed ) )

							# run out of extractions to check?
							if nExtractionPos >= len(listExtraction) :
								break

						elif (nLastSeqPos != None) and (listExtraction[nExtractionPos][0] == tupleSequence[nLastSeqPos] ) and (listExtraction[nExtractionPos][0] not in prevent_sequential_instances) :
							# annotation matches previous in sequence (e.g. several args in a row)

							# add extraction to seed list
							listSeed.append( tuple( listExtraction[nExtractionPos] ) )

							# last tuple populated? add all variants as we make them with variable last tuple sequence instance length
							if nSeqPos == len(tupleSequence) :
								listSeedTuples.append( tuple( listSeed ) )

							# move to next in extraction
							nExtractionPos = nExtractionPos + 1

							# run out of extractions to check?
							if nExtractionPos >= len(listExtraction) :
								break

						else :
							# abort as sequence did not match
							break

	elif generation_strategy == 'contiguous_tuple' :

		# for each sent get the list of var candidates, and compute all the possible tuples (up to quad)
		# which are contiguous in the sent address range
		# e.g. arg1, rel2, arg3, arg4, rel5, arg6 => (arg1, rel2, arg3), (arg1, rel2, arg4), (arg1, rel2, arg6) ...
		# allow multiple instances of the same annotation type to be matched to a single annotation
		# the idea is to let the extraction filtering choose the resulting patterns that have a low semantic drift (as this will include a lot of noise)

		if list_sequences == None :
			raise Exception( 'list_sequences is None (required)' )
		if prevent_sequential_instances == None :
			raise Exception( 'prevent_sequential_instances is None (required)' )

		for tuple_pattern in list_sequences :

			if len(tuple_pattern) < 1 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too small)' )
			if len(tuple_pattern) > 4 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too large)' )

			# loop on sent vars and generate all valid triple combinations
			for nSentIndex in range(len(listSentExtractions)) :
				listExtraction = listSentExtractions[nSentIndex]

				#dict_openie_config['logger'].info( 'S1 = ' + repr( (nSentIndex, listExtraction ) ) )

				# make a list of vars with correct type for each of the 1..4 tuple levels
				# assert all available combinations that preserve the extraction position sequence
				for nExtractionPos1 in range(len(listExtraction)) :
					if listExtraction[nExtractionPos1][0] == tuple_pattern[0] :
						tupleLevel1 = tuple( listExtraction[nExtractionPos1] )

						if len(tuple_pattern) > 1 :
							for nExtractionPos2 in range(nExtractionPos1+1, len(listExtraction)) :
								if listExtraction[nExtractionPos2][0] == tuple_pattern[1] :
									tupleLevel2 = tuple( listExtraction[nExtractionPos2] )

									if len(tuple_pattern) > 2 :
										for nExtractionPos3 in range(nExtractionPos2+1, len(listExtraction)) :
											if listExtraction[nExtractionPos3][0] == tuple_pattern[2] :
												tupleLevel3 = tuple( listExtraction[nExtractionPos3] )

												if len(tuple_pattern) > 3 :
													for nExtractionPos4 in range(nExtractionPos3+1, len(listExtraction)) :
														if listExtraction[nExtractionPos4][0] == tuple_pattern[3] :
															tupleLevel4 = tuple( listExtraction[nExtractionPos4] )

															# we now have a viable triple option so add to list
															listSeedTuples.append( ( tupleLevel1, tupleLevel2, tupleLevel3, tupleLevel4 ) )

												else :
													# we now have a viable triple option so add to list
													listSeedTuples.append( ( tupleLevel1, tupleLevel2, tupleLevel3 ) )
									else :
										# we now have a viable triple option so add to list
										listSeedTuples.append( ( tupleLevel1, tupleLevel2 ) )

						else :
							# we now have a viable triple option so add to list
							listSeedTuples.append( ( tupleLevel1 ) )


	elif generation_strategy == 'contiguous_tuple_candidates' :

		# for each sent get the list of var type candidates, and compute all the possible triples (actually 1..3 tuple)
		# which are contiguous in the sent address range
		# e.g. arg1, rel2, arg3, arg4, rel5, arg6 => (arg1, rel2, arg3), (arg1, rel2, arg4), (arg1, rel2, arg6) ...
		# allow multiple instances of the same annotation type to be matched to a single annotation

		if list_sequences == None :
			raise Exception( 'list_sequences is None (required)' )
		if prevent_sequential_instances == None :
			raise Exception( 'prevent_sequential_instances is None (required)' )

		for tuple_pattern in list_sequences :

			if len(tuple_pattern) < 1 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too small)' )
			if len(tuple_pattern) > 4 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too large)' )

			# loop on var candidates for each sent and generate all valid triple combinations
			for nSentIndex in range(len(listSentVarCandidates)) :
				listVarCandidates = listSentVarCandidates[nSentIndex]

				# loop on all candidates for this sent, finding all contiguous combinations for a triple
				# note: phrase pos is the position in the list of extracted annotations (e.g. arg1, arg2, rel3, arg4 -> pos 2 = arg2)
				#       this is not a token index in sent. extractions do however appear in the order they appear in sents so we can use this to check for contiguous
				for nCandidateIndex1 in range(len(listVarCandidates)) :
					(strVarTypeCandidate1, nPhraseCandidatePos1, listPhraseCandidate1) = listVarCandidates[nCandidateIndex1]
					listLevel1 = []
					if strVarTypeCandidate1 == tuple_pattern[0] :
						# add match
						listEntry = [strVarTypeCandidate1]
						listEntry.extend( listPhraseCandidate1 )
						listLevel1.append( tuple( listEntry ) )

						# add an sequential candidates also (if same type)
						if not strVarTypeCandidate1 in prevent_sequential_instances :
							for nCandidateIndex1_seq in range(nCandidateIndex1+1, len(listVarCandidates)) :
								(strVarTypeCandidate1_seq, nPhraseCandidatePos1_seq, listPhraseCandidate1_seq) = listVarCandidates[nCandidateIndex1_seq]
								if strVarTypeCandidate1_seq == tuple_pattern[0] :
									# add seq match
									listEntry = [strVarTypeCandidate1_seq]
									listEntry.extend( listPhraseCandidate1_seq )
									listLevel1.append( tuple( listEntry ) )
								else :
									# end of seq so stop looking
									break

						if len(tuple_pattern) > 1 :
							for nCandidateIndex2 in range(len(listVarCandidates)) :
								(strVarTypeCandidate2, nPhraseCandidatePos2, listPhraseCandidate2) = listVarCandidates[nCandidateIndex2]
								listLevel2 = []
								if (strVarTypeCandidate2 == tuple_pattern[1]) and (nPhraseCandidatePos2 > nPhraseCandidatePos1) :
									# add match
									listEntry = [strVarTypeCandidate2]
									listEntry.extend( listPhraseCandidate2 )
									listLevel2.append( tuple( listEntry ) )

									# add an sequential candidates also (if same type)
									if not strVarTypeCandidate2 in prevent_sequential_instances :
										for nCandidateIndex2_seq in range(nCandidateIndex2+1, len(listVarCandidates)) :
											(strVarTypeCandidate2_seq, nPhraseCandidatePos2_seq, listPhraseCandidate2_seq) = listVarCandidates[nCandidateIndex2_seq]
											if strVarTypeCandidate2_seq == tuple_pattern[1] :
												# add seq match
												listEntry = [strVarTypeCandidate2_seq]
												listEntry.extend( listPhraseCandidate2_seq )
												listLevel2.append( tuple( listEntry ) )
											else :
												# end of seq so stop looking
												break

									if len(tuple_pattern) > 2 :
										for nCandidateIndex3 in range(len(listVarCandidates)) :
											(strVarTypeCandidate3, nPhraseCandidatePos3, listPhraseCandidate3) = listVarCandidates[nCandidateIndex3]
											listLevel3 = []
											if (strVarTypeCandidate3 == tuple_pattern[2]) and (nPhraseCandidatePos3 > nPhraseCandidatePos2) :
												# add match
												listEntry = [strVarTypeCandidate3]
												listEntry.extend( listPhraseCandidate3 )
												listLevel3.append( tuple( listEntry ) )

												# add an sequential candidates also (if same type)
												if not strVarTypeCandidate3 in prevent_sequential_instances :
													for nCandidateIndex3_seq in range(nCandidateIndex3+1, len(listVarCandidates)) :
														(strVarTypeCandidate3_seq, nPhraseCandidatePos3_seq, listPhraseCandidate3_seq) = listVarCandidates[nCandidateIndex3_seq]
														if strVarTypeCandidate3_seq == tuple_pattern[2] :
															# add seq match
															listEntry = [strVarTypeCandidate3_seq]
															listEntry.extend( listPhraseCandidate3_seq )
															listLevel3.append( tuple( listEntry ) )
														else :
															# end of seq so stop looking
															break

												if len(tuple_pattern) > 3 :
													for nCandidateIndex4 in range(len(listVarCandidates)) :
														(strVarTypeCandidate4, nPhraseCandidatePos4, listPhraseCandidate4) = listVarCandidates[nCandidateIndex4]
														listLevel4 = []
														if (strVarTypeCandidate4 == tuple_pattern[3]) and (nPhraseCandidatePos4 > nPhraseCandidatePos3) :
															# add match
															listEntry = [strVarTypeCandidate4]
															listEntry.extend( listPhraseCandidate4 )
															listLevel4.append( tuple( listEntry ) )

															# add an sequential candidates also (if same type)
															if not strVarTypeCandidate4 in prevent_sequential_instances :
																for nCandidateIndex4_seq in range(nCandidateIndex4+1, len(listVarCandidates)) :
																	(strVarTypeCandidate4_seq, nPhraseCandidatePos4_seq, listPhraseCandidate4_seq) = listVarCandidates[nCandidateIndex4_seq]
																	if strVarTypeCandidate4_seq == tuple_pattern[3] :
																		# add seq match
																		listEntry = [strVarTypeCandidate4_seq]
																		listEntry.extend( listPhraseCandidate4_seq )
																		listLevel4.append( tuple( listEntry ) )
																	else :
																		# end of seq so stop looking
																		break

															# we now have a viable triple option so add to list
															listLevelResult = copy.copy( listLevel1 )
															listLevelResult.extend( listLevel2 )
															listLevelResult.extend( listLevel3 )
															listLevelResult.extend( listLevel4 )
															listSeedTuples.append( tuple( listLevelResult ) )


												else :
													# we now have a viable triple option so add to list
													listLevelResult = copy.copy( listLevel1 )
													listLevelResult.extend( listLevel2 )
													listLevelResult.extend( listLevel3 )
													listSeedTuples.append( tuple( listLevelResult ) )
									else :
										# we now have a viable triple option so add to list
										listLevelResult = copy.copy( listLevel1 )
										listLevelResult.extend( listLevel2 )
										listSeedTuples.append( tuple( listLevelResult ) )

						else :
							# we now have a viable triple option so add to list
							listLevelResult = copy.copy( listLevel1 )
							listSeedTuples.append( tuple( listLevelResult ) )

	elif generation_strategy == 'contiguous_tuple_with_seq_groups' :

		# for each sent get the list of var type candidates, and compute all the possible tuples (up to quad)
		# BOTH contiguous and sequence groups are allowed
		# e.g. (arg, rel, arg) ==> (arg1, rel2, arg3), (arg1, rel2, arg4), (arg1, rel2, arg6) ...
		# e.g. (entity, (attr, prep), entity) ==> (entity1 ... attr5, prep6 ... entity7), (entity1, attr2, prep3, entity4) ...
		# sequence groups must appear without any other 
		# the idea is to let the extraction filtering choose the resulting patterns that have a low semantic drift (as this will include a lot of noise) but still include apriori known sequence criteria

		if list_sequences == None :
			raise Exception( 'list_sequences is None (required)' )
		if prevent_sequential_instances == None :
			raise Exception( 'prevent_sequential_instances is None (required)' )

		# listSentExtractions = [ [ ('ARGUMENT','John'), ('RELATION','come from'), ('ARGUMENT','Paris'), ... ], ... ]


		for tuple_pattern in list_sequences :

			if len(tuple_pattern) < 1 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too small)' )
			if len(tuple_pattern) > 4 :
				raise Exception( 'list_sequences does not contain a tuple pattern (too large)' )

			# loop on sent vars and generate all valid triple combinations
			for nSentIndex in range(len(listSentExtractions)) :
				listExtraction = listSentExtractions[nSentIndex]

				#dict_openie_config['logger'].info( 'S1 = ' + repr( (nSentIndex, listExtraction ) ) )

				# make a list of vars with correct type for each of the 1..4 tuple levels
				# assert all available combinations that preserve the extraction position sequence
				nExtractionPos1 = 0
				while nExtractionPos1 < len(listExtraction) :

					# get sequence of seeds that must appear continuously at this level
					if isinstance( tuple_pattern[0], str ) :
						listSeq1 = [ tuple_pattern[0] ]
					elif isinstance( tuple_pattern[0], (tuple) ) :
						listSeq1 = tuple_pattern[0]
					else :
						raise Exception( 'tuple_pattern entry not a string or tuple' )

					# check seq is available (sequentially)
					listLevel1 = []
					nExtractionPos1_seq = nExtractionPos1
					for strTarget in listSeq1 :
						if (nExtractionPos1_seq < len(listExtraction)) and (listExtraction[nExtractionPos1_seq][0] == strTarget) :
							listLevel1.append( tuple( listExtraction[nExtractionPos1_seq] ) )
							nExtractionPos1_seq = nExtractionPos1_seq + 1

					#dict_openie_config['logger'].info( 'S3.1 = ' + repr( listLevel1 ) )

					# check if continuous sequence found
					if len(listLevel1) == len(listSeq1) :

						nExtractionPos2 = nExtractionPos1_seq

						if len(tuple_pattern) > 1 :
							while nExtractionPos2 < len(listExtraction) :

								# get sequence of seeds that must appear continuously at this level
								if isinstance( tuple_pattern[1], str ) :
									listSeq2 = [ tuple_pattern[1] ]
								elif isinstance( tuple_pattern[1], (tuple) ) :
									listSeq2 = tuple_pattern[1]
								else :
									raise Exception( 'tuple_pattern entry not a string or tuple' )

								# check seq is available (sequentially)
								listLevel2 = []
								nExtractionPos2_seq = nExtractionPos2
								for strTarget in listSeq2 :
									if (nExtractionPos2_seq < len(listExtraction)) and (listExtraction[nExtractionPos2_seq][0] == strTarget) :
										listLevel2.append( tuple( listExtraction[nExtractionPos2_seq] ) )
										nExtractionPos2_seq = nExtractionPos2_seq + 1

								#dict_openie_config['logger'].info( 'S3.2 = ' + repr( listLevel2 ) )

								# check if continuous sequence found
								if len(listLevel2) == len(listSeq2) :

									nExtractionPos3 = nExtractionPos2_seq

									if len(tuple_pattern) > 2 :
										while nExtractionPos3 < len(listExtraction) :

											# get sequence of seeds that must appear continuously at this level
											if isinstance( tuple_pattern[2], str ) :
												listSeq3 = [ tuple_pattern[2] ]
											elif isinstance( tuple_pattern[2], (tuple) ) :
												listSeq3 = tuple_pattern[2]
											else :
												raise Exception( 'tuple_pattern entry not a string or tuple' )

											# check seq is available (sequentially)
											listLevel3 = []
											nExtractionPos3_seq = nExtractionPos3
											for strTarget in listSeq3 :
												if (nExtractionPos3_seq < len(listExtraction)) and (listExtraction[nExtractionPos3_seq][0] == strTarget) :
													listLevel3.append( tuple( listExtraction[nExtractionPos3_seq] ) )
													nExtractionPos3_seq = nExtractionPos3_seq + 1

											#dict_openie_config['logger'].info( 'S3.3 = ' + repr( listLevel3 ) )

											# check if continuous sequence found
											if len(listLevel3) == len(listSeq3) :

												nExtractionPos4 = nExtractionPos3_seq

												if len(tuple_pattern) > 3 :
													while nExtractionPos4 < len(listExtraction) :

														# get sequence of seeds that must appear continuously at this level
														if isinstance( tuple_pattern[3], str ) :
															listSeq4 = [ tuple_pattern[3] ]
														elif isinstance( tuple_pattern[3], (tuple) ) :
															listSeq4 = tuple_pattern[3]
														else :
															raise Exception( 'tuple_pattern entry not a string or tuple' )

														# check seq is available (sequentially)
														listLevel4 = []
														nExtractionPos4_seq = nExtractionPos4
														for strTarget in listSeq4 :
															if (nExtractionPos4_seq < len(listExtraction)) and (listExtraction[nExtractionPos4_seq][0] == strTarget) :
																listLevel4.append( tuple( listExtraction[nExtractionPos4_seq] ) )
																nExtractionPos4_seq = nExtractionPos4_seq + 1

														#dict_openie_config['logger'].info( 'S3.4 = ' + repr( listLevel4 ) )

														# check if continuous sequence found
														if len(listLevel4) == len(listSeq4) :

															# we now have a viable tuple option so add to list
															listEntry = copy.copy( listLevel1 )
															listEntry.extend( listLevel2 )
															listEntry.extend( listLevel3 )
															listEntry.extend( listLevel4 )
															listSeedTuples.append( tuple( listEntry ) )

													nExtractionPos4 = nExtractionPos4 + 1

												else :

													# we now have a viable tuple option so add to list
													listEntry = copy.copy( listLevel1 )
													listEntry.extend( listLevel2 )
													listEntry.extend( listLevel3 )
													listSeedTuples.append( tuple( listEntry ) )

											nExtractionPos3 = nExtractionPos3 + 1

									else :

										# we now have a viable tuple option so add to list
										listEntry = copy.copy( listLevel1 )
										listEntry.extend( listLevel2 )
										listSeedTuples.append( tuple( listEntry ) )

								nExtractionPos2 = nExtractionPos2 + 1

						else :

							# we now have a viable tuple option so add to list
							listEntry = copy.copy( listLevel1 )
							listSeedTuples.append( tuple( listEntry ) )

					nExtractionPos1 = nExtractionPos1 + 1

	else :
		raise Exception( 'unknown strategy value : ' + generation_strategy )

	# filter out tokens in seed phrases that will not appear in a dep graph so cannot be matched i.e. ,:;
	listFilterPhrases = [ ';', ':', ',', '.' ]
	nIndexSeed = 0
	while nIndexSeed < len(listSeedTuples) :
		# convert to list so we can edit it e.g. [ ('ARGUMENT','John'), ('RELATION','come','from'), ('ARGUMENT','Paris') ]
		listSeed = list( listSeedTuples[nIndexSeed] )

		nIndexPhrase = 0
		bDeleteSeed = False
		while nIndexPhrase < len(listSeed) :
			# convert to list so we can edit it i.e. [ 'RELATION','come','from' ]
			listPhrase = list( listSeed[nIndexPhrase] )

			# look on tokens for this seed phrase. 0 index is the type e.g. ARGUMENT
			nIndexToken = 1
			while nIndexToken < len(listPhrase) :
				if listPhrase[nIndexToken] in listFilterPhrases :
					del listPhrase[nIndexToken]
				else :
					nIndexToken = nIndexToken + 1
			
			# check if we have some tokens left in phrase
			if len(listPhrase) > 1 :
				# insert new phrase
				listSeed[nIndexPhrase] = tuple( listPhrase )
				nIndexPhrase = nIndexPhrase + 1
			else :
				# flag seed for removal as its no longer viable
				bDeleteSeed = True
				break

		if bDeleteSeed == True :
			del listSeedTuples[nIndexSeed]
		else :
			listSeedTuples[nIndexSeed] = tuple( listSeed )
			nIndexSeed = nIndexSeed + 1

	# filter out tokens in var candidates that will not appear in a dep graph so cannot be matched i.e. ,:;
	for strVarType in dictVarCandidates :
		nIndexPhrase = 0
		while nIndexPhrase < len(dictVarCandidates[strVarType]) :

			listPhrase = list( dictVarCandidates[strVarType][nIndexPhrase] )

			# look on tokens for this phrase
			nIndexToken = 0
			while nIndexToken < len(listPhrase) :
				if listPhrase[nIndexToken] in listFilterPhrases :
					del listPhrase[nIndexToken]
				else :
					nIndexToken = nIndexToken + 1

			# check if we have some tokens left in phrase
			if len(listPhrase) > 0 :
				# insert new phrase
				dictVarCandidates[strVarType][nIndexPhrase] = tuple( listPhrase )
				nIndexPhrase = nIndexPhrase + 1
			else :
				# delete it (empty phrase list for a var type is OK)
				del dictVarCandidates[strVarType][nIndexPhrase]

	# finished
	return ( listSeedTuples, dictVarCandidates )


#
# open template pattern extraction functions
#

def get_dependency_parser( dict_openie_config = None, dep_options = ['-tokenized','-tagSeparator','/','-tokenizerFactory','edu.stanford.nlp.process.WhitespaceTokenizer','-tokenizerMethod','newCoreLabelTokenizerFactory', '-maxLength', '200' ] ) :
	"""
	return a java command line for popen to run the Stanford dependency parser using exec_dep_parser().
	CMD is without an input text filename so assumes tagged text is provided via STDIN.
	default options limit parser to 200 words to avoid reported dep parser hanging situations processing overly long sentences.


	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	:param list dep_options: list of options for stanford dep parser

	:return: java command line for popen()
	:rtype: list
	"""

	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( dep_options, list ) :
		raise Exception( 'invalid dep_options' )

	if not 'dep_model_path' in dict_openie_config :
		raise Exception( 'dep_model_path not specified in dict_openie_config' )
	if not 'dep_model_jar' in dict_openie_config :
		raise Exception( 'dep_model_jar not specified in dict_openie_config' )
	if not 'stanford_parser_dir' in dict_openie_config :
		raise Exception( 'stanford_parser_dir not specified in dict_openie_config' )

	strModelPath = dict_openie_config['dep_model_path']
	strModelJar = dict_openie_config['dep_model_jar']
	strDepJar = dict_openie_config['stanford_parser_dir'] + os.sep + 'stanford-parser.jar' + os.pathsep + strModelJar

	listCMD = [
		'java',
		'-mx4g',
		'-cp',
		strDepJar,
		'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
		'-outputFormat',
		'conll2007',
		'-sentences',
		'newline',
		]

	for strOption in dep_options :
		listCMD.append( strOption )
	
	# for STDIN the model file needs to be defined at end without the -model path, and the special filename '-' added
	listCMD.append( strModelPath )
	listCMD.append( '-' )

	return listCMD

	'''

	#note: the dep_parser.tagged_parse_sents() function will return a graph that has { 'address' = None } values for values such as punctuation.
	#this causes problems re-parsing after serialization (e.g. dep_graph.to_conll( style=4 ) as the parser does not allow { 'head' = None }.
	#to avoid this all { 'address' = None } entries must have a special head value '_' which is understood by the parser e.g. { 'address' = None, 'head' = '_' }

	dep_parser = nltk.parse.stanford.StanfordDependencyParser(
		encoding = 'utf8',
		model_path = strModelPath,
		path_to_jar = strDepJar,
		path_to_models_jar = strModelJar,
		corenlp_options = strDepOptions,
		java_options = '-mx4096m',
		)

	return dep_parser
	'''

def exec_dep_parser( list_tagged_sents = None, dep_parser_cmd = None, dict_openie_config = None, timeout = 300, sigterm_handler = False ) :
	"""
	exec a java command line (created from get_dependency_parser()) using popen to run the Stanford dependency parser.
	pipes are used to avoid any need for file IO

	:param list list_tagged_sents: list of tagged sents from soton_corenlppy.common_parse_lib.pos_tag_tokenset()
	:param list dep_parser_cmd: list of commands for popen() from get_dependency_parser()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	:param int timeout: timeout in seconds for Dep Parser process in the unlikely event the POS tagger hangs
	:param bool sigterm_handler: if True SIGTERM will be setup to terminate the process handle before exit

	:return: list of nltk.parse.DependencyGraph objects (one per sent)
	:rtype: list
	"""

	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( list_tagged_sents, list ) :
		raise Exception( 'invalid list_tagged_sents' )
	if not isinstance( dep_parser_cmd, list ) :
		raise Exception( 'invalid dep_parser_cmd' )
	if not isinstance( timeout, int ) :
		raise Exception( 'invalid timeout' )

	p = None
	queueBufferOut = None
	queueBufferErr = None

	try :
		# prepare the tagged sentences input for STDIN
		listInput = []
		for listTaggedSent in list_tagged_sents :
			strTaggedSent = soton_corenlppy.common_parse_lib.serialize_tagged_list(
				list_pos = listTaggedSent,
				dict_common_config = dict_openie_config,
				serialization_style = 'pos' )
			listInput.append( strTaggedSent )

		# depparser run as an external process using PIPE's (to avoid need for access rights to disk)
		# note: the dep_parser needs a POS tag ./. at the end to indicate the end of a sentence, as it will not do sent tokenization itself
		p = subprocess.Popen( dep_parser_cmd, cwd='.', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )

		# remember the last process handle so kill_dep_parser() will be able to terminate it in the event of a SIGTERM
		if sigterm_handler == True :
			p_global = p
			signal.signal( signal.SIGTERM, kill_dep_parser )

		# read in a thread to avoid PIPE deadlocks (see popen() and all the pipe horrors for python!)
		# set them as daemon so main process can exit and these will be killed (as opposed to non-daemon where main thread waits for them to finish)
		queueBufferOut = queue.Queue()
		threadOut = threading.Thread( target = read_pipe_stdout, args=(p.stdout,queueBufferOut) )
		threadOut.setDaemon( True )
		threadOut.start()

		queueBufferErr = queue.Queue()
		threadErr = threading.Thread( target = read_pipe_stderr, args=(p.stderr,queueBufferErr) )
		threadErr.setDaemon( True )
		threadErr.start()

		time.sleep( 0.001 )

		# loop on each sentence, write it, get the answer then move to next one
		listDepGraphTotal = []
		for nIndexSent in range(len(listInput)) :
			strSent = listInput[nIndexSent].strip()

			# is process dead?
			if p.poll() != None :
				# raise exception with the errors (process dead)
				listError = []
				while queueBufferErr.empty() == False :
					listError.append( queueBufferErr.get().strip() )
				raise Exception( 'DEP PARSE failed : ' + '\n'.join( listError ) )

			# send set of tokens for each sentence to dep_parser
			strIn = strSent.encode( 'utf8' )

			# write newline (properties use newline to provide the sent delimiter)
			strIn = strIn + '\r\n'.encode( 'utf8' )

			#dict_openie_config['logger'].info('STDIN >> ' + repr(strIn) )

			# push to STDIN
			p.stdin.write( strIn )
			p.stdin.flush()

			# set a timeout (5 mins) after which we give up trying to read from stdout (in case of error on last token)
			dateExpire = datetime.datetime.now() + datetime.timedelta( seconds = timeout )

			# read conll2007 formatted output until we get a empty line (indicating its finished)
			# note: stderr is spammed with loads of stuff so only report it if we dont get the right number of dep graphs back
			# note: Stanford parser RAM usage increases squared to sent length. Also computation speed degrades with sent length. Thats why we use the -maxLength to limit sent length.
			bFinished = False
			strConll2007 = ''
			while bFinished == False :
				# are we timed out?
				if (dateExpire != None) and (datetime.datetime.now() > dateExpire) :
					listError = []
					while queueBufferErr.empty() == False :
						listError.append( queueBufferErr.get().strip() )
					#dict_openie_config['logger'].info('STDIN (failed) >> ' + repr(strIn) )
					#dict_openie_config['logger'].info('STDOUT (failed) >> ' + repr(strConll2007) )
					raise Exception( 'DEP PARSE timeout waiting on stdout results (sent length too large?) : ' + '\n'.join( listError ) )

				# new output?
				if queueBufferOut.empty() == False :
					# get output
					strOutput = queueBufferOut.get()
					strConll2007 = strConll2007 + strOutput

					# clear the error buffer (to avoid spam if we are processing 1000's of sents)
					# stanford parser will output to stderr progress information not just error information
					# clearing stderr queue avoids it getting too large and going above the 1000 size and potentially causing problems (e.g. dropped entries)
					while queueBufferErr.empty() == False :
						queueBufferErr.get()

				else :
					# micro delay to allow CPU balancing
					time.sleep( 0.001 )
				
				# finished?
				# if there is no dep tree (e.g. tagged sent == "!\.") then the STDOUT is just '\r\n'
				# if there is a dep tree then the STDOUT will be '... dep tree in conll2007 format with several newlines ...\r\n\r\n'
				if (strConll2007 == '\r\n') or (strConll2007.endswith( '\r\n\r\n' )) :
					bFinished = True
					break

				# failure due to sentence being too long? return an empty string 
				if strConll2007 == '(())\r\n' :
					strConll2007 = ''
					bFinished = True
					dict_openie_config['logger'].info( 'DEP PARSE - sent too long (returning empty graph) : ' + repr(strIn) )
					break

				# alive? process will not be killed until later so if its dead this would indicate a failure of stanford parser
				nReturnCode = p.poll()
				if nReturnCode != None :
					listError = []
					while queueBufferErr.empty() == False :
						listError.append( queueBufferErr.get().strip() )
					raise Exception( 'DEP PARSE dead waiting on stdout results : ' + '\n'.join( listError ) )

			#dict_openie_config['logger'].info('STDOUT >> ' + repr(strConll2007) )

			# terminate dep_parse is we are at end of sents
			if nIndexSent == len(listInput)-1 :
				p.terminate()

			# parse conll2007 into a depGraph object
			# note: we ignore UserWarning (see top of code file) otherwise DependencyGraph will tell us if a dep graph has no nodes linked to the root node
			depGraph = nltk.parse.DependencyGraph(
								tree_str = strConll2007,
								top_relation_label = 'root',
								cell_separator = '\t' )
			listDepGraphTotal.append( depGraph )

		# collect error output (which will have loads of spam output even on a successful run)
		listError = []
		if queueBufferErr.empty() == False :
			while queueBufferErr.empty() == False :
				listError.append( queueBufferErr.get().strip() )

		# check we have enough dep graphs
		if len(list_tagged_sents) != len(listDepGraphTotal) :
			raise Exception( 'exec_dep_parser result is missing some sentences (parser failure?) : ' + str(len(list_tagged_sents)) + ' : ' + str(len(listDepGraphTotal)) + ' : STDERR = ' + '\n'.join( listError ) )

		# return a dep graph per sent
		return listDepGraphTotal

	except :
		# re-raise to propogate this exception
		dict_openie_config['logger'].exception('exec_dep_parser exception')
		raise

	finally : 
		# hard kill tagger process if its still open at the end to avoid widowed zombies on error
		if p != None :
			if p.poll() == None :
				'''
				if p.stdin != None :
					p.stdin.close()
				if p.stdout != None :
					p.stdout.close()
				if p.stderr != None :
					p.stderr.close()
				'''
				p.terminate()

		if queueBufferOut != None :
			while queueBufferOut.empty() == False :
				queueBufferOut.get()
		if queueBufferErr != None :
			while queueBufferErr.empty() == False :
				queueBufferErr.get()

def kill_dep_parser() :
	"""
	SIGTERM handler for exec_dep_parser() to ensure the stanford dep parser process is terminated.
	otherwise it will hang about forever waiting for more text to appear via STDIN
	"""
	if p_global != None :
		if p_global.poll() == None :
			p_global.terminate()


def read_pipe_stdout( pipe_handle, queue_buffer ) :
	"""
	internal DEP PARSE process pipe callback function

	:param file file_handle: pipe handle to DEP PARSE output
	:param Queue.Queue() queue_buffer: queue where pipe output can be stored
	"""

	try :
		while True :
			strLine = pipe_handle.readline().decode( 'utf-8' )
			if len(strLine) > 0 :
				queue_buffer.put( strLine )
	except :
		# read until pipe fails or is closed (and thus fails)
		return

def read_pipe_stderr( pipe_handle, queue_buffer ) :
	"""
	internal DEP PARSE process pipe callback function

	:param file file_handle: pipe handle to DEP PARSE errors
	:param Queue.Queue() queue_buffer: queue where pipe errors can be stored
	"""
	try :
		while True :
			strLine = pipe_handle.readline().decode( 'utf-8' )
			if len(strLine) > 0 :
				queue_buffer.put( strLine )
	except :
		# read until pipe fails or is closed (and thus fails)
		return


def serialize_b4_dep_graph_as_conll2007( root_dep_node = None, root_tokens_node = None, dict_openie_config = None ) :
	"""
	take stanford XML parsed bs4 soup nodes and return a serialized CoNLL 2007 formatted dependancy graph

	:param bs4.element.Tag root_dep_node: bs4 root node for basic-dependencies list of dep types
	:param bs4.element.Tag root_tokens_node: bs4 root node for token list
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: serialized CoNLL 2007 formatted dep graph, with row columns = {sent_index} \t {word} \t {lemma} \t {ctag} \t {tag} \t _ \t {head} \t {rel} \t _ \t _
	:rtype: unicode
	"""

	#
	# conll 2007 format [output]
	# {i}\t{word}\t{lemma}\t{ctag}\t{tag}\t_\t{head}\t{rel}\t_\t_\n
	#
	#1   Ze                ze                Pron  Pron  per|3|evofmv|nom                 2   su      _  _
	#2   had               heb               V     V     trans|ovt|1of2of3|ev             0   ROOT    _  _
	#3   met               met               Prep  Prep  voor                             8   mod     _  _
	#4   haar              haar              Pron  Pron  bez|3|ev|neut|attr               5   det     _  _
	#5   moeder            moeder            N     N     soort|ev|neut                    3   obj1    _  _
	#6   kunnen            kan               V     V     hulp|ott|1of2of3|mv              2   vc      _  _
	#7   gaan              ga                V     V     hulp|inf                         6   vc      _  _
	#8   winkelen          winkel            V     V     intrans|inf                      11  cnj     _  _
	#9   ,                 ,                 Punc  Punc  komma                            8   punct   _  _
	#10  zwemmen           zwem              V     V     intrans|inf                      11  cnj     _  _
	#11  of                of                Conj  Conj  neven                            7   vc      _  _
	#12  terrassen         terras            N     N     soort|mv|neut                    11  cnj     _  _
	#13  .                 .                 Punc  Punc  punt                             12  punct   _  _
	#
	# b4 xml dep graph [input]
	#
	#        <dependencies type="basic-dependencies">
	#          <dep type="root">
	#            <governor idx="0">ROOT</governor>
	#            <dependent idx="10">want</dependent>
	#          </dep>
	#          <dep type="case">
	#            <governor idx="4">time</governor>
	#            <dependent idx="1">At</dependent>
	#          </dep>
	#
	# b4 xml token list [input]
	#        <tokens>
	#          <token id="1">
	#            <word>At</word>
	#            <lemma>at</lemma>
	#            <CharacterOffsetBegin>0</CharacterOffsetBegin>
	#            <CharacterOffsetEnd>2</CharacterOffsetEnd>
	#            <POS>IN</POS>
	#            <NER>O</NER>
	#          </token>

	if not isinstance( root_dep_node, bs4.element.Tag ) :
		raise Exception( 'invalid root_dep_node' )
	if not isinstance( root_tokens_node, bs4.element.Tag ) :
		raise Exception( 'invalid root_tokens_node' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )


	dictDep = {}
	for nodeDep in root_dep_node.find_all( 'dep' ) :
		strType = nodeDep['type']

		nodeGovernor = nodeDep.find( 'governor' )
		strNodeHead = str( nodeGovernor.string )
		nIndexHead = int( nodeGovernor['idx'] )

		nodeDependent = nodeDep.find( 'dependent' )
		strNodeChild = str( nodeDependent.string )
		nIndexChild = int( nodeDependent['idx'] )

		dictDep[nIndexChild] = { 'rel' : strType, 'head' : nIndexHead }

	for nodeToken in root_tokens_node.find_all('token') :
		nIndexToken = int( nodeToken['id'] )
		if not nIndexToken in dictDep :
			raise Exception('token ' + repr(nIndexToken) + ' not in dep graph' )
		
		dictDep[nIndexToken]['word'] = str( nodeToken.find('word').string )
		dictDep[nIndexToken]['lemma'] = str( nodeToken.find('lemma').string )
		dictDep[nIndexToken]['tag'] = str( nodeToken.find('POS').string )

		# Stanford CoreNLP when serializing XML replaces word spaces with non-breaking space character /xa0 (!) this does not convert back to standard utf-8 properly when serialized, so replace with a true space
		dictDep[nIndexToken]['word'] = dictDep[nIndexToken]['word'].replace( '\xa0', ' ' )
		dictDep[nIndexToken]['lemma'] = dictDep[nIndexToken]['lemma'].replace( '\xa0', ' ' )
		dictDep[nIndexToken]['tag'] = dictDep[nIndexToken]['tag'].replace( '\xa0', ' ' )


	listLines = []
	listTokenSorted = sorted( dictDep.keys() )
	for nTokenIndex in listTokenSorted :
		# {i}\t{word}\t{lemma}\t{ctag}\t{tag}\t_\t{head}\t{rel}\t_\t_\n
		listColumns = []
		listColumns.append( str(nTokenIndex) )
		listColumns.append( soton_corenlppy.common_parse_lib.escape_token( dictDep[nTokenIndex]['word'] ) )
		listColumns.append( soton_corenlppy.common_parse_lib.escape_token( dictDep[nTokenIndex]['lemma'] ) )
		listColumns.append( soton_corenlppy.common_parse_lib.escape_token( dictDep[nTokenIndex]['tag'] ) )
		listColumns.append( soton_corenlppy.common_parse_lib.escape_token( dictDep[nTokenIndex]['tag'] ) )
		listColumns.append( '_' )
		listColumns.append( str( dictDep[nTokenIndex]['head'] ) )
		listColumns.append( dictDep[nTokenIndex]['rel'] )
		listColumns.append( '_' )
		listColumns.append( '_' )

		strLine = '\t'.join( listColumns )
		listLines.append( strLine )
	
	return '\n'.join( listLines )


def exec_stanford_corenlp( dict_text = None, work_dir = None, annotators = 'tokenize,ssplit,pos,depparse,lemma,ner', option_list = ['-tokenize.options', 'asciiQuotes=true,americanize=false', '-ssplit.eolonly', 'true'], num_processes = 6, dict_openie_config = None ) :
	"""
	run stanford CoreNLP to do one or more of the following:
		* Tokenization
		* POS tagging
		* Dependancy parsing
		* NER

	:param dict dict_text: set of sentences to process, where key is str(sent index)
	:param unicode work_dir: directory to work in (will serialize sentences for stanford to work on)
	:param unicode annotators: list of stanford coreNLP annotators to use (see https://stanfordnlp.github.io/CoreNLP/cmdline.html#inputting-serialized-files)
	:param list option_list: options to pass on command line for stanford coreNLP (see https://stanfordnlp.github.io/CoreNLP/cmdline.html#inputting-serialized-files)
	:param int num_processes: number of processors to use (will set thread options for stanford coreNLP)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: tuple of requested information e.g. ( dict_tokens, dict_pos, dict_dep_graph, dict_ner ). all dict use sent_index as the key.
	:rtype: tuple
	"""

	if not isinstance( dict_text, dict ) :
		raise Exception( 'invalid dict_text' )
	if not isinstance( work_dir, str ) :
		raise Exception( 'invalid work_dir' )
	if not isinstance( annotators, str ) :
		raise Exception( 'invalid annotators' )
	if not isinstance( option_list, list ) :
		raise Exception( 'invalid option_list' )
	if not isinstance( num_processes, int ) :
		raise Exception( 'invalid num_processes' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if not 'stanford_corenlp_dir' in dict_openie_config :
		raise Exception( 'stanford_corenlp_dir not specified in dict_openie_config' )
	if not 'corenlp_jars' in dict_openie_config :
		raise Exception( 'corenlp_jars not specified in dict_openie_config' )

	strStanfordDir = dict_openie_config['stanford_corenlp_dir']
	strJars = dict_openie_config['corenlp_jars']

	if os.path.exists( strStanfordDir ) == False :
		raise Exception( 'stanford corenlp dir does not exist : ' + repr(strStanfordDir) )

	dictTokens = {}
	dictPOS = {}
	dictDepGraph = {}
	dictNER = {}

	# serialize sentances to a plain text newline delimited corpus for stanford coreNLP
	strSentCorpus = work_dir + os.sep + 'sentences_for_stanford_corenlp.txt'
	writeHandle = codecs.open( strSentCorpus, 'w', 'utf-8', errors = 'replace' )
	listSentIndexSorted = sorted( list(dict_text.keys()), key=lambda entry: int( entry ), reverse=False )
	for nIndexDoc in listSentIndexSorted :
		strUTF8Text = dict_text[nIndexDoc]
		writeHandle.write( strUTF8Text + '\n' )
	writeHandle.close()

	#
	# run Stanford CoreNLP to do tokenization, POS, dep parse and NER all in one go. avoid sentence splitting (ssplit) so we are guarenteed num sent input = num sent output.
	# will generate .xml files for every processed corpus file
	#
	# cd C:\stanford-corenlp-full-2018-10-05
	# java -Xmx12g -cp stanford-corenlp-3.9.2.jar;stanford-corenlp-3.9.2-models.jar;* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,coref -coref.algorithm neural -outputDirectory C:\projects\datasets\20newsgroups -fileList C:\projects\datasets\20newsgroups\filelist.txt
	# java -Xmx12g -cp stanford-corenlp-3.9.2.jar;stanford-corenlp-3.9.2-models.jar;* edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner -outputDirectory C:\projects\datasets\20newsgroups -fileList C:\projects\datasets\20newsgroups\filelist.txt
	#

	listCmd = [
		'java',
		'-Xmx12g',
		'-cp',
		strJars,
		#'stanford-corenlp-3.9.2.jar;stanford-corenlp-3.9.2-models.jar;*',
		'edu.stanford.nlp.pipeline.StanfordCoreNLP',
		'-annotators',
		annotators ]
	listCmd.extend( option_list )
	listCmd.extend( [
		'depparse.nthreads',
		str(num_processes),
		'ner.nthreads',
		str(num_processes),
		'parse.nthreads',
		str(num_processes),
		'-outputDirectory',
		os.path.abspath( work_dir ),
		'-outputFormat',
		'xml',
		'-file',
		os.path.abspath( strSentCorpus )
		] )

	p = subprocess.Popen( listCmd, cwd=strStanfordDir, shell=False )
	if p.wait() != 0:
		raise Exception( 'Stanford NLP failed' )

	#
	# read in XML result from stanford and parse it
	#

	dict_openie_config['logger'].info( 'Parsing XML result from stanford CoreNLP' )

	strFile = work_dir + os.sep + 'sentences_for_stanford_corenlp.txt.xml'
	readHandle = codecs.open( strFile, 'r', 'utf-8', errors = 'replace' )
	listLines = readHandle.readlines()
	readHandle.close()

	# parse XML
	strXML = '\n'.join( listLines )
	soup = bs4.BeautifulSoup( markup = strXML, features = "xml", from_encoding="utf-8" )

	# example XML from Stanford NER
	#<root>
	#  <document>
	#    <docId>179106</docId>
	#    <sentences>
	#      <sentence id="1">
	#        <tokens>
	#          <token id="1">
	#            <word>Yesterday</word>
	#            <lemma>yesterday</lemma>
	#            <CharacterOffsetBegin>2</CharacterOffsetBegin>
	#            <CharacterOffsetEnd>11</CharacterOffsetEnd>
	#            <POS>NN</POS>
	#            <NER>DATE</NER>
	#            <NormalizedNER>OFFSET P-1D</NormalizedNER>
	#            <Timex tid="t1" type="DATE"/>
	#          </token>
	#        <dependencies type="basic-dependencies">
	#          <dep type="root">
	#            <governor idx="0">ROOT</governor>
	#            <dependent idx="10">want</dependent>
	#          </dep>
	#          <dep type="case">
	#            <governor idx="4">time</governor>
	#            <dependent idx="1">At</dependent>
	#          </dep>
	#          <dep type="det">
	#            <governor idx="4">time</governor>
	#            <dependent idx="2">the</dependent>
	#          </dep>
	#

	# loop on each sentence in this document (post)
	# loop on each token and compile a list of phrases (sequential NER words of same type)
	# note: the dict's use sent_index as doc_index, so there is only ever a single sent per value. this is to allow us later to use functions that allow multiple sents per doc (which we wont have here).

	nodeDoc = soup.find( 'document' )
	listSentNodes = nodeDoc.find_all( 'sentence' )
	for nodeSent in listSentNodes :
		# get sent index (0 offset) but it still needs to be a string
		nSentIndex = str( int( nodeSent['id'] ) - 1 )

		# get annotated tokens
		listTokenNodes = nodeSent.find_all( 'token' )

		# compile token, POS and NER lists for this sent
		listTokens = []
		listPOS = []
		listNER = []
		listCurrentNERTuples = []
		strCurrentNERType = None
		strNEROther = 'O'
		for nodeToken in listTokenNodes :
			# get token index (0 offset)
			nAddrToken = int( nodeToken['id'] ) - 1

			# Stanford CoreNLP when serializing XML replaces word spaces with non-breaking space character /xa0 (!)
			# and adds tabs for phrases like '87 1/2' to avoid using a space
			# this does not convert back to standard utf-8 properly when serialized, so replace with a true space
			strWord = str( nodeToken.find( 'word' ).string )
			strWord = strWord.replace( '\xa0', ' ' )
			strWord = strWord.replace( '\t', ' ' )
			strWord = soton_corenlppy.common_parse_lib.unescape_token( strWord )
			listTokens.append( strWord )

			if nodeToken.find( 'POS' ) != None :
				strPOS = str( nodeToken.find( 'POS' ).string )
				strPOS = strPOS.replace( '\xa0', ' ' )
				strPOS = strPOS.replace( '\t', ' ' )
				strPOS = soton_corenlppy.common_parse_lib.unescape_token( strPOS )
				listPOS.append( ( strWord, strPOS ) )

			if nodeToken.find( 'NER' ) != None :
				strNER = str( nodeToken.find( 'NER' ).string )
				strNER = strNER.replace( '\xa0', ' ' )
				strNER = strNER.replace( '\t', ' ' )
				strNER = soton_corenlppy.common_parse_lib.unescape_token( strNER )

				if len(listCurrentNERTuples) == 0 :
					if strNER != strNEROther :
						# start a new NER phrase
						listCurrentNERTuples.append( ( strWord, nAddrToken ) )
						strCurrentNERType = strNER
				else :
					if strNER == strCurrentNERType :
						# append to current NER phrase
						listCurrentNERTuples.append( ( strWord, nAddrToken ) )
					else :
						# add the complete (old) NER phrase and reset current
						listNER.append( ( strCurrentNERType, listCurrentNERTuples ) )
						listCurrentNERTuples = []
						strCurrentNERType = None

						if strNER != strNEROther :
							# start a new NER phrase
							listCurrentNERTuples.append( ( strWord, nAddrToken ) )
							strCurrentNERType = strNER

		if len(listCurrentNERTuples) > 0 :
			# add the complete (old) NER phrase and reset current
			listNER.append( ( strCurrentNERType, listCurrentNERTuples ) )

		dictTokens[ nSentIndex ] = listTokens

		if len(listPOS) > 0 :
			# make a tree of POS and add to dictSentTreesPOSPatterns
			# note: one sent per text line assumed (no sent tokenization)
			strPOSSerialized = soton_corenlppy.common_parse_lib.serialize_tagged_list(
				list_pos = listPOS,
				dict_common_config = dict_openie_config,
				serialization_style = 'tree' )

			strTreeSerialized = '(S ' + strPOSSerialized + ')'

			treeObj = soton_corenlppy.common_parse_lib.parse_serialized_tagged_tree(
				serialized_tree = strTreeSerialized,
				dict_common_config = dict_openie_config )

			dictPOS[ nSentIndex ] = treeObj

		if len(listNER) > 0 :
			dictNER[nSentIndex] = listNER

		# get basic-dependencies graph root node (if its there)
		listDepGraphSet = nodeSent.find_all( 'dependencies' )
		if listDepGraphSet != None :

			nodeDepGraphRoot = None
			for nodeDepGraph in listDepGraphSet :
				if nodeDepGraph['type'] == 'basic-dependencies' :
					nodeDepGraphRoot = nodeDepGraph
					break

			if nodeDepGraphRoot != None :
				# build a dep graph tree from the dep graph node data
				strDepGraphConll = serialize_b4_dep_graph_as_conll2007(
					root_dep_node = nodeDepGraphRoot,
					root_tokens_node = nodeSent.find( 'tokens' ),
					dict_openie_config = dict_openie_config,
					)

				# cells are seperated by tabs. dont use None as that defaults to whitespace, which fails when tokens have spaced in them.
				depGraph = nltk.parse.DependencyGraph(
									tree_str = strDepGraphConll,
									top_relation_label = 'root',
									cell_separator = '\t' )

				dictDepGraph [nSentIndex] = depGraph

	# compile the result tuple
	listResult = []
	if len(dictTokens) > 0 :
		listResult.append( dictTokens )
	if len(dictPOS) > 0 :
		listResult.append( dictPOS )
	if len(dictNER) > 0 :
		listResult.append( dictNER )
	if len(dictDepGraph) > 0 :
		listResult.append( dictDepGraph )
	
	# all done
	return tuple( listResult )


def prepare_tags_for_dependency_parse( list_tagged_sents = None, dict_custom_pos_mappings = {}, space_replacement_char = '_', dict_openie_config = None ) :
	"""
	prepare a list of tagged sents for dependency parsing. the stanford dependency parser gets confused if there are spaces in tokens (e.g. phrases) and does not understand custom POS tags.
	for following processing is applied to list_tagged_sents:
		* replace all token spaces with a replacement char
		* replace all custom POS tags (e.g. CITATION) with a replacement the taggger understands (e.g. PENN tags)

	:param list list_tagged_sents: reference argument providing a list of tagged sents that will be modified directly i.e. [ [ (token, pos), (token, pos), ... ], ... ]
	:param dict dict_custom_pos_mappings: dict of custom POS mappings e.g. { 'FIGURE' : 'CD', 'TABLE' : 'CD', ... }
	:param str space_replacement_char: replacement char for all token spaces
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()
	"""

	if not isinstance( list_tagged_sents, list ) :
		raise Exception( 'invalid list_tagged_sents' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( dict_custom_pos_mappings, dict ) :
		raise Exception( 'invalid dict_custom_pos_mappings' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	for nIndex1 in range(len(list_tagged_sents)) :
		for nIndex2 in range(len(list_tagged_sents[ nIndex1 ])) :

			tuplePOS = list_tagged_sents[ nIndex1 ][ nIndex2 ]

			# ensure there are no spaces in tokens (by replacing them with _ character)
			if ' ' in tuplePOS[0] :
				strReplacementToken = tuplePOS[0].replace(' ',space_replacement_char)
				tuplePOS = ( strReplacementToken,tuplePOS[1] )

			# replace any non-PENN tags with the closest PENN equivalent to get the best dependancy parse result
			if tuplePOS[1] in dict_custom_pos_mappings :
				strReplacementPOS = dict_custom_pos_mappings[ tuplePOS[1] ]
				tuplePOS = ( tuplePOS[0], strReplacementPOS )

			'''
			RELIC as no longer using NLTK to invoke the Stanford Parser (so NLTK encoding bug is not a problem)
			# handle NLTK bug (which was fixed late 2017 apparently)
			# https://github.com/nltk/nltk/issues/1424
			if u'à' in tuplePOS[0] :
				strReplacementToken = tuplePOS[0].replace( u'à',u'a' )
				tuplePOS = ( strReplacementToken,tuplePOS[1] )
			'''

			# update tagged entry
			list_tagged_sents[ nIndex1 ][ nIndex2 ] = tuplePOS

	# all done
	return

def serialize_dependency_graph( dep_graph, dict_openie_config ) :
	"""
	safely serialize a NLTK dependency graph using to_conll( style=4 ) including the special head '_' token for blank nodes.

	the dep_parser.tagged_parse_sents() function will return a Stanford Parser dep graph that has { 'address' = None } values for values such as punctuation (e.g. ',').
	this causes errors re-parsing a serialized graph as the NLTK parser does not allow a value for conll head of 'None'. instead it needs a special '_' value which Stanford Parser produces.

	:param nltk.parse.DependencyGraph dep_graph: dependency graph to serialize
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: serialized graph that can be read back in using nltk.parse.DependencyGraph( tree_str = str_serialized_graph, top_relation_label = 'root' )
	:rtype: unicode
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# make a copy of the nodes as we will change it later
	nodeCopy = copy.deepcopy( dep_graph.nodes )

	# fix node graph so it will serialize OK
	nLastAddr = None
	setMissingAddr = set([])
	listAddr = sorted( dep_graph.nodes.keys() )
	for nAddr in listAddr :
		# graphs read in by NLTK from conll (e.g. Stanford Parser) will have nodes that have a None head (serialized as '_') which gets parsed by NLTK as head = None
		# replace head = None with head = '_' so it serializes back to conll correctly
		if dep_graph.nodes[nAddr]['head'] == None :
			 dep_graph.nodes[nAddr].update( { 'head' : '_' } )

		# find any missing addresses
		if nLastAddr != None :
			for nMissingAddr in range( nLastAddr + 1, nAddr ) :
				setMissingAddr.add( nMissingAddr )
		nLastAddr = nAddr

	# graphs might not contain every address as some are removed by Stanford Parser (e.g. punctuation like ':')
	# this is a problem as the conll format assumes all nodes are output and the row == address (so missing rows gives the wrong address, which in turn causes bad trees)
	# add in extra nodes for all these missing nodes just for serialization purposes
	for nAddr in setMissingAddr :
		dep_graph.nodes[nAddr].update( { 'address' : nAddr, 'head' : '_' } )

	# serialize tree with missing values filled in (will use tab delimiters)
	strSerialized = dep_graph.to_conll( style=4 )

	# change dep graph address = None nodes back to head = None
	dep_graph.nodes = nodeCopy

	# all done
	return strSerialized

def get_dep_tree_addresses( dep_graph = None, branch_address = None, list_address_set = None, dict_openie_config = None ) :
	"""
	return a list of all address nodes under a branch node in a dep graph

	:param nltk.parse.DependencyGraph dep_graph: dependency graph to process
	:param int branch_address: address of branch to process
	:param list list_address_set: result list of addresses (list will be populated by function)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( branch_address, int ) :
		raise Exception( 'invalid branch_address' )
	if not isinstance( list_address_set, list ) :
		raise Exception( 'invalid list_address_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if branch_address in dep_graph.nodes :

		# add branch address to list
		if not branch_address in list_address_set :
			list_address_set.append( branch_address )

		# process all children
		for strDep in dep_graph.nodes[branch_address]['deps'] :
			for nAddressChild in dep_graph.nodes[branch_address]['deps'][ strDep ] :
				if not nAddressChild in list_address_set :

					# recurse for child branch
					get_dep_tree_addresses(
						dep_graph = dep_graph,
						branch_address = nAddressChild,
						list_address_set = list_address_set,
						dict_openie_config = dict_openie_config )

def parse_sent_trees_batch( dict_doc_sent_trees = None, dep_parser = None, dict_custom_pos_mappings = {}, space_replacement_char = '_', max_processes = 4, dict_openie_config = None ) :
	"""
	dependency parse a batch of documents, each with a list of Stanford POS tagged sents from soton_corenlppy.common_parse_lib.create_sent_trees()
	use multiprocess spawning to maximize the CPU usage as this is a slow process that is CPU intensive.

	:param dict dict_doc_sent_trees: dict of documents { docID : list of sent trees }
	:param list dep_parser: list of commands for popen() from get_dependency_parser()
	:param dict dict_custom_pos_mappings: dict of custom POS mappings e.g. { 'FIGURE' : 'CD', 'TABLE' : 'CD', ... }
	:param str space_replacement_char: replacement char for all token spaces
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: dict of documents { docID : list of nltk.parse.DependencyGraph }
	:rtype: dict
	"""

	if not isinstance( dict_doc_sent_trees, dict ) :
		raise Exception( 'invalid dict_doc_sent_trees' )
	if not isinstance( dep_parser, list ) :
		raise Exception( 'invalid dep_parser' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( dict_custom_pos_mappings, dict ) :
		raise Exception( 'invalid dict_custom_pos_mappings' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )
		listQueueResultsPending.append( 0 )

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in dict_doc_sent_trees:

		# add to queue a the list of document sent trees to process
		listSentTrees = dict_doc_sent_trees[strDocumentID]
		#listQueue[nProcess][0].put( ( strDocumentID, listSentTrees ) )
		listQueueInput[nProcess].append( ( strDocumentID, listSentTrees ) )
		listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] + 1

		# round robin assignment to queues
		nProcess = nProcess + 1
		if nProcess >= max_processes :
			nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.copy( dict_openie_config )
	dictConfigCopy['logger'] = None

	# setup a process pool
	listProcesses = []
	for nProcess in range(max_processes) :
		dict_openie_config['logger'].info( 'starting process ' + str(nProcess) + ' [dep parse]' )

		processWorker = multiprocessing.Process(
			target = parse_sent_trees_worker,
			args = (
				listQueue[nProcess],
				dep_parser,
				dict_custom_pos_mappings,
				space_replacement_char,
				1,
				nProcess,
				dictConfigCopy )
			)
		listProcesses.append( processWorker )

	# write number of documents to expect
	for nProcess in range(max_processes) :
		listQueue[nProcess][0].put( len(listQueueInput[nProcess]) )

	for nProcess in range(max_processes) :
		listProcesses[nProcess].start()

	# write all the input (sync to ensure in queues are limited in size)
	bFinishedInput = False
	while bFinishedInput == False :

		for nProcess in range(max_processes) :

			while len(listQueueInput[nProcess]) > 0 :

				# check for input queue overload (which can cause multiprocess Queue handling errors and lost results).
				# pause until the queue is smaller if this is the case.
				if listQueue[nProcess][0].qsize() > 100 :
					break
				
				# write entry and remove from list
				listQueue[nProcess][0].put( listQueueInput[nProcess].pop(0) )

		bFinishedInput = True
		for nProcess in range(max_processes) :
			if len(listQueueInput[nProcess]) > 0 :
				# input data left so pause and try to upload again
				bFinishedInput = False
				time.sleep(1)

	dict_openie_config['logger'].info( 'documents written OK ' + str(len(dict_doc_sent_trees)) + ' [dep parse]' )

	# read results
	try :
		listOutputResults = {}

		# download the pattern list result from each process queue (only one per process)
		# note: do not use blocking queues or thread joins (just an error queue) to avoid issues with queues closing but still being written to (if thread error occurs)
		#       e.g. IOError: [Errno 232] The pipe is being closed
		bFinished = False
		bError = False
		while (bFinished == False) and (bError == False) :

			bPause = True

			# check each process and try to get (a) errors (b) 1 result each
			for nProcess in range(max_processes) :

				# does this process still have work to do?
				if listQueueResultsPending[nProcess] > 0 :

					# non-blocking attempt to get errors
					try :
						strErrorMsg = listQueue[nProcess][2].get( False )

						dict_openie_config['logger'].info( '\tprocess ' + str(nProcess) + ' [dep parse] failure > ' + strErrorMsg )

						# expect no more results from this process
						listQueueResultsPending[nProcess] = 0

						# flush input buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][0].empty() == False :
							listQueue[nProcess][0].get()

						# flush output buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][1].empty() == False :
							listQueue[nProcess][1].get()

						bError = True

						break
					except queue.Empty :
						pass


					# non-blocking attempt to get a result
					try :
						# get set of serialized graphs for a document
						( strDocumentID, listSentTrees ) = listQueue[nProcess][1].get( False )

						#dict_openie_config['logger'].info( 'URI result (' + str(nProcess) + ') = ' + strDocumentID )

						# make NLTK dep graph objects from the serialized form
						for nGraph in range(len(listSentTrees)) :
							listSentTrees[nGraph] = nltk.parse.DependencyGraph(
								tree_str = listSentTrees[nGraph],
								top_relation_label = 'root',
								cell_separator = '\t' )

						# add to final result
						listOutputResults[ strDocumentID ] = listSentTrees

						listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] - 1
						bPause = False

						#dict_openie_config['logger'].info( 'pending (' + str(nProcess) + ') = ' + str(listQueueResultsPending[nProcess]) )

					except queue.Empty :
						pass

			# more results?
			bFinished = True
			for nProcess in range(max_processes) :
				if listQueueResultsPending[nProcess] > 0 :
					bFinished = False

			# pause for 1 second if we did not get any results to give workers a change to make them
			if (bFinished == False) and (bPause == True) :
				time.sleep(1)

		# errors?
		if bError == True :
			raise Exception( 'errors processing request (see log)' )

		dict_openie_config['logger'].info( 'results aggregated OK [dep parse]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input queue before
		time.sleep(2)

		# do cleanup
		dict_openie_config['logger'].info( 'tidying up from worker processes [dep parse]' )
		( exctype, value ) = sys.exc_info()[:2]
		if exctype != None :
			dict_common_config['logger'].info( 'Exception (will continue) : ' + repr( ( exctype, value ) ) )

		for nProcess in range(max_processes) :
			# ensure all processes are terminates
			if listProcesses[nProcess] != None :
				if listProcesses[nProcess].is_alive() == True :
					listProcesses[nProcess].terminate()

			# ensure all queues for this thread are empty and closed
			for nQueue in range(len(listQueue[nProcess])) :
				while listQueue[nProcess][nQueue].empty() == False :
					listQueue[nProcess][nQueue].get()
				#listQueue[nProcess][nQueue].close()

		dict_openie_config['logger'].info( 'tidy up complete [dep parse]' )

	# all done
	return listOutputResults

def parse_sent_trees_worker( tuple_queue = None, dep_parser = None, dict_custom_pos_mappings = {}, space_replacement_char = '_', pause_on_start = 0, process_id = 0, dict_openie_config = None ) :
	"""
	worker thread for comp_sem_lib.parse_sent_trees_batch()

	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). the queueIn has ( docID, list_sent_trees ). queueOut has ( docID, list_serialized_graphs )
	:param list dep_parser: list of commands for popen() from get_dependency_parser()
	:param dict dict_custom_pos_mappings: dict of custom POS mappings e.g. { 'FIGURE' : 'CD', 'TABLE' : 'CD', ... }
	:param str space_replacement_char: replacement char for all token spaces
	:param int pause_on_start: number of seconds to pause to allow other workers to start
	:param int process_id: process ID
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )
	if not isinstance( dep_parser, list ) :
		raise Exception( 'invalid dep_parser' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( dict_custom_pos_mappings, dict ) :
		raise Exception( 'invalid dict_custom_pos_mappings' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.copy( dict_openie_config )

		logger = logging.getLogger( __name__ )
		if len(logger.handlers) == 0 :
			hdlr = logging.StreamHandler( stream = sys.stdout )
			LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
			fmt = logging.Formatter( fmt = LOG_FORMAT )
			hdlr.setFormatter( fmt )
			logger.addHandler( hdlr )
		logger.setLevel( logging.INFO )

		dictConfigCopy['logger'] = logger

		# pause 1 second to allow all other worker threads to start properly (otherwise startup might be delayed as CPU is grabbed by first workers)
		time.sleep( pause_on_start )
		#logger.info( 'worker process started (' + str(process_id) + ') [dep parse]' )

		# read number of documents
		nDocumentMax = tuple_queue[0].get()

		logger.info( 'worker process started (' + str(process_id) + ') = ' + str(nDocumentMax) + ' docs [dep parse]' )

		# read all input data to process
		listCorpusDepGraphs = []
		listDocMeta = []
		for nDocument in range(nDocumentMax) :

			# get tokens to POS tag
			( strDocumentID, listSentTrees ) = tuple_queue[0].get()

			# remember the start and end index in corpus token set so we can create the document dict later
			listDocMeta.append( ( strDocumentID, len(listCorpusDepGraphs), len(listSentTrees) ) )
			listCorpusDepGraphs.extend( listSentTrees )

		# create dep graphs for all sent trees in one large batch.
		# this avoids creating loads of subprocesses, which would eventually run out of file handles for them and generate "OSError: [Errno 24] Too many open files" errors
		#logger.info( 'worker process (' + str(process_id) + ') starting dep parse' )

		listDepGraphs = parse_sent_trees(
			list_sent_trees = listCorpusDepGraphs,
			dep_parser = dep_parser,
			dict_custom_pos_mappings = dict_custom_pos_mappings,
			space_replacement_char = space_replacement_char,
			dict_openie_config = dictConfigCopy )

		#logger.info( 'worker process (' + str(process_id) + ') finished dep parse' )

		for nDocument in range(nDocumentMax) :

			# get sent trees for a document
			strDocumentID = listDocMeta[nDocument][0]

			# serialize graphs as dep graph contains function pointers which cannot be pickled on a Queue
			listSerializedGraphs = []
			for nGraph in range( listDocMeta[nDocument][1], listDocMeta[nDocument][1] + listDocMeta[nDocument][2] ) :
				strSerializedGraph = serialize_dependency_graph(
					dep_graph = listDepGraphs[nGraph],
					dict_openie_config = dictConfigCopy)
				listSerializedGraphs.append( strSerializedGraph )

			# add result to output queue
			tuple_queue[1].put( ( strDocumentID, listSerializedGraphs ) )

			# micro pause to allow CPU balancing if run in batch mode
			time.sleep( 0.001 )

			# check for output queue overload (which can cause multiprocess Queue handling errors and lost results).
			# pause until the queue is smaller if this is the case.
			while tuple_queue[1].qsize() > 100 :
				time.sleep( 1 )

		logger.info( 'process ended (' + str(process_id) + ') [dep parse]' )

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'parse_sent_trees_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )


def parse_sent_trees( list_sent_trees = None, dep_parser = None, dict_custom_pos_mappings = {}, space_replacement_char = '_', dict_openie_config = None ) :
	"""
	parse a list of sentence trees from soton_corenlppy.common_parse_lib.create_sent_trees() and return a list of dep graph objects

	:param list list_sent_trees: list of stanford POS tagged sent trees
	:param list dep_parser: list of commands for popen() from get_dependency_parser()
	:param dict dict_custom_pos_mappings: dict of custom POS mappings e.g. { 'FIGURE' : 'CD', 'TABLE' : 'CD', ... }
	:param str space_replacement_char: replacement char for all token spaces
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of nltk.parse.DependencyGraph
	:rtype: list
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'invalid list_sent_trees' )
	if not isinstance( dep_parser, list ) :
		raise Exception( 'invalid dep_parser' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( dict_custom_pos_mappings, dict ) :
		raise Exception( 'invalid dict_custom_pos_mappings' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# flatten the sents (POS pattern phrases prior to ReVerb annotations) to become a list of POS tagged phrases. this is needed as the dependancy parser works on a tagged list of tokens i.e. not a sent tree
	listTaggedSentsDepParse = []
	for nIndexSent in range(len(list_sent_trees)) :
		treeFlat = soton_corenlppy.common_parse_lib.flattern_sent(
			tree_sent = list_sent_trees[nIndexSent],
			dict_common_config = dict_openie_config )
		listTaggedSentsDepParse.append( treeFlat.pos() )

	# replace any non-Stanford POS tags with an equivilent so the dependency parse is as good as it can be, and replace spaces with '_' in tokens (if phrases are allowed) as dep parser expects unigram tokens
	prepare_tags_for_dependency_parse(
		list_tagged_sents = listTaggedSentsDepParse,
		dict_custom_pos_mappings = dict_custom_pos_mappings,
		dict_openie_config = dict_openie_config )

	#sentDepGraphs = dep_parser.tagged_parse_sents( sentences = listTaggedSentsDepParse )
	sentDepGraphs = exec_dep_parser(
		list_tagged_sents = listTaggedSentsDepParse,
		dep_parser_cmd = dep_parser,
		dict_openie_config = dict_openie_config,
		sigterm_handler = True )

	# return dep graph objects
	return sentDepGraphs

	'''
	listSentGraphs = []
	for depGraphIter in sentDepGraphs :
		# tagged_parse_sents() returns an iterator for some reason so just get graph and break
		for depObj in depGraphIter :
			listSentGraphs.append( depObj )

			# draw graph for presentations (disable normally). will block wait until window is closed
			# depObj.tree().draw()

			break

	# all done
	return listSentGraphs
	'''


def generate_open_extraction_templates_batch( seed_tuples = None, var_candidates = None, dict_document_sent_graphs = {}, dict_seed_to_template_mappings = {}, dict_context_dep_types = [], max_processes = 4, longest_dep_path = 32, longest_inter_target_walk = 2, max_seed_variants = 128, allow_seed_subsumption = True, avoid_dep_set = set([]), dict_openie_config = None ) :
	"""
	generate a set of open pattern templates based on a training corpus (dependency parsed into graphs) and seed_tuples with known 'high quality' argument and relation groups.
	use multiprocess spawning to maximize the CPU usage as this is a slow process that is CPU intensive.

	see comp_sem_lib.generate_open_extraction_templates() for details

	:param list seed_tuples: list (or set) of seed_tuples from comp_sem_lib.generate_seed_tuples()
	:param dict var_candidates: dict of seed tuple variable types, each value containing a list of phrase tuples that are var candidates, from comp_sem_lib.generate_seed_tuples()
	:param dict dict_document_sent_graphs: dict of document ID keys, each value being a list of nltk.parse.DependencyGraph objects for a corpus of sents
	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probably meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of open template extraction strings ready for parsing using comp_sem_lib.parse_extraction_pattern()
	:rtype: list
	"""

	if not isinstance( seed_tuples, (list,set) ) :
		raise Exception( 'invalid seed_tuples' )
	if not isinstance( var_candidates, dict ) :
		raise Exception( 'invalid var_candidates' )
	if not isinstance( dict_document_sent_graphs, dict ) :
		raise Exception( 'invalid dict_document_sent_graphs' )
	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )

		# generate creates a single output (set of templates) given N input graphs
		listQueueResultsPending.append( 1 )

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in dict_document_sent_graphs:
		# add to queue the list of sent graphs for this document
		listGraph = dict_document_sent_graphs[strDocumentID]
		for depObj in listGraph :

			# dict_openie_config['logger'].info( 'GRAPH1 = ' + depObj.to_dot() )

			strSerializedGraph = serialize_dependency_graph( dep_graph = depObj, dict_openie_config = dict_openie_config )
			#listQueue[nProcess][0].put( strSerializedGraph )
			listQueueInput[nProcess].append( strSerializedGraph )

			#depObj2 = nltk.parse.DependencyGraph( tree_str = strSerializedGraph, top_relation_label = 'root' )
			#dict_openie_config['logger'].info( 'GRAPH3 = ' + depObj2.to_dot() )

			# round robin assignment to queues
			nProcess = nProcess + 1
			if nProcess >= max_processes :
				nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.copy( dict_openie_config )
	dictConfigCopy['logger'] = None

	# setup a process pool as the template generation is very CPU intensive so we need to use all cores on a machine to speed it up
	listProcesses = []
	for nProcess in range(max_processes) :
		dict_openie_config['logger'].info( 'starting process ' + str(nProcess) + ' with ' + str( len( listQueueInput[nProcess] ) ) + ' sent graphs [generate]' )

		processWorker = multiprocessing.Process(
			target = generate_open_extraction_templates_worker,
			args = (
				seed_tuples,
				var_candidates,
				listQueue[nProcess],
				dict_seed_to_template_mappings,
				dict_context_dep_types,
				longest_dep_path,
				longest_inter_target_walk,
				max_seed_variants,
				allow_seed_subsumption,
				avoid_dep_set,
				1,
				nProcess,
				dictConfigCopy )
			)
		listProcesses.append( processWorker )

	# write number of documents to expect
	for nProcess in range(max_processes) :
		listQueue[nProcess][0].put( len(listQueueInput[nProcess]) )

	for nProcess in range(max_processes) :
		listProcesses[nProcess].start()

	# write all the input (sync to ensure in queues are limited in size)
	bFinishedInput = False
	while bFinishedInput == False :

		for nProcess in range(max_processes) :

			while len(listQueueInput[nProcess]) > 0 :

				# check for input queue overload (which can cause multiprocess Queue handling errors and lost results).
				# pause until the queue is smaller if this is the case.
				if listQueue[nProcess][0].qsize() > 100 :
					break
				
				# write entry and remove from list
				listQueue[nProcess][0].put( listQueueInput[nProcess].pop(0) )

		bFinishedInput = True
		for nProcess in range(max_processes) :
			if len(listQueueInput[nProcess]) > 0 :
				# input data left so pause and try to upload again
				bFinishedInput = False
				time.sleep(1)

	dict_openie_config['logger'].info( 'documents written OK [generate]' )

	try :
		listOutputResults = []

		# download the pattern list result from each process queue (only one per process)
		# note: do not use blocking queues or thread joins (just an error queue) to avoid issues with queues closing but still being written to (if thread error occurs)
		#       e.g. IOError: [Errno 232] The pipe is being closed
		bFinished = False
		bError = False
		while (bFinished == False) and (bError == False) :

			bPause = True

			# check each process and try to get (a) errors (b) 1 result each
			for nProcess in range(max_processes) :

				# does this process still have work to do?
				if listQueueResultsPending[nProcess] > 0 :

					# non-blocking attempt to get errors
					try :
						strErrorMsg = listQueue[nProcess][2].get( False )

						dict_openie_config['logger'].info( '\tprocess ' + str(nProcess) + ' [generate] failure > ' + strErrorMsg )

						# expect no more results from this process
						listQueueResultsPending[nProcess] = 0

						# flush input buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][0].empty() == False :
							listQueue[nProcess][0].get()

						# flush output buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][1].empty() == False :
							listQueue[nProcess][1].get()

						bError = True

						break
					except queue.Empty :
						pass


					# non-blocking attempt to get a result
					try :
						listMatches = listQueue[nProcess][1].get( False )
						listOutputResults.extend( listMatches )

						listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] - 1
						bPause = False

					except queue.Empty :
						pass

			# more results?
			bFinished = True
			for nProcess in range(max_processes) :
				if listQueueResultsPending[nProcess] > 0 :
					bFinished = False

			# pause for 1 second if we did not get any results to give workers a change to make them
			if (bFinished == False) and (bPause == True) :
				time.sleep(1)

		# errors?
		if bError == True :
			raise Exception( 'errors processing request (see log)' )

		dict_openie_config['logger'].info( 'results aggregated OK [generate]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input quete before
		time.sleep(2)

		# do cleanup
		dict_openie_config['logger'].info( 'tidying up from worker processes [generate]' )
		( exctype, value ) = sys.exc_info()[:2]
		if exctype != None :
			dict_common_config['logger'].info( 'Exception (will continue) : ' + repr( ( exctype, value ) ) )

		for nProcess in range(max_processes) :
			# ensure all processes are terminates
			if listProcesses[nProcess] != None :
				if listProcesses[nProcess].is_alive() == True :
					listProcesses[nProcess].terminate()

			# ensure all queues for this thread are empty and closed
			for nQueue in range(len(listQueue[nProcess])) :
				while listQueue[nProcess][nQueue].empty() == False :
					listQueue[nProcess][nQueue].get()
				#listQueue[nProcess][nQueue].close()

		dict_openie_config['logger'].info( 'tidy up complete [generate]' )

	# all done
	return listOutputResults

def generate_open_extraction_templates_worker( seed_tuples = None, var_candidates = None, tuple_queue = None, dict_seed_to_template_mappings = {}, dict_context_dep_types = [], longest_dep_path = 32, longest_inter_target_walk = 2, max_seed_variants = 128, allow_seed_subsumption = True, avoid_dep_set = set([]), pause_on_start = 0, process_id = 0, dict_openie_config = None ) :
	"""
	worker thread for comp_sem_lib.generate_open_extraction_templates_batch()

	:param list seed_tuples: list (or set) of seed_tuples from comp_sem_lib.generate_seed_tuples()
	:param dict var_candidates: dict of seed tuple variable types, each containing a list of phrases that are var candidates, from comp_sem_lib.generate_seed_tuples()
	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). the queueIn has serialized nltk.parse.DependencyGraph objects. queueOut has list of template patterns for this graph.
	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probably meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param int pause_on_start: number of seconds to delay thread startup before CPU intensive work begins (to allow other workers to startup also)
	:param int process_id: process ID for logging
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( seed_tuples, (list,set) ) :
		raise Exception( 'invalid seed_tuples' )
	if not isinstance( var_candidates, dict ) :
		raise Exception( 'invalid var_candidates' )
	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )
	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.copy( dict_openie_config )

		logger = logging.getLogger( __name__ )
		if len(logger.handlers) == 0 :
			hdlr = logging.StreamHandler( stream = sys.stdout )
			LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
			fmt = logging.Formatter( fmt = LOG_FORMAT )
			hdlr.setFormatter( fmt )
			logger.addHandler( hdlr )
		logger.setLevel( logging.INFO )

		dictConfigCopy['logger'] = logger

		# pause 1 second to allow all other worker threads to start properly (otherwise startup might be delayed as CPU is grabbed by first workers)
		time.sleep( pause_on_start )

		# read number of documents
		nDocumentMax = tuple_queue[0].get()

		logger.info( 'worker process started (' + str(process_id) + ') = ' + str(nDocumentMax) + ' docs [generate]' )

		# read all input data to process
		listSerializedGraph = []
		for nDocument in range(nDocumentMax) :

			# get serialized graph
			strSerializedGraph = tuple_queue[0].get()
			listSerializedGraph.append( strSerializedGraph )

		# loop on all input graphs, re-create the dep graph list and generate templates
		listPatternsTotal = []
		for strSerializedGraph in listSerializedGraph :

			# make a NLTK dep graph object
			depObj = nltk.parse.DependencyGraph( tree_str = strSerializedGraph, top_relation_label = 'root', cell_separator = '\t' )

			# generate templates for this sent
			# do then one by one as its just as efficient as batch and allows micro pauses
			listPatterns = generate_open_extraction_templates(
				seed_tuples = seed_tuples,
				var_candidates = var_candidates,
				corpus_sent_graphs = [ depObj ],
				dict_seed_to_template_mappings = dict_seed_to_template_mappings,
				dict_context_dep_types = dict_context_dep_types,
				longest_dep_path = longest_dep_path,
				longest_inter_target_walk = longest_inter_target_walk,
				max_seed_variants = max_seed_variants,
				allow_seed_subsumption = allow_seed_subsumption,
				avoid_dep_set = avoid_dep_set,
				dict_openie_config = dictConfigCopy )

			listPatternsTotal.extend( listPatterns )

			# micro pause to allow CPU balancing if run in batch mode
			time.sleep( 0.001 )

		# add result to output queue (only 1 so no need for queue size checks)
		tuple_queue[1].put( listPatternsTotal )

		logger.info( 'process ended (' + str(process_id) + ') [generate]' )

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'generate_open_extraction_templates_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )


def generate_open_extraction_templates( seed_tuples = None, var_candidates = None, corpus_sent_graphs = None, dict_seed_to_template_mappings = {}, dict_context_dep_types = [], longest_dep_path = 32, longest_inter_target_walk = 2, max_seed_variants = 128, allow_seed_subsumption = True, avoid_dep_set = set([]), space_replacement_char = '_', dict_openie_config = None ) :
	"""
	generate a set of open pattern templates based on a training corpus (dependency parsed into graphs) and seed_tuples with known 'high quality' argument and relation groups.

	for each seed_tuple generate specific open pattern templates:
		* for each sent, get all possible combinations of seed tokens where the seed tokens appear in the same sequential order as the seed tuple
		* remove any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch). subsumed seeds will be includes later when branches are collapsed.
		* for each combination of seed tokens, compute the shortest dependancy graph path which contains all seed tuple words
		* reject dependancy path lengths > threshold, as too verbose and unlikely to express the true original tuple's meaning
		* walk the dependancy path and generate a very specific open pattern templates (lexical and pos constraints)

	:param list seed_tuples: list (or set) of seed_tuples from comp_sem_lib.generate_seed_tuples()
	:param dict var_candidates: dict of seed tuple variable types, each containing a list of phrases that are var candidates, from comp_sem_lib.generate_seed_tuples()
	:param list corpus_sent_graphs: list of nltk.parse.DependencyGraph objects for a corpus of sents
	:param dict dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg'). template type must not contain a '_' character.
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probably meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param str space_replacement_char: replacement char for all token spaces as dep graph cannot have a space. should be same as prepare_tags_for_dependency_parse()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of open template extraction strings ready for parsing using comp_sem_lib.parse_extraction_pattern()
	:rtype: list
	"""

	if not isinstance( seed_tuples, (list,set) ) :
		raise Exception( 'invalid seed_tuples' )
	if not isinstance( var_candidates, dict ) :
		raise Exception( 'invalid var_candidates' )
	if not isinstance( corpus_sent_graphs, list ) :
		raise Exception( 'invalid corpus_sent_graphs' )
	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# generate specific patterns from seed tuples
	# seed_tuples = [ ( ('ARGUMENT','John'), ('RELATION','come','from'), ('ARGUMENT','Paris') ), ... ]
	listPatterns = []
	for tupleSeed in seed_tuples :
		# debug
		#if tupleSeed != ( (u'ARGUMENT', u'whether', u'they'), (u'RELATION', u'plan', u'to'), (u'RELATION', u'continue', u'providing'), (u'ARGUMENT', u'health', u'insurance'), (u'ARGUMENT', u'to', u'Medicare', u'recipients'), (u'ARGUMENT', u'next', u'year') ) :
		#	continue
		#if tupleSeed != ((u'SUBJECT', u'Rim', u'body', u'and', u'handle', u'sherd', u'(rejoined from four fragments)'), (u'ATTR', u'of'), (u'OBJECT', u'Vroulian', u'pottery', u'shallow', u'cup')) :
		#	continue
		#dict_openie_config['logger'].info( 'SEED UNDER TEST = ' + repr(tupleSeed) )

		for nSentIndex in range(len(corpus_sent_graphs)) :
		#for nSentIndex in range(1,2) :

			depGraph = corpus_sent_graphs[ nSentIndex ]
			#dict_openie_config['logger'].info( 'GRAPH = ' + repr(unicode(depGraph.tree())) )
			#dict_openie_config['logger'].info( 'GRAPH = ' + repr(depGraph.to_dot()) )
			#dict_openie_config['logger'].info( 'SENT = ' + repr(nSentIndex) )

			# compute a complete list of the addresses under each node. this is important to guide the graph walk later
			dictNodeAddrSet = construct_node_index(
				dep_graph = depGraph,
				dict_openie_config = dict_openie_config )

			listSortedAddr = sorted( depGraph.nodes.keys() )

			# debug
			#for nTest in listSortedAddr :
			#	dict_openie_config['logger'].info( '\t' + repr(depGraph.nodes[ nTest ]) )

			listSeedOptions = []

			# loop on seeds
			bNoSeedMatch = False
			for nSeedIndex in range(len(tupleSeed)) :
				dictOptionsNew = {}

				# get previous option (or a dummy one if starting at index 1 just after root)
				if nSeedIndex > 0 :
					dictOptionsPrev = listSeedOptions[-1]
				else :
					dictOptionsPrev = { -1 : { 'next_addr' : 1 } }

				# use the previous options next address as a starting point for this seen token
				nCount = 0
				for nCountPrev in dictOptionsPrev :
					dictOption = dictOptionsPrev[nCountPrev]

					# check for start and end annotations
					if tupleSeed[nSeedIndex][0] == 'START' :
						if dictOption['next_addr'] == 1 :
							# START found and it really is the start address, so move to next seed index but dont add any address to listSeedGraphAddress
							dictOptionsNew[nCount] = {
									'next_addr' : 1,
									'linked_seed' : nCountPrev
								}
							nCount = nCount + 1

						# dont try to match START
						continue

					elif tupleSeed[nSeedIndex][0] == 'END' :
						if dictOption['next_addr'] == len(listSortedAddr) :
							# END found and it really is the last address, so move to next seed index but dont add any address to listSeedGraphAddress
							dictOptionsNew[nCount] = {
									'next_addr' : len(listSortedAddr),
									'linked_seed' : nCountPrev
								}
							nCount = nCount + 1

						# dont try to match END
						continue

					# try every starting address from the previous seed 'next_addr' until the end.
					# this is to find cases where there are more than one valid seed match in a sent
					# e.g. he was going to the shop then going to the bar => {he, going, shop}, {he, going, bar} ==> dont stop at first 'going' token match!
					nOldCount = nCount
					for nAddrSearch in range( dictOption['next_addr'], len(listSortedAddr) ) :
						# addr index to test for matching
						nAddrIndex = nAddrSearch
						#dict_openie_config['logger'].info( 'T1.0 = ' + repr(nAddrIndex) )

						# process each seed token on its own and add each address separately
						# this will generate the worst option (every address has an explicit target) - but we check for subsuming branches later
						# enforce that tokens within a single seed appear sequentially by address order, to avoid matching contiguous phrases with rubbish in the middle
						listSeedEntry = []
						setVarNames = set([])
						bAbort = False
						for nIndexSeedToken in range( 1, len( tupleSeed[nSeedIndex] ) ) :
							strSeedToken = tupleSeed[nSeedIndex][nIndexSeedToken]

							# dep graph tokens cannot have spaces. therefore we need to replace spaces with the replacement chart used in prepare_tags_for_dependency_parse() so we can string match later
							strSeedToken = strSeedToken.replace(' ',space_replacement_char)
							#dict_openie_config['logger'].info( 'T1.1 = ' + repr(strSeedToken) )

							bFound = False
							while bFound == False :

								if nAddrIndex >= len(listSortedAddr) :
									bAbort = True
									break

								nAddress = listSortedAddr[nAddrIndex]

								# avoid None addresses (e.g. punctuation symbols like ':')
								if depGraph.nodes[ nAddress ]['address'] == None :
									nAddrIndex = nAddrIndex + 1
									continue

								# ignore nodes that have a head of a missing node
								if depGraph.nodes[ nAddress ]['head'] == None :
									nAddrIndex = nAddrIndex + 1
									continue

								#dict_openie_config['logger'].info( 'checking ' + repr( (nAddrIndex, nAddress) ) )
								
								# match? if so add to seed address list and move to next token
								if depGraph.nodes[ nAddress ]['word'] == strSeedToken :

									#dict_openie_config['logger'].info( 'word found' )

									# if this is not the first token in a seed then check its appearing sequentially next to the previous token
									# allowing for the fact that dep graph addresses might be skipped if they have no head or address (e.g. ,)
									if nIndexSeedToken > 1 :
										nPreviousAddr = listSeedEntry[-1][2]
										if nAddrIndexLastValid != nPreviousAddr :
											# seed token N not sequential to seed token N-1 so abort
											bAbort = True
											#dict_openie_config['logger'].info( 'prev check failed : ' + repr(nPreviousAddr) )
											break

									# look up variable name (from seed)
									if not tupleSeed[nSeedIndex][0] in dict_seed_to_template_mappings :
										raise Exception( 'no template mapping for seed template type : ' + repr(tupleSeed[nSeedIndex][0]) )
									strVarType = dict_seed_to_template_mappings[ tupleSeed[nSeedIndex][0] ]
									if '_' in strVarType :
										raise Exception( 'seed to template mapping error - variable name contains _ character : ' + repr(strVarType) )
									strVarName = strVarType + str(nSeedIndex+1)
									strVarNameUnique = strVarType + str(nSeedIndex+1) + '_' + str(nIndexSeedToken)
									setVarNames.add( strVarName )

									listSeedEntry.append( ( strVarType, strVarName, nAddress, strVarNameUnique ) )
									bFound = True
									nAddrIndexLastValid = nAddress
									nAddrIndex = nAddrIndex + 1
									break

								# no match, give up
								break

							if bFound == False :
								bAbort = True
								break

							#dict_openie_config['logger'].info( 'T1.2 = ' + repr( (nAddrIndex-1, nAddrIndexLastValid) ) )

						if bAbort == False :

							#dict_openie_config['logger'].info( 'T1.3 = ' + repr(listSeedEntry) )

							# check if a variable address is head of a branch that subsumes all of its other seed addreses
							# if so delete the other subsumed addresses so they are not needed
							if allow_seed_subsumption == True :
								for strVarName in setVarNames :

									# make a list of entries for this variable to check
									listToCheck = []
									for nIndexSeedGraph1 in range(len(listSeedEntry)) :
										( strVarType1, strVarName1, nAddress1, strVarNameUnique1 ) = listSeedEntry[nIndexSeedGraph1]
										if strVarName1 == strVarName :
											setAddrUnderBranch = dictNodeAddrSet[ nAddress1 ]
											listToCheck.append( ( strVarName1, nAddress1, setAddrUnderBranch ) )

									if len(listToCheck) > 1 :

										# find all addresses that are subsumed by another address. delete the subsumed addresses
										setAddrToRemove = set([])
										for ( strVarName1, nAddress1, setAddrUnderBranch1 ) in listToCheck :
											for ( strVarName2, nAddress2, setAddrUnderBranch2 ) in listToCheck :
												if (nAddress1 != nAddress2) and (nAddress2 in setAddrUnderBranch1) :
													setAddrToRemove.add( nAddress2 )

										# if we have subsumption, delete the subsumed addresses
										if len(setAddrToRemove) > 0 :
											#dict_openie_config['logger'].info( 'T2 (subsumption) = ' + repr( (strVarName,setAddrToRemove) ) )

											nIndexSeedGraph1 = 0
											while nIndexSeedGraph1 < len(listSeedEntry) :
												( strVarType1, strVarName1, nAddress1, strVarNameUnique1 ) = listSeedEntry[nIndexSeedGraph1]
												if (nAddress1 in setAddrToRemove) :
													del listSeedEntry[nIndexSeedGraph1]
												else :
													nIndexSeedGraph1 = nIndexSeedGraph1 + 1

							#dict_openie_config['logger'].info( 'T1.4 = ' + repr(listSeedEntry) )

							# add final seed entry to options at this seed index point (linked to a previous option)
							dictOptionsNew[nCount] = {
									'next_addr' : nAddrIndex,
									'linked_seed' : nCountPrev,
									'seed_addr' : listSeedEntry,
									'vars_used' : setVarNames
								}
							nCount = nCount + 1

				# has this seed any match options at all? if not abort the whole seed tuple
				if len(dictOptionsNew) == 0 :
					bNoSeedMatch = True
					break

				listSeedOptions.append( dictOptionsNew )

			# have we failed to get at least 1 match for each seed token? if so move to next sent
			if bNoSeedMatch == True :
				#dict_openie_config['logger'].info( 'T1.5.1 = no seed match' )
				continue

			#dict_openie_config['logger'].info( 'T1.5 = ' + repr(listSeedOptions) )

			# construct a set of full seed address options from the nested dict structure cxreated previously
			listSeedGraphAddressOptions = []
			construct_seed_addr_options(
				seed_options = listSeedOptions,
				seed_graph_address_output = listSeedGraphAddressOptions,
				dict_openie_config = dict_openie_config )

			#dict_openie_config['logger'].info( 'T1.6 = ' + repr(listSeedGraphAddressOptions) )

			# no good options? try next sent
			if len(listSeedGraphAddressOptions) == 0 :
				continue

			#dict_openie_config['logger'].info( 'SEED UNDER TEST (2) = ' + repr(tupleSeed) )
			#dict_openie_config['logger'].info( 'GRAPH = ' + repr(depGraph.to_dot()) )
			#dict_openie_config['logger'].info( 'seed options = ' + repr(listSeedGraphAddressOptions) )

			# loop on all possible seed options and do a graph walk to find if a pattern exists that matches them
			for listSeedGraphAddress in listSeedGraphAddressOptions :

				# make a list of targets
				listTargets = []
				for ( strVarType, strVarName, nAddr, strVarNameUnique ) in listSeedGraphAddress :
					# (address, seed var name)
					listTargets.append( ( nAddr, strVarNameUnique, strVarType ) )

				# create a pattern by walking the graph and connecting all targets (based on branches with seed tuple tokens in)
				#dict_openie_config['logger'].info( 'MATCH_GRAPH ' + str(nSeedIndex) + ' ' + repr(listSeedGraphAddress) )
				'''
				listTargets = []
				for nSeedElement in range(len(tupleSeed)) :
					strType = tupleSeed[nSeedElement][0]
					# (address, seed_type)
					listTargets.append( (listSeedGraphAddress[nSeedElement], strType) )
				'''
				#dict_openie_config['logger'].info( '\n\n\n\n' )
				#dict_openie_config['logger'].info( 'SEED UNDER TEST = ' + repr(tupleSeed) )
				#dict_openie_config['logger'].info( 'GRAPH = ' + repr(depGraph.to_dot()) )
				#dict_openie_config['logger'].info( 'INDEX = ' + repr(dictNodeAddrSet) )
				#dict_openie_config['logger'].info( 'TARGETS = ' + repr(listTargets) )

				# find all paths starting from all positions
				listShortestPath = []
				for nAddressTest in depGraph.nodes :

					# avoid starting at nodes that do not contain all the target addresses
					bExploreBranch = False
					if dictNodeAddrSet == None :
						bExploreBranch = True
					else :
						for ( nAddrE, strVarNameUniqueE, strVarTypeE ) in listTargets :
							if (nAddrE == nAddressTest) or (nAddrE in dictNodeAddrSet[ nAddressTest ]) :
								bExploreBranch = True
								break

					# do a graph walk to find the targets
					if bExploreBranch == True :
						calc_graph_paths_connecting_targets(
							list_targets = listTargets,
							dep_graph = depGraph,
							start_address = nAddressTest,
							list_shortest_path = listShortestPath,
							longest_dep_path = longest_dep_path,
							longest_inter_target_walk = longest_inter_target_walk,
							avoid_dep_set = avoid_dep_set,
							node_branch_index = dictNodeAddrSet,
							dict_openie_config = dict_openie_config )

				# sort all paths by length (we want the shortest)
				#dict_openie_config['logger'].info( 'SHORTEST PATH = ' + repr(listShortestPath) )

				# debug
				#return listPatterns

				if len(listShortestPath) > 0 :
					nVarCount = len(tupleSeed)
					dictVarNamesUsed = {}
					setWalkAddresses = set([])

					#if tupleSeed[0] == (u'ARGUMENT', u'The', u'nation', u"'s", u'health', u'maintenance', u'organizations') :
					#	dict_openie_config['logger'].info( 'SHORTEST PATH 1 = ' + repr(listShortestPath) )

					#dict_openie_config['logger'].info( 'SHORTEST WALK 1 = ' + repr(listShortestPath) )

					# compile set of walk addresses
					for nWalkIndex in range(len(listShortestPath)) :
						(nAddressWalk, strVarName, strVarType) = listShortestPath[nWalkIndex]
						setWalkAddresses.add( nAddressWalk )

					# replace any context variables with target variables if they share the same address space
					# this might happen if a target is added as context during walk, prior to being explicitly added on main path
					for nWalkIndex in range(len(listShortestPath)) :
						(nAddressWalk, strVarName, strVarType) = listShortestPath[nWalkIndex]
						if strVarName == None :
							for ( nTargetAddr, strTargetVarName, strTargetVarType ) in listTargets :
								if nAddressWalk == nTargetAddr :

									# replace (addr,None,None) entry with the target variable details
									listShortestPath[ nWalkIndex ] = ( nTargetAddr, strTargetVarName, strTargetVarType )
									break

					# make template based on walk along shortest path
					#dict_openie_config['logger'].info( 'MAPPINGS = ' + repr(dict_seed_to_template_mappings) )
					#dict_openie_config['logger'].info( 'GRAPH = ' + repr(depGraph.to_dot()) )
					#dict_openie_config['logger'].info( 'SEED UNDER TEST = ' + repr(tupleSeed) )
					#dict_openie_config['logger'].info( 'SHORTEST WALK 2 = ' + repr(listShortestPath) )

					# set of original walk addresses (so we make sure these addresses are not added as extra context when they are on the walk path anyway)
					listTemplate = []
					nWalkIndex = 0
					bIgnoreCurrentAddr = False
					while nWalkIndex < len(listShortestPath) :
						(nAddressWalk, strVarName, strVarType) = listShortestPath[nWalkIndex]
						setWalkAddresses.add( nAddressWalk )

						strToken = escape_extraction_pattern( depGraph.nodes[ nAddressWalk ]['word'].lower() )
						strPOS = depGraph.nodes[ nAddressWalk ]['ctag'].upper()

						# look up variable names for addresses that were previously walked (e.g. backtrack)
						if nAddressWalk in dictVarNamesUsed :
							strVarName = dictVarNamesUsed[ nAddressWalk ]
						else :
							if strVarName == None :
								strVarName = 'ctxt' + str(nVarCount) + '_1'
								nVarCount = nVarCount + 1
							dictVarNamesUsed[ nAddressWalk ] = strVarName

						if strVarType == None :
							strVarType = 'ctxt'

						if bIgnoreCurrentAddr == False :

							# is this the START or END token in sent? if so change the position flag
							strPositionFlag = '-'
							if nAddressWalk == 1 :
								strPositionFlag = 'S'
							if nAddressWalk == len( depGraph.nodes ) - 1 :
								strPositionFlag = 'E'

							# add node with variable name
							listTemplate.append( '{' + strVarName + ':' + strPositionFlag + ':pos=' + strPOS + ';lex=' + strToken + '}' )

							#dict_openie_config['logger'].info( 'PATH NODE = ' + repr( listTemplate[-1] ) )

						# reset ignore flag (used by dep_child_immediate)
						bIgnoreCurrentAddr = False

						#
						# add context not explicitly on the walk
						# for each variable (including context) on the walk path look 1-deep under its branch for additional context nodes to add
						# so we can pick up contextual stuff like neg that might not be on the dirtect walk
						# use dep_child, not dep_child_immediate move so each context variable is explicitly added to pattern, including its lexical terms, to constrain the matching so it must include this context
						#

						#dict_openie_config['logger'].info( 'T0 = ' + repr( nWalkIndex ) + ' : ' + repr(listShortestPath) )

						dictDeps = depGraph.nodes[nAddressWalk]['deps']
						for strDep in dictDeps :

							# parse allowed dep structure
							listAllowed = parse_allowed_dep_set(
								allowed_dep_set = dict_context_dep_types[strVarType],
								dict_openie_config = dict_openie_config )

							# loop on all nodes with this allowed dep child
							for nAddressChild in dictDeps[ strDep ] :
								if (not nAddressChild in setWalkAddresses) and (not nAddressChild in dictVarNamesUsed) and (depGraph.nodes[ nAddressChild ]['word'] != None) and (depGraph.nodes[ nAddressChild ]['ctag'] != None) :

									# check dep type is allowed and the child address is not outside limits for that dep type
									bAllowed = False
									for tupleAllowed in listAllowed :
										if (tupleAllowed[1] == False) and (strDep == tupleAllowed[0]) :
											bAllowed = True

										elif (tupleAllowed[1] == True) and (strDep.startswith( tupleAllowed[0] ) == True) :
											bAllowed = True

									if bAllowed == True :
										# child node not used in walk AND of a type important for context
										# add a temp move down to the node and the node itself as a context node

										strTokenContext = escape_extraction_pattern( depGraph.nodes[ nAddressChild ]['word'].lower() )
										strPOSContext = depGraph.nodes[ nAddressChild ]['ctag'].upper()

										listTemplate.append( '+' + strDep + '+' )

										# seed token index is always '1' as context tokens are a unigram
										strVarNameContext = 'ctxt' + str(nVarCount) + '_1'
										nVarCount = nVarCount + 1

										# is this the START or END token in sent? if so change the position flag
										strPositionFlag = '-'
										if nAddressChild == 1 :
											strPositionFlag = 'S'
										if nAddressChild == len( depGraph.nodes ) - 1 :
											strPositionFlag = 'E'

										listTemplate.append( '{' + strVarNameContext + ':' + strPositionFlag + ':pos=' + strPOSContext + ';lex=' + strTokenContext + '}' )
										dictVarNamesUsed[ nAddressChild ] = strVarNameContext

										# add context onto walk path so its not repeated later
										listShortestPath.insert( nWalkIndex, ( nAddressChild, strVarNameContext, 'ctxt' ) )
										setWalkAddresses.add( nAddressChild )
										nWalkIndex = nWalkIndex + 1

										#dict_openie_config['logger'].info( 'T1.4 = ' + repr( nWalkIndex ) + ' : ' + repr(listShortestPath) )

						#
						# execute walk instructions (if not at end)
						# move up (dep_parent) or down (dep_child), and if there are N down moves, all using the same dep, use 1 deep down (dep_child_immediate)
						#
						if nWalkIndex < len(listShortestPath)-1 :
							nNextAddr = listShortestPath[nWalkIndex+1][0]

							# move up?
							if nNextAddr == depGraph.nodes[nAddressWalk]['head'] :

								# get head dep that leads to the current node
								strMoveDep = None
								dictDeps = depGraph.nodes[nNextAddr]['deps']
								for strDep in dictDeps :
									if nAddressWalk in dictDeps[ strDep ] :
										strMoveDep = strDep
										break
								if strMoveDep == None :
									raise Exception( 'invalid move up - bad dependency tree?' )

								listTemplate.append( '<' + strMoveDep + '<' )
								#dict_openie_config['logger'].info( 'MOVE up = ' + repr( strMoveDep ) )

							# move down?
							else :

								#dict_openie_config['logger'].info( 'T2 = ' + repr( nWalkIndex ) + ' : ' + repr(nNextAddr) )

								strMoveDep = None
								dictDeps = depGraph.nodes[nAddressWalk]['deps']
								#dict_openie_config['logger'].info( 'T3 = ' + repr( dictDeps ) )
								for strDep in dictDeps :
									if nNextAddr in dictDeps[ strDep ] :
										strMoveDep = strDep
								if strMoveDep == None :
									raise Exception( 'invalid move down - bad dependency tree?' )

								# if all children of this dep type appear in the next walk addresses (returning to the current address each time afterwards)
								# then add a 'dep_child_immediate' move type NOT a 'dep_child' move type
								# this is so we can create templates that handle arbitary numbers of some dep types, such as compound
								# e.g. 3 x compound moves, each returning to the current node afterwards
								bLookAheadMore = True
								nWalkIndexSearch = nWalkIndex
								listChildrenVisited = []
								strVarBaseChild = None
								strVarTypeChild = None

								while bLookAheadMore == True :
									# is the next address a child (of strMoveDep) AND address after that is the current address (i.e. back to same place)?
									if len(listShortestPath) <= nWalkIndexSearch+2:
										bLookAheadMore = False
									else :
										if listShortestPath[nWalkIndexSearch+2][0] != nAddressWalk :
											bLookAheadMore = False
										else :
											bLookAheadMore = False
											(nAddressWalkSearch, strVarNameSearch, strVarTypeSearch) = listShortestPath[nWalkIndexSearch+1]
											strVarBaseSearch = strVarNameSearch.split('_')[0]
											if (strVarBaseChild != None) and (strVarBaseChild != strVarBaseSearch) :
												# dep has several children, with a mix of variables
												# arg1_1 > nmod > arg2_1
												#        > nmod > rel3_1
												break
											for nChildOfCurrentNode in dictDeps[strMoveDep] :
												if listShortestPath[nWalkIndexSearch+1][0] == nChildOfCurrentNode :
													# dep has a children, with same base variable as first child
													# arg1_1 > nmod > arg2_1
													#        > nmod > arg2_2
													bLookAheadMore = True
													listChildrenVisited.append( nChildOfCurrentNode )
													break

									if bLookAheadMore == True :
										(nAddressWalkSearch, strVarNameSearch, strVarTypeSearch) = listShortestPath[nWalkIndexSearch+1]
										strVarBaseSearch = strVarNameSearch.split('_')[0]
										if strVarBaseChild == None :
											strVarBaseChild = strVarBaseSearch
											strVarTypeChild = strVarTypeSearch

										nWalkIndexSearch = nWalkIndexSearch + 2

								if (nWalkIndexSearch > nWalkIndex) and (listChildrenVisited == dictDeps[strMoveDep]) :
									# add a POS and LEX constraint for this move so we dont match random stuff in another sent with this pattern
									listPOSContext = []
									listTokenContext = []
									for nIndexNode in listChildrenVisited :
										listPOSContext.append( depGraph.nodes[ nIndexNode ]['ctag'].upper() )
										listTokenContext.append( escape_extraction_pattern( depGraph.nodes[ nIndexNode ]['word'].lower() ) )
									strVarBaseChildConstrained = strVarBaseChild + ':pos=' + '|'.join( listPOSContext ) + ';lex=' + '|'.join( listTokenContext )

									# all children of this dep are on walk as a immediate child, not going any deeper, so add as a dep_child_immediate
									# dep_child_immediate -> add all children with this dep but dont move
									listTemplate.append( '@' + strMoveDep + ',' + strVarBaseChildConstrained + ',' + strVarTypeChild + '@' )

									# move to walk position where we have returned to the current node (remember walk index will be incremented at end of loop)
									nWalkIndex = nWalkIndexSearch - 1
									bIgnoreCurrentAddr = True

									#dict_openie_config['logger'].info( 'MOVE down immediate = ' + repr( strMoveDep ) )
								else :
									# dep_child -> get a child with this dep and move to its position (further down branch)
									listTemplate.append( '>' + strMoveDep + '>' )

									#dict_openie_config['logger'].info( 'MOVE down = ' + repr( strMoveDep ) )

						# next instruction on walk
						nWalkIndex = nWalkIndex + 1

					#if tupleSeed[0] == (u'ARGUMENT', u'The', u'nation', u"'s", u'health', u'maintenance', u'organizations') :
					#	dict_openie_config['logger'].info( 'SHORTEST PATH 4 = ' + repr(listShortestPath) )

					# make final template
					listPatterns.append( ' '.join( listTemplate ) )

					#dict_openie_config['logger'].info( 'FINAL WALK = ' + repr(listTemplate) )

			#dict_openie_config['logger'].info( 'GRAPH END' )

	return listPatterns


def generate_seeds_and_templates_batch(
	dict_document_sent_trees = {},
	generation_strategy = 'contiguous_tuple',
	seed_filter_strategy = 'premissive',
	set_annotations = None,
	dict_annotation_phrase_patterns = {},
	list_sequences = None,
	prevent_sequential_instances = None,
	lower_case = False,
	stemmer = None,
	lex_phrase_index = None,
	lex_uri_index = None,
	dict_document_sent_graphs = {},
	dict_seed_to_template_mappings = {},
	dict_context_dep_types = [],
	max_processes = 4,
	longest_dep_path = 32,
	longest_inter_target_walk = 2,
	max_seed_variants = 128,
	allow_seed_subsumption = True,
	avoid_dep_set = set([]),
	dict_openie_config = None ) :
	"""
	aggregate function.
	this will call generate_seed_tuples() and then generate_open_extraction_templates_batch() per document rather than per corpus.
	this is a lot faster as the seed search space is constrained to document level not corpus level, but might reject some useful seeds not found in the original POS seed patterns.

	:param dict dict_document_sent_trees: dict of document ID keys, each value being a list of nltk.Tree representing the sents in that doc = [ nltk.Tree( '(S (DT the) (ARGUMENT (NN handle)) (RELATION (VBZ missing)) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' ), ... ]
	:param str generation_strategy: name of generation strategy = predefined_sequences|contiguous_tuple|contiguous_tuple_candidates
	:param set set_annotations: filter set of annotation labels to create sequences for e.g. set( ['RELATION','ARGUMENT'] ) - [predefined_sequences, contiguous_triples]
	:param dict dict_annotation_phrase_patterns: allowed phrase patterns for each variable type e.g. { 'ARGUMENT' : ['noun_phrase','pronoun'], 'RELATION' : [verb_phrase'] }
	:param list list_sequences: list of sequences to allow as seed_tuples, including special START and END labels. for predefined_sequences its the set of predefined sequences  e.g. [ ('ARGUMENT','RELATION','ARGUMENT'), ('ARGUMENT','RELATION') ]). for contiguous_tuple its the tuple pattern (up to quad) to generate e.g. [ 'ARGUMENT','RELATION','ARGUMENT' ] - [predefined_sequences, contiguous_triples]
	:param list prevent_sequential_instances: list of seed types to prevent sequencial instance matching e.g. ['PREPOSITION'] - [predefined_sequences]
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()

	:param dict dict_document_sent_graphs: dict of document ID keys, each value being a list of nltk.parse.DependencyGraph objects for a corpus of sents
	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probbaly meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of open template extraction strings ready for parsing using comp_sem_lib.parse_extraction_pattern()
	:rtype: list
	"""

	if not isinstance( dict_document_sent_trees, dict ) :
		raise Exception( 'invalid dict_document_sent_trees' )
	if not isinstance( generation_strategy, str ) :
		raise Exception( 'invalid generation_strategy' )
	if not isinstance( set_annotations, (set,type(None)) ) :
		raise Exception( 'invalid set_annotations' )
	if not isinstance( dict_annotation_phrase_patterns, dict ) :
		raise Exception( 'invalid dict_annotation_phrase_patterns' )
	if not isinstance( list_sequences, (list,type(None)) ) :
		raise Exception( 'invalid list_sequences' )
	if not isinstance( prevent_sequential_instances, (list,type(None)) ) :
		raise Exception( 'invalid prevent_sequential_instances' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( seed_filter_strategy, str ) :
		raise Exception( 'invalid seed_filter_strategy' )
	if not isinstance( lex_uri_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_phrase_index' )

	if not isinstance( dict_document_sent_graphs, dict ) :
		raise Exception( 'invalid dict_document_sent_graphs' )
	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )

		# generate creates a single output (set of templates) given N input graphs
		listQueueResultsPending.append( 1 )

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in dict_document_sent_trees:
		# check two dicts are consistent
		if not strDocumentID in dict_document_sent_graphs :
			raise Exception('document ' + str(strDocumentID) + ' has a set list but is missing a dep graph list')

		# add to queue the list of sent graphs for this document
		listSent = dict_document_sent_trees[strDocumentID]
		listGraph = []

		# convert dep graph objects to its serialized form (for use in a queue)
		for nIndexGraph in range(len(dict_document_sent_graphs[strDocumentID])) :
			depObj = dict_document_sent_graphs[strDocumentID][nIndexGraph]
			strSerializedGraph = serialize_dependency_graph( dep_graph = depObj, dict_openie_config = dict_openie_config )
			listGraph.append( strSerializedGraph )

		# add document sents and graphs to queue
		listQueueInput[nProcess].append( (listSent,listGraph,strDocumentID) )

		# round robin assignment to queues
		nProcess = nProcess + 1
		if nProcess >= max_processes :
			nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.copy( dict_openie_config )
	dictConfigCopy['logger'] = None

	# setup a process pool as the template generation is very CPU intensive so we need to use all cores on a machine to speed it up
	listProcesses = []
	for nProcess in range(max_processes) :
		dict_openie_config['logger'].info( 'starting process ' + str(nProcess) + ' with ' + str( len( listQueueInput[nProcess] ) ) + ' sent graphs [seed and generate]' )

		processWorker = multiprocessing.Process(
			target = generate_seeds_and_templates_worker,
			args = (
				listQueue[nProcess],
				generation_strategy,
				seed_filter_strategy,
				set_annotations,
				dict_annotation_phrase_patterns,
				list_sequences,
				prevent_sequential_instances,
				lower_case,
				stemmer,
				lex_phrase_index,
				lex_uri_index,
				dict_seed_to_template_mappings,
				dict_context_dep_types,
				longest_dep_path,
				longest_inter_target_walk,
				max_seed_variants,
				allow_seed_subsumption,
				avoid_dep_set,
				1,
				nProcess,
				dictConfigCopy )
			)
		listProcesses.append( processWorker )

	# write number of documents to expect
	for nProcess in range(max_processes) :
		listQueue[nProcess][0].put( len(listQueueInput[nProcess]) )

	for nProcess in range(max_processes) :
		listProcesses[nProcess].start()

	# write all the input (sync to ensure in queues are limited in size)
	bFinishedInput = False
	while bFinishedInput == False :

		for nProcess in range(max_processes) :

			while len(listQueueInput[nProcess]) > 0 :

				# check for input queue overload (which can cause multiprocess Queue handling errors and lost results).
				# pause until the queue is smaller if this is the case.
				if listQueue[nProcess][0].qsize() > 100 :
					break
				
				# write entry and remove from list
				listQueue[nProcess][0].put( listQueueInput[nProcess].pop(0) )

		bFinishedInput = True
		for nProcess in range(max_processes) :
			if len(listQueueInput[nProcess]) > 0 :
				# input data left so pause and try to upload again
				bFinishedInput = False
				time.sleep(1)

	dict_openie_config['logger'].info( 'documents written OK [seed and generate]' )

	listOutputResults = []
	dictSeedTuplePerDocTotal = {}
	dictVarCandidatePerDocTotal = {}

	try :
		# download the pattern list result from each process queue (only one per process)
		# note: do not use blocking queues or thread joins (just an error queue) to avoid issues with queues closing but still being written to (if thread error occurs)
		#       e.g. IOError: [Errno 232] The pipe is being closed
		bFinished = False
		bError = False
		while (bFinished == False) and (bError == False) :

			bPause = True

			# check each process and try to get (a) errors (b) 1 result each
			for nProcess in range(max_processes) :

				# does this process still have work to do?
				if listQueueResultsPending[nProcess] > 0 :

					# non-blocking attempt to get errors
					try :
						strErrorMsg = listQueue[nProcess][2].get( False )

						dict_openie_config['logger'].info( '\tprocess ' + str(nProcess) + ' [seed and generate] failure > ' + strErrorMsg )

						# expect no more results from this process
						listQueueResultsPending[nProcess] = 0

						# flush input buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][0].empty() == False :
							listQueue[nProcess][0].get()

						# flush output buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][1].empty() == False :
							listQueue[nProcess][1].get()

						bError = True

						break
					except queue.Empty :
						pass


					# non-blocking attempt to get a result
					try :
						( listPatternsTotal, dictSeedTuplePerDoc, dictVarCandidatePerDoc ) = listQueue[nProcess][1].get( False )
						listOutputResults.extend( listPatternsTotal )
						for strDoc in dictSeedTuplePerDoc :
							dictSeedTuplePerDocTotal[strDoc] = dictSeedTuplePerDoc[strDoc]
							dictVarCandidatePerDocTotal[strDoc] = dictVarCandidatePerDoc[strDoc]

						#listMatches = listQueue[nProcess][1].get( False )
						#listOutputResults.extend( listMatches )

						listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] - 1
						bPause = False

					except queue.Empty :
						pass

			# more results?
			bFinished = True
			for nProcess in range(max_processes) :
				if listQueueResultsPending[nProcess] > 0 :
					bFinished = False

			# pause for 1 second if we did not get any results to give workers a change to make them
			if (bFinished == False) and (bPause == True) :
				time.sleep(1)

		# errors?
		if bError == True :
			raise Exception( 'errors processing request (see log)' )

		dict_openie_config['logger'].info( 'results aggregated OK [seed and generate]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input quete before
		time.sleep(2)

		# do cleanup
		dict_openie_config['logger'].info( 'tidying up from worker processes [seed and generate]' )
		( exctype, value ) = sys.exc_info()[:2]
		if exctype != None :
			dict_common_config['logger'].info( 'Exception (will continue) : ' + repr( ( exctype, value ) ) )

		for nProcess in range(max_processes) :
			# ensure all processes are terminates
			if listProcesses[nProcess] != None :
				if listProcesses[nProcess].is_alive() == True :
					listProcesses[nProcess].terminate()

			# ensure all queues for this thread are empty and closed
			for nQueue in range(len(listQueue[nProcess])) :
				while listQueue[nProcess][nQueue].empty() == False :
					listQueue[nProcess][nQueue].get()
				#listQueue[nProcess][nQueue].close()

		dict_openie_config['logger'].info( 'tidy up complete [seed and generate]' )

	# all done
	return ( listOutputResults, dictSeedTuplePerDocTotal, dictVarCandidatePerDocTotal )

def generate_seeds_and_templates_worker(
	tuple_queue = None,
	generation_strategy = 'contiguous_tuple',
	seed_filter_strategy = 'premissive',
	set_annotations = None,
	dict_annotation_phrase_patterns = {},
	list_sequences = None,
	prevent_sequential_instances = None,
	lower_case = False,
	stemmer = None,
	lex_phrase_index = None,
	lex_uri_index = None,
	dict_seed_to_template_mappings = {},
	dict_context_dep_types = [],
	longest_dep_path = 32,
	longest_inter_target_walk = 2,
	max_seed_variants = 128,
	allow_seed_subsumption = True,
	avoid_dep_set = set([]),
	pause_on_start = 0,
	process_id = 0,
	dict_openie_config = None ) :

	"""
	worker thread for comp_sem_lib.generate_seeds_and_templates_batch()

	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). the queueIn has serialized nltk.parse.DependencyGraph objects. queueOut has list of template patterns for this graph.

	:param str generation_strategy: name of generation strategy = predefined_sequences|contiguous_tuple|contiguous_tuple_candidates
	:param set set_annotations: filter set of annotation labels to create sequences for e.g. set( ['RELATION','ARGUMENT'] ) - [predefined_sequences, contiguous_triples]
	:param dict dict_annotation_phrase_patterns: allowed phrase patterns for each variable type e.g. { 'ARGUMENT' : ['noun_phrase','pronoun'], 'RELATION' : [verb_phrase'] }
	:param list list_sequences: list of sequences to allow as seed_tuples, including special START and END labels. for predefined_sequences its the set of predefined sequences  e.g. [ ('ARGUMENT','RELATION','ARGUMENT'), ('ARGUMENT','RELATION') ]). for contiguous_tuple its the tuple pattern (up to quad) to generate e.g. [ 'ARGUMENT','RELATION','ARGUMENT' ] - [predefined_sequences, contiguous_triples]
	:param list prevent_sequential_instances: list of seed types to prevent sequencial instance matching e.g. ['PREPOSITION'] - [predefined_sequences]
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()

	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probbaly meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param int pause_on_start: number of seconds to delay thread startup before CPU intensive work begins (to allow other workers to startup also)
	:param int process_id: process ID for logging
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )

	if not isinstance( generation_strategy, str ) :
		raise Exception( 'invalid generation_strategy' )
	if not isinstance( set_annotations, (set,type(None)) ) :
		raise Exception( 'invalid set_annotations' )
	if not isinstance( dict_annotation_phrase_patterns, dict ) :
		raise Exception( 'invalid dict_annotation_phrase_patterns' )
	if not isinstance( list_sequences, (list,type(None)) ) :
		raise Exception( 'invalid list_sequences' )
	if not isinstance( prevent_sequential_instances, (list,type(None)) ) :
		raise Exception( 'invalid prevent_sequential_instances' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( seed_filter_strategy, str ) :
		raise Exception( 'invalid seed_filter_strategy' )
	if not isinstance( lex_uri_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_phrase_index' )

	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )


	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.copy( dict_openie_config )

		logger = logging.getLogger( __name__ )
		if len(logger.handlers) == 0 :
			hdlr = logging.StreamHandler( stream = sys.stdout )
			LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
			fmt = logging.Formatter( fmt = LOG_FORMAT )
			hdlr.setFormatter( fmt )
			logger.addHandler( hdlr )
		logger.setLevel( logging.INFO )

		dictConfigCopy['logger'] = logger

		# pause 1 second to allow all other worker threads to start properly (otherwise startup might be delayed as CPU is grabbed by first workers)
		time.sleep( pause_on_start )

		# read number of documents
		nDocumentMax = tuple_queue[0].get()

		logger.info( 'worker process started (' + str(process_id) + ') = ' + str(nDocumentMax) + ' docs [seed and generate]' )

		# read all input data to process and empty the input queue
		listWorkload = []
		for nDocument in range(nDocumentMax) :

			# get document sents and serialized graphs
			(listSent, listGraph, strDocumentID) = tuple_queue[0].get()

			# convert serialized graph to a object
			for nIndexGraph in range(len(listGraph)) :

				# make a NLTK dep graph object
				depObj = nltk.parse.DependencyGraph( tree_str = listGraph[nIndexGraph], top_relation_label = 'root', cell_separator = '\t' )
				listGraph[nIndexGraph] = depObj
			
			# add to workload
			listWorkload.append( (listSent, listGraph, strDocumentID) )

		# input queue now empty so start work
		listPatternsTotal = []
		dictSeedTuplePerDoc = {}
		dictVarCandidatePerDoc = {}
		for nIndexWork in range(len(listWorkload)) :
			(listSent, listGraph, strDocumentID) = listWorkload[nIndexWork]

			# generate seeds
			( listSeedTuples, dictVarCandidates ) = generate_seed_tuples(
				list_sent_trees = listSent,
				generation_strategy = generation_strategy,
				set_annotations = set_annotations,
				dict_annotation_phrase_patterns = dict_annotation_phrase_patterns,
				list_sequences = list_sequences,
				prevent_sequential_instances = prevent_sequential_instances,
				lower_case = lower_case,
				stemmer = stemmer,
				dict_openie_config = dictConfigCopy )
			
			dictSeedTuplePerDoc[strDocumentID] = listSeedTuples
			dictVarCandidatePerDoc[strDocumentID] = dictVarCandidates

			# debug
			# logger.info( 'worker process seed (' + str(process_id) + ') = work index ' + str(nIndexWork) + ' = ' + repr(listSeedTuples) + ' [seed and generate]' )

			# filter seed_tuple arguments using lexicon (to ensure they are high quality matches that appear)
			# strategy A (permissive): make sure at least 1 arg or rel is in the lexicon
			# strategy B (selective): make sure at least 2 arg or rel is in the lexicon
			# strategy C (strict): make sure at least all arg or rel is in the lexicon
			if (len(lex_uri_index) > 0) and (seed_filter_strategy != 'no_filter') :
				nIndex = 0
				while nIndex < len(listSeedTuples) :
					nVarsOK = 0
					nVarsChecked = 0

					for nIndexVar in range(len(listSeedTuples[nIndex])) :
						tupleSeed = listSeedTuples[nIndex][nIndexVar]
						strVarType = tupleSeed[0]
						listPhrase = list( tupleSeed[1:] )

						nVarsChecked = nVarsChecked + 1

						# stem if needed
						if stemmer != None :
							for nIndex2 in range(len(listPhrase)) :
								listPhrase[nIndex2] = stemmer.stem( listPhrase[nIndex2].lower() )

						# get all possible lexicon matches using morphy
						listLexiconMatch = soton_corenlppy.lexico.lexicon_lib.phrase_lookup(
							phrase_tokens = listPhrase,
							head_token = None,
							lex_phrase_index = lex_phrase_index,
							lex_uri_index = lex_uri_index,
							max_gram = 5,
							stemmer = stemmer,
							apply_wordnet_morphy = True,
							hyphen_variant = True,
							dict_lexicon_config = dictConfigCopy )

						# any match is OK
						if len(listLexiconMatch) > 0 :
							nVarsOK = nVarsOK + 1
					
					# prune seed tuples to ensure only good ones remain prior to generating open templates
					bFailed = False
					if seed_filter_strategy == 'premissive' :
						# strategy A (permissive): make sure at least 1 arg or rel is in the lexicon
						if nVarsOK == 0 :
							bFailed = True
					elif seed_filter_strategy == 'selective' :
						# strategy B (selective): make sure at least 2 vars match in set, unless only one then allow 1
						if nVarsOK < 2 :
							bFailed = True
						if (nVarsChecked == 1) and (nVarsOK != 1) :
							bFailed = True
					elif seed_filter_strategy == 'strict' :
						# strategy C (strict): make sure at least all arg or rel is in the lexicon
						if nVarsOK != nVarsChecked :
							bFailed = True
					elif seed_filter_strategy == 'no_filter' :
						# do nothing
						pass

					# delete seed tuples that fail lexicon lookup
					if bFailed == True :
						del listSeedTuples[nIndex]
					else :
						nIndex = nIndex + 1

			# debug
			# logger.info( 'worker process filtered seed (' + str(process_id) + ') = work index ' + str(nIndexWork) + ' = ' + repr(listSeedTuples) + ' [seed and generate]' )

			# generate templates
			# var candidates not needed (relic)
			listPatterns = generate_open_extraction_templates(
				seed_tuples = listSeedTuples,
				var_candidates = {},
				corpus_sent_graphs = listGraph,
				dict_seed_to_template_mappings = dict_seed_to_template_mappings,
				dict_context_dep_types = dict_context_dep_types,
				longest_dep_path = longest_dep_path,
				longest_inter_target_walk = longest_inter_target_walk,
				max_seed_variants = max_seed_variants,
				allow_seed_subsumption = allow_seed_subsumption,
				avoid_dep_set = avoid_dep_set,
				dict_openie_config = dictConfigCopy )

			listPatternsTotal.extend( listPatterns )

			# micro pause to allow CPU balancing if run in batch mode
			time.sleep( 0.001 )

		# add result to output queue (only 1 so no need for queue size checks)
		tuple_queue[1].put( ( listPatternsTotal, dictSeedTuplePerDoc, dictVarCandidatePerDoc ) )

		logger.info( 'process ended (' + str(process_id) + ') [seed and generate]' )

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'generate_seeds_and_templates_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )


def generate_templates_from_predefined_seeds_batch(
	dict_document_sent_trees = {},
	dict_document_seed_tuples = {},
	dict_document_var_candidates = {},
	seed_filter_strategy = 'premissive',
	lower_case = False,
	stemmer = None,
	lex_phrase_index = None,
	lex_uri_index = None,
	dict_document_sent_graphs = {},
	dict_seed_to_template_mappings = {},
	dict_context_dep_types = [],
	max_processes = 4,
	longest_dep_path = 32,
	longest_inter_target_walk = 2,
	max_seed_variants = 128,
	allow_seed_subsumption = True,
	avoid_dep_set = set([]),
	dict_openie_config = None ) :
	"""
	aggregate function using pre-loaded seed tuples

	:param dict dict_document_sent_trees: dict of document ID keys, each value being a list of nltk.Tree representing the sents in that doc = [ nltk.Tree( '(S (DT the) (ARGUMENT (NN handle)) (RELATION (VBZ missing)) ... (REF (NP Agora) (NP XXIII) (, ,) (DOC_SECTION pl. 44) (DOC_SECTION no. 448)) ...)' ), ... ]
	:param dict dict_document_seed_tuples: dict of seed tuples for each doc created from generate_seed_tuples()
	:param dict dict_document_var_candidates: dict of var candidates for each doc from generate_seed_tuples()
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()

	:param dict dict_document_sent_graphs: dict of document ID keys, each value being a list of nltk.parse.DependencyGraph objects for a corpus of sents
	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probbaly meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of open template extraction strings ready for parsing using comp_sem_lib.parse_extraction_pattern()
	:rtype: list
	"""

	if not isinstance( dict_document_sent_trees, dict ) :
		raise Exception( 'invalid dict_document_sent_trees' )
	if not isinstance( dict_document_seed_tuples, dict ) :
		raise Exception( 'invalid dict_document_seed_tuples' )
	if not isinstance( dict_document_var_candidates, dict ) :
		raise Exception( 'invalid dict_document_var_candidates' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( seed_filter_strategy, str ) :
		raise Exception( 'invalid seed_filter_strategy' )
	if not isinstance( lex_uri_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_phrase_index' )

	if not isinstance( dict_document_sent_graphs, dict ) :
		raise Exception( 'invalid dict_document_sent_graphs' )
	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )

		# generate creates a single output (set of templates) given N input graphs
		listQueueResultsPending.append( 1 )

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in dict_document_sent_trees:
		# check two dicts are consistent
		if not strDocumentID in dict_document_sent_graphs :
			raise Exception('document ' + str(strDocumentID) + ' has a set list but is missing a dep graph list')

		# add to queue the list of sent graphs for this document
		listSent = dict_document_sent_trees[strDocumentID]
		listGraph = []

		if not strDocumentID in dict_document_seed_tuples :
			raise Exception('document ' + str(strDocumentID) + ' has a set list but is missing a seed tuple entry')
		listSeedTuples = dict_document_seed_tuples[strDocumentID]

		# convert dep graph objects to its serialized form (for use in a queue)
		for nIndexGraph in range(len(dict_document_sent_graphs[strDocumentID])) :
			depObj = dict_document_sent_graphs[strDocumentID][nIndexGraph]
			strSerializedGraph = serialize_dependency_graph( dep_graph = depObj, dict_openie_config = dict_openie_config )
			listGraph.append( strSerializedGraph )

		# add document sents and graphs to queue
		listQueueInput[nProcess].append( (listSent, listGraph, listSeedTuples) )

		# round robin assignment to queues
		nProcess = nProcess + 1
		if nProcess >= max_processes :
			nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.copy( dict_openie_config )
	dictConfigCopy['logger'] = None

	# setup a process pool as the template generation is very CPU intensive so we need to use all cores on a machine to speed it up
	listProcesses = []
	for nProcess in range(max_processes) :
		dict_openie_config['logger'].info( 'starting process ' + str(nProcess) + ' with ' + str( len( listQueueInput[nProcess] ) ) + ' sent graphs [seed and generate]' )

		processWorker = multiprocessing.Process(
			target = generate_templates_from_predefined_seeds_worker,
			args = (
				listQueue[nProcess],
				seed_filter_strategy,
				lower_case,
				stemmer,
				lex_phrase_index,
				lex_uri_index,
				dict_seed_to_template_mappings,
				dict_context_dep_types,
				longest_dep_path,
				longest_inter_target_walk,
				max_seed_variants,
				allow_seed_subsumption,
				avoid_dep_set,
				1,
				nProcess,
				dictConfigCopy )
			)
		listProcesses.append( processWorker )

	# write number of documents to expect
	for nProcess in range(max_processes) :
		listQueue[nProcess][0].put( len(listQueueInput[nProcess]) )

	for nProcess in range(max_processes) :
		listProcesses[nProcess].start()

	# write all the input (sync to ensure in queues are limited in size)
	bFinishedInput = False
	while bFinishedInput == False :

		for nProcess in range(max_processes) :

			while len(listQueueInput[nProcess]) > 0 :

				# check for input queue overload (which can cause multiprocess Queue handling errors and lost results).
				# pause until the queue is smaller if this is the case.
				if listQueue[nProcess][0].qsize() > 100 :
					break
				
				# write entry and remove from list
				listQueue[nProcess][0].put( listQueueInput[nProcess].pop(0) )

		bFinishedInput = True
		for nProcess in range(max_processes) :
			if len(listQueueInput[nProcess]) > 0 :
				# input data left so pause and try to upload again
				bFinishedInput = False
				time.sleep(1)

	dict_openie_config['logger'].info( 'documents written OK [seed and generate]' )

	try :
		listOutputResults = []

		# download the pattern list result from each process queue (only one per process)
		# note: do not use blocking queues or thread joins (just an error queue) to avoid issues with queues closing but still being written to (if thread error occurs)
		#       e.g. IOError: [Errno 232] The pipe is being closed
		bFinished = False
		bError = False
		while (bFinished == False) and (bError == False) :

			bPause = True

			# check each process and try to get (a) errors (b) 1 result each
			for nProcess in range(max_processes) :

				# does this process still have work to do?
				if listQueueResultsPending[nProcess] > 0 :

					# non-blocking attempt to get errors
					try :
						strErrorMsg = listQueue[nProcess][2].get( False )

						dict_openie_config['logger'].info( '\tprocess ' + str(nProcess) + ' [seed and generate] failure > ' + strErrorMsg )

						# expect no more results from this process
						listQueueResultsPending[nProcess] = 0

						# flush input buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][0].empty() == False :
							listQueue[nProcess][0].get()

						# flush output buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][1].empty() == False :
							listQueue[nProcess][1].get()

						bError = True

						break
					except queue.Empty :
						pass


					# non-blocking attempt to get a result
					try :
						listMatches = listQueue[nProcess][1].get( False )
						listOutputResults.extend( listMatches )

						listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] - 1
						bPause = False

					except queue.Empty :
						pass

			# more results?
			bFinished = True
			for nProcess in range(max_processes) :
				if listQueueResultsPending[nProcess] > 0 :
					bFinished = False

			# pause for 1 second if we did not get any results to give workers a change to make them
			if (bFinished == False) and (bPause == True) :
				time.sleep(1)

		# errors?
		if bError == True :
			raise Exception( 'errors processing request (see log)' )

		dict_openie_config['logger'].info( 'results aggregated OK [seed and generate]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input quete before
		time.sleep(2)

		# do cleanup
		dict_openie_config['logger'].info( 'tidying up from worker processes [seed and generate]' )
		( exctype, value ) = sys.exc_info()[:2]
		if exctype != None :
			dict_common_config['logger'].info( 'Exception (will continue) : ' + repr( ( exctype, value ) ) )

		for nProcess in range(max_processes) :
			# ensure all processes are terminates
			if listProcesses[nProcess] != None :
				if listProcesses[nProcess].is_alive() == True :
					listProcesses[nProcess].terminate()

			# ensure all queues for this thread are empty and closed
			for nQueue in range(len(listQueue[nProcess])) :
				while listQueue[nProcess][nQueue].empty() == False :
					listQueue[nProcess][nQueue].get()
				#listQueue[nProcess][nQueue].close()

		dict_openie_config['logger'].info( 'tidy up complete [seed and generate]' )

	# all done
	return listOutputResults

def generate_templates_from_predefined_seeds_worker(
	tuple_queue = None,
	seed_filter_strategy = 'premissive',
	lower_case = False,
	stemmer = None,
	lex_phrase_index = None,
	lex_uri_index = None,
	dict_seed_to_template_mappings = {},
	dict_context_dep_types = [],
	longest_dep_path = 32,
	longest_inter_target_walk = 2,
	max_seed_variants = 128,
	allow_seed_subsumption = True,
	avoid_dep_set = set([]),
	pause_on_start = 0,
	process_id = 0,
	dict_openie_config = None ) :

	"""
	worker thread for comp_sem_lib.generate_seeds_and_templates_batch()

	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). the queueIn has serialized nltk.parse.DependencyGraph objects. queueOut has list of template patterns for this graph.

	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()

	:param list dict_seed_to_template_mappings: dict of mappings from seed_tuple type names (e.g. 'ARGUMENT') to open extraction template types (e.g. 'arg')
	:param dict dict_context_dep_types: dict of contextual dependency types that are to be added if not already on graph path (e.g. neg)
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probbaly meaningless
	:param int max_seed_variants: max number of seed variants possible for an individual sent graph. seed variants are created by matching seed tokens to sent graph tokens, and exploding the combinations so all possibilities are checked. if a seed phrase contains tokens that appear many times in a sent, the combinations could get large. this setting provides an upper limit to ensure for these unusual cases processing time is not excessive.
	:param bool allow_seed_subsumption: if True removes any seed token which is subsumed by other seed token (i.e. its under a root seed node on a dependancy graph branch)
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param int pause_on_start: number of seconds to delay thread startup before CPU intensive work begins (to allow other workers to startup also)
	:param int process_id: process ID for logging
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )

	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( seed_filter_strategy, str ) :
		raise Exception( 'invalid seed_filter_strategy' )
	if not isinstance( lex_uri_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_phrase_index' )

	if not isinstance( dict_seed_to_template_mappings, dict ) :
		raise Exception( 'invalid dict_seed_to_template_mappings' )
	if not isinstance( dict_context_dep_types, dict ) :
		raise Exception( 'invalid dict_context_dep_types' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( max_seed_variants, int ) :
		raise Exception( 'invalid max_seed_variants' )
	if not isinstance( allow_seed_subsumption, bool ) :
		raise Exception( 'invalid allow_seed_subsumption' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )


	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.copy( dict_openie_config )

		logger = logging.getLogger( __name__ )
		if len(logger.handlers) == 0 :
			hdlr = logging.StreamHandler( stream = sys.stdout )
			LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
			fmt = logging.Formatter( fmt = LOG_FORMAT )
			hdlr.setFormatter( fmt )
			logger.addHandler( hdlr )
		logger.setLevel( logging.INFO )

		dictConfigCopy['logger'] = logger

		# pause 1 second to allow all other worker threads to start properly (otherwise startup might be delayed as CPU is grabbed by first workers)
		time.sleep( pause_on_start )

		# read number of documents
		nDocumentMax = tuple_queue[0].get()

		logger.info( 'worker process started (' + str(process_id) + ') = ' + str(nDocumentMax) + ' docs [seed and generate]' )

		# read all input data to process and empty the input queue
		listWorkload = []
		for nDocument in range(nDocumentMax) :

			# get document sents and serialized graphs
			(listSent, listGraph, listSeedTuples) = tuple_queue[0].get()

			# convert serialized graph to a object
			for nIndexGraph in range(len(listGraph)) :

				# make a NLTK dep graph object
				depObj = nltk.parse.DependencyGraph( tree_str = listGraph[nIndexGraph], top_relation_label = 'root', cell_separator = '\t' )
				listGraph[nIndexGraph] = depObj
			
			# add to workload
			listWorkload.append( (listSent, listGraph, listSeedTuples) )

		# input queue now empty so start work
		listPatternsTotal = []
		for nIndexWork in range(len(listWorkload)) :
			(listSent, listGraph, listSeedTuples) = listWorkload[nIndexWork]

			# debug
			#logger.info( 'worker process seed (' + str(process_id) + ') = work index ' + str(nIndexWork) + ' = ' + repr(listSeedTuples) + ' [seed and generate]' )

			# filter seed_tuple arguments using lexicon (to ensure they are high quality matches that appear)
			# strategy A (permissive): make sure at least 1 arg or rel is in the lexicon
			# strategy B (selective): make sure at least 2 arg or rel is in the lexicon
			# strategy C (strict): make sure at least all arg or rel is in the lexicon
			if (len(lex_uri_index) > 0) and (seed_filter_strategy != 'no_filter') :
				nIndex = 0
				while nIndex < len(listSeedTuples) :
					nVarsOK = 0
					nVarsChecked = 0

					for nIndexVar in range(len(listSeedTuples[nIndex])) :
						tupleSeed = listSeedTuples[nIndex][nIndexVar]
						strVarType = tupleSeed[0]
						listPhrase = list( tupleSeed[1:] )

						nVarsChecked = nVarsChecked + 1

						# stem if needed
						if stemmer != None :
							for nIndex2 in range(len(listPhrase)) :
								listPhrase[nIndex2] = stemmer.stem( listPhrase[nIndex2].lower() )

						# get all possible lexicon matches using morphy
						listLexiconMatch = soton_corenlppy.lexico.lexicon_lib.phrase_lookup(
							phrase_tokens = listPhrase,
							head_token = None,
							lex_phrase_index = lex_phrase_index,
							lex_uri_index = lex_uri_index,
							max_gram = 5,
							stemmer = stemmer,
							apply_wordnet_morphy = True,
							hyphen_variant = True,
							dict_lexicon_config = dictConfigCopy )

						# any match is OK
						if len(listLexiconMatch) > 0 :
							nVarsOK = nVarsOK + 1
					
					# prune seed tuples to ensure only good ones remain prior to generating open templates
					bFailed = False
					if seed_filter_strategy == 'premissive' :
						# strategy A (permissive): make sure at least 1 arg or rel is in the lexicon
						if nVarsOK == 0 :
							bFailed = True
					elif seed_filter_strategy == 'selective' :
						# strategy B (selective): make sure at least 2 vars match in set, unless only one then allow 1
						if nVarsOK < 2 :
							bFailed = True
						if (nVarsChecked == 1) and (nVarsOK != 1) :
							bFailed = True
					elif seed_filter_strategy == 'strict' :
						# strategy C (strict): make sure at least all arg or rel is in the lexicon
						if nVarsOK != nVarsChecked :
							bFailed = True
					elif seed_filter_strategy == 'no_filter' :
						# do nothing
						pass

					# delete seed tuples that fail lexicon lookup
					if bFailed == True :
						del listSeedTuples[nIndex]
					else :
						nIndex = nIndex + 1

			# debug
			#logger.info( 'worker process filtered seed (' + str(process_id) + ') = work index ' + str(nIndexWork) + ' = ' + repr(listSeedTuples) + ' [seed and generate]' )

			# generate templates
			# var candidates not needed (relic)
			listPatterns = generate_open_extraction_templates(
				seed_tuples = listSeedTuples,
				var_candidates = {},
				corpus_sent_graphs = listGraph,
				dict_seed_to_template_mappings = dict_seed_to_template_mappings,
				dict_context_dep_types = dict_context_dep_types,
				longest_dep_path = longest_dep_path,
				longest_inter_target_walk = longest_inter_target_walk,
				max_seed_variants = max_seed_variants,
				allow_seed_subsumption = allow_seed_subsumption,
				avoid_dep_set = avoid_dep_set,
				dict_openie_config = dictConfigCopy )

			listPatternsTotal.extend( listPatterns )

			# micro pause to allow CPU balancing if run in batch mode
			time.sleep( 0.001 )

		# add result to output queue (only 1 so no need for queue size checks)
		tuple_queue[1].put( listPatternsTotal )

		logger.info( 'process ended (' + str(process_id) + ') [seed and generate]' )

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'generate_seeds_and_templates_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )
		#logger.info( 'process error (' + str(process_id) + ') [seed and generate] = ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )


def construct_node_index( dep_graph = None, dict_openie_config = None ) :
	"""
	compute a complete list of the addresses under each node. this is important to guide the graph walk later
	internal method called by generate_open_extraction_templates()

	:param nltk.parse.DependencyGraph dep_graph: nltk.parse.DependencyGraph object
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: index of each address containing node addresses under it in tree { addr : [ childaddr1, childaddr2 ... ] }
	:rtype: dict
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	dictNodeAddrSet = {}
	for nAddress in dep_graph.nodes :
		setAddrUnderNode = set([])
		setNextAddrToCheck = set([nAddress])

		while len(setNextAddrToCheck) > 0 :
			setCheck = copy.copy( setNextAddrToCheck )
			setNextAddrToCheck = set([])

			for nAddrToCheck in setCheck :
				dictDeps = dep_graph.nodes[nAddrToCheck]['deps']
				for strDep in dictDeps :
					for nAddrChild in dictDeps[strDep] :
						setAddrUnderNode.add( nAddrChild )
						setNextAddrToCheck.add( nAddrChild )

		dictNodeAddrSet[ nAddress ] = setAddrUnderNode
	
	return dictNodeAddrSet


def construct_seed_addr_options( seed_options = None, seed_graph_address_output = None, dict_openie_config = None ) :
	"""
	calculate seed address walks given a set of seed address options in a nested structure.
	internal method called by generate_open_extraction_templates()

	:param dict seed_options: dict of seed options
	:param list seed_graph_address_output: output list which will be populated with seed walk options
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	# dictOptionSeed1 =
	# {
	#   option1 : { seed_addr : [ ( 'arg', 'arg1', 1, 'arg1_1' ),
	#                             ( 'arg', 'arg1', 2, 'arg1_2' ) ],
	#               next_addr : 3,
	#               vars_used : set( [ 'arg1' ] ),
	#               linked_seed : None,
	#             },
	#   option2 : { seed_addr : [ ( 'arg', 'arg1', 10, 'arg1_1' ),
	#                             ( 'arg', 'arg1', 11, 'arg1_2' ) ],
	#               next_addr : 12,
	#               vars_used : set( [ 'arg1' ] )
	#               linked_seed : None,
	#             }
	# }
	# dictOptionSeed2 =
	# {
	#   option1 : { seed_addr : [ ( 'rel', 'rel2', 15, 'rel2_1' ) ],
	#               next_addr : 16,
	#               vars_used : set( [ 'rel2' ] )
	#               linked_seed : option1,
	#             },
	#   option2 : { seed_addr : [ ( 'rel', 'rel2', 15, 'rel2_1' ) ],
	#               next_addr : 16,
	#               vars_used : set( [ 'rel2' ] )
	#               linked_seed : option2,
	#             },
	# }
	# listSeedOptions = [ dictOptionSeed1,dictOptionSeed2 ]
	# listSeedGraphAddressOptions = [
	#                                 [ ( 'arg', 'arg1', 1, 'arg1_1' ), ( 'arg', 'arg1', 2, 'arg1_2' ), ( 'rel', 'rel2', 15, 'rel2_1' ) ],
	#                                 ...
	#                               ]

	if not isinstance( seed_options, list ) :
		raise Exception( 'invalid seed_options' )
	if not isinstance( seed_graph_address_output, list ) :
		raise Exception( 'invalid seed_graph_address_output' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	#dict_openie_config['logger'].info( 'OPTIONS = ' + repr(seed_options) )

	# loop on final seeds option entries, and make a address walk based on the backward links
	# first seed with have a linked count of -1
	dictOptionsLast = seed_options[-1]
	for nCount in dictOptionsLast :
		dictEntry = dictOptionsLast[nCount]

		# START and END entries do not have addresses, so start with an []
		if not 'seed_addr' in dictEntry :
			listSeedGraphAddress = []
		else :
			listSeedGraphAddress = dictEntry[ 'seed_addr' ]

		# create seed address chain for this option
		nLinkedCount = dictEntry[ 'linked_seed' ]
		nLinkedSeedIndex = len(seed_options) - 2
		while nLinkedCount != -1 :
			dictEntry = seed_options[nLinkedSeedIndex][nLinkedCount]
			if 'seed_addr' in dictEntry :
				listSeedGraphAddressNew = copy.copy( dictEntry[ 'seed_addr' ] )
				listSeedGraphAddressNew.extend( listSeedGraphAddress )
				listSeedGraphAddress = listSeedGraphAddressNew

			nLinkedCount = dictEntry[ 'linked_seed' ]
			nLinkedSeedIndex = nLinkedSeedIndex - 1

		# add complete chains of seed {type,var,addr,var_unique} into the final option list
		seed_graph_address_output.append( listSeedGraphAddress )

	#dict_openie_config['logger'].info( 'OPTIONS 2 = ' + repr(seed_graph_address_output) )


def calc_graph_paths_connecting_targets( list_targets = None, dep_graph = None, start_address = 0, list_shortest_path = [], longest_dep_path = 32, longest_inter_target_walk = 2, avoid_dep_set = set([]), node_branch_index = None, dict_openie_config = None ) :
	"""
	calculate a graph walk path that connects all targets.
	this algorithm uses a fast depth first exploration of dep branches, as opposed to a slower random walk approach.
	the order of targets found is not important as we want to allow all sequences of targets (e.g. arg rel arg AND rel arg arg ).

	:param list list_targets: list of tuples (address, var_name, var_type) to find on graph walk in sequential order they must be found
	:param nltk.parse.DependencyGraph dep_graph: dependancy graph for walk
	:param int start_address: root address in graph branch to walk
	:param list list_shortest_path: shortest path so far
	:param int longest_dep_path: longest graph path allowed for walks, to avoid very large walks with many combinations that simply take too long.
	:param int longest_inter_target_walk: longest inter-target variable walk distance allowed. if there are too many dep graph steps the semantic drift will be too big and the resulting extraction probably meaningless
	:param set avoid_dep_set: set of dep types to avoid walking (defauly empty set)
	:param dict node_branch_index: index of branch addresses under each node (to make walk more efficient by avoiding branches without the target node)
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: shortest path connecting all targets = [ (address, var_name, var_type), ... ]
	:rtype: list
	"""

	if not isinstance( list_targets, list ) :
		raise Exception( 'invalid list_targets' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( start_address, int ) :
		raise Exception( 'invalid start_address' )
	if not isinstance( list_shortest_path, list ) :
		raise Exception( 'invalid list_shortest_path' )
	if not isinstance( longest_dep_path, int ) :
		raise Exception( 'invalid longest_dep_path' )
	if not isinstance( longest_inter_target_walk, int ) :
		raise Exception( 'invalid longest_inter_target_walk' )
	if not isinstance( avoid_dep_set, set ) :
		raise Exception( 'invalid avoid_dep_set' )
	if not isinstance( node_branch_index, dict ) :
		raise Exception( 'invalid node_branch_index' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# reject start_address if the branch does not contain all the target nodes we need
	bExploreBranch = True
	for ( nAddrE, strVarNameUniqueE, strVarTypeE ) in list_targets :
		if (nAddrE != start_address) and (not nAddrE in node_branch_index[ start_address ]) :
			bExploreBranch = False
			break
	if bExploreBranch == False :
		return

	#dict_openie_config['logger'].info( 'T1 (start)' )

	nAddr = start_address

	# abort if we find a non-word address
	if dep_graph.nodes[nAddr]['address'] == None :
		return
	if dep_graph.nodes[nAddr]['word'] == None :
		return
	if len(dep_graph.nodes[nAddr]['word']) == 0 :
		return
	if dep_graph.nodes[nAddr]['ctag'] == None :
		return

	# depth first search of branch from the provided address
	# keep a node of the steps taken
	setUniqueAddrSinceLastTarget = set([])
	listAddrWalk = []
	setAddrExplored = set([])
	listTargetsLeft = copy.copy( list_targets )
	while len(listTargetsLeft) > 0 :

		# add address to explored list
		setAddrExplored.add( nAddr )
		#dict_openie_config['logger'].info( 'T2 = ' + repr(nAddr) )

		# count the number of unique addresses since last target var has been found
		# if its larger than max inter-var walk then abort
		setUniqueAddrSinceLastTarget.add( nAddr )
		if len(setUniqueAddrSinceLastTarget) > longest_inter_target_walk :
			#dict_openie_config['logger'].info( 'T3' )
			return

		# is this address a target?
		bTargetFound = False
		for nIndexT in range(len(listTargetsLeft)) :
			( nAddrT, strVarNameUniqueT, strVarTypeT ) = listTargetsLeft[nIndexT]
			if nAddr == nAddrT :

				# add target variable to walk
				bTargetFound = True
				listAddrWalk.append( ( nAddrT, strVarNameUniqueT, strVarTypeT ) )
				#dict_openie_config['logger'].info( 'T5 = ' + repr( ( nAddrT, strVarNameUniqueT, strVarTypeT ) ) )

				# is walk too large?
				if len(listAddrWalk) > longest_dep_path :
					#dict_openie_config['logger'].info( 'T4' )
					return

				# remove found target from list
				del listTargetsLeft[nIndexT]
				setUniqueAddrSinceLastTarget = set([])
				break

		# found all targets?
		if len(listTargetsLeft) == 0 :
			break

		# if target not found add this walk address as a context node
		if bTargetFound == False :
			listAddrWalk.append( ( nAddr, None, None ) )

			# is walk now too large?
			if len(listAddrWalk) > longest_dep_path :
				#dict_openie_config['logger'].info( 'T4.1' )
				return

		# move to next address using a depth first strategy
		# move down if we can, otherwise go back up (not above start_address), until we have seen every address in branch
		nAddrNext = None
		dictDeps = dep_graph.nodes[nAddr]['deps']
		for strDep in dictDeps :

			# check list of forbidden dep types (default is an empty set)
			bForbid = False
			for strForbidDep in avoid_dep_set :
				if strForbidDep.endswith(':*') :
					listForbid = strForbidDep.split(':')
					if ( strDep.startswith( listForbid[0] + ':' ) == True ) :
						bForbid = True
				elif strDep == strForbidDep :
					bForbid = True
			if bForbid == True :
				continue

			# get next child that we have not yet seen
			for nAddressChild in dictDeps[ strDep ] :
				if (not nAddressChild in setAddrExplored) and (nAddressChild != None) :

					# dont explore a child address which does not have a target in its branch
					bExploreBranch = False
					for ( nAddrE, strVarNameUniqueE, strVarTypeE ) in listTargetsLeft :
						if (nAddrE == nAddressChild) or (nAddrE in node_branch_index[ nAddressChild ]) :
							bExploreBranch = True
							break
					if bExploreBranch == True :
						nAddrNext = nAddressChild


						break

			if nAddrNext != None :
				break

		# no valid children available? go up if we are not at top of branch already
		if nAddrNext == None :
			if nAddr != start_address :
				nAddrNext = dep_graph.nodes[nAddr]['head']

		if nAddrNext == None :
			# we have run out of addresses to try, and the target list is not empty, so its a failure
			return
		else :
			# move to next address
			nAddr = nAddrNext

	#dict_openie_config['logger'].info( 'T6 = ' + repr( listAddrWalk ) )

	# success! replace shortest path if its currently longer than the walk we have just found
	if (len(list_shortest_path) == 0) or (len(list_shortest_path) > len(listAddrWalk)) :
		# empty shortest path variable
		while len(list_shortest_path) > 0 :
			list_shortest_path.pop()

		# add new walk
		list_shortest_path.extend( listAddrWalk )

		#dict_openie_config['logger'].info( 'T7' )

	# all done
	return

def normalize_open_extraction_templates( list_patterns = None, topN = 1000, lang = 'eng', dict_generalize_strategy = dict_generalize_strategy_default, dict_openie_config = None ) :
	"""
	aggregate and normalize a set of open pattern templates generated by comp_sem_lib.generate_open_extraction_templates()

	aggregate and normalize open pattern templates:
		* merge lexical and pos constraints for patterns with the same structure
		* remove all pos and lexical constraints on args based on dict_generalize_strategy
		* remove all lexical constraints on relations
		* TODO use lexicon (e.g. WordNet) to include semantic generalizations (i.e. hypernym) for known lexical constraints

	:param list list_patterns: list of open template extraction strings ready for parsing using comp_sem_lib.parse_extraction_pattern()
	:param int topN: top N templates to return (-1 for all)
	:param str lang: WordNet language
	:param dict dict_generalize_strategy: { 'relax_lex' : list_of_var_types, 'relax_pos' : list_of_var_types } 
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of open template extraction strings read for parsing using comp_sem_lib.parse_extraction_pattern()
	:rtype: list
	"""

	if not isinstance( list_patterns, (list,set) ) :
		raise Exception( 'invalid list_patterns' )
	if not isinstance( topN, int ) :
		raise Exception( 'invalid topN' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( dict_generalize_strategy, dict ) :
		raise Exception( 'invalid dict_generalize_strategy' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if not 'relax_lex' in dict_generalize_strategy :
		raise Exception('relax_lex not in dict_generalize_strategy' )
	if not 'relax_pos' in dict_generalize_strategy :
		raise Exception('relax_pos not in dict_generalize_strategy' )

	# parse open pattern templates 
	listParsedExtractionPatterns = []
	listFreqStats = []
	nIndex1 = 0
	for strPattern in list_patterns :
		# store parsed pattern
		listParsedExtractionPatterns.append( parse_extraction_pattern( str_pattern = strPattern, dict_openie_config = dict_openie_config ) )

		# set freq to 1
		listFreqStats.append( ( nIndex1, 1 ) )
		nIndex1 = nIndex1 + 1

	# loop on each pattern and find any patterns with the same structure (same arg, rel and slots)
	# then merge the POS and LEX to make a single pattern
	for nIndex1 in range(len(listParsedExtractionPatterns)) :
		listTemplate1 = listParsedExtractionPatterns[nIndex1]
		listToBeMerged = []

		if listTemplate1 == None :
			continue

		for nIndex2 in range(nIndex1 + 1, len(listParsedExtractionPatterns)) :
			listTemplate2 = listParsedExtractionPatterns[nIndex2]

			if listTemplate2 == None :
				continue

			# check if they have an identical structure
			# [ ('rel', 'rel1', '-', ( ('VBZ,VBN'),('contains','holds') )), ... ]
			bIdenticalStructure = True
			if len(listTemplate1) != len(listTemplate2) :
				bIdenticalStructure = False
			else :
				for nIndex3 in range(len(listTemplate1)) :
					# all types need to be the same (but values can vary)
					if listTemplate1[nIndex3][0] != listTemplate2[nIndex3][0] :
						bIdenticalStructure = False
					else :
						if not listTemplate1[nIndex3][0] in ( 'dep_parent', 'dep_child', 'dep_child_returning', 'dep_child_immediate' ) :
							# pos marker need to be the same for var entries
							if listTemplate1[nIndex3][2] != listTemplate2[nIndex3][2] :
								bIdenticalStructure = False
						else :
							# all move instructions need to be the same
							if listTemplate1[nIndex3][1] != listTemplate2[nIndex3][1] :
								bIdenticalStructure = False

			if bIdenticalStructure == True :
				listToBeMerged.append( nIndex2 )

		if len(listToBeMerged) > 0 :
			listTemplate1 = list( listTemplate1 )

			for nIndex2 in range(len(listTemplate1)) :
				if not listTemplate1[nIndex2][0] in ( 'dep_parent', 'dep_child', 'dep_child_returning', 'dep_child_immediate' ) :
					listPOS1 = list( listTemplate1[nIndex2][3][0] )
					listTokens1 = list( listTemplate1[nIndex2][3][1] )

					for nIndex3 in listToBeMerged :
						listTemplate2 = listParsedExtractionPatterns[nIndex3]
						listPOS2 = listTemplate2[nIndex2][3][0]
						listTokens2 = listTemplate2[nIndex2][3][1]

						# merge pos and lexicon lists
						listPOS1.extend( listPOS2 )
						listTokens1.extend( listTokens2 )

					# remove any duplicates
					listPOS1 = list( set( listPOS1 ) )
					listTokens1 = list( set( listTokens1 ) )

					listTemplate1[nIndex2] = ( listTemplate1[nIndex2][0], listTemplate1[nIndex2][1], listTemplate1[nIndex2][2], ( listPOS1, listTokens1 ) )

			# replace old version with merged version
			listParsedExtractionPatterns[nIndex1] = listTemplate1

			# update freq stats as we have merged patterns
			listFreqStats[nIndex1] = ( nIndex1, listFreqStats[nIndex1][1] + len(listToBeMerged) )

			# remove all other versions
			for nIndex2 in listToBeMerged :
				listParsedExtractionPatterns[nIndex2] = None

	# aggresive generalization
	for nIndex1 in range(len(listParsedExtractionPatterns)) :
		listTemplate1 = listParsedExtractionPatterns[nIndex1]
		if listTemplate1 == None :
			continue

		# aggresive generalization of syntactic patterns as there is no context beyond the rel terms
		for nIndex2 in range(len(listTemplate1)) :

			if listTemplate1[nIndex2][0] in dict_generalize_strategy['relax_lex'] :
				listPOS1 = listTemplate1[nIndex2][3][0]
				listTemplate1[nIndex2] = ( listTemplate1[nIndex2][0], listTemplate1[nIndex2][1], listTemplate1[nIndex2][2], ( listPOS1, [] ) )

			elif listTemplate1[nIndex2][0] in dict_generalize_strategy['relax_pos'] :
				listTokens1 = listTemplate1[nIndex2][3][1]
				listTemplate1[nIndex2] = ( listTemplate1[nIndex2][0], listTemplate1[nIndex2][1], listTemplate1[nIndex2][2], ( [], listTokens1 ) )

			elif listTemplate1[nIndex2][0] in dict_generalize_strategy['relax_pos_number_aware'] :
				listTokens1 = listTemplate1[nIndex2][3][1]
				listPOS1 = listTemplate1[nIndex2][3][0]
				if 'cd' in listPOS1 :
					# numbers (and only numbers) get replaced with POS (so any number can match)
					listTemplate1[nIndex2] = ( listTemplate1[nIndex2][0], listTemplate1[nIndex2][1], listTemplate1[nIndex2][2], ( listPOS1, [] ) )
				else :
					# otherwise use the lex list and discard POS
					listTemplate1[nIndex2] = ( listTemplate1[nIndex2][0], listTemplate1[nIndex2][1], listTemplate1[nIndex2][2], ( [], listTokens1 ) )

		# replace old version with generalized one
		listParsedExtractionPatterns[nIndex1] = listTemplate1

	# debug
	'''
	dict_openie_config['logger'].info( 'PRE-FILTER-NORMALIZED' )
	for nIndex in range(len(listParsedExtractionPatterns)) :
		dict_openie_config['logger'].info(
			serialize_extraction_pattern(
				list_pattern = listParsedExtractionPatterns[nIndex],
				dict_openie_config = dict_openie_config
				)
			)
	'''

	# remove duplicates AND calc freq statistics for each unique pattern (as there will be duplicates after generalization)
	for nIndex1 in range(len(listParsedExtractionPatterns)) :
		listTemplate1 = listParsedExtractionPatterns[nIndex1]
		if listTemplate1 == None :
			continue

		for nIndex2 in range(nIndex1 + 1, len(listParsedExtractionPatterns)) :
			listTemplate2 = listParsedExtractionPatterns[nIndex2]
			if listTemplate2 == None :
				continue

			# template duplicate? merge freq counts and then remove it
			if listTemplate1 == listTemplate2 :
				listFreqStats[ nIndex1 ] =  ( nIndex1, listFreqStats[ nIndex1 ][1] + listFreqStats[ nIndex2 ][1] )
				listParsedExtractionPatterns[nIndex2] = None

	# remove blank patterns
	# note: this breaks the index connection back to listParsedExtractionPatterns so we fix it later
	nIndex1 = 0
	while nIndex1 < len(listParsedExtractionPatterns) :
		if listParsedExtractionPatterns[nIndex1] == None :
			del listParsedExtractionPatterns[nIndex1]
			del listFreqStats[nIndex1]
		else :
			# reset index value as it will be broken by deletions
			listFreqStats[nIndex1] = ( nIndex1, listFreqStats[nIndex1][1] )
			nIndex1 = nIndex1 + 1

	# sort pattern indexes by frequency
	listFreqStats = sorted( listFreqStats, key=lambda entry: entry[1], reverse=True )

	# debug
	'''
	dict_openie_config['logger'].info( 'RANKED-NON-DUPLICATES' )
	for ( nIndex, nFreq ) in listFreqStats :
		dict_openie_config['logger'].info(
			'FREQ ' + str(nFreq) + ' ' +
			serialize_extraction_pattern(
				list_pattern = listParsedExtractionPatterns[nIndex],
				dict_openie_config = dict_openie_config
				)
			)
	'''

	# rank templates according to freq of occurance (assumption is frequent patterns are more important)
	if (topN != -1) and (len(listFreqStats) > topN) :
		listFreqStats = listFreqStats[:topN]

	# serialize remaining patterns
	listSerializedPatterns = []
	for ( nIndex, nFreq ) in listFreqStats :
		strSerialized = serialize_extraction_pattern(
				list_pattern = listParsedExtractionPatterns[nIndex],
				dict_openie_config = dict_openie_config
				)
		if strSerialized != None :
			listSerializedPatterns.append( strSerialized )

	# return the serialized patterns
	return listSerializedPatterns

def filter_open_extraction_templates_using_relevance_feedback( list_parsed_patterns = None, list_doc_set_of_propositions = None, list_relevance_feedback = None, dict_openie_config = None ) :
	"""
	filter a set of parsed open pattern templates generated by comp_sem_lib.generate_open_extraction_templates() using relevance feedback.
	relevance feedback is provided in the form of a list of scored extractions.
	any template which creates an extraction, which is incorrect will be removed from the list provided.

	:param list list_parsed_patterns: list of parsed open template extraction patterns generated by comp_sem_lib.parse_extraction_pattern()
	:param list list_doc_set_of_propositions: list of tuples = ( str_index_doc, list_phrases_prop, parsed_pattern_index, list_prop_pattern, list_head_text ). parsed_pattern_index is index of pattern within list_parsed_patterns.
	:param list list_relevance_feedback: list of tuples = ( str_index_doc, list_phrases_prop, str_score ). a score of 0 is incorrect, a score of 1 is correct.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 
	"""

	if not isinstance( list_parsed_patterns, list ) :
		raise Exception( 'invalid list_parsed_patterns' )
	if not isinstance( list_doc_set_of_propositions, list ) :
		raise Exception( 'invalid list_doc_set_of_propositions' )
	if not isinstance( list_relevance_feedback, list ) :
		raise Exception( 'invalid list_relevance_feedback' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listFilterIndex = []

	# compare each proposition in each dcoument to the relevance feedback
	for ( strIndexDoc1, listPhrasesProposition1, nPatternIndex1, nConf1, listPropPattern1, listHeadText1 ) in list_doc_set_of_propositions :

		for ( strIndexDoc2, listPhrasesProposition2, strScore2 ) in list_relevance_feedback :
			if (strIndexDoc1 == strIndexDoc2) and (listPhrasesProposition1 == listPhrasesProposition2) :
				# have we found a proposition that in relevance feedback is marked incorrect? if so add template index to filter list
				if strScore2 == '0' :
					if not nPatternIndex1 in listFilterIndex :
						listFilterIndex.append( nPatternIndex1 )
						break

	# delete filtered templates in reverse order
	listFilterIndex = sorted( listFilterIndex, reverse = True )
	for nIndex in listFilterIndex :
		del list_parsed_patterns[nIndex]


def parse_extraction_pattern( str_pattern = None, dict_openie_config = None ) :
	"""
	parse an open pattern template serialized as a unicode string into a format easier to process by the function comp_sem_lib.match_extraction_patterns().

	the open pattern template represents a directed walk of a dependency parsed sentence graph. the pattern elements are matched left to right. arguments represent noun phrases. relations represent verbs. slots represent context to the relation such as adverbs.

	pattern elements:
		* {varN_1:POS_MARK:pos=TAG|TAG|...;lex=TOKEN|TOKEN|...} = variable node (suffix '_<seed_token_id>') that has a POS tag in the set defined (any if set not defined), and token in the set defined (any if set not defined). POS_MARK = S (start), E (end) or - (somewhere in middle of sent). var = {arg, rel, context, prep ...}
		* <dep_label< = instruction to permanently move up dependency tree via a specific dependency label (abort if dep_label not found)
		* >dep_label> = instruction to permanently move down dependency tree via a specific dependency label (abort if dep_label not found)
		* -dep_label- = instruction to move to siblings, bind next variable then return to the original position in the graph (abort if dep_label not found)
		* +dep_label+ = instruction to move to children, bind next variable then return to the original position in the graph (abort if dep_label not found)

	pattern examples:
		* {arg1_1:} <nsubj< {rel1_1:pos=VBD} >dobj> {arg2_1:}
		* {rel1_1:pos=VBN;lex=announce|choose} <amod< {context0_1:pos=JJ} +case+ {arg1_1:} -appos- {arg2_1:}

	:param unicode str_pattern: serialized open pattern template
	:param dict dict_inverted_index_pos_phrase_patterns: inverted index from soton_corenlppy.re.openie_lib.calc_inverted_index_pos_phrase_patterns()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: list of tuples, each with a pattern instructions e.g. [ ( 'rel', 'rel1_1', '-', ( ('vbz,vbn'),('contains','holds') ) ), ( 'dep_child', 'aux' ), ... ]
	:rtype: list
	"""

	if not isinstance( str_pattern, str ) :
		raise Exception( 'invalid str_pattern' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listResult = []
	listPattern = str_pattern.split(' ')
	for strEntry in listPattern :

		matchObj = regexVariableOpenTemplate.match( strEntry )
		if matchObj != None :

			strType = None
			nIndex = None
			nAddr = None
			nSeedToken = None
			listPOS = []
			listLex = []
			if 'TYPE' in matchObj.groupdict() :
				strType = matchObj.groupdict()['TYPE']

			if 'INDEX' in matchObj.groupdict() :
				strIndex = matchObj.groupdict()['INDEX']
				if strIndex != None :
					nIndex = int( strIndex )

			if 'SEEDTOKEN' in matchObj.groupdict() :
				strSeedTokenID = matchObj.groupdict()['SEEDTOKEN']
				if strSeedTokenID != None :
					nSeedToken = int( strSeedTokenID )

			if 'POS_MARK' in matchObj.groupdict() :
				strPosMark = matchObj.groupdict()['POS_MARK']

			if 'POS' in matchObj.groupdict() :
				strPOS = matchObj.groupdict()['POS']
				if strPOS != None :
					strPOS = unescape_extraction_pattern( strPOS )
					listPOS = strPOS.lower().split('|')
					# remove any empty values
					while '' in listPOS :
						listPOS.remove('')


			if 'LEX' in matchObj.groupdict() :
				strLex = matchObj.groupdict()['LEX']
				if strLex != None :
					strLex = unescape_extraction_pattern( strLex )
					listLex = strLex.lower().split('|')
					# remove any empty values
					while '' in listLex :
						listLex.remove('')

			tupleEntry = ( strType, strType + str(nIndex) + '_' + str(nSeedToken), strPosMark, ( tuple(listPOS),tuple(listLex) ) )

		elif strEntry.startswith( '<' ) :
			if len(strEntry[1:-1]) == 0 :
				raise Exception( 'invalid extraction pattern : <dep< : ' + repr(strEntry) )
			tupleEntry = ( 'dep_parent', strEntry[1:-1] )

		elif strEntry.startswith( '>' ) :
			if len(strEntry[1:-1]) == 0 :
				raise Exception( 'invalid extraction pattern : >dep> : ' + repr(strEntry) )
			tupleEntry = ( 'dep_child', strEntry[1:-1] )

		elif strEntry.startswith( '+' ) :
			if len(strEntry[1:-1]) == 0 :
				raise Exception( 'invalid extraction pattern : +dep+ : ' + repr(strEntry) )
			tupleEntry = ( 'dep_child_returning', strEntry[1:-1] )

		elif strEntry.startswith( '@' ) :
			if len(strEntry[1:-1]) == 0 :
				raise Exception( 'invalid extraction pattern : @dep@ : ' + repr(strEntry) )

			matchObj2 = regexEncodedExtractionImmediateChild.match( strEntry )
			if matchObj2 != None :
				nIndex = None
				nSeedToken = None
				listPOS = []
				listLex = []
				if 'DEP_TYPE' in matchObj2.groupdict() :
					strDepType2 = matchObj2.groupdict()['DEP_TYPE']
				if 'VAR_BASE' in matchObj2.groupdict() :
					strVarBase = matchObj2.groupdict()['VAR_BASE']
				if 'POS' in matchObj2.groupdict() :
					strPOS = matchObj2.groupdict()['POS']
					if strPOS != None :
						strPOS = unescape_extraction_pattern( strPOS )
						listPOS = strPOS.lower().split('|')
						# remove any empty values
						while '' in listPOS :
							listPOS.remove('')
				if 'LEX' in matchObj2.groupdict() :
					strLex = matchObj2.groupdict()['LEX']
					if strLex != None :
						strLex = unescape_extraction_pattern( strLex )
						listLex = strLex.lower().split('|')
						# remove any empty values
						while '' in listLex :
							listLex.remove('')

				if 'VAR_TYPE' in matchObj2.groupdict() :
					strVarType = matchObj2.groupdict()['VAR_TYPE']

				tupleEntry = ( 'dep_child_immediate', strDepType2, ( strVarBase, tuple(listPOS), tuple(listLex) ), strVarType )

			else :
				raise Exception( 'invalid extraction pattern : @dep@ parse : ' + repr(strEntry) + ' : ' + repr(str_pattern) )

		else :
			raise Exception( 'invalid extraction pattern : unknown cmd : ' + repr(strEntry) + ' : ' + repr(str_pattern) )

		listResult.append( tupleEntry )
	
	return listResult

def serialize_extraction_pattern( list_pattern = None, dict_openie_config = None ) :
	"""
	serialize an open pattern template.
	see comp_sem_lib.parse_extraction_pattern()

	:param list list_pattern: parsed pattern from comp_sem_lib.parse_extraction_pattern()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config() 

	:return: serialized pattern
	:rtype: unicode
	"""

	if not isinstance( list_pattern, list ) :
		raise Exception( 'invalid list_pattern' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listPatternComponents = []
	for tupleEntry in list_pattern :

		if not tupleEntry[0] in ( 'dep_parent', 'dep_child', 'dep_child_returning', 'dep_child_immediate' ) :
			strPosMark = tupleEntry[2]

			strVocab = ''
			if len(tupleEntry[3][0]) > 0 :
				# POS upper for serialization (it all gets converted to lower when matching is done anyway)
				listValues = list( tupleEntry[3][0] )
				for nIndex in range(len(listValues)) :
					listValues[nIndex] = escape_extraction_pattern( listValues[nIndex].upper() )
				strVocab = 'pos=' + '|'.join( listValues )

			if len(tupleEntry[3][1]) > 0 :
				if len(strVocab) > 0 :
					strVocab = strVocab + ';'
				# LEX lower for serialization (it all gets converted to lower when matching is done anyway)
				listValues = list( tupleEntry[3][1] )
				for nIndex in range(len(listValues)) :
					listValues[nIndex] = escape_extraction_pattern( listValues[nIndex].lower() )
				strVocab = strVocab + 'lex=' + '|'.join( listValues )

			# arg1_1:pos=VBG|lex=running
			listPatternComponents.append( '{' + tupleEntry[1] + ':' + strPosMark + ':' + strVocab + '}' )

		elif tupleEntry[0] == 'dep_parent' :
			listPatternComponents.append( '<' + tupleEntry[1] + '<' )

		elif tupleEntry[0] == 'dep_child' :
			listPatternComponents.append( '>' + tupleEntry[1] + '>' )

		elif tupleEntry[0] == 'dep_child_returning' :
			listPatternComponents.append( '+' + tupleEntry[1] + '+' )

		elif tupleEntry[0] == 'dep_child_immediate' :
			strVocab = ''
			if len(tupleEntry[2][1]) > 0 :
				# POS upper for serialization (it all gets converted to lower when matching is done anyway)
				listValues = list( tupleEntry[2][1] )
				for nIndex in range(len(listValues)) :
					listValues[nIndex] = escape_extraction_pattern( listValues[nIndex].upper() )
				strVocab = 'pos=' + '|'.join( listValues )

			if len(tupleEntry[2][2]) > 0 :
				if len(strVocab) > 0 :
					strVocab = strVocab + ';'
				# LEX lower for serialization (it all gets converted to lower when matching is done anyway)
				listValues = list( tupleEntry[2][2] )
				for nIndex in range(len(listValues)) :
					listValues[nIndex] = escape_extraction_pattern( listValues[nIndex].lower() )
				strVocab = strVocab + 'lex=' + '|'.join( listValues )

			strVarPattern = tupleEntry[2][0] + ':' + strVocab

			#strVarPattern = tupleEntry[2][0] + ':pos=' + '|'.join( tupleEntry[2][1] ) + ';lex=' + '|'.join( tupleEntry[2][2] )
			listPatternComponents.append( '@' + tupleEntry[1] + ',' + strVarPattern + ',' + tupleEntry[3] + '@' )

		else :
			raise Exception( 'invalid extraction pattern : unknown entry : ' + repr(tupleEntry) )

	return ' '.join( listPatternComponents )

def escape_extraction_pattern( token = None ) :
	"""
	escape extraction pattern tokens.
	replacing | with -ESC_PIPE-, : with -ESC_COLON-, {} with -ESC_LCB- and -ESC_RCB-, [] with -ESC_LSB- and -ESC_LCB-.
	the escape replacement labels are deliberately different from Stanford escaping to avoid conflicts

	:param unicode token: token to escape

	:return: escaped token
	:rtype: unicode
	"""

	if not isinstance( token, str ) :
		raise Exception( 'invalid token' )
	strSafe = token.replace( '|', '-ESC_PIPE-' )
	strSafe = strSafe.replace( ':', '-ESC_COLON-' )
	strSafe = strSafe.replace( '{', '-ESC_LCB-' )
	strSafe = strSafe.replace( '}', '-ESC_RCB-' )
	strSafe = strSafe.replace( '[', '-ESC_LSB-' )
	strSafe = strSafe.replace( ']', '-ESC_RSB-' )
	strSafe = strSafe.replace( ' ', '-SPACE-' )
	return strSafe

def unescape_extraction_pattern( token = None ) :
	"""
	unescape extraction pattern tokens. see comp_sem_lib.escape_extraction_pattern()

	:param unicode token: token to escape

	:return: escaped token
	:rtype: unicode
	"""

	if not isinstance( token, str ) :
		raise Exception( 'invalid token' )
	strSafe = token.replace( '-ESC_PIPE-', '|' )
	strSafe = strSafe.replace( '-ESC_COLON-', ':' )
	strSafe = strSafe.replace( '-ESC_LCB-', '{' )
	strSafe = strSafe.replace( '-ESC_RCB-','}' )
	strSafe = strSafe.replace( '-ESC_LSB-', '[' )
	strSafe = strSafe.replace( '-ESC_RSB-',']' )
	strSafe = strSafe.replace( '-SPACE-',' ' )
	return strSafe

def match_extraction_patterns_batch( dict_document_sent_graphs = {}, list_extraction_patterns = [], dict_collapse_dep_types = {}, dict_assert_true = dict_assertion_true, dict_assert_false = dict_assertion_false, max_processes = 4, dict_openie_config = None ) :
	"""
	apply a set of open pattern templates, parsed using comp_sem_lib.parse_extraction_pattern(), to a dependency graph.
	use multiprocess spawning to maximize the CPU usage as this is a slow process that is CPU intensive.

	the patterns are executed in the order they appear in the list.
	the result of a match is a set of matched variables from the open pattern template, including for each a graph_address (i.e. token position) and collapsed phrase (i.e. dependancy graph collapsed to produce a text phrase for the variable).

	:param dict dict_document_sent_graphs: dict of document ID keys, each value being a list of nltk.parse.DependencyGraph objects representing a sent
	:param list list_extraction_patterns: list of parsed open pattern templates from comp_sem_lib.parse_extraction_pattern()
	:param dict dict_collapse_dep_types: dependency graph types to use when collapsing variable branches = { 'var_type' : set([dep_type, dep_type, ...]), ... }
	:param dict dict_assert_true: dict of language specific vocabulary for tokens asserting truth used for handling negation. use {} to avoid using a negation vocabulary.
	:param dict dict_assert_false: dict of language specific vocabulary for tokens asserting falsehood used for handling negation. use {} to avoid using a negation vocabulary.
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: dict of sent matches = { documentID : [ [ [ ( var_type, var_name, graph_address, collapsed_graph_addresses[], { dep : [ var_name, ... ] } ), ... x Nvar ], ... x Nextract  ] ... x Nsent ] }
	:rtype: dict
	"""

	if not isinstance( dict_document_sent_graphs, dict ) :
		raise Exception( 'invalid dict_document_sent_graphs' )
	if not isinstance( list_extraction_patterns, list ) :
		raise Exception( 'invalid list_extraction_patterns' )
	if not isinstance( dict_collapse_dep_types, dict ) :
		raise Exception( 'invalid dict_collapse_dep_types' )
	if not isinstance( dict_assert_true, dict ) :
		raise Exception( 'invalid dict_assert_true' )
	if not isinstance( dict_assert_false, dict ) :
		raise Exception( 'invalid dict_assert_false' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )
		listQueueResultsPending.append( 0 )

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in dict_document_sent_graphs:
		listSentGraphs = dict_document_sent_graphs[strDocumentID]

		if len(listSentGraphs) == 0 :
			#listQueue[nProcess][0].put( ( strDocumentID, None, None ) )
			listQueueInput[nProcess].append( ( strDocumentID, None, None ) )
			listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] + 1

			# round robin assignment to queues
			nProcess = nProcess + 1
			if nProcess >= max_processes :
				nProcess = 0

		else :
			for nSentIndex in range(len(listSentGraphs)) :
				depObj = listSentGraphs[nSentIndex]
				strSerializedGraph = serialize_dependency_graph( dep_graph = depObj, dict_openie_config = dict_openie_config )

				# listQueue[nProcess][0].put( ( strDocumentID, nSentIndex, strSerializedGraph ) )
				listQueueInput[nProcess].append( ( strDocumentID, nSentIndex, strSerializedGraph ) )
				listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] + 1

				# round robin assignment to queues
				nProcess = nProcess + 1
				if nProcess >= max_processes :
					nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.copy( dict_openie_config )
	dictConfigCopy['logger'] = None

	# setup a process pool as the template generation is very CPU intensive so we need to use all cores on a machine to speed it up
	listProcesses = []
	for nProcess in range(max_processes) :
		dict_openie_config['logger'].info( 'starting process ' + str(nProcess) + ' with ' + str( len(listQueueInput[nProcess]) ) + ' sent graphs [extract]' )

		processWorker = multiprocessing.Process(
			target = match_extraction_patterns_batch_worker,
			args = (
				listQueue[nProcess],
				list_extraction_patterns,
				dict_collapse_dep_types,
				dict_assert_true,
				dict_assert_false,
				1,
				nProcess,
				dictConfigCopy )
			)
		listProcesses.append( processWorker )


	# write number of documents to expect
	for nProcess in range(max_processes) :
		listQueue[nProcess][0].put( len(listQueueInput[nProcess]) )

	for nProcess in range(max_processes) :
		listProcesses[nProcess].start()

	# write all the input (sync to ensure in queues are limited in size)
	bFinishedInput = False
	while bFinishedInput == False :

		for nProcess in range(max_processes) :

			while len(listQueueInput[nProcess]) > 0 :

				# check for input queue overload (which can cause multiprocess Queue handling errors and lost results).
				# pause until the queue is smaller if this is the case.
				if listQueue[nProcess][0].qsize() > 100 :
					break
				
				# write entry and remove from list
				listQueue[nProcess][0].put( listQueueInput[nProcess].pop(0) )

		bFinishedInput = True
		for nProcess in range(max_processes) :
			if len(listQueueInput[nProcess]) > 0 :
				# input data left so pause and try to upload again
				bFinishedInput = False
				time.sleep(1)

	dict_openie_config['logger'].info( 'documents written OK  [extract]' )

	try :
		dictOutputResults = {}

		# download the results from each process queue in a round robbin way until they are all read in
		# note: do not use blocking queues or thread joins (just an error queue) to avoid issues with queues closing but still being written to (if thread error occurs)
		#       e.g. IOError: [Errno 232] The pipe is being closed
		bFinished = False
		bError = False
		while (bFinished == False) and (bError == False) :

			bPause = True

			# check each process and try to get (a) errors (b) 1 result each
			for nProcess in range(max_processes) :

				# does this process still have work to do?
				if listQueueResultsPending[nProcess] > 0 :

					# non-blocking attempt to get errors
					try :
						strErrorMsg = listQueue[nProcess][2].get( False )

						dict_openie_config['logger'].info( '\tprocess ' + str(nProcess) + ' [extract] failure > ' + strErrorMsg )

						# expect no more results from this process
						listQueueResultsPending[nProcess] = 0

						# flush input buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][0].empty() == False :
							listQueue[nProcess][0].get()

						# flush output buffer so the queue background thread can terminate (and thus the main process can terminate)
						while listQueue[nProcess][1].empty() == False :
							listQueue[nProcess][1].get()

						bError = True

						break
					except queue.Empty :
						pass


					# non-blocking attempt to get a result
					try :
						( strDocumentID, nSentIndex, listExtractions ) = listQueue[nProcess][1].get( False )

						#dict_openie_config['logger'].info( 'result from p' + str(nProcess) + ' : s' + str(nSentIndex) + ' : ' + strDocumentID )

						# process result
						if not strDocumentID in dictOutputResults :
							dictOutputResults[strDocumentID] = []

						if nSentIndex != None :
							if len( dictOutputResults[strDocumentID] ) < nSentIndex + 1 :
								# make the list the right length (with empty lists) as we are merging fragments of sents across the processes
								for nExtra in range( len( dictOutputResults[strDocumentID] ), nSentIndex + 1 ) :
									dictOutputResults[strDocumentID].append( [] )

							dictOutputResults[strDocumentID][nSentIndex] = listExtractions

						listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] - 1
						bPause = False

					except queue.Empty :
						pass

			# more results?
			bFinished = True
			for nProcess in range(max_processes) :
				if listQueueResultsPending[nProcess] > 0 :
					bFinished = False

			# pause for 1 second if we did not get any results to give workers a change to make them
			if (bFinished == False) and (bPause == True) :
				time.sleep(1)

		# errors?
		if bError == True :
			raise Exception( 'errors processing request (see log)' )

		dict_openie_config['logger'].info( 'results aggregated OK [extract]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input quete before
		time.sleep(2)

		# begin cleanup
		dict_openie_config['logger'].info( 'tidying up from worker processes [extract]' )
		( exctype, value ) = sys.exc_info()[:2]
		if exctype != None :
			dict_common_config['logger'].info( 'Exception (will continue) : ' + repr( ( exctype, value ) ) )

		for nProcess in range(max_processes) :
			# ensure all processes are terminates
			if listProcesses[nProcess] != None :
				if listProcesses[nProcess].is_alive() == True :
					listProcesses[nProcess].terminate()

			# ensure all queues for this thread are empty and closed
			for nQueue in range(len(listQueue[nProcess])) :
				while listQueue[nProcess][nQueue].empty() == False :
					listQueue[nProcess][nQueue].get()
				#listQueue[nProcess][nQueue].close()

		dict_openie_config['logger'].info( 'tidy up complete [extract]' )

	# all done
	return dictOutputResults


def match_extraction_patterns_batch_worker( tuple_queue = None, list_extraction_patterns = [], dict_collapse_dep_types = {}, dict_assert_true = dict_assertion_true, dict_assert_false = dict_assertion_false, pause_on_start = 0, process_id = 0, dict_openie_config = None ) :
	"""
	worker thread for comp_sem_lib.match_extraction_patterns_batch()

	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). queueIn has tuples of ( doc_id, sent_index, serialized nltk.parse.DependencyGraph object ). queueOut has tuples of ( doc_id, sent_index, list_extractions ).
	:param list list_extraction_patterns: list of parsed open pattern templates from comp_sem_lib.parse_extraction_pattern()
	:param dict dict_collapse_dep_types: dependency graph types to use when collapsing variable branches = { 'var_type' : set([dep_type, dep_type, ...]), ... }
	:param dict dict_assert_true: dict of language specific vocabulary for tokens asserting truth used for handling negation. use {} to avoid using a negation vocabulary.
	:param dict dict_assert_false: dict of language specific vocabulary for tokens asserting falsehood used for handling negation. use {} to avoid using a negation vocabulary.
	:param int pause_on_start: number of seconds to delay thread startup before CPU intensive work begins (to allow other workers to startup also)
	:param int process_id: ID of process for logging purposes
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()
	"""

	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )
	if not isinstance( list_extraction_patterns, list ) :
		raise Exception( 'invalid list_extraction_patterns' )
	if not isinstance( dict_collapse_dep_types, dict ) :
		raise Exception( 'invalid dict_collapse_dep_types' )
	if not isinstance( dict_assert_true, dict ) :
		raise Exception( 'invalid dict_assert_true' )
	if not isinstance( dict_assert_false, dict ) :
		raise Exception( 'invalid dict_assert_false' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.copy( dict_openie_config )

		logger = logging.getLogger( __name__ )
		if len(logger.handlers) == 0 :
			hdlr = logging.StreamHandler( stream = sys.stdout )
			LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
			fmt = logging.Formatter( fmt = LOG_FORMAT )
			hdlr.setFormatter( fmt )
			logger.addHandler( hdlr )
		logger.setLevel( logging.INFO )

		dictConfigCopy['logger'] = logger

		# pause 1 second to allow all other worker threads to start properly (otherwise startup might be delayed as CPU is grabbed by first workers)
		time.sleep( pause_on_start )

		# read number of documents
		nDocumentMax = tuple_queue[0].get()

		logger.info( 'worker process started (' + str(process_id) + ') = ' + str(nDocumentMax) + ' docs [extract]' )

		# read all input data to process
		listGraphsToProcess = []
		for nDocument in range(nDocumentMax) :

			# get tokens to POS tag
			( strDocumentID, nSentIndex, strSerializedGraph ) = tuple_queue[0].get()
			listGraphsToProcess.append( ( strDocumentID, nSentIndex, strSerializedGraph ) )

		# loop on input queue and get extractions for each sent in each document
		for ( strDocumentID, nSentIndex, strSerializedGraph ) in listGraphsToProcess :

			#logger.info( 'URI (' + str(process_id) + ') = ' + strDocumentID )

			if nSentIndex == None :
				tuple_queue[1].put( ( strDocumentID, None, None ) )
			else :
				# make a NLTK dep graph object
				depObj = nltk.parse.DependencyGraph( tree_str = strSerializedGraph, top_relation_label = 'root', cell_separator = '\t' )

				# apply patterns to get matches
				listMatches = match_extraction_patterns(
					dep_graph = depObj,
					list_extraction_patterns = list_extraction_patterns,
					dict_collapse_dep_types = dict_collapse_dep_types,
					dict_assert_true = dict_assert_true,
					dict_assert_false = dict_assert_false,
					dict_openie_config = dictConfigCopy )
				
				# add result to queue
				tuple_queue[1].put( ( strDocumentID, nSentIndex, copy.copy( listMatches ) ) )

			# micro delay to allow CPU balancing
			time.sleep( 0.001 )

			# check for output queue overload (which can cause multiprocess Queue handling errors and lost results).
			# pause until the queue is smaller if this is the case.
			while tuple_queue[1].qsize() > 100 :
				time.sleep( 1 )

		logger.info('process ended (' + str(process_id) + ') [extract]')

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'match_extraction_patterns_batch_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )


# func to match patterns to dep graph and extract arg,rel and slot values
def match_extraction_patterns( dep_graph = None, list_extraction_patterns = [], dict_collapse_dep_types = {}, dict_assert_true = dict_assertion_true, dict_assert_false = dict_assertion_false, dict_openie_config = None ) :
	"""
	apply a set of open pattern templates, parsed using comp_sem_lib.parse_extraction_pattern(), to a dependency graph.
	the patterns are executed in the order they appear in the list, and all possible matches are returned (a pattern could be materialized in several ways if there are multiple dep options for example)
	the result of a match is a set of matched variables from the open pattern template, including for each a graph_address (i.e. token position) and collapsed phrase (i.e. dependancy graph collapsed to produce a text phrase for the variable).

	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param list list_extraction_patterns: list of parsed open pattern templates from comp_sem_lib.parse_extraction_pattern()
	:param dict dict_collapse_dep_types: dependency graph types to use when collapsing variable branches = { 'var_type' : set([dep_type, dep_type, ...]), ... }
	:param dict dict_assert_true: dict of language specific vocabulary for tokens asserting truth used for handling negation. use {} to avoid using a negation vocabulary.
	:param dict dict_assert_false: dict of language specific vocabulary for tokens asserting falsehood used for handling negation. use {} to avoid using a negation vocabulary.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of matches, each with a list of variables from the matched pattern, or [] if no match occured = [ [ ( var_type, var_name, graph_address, collapsed_graph_addresses[], dictConnection{}, pattern_index ), ... ], ... ]. dictConnection is obtained from get_variables_connections()
	:rtype: list
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph  ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( list_extraction_patterns, list ) :
		raise Exception( 'invalid list_extraction_patterns' )
	if not isinstance( dict_collapse_dep_types, dict ) :
		raise Exception( 'invalid dict_collapse_dep_types' )
	if not isinstance( dict_assert_true, dict ) :
		raise Exception( 'invalid dict_assert_true' )
	if not isinstance( dict_assert_false, dict ) :
		raise Exception( 'invalid dict_assert_false' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listResultsAllMatches = []

	#dict_openie_config['logger'].info( 'GRAPH ' + repr(dep_graph.to_dot()) )

	# loop on each extraction pattern
	for nIndexExtraction in range(len(list_extraction_patterns)) :
		listExtractionPattern = list_extraction_patterns[nIndexExtraction]

		#dict_openie_config['logger'].info( 'MATCHING ' + repr(listExtractionPattern) )

		# try each node in the dependency graph as a starting point
		for nStartAddress in dep_graph.nodes :

			#dict_openie_config['logger'].info( 'ADDR ' + repr(nStartAddress) )

			listResultSet = []
			pattern_match_recurse_into_graph(
				dep_graph = dep_graph,
				graph_address = nStartAddress,
				pattern_spec = listExtractionPattern,
				pattern_pos = 0,
				pattern_result = [],
				pattern_success = listResultSet,
				dict_openie_config = dict_openie_config )
			
			if len(listResultSet) > 0 :

				# process all possible matches of this pattern
				# listResult = list of vars extracted = [(var_type, var_name, graph_address), ...] at this stage, but we will append values to each entry
				for listResult in listResultSet :

					# the extraction is based on a walk so bound variables might be visited several times.
					# remove all but the first instance of each bound variable
					nIndex1 = 0
					while nIndex1 < len(listResult) :
						strVarName1 = listResult[nIndex1][1]

						nIndex2 = nIndex1 + 1
						while nIndex2 < len(listResult) :
							strVarName2 = listResult[nIndex2][1]
							if strVarName2 == strVarName1 :
								# duplicate so remove it from list
								del listResult[nIndex2]
							else :
								nIndex2 = nIndex2 + 1

						nIndex1 = nIndex1 + 1

					# compile a list of returned addresses so they can be excluded from any collapsed rel graph to avoid duplication of text
					listReturnedAddresses = []
					nLastHeadAddr = None
					nFirstHeadAddr = None
					for nIndex in range(len(listResult)) :
						nAddress = listResult[nIndex][2]
						listReturnedAddresses.append( nAddress )
						if (nLastHeadAddr == None) or (nAddress > nLastHeadAddr) :
							nLastHeadAddr = nAddress
						if (nFirstHeadAddr == None) or (nAddress < nFirstHeadAddr) :
							nFirstHeadAddr = nAddress
					setReturnedAddresses = set( listReturnedAddresses )

					# collapse dependency graph branch for this variable
					# pass#1 using head address range for variable_head_range, so we get addresses WITHOUT any 'not_after_last_var' or 'not_before_first_var' entries outside head range
					nCollapsedRangeMin = None
					nCollapsedRangeMax = None
					for nIndex in range(len(listResult)) :
						strType = listResult[nIndex][0]
						nAddress = listResult[nIndex][2]
						listAddressCollapsed = []

						if strType in dict_collapse_dep_types :
							# arg, rel, prep
							listAddressCollapsed = collapse_graph_to_make_phrase(
								dep_graph = dep_graph,
								node_address = nAddress,
								allowed_dep_set = dict_collapse_dep_types[strType],
								forbidden_address_set = setReturnedAddresses,
								variable_head_range = ( nFirstHeadAddr,nLastHeadAddr ),
								dict_openie_config = dict_openie_config )
						else :
							# context
							listAddressCollapsed = [ nAddress ]

						listResult[nIndex].append( listAddressCollapsed )

						if nCollapsedRangeMin == None :
							nCollapsedRangeMin = min( listAddressCollapsed )
						else :
							nCollapsedRangeMin = min( min( listAddressCollapsed ), nCollapsedRangeMin )

						if nCollapsedRangeMax == None :
							nCollapsedRangeMax = max( listAddressCollapsed )
						else :
							nCollapsedRangeMax = max( max( listAddressCollapsed ), nCollapsedRangeMax )

					# collapse dependency graph branch for this variable
					# pass#1 using collapsed address range for variable_head_range, so we get addresses WITH any 'not_after_last_var' or 'not_before_first_var' entries outside head range but inside collapsed address range
					for nIndex in range(len(listResult)) :
						strType = listResult[nIndex][0]
						nAddress = listResult[nIndex][2]
						listAddressCollapsed = []

						if strType in dict_collapse_dep_types :
							# arg, rel, prep
							listAddressCollapsed = collapse_graph_to_make_phrase(
								dep_graph = dep_graph,
								node_address = nAddress,
								allowed_dep_set = dict_collapse_dep_types[strType],
								forbidden_address_set = setReturnedAddresses,
								variable_head_range = ( nCollapsedRangeMin,nCollapsedRangeMax ),
								dict_openie_config = dict_openie_config )
						else :
							# context
							listAddressCollapsed = [ nAddress ]

						# replace pass#1 with pass#2
						listResult[nIndex][-1] = listAddressCollapsed

					# record dep connections between variables
					for nIndex in range(len(listResult)) :
						dictConnection = get_variables_connections(
							check_index = nIndex,
							list_variables = listResult,
							dep_graph = dep_graph,
							dict_openie_config = dict_openie_config )
						listResult[nIndex].append( dictConnection )

					# append the extraction template index that generated this extraction (useful for relevance feedback later)
					for nIndex in range(len(listResult)) :
						listResult[nIndex].append( nIndexExtraction )

					# success
					listResultsAllMatches.append( listResult )

	# all done
	return listResultsAllMatches


def pattern_match_recurse_into_graph( dep_graph = None, graph_address = 0, force_next_address = None, pattern_spec = [], pattern_pos = 0, pattern_result = None, pattern_success = None, dict_openie_config = None ) :
	"""
	internal function called by comp_sem_lib.match_extraction_patterns()
	try nodes in the dependency graph using a breadth first search strategy. for each search node try to apply the open pattern template and recuse until either failure or success (end of template)
	the reference parameter pattern_result contains the variables matched at what ever level of recursion the algoriothm has got to.
	memory note - a copy of the variables found is kept at each seatch node, so if the breadth first search has a lot of combinations then the memory footprint will get large.

	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param int graph_address: address is the token index in the dependency graph
	:param int force_next_address: address to force any recursive call (allows a temp node to be explored and then switch back to a previous position in graph)
	:param list pattern_spec: parsed open pattern template from comp_sem_lib.parse_extraction_pattern()
	:param int pattern_pos: current position in parsed open pattern template 
	:param list pattern_result: current partially populated patterns = [(var_type, var_name, graph_address), ... ]
	:param list pattern_success: successful fully populated patterns = [(var_type, var_name, graph_address), ... ]
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph  ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( graph_address, int ) :
		raise Exception( 'invalid graph_address' )
	if not isinstance( force_next_address, (type(None),int) ) :
		raise Exception( 'invalid force_next_address' )
	if not isinstance( pattern_spec, list ) :
		raise Exception( 'invalid pattern_spec' )
	if not isinstance( pattern_pos, int ) :
		raise Exception( 'invalid pattern_pos' )
	if not isinstance( pattern_result, list ) :
		raise Exception( 'invalid pattern_result' )
	if not isinstance( pattern_success, list ) :
		raise Exception( 'invalid pattern_success' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# check we have not navigated to a node that does not exist (prob impossible but best check).
	# dep graph nodes use a defaultdict so trying to access a missing node will actually insert a blank entry (!)
	# which then changes the nodes tree and the original iteration will fail (and its a very bad thing to do anyway)
	if not graph_address in dep_graph.nodes :
		return

	# blank nodes always fail a match
	if dep_graph.nodes[ graph_address ]['address'] == None :
		return

	# dep_graph.nodes = { address = node_index, word = node_label, lemma, ctag = node_pos, tag, feats, head, deps = { rel : [address,address ...] }, rel = dep_type }
	strPOS = dep_graph.nodes[ graph_address ]['ctag']
	if strPOS != None :
		strPOS = strPOS.lower()

	strToken = dep_graph.nodes[ graph_address ]['word']
	if strToken != None :
		strToken = strToken.lower()

	nHeadAddress = dep_graph.nodes[ graph_address ]['head']

	# end of the pattern without failure, so success!
	if pattern_pos >= len( pattern_spec ) :
		#dict_openie_config['logger'].info( 'success' )

		# add successful result to the list of successful results
		pattern_success.append( copy.copy( pattern_result ) )
		return

	# get next pattern instruction
	tupleInstruction = pattern_spec[pattern_pos]

	#dict_openie_config['logger'].info( str(pattern_pos) + ' of ' + str(len(pattern_spec)) + ' looking for ' + repr(tupleInstruction) + ' within ' + repr( (strPOS, strToken) ) )

	if not tupleInstruction[0] in ( 'dep_parent', 'dep_child', 'dep_child_returning', 'dep_child_immediate' ) :
		# check pos marker (start or end address is its not -)
		bPosMark = True
		strPosMark = tupleInstruction[2]
		if strPosMark == 'S' :
			if graph_address != 1 :
				bPosMark = False
		elif strPosMark == 'E' :
			if graph_address != len( dep_graph.nodes ) - 1 :
				bPosMark = False

		# check POS tag
		bPOS = True
		if len( tupleInstruction[3][0] ) > 0 :
			bPOS = False
			if strPOS in tupleInstruction[3][0] :
				bPOS = True

		# check lexical tokens
		bLex = True
		if len( tupleInstruction[3][1] ) > 0 :
			bLex = False
			if strToken in tupleInstruction[3][1] :
				bLex = True

		# match ok?
		if (strToken != None) and (bLex == True) and (bPOS == True) and (bPosMark == True) :
			# add matched node to result
			strVarType = tupleInstruction[0]
			strVarName = tupleInstruction[1]

			# make a new list for data node
			listResultNode = [ strVarType, strVarName, graph_address ]

			# make a deep copy of the current pattern_result (to avoid it changing structure in other search paths)
			listPatternResultDeepCopy = copy.deepcopy( pattern_result )

			# add to deep copy
			listPatternResultDeepCopy.append( listResultNode )

			# process next pattern instruction
			if force_next_address == None :
				pattern_match_recurse_into_graph(
					dep_graph = dep_graph,
					graph_address = graph_address,
					force_next_address = None,
					pattern_spec = pattern_spec,
					pattern_pos = pattern_pos + 1,
					pattern_result = listPatternResultDeepCopy,
					pattern_success = pattern_success,
					dict_openie_config = dict_openie_config )
			else :
				pattern_match_recurse_into_graph(
					dep_graph = dep_graph,
					graph_address = force_next_address,
					force_next_address = None,
					pattern_spec = pattern_spec,
					pattern_pos = pattern_pos + 1,
					pattern_result = listPatternResultDeepCopy,
					pattern_success = pattern_success,
					dict_openie_config = dict_openie_config )

	elif tupleInstruction[0] == 'dep_parent' :
		# check head has the required dependency
		dictDeps = dep_graph.nodes[ nHeadAddress ]['deps']
		strDepName = tupleInstruction[1]
		if strDepName in dictDeps :
			if graph_address in dictDeps[ strDepName ] :

				# always allow revisiting addresses up the tree
				#dict_openie_config['logger'].info( 'dep_parent ' + repr( (nHeadAddress, strDepName) ) + ' => ' + str(pattern_pos) + ' of ' + str(len(pattern_spec)) )
				pattern_match_recurse_into_graph(
					dep_graph = dep_graph,
					graph_address = nHeadAddress,
					force_next_address = None,
					pattern_spec = pattern_spec,
					pattern_pos = pattern_pos + 1,
					pattern_result = pattern_result,
					pattern_success = pattern_success,
					dict_openie_config = dict_openie_config )

	elif tupleInstruction[0] == 'dep_child' :
		# check this node has required dependency
		strDepName = tupleInstruction[1]
		dictDeps = dep_graph.nodes[ graph_address ]['deps']
		if strDepName in dictDeps :

			# if the variable name after this move (if there is one) has previously been bound to a <varname_addr>, then this revisit move must go to that previously bound address
			nBoundAddress = None
			if pattern_pos+1 < len( pattern_spec ) :
				tupleInstructionNext = pattern_spec[pattern_pos+1]
				strNextVarName = tupleInstructionNext[1]

				for (strType, strVar, nAddressResult) in pattern_result :
					if strVar == strNextVarName :
						nBoundAddress = nAddressResult
						#dict_openie_config['logger'].info( 'bound ' + repr( (nBoundAddress, strNextVarName) ) )
						break

			for nAddressChild in dictDeps[ strDepName ] :

				bValid = True

				# ensure bound variable addresses are reused
				# otherwise allow any previously unused address. this ensures the graph walk does not ping pong (up and down) between two nodes
				if nBoundAddress != None :
					if nAddressChild != nBoundAddress :
						bValid = False
				else :
					for (strType, strVar, nAddressResult) in pattern_result :
						if nAddressResult == nAddressChild :
							bValid = False
							break

				if bValid == True :

					#dict_openie_config['logger'].info( 'dep_child ' + repr( (nAddressChild, strDepName) ) + ' => ' + str(pattern_pos) + ' of ' + str(len(pattern_spec)) )
					pattern_match_recurse_into_graph(
						dep_graph = dep_graph,
						graph_address = nAddressChild,
						force_next_address = None,
						pattern_spec = pattern_spec,
						pattern_pos = pattern_pos + 1,
						pattern_result = pattern_result,
						pattern_success = pattern_success,
						dict_openie_config = dict_openie_config )

	elif tupleInstruction[0] == 'dep_child_immediate' :
		# check this node has required dependency
		strDepName = tupleInstruction[1]
		( strVarBase, listPOSConstraint, listLexConstraint ) = tupleInstruction[2]
		strVarType = tupleInstruction[3]

		dictDeps = dep_graph.nodes[ graph_address ]['deps']
		if strDepName in dictDeps :

			nMaxID = 0
			for (strVarTypeLookup, strVarNameLookup, nAddressLookup) in pattern_result :
				listComponents = strVarNameLookup.split('_')
				strVarBaseLookup = listComponents[0]
				nVarID = int( listComponents[1] )
				if strVarBaseLookup == strVarBase :
					if nMaxID < nVarID :
						nMaxID = nVarID

			# make a deep copy of the current pattern_result (to avoid it changing structure in other search paths)
			nOriginalResultLen = len( pattern_result )
			listPatternResultDeepCopy = copy.deepcopy( pattern_result )

			# add all immediate children with this dep type into the result
			for nAddressChild in dictDeps[ strDepName ] :

				bValid = True

				# ensure variable addresses has not already been returned somehow (should be impossible for a valid template)
				for (strType, strVar, nAddressResult) in pattern_result :
					if nAddressResult == nAddressChild :
						bValid = False
						break

				# get child POS and token
				strPOSChild = dep_graph.nodes[ nAddressChild ]['ctag']
				if strPOSChild != None :
					strPOSChild = strPOSChild.lower()
				else :
					bValid = False

				strTokenChild = dep_graph.nodes[ nAddressChild ]['word']
				if strTokenChild != None :
					strTokenChild = strTokenChild.lower()
				else :
					bValid = False

				# check POS and lex constraints
				if len(listPOSConstraint) > 0 :
					if not strPOSChild in listPOSConstraint :
						bValid = False
				if len(listLexConstraint) > 0 :
					if not strTokenChild in listLexConstraint :
						bValid = False

				if bValid == True :
					# create a variable name by adding a unique number to its base
					nMaxID = nMaxID + 1
					strVarName = strVarBase + '_' + str(nMaxID)

					# make a new list for data node
					listResultNode = [ strVarType, strVarName, nAddressChild ]

					# add to deep copy
					listPatternResultDeepCopy.append( listResultNode )

			# only proceed if we have added a new variable. otherwise the result will be missing the var type defined under the dep_child_immediate (resulting in potentially massive sets of partial matches)
			nNewResultLen = len( listPatternResultDeepCopy )
			if nNewResultLen > nOriginalResultLen :

				#dict_openie_config['logger'].info( 'dep_child_immediate ' + repr( (nAddressChild, strDepName) ) + ' => ' + str(pattern_pos) + ' of ' + str(len(pattern_spec)) )
				pattern_match_recurse_into_graph(
					dep_graph = dep_graph,
					graph_address = graph_address,
					force_next_address = None,
					pattern_spec = pattern_spec,
					pattern_pos = pattern_pos + 1,
					pattern_result = listPatternResultDeepCopy,
					pattern_success = pattern_success,
					dict_openie_config = dict_openie_config )

	elif tupleInstruction[0] == 'dep_child_returning' :
		# for all children try to match next node
		# when done return to this node and continue

		# check this node has required dependency
		dictDeps = dep_graph.nodes[ graph_address ]['deps']
		strDepName = tupleInstruction[1]
		if strDepName in dictDeps :

			# if the variable name after this move (if there is one) has previously been bound to an address, then this revisit move must go to the previously bound address
			nBoundAddress = None
			if pattern_pos+1 < len( pattern_spec ) :
				tupleInstructionNext = pattern_spec[pattern_pos+1]
				strNextVarName = tupleInstructionNext[1]

				for (strType, strVar, nAddressResult) in pattern_result :
					if strVar == strNextVarName :
						nBoundAddress = nAddressResult
						#dict_openie_config['logger'].info( 'bound ' + repr( (nBoundAddress, strNextVarName) ) )
						break

			for nAddressChild in dictDeps[ strDepName ] :

				bValid = True

				# ensure bound variable addresses are reused
				# otherwise allow any previously unused address. this ensures the graph walk does not ping pong (up and down) between two nodes
				if nBoundAddress != None :
					if nAddressChild != nBoundAddress :
						bValid = False
				else :
					for (strType, strVar, nAddressResult) in pattern_result :
						if nAddressResult == nAddressChild :
							bValid = False
							break

				if bValid == True :

					#dict_openie_config['logger'].info( 'dep_child ' + repr( (nAddressChild, strDepName) ) + ' => ' + str(pattern_pos) + ' of ' + str(len(pattern_spec)) )
					pattern_match_recurse_into_graph(
						dep_graph = dep_graph,
						graph_address = nAddressChild,
						force_next_address = graph_address,
						pattern_spec = pattern_spec,
						pattern_pos = pattern_pos + 1,
						pattern_result = pattern_result,
						pattern_success = pattern_success,
						dict_openie_config = dict_openie_config )


def parse_allowed_dep_set( allowed_dep_set = None, dict_openie_config = None ) :
	"""
	internal function used by generate_open_extraction_templates() and match_extraction_patterns() via collapse_graph_to_make_phrase()

	:param set allowed_dep_set: set of allowed dependancy types to include in the collapsed phrase. supports lexical constraints (e.g. 'case:of') for a finer grained filtering. None to allow any dep.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of tuple = [ ( dep, wild_card, [ conditionals, ... ] ), ... ]
	:rtype: list
	"""

	if not isinstance( allowed_dep_set, ( set, type(None) ) ) :
		raise Exception( 'invalid allowed_dep_set' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# parse allowed dep set
	# e.g.
	#   case[not_before_first_var,not_after_last_var]
	#   compound:*
	#   compound:*[not_before_first_var]
	listAllowed = []
	if allowed_dep_set != None :
		for strAllowedDep in allowed_dep_set :
			if '[' in strAllowedDep :
				nPos1 = strAllowedDep.index('[')
				listConditionals = strAllowedDep[ nPos1+1 : -1 ].split(',')
				strAllowedDepParsed = strAllowedDep[ : nPos1 ]
			else :
				listConditionals = []
				strAllowedDepParsed = strAllowedDep

			if strAllowedDepParsed.endswith(':*') :
				tupleAllowed = ( strAllowedDepParsed[:-2], True, tuple( listConditionals ) )
			else :
				tupleAllowed = ( strAllowedDepParsed, False, tuple( listConditionals ) )

			listAllowed.append( tupleAllowed )
	
	return listAllowed



def collapse_graph_to_make_phrase( dep_graph = None, node_address = None, allowed_dep_set = None, forbidden_address_set = set([]), variable_head_range = None, search_depth = 0, dict_openie_config = None ) :
	"""
	collapse a dependency graph and generate a set of text tokens representing a phrase for this node.
	ensure all tokens appear sequentially around the root node address (e.g. 'the only other plan' -> 'the other plan' is not allowed, 'only other plan' is allowed)

	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param int node_address: address is the token index in the dependency graph
	:param set allowed_dep_set: set of allowed dependancy types to include in the collapsed phrase. supports lexical constraints (e.g. 'case:of') for a finer grained filtering. None to allow any dep.
	:param set forbidden_address_set: set of forbidden dependancy graph addresses to avoid in the collapsed phrase
	:param int variable_head_range: tuple (first var head addr, last var head addr) for use with metadata commands ('not_before_first_var', 'not_after_last_var')
	:param int search_depth: internal argument, recursion depth
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: success or failure of pattern matching. the reference argument pattern_result will contain the variables matched if this is successful.
	:rtype: bool
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( node_address, int ) :
		raise Exception( 'invalid node_address' )
	if not isinstance( allowed_dep_set, ( set, type(None) ) ) :
		raise Exception( 'invalid allowed_dep_set' )
	if not isinstance( forbidden_address_set, set ) :
		raise Exception( 'invalid forbidden_address_set' )
	if not isinstance( variable_head_range, tuple ) :
		raise Exception( 'invalid variable_head_range' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listResult = []
	listResult.append( node_address )

	# parse allowed dep structure
	listAllowed = parse_allowed_dep_set(
		allowed_dep_set = allowed_dep_set,
		dict_openie_config = dict_openie_config )

	# compile address list under target node address
	dictDeps = dep_graph.nodes[ node_address ]['deps']
	for strDep in dictDeps :
		for nAddressChild in dictDeps[ strDep ] :
			if not nAddressChild in forbidden_address_set :

				# check dep type is allowed and the child address is not outside limits for that dep type
				bAllowed = False
				if allowed_dep_set == None :
					bAllowed = True
				else :
					for tupleAllowed in listAllowed :
						if (tupleAllowed[1] == False) and (strDep == tupleAllowed[0]) :
							if ('not_before_first_var' in tupleAllowed[2]) and (variable_head_range[0] > nAddressChild) :
								continue
							if ('not_after_last_var' in tupleAllowed[2]) and (variable_head_range[1] < nAddressChild) :
								continue
							bAllowed = True

						elif (tupleAllowed[1] == True) and (strDep.startswith( tupleAllowed[0] ) == True) :
							if ('not_before_first_var' in tupleAllowed[2]) and (variable_head_range[0] > nAddressChild) :
								continue
							if ('not_after_last_var' in tupleAllowed[2]) and (variable_head_range[1] < nAddressChild) :
								continue
							bAllowed = True

				if bAllowed == True :
					listResult.extend(
						collapse_graph_to_make_phrase(
							dep_graph = dep_graph,
							node_address = nAddressChild,
							allowed_dep_set = allowed_dep_set,
							forbidden_address_set = forbidden_address_set,
							variable_head_range = variable_head_range,
							search_depth = search_depth + 1,
							dict_openie_config = dict_openie_config )
						)

	# sort by address order so the entity tokens appears as they were originally written
	listResult = sorted( listResult )

	# all done
	return listResult

def check_for_negation( dep_graph = None, node_address = None, lang = 'en', dict_assert_true = dict_assertion_true, dict_assert_false = dict_assertion_false, dict_openie_config = None ) :
	"""
	check dependency graph for evidence of negation of node or genuine/fake claims with this node as the subject
	negation strategy:
		* check neg dep
		* check amod dep leading to a true|false assertion (and then check for a neg dep)
		* check head for [nsubj,nsubjpass] dep originating from a true|false assertion (and then check head for a neg dep)

	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param int node_address: address is the token index in the dependency graph
	:param str lang: ISO 639-1 2 character language codes e.g. ['en','fr']
	:param dict dict_assert_true: dict of language specific vocabulary for tokens asserting truth. use {} to avoid using a negation vocabulary.
	:param dict dict_assert_false: dict of language specific vocabulary for tokens asserting falsehood. use {} to avoid using a negation vocabulary.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: negation status = (negated, genuine) = (true|None, true|false|None)
	:rtype: tuple
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( node_address, int ) :
		raise Exception( 'invalid node_address' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# example: negation
	# have > nsubj > John > neg > not == did not have
	# have > ... dobj > flower > conj > lotus > conj > poppy > nmod > statue > neg > no == have a flower, lotus and poppy but no statue

	# example: adjective modifiers (false, true) which itself can be negated
	# was > nsubj > report > amod > false == was a false report
	# was > nsubj > report > amod > false > neg > not == was not a false report
	# rumour > nmod > riots > acl:relcl > true > neg > not == rumour riots not true

	# check child deps
	dictDeps = dep_graph.nodes[ node_address ]['deps']
	for strDep in dictDeps :
		# child neg = this node is negated
		if strDep == 'neg' :
			return (True,None)

		# check for true|false assertions (which themselves might be negated)
		if (strDep == 'amod') or (strDep.startswith('acl') == True) :
			for nAddressChild in dictDeps[strDep] :
				strToken = dep_graph.nodes[ nAddressChild ]['word']
				if strToken != None :

					if (lang in dict_assert_true) and (strToken.lower() in dict_assert_true[lang]) :

						bNeg = False
						dictDepsChild = dep_graph.nodes[ nAddressChild ]['deps']
						for strDep in dictDepsChild :
							if strDep == 'neg' :
								bNeg = True
								break

						if bNeg :
							# not genuine
							return (None,False)
						else :
							# genuine
							return (None,True)

					if (lang in dict_assert_false) and (strToken.lower() in dict_assert_false[lang]) :

						bNeg = False
						dictDepsChild = dep_graph.nodes[ nAddressChild ]['deps']
						for strDep in dictDepsChild :
							if strDep == 'neg' :
								bNeg = True
								break

						if bNeg :
							# not fake
							return (None,True)
						else :
							# fake
							return (None,False)

	# example: copula link subjects to non-verbal predicates
	# genuine > nsubj > reports > nmod > rioting == reports of rioiting are genuine

	# check head deps
	strDep = dep_graph.nodes[ node_address ]['rel']
	if strDep in [ 'nsubj','nsubjpass' ] :

		nHeadAddress = dep_graph.nodes[ node_address ]['head']
		strToken = dep_graph.nodes[ nHeadAddress ]['word']
		if (strToken != None) and (nHeadAddress != None) :

			if (lang in dict_assert_true) and (strToken.lower() in dict_assert_true[lang]) :

				bNeg = False
				dictDepsChild = dep_graph.nodes[ nHeadAddress ]['deps']
				for strDep in dictDepsChild :
					if strDep == 'neg' :
						bNeg = True
						break

				if bNeg :
					# not genuine
					return (None,False)
				else :
					# genuine
					return (None,True)

			if (lang in dict_assert_false) and (strToken.lower() in dict_assert_false[lang]) :

				bNeg = False
				dictDepsChild = dep_graph.nodes[ nHeadAddress ]['deps']
				for strDep in dictDepsChild :
					if strDep == 'neg' :
						bNeg = True
						break

				if bNeg :
					# not fake
					return (None,True)
				else :
					# fake
					return (None,False)

	# no evidence of negation OR genuine/fake
	return (None,None)

def get_variables_connections( check_index = None, list_variables = None, dep_graph = None, str_connection_path = '', recurse_address = None, dict_openie_config = None ) :
	"""
	get dependency graph connections from this variable (any addresses in collapsed set) to any other variables (any addresses in collapsed set)

	:param int check_index: index of variable to check
	:param list list_variables: list of variables in extraction to try to connect
	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: { 'dep>nsubj' : set(['arg1']), ... }
	:rtype: dict
	"""

	if not isinstance( check_index, int ) :
		raise Exception( 'invalid check_index' )
	if not isinstance( list_variables, list ) :
		raise Exception( 'invalid list_variables' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# init
	dictConnections = {}

	if recurse_address == None :
		# root level? use head addresses of variable to check
		nAddressCheck = list_variables[ check_index ][2]
	else :
		# into recursion? use recurse_address
		nAddressCheck = recurse_address

	# look at children of all nodes in the variable to be checked
	# if there is no variable found go down to next level (and so on recursively) until end of dep tree branch

	# check the child dep graph for all nodes in this variables collapsed set
	dictDeps = dep_graph.nodes[ nAddressCheck ]['deps']
	for strDep in dictDeps :
		for nAddressChild in dictDeps[strDep] :

			bConnected = False

			# check for 1st level children in dep graph (add any)
			for nIndexVar in range(len(list_variables)) :
				if nIndexVar != check_index :

					# loop on collased set of addresses for this target variable
					for nAddressTarget in list_variables[ nIndexVar ][3] :
						if nAddressTarget == nAddressChild :

							# add variable connection path to list
							strConnPath = str_connection_path + strDep
							if not strConnPath in dictConnections :
								dictConnections[ strConnPath ] = set([])
							dictConnections[ strConnPath ].add( list_variables[ nIndexVar ][1] )
							bConnected = True

			# if no connection found for this child recurse and look at the next level down
			if bConnected == False :
				strConnPath = str_connection_path + strDep + '>'

				# recurse
				dictConnectionsRecurse = get_variables_connections( check_index = check_index, list_variables = list_variables, dep_graph = dep_graph, str_connection_path = strConnPath, recurse_address = nAddressChild, dict_openie_config = dict_openie_config )

				# add results (if any) to this level of recurse
				if len(dictConnectionsRecurse) > 0 :

					for strConnPath in dictConnectionsRecurse :
						if not strConnPath in dictConnections :
							dictConnections[ strConnPath ] = set([])
						for strVar in dictConnectionsRecurse[strConnPath] :
							dictConnections[strConnPath].add( strVar )

	# all done
	return dictConnections

def index_cross_variable_connections( list_variables = None, dict_sem_drift = dict_semantic_drift_default, dict_openie_config = None ) :
	"""
	compute an index of how each variable connects to other variables within a specific extraction.
	direct connections between variables are indexed first, where one variable can be walked via dep graph to another directly.
	indirect N-deep connections between variables are also indexed, where one variable can be walked via dep graph to another directly OR via an intermediate variable.
	variable bases are used to map connections, not individual variables so multi-token variables will not be connected multiple times i.e. 'arg1' not 'arg1_2'

	the number of dep graph walk steps between variables is recorded as a kind of proxy to semantic drift along graph walk between extracted variables.
	each coordinating conjunction, loose joining relations and appositional modifier adds an extra 2 to the step count.

	Index types:
		* index_direct_connect - base variable inter-connections
		* index_any_connect - compute for each variable the other variables it has a connection to (including via context and other intermediate variables)
		* index_context_connect - compute for each variable the other variables it has a connection to ONLY following context links

	:param list list_variables: list of variables in extraction
	:param dict dict_sem_drift: dict of semantic drift costs for dep types e.g. { 'conj' : 2 }
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: tuple = ( index_direct_connect, index_any_connect, index_context_connect ). index_direct_connect = { var_base : set([ ( direct_var_connection, walk_steps ), ... ]) }. index_any_connect = { var_base : set([ ( any_var_connection, walk_steps ) ]) }
	:rtype: tuple
	"""

	if not isinstance( list_variables, list ) :
		raise Exception( 'invalid list_variables' )
	if not isinstance( dict_sem_drift, dict ) :
		raise Exception( 'invalid dict_sem_drift' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	#dict_openie_config['logger'].info( 'I1 = ' + repr( list_variables ) )

	# index base variable inter-connections
	dictVarNetwork = {}
	for nIndexVar in range(len(list_variables)) :
		( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) = list_variables[nIndexVar]

		if not '_' in strVar :
			raise Exception('invalid variable : ' + repr(strVar) )
		strVarBase = strVar.split('_')[0]

		setVarConnected = set([])
		for strDepWalk in dictConnections :

			listDepSteps = strDepWalk.split('>')
			nSteps = len(listDepSteps)

			for strDrift in dict_sem_drift :
				for strDepStep in listDepSteps :
					if strDepStep.startswith( strDrift ) :
						nSteps = nSteps + dict_sem_drift[strDrift]

			for strVarConnected in dictConnections[strDepWalk] :
				if not '_' in strVarConnected :
					raise Exception('invalid connected variable : ' + repr(strVarConnected) )
				strVarConnectedBase = strVarConnected.split('_')[0]
				setVarConnected.add( (strVarConnectedBase, nSteps, strDepWalk) )

		# there can be multiple var entries per base, each with a variable connection of its own e.g. arg1_1, arg1_2
		if not strVarBase in dictVarNetwork :
			dictVarNetwork[ strVarBase ] = setVarConnected
		else :
			dictVarNetwork[ strVarBase ] = dictVarNetwork[ strVarBase ].union( setVarConnected )

	#dict_openie_config['logger'].info( 'I2 = ' + repr( dictVarNetwork ) )

	# compute for each variable the other variables it has a connection to (including via context and other intermediate variables)
	dictVarConnections = {}
	for nIndexVar in range(len(list_variables)) :
		( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) = list_variables[nIndexVar]

		if not '_' in strVar :
			raise Exception('invalid variable : ' + repr(strVar) )
		strVarBase = strVar.split('_')[0]

		#dict_openie_config['logger'].info( 'T3.1 = ' + repr( strVarBase ) )

		setConnected = set([])
		setToCheck = set([ (strVarBase,0, '') ])
		setChecked = set([])
		while len(setToCheck) > 0 :
			( strVarToCheck, nSteps, strDepWalk ) = setToCheck.pop()
			setChecked.add( strVarToCheck )
			setVarConnected = dictVarNetwork[strVarToCheck]
			if len(setVarConnected) > 0 :
				for ( strConnected, nStepConnected, strDepWalk2 ) in setVarConnected :
					if strConnected not in setChecked :
						if len(strDepWalk) > 0 :
							setConnected.add( ( strConnected, nSteps + nStepConnected, strDepWalk + '>' + strDepWalk2 ) )
							setToCheck.add( ( strConnected, nSteps + nStepConnected, strDepWalk + '>' + strDepWalk2 ) )
						else :
							setConnected.add( ( strConnected, nSteps + nStepConnected, strDepWalk2 ) )
							setToCheck.add( ( strConnected, nSteps + nStepConnected, strDepWalk2 ) )

		#dict_openie_config['logger'].info( 'T3.1 = ' + repr( setConnected ) )

		if not strVarBase in dictVarConnections :
			dictVarConnections[ strVarBase ] = setConnected
		else :
			dictVarConnections[ strVarBase ] = dictVarConnections[ strVarBase ].union( setConnected )

	#dict_openie_config['logger'].info( 'I3 = ' + repr( dictVarConnections ) )

	# compute for each variable the other variables it has a connection to ONLY following context links
	dictVarContextConnections = {}
	for nIndexVar in range(len(list_variables)) :
		( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) = list_variables[nIndexVar]

		if not '_' in strVar :
			raise Exception('invalid variable : ' + repr(strVar) )
		strVarBase = strVar.split('_')[0]

		setConnected = set([])
		setToCheck = set([ (strVarBase,0,'') ])
		setChecked = set([])
		while len(setToCheck) > 0 :
			( strVarToCheck, nSteps, strDepWalk ) = setToCheck.pop()
			setChecked.add( strVarToCheck )
			setVarConnected = dictVarNetwork[strVarToCheck]
			if len(setVarConnected) > 0 :
				for ( strConnected, nStepConnected, strDepWalk2 ) in setVarConnected :
					if (strConnected not in setChecked) and (strConnected.startswith( 'ctxt' ) == True) :
						if len(strDepWalk) > 0 :
							setConnected.add( ( strConnected, nSteps + nStepConnected, strDepWalk + '>' + strDepWalk2 ) )
							setToCheck.add( ( strConnected, nSteps + nStepConnected, strDepWalk + '>' + strDepWalk2 ) )
						else :
							setConnected.add( ( strConnected, nSteps + nStepConnected, strDepWalk2 ) )
							setToCheck.add( ( strConnected, nSteps + nStepConnected, strDepWalk2 ) )

		#dict_openie_config['logger'].info( 'T2 = ' + repr( setConnected ) )
		if not strVarBase in dictVarContextConnections :
			dictVarContextConnections[ strVarBase ] = setConnected
		else :
			dictVarContextConnections[ strVarBase ] = dictVarContextConnections[ strVarBase ].union( setConnected )

	#dict_openie_config['logger'].info( 'I4 = ' + repr( dictVarContextConnections ) )

	return ( dictVarNetwork, dictVarConnections, dictVarContextConnections )

def filter_extractions( dep_graph = None, list_extractions = [], filter_strategy = 'min_semantic_drift_per_target', use_context = False, max_context = 4, min_var_connection = 2, max_semantic_drift = 4, target_var_type = None, dict_sem_drift = dict_semantic_drift_default, dict_openie_config = None ) :
	"""
	filter a set of extractions for a sent, to get a more focussed set without redundant and overlapping extractions.

	filtering strategy - segment_coordinating_conj:
		* idea - ensures extractions cover the parts of a proposition, avoiding over-large propositions and making it easier to extract individual entity attributes (good for knowledge-base production methods)
		* segment sent address range by coordinating conjunction [CC , :] = (addr_start, addr_end)
		* for each address segment find smallest extractions that fully span this address range, favouring highest variable count if multiple options exist
		* if none exist get extractions that cover as many of the individual addresses, faviouring extractions whose size fits best to the segment size

	filtering strategy - segment_subsumption:
		* idea - ensures extractions contain full context, providing large propositions that are easu for humans to understand (good for human intelligence gathering)
		* select extractions whose tokens fully subsume another extraction,favouring highest variable count if multiple options exist
		* head address only used for subsumption checks

	filtering strategy - min_semantic_drift_per_target:
		* idea - ensures there is an extraction for each instance of a target var type (e.g. verb-mediated rel in sent)
		* for each target var instance select extractions containing it that have the lowest max inter-var path between variables (not context) and the target var. a preference for widest address range is used to differentiate between extractions with same max inter-var path.

	filtering strategy - threshold_semantic_drift_per_target:
		* idea - ensures there is an extraction for each instance of a target var type (e.g. verb-mediated rel in sent)
		* for each target var instance select extractions containing it that have a <= threshold inter-var path between variables (not context) and the target var.

	confidence value:
			* the confidence value appended to end of each extraction (higher numbers are better)
			* confidence = number of extractions allowed / total number of extractions [high good]

	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param list list_extractions: list of extractions from comp_sem_lib.match_extraction_patterns()
	:param unicode filter_strategy: name of filter strategy to apply. Can also be None for no filtering.
	:param bool use_context: use context variables as targets when applying strategy (default is False so only non context variables are considered for intervar distances and address ranges)
	:param int max_context: max number of context variables to allow per extraction (can be none)
	:param int min_var_connection: min number of variables connected to target for extraction to be considered (filter prior to looking at semantic drift) (can be none)
	:param int max_semantic_drift: max semantic drift between variables (can be none)
	:param unicode target_var_type: name of target var type (for min_semantic_drift_per_target strategy)
	:param dict dict_sem_drift: dict of semantic drift costs for dep types e.g. { 'conj' : 2 }
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: tuple = (list_extractions_filtered, list_conf). list_extractions_filtered is a filtered list of extractions using same format as comp_sem_lib.match_extraction_patterns(). list_conf is a list of float confidence values per extraction, high value = good
	:rtype: tuple
	"""

	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( list_extractions, list ) :
		raise Exception( 'invalid list_extractions' )
	if not isinstance( filter_strategy, (str,type(None)) ) :
		raise Exception( 'invalid filter_strategy' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( use_context, bool ) :
		raise Exception( 'invalid use_context' )
	if not isinstance( max_context, (int,type(None)) ) :
		raise Exception( 'invalid max_context' )
	if not isinstance( min_var_connection, (int,type(None)) ) :
		raise Exception( 'invalid min_var_connection' )
	if not isinstance( max_semantic_drift, (int,type(None)) ) :
		raise Exception( 'invalid max_semantic_drift' )
	if not isinstance( target_var_type, (str,type(None)) ) :
		raise Exception( 'invalid target_var_type' )
	if not isinstance( dict_sem_drift, dict ) :
		raise Exception( 'invalid dict_sem_drift' )
	if filter_strategy not in ['segment_coordinating_conj','segment_subsumption','min_semantic_drift_per_target','threshold_semantic_drift_per_target',None] :
		raise Exception( 'unknown filtering strategy : ' + repr(filter_strategy) )

	if len(list_extractions) == 0 :
		return ( [], [] )

	# make a copy for result
	listFilteredExtractions = copy.deepcopy( list_extractions )
	listConf = []

	# index address range of each extraction and the number of variables
	listIndexVariables = []
	for nIndex1 in range(len(list_extractions)) :
		# get min and max of token addresses this extraction covers (ignoring slot nodes)
		nMaxAddress = None
		nMinAddress = None
		bNegation = None
		bGenuine = None
		nVariableCount = 0
		nContextCount = 0
		dictVarConnections = {}

		( dictVarNetwork, dictVarConnections, dictVarContextConnections ) = index_cross_variable_connections(
			list_variables = list_extractions[nIndex1],
			dict_sem_drift = dict_sem_drift,
			dict_openie_config = dict_openie_config )

		#dict_openie_config['logger'].info( 'T1 = ' + repr( (nIndex1, dictVarNetwork, dictVarConnections, dictVarContextConnections ) ) )

		# get address range and inter variable walk distance
		for nIndexVar in range(len(list_extractions[nIndex1])) :
			( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) = list_extractions[nIndex1][nIndexVar]

			if strType == 'ctxt' :
				nContextCount = nContextCount + 1
				if use_context == False :
					continue

			if len(listCollapsed) == 0 :
				continue

			nVariableCount = nVariableCount + 1

			listCollapsedSorted = sorted( listCollapsed )

			# get range of collapsed tokens under head variable (which will include the head variable)
			if (nMinAddress == None) or (nMinAddress > listCollapsedSorted[0]) :
				nMinAddress = listCollapsedSorted[0]
			if (nMaxAddress == None) or (nMaxAddress < listCollapsedSorted[-1]) :
				nMaxAddress = listCollapsedSorted[-1]

			'''
			# for addr range only consider the head.
			# this is to stop a head var with a long collapsed span being favoured when there are options of head vars in the span terms themselves (that would provide a better head address coverage)
			if (nMaxAddress == None) or (nMaxAddress < nAddress) :
				nMaxAddress = nAddress

			if (nMinAddress == None) or (nMinAddress > nAddress) :
				nMinAddress = nAddress
			'''

		#dict_openie_config['logger'].info( 'T2 = ' + repr( dictVarConnections ) )

		# record stats for extraction
		listIndexVariables.append( (nMinAddress, nMaxAddress, nVariableCount, nContextCount, dictVarConnections ) )

	# apply segment coordinating conj strategy
	if filter_strategy == 'segment_coordinating_conj' :

		# filtering strategy to ensure extractions cover the parts of a proposition (avoiding over-large propositions where several attributes are defined in one go thats hard to extract later into a KBP)
		# - segment sent address range by coordinating conjunction [CC , :] = (addr_start, addr_end)
		# - for each address segment
		#     find smallest extractions that fully span this address range
		#        from this set select the highest variable count
		#     if none fully span this address range
		#        loop on address in segment
		#           select extraction(s) that cover this address AND jump loop to extraction end address

		# index coordinating conjunction
		listCoordinatingAddrs = []

		nLastAddr = -1
		listAddrSorted = sorted( dep_graph.nodes.keys() )
		if len(listAddrSorted) == 0 :
			return listFilteredExtractions

		for nAddr in listAddrSorted :
			# add coordinating conjunction (cc) such as and, or ...
			if dep_graph.nodes[nAddr]['rel'] == 'cc' :
				listCoordinatingAddrs.append( nAddr )

			# add missing nodes (i.e. comma, semi-colon, colon) which are removed from dep_graph by stanford parser
			if nAddr != nLastAddr + 1 :
				for nMissingAddr in range( nLastAddr + 1, nAddr ) :
					listCoordinatingAddrs.append( nMissingAddr )
			
			nLastAddr = nAddr

		#dict_openie_config['logger'].info( 'T1 (coord addr) = ' + repr(listCoordinatingAddrs) )

		# process each address segment
		# start at address 1 since root is always address 0
		setIndexToSave = set( [] )
		listCoordinatingAddrs.append( listAddrSorted[-1] + 1 )
		nLastAddr = 0
		for nCoordinatingAddr in listCoordinatingAddrs :
			nStartAddr = nLastAddr + 1
			nEndAddr = nCoordinatingAddr - 1
			if nEndAddr <= nStartAddr :
				nLastAddr = nCoordinatingAddr
				continue

			#dict_openie_config['logger'].info( 'T2 (segment) = ' + repr( (nStartAddr,nEndAddr) ) )

			# get extractions that cover this segment completely
			listMatches = []
			for nIndexExtraction in range(len(listIndexVariables)) :
				( nMinAddress, nMaxAddress, nVariableCount, nContextCount, dictVarConnections ) = listIndexVariables[nIndexExtraction]

				# reject extractions with too much context
				if (max_context != None) and (nContextCount > max_context) :
					continue

				if (nMinAddress <= nStartAddr) and (nMaxAddress >= nEndAddr) :
					listMatches.append( ( nIndexExtraction, nMaxAddress - nMinAddress, nVariableCount ) )

			if len(listMatches) == 0 :
				nLastAddr = nCoordinatingAddr
				continue

			#dict_openie_config['logger'].info( 'T2.1 (match) = ' + repr( listMatches ) )

			# sort by extraction length (smallest first)
			listMatches = sorted( listMatches, key=lambda entry: entry[1], reverse=False )

			# remove all but the smallest matching extractions
			nSmallestLength = listMatches[0][1]
			nIndexMatch = 0
			while nIndexMatch < len(listMatches) :
				if listMatches[nIndexMatch][1] != nSmallestLength :
					del listMatches[nIndexMatch]
				else :
					nIndexMatch = nIndexMatch + 1

			#dict_openie_config['logger'].info( 'T2.2 (match) = ' + repr( listMatches ) )

			# sort by variable count
			listMatches = sorted( listMatches, key=lambda entry: entry[2], reverse=True )

			# remove all but the largest variable counts
			nLargestCount = listMatches[0][2]
			nIndexMatch = 0
			while nIndexMatch < len(listMatches) :
				if listMatches[nIndexMatch][2] != nLargestCount :
					del listMatches[nIndexMatch]
				else :
					nIndexMatch = nIndexMatch + 1

			#dict_openie_config['logger'].info( 'T2.3 (match) = ' + repr( listMatches ) )

			# do we have anything left?
			# YES - add to the save set
			if len(listMatches) > 0 :
				for ( nIndexExtraction, nAddrLength, nVariableCount ) in listMatches :
					setIndexToSave.add( nIndexExtraction )

			# NO - get extractions that at least cover as many of the addresses in the segment range as we can do
			else :
				# loop on segment addresses
				nAddr = nStartAddr
				while nAddr <= nEndAddr :

					#dict_openie_config['logger'].info( 'T2.4 (addr) = ' + repr( nAddr ) )

					# get all extractions that contain this specific address
					listMatches = []
					for nIndexExtraction in range(len(listIndexVariables)) :
						( nMinAddress, nMaxAddress, nVariableCount, nContextCount, dictVarConnections ) = listIndexVariables[nIndexExtraction]
						if (nMinAddress <= nAddr) and (nMaxAddress >= nAddr) :
							listMatches.append( ( nIndexExtraction, nMinAddress, nMaxAddress, nVariableCount ) )

					# sort by min address, reverse order so largest first
					listMatches = sorted( listMatches, key=lambda entry: entry[1], reverse=True )

					# remove all but the largest start addr
					nBestAddr = listMatches[0][1]
					nIndexMatch = 0
					while nIndexMatch < len(listMatches) :
						if listMatches[nIndexMatch][1] != nBestAddr :
							del listMatches[nIndexMatch]
						else :
							nIndexMatch = nIndexMatch + 1

					#dict_openie_config['logger'].info( 'T2.5 (match) = ' + repr( listMatches ) )

					# no matches? try next address in segment
					if len(listMatches) == 0 :
						nAddr = nAddr + 1
						continue

					# sort by max address deviation from end of segment (0 = end of segment is end of extraction, positive = too big, negative too small)
					listMatches = sorted( listMatches, key=lambda entry: abs( entry[2] - nEndAddr ), reverse=False )

					# get smallest deviation from ideal (end extraction is end segment)
					# remove all but best option
					nBestAddr = listMatches[0][2]
					nIndexMatch = 0
					while nIndexMatch < len(listMatches) :
						if listMatches[nIndexMatch][2] != nBestAddr :
							del listMatches[nIndexMatch]
						else :
							nIndexMatch = nIndexMatch + 1

					#dict_openie_config['logger'].info( 'T2.6 (match) = ' + repr( listMatches ) )

					# no matches? try next address in segment
					if len(listMatches) == 0 :
						nAddr = nAddr + 1
						continue

					# add matches to the save set
					for ( nIndexExtraction, nMinAddress, nMaxAddress, nVariableCount ) in listMatches :
						setIndexToSave.add( nIndexExtraction )
					nAddr = nBestAddr + 1

			# next segment
			nLastAddr = nCoordinatingAddr

		# confidence is the number of extractions saved / total number of extractions
		nConf = ( 1.0 * len(setIndexToSave) ) / len(listFilteredExtractions)

		# apply filter to extractions
		setIndexToSave = sorted( list(setIndexToSave), reverse = True )
		for nIndex in range(len(listFilteredExtractions)-1,-1,-1) :
			if nIndex not in setIndexToSave :
				del listFilteredExtractions[nIndex]

		# append confidence value based on number of target variables 
		for nIndex in range(len(listFilteredExtractions)) :
			listConf.append( nConf )

	# apply segment subsumption strategy
	elif filter_strategy == 'segment_subsumption' :

		# remove extractions which are fully subsumed by other extractions
		# or have less variables (not including context variables) if address range is equal
		# or just use first one

		setIndexToDelete = set( [] )
		for nIndex1 in range(len(listIndexVariables)) :
			# reject extractions with too much context
			if (max_context != None) and (nContextCount > max_context) :
				setIndexToDelete.add( nIndex1 )
				continue

			if not nIndex1 in setIndexToDelete :
				( nMinAddress1, nMaxAddress1, nVariableCount1, nContextCount1, dictVarConnections1 ) = listIndexVariables[nIndex1]

				for nIndex2 in range(nIndex1+1, len(listIndexVariables)) :
					if not nIndex2 in setIndexToDelete :
						( nMinAddress2, nMaxAddress2, nVariableCount2, nContextCount2, dictVarConnections2 ) = listIndexVariables[nIndex2]

						bSubsumed1 = False
						bSubsumed2 = False

						if (nMinAddress1 == nMinAddress2) and (nMaxAddress1 == nMaxAddress2) :
							# exactly the same addresses range? use the one with the most variables extracted
							if nVariableCount1 >= nVariableCount2 :
								bSubsumed2 = True
							else :
								bSubsumed1 = True
						else :
							# check for address subsumption
							if (nMinAddress1 <= nMinAddress2) and (nMaxAddress1 >= nMaxAddress2) :
								bSubsumed2 = True

							if (nMinAddress2 <= nMinAddress1) and (nMaxAddress2 >= nMaxAddress1) :
								bSubsumed1 = True

						if bSubsumed2 == True :
							setIndexToDelete.add( nIndex2 )
							# continue looking for extractions that extraction1 subsumes
							continue
						elif bSubsumed1 == True :
							setIndexToDelete.add( nIndex1 )
							# stop looking for extractions that extraction1 subsumes as we have just removed extraction1
							break

		# confidence is the number of extractions saved / total number of extractions
		nConf = ( 1.0 * ( len(listFilteredExtractions) - len(listIndextoDelete) ) ) / len(listFilteredExtractions)

		# apply filter to extractions
		listIndextoDelete = sorted( list(setIndexToDelete), reverse = True )
		for nIndex in listIndextoDelete :
			del listFilteredExtractions[nIndex]

		# append confidence value based on number of target variables 
		for nIndex in range(len(listFilteredExtractions)) :
			listConf.append( nConf )


	# apply min_semantic_drift_per_target strategy
	elif filter_strategy == 'min_semantic_drift_per_target' :

		if target_var_type == None :
			raise Exception( 'min_semantic_drift_per_target strategy needs a non-null target var type' ) 

		# get a list of N instances (identified by head address) of a target var type appearing in the extraction set
		# for each instance, find the minimal inter-variable walk distance, as a proxy for semantic closeness of variables in the extraction
		# if inter-var walk distance same then choose the smallest walk distance (for a tight extraction fit)
		# filter out all but the minmal address ranges, leaving N extractions (one per instance of target variable)

		setAddrOfInstance = set([])
		for nIndex1 in range(len(list_extractions)) :
			for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extractions[nIndex1] :
				if strType == target_var_type :
					setAddrOfInstance.add( nAddress )

		dictExtractionScore = {}
		setIndexToSave = set([])
		for nAddrOfInstance in setAddrOfInstance :
			nInterVarWalk = None
			nRange = None
			setMinimalIndex = set([])

			nFreq = 0
			for nIndex1 in range(len(list_extractions)) :
				for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extractions[nIndex1] :
					if (nAddress == nAddrOfInstance) and (strType == target_var_type) :
						( nMinAddress, nMaxAddress, nVariableCount, nContextCount, dictVarConnections ) = listIndexVariables[nIndex1]

						# count num of extractions that contain this target address
						nFreq = nFreq + 1

						# reject extractions with too much context
						if (max_context != None) and (nContextCount > max_context) :
							continue

						# calc the longest walk from target var to other var (not context)
						# reject extractions, where target vars is not not connected to at least 2 other vars (directly or indirectly)
						# check connections to target and from target, and N deep paths to and from target
						# patterns
						#    arg > arg > rel
						#    arg > rel, rel > arg
						#    rel > arg > arg
						#    arg > rel, rel < arg
						listConnectionsToTarget = []
						strTargetVarBase = strVar.split('_')[0]

						# add any child var of the target var
						for ( strConnection, nSteps, strDepWalk ) in dictVarConnections[strTargetVarBase] :
							if (strConnection != strTargetVarBase) and (not strConnection.startswith('ctxt')) :
								listConnectionsToTarget.append( ( strConnection, nSteps, strDepWalk ) )

						#dict_openie_config['logger'].info( 'T4.1 = ' + repr( listConnectionsToTarget ) )

						# add any root var, where it has a child of the target var
						for strVarBaseToCheck in dictVarConnections :
							for ( strConnectionRoot, nStepsRoot, strDepWalkRoot ) in dictVarConnections[strVarBaseToCheck] : 
								if strTargetVarBase == strConnectionRoot :
									if (strVarBaseToCheck != strTargetVarBase) and (not strVarBaseToCheck.startswith('ctxt')) :
										listConnectionsToTarget.append( ( strVarBaseToCheck, nStepsRoot, strDepWalkRoot ) )

										# add all siblings of a valid root var
										for ( strSiblingVarBase, nStepsSibling, strDepWalkSibling ) in dictVarConnections[strVarBaseToCheck] :
											if (strSiblingVarBase != strTargetVarBase) and (not strSiblingVarBase.startswith('ctxt')) :
												# the number of dep steps to target var is the path to root var + path to sibling from root
												listConnectionsToTarget.append( ( strSiblingVarBase, nStepsSibling + nStepsRoot, strDepWalkRoot + '>' + strDepWalkSibling ) )

												# add all children of the sibling
												for ( strConnection, nStepsSiblingChild, strDepWalkChild ) in dictVarConnections[strSiblingVarBase] :
													if (strConnection != strTargetVarBase) and (not strConnection.startswith('ctxt')) :
														# the number of dep steps to target var is the path to root var + path to sibling from root + path to its child
														listConnectionsToTarget.append( ( strConnection, nStepsSibling + nStepsRoot + nStepsSiblingChild, strDepWalkRoot + '>' + strDepWalkSibling + '>' + strDepWalkChild ) )

						#dict_openie_config['logger'].info( 'T4.2 = ' + repr( listConnectionsToTarget ) )

						# remove duplicate connections links via different paths (e.g. arg whose tokens include the dobj and nsubj)
						nIndexConn1 = 0
						while nIndexConn1 < len(listConnectionsToTarget) :
							( strConnection1, nSteps1, strDepWalk1 ) = listConnectionsToTarget[nIndexConn1]

							nIndexConn2 = nIndexConn1 + 1
							while nIndexConn2 < len(listConnectionsToTarget) :
								( strConnection2, nSteps2, strDepWalk2 ) = listConnectionsToTarget[nIndexConn2]

								if strConnection2 == strConnection1 :
									if nSteps2 < nSteps1 :
										# keep shortest path if we have duplicates
										listConnectionsToTarget[nIndexConn1] = listConnectionsToTarget[nIndexConn2]
									del listConnectionsToTarget[nIndexConn2]
								else :
									nIndexConn2 = nIndexConn2 + 1
							
							nIndexConn1 = nIndexConn1 + 1

						#dict_openie_config['logger'].info( 'T4.3 = ' + repr( listConnectionsToTarget ) )

						# reject extractions where there is not at least 2 vars connected to the target var
						if (min_var_connection != None) and (len(listConnectionsToTarget) < min_var_connection) :
							continue

						# get the worse case inter-var path between variables and the target var
						nMaxSteps = 0
						for ( strConnection, nSteps, strDepWalk ) in listConnectionsToTarget :
							if nSteps > nMaxSteps :
								nMaxSteps = nSteps

						# reject any large semantic drifts
						if (max_semantic_drift != None) and (nMaxSteps > max_semantic_drift) :
							continue
						#dict_openie_config['logger'].info( 'T5 = ' + repr( ( nMaxSteps, setMinimalIndex, nMinAddress, nMaxAddress, nRange  ) ) )

						# select extraction wth shortest inter variable walk distance
						if (nInterVarWalk == None) or (nMaxSteps < nInterVarWalk) :
							# new minimal, so new best case
							nInterVarWalk = nMaxSteps
							nRange = nMaxAddress - nMinAddress
							setMinimalIndex = set([nIndex1])

						elif (nMaxSteps == nInterVarWalk) and (nRange < (nMaxAddress - nMinAddress)) :
							# same as best minimal, but wider address range so its the new best case
							nRange = nMaxAddress - nMinAddress
							setMinimalIndex = set([nIndex1])

						elif (nMaxSteps == nInterVarWalk) and (nRange == (nMaxAddress - nMinAddress)) :
							# same as best minimal, same range, so save it to best case set as both potentially good
							setMinimalIndex.add( nIndex1 )

						#dict_openie_config['logger'].info( 'T6 = ' + repr( setMinimalIndex ) )

			# if we have a viable extraction save it (otherwise ignore target instance completely as having no viable extraction)
			if len(setMinimalIndex) > 0 :
				# confidence of extractions for a target address = number of extractions saved / total number of extractions [high good]
				nConf = ( 1.0 * len(setMinimalIndex) ) / nFreq

				#dict_openie_config['logger'].info( 'T7 (saved) = ' + repr( setMinimalIndex ) )
				for nMinimalIndex in setMinimalIndex :
					setIndexToSave.add( ( nMinimalIndex, nConf ) )

		# apply filter to extractions
		listIndexToSave = sorted( list(setIndexToSave), key=lambda entry: entry[0], reverse = True )

		for nIndex in range(len(listFilteredExtractions)) :
			listConf.append( 3.0 )

		for nIndex in range(len(listFilteredExtractions)-1,-1,-1) :

			bSave = False
			nLowestConf = 2.0
			for ( nIndexSave, nConf ) in listIndexToSave :
				if nIndex == nIndexSave :
					bSave = True
					if nLowestConf > nConf :
						nLowestConf = nConf

			if bSave == False :
				del listFilteredExtractions[nIndex]
				del listConf[nIndex]
			else :
				listConf[nIndex] = nLowestConf

	# apply threshold_semantic_drift_per_target strategy
	elif filter_strategy == 'threshold_semantic_drift_per_target' :

		if target_var_type == None :
			raise Exception( 'threshold_semantic_drift_per_target strategy needs a non-null target var type' ) 
		if max_semantic_drift == None :
			raise Exception( 'threshold_semantic_drift_per_target strategy needs a non-null max semantic drift' ) 

		# get a list of N instances (identified by head address) of a target var type appearing in the extraction set
		# for each instance, find the inter-variable walk distance, as a proxy for semantic closeness of variables in the extraction
		# reject any inter-var walk distance > threshold

		setAddrOfInstance = set([])
		for nIndex1 in range(len(list_extractions)) :
			for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extractions[nIndex1] :
				if strType == target_var_type :
					setAddrOfInstance.add( nAddress )

		#dict_openie_config['logger'].info( 'T0 = ' + repr( setAddrOfInstance ) )

		dictExtractionScore = {}
		setIndexToSave = set([])
		for nAddrOfInstance in setAddrOfInstance :
			nInterVarWalk = None
			nRange = None
			setBelowThresholdIndex = set([])

			nFreq = 0
			for nIndex1 in range(len(list_extractions)) :
				for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extractions[nIndex1] :
					if (nAddress == nAddrOfInstance) and (strType == target_var_type) :
						( nMinAddress, nMaxAddress, nVariableCount, nContextCount, dictVarConnections ) = listIndexVariables[nIndex1]

						# count num of extractions that contain this target address
						nFreq = nFreq + 1

						# reject extractions with too much context
						if (max_context != None) and (nContextCount > max_context) :
							continue

						#dict_openie_config['logger'].info( 'T3 = ' + repr( ( nIndex1, strVar, nAddress, dictVarConnections ) ) )

						# calc the longest walk from traget var to other var (not context)
						# reject extractions, where target vars is not not connected to at least 2 other vars (directly or indirectly)
						# check connections to target and from target, and N deep paths to and from target
						# patterns
						#    arg > arg > rel
						#    arg > rel, rel > arg
						#    rel > arg > arg
						#    arg > rel, rel < arg
						listConnectionsToTarget = []
						strTargetVarBase = strVar.split('_')[0]

						# add any child var of the target var
						for ( strConnection, nSteps, strDepWalk ) in dictVarConnections[strTargetVarBase] :
							if (strConnection != strTargetVarBase) and (not strConnection.startswith('ctxt')) :
								listConnectionsToTarget.append( ( strConnection, nSteps, strDepWalk ) )

						#dict_openie_config['logger'].info( 'T4.1 = ' + repr( listConnectionsToTarget ) )

						# add any root var, where it has a child of the target var
						for strVarBaseToCheck in dictVarConnections :
							for ( strConnectionRoot, nStepsRoot, strDepWalkRoot ) in dictVarConnections[strVarBaseToCheck] : 
								if strTargetVarBase == strConnectionRoot :
									if (strVarBaseToCheck != strTargetVarBase) and (not strVarBaseToCheck.startswith('ctxt')) :
										listConnectionsToTarget.append( ( strVarBaseToCheck, nStepsRoot, strDepWalkRoot ) )

										# add all siblings of a valid root var
										for ( strSiblingVarBase, nStepsSibling, strDepWalkSibling ) in dictVarConnections[strVarBaseToCheck] :
											if (strSiblingVarBase != strTargetVarBase) and (not strSiblingVarBase.startswith('ctxt')) :
												# the number of dep steps to target var is the path to root var + path to sibling from root
												listConnectionsToTarget.append( ( strSiblingVarBase, nStepsSibling + nStepsRoot, strDepWalkRoot + '>' + strDepWalkSibling ) )

												# add all children of the sibling
												for ( strConnection, nStepsSiblingChild, strDepWalkChild ) in dictVarConnections[strSiblingVarBase] :
													if (strConnection != strTargetVarBase) and (not strConnection.startswith('ctxt')) :
														# the number of dep steps to target var is the path to root var + path to sibling from root + path to its child
														listConnectionsToTarget.append( ( strConnection, nStepsSibling + nStepsRoot + nStepsSiblingChild, strDepWalkRoot + '>' + strDepWalkSibling + '>' + strDepWalkChild ) )

						#dict_openie_config['logger'].info( 'T4.2 = ' + repr( listConnectionsToTarget ) )

						# remove duplicate connections links via different paths (e.g. arg whose tokens include the dobj and nsubj)
						nIndexConn1 = 0
						while nIndexConn1 < len(listConnectionsToTarget) :
							( strConnection1, nSteps1, strDepWalk1 ) = listConnectionsToTarget[nIndexConn1]

							nIndexConn2 = nIndexConn1 + 1
							while nIndexConn2 < len(listConnectionsToTarget) :
								( strConnection2, nSteps2, strDepWalk2 ) = listConnectionsToTarget[nIndexConn2]

								if strConnection2 == strConnection1 :
									if nSteps2 < nSteps1 :
										# keep shortest path if we have duplicates
										listConnectionsToTarget[nIndexConn1] = listConnectionsToTarget[nIndexConn2]
									del listConnectionsToTarget[nIndexConn2]
								else :
									nIndexConn2 = nIndexConn2 + 1
							
							nIndexConn1 = nIndexConn1 + 1

						#dict_openie_config['logger'].info( 'T4.3 = ' + repr( listConnectionsToTarget ) )

						# reject extractions where there is not at least 2 vars connected to the target var
						if (min_var_connection != None) and (len(listConnectionsToTarget) < min_var_connection) :
							continue

						# get the worse case inter-var path between variables and the target var
						nMaxSteps = 0
						for ( strConnection, nSteps, strDepWalk ) in listConnectionsToTarget :
							if nSteps > nMaxSteps :
								nMaxSteps = nSteps

						#dict_openie_config['logger'].info( 'T5 = ' + repr( ( nMaxSteps, setBelowThresholdIndex, nMinAddress, nMaxAddress, nRange  ) ) )

						# reject any large semantic drifts
						if (max_semantic_drift != None) and (nMaxSteps > max_semantic_drift) :
							continue

						setBelowThresholdIndex.add( nIndex1 )

						#dict_openie_config['logger'].info( 'T6 = ' + repr( setBelowThresholdIndex ) )

			# if we have a viable extraction save it (otherwise ignore target instance completely as having no viable extraction)
			if len(setBelowThresholdIndex) > 0 :
				# confidence of extractions for a target address = number of extractions saved / total number of extractions [high good]
				nConf = ( 1.0 * len(setBelowThresholdIndex) ) / nFreq

				# dict_openie_config['logger'].info( 'T7 (saved) = ' + repr( setBelowThresholdIndex ) )
				for nSelectedIndex in setBelowThresholdIndex :
					setIndexToSave.add( ( nSelectedIndex, nConf ) )

		# apply filter to extractions
		for nIndex in range(len(listFilteredExtractions)-1,-1,-1) :
			nSaveConf = None
			for ( nIndexSave, nConf ) in setIndexToSave :
				if nIndex == nIndexSave :
					nSaveConf = nConf
					break

			if nSaveConf == None :
				del listFilteredExtractions[nIndex]
			else :
				listConf.insert(0,nSaveConf)

	# apply no filtering (return a copy with max confidence in all extractions)
	elif filter_strategy == None :
		for nIndex in range(len(listFilteredExtractions)) :
			listConf.append( 1.0 )

	# dict_openie_config['logger'].info( 'S4 = ' + repr( len(list_extractions) ) )
	# dict_openie_config['logger'].info( 'T3 (filtered) = ' + repr( listFilteredExtractions ) )

	# return filtered list
	return ( listFilteredExtractions, listConf )



def pretty_print_extraction( list_extracted_vars = None, dep_graph = None, set_var_types = set([]), style = 'highlighted_vars', space_replacement_char = '_', dict_openie_config = None ) :
	"""
	pretty print a set of extracted variables from comp_sem_lib.match_extraction_patterns(). arguments are sorted in lexical order for easier reading.

	:param list list_extracted_vars: list of variables from comp_sem_lib.match_extraction_patterns()
	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param set set_var_types: set of {var} types for pretty print
	:param str style: style for print = highlighted_vars, plain_vars, tokens_only
	:param str space_replacement_char: replacement char for all token spaces. should be same as prepare_tags_for_dependency_parse()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: pretty print version of arguments
	:rtype: unicode
	"""

	if not isinstance( list_extracted_vars, (list,tuple) ) :
		raise Exception( 'invalid list_extracted_vars' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( set_var_types, set ) :
		raise Exception( 'invalid set_var_types' )
	if not isinstance( style, str ) :
		raise Exception( 'invalid style' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )

	if not style in [ 'highlighted_vars', 'plain_vars', 'tokens_only' ] :
		raise Exception( 'unknown style value : ' + style )

	# compile a list of (address,word,var,head_flag,dictConnections,pattern_index)
	listTokens = []
	for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extracted_vars :
		for nAddressCollapsed in listCollapsed :
			if nAddressCollapsed == nAddress :
				bHead = True
			else :
				bHead = False
			strRel = dep_graph.nodes[ nAddressCollapsed ][ 'rel' ]
			strToken = dep_graph.nodes[ nAddressCollapsed ][ 'word' ]
			if strToken != None :
				strToken = strToken.replace( space_replacement_char, ' ' )
			listTokens.append( ( nAddressCollapsed, strToken, strRel, strType, strVar, bHead, dictConnections, nPatternIndex ) )

	# sort list by address order so pretty print tokens come out in the word sequence of the original sent
	listTokens = sorted( listTokens, key=lambda entry: entry[0], reverse=False )
	nTokenStart = listTokens[0][0]
	nTokenEnd = listTokens[-1][0]

	# pretty print list
	listComponents = []
	strLastVar = None
	for nTokenIndex in range( nTokenStart,nTokenEnd+1 ) :
		strEntry = ''

		# see if it a token in an extracted var
		for nEntryIndex in range(len(listTokens)) :
			if listTokens[nEntryIndex][0] == nTokenIndex :

				if style in [ 'highlighted_vars', 'plain_vars' ] :
					if listTokens[nEntryIndex][3] in set_var_types :
						if strLastVar != listTokens[nEntryIndex][4] :
							# start of variable
							strEntry += '{' + listTokens[nEntryIndex][4] + ' '

							# find head for this var and report it
							strHead = None
							for nEntryIndex2 in range(len(listTokens)) :
								if (listTokens[nEntryIndex2][4] == listTokens[nEntryIndex][4]) and (listTokens[nEntryIndex2][5] == True) :
									strHead = listTokens[nEntryIndex][1]
									break

							# connections
							strConn = ''
							for strDep in listTokens[nEntryIndex][6] :
								for strVarConnection in listTokens[nEntryIndex][6][strDep] :
									strConn += strDep + '>' + strVarConnection + ';'
							if len( strConn ) > 0 :
								strEntry += '[' + strConn + '] '

				if style in [ 'highlighted_vars' ] :
					if listTokens[nEntryIndex][3] in set_var_types :
						if listTokens[nEntryIndex][5] == True :
							strEntry += '*'

				# print variable token even if its not in list (e.g. slot var) so we have context
				if style in [ 'highlighted_vars', 'plain_vars', 'tokens_only' ] :
					if listTokens[nEntryIndex][1] != None :
						strEntry += listTokens[nEntryIndex][1]

				if style in [ 'highlighted_vars' ] :
					if listTokens[nEntryIndex][3] in set_var_types :
						if listTokens[nEntryIndex][5] == True :
							strEntry += '*'

				if style in [ 'highlighted_vars', 'plain_vars' ] :
					if listTokens[nEntryIndex][3] in set_var_types :
						bCloseVar = True
						for nEntryIndexNext in range(len(listTokens)) :
							if listTokens[nEntryIndexNext][0] == nTokenIndex + 1 :
								if listTokens[nEntryIndexNext][4] == listTokens[nEntryIndex][4] :
									bCloseVar = False
									break

						if bCloseVar == True :
							strEntry += '}'
							strLastVar = None

				strLastVar = listTokens[nEntryIndex][4]
				break

		# not a var? use the token anyway so the pretty print text contains the filler tokens that can allow it to make human sense
		if len(strEntry) == 0 :
			if style in [ 'highlighted_vars', 'plain_vars', 'tokens_only' ] :
				strToken = dep_graph.nodes[ nTokenIndex ][ 'word' ]
				if strToken != None :
					strToken = strToken.replace( space_replacement_char, ' ' )
					strEntry = strToken
			strLastVar = None

		# add to list
		if len(strEntry) > 0 :
			listComponents.append( strEntry )

	# all done
	return ' '.join( listComponents )

def generate_proposition_set_from_extraction( list_extracted_vars = None, dep_graph = None, proposition_pattern = list_proposition_pattern_default, dict_displaced_context = dict_displaced_context_default, max_semantic_dist = None, include_context = True, space_replacement_char = '_', dict_sem_drift = dict_semantic_drift_default, dict_openie_config = None ) :
	"""
	generate a proposition set from a set of extracted variables from comp_sem_lib.match_extraction_patterns().

	:param list list_extracted_vars: list of variables from comp_sem_lib.match_extraction_patterns()
	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param list proposition_pattern: sequence of variable types to use to make a propositional expression
	:param int max_semantic_dist: max allowed semantic distance between vars in a proposition (can be None)
	:param bool include_context: include context variables within proposition phrases (maybe displaced from target variables in proposition_pattern)
	:param str space_replacement_char: replacement char for all token spaces. should be same as prepare_tags_for_dependency_parse()
	:param dict dict_sem_drift: dict of semantic drift costs for dep types e.g. { 'conj' : 2 }
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of tuples = (prop_phrase,prop_head,prop_addr_list,head_addr_list,pattern_index,proposition_pattern) or None. prop_phrase = propositional expression from extraction as defined by requested pattern [arg_phrase, rel_phrase, arg_phrase]. prob_head = propositional expression's head tokens [arg_head, rel_head, arg_head]. pattern_index = index of original extraction pattern that generated this proposition.
	:rtype: list
	"""

	if not isinstance( list_extracted_vars, (list,tuple) ) :
		raise Exception( 'invalid list_extracted_vars' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( proposition_pattern, list ) :
		raise Exception( 'invalid proposition_pattern' )
	if not isinstance( dict_displaced_context, dict ) :
		raise Exception( 'invalid dict_displaced_context' )
	if not isinstance( max_semantic_dist, (int,type(None)) ) :
		raise Exception( 'invalid max_semantic_dist' )
	if not isinstance( include_context, bool ) :
		raise Exception( 'invalid include_context' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( dict_sem_drift, dict ) :
		raise Exception( 'invalid dict_sem_drift' )

	# index node tree
	dictNodeAddrSet = construct_node_index(
		dep_graph = dep_graph,
		dict_openie_config = dict_openie_config )

	# get index of variable inter-connections
	( dictVarNetwork, dictVarConnections, dictVarContextConnections ) = index_cross_variable_connections(
		list_variables = list_extracted_vars,
		dict_sem_drift = dict_sem_drift,
		dict_openie_config = dict_openie_config )

	# make a list of variable data we need
	# note: pattern index will be same for all extracted vars as they will have come from same extraction pattern
	listSortedVars = []
	nPatternIndexProposition = None
	for nIndexVar in range(len(list_extracted_vars)) :
		( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) = list_extracted_vars[nIndexVar]

		# get var base
		if not '_' in strVar :
			raise Exception('invalid variable : ' + repr(strVar) )
		strVarBase = strVar.split('_')[0]

		if (include_context == False) and (strVarBase.startswith('ctxt')) :
			continue

		# add to list
		listSortedVars.append( ( strType, strVar, nAddress, listCollapsed, strVarBase ) )
		nPatternIndexProposition = nPatternIndex

	# sort variables by head address
	listSortedVars = sorted( listSortedVars, key=lambda entry: entry[2], reverse=False )

	# check displaced context is OK
	for strType in proposition_pattern :
		if not strType in dict_displaced_context :
			raise Exception( 'type ' + repr(strType) + ' missing in dict_displaced_context' )

	# compile a set of all possible propositions
	# work out the length of the semantic distance from 1st var to last var (including backtracking if it occurs)
	listCandidates = []
	for strTargetVarType in proposition_pattern :

		# dict_openie_config['logger'].info( 'P4 = ' + repr(strTargetVarType) + ' : ' + repr(len(listCandidates)) )

		# remember last candidate set and use it as a base for adding new target matches
		listCandidatesBase = listCandidates
		listCandidates = []

		# loop on each base candidate and get the list of previous var indexes, so we do not allow a target var match with an address that appears before the previous var
		listVarPrevious = []
		if len(listCandidatesBase) == 0 :
			listVarPrevious.append( -1 )
		else :
			for nIndexBase in range(len(listCandidatesBase)) :
				( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) = listCandidatesBase[nIndexBase][-1]
				listVarPrevious.append( nIndexVar )

		# dict_openie_config['logger'].info( 'P4.1 = ' + repr(listVarPrevious) )

		# get all possible next targets for each candidate base
		nCandidateBaseIndex = 0
		for nIndexVarPrevious in listVarPrevious :
			# note vars already in this pattern
			setVarsInPattern = set([])
			for nIndexVar in range( 0, nIndexVarPrevious+1 ) :
				( strType1, strVar1, nAddress1, listCollapsed1, strVarBase1 ) = listSortedVars[nIndexVar]
				setVarsInPattern.add( strVarBase1 )

			# find next instance of this type, ignoring variables that appear before the previous match
			for nIndexVar in range( nIndexVarPrevious+1, len(listSortedVars) ) :
				( strType1, strVar1, nAddress1, listCollapsed1, strVarBase1 ) = listSortedVars[nIndexVar]

				if (not strVarBase1 in setVarsInPattern) and (strType1 == strTargetVarType) :

					# add to output proposition
					setVarsInPattern.add( strVarBase1 )
					nIndexVarPrevious = nIndexVar

					# add the collapsed set of variable token addresses (for any variable who has this base)
					listTokenAddr = []
					listTokenAddrDisplaced = []
					listHeadAddr = []
					for ( strType2, strVar2, nAddress2, listCollapsed2, strVarBase2 ) in listSortedVars :
						if strVar2.startswith( strVarBase1 ) :
							listTokenAddr.extend( listCollapsed2 )

							# remove any subsumed addresses from head so its the minimal head of dep graph branch
							# use original dep_graph for this as we want the top nodes in graph regardless of collapse settings
							bSubsumed = False
							for ( strType3, strVar3, nAddress3, listCollapsed3, strVarBase3 ) in listSortedVars :
								if (strVar3 != strVar2) and (strVar3.startswith( strVarBase1 ) == True) :
									if nAddress2 in dictNodeAddrSet[nAddress3] :
										bSubsumed = True
										break

							if bSubsumed == False :
								listHeadAddr.append( nAddress2 )

					#if strVar1 == 'rel2_2' :
					# dict_openie_config['logger'].info( 'P1 = ' + repr(listTokenAddr) )

					# get a list of all directly and indirectly connected context variables from this base var
					setConnectedContext = set([])
					for (strConnectedVar, nStep, strDepWalk) in dictVarContextConnections[strVarBase1] :
						if strConnectedVar.startswith('ctxt') :
							# should we allow this connected context to be part of the target variable? or displace its tokens to adjacent vars
							# note: strDepWalk can make multiple steps so we cannot do a naive string match e.g. nmod > nmod > acl
							listSplitDepWalk = strDepWalk.split('>')
							bDisplace = False
							for strDepStep in listSplitDepWalk :
								for strAllowedDep in dict_displaced_context[strTargetVarType] :
									if strAllowedDep.endswith(':*') :
										listAllowed = strAllowedDep.split(':')
										if ( strDepStep.startswith( listAllowed[0] + ':' ) == True ) :
											bDisplace = True
											break
									elif strDepStep == strAllowedDep :
										bDisplace = True
										break
								if bDisplace == True :
									break

							setConnectedContext.add( ( strConnectedVar, bDisplace ) )

					#if strVar1 == 'rel2_2' :
					# dict_openie_config['logger'].info( 'P2 = ' + repr(setConnectedContext) )

					# find all connected context vars in list, and add the collapsed addresses
					for ( strType2, strVar2, nAddress2, listCollapsed2, strVarBase2 ) in listSortedVars :
						tupleAdd = None
						for ( strConnectedVar, bDisplace ) in setConnectedContext :
							if strVar2.startswith( strConnectedVar ) :
								tupleAdd = ( listCollapsed2, bDisplace )
								break
					
						if tupleAdd != None :
							if tupleAdd[1] == True :
								listTokenAddrDisplaced.extend( tupleAdd[0] )
							else :
								listTokenAddr.extend( tupleAdd[0] )

					#if strVar1 == 'arg3_2' :
					# dict_openie_config['logger'].info( 'P3 = ' + repr(listTokenAddr) )

					# add this target match to each candidate base to make a new viable proposition
					# dict_openie_config['logger'].info( 'P4.1 (sem dist) = ' + repr(dictVarConnections) )
					if len(listCandidatesBase) == 0 :

						# add new candidate (first variable, semantic distance 0)
						listPropositionNew = [ ( strVarBase1, sorted( listTokenAddr ), sorted( listTokenAddrDisplaced ), listHeadAddr, nIndexVar ) ]
						listCandidates.append( listPropositionNew )

					else :

						# append to existing candidates, to make new ones
						listProposition = listCandidatesBase[nCandidateBaseIndex]

						# add new candidate
						listPropositionNew = copy.copy( listProposition )
						listPropositionNew.append( ( strVarBase1, sorted( listTokenAddr ), sorted( listTokenAddrDisplaced ), listHeadAddr, nIndexVar ) )
						listCandidates.append( listPropositionNew )

		# if target not found at all then there will be no viable candidates generated
		if len(listCandidates) == 0 :
			# dict_openie_config['logger'].info( 'P5 not found' )
			return None

	# for each candidate calculate the overall semantic distance between its variables
	listSemDist = []
	for listProposition in listCandidates :
		#dict_openie_config['logger'].info( 'P6.1.0 (sem dist) = ' + repr(dictVarConnections) )
		#dict_openie_config['logger'].info( 'P6.1 (sem dist) = ' + repr(listProposition) )

		# calculate the semantic distance between all variables
		# find a variable which is connected to all the others.
		# add up the semantic distances from this root var.
		# if any connected variable is already linked to another variable, subtract this from distance (e.g. attr1 > entity4[1] & entity2[1] & prep3[2] == dist 4, but if entity2 > prep3 [1] so dist == 4 - 1 == 3)

		setVarsCandidate = set([])
		for ( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) in listProposition :
			setVarsCandidate.add( strVarBase )

		strVarBaseRoot = None
		nSemanticDistance = 0

		# check if any var contains all other vars (e.g. ctxt6 > rel2 > arg3, ctxt6 > arg1)
		for strVarToCheck in dictVarConnections :

			# check if this var links to all other vars (i.e. its the root)
			strVarBaseRoot = strVarToCheck
			dictDist = {}
			for ( strConnectedVar, nStepConnected, strDepWalk ) in dictVarConnections[strVarToCheck] :
				if strConnectedVar in setVarsCandidate :
					# get shortest path if there is more than one path (e.g. direct or via a context var)
					if strConnectedVar in dictDist :
						if dictDist[strConnectedVar] > nStepConnected :
							dictDist[strConnectedVar] = nStepConnected
					else :
						dictDist[strConnectedVar] = nStepConnected

			if strVarBaseRoot in setVarsCandidate :
				nNumNeeded = len(setVarsCandidate)-1
			else :
				nNumNeeded = len(setVarsCandidate)

			if len(dictDist) < nNumNeeded :
				# keep looking if not found all candidate variables except root (or for a ctxt root all candidate variables)
				strVarBaseRoot = None
				nSemanticDistance = 0
			else :
				# stop looking if found
				nSemanticDistance = 0
				for strConnectedVar in dictDist :
					nSemanticDistance = nSemanticDistance + dictDist[strConnectedVar]
				break

		# check if any var is linked to by all other vars (e.g. arg1 > rel2, arg3 > rel2)
		if strVarBaseRoot == None :
			# try extracted variables
			for strVarToCheck in setVarsCandidate :

				# check if any var links to this var (i.e. its the child)
				strVarBaseRoot = strVarToCheck
				dictDist = {}
				for strVarToCheck2 in setVarsCandidate :
					if strVarToCheck != strVarToCheck2 :
						for ( strConnectedVar, nStepConnected, strDepWalk ) in dictVarConnections[strVarToCheck2] :
							if strConnectedVar == strVarToCheck :
								# get shortest path if there is more than one path (e.g. direct or via a context var)
								if strVarToCheck2 in dictDist :
									if dictDist[strVarToCheck2] > nStepConnected :
										dictDist[strVarToCheck2] = nStepConnected
								else :
									dictDist[strVarToCheck2] = nStepConnected

				if strVarBaseRoot in setVarsCandidate :
					nNumNeeded = len(setVarsCandidate)-1
				else :
					nNumNeeded = len(setVarsCandidate)

				if len(dictDist) < nNumNeeded :
					# keep looking if not found
					strVarBaseRoot = None
					nSemanticDistance = 0
				else :
					# stop looking if found
					nSemanticDistance = 0
					for strConnectedVar in dictDist :
						nSemanticDistance = nSemanticDistance + dictDist[strConnectedVar]
					break

		if strVarBaseRoot == None :
			raise Exception( 'no single root var connecting others : ' + repr(setVarsCandidate) + ' : ' + repr(dictVarConnections) )

		# subtract paths embedded in other paths (to avoid double counting)
		for strVarToCheck in dictDist :
			for ( strConnectedVar, nStepConnected, strDepWalk ) in dictVarConnections[strVarToCheck] :
				if (strConnectedVar != strVarBaseRoot) and (strConnectedVar in setVarsCandidate) :
					nSemanticDistance = nSemanticDistance - nStepConnected

		'''
		# subtract paths embedded in other paths
		for strVarToCheck in dictVarConnections :
			if strVarToCheck != strVarBaseRoot :
				for ( strConnectedVar, nStepConnected, strDepWalk ) in dictVarConnections[strVarToCheck] :
					if strConnectedVar in setVarsCandidate :
						nSemanticDistance = nSemanticDistance - nStepConnected
		'''

		#dict_openie_config['logger'].info( 'P6.2 (sem dist) = ' + repr(nSemanticDistance) + ' : ' + repr(dictDist) )
		listSemDist.append( nSemanticDistance )

	# compile an index of unique variable combinations, and the candidate propositions that use them
	dictIndexCandidates = {}
	for nIndexCandidate in range(len(listCandidates)) :
		listProposition = listCandidates[nIndexCandidate]
		nDist = listSemDist[nIndexCandidate]

		listVars = []
		for ( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) in listProposition :
			listVars.append( strVarBase )
		tupleVarSet = tuple( listVars )

		if not tupleVarSet in dictIndexCandidates :
			dictIndexCandidates[tupleVarSet] = [ ( listProposition, nDist ) ]
		else :
			dictIndexCandidates[tupleVarSet].append( ( listProposition, nDist ) )

	# select for each unique variable combination only the best (or joint best) propositions based on lowest semantic distance
	for tupleVarSet in dictIndexCandidates :
		#dict_openie_config['logger'].info( 'P7.1 (varset) = ' + repr(tupleVarSet) + ' len ' + str(len(dictIndexCandidates[tupleVarSet])) )

		# sort by score (lowest first)
		dictIndexCandidates[tupleVarSet] = sorted( dictIndexCandidates[tupleVarSet], key=lambda entry: entry[1], reverse=False )

		# get top N with same score (best is first in list)
		nDistBest = dictIndexCandidates[tupleVarSet][0][1]

		# if best is worse than the max allowed semantic distance, then delete all entries
		if (max_semantic_dist != None) and (nDistBest > max_semantic_dist) :
			nDistBest = -1

		# apply filter to choose best only
		nPropIndex = 0
		while nPropIndex < len(dictIndexCandidates[tupleVarSet]) :
			if dictIndexCandidates[tupleVarSet][nPropIndex][1] != nDistBest :
				del dictIndexCandidates[tupleVarSet][nPropIndex]
			else :
				nPropIndex = nPropIndex + 1

		#dict_openie_config['logger'].info( 'P7.2 (varset) = ' + repr(nDistBest) + ' len ' + str(len(dictIndexCandidates[tupleVarSet])) )

	# return a propositional structure for every unqiue set of variables we could get from this extraction
	listFinalSet = []
	for tupleVarSet in dictIndexCandidates :

		listPropOptions = dictIndexCandidates[tupleVarSet]
		for ( listProposition, nDist ) in listPropOptions :

			# assign addresses so they appear in propositional variable order, with token overlaps handled.
			# if an address overlaps with a previous variable, allow its tokens to be re-assigned to that variable so the logical sent order is not lost
			# e.g. sometimes a 'while' or 'and' might be in dep graph one var, but appear much earlier in sentence
			listPhrasesProposition = []
			listHeadProposition = []
			listRangeProposition = []
			for nIndex in range(len(listProposition)) :
				( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) = listProposition[nIndex]
				listPhrasesProposition.append( [] )
				listRangeProposition.append( ( min(listHeadAddr), max(listHeadAddr) ) )

			for nIndex in range(len(listProposition)) :
				( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) = listProposition[nIndex]

				# note head tokens (if head gets displaced then it will be rejected later anyway)
				listHeadProposition.append( listHeadAddr )

				# variable addresses should be assigned to the variable they come from, unless the token address range falls within another variables range
				for nAddr in listTokenAddr :

					# default assignment is the variable the token addr comes from
					nAssignment = nIndex

					# check if addr is inside previous var address range, if so assign to the previous 
					for nIndexPrev in range( 0, nIndex ) :
						if len(listPhrasesProposition[ nIndexPrev ]) > 0 :
							if nAddr <= max( listPhrasesProposition[ nIndexPrev ] ) :
								nAssignment = nIndexPrev
								break

					# check if the addr is > any future var's head address range
					for nIndexNext in range( len(listPhrasesProposition)-1, nIndex, -1 ) :
						if nAddr >= listRangeProposition[ nIndexNext ][0] :
							nAssignment = nIndexNext
							break

					# add address to the assigned var
					listPhrasesProposition[ nAssignment ].append( nAddr )

				# displaced addresses should not (unless no alternative) be assigned to the variable they are connected to (e.g. subject of a verb)
				for nAddr in listTokenAddrDisplaced :

					# default displaced assignment is left or right based on position relative to current proposition (which will have non-displaced tokens populated already like head tokens)
					# unless its in the middle then we keep it in current proposition
					if len(listPhrasesProposition[ nIndex ]) > 0 :
						if nAddr < min( listPhrasesProposition[ nIndex ] ) :
							if (nIndex-1 >= 0) :
								nAssignment = nIndex-1
						elif nAddr > max( listPhrasesProposition[ nIndex ] ) :
							if (nIndex+1 < len(listPhrasesProposition)) :
								nAssignment = nIndex+1
						else :
							nAssignment = nIndex
					else :
						# if current proposition is empty dont displace as no point
						nAssignment = nIndex

					# check if addr is inside previous var address range, if so assign to the previous 
					for nIndexPrev in range( 0, nIndex ) :
						if len(listPhrasesProposition[ nIndexPrev ]) > 0 :
							if nAddr <= max( listPhrasesProposition[ nIndexPrev ] ) :
								nAssignment = nIndexPrev
								break

					# check if the addr is > any future var's head address range
					for nIndexNext in range( len(listPhrasesProposition)-1, nIndex, -1 ) :
						if nAddr >= listRangeProposition[ nIndexNext ][0] :
							nAssignment = nIndexNext
							break

					# add address to the assigned var
					listPhrasesProposition[ nAssignment ].append( nAddr )

			# check if the head tokens of each var appear in a proposition of the right type
			# if not reject the proposition, as it might be {arg, arg, rel} where we asked for {arg,rel,arg}
			bInvalid = False
			for nIndex in range(len(listProposition)) :
				( strVarBase, listTokenAddr, listTokenAddrDisplaced, listHeadAddr, nIndexVar ) = listProposition[nIndex]
				for nAddrHead in listHeadAddr :
					if not nAddrHead in listPhrasesProposition[ nIndex ] :
						bInvalid = True
						break
				if bInvalid == True :
					break

			if bInvalid == True :
				#dict_openie_config['logger'].info( 'P8 invalid' )
				return None

			# create phrases from lists of addresses
			listPhraseText = []
			listHeadText = []
			bOK = True
			for nIndex in range(len(listPhrasesProposition)) :
				listPhrase = []
				listAddr = sorted( listPhrasesProposition[nIndex] )
				for nAddr in listAddr :
					strToken = dep_graph.nodes[nAddr]['word']
					if strToken != None :
						strToken = strToken.replace( space_replacement_char, ' ' )
					listPhrase.append( strToken )

				if len(listPhrase) == 0 :
					bOK = False

				listPhraseText.append( ' '.join( listPhrase ) )

				listPhrase = []
				listAddr = sorted( listHeadProposition[nIndex] )
				for nAddr in listAddr :
					strToken = dep_graph.nodes[nAddr]['word']
					if strToken != None :
						strToken = strToken.replace( space_replacement_char, ' ' )
					listPhrase.append( strToken )

				if len(listPhrase) == 0 :
					bOK = False

				listHeadText.append( ' '.join( listPhrase ) )

			if bOK == True :
				listFinalSet.append( ( listPhraseText, listHeadText, listPhrasesProposition, listHeadProposition, nPatternIndexProposition, proposition_pattern ) )

	# all done
	return listFinalSet

def filter_proposition_set( list_proposition_set = None, list_proposition_set_conf = None, target_index = 1, filter_strategy = 'prop_subsumption', dict_index_stoplist_prefix = dict_index_stoplist_prefix_default, dict_index_stoplist_suffix = dict_index_stoplist_suffix_default, lex_phrase_index = None, lex_uri_index = None, dict_openie_config = None ) :
	
	"""
	filter a proposition set selecting the best target. filtered entries are deleted from list_proposition_set

	filter strategy:
		* min_length - group propositions at target_index which share a common head address. sort this group by address length (target_index first, then other indexes). select top of list (min length) as single option.
		* max_length - group propositions at target_index which share a common head address. sort this group by address length (target_index first, then other indexes). select bottom of list (max length) as single option.
		* prop_subsumption - remove any n-gram proposition that is subsumed by a higher gram proposition.
		* lexicon_filter - remove any n-gram proposition which does not at least 1 variable with a lexicon phrase match (unigram, bigram and trigrams are checked with morphy).

	:param list list_proposition_set: list of tuples obtained from calls to comp_sem_lib.generate_proposition_set_from_extraction(). filtered entries will be removed from this set.
	:param list list_proposition_set_conf: list of confidence values associated with each proposition. filtered entries will be removed from this set.
	:param int target_index: proposition index of target variable to base filtering on (e,.g. index of rel)
	:param str filter_strategy: filter strategy = min_length|max_length
	:param dict index_stoplist_prefix: dict of prefixes for each index to not allow e.g. 'of ' on first argument of {arg,rel,arg}
	:param dict index_stoplist_suffix: dict of suffixes for each index to not allow e.g. ' and' on rel argument of {arg,rel,arg}
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()
	"""

	if not isinstance( list_proposition_set, list ) :
		raise Exception( 'invalid list_proposition_set' )
	if not isinstance( list_proposition_set_conf, list ) :
		raise Exception( 'invalid list_proposition_set_conf' )
	if not isinstance( target_index, (int,type(None)) ) :
		raise Exception( 'invalid target_index' )
	if not isinstance( filter_strategy, str ) :
		raise Exception( 'invalid filter_strategy' )
	if not isinstance( dict_index_stoplist_prefix, (dict,type(None)) ) :
		raise Exception( 'invalid dict_index_stoplist_prefix' )
	if not isinstance( dict_index_stoplist_suffix, (dict,type(None)) ) :
		raise Exception( 'invalid dict_index_stoplist_suffix' )
	if not isinstance( lex_phrase_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_phrase_index' )
	if not isinstance( lex_uri_index, (dict,type(None)) ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if not filter_strategy in ['min_length','max_length','prop_subsumption','lexicon_filter'] :
		raise Exception( 'Invalid filter strategy : ' + repr(filter_strategy) )

	if len(list_proposition_set) == 0 :
		return

	# filter out any proposition that contains a prefix stoplist term
	if dict_index_stoplist_prefix != None :
		nIndex1 = 0
		while nIndex1 < len(list_proposition_set) :
			( listPhraseText, listHeadText, listPhrasesProposition, listHeadProposition, nPatternIndexProposition, listPropPattern ) = list_proposition_set[nIndex1]

			bBad = False
			for nIndexProp in dict_index_stoplist_prefix :
				if nIndexProp > len(listPhraseText) :
					bBad = True
				else :
					listStoplist = dict_index_stoplist_prefix[nIndexProp]
					for strPrefix in listStoplist :
						if listPhraseText[nIndexProp].startswith( strPrefix ) :
							bBad = True
							break
				if bBad == True :
					break

			if bBad == True :
				#dict_openie_config['logger'].info( 'PREFIX FAIL = ' + repr(list_proposition_set[nIndex1]) )
				del list_proposition_set[nIndex1]
				del list_proposition_set_conf[nIndex1]
			else :
				nIndex1 = nIndex1 + 1

	# filter out any proposition that contains a suffix stoplist term
	if dict_index_stoplist_suffix != None :
		nIndex1 = 0
		while nIndex1 < len(list_proposition_set) :
			( listPhraseText, listHeadText, listPhrasesProposition, listHeadProposition, nPatternIndexProposition, listPropPattern ) = list_proposition_set[nIndex1]

			bBad = False
			for nIndexProp in dict_index_stoplist_suffix :
				if nIndexProp > len(listPhraseText) :
					bBad = True
				else :
					listStoplist = dict_index_stoplist_suffix[nIndexProp]
					for strSuffix in listStoplist :
						if listPhraseText[nIndexProp].endswith( strSuffix ) :
							bBad = True
							break
				if bBad == True :
					break

			if bBad == True :
				#dict_openie_config['logger'].info( 'SUFFIX FAIL = ' + repr(list_proposition_set[nIndex1]) )
				del list_proposition_set[nIndex1]
				del list_proposition_set_conf[nIndex1]
			else :
				nIndex1 = nIndex1 + 1

	if len(list_proposition_set) == 0 :
		return

	# debug
	'''
	for entry in list_proposition_set :
		dict_openie_config['logger'].info( 'PROP1 = ' + repr( entry[0] ) )
		dict_openie_config['logger'].info( '      = ' + repr( entry[1] ) )
		dict_openie_config['logger'].info( '      = ' + repr( entry[3] ) )
	'''

	if filter_strategy in ['min_length','max_length'] :

		if target_index == None :
			raise Exception( 'target_index none : ' + repr(filter_strategy) )

		# debug
		'''
		for entry in list_proposition_set :
			dict_openie_config['logger'].info( 'PROP = ' + repr( entry[0] ) )
		for entry in list_proposition_set_conf :
			dict_openie_config['logger'].info( 'CONF = ' + repr( entry[0] ) )
		'''

		# apply filter strategy with whats left based on prop size for each unique prop head
		nIndex1 = 0
		while nIndex1 < len(list_proposition_set) :
			# get head addr range for target variable (e.g. rel)
			if target_index >= len(list_proposition_set[nIndex1][3]) :
				raise Exception( 'target_index out of range of prop set tuples' )
			setHeadAddr1 = set( list_proposition_set[nIndex1][3][target_index] )

			# get phrase addr range for target variable
			nSizeTarget1 = len( list_proposition_set[nIndex1][2][target_index] )

			# get phrase addr range for others
			nSizeOther1 = 0
			for nIndexOther in range(len(list_proposition_set[nIndex1][2])) :
				if nIndexOther != target_index :
					if len( list_proposition_set[nIndex1][2][nIndexOther] ) > nSizeOther1 :
						nSizeOther1 = len( list_proposition_set[nIndex1][2][nIndexOther] )

			# start a group
			listGroup = [ (nIndex1, nSizeTarget1, nSizeOther1 ) ]

			nIndex2 = nIndex1 + 1
			while nIndex2 < len(list_proposition_set) :
				# get head addr range for target
				if target_index >= len(list_proposition_set[nIndex2][3]) :
					raise Exception( 'target_index out of range of prop set tuples' )
				setHeadAddr2 = set( list_proposition_set[nIndex2][3][target_index] )

				# get phrase addr range for target
				nSizeTarget2 = len( list_proposition_set[nIndex2][2][target_index] )

				# get phrase addr range for others
				nSizeOther2 = 0
				for nIndexOther in range(len(list_proposition_set[nIndex2][2])) :
					if nIndexOther != target_index :
						if len( list_proposition_set[nIndex2][2][nIndexOther] ) > nSizeOther2 :
							nSizeOther2 = len( list_proposition_set[nIndex2][2][nIndexOther] )

				# head address overlap for target index? if so add to group to be filtered
				if len( setHeadAddr1.intersection( setHeadAddr2 ) ) > 0 :
					listGroup.append( (nIndex2, nSizeTarget2, nSizeOther2 ) )

				# next
				nIndex2 = nIndex2 + 1

			# debug
			#dict_openie_config['logger'].info( 'GROUP = ' + repr( listGroup ) )

			if len(listGroup) > 1 :

				# sort group (target phrase size first, then other phrase size)
				if filter_strategy == 'min_length' :
					listGroup = sorted( listGroup, key=lambda entry: entry[1] * 10000 + entry[2], reverse=False )
				elif filter_strategy == 'max_length' :
					listGroup = sorted( listGroup, key=lambda entry: entry[1] * 10000 + entry[2], reverse=True )

				# delete (in reverse order to preserve index during delete) all of group except minimum size option
				listIndexToDelete = []
				for entry in listGroup[1:] :
					listIndexToDelete.append( entry[0] )
				listIndexToDelete = sorted( listIndexToDelete, reverse=True )

				#dict_openie_config['logger'].info( 'DELETE = ' + repr( listIndexToDelete ) )

				for nIndexToDelete in listIndexToDelete :
					del list_proposition_set[nIndexToDelete]
					del list_proposition_set_conf[nIndexToDelete]

				# re-check this index after deletion in case it was removed
				nIndex1 = nIndex1 - 1

			# next
			nIndex1 = nIndex1 + 1

	elif filter_strategy == 'prop_subsumption' :

		# apply filter strategy with whats left based on prop subsumption
		# if a prop subsumes another, then perfer it
		# e.g. (It, really has, increased, the size), (It, increased, the size) >> (It, really has, increased, the size)

		
		# debug
		'''
		for entry in list_proposition_set :
			dict_openie_config['logger'].info( 'PROP1 = ' + repr( entry[0] ) )
		'''
		

		setToDelete = set([])
		nIndex1 = 0
		while nIndex1 < len(list_proposition_set) :
			( listPhraseText1, listHeadText1, listPhrasesProposition1, listHeadProposition1, nPatternIndexProposition1, listPropPattern1 ) = list_proposition_set[nIndex1]

			nIndex2 = nIndex1 + 1
			while nIndex2 < len(list_proposition_set) :
				( listPhraseText2, listHeadText2, listPhrasesProposition2, listHeadProposition2, nPatternIndexProposition2, listPropPattern2 ) = list_proposition_set[nIndex2]

				# check the largest prop
				if len(listPhraseText1) > len(listPhraseText2) :
					nCheckA = nIndex1
					nCheckB = nIndex2
				elif len(listPhraseText2) > len(listPhraseText1) :
					nCheckA = nIndex2
					nCheckB = nIndex1
				else :
					nCheckA = None
					nCheckB = None

				if nCheckA != None :
					( listPhraseTextA, listHeadTextA, listPhrasesPropositionA, listHeadPropositionA, nPatternIndexPropositionA, listPropPatternA ) = list_proposition_set[nCheckA]
					( listPhraseTextB, listHeadTextB, listPhrasesPropositionB, listHeadPropositionB, nPatternIndexPropositionB, listPropPatternB ) = list_proposition_set[nCheckB]

					# check for sequential matches
					setMatch = set([])
					nPhraseB = 0
					for nPhraseA in range(len(listPhraseTextA)) :
						if listPhraseTextA[nPhraseA] == listPhraseTextB[nPhraseB] :
							setMatch.add( nPhraseA )
							nPhraseB = nPhraseB + 1
							if nPhraseB >= len(listPhraseTextB) :
								break
					
					# has A subsumed B?
					if len(setMatch) == len(listPhraseTextB) :
						setToDelete.add( nCheckB )
				
				nIndex2 = nIndex2 + 1

			nIndex1 = nIndex1 + 1

		#dict_openie_config['logger'].info( 'PROP1 del = ' + repr( setToDelete ) )

		listIndexToDelete = sorted( list(setToDelete), reverse=True )
		for nIndexToDelete in listIndexToDelete :
			del list_proposition_set[nIndexToDelete]
			del list_proposition_set_conf[nIndexToDelete]

	elif filter_strategy == 'lexicon_filter' :

		# apply filter strategy with whats left based on phrase lookup in a lexicon
		# if at least 1 variable matches a lexicon phrase then keep it, otherwise filter the extraction out

		setToDelete = set([])
		nIndex1 = 0
		while nIndex1 < len(list_proposition_set) :
			( listPhraseText1, listHeadText1, listPhrasesProposition1, listHeadProposition1, nPatternIndexProposition1, listPropPattern1 ) = list_proposition_set[nIndex1]

			bOK = False
			for nIndexPhrase in range(len(listPhraseText1)) :
				listPhrase = listPhraseText1[nIndexPhrase].split(' ')

				# from each proposition variable extraction we compute all possible 1/2/3-gram phrases
				# and check them with the lexicon for a match
				listPhrasesForEachGram = soton_corenlppy.common_parse_lib.create_ngram_tokens(
					listPhrase,
					max_gram = 3,
					sent_temination_tokens = None )

				for listPhraseSet in listPhrasesForEachGram :
					for tuplePhraseToCheck in listPhraseSet :
						listPhraseToCheck = list( tuplePhraseToCheck )

						# lexicon match using a head token of the last token in a phrase
						# e.g. [rotten,yellow,Bananas] -> head = Bananas
						#      morphy will be applied to last term, so Bananas = Banana
						#      head term must appear in any n-gram phrase to be matched
						#      so a lexicon with Banana in its index will match this target phrase
						listLexiconMatch = soton_corenlppy.lexico.lexicon_lib.phrase_lookup(
							phrase_tokens = listPhraseToCheck,
							head_token = listPhraseToCheck[-1],
							lex_phrase_index = lex_phrase_index,
							lex_uri_index = lex_uri_index,
							max_gram = 5,
							stemmer = None,
							apply_wordnet_morphy = True,
							hyphen_variant = False,
							dict_lexicon_config = dict_openie_config )
						
						# any lexicon match is enough to save this proposition
						if len(listLexiconMatch) > 0 :
							bOK = True
							break

					if bOK == True :
						break

				if bOK == True :
					break

			if bOK == False :
				setToDelete.add( nIndex1 )
				
			nIndex1 = nIndex1 + 1

		#dict_openie_config['logger'].info( 'PROP1 del = ' + repr( setToDelete ) )

		listIndexToDelete = sorted( list(setToDelete), reverse=True )
		for nIndexToDelete in listIndexToDelete :
			del list_proposition_set[nIndexToDelete]
			del list_proposition_set_conf[nIndexToDelete]

	# debug
	'''
	for entry in list_proposition_set :
		dict_openie_config['logger'].info( 'PROP2 = ' + repr( entry[0] ) )
	'''


def encode_extraction( list_extracted_vars = None, dep_graph = None, set_var_types = set([]), dict_pretty_dep_rels = dict_pretty_print_var_dep_rels_default, space_replacement_char = '_', dict_openie_config = None ) :
	"""
	encode an extraction in a serialize format that can be parsed using comp_sem_lib.parse_encoded_extraction()

	:param list list_extracted_vars: list of variables from comp_sem_lib.match_extraction_patterns()
	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param set set_var_types: set of {var} types for pretty print
	:param dict dict_pretty_dep_rels: dict of dep rels to allow in pretty print based on address position relative to head { 'any' : [], 'not_before_head' : [],'not_after_head' : [] }
	:param str space_replacement_char: replacement char for all token spaces
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: encoded extraction
	:rtype: unicode
	"""

	if not isinstance( list_extracted_vars, (list,tuple) ) :
		raise Exception( 'invalid list_extracted_vars' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( set_var_types, set ) :
		raise Exception( 'invalid set_var_types' )
	if not isinstance( dict_pretty_dep_rels, dict ) :
		raise Exception( 'invalid dict_pretty_dep_rels' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )

	# loop on each variable in order
	listComponents = []
	for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extracted_vars :
		if strType in set_var_types :

			# tuple = ( pretty_print_variable, head_token, { dep : [ var,var... ], ... }, address )
			# version with DET etc removed for easier lexicon matching
			tuplePretty = pretty_print_extraction_var(
				list_extracted_vars = list_extracted_vars,
				dep_graph = dep_graph,
				var_name = strVar,
				dict_pretty_dep_rels = dict_pretty_dep_rels,
				space_replacement_char = space_replacement_char,
				dict_openie_config = dict_openie_config )

			# get a version with no filtering (true human pretty print)
			tuplePrettyAll = pretty_print_extraction_var(
				list_extracted_vars = list_extracted_vars,
				dep_graph = dep_graph,
				var_name = strVar,
				dict_pretty_dep_rels = None,
				space_replacement_char = space_replacement_char,
				dict_openie_config = dict_openie_config )

			# encode variable information
			strEntry = '{' +strVar + ' '

			if tuplePretty[1] != None :
				strEntry += '[head=' + escape_extraction_pattern( tuplePretty[1] ) + '] '

			strEntry += '[addr=' + str(nAddress) + '] '

			strConn = ''
			for strDepPath in tuplePretty[2] :
				# strVarConnection == 'nmod>dep' etc
				for strVarConnection in tuplePretty[2][strDepPath] :
					strConn += strDepPath + '>' + strVarConnection + ';'
			if len( strConn ) > 0 :
				strEntry += '[' + strConn + '] '

			# extraction template pattern index that extracted this variable
			strEntry += '[pindex=' + str(nPatternIndex) + '] '

			# pretty print = ... pretty_lexicon ... [] ... pretty_human ...
			strEntry += escape_extraction_pattern( tuplePretty[0] ) + '[]' + escape_extraction_pattern( tuplePrettyAll[0] ) + '}'

			# add to list
			listComponents.append( strEntry )

	# all done
	return ' '.join( listComponents )

def parse_encoded_extraction( encoded_str = None, dict_openie_config = None ) :
	"""
	parse an encoded extraction produced from comp_sem_lib.encode_extraction().
	variables ordered by address

	:param unicode encoded_str: encoded extraction from comp_sem_lib.pretty_print_extraction( style='encoded' )
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of extracted variables = [ ( var_name, var_head, var_phrase, { dep_path : [ var,var... ], ... }, address, pattern_index, var_phrase_human ), ... ]
	:rtype: list
	"""

	if not isinstance( encoded_str, str ) :
		raise Exception( 'invalid encoded_str' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# examples
	# {arg1 [head=Lakeshore]Lakeshore virus} {rel2 [neg] warning} {arg3 [case>rel2] Cook}
	# {arg1 Lakeshore virus} {rel2 warning} {arg3 [genuine] [case>rel2] Cook}
	# note: the encoded text has been escaped by comp_sem_lib.pretty_print_extraction() so {}[] will not appear in phrases

	listResult = []

	# extract each variable
	listVars = encoded_str.split('}')
	for nIndex in range(len(listVars)) :
		# last } will create an empty string using split
		if len(listVars[nIndex]) > 0 :
			# add } back in as we used it to split the variables
			listVars[nIndex] = listVars[nIndex].strip() + '}'

			# run regex to parse variable
			matchObj = regexEncodedExtraction.match( listVars[nIndex] )
			if matchObj != None :
				strVarName = None
				strHead = None
				nAddr = 0
				nPatternIndex = None
				dictConnection = {}

				if 'VAR' in matchObj.groupdict() :
					strVarName = matchObj.groupdict()['VAR']

				if 'HEAD' in matchObj.groupdict() :
					#[head=...]
					strHead = matchObj.groupdict()['HEAD']
					if strHead != None :
						# remove space at end
						strHead = strHead.strip()
						strHead = unescape_extraction_pattern( strHead[6:-1] )
						if len(strHead) == 0 :
							raise Exception( 'parse error : bad head value : ' + listVars[nIndex] + ' : ' + encoded_str )

				if 'ADDR' in matchObj.groupdict() :
					#[addr=...]
					strAddr = matchObj.groupdict()['ADDR']
					if strAddr != None :
						# remove space at end
						strAddr = strAddr.strip()
						strAddr = unescape_extraction_pattern( strAddr[6:-1] )
						if len(strAddr) == 0 :
							raise Exception( 'parse error : bad addr value : ' + listVars[nIndex] + ' : ' + encoded_str )
						if not strAddr.isdigit() :
							raise Exception( 'parse error : bad addr value : ' + listVars[nIndex] + ' : ' + encoded_str )
						nAddr = int( strAddr )

				if 'PATTERN_INDEX' in matchObj.groupdict() :
					#[pindex=...]
					strPatternIndex = matchObj.groupdict()['PATTERN_INDEX']
					if strPatternIndex != None :
						# remove space at end
						strPatternIndex = strPatternIndex.strip()
						strPatternIndex = unescape_extraction_pattern( strPatternIndex[8:-1] )
						if len(strPatternIndex) == 0 :
							raise Exception( 'parse error : bad pattern index value : ' + listVars[nIndex] + ' : ' + encoded_str )
						if not strPatternIndex.isdigit() :
							raise Exception( 'parse error : bad pattern index value : ' + listVars[nIndex] + ' : ' + encoded_str )
						nPatternIndex = int( strPatternIndex )

				if 'CONNECTION' in matchObj.groupdict() :
					#[nsubj>arg1;dobj>arg2...]
					strConn = matchObj.groupdict()['CONNECTION']
					if strConn != None :
						strConn = strConn.strip()
						strConn = strConn[1:-1]
						listConn = strConn.split(';')
						for conn in listConn :
							# ignore last one
							if len(conn) == 0 :
								continue
							# syntax check
							if not '>' in conn :
								raise Exception('parse error : invalid connection : ' + repr(conn) + ' : ' + encoded_str )

							# get the last '>' in the dep string e.g. nmod>dep>arg1
							nCountDep = conn.count('>')
							if nCountDep == 1 :
								nIndexConn = conn.index( '>' )
							else :
								nIndexConn = -1
								for nIndexDep in range(nCountDep) :
									nIndexConn = nIndexConn + 1 + conn[nIndexConn+1:].index( '>' )

							strDep = conn[:nIndexConn]
							strVarConn = conn[nIndexConn+1:]
							if (len(strDep) == 0) or (len(strVarConn) == 0) :
								raise Exception('parse error : invalid connection : ' + repr([conn,strDep,strVarConn]) + ' : ' + encoded_str )

							if not strDep in dictConnection :
								dictConnection[strDep] = set([])
							dictConnection[strDep].add( strVarConn )

				if 'PHRASE' in matchObj.groupdict() :
					strPhrase = matchObj.groupdict()['PHRASE']
					if strPhrase != None :
						# pretty print = ... pretty_lexicon ... [] ... pretty_human ...
						if not '[]' in strPhrase :
							raise Exception( 'parse error : missing break token : ' + listVars[nIndex] + ' : ' + encoded_str )
						nIndexBreakToken = strPhrase.index( '[]' )
						strPhraseLexicon = strPhrase[ 0 : nIndexBreakToken ]
						strPhraseHuman = strPhrase[ nIndexBreakToken+2 : ]

						strPhraseLexicon = strPhraseLexicon.strip()
						strPhraseLexicon = unescape_extraction_pattern( strPhraseLexicon )
						if len(strPhraseLexicon) == 0 :
							raise Exception( 'parse error : bad phrase lexicon value : ' + listVars[nIndex] + ' : ' + encoded_str )

						strPhraseHuman = strPhraseHuman.strip()
						strPhraseHuman = unescape_extraction_pattern( strPhraseHuman )
						if len(strPhraseHuman) == 0 :
							raise Exception( 'parse error : bad phrase human value : ' + listVars[nIndex] + ' : ' + encoded_str )

				if strVarName == None :
					raise Exception( 'parse error : missing var name : ' + listVars[nIndex] + ' : ' + encoded_str )
				if strPhrase == None :
					raise Exception( 'parse error : missing phrase : ' + listVars[nIndex] + ' : ' + encoded_str )

				tupleEntry = ( strVarName, strHead, strPhraseLexicon, dictConnection, nAddr, nPatternIndex, strPhraseHuman )
				listResult.append( tupleEntry )
			else :
				raise Exception( 'parse error : ' + listVars[nIndex] + ' : ' + encoded_str )

	# sort by address (earliest first)
	listResult = sorted( listResult, key=lambda entry: entry[4], reverse=False )

	# all done
	return listResult


def get_extraction_vars( list_extracted_vars = None, dict_openie_config = None ) :
	"""
	return a list of extraction variable names and types from an extraction

	:param list list_extracted_vars: list of variables from comp_sem_lib.match_extraction_patterns()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of tuple = ( variable_name, variable_type )
	:rtype: list
	"""

	if not isinstance( list_extracted_vars, (list,tuple) ) :
		raise Exception( 'invalid list_extracted_vars' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listResult = []
	for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extracted_vars :
		listResult.append( ( strVar, strType ) )

	# all done
	return listResult

def pretty_print_extraction_var( list_extracted_vars = None, dep_graph = None, var_name = None, dict_pretty_dep_rels = dict_pretty_print_var_dep_rels_default, space_replacement_char = '_', dict_openie_config = None ) :
	"""
	pretty print a specific variable in a specific extraction from comp_sem_lib.match_extraction_patterns(). pretty printed text appears in lexical order for easier reading.

	:param list list_extracted_vars: list of variables from comp_sem_lib.match_extraction_patterns()
	:param nltk.parse.DependencyGraph dep_graph: dependency graph parsed using a dependency parser such as nltk.parse.stanford.StanfordDependencyParser()
	:param str var_name: name of variable
	:param dict dict_pretty_dep_rels: dict of dep rels to allow in pretty print based on address position relative to head { 'any' : [], 'before_head' : [],'after_head' : [] }. None allows any dep
	:param str space_replacement_char: replacement char for all token spaces. should be same as prepare_tags_for_dependency_parse()
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: tuple = ( pretty_print_variable, head_token, (negated, genuine), { dep_path : [ var,var... ], ... } )
	:rtype: tuple
	"""

	if not isinstance( list_extracted_vars, (list,tuple) ) :
		raise Exception( 'invalid list_extracted_vars' )
	if not isinstance( dep_graph, nltk.parse.DependencyGraph ) :
		raise Exception( 'invalid dep_graph' )
	if not isinstance( var_name, str ) :
		raise Exception( 'invalid var_name' )
	if not isinstance( dict_pretty_dep_rels, (dict,type(None)) ) :
		raise Exception( 'invalid dict_pretty_dep_rels' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )
	if not isinstance( space_replacement_char, str ) :
		raise Exception( 'invalid space_replacement_char' )

	# compile a list of (address, word, var, head_flag, dictConnections, nPatternIndex) for this variable
	listTokens = []
	for ( strType, strVar, nAddress, listCollapsed, dictConnections, nPatternIndex ) in list_extracted_vars :
		if strVar == var_name :
			nHeadAddr = nAddress

			for nAddressCollapsed in listCollapsed :
				if nAddressCollapsed == nAddress :
					bHead = True
				else :
					bHead = False
				strRel = dep_graph.nodes[ nAddressCollapsed ][ 'rel' ]
				strToken = dep_graph.nodes[ nAddressCollapsed ][ 'word' ]
				if strToken != None :
					strToken = strToken.replace( space_replacement_char, ' ' )
				listTokens.append( ( nAddressCollapsed, strToken, strRel, strType, strVar, bHead, dictConnections ) )

	if nHeadAddr == None :
		raise Exception( 'variable not found' )

	# sort list by address order so pretty print tokens come out in the word sequence of the original sent
	listTokens = sorted( listTokens, key=lambda entry: entry[0], reverse=False )

	# pretty print variable
	# only use a set of pre-defined dep rels to avoid variable pretty print containing stuff like DET which would make automated lexicon matching very difficult later
	listComponents = []
	strHead = None
	dictConnections = {}
	for nEntryIndex in range(len(listTokens)) :

		nAddrEntry = listTokens[nEntryIndex][0]
		strRel = listTokens[nEntryIndex][2]

		# check for head token (and use subj/obj/case links of the head)
		if listTokens[nEntryIndex][5] == True :
			strHead = listTokens[nEntryIndex][1]
			dictConnections = listTokens[nEntryIndex][6]

		# add token to pretty print for variable
		bOK = False
		if nAddrEntry == nHeadAddr :
			bOK = True
		elif dict_pretty_dep_rels == None :
			bOK = True
		elif strRel in dict_pretty_dep_rels['any'] :
			bOK = True
		elif (strRel in dict_pretty_dep_rels['before_head']) and (nAddrEntry < nHeadAddr) :
			bOK = True
		elif (strRel in dict_pretty_dep_rels['after_head']) and (nAddrEntry > nHeadAddr) :
			bOK = True

		if (bOK == False) or (listTokens[nEntryIndex][1] == None) :
			# not a pretty print dep, or no token at all, so ignore it
			continue

		listComponents.append( listTokens[nEntryIndex][1] )

	# all done
	return ( ' '.join( listComponents ), strHead, dictConnections )


