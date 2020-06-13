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

Lexicon bootstrapping library

"""

import array,sys,codecs,os,re,copy,math,warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim, nltk.corpus
#import numpy, scipy.sparse
import soton_corenlppy

#from fim import fpgrowth


#
# numpy 1.11
# scipy 0.18
# gensim 1.0.0 ==> pip install gensim
# fim ==> download compiled 64bit Windows/Linux python from http://www.borgelt.net/pyfim.html
#

#
# LSA https://radimrehurek.com/gensim/wiki.html#latent-semantic-analysis
# LDA https://radimrehurek.com/gensim/wiki.html#latent-dirichlet-allocation
# https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/gensim%20Quick%20Start.ipynb
#


def calc_topic_degree_lists( set_lexicon, list_topic_sets, term_degree = 1, stemmer = None, dict_lexicon_config = None ) :
	"""
	for all topics with seed words get a list of topics they appear in and a set of 1st degree topically relevant words.
	for topically relevant words get the topics they appear in, and a set of 2nd degree topically relevant words
	| e.g. statue -> topic [ statue, terracotta ] -> statue, terracotta, head, figure, hand, broken toe -> topic [ head, crown ], [ figure, zeus ] -> head, crown, figure, zeus

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param list list_topic_sets: list of topics, each of which is a list of terms
	:param int term_degree: use 1st or 2nd degree terms as calculated by lexicon_bootstrap_lib.calc_topic_degree_lists()
	:param nltk.stemmer stemmer: stemmer to use for result terms (or None)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: 1st and 2nd degree topic lists = (set_terms_1st_degree,set_terms_2nd_degree)

	:rtype: tuple
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( list_topic_sets, list ) :
		raise Exception( 'invalid list_topic_sets' )
	if not isinstance( term_degree, int ) :
		raise Exception( 'invalid term_degree' )
	if (stemmer != None) and (not isinstance( stemmer, nltk.stem.api.StemmerI )) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if not term_degree in [1,2] :
		raise Exception( 'invalid term_degree value - allowed = [1,2]' )

	listTopicIndex1stDegree = []
	setTerms1stDegree = set([])
	listTopicIndex2ndDegree = []
	setTerms2ndDegree = set([])

	for nIndexTopic1 in range(len(list_topic_sets)) :
		listFilterSet = list_topic_sets[nIndexTopic1]
		bMatch = False
		for strTopicTerm in listFilterSet :

			for strTerm in set_lexicon :
				listTermComponents = strTerm.split('.')
				strLemma = listTermComponents[0]
				if stemmer != None :
					strLemma = stemmer.stem( strLemma )

				if strTopicTerm == strLemma :
					listTopicIndex1stDegree.append( nIndexTopic1 )
					bMatch = True
					break
			if bMatch == True :
				break

	for nIndexTopic1 in listTopicIndex1stDegree :
		listFilterSet = list_topic_sets[nIndexTopic1]
		for strTopicTerm in listFilterSet :
			setTerms1stDegree.add( strTopicTerm )

	if term_degree == 1 :
		return setTerms1stDegree

	for nIndexTopic1 in range(len(list_topic_sets)) :
		listFilterSet = list_topic_sets[nIndexTopic1]
		for strTopicTerm in listFilterSet :
			if strTopicTerm in setTerms1stDegree :
				listTopicIndex2ndDegree.append( nIndexTopic1 )
				break

	for nIndexTopic1 in listTopicIndex2ndDegree :
		listFilterSet = list_topic_sets[nIndexTopic1]
		for strTopicTerm in listFilterSet :
			setTerms2ndDegree.add( strTopicTerm )

	return setTerms2ndDegree



def build_lda_model( bag_of_words, corpus_dictionary, num_topics = 100, num_passes = -1, chunksize = 4096, dict_lexicon_config = None ) :
	"""
	build a LDA topic model for a corpus
	| default parameters taken from Hoffman 2010 paper
	| see https://radimrehurek.com/gensim/models/ldamodel.html

	:param list bag_of_words: bag of words representation of corpus. [ [ (term_index,term_freq), ... N_term_in_doc ] ... N_doc ]
	:param gensim.corpora.dictionary.Dictionary() corpus_dictionary: dictionary of corpus { term_index : term_token ]
	:param int num_topics: number of LDA topics
	:param int num_passes: number of LDA passes (-1 to calculate based on corpus document size)
	:param int chunksize: size of chunks per pass
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: LDA model
	:rtype: gensim.models.ldamodel.LdaModel
	"""

	if not isinstance( bag_of_words, list ) :
		raise Exception( 'invalid bag_of_words' )
	if not isinstance( corpus_dictionary, gensim.corpora.dictionary.Dictionary ) :
		raise Exception( 'invalid corpus_dictionary' )
	if not isinstance( num_topics, int ) :
		raise Exception( 'invalid num_topics' )
	if not isinstance( num_passes, int ) :
		raise Exception( 'invalid num_passes' )
	if not isinstance( chunksize, int ) :
		raise Exception( 'invalid chunksize' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	nDocuments = len(bag_of_words)
	nMiniBatchSize = chunksize
	if num_passes == -1 :
		nPasses = int( nDocuments/nMiniBatchSize )
		if nPasses < 1 :
			nPasses = 1
	else :
		nPasses = num_passes

	if dict_lexicon_config['logger'] != None :
		dict_lexicon_config['logger'].info( 'running LDA size mini-batch size {0} and passes {1}'.format( nMiniBatchSize, nPasses ) )

	return gensim.models.ldamodel.LdaModel( corpus=bag_of_words, id2word=corpus_dictionary, num_topics=num_topics, update_every=1, chunksize=nMiniBatchSize, passes=nPasses )


def build_lsa_model( bag_of_words, corpus_dictionary, num_topics = 100, chunksize = 40000, onepass = False, power_iters = 3, extra_samples = 400, dict_lexicon_config = None ) :
	"""
	build a LDA topic model for a corpus
	| default parameters taken from Hoffman 2010 paper
	| see https://radimrehurek.com/gensim/models/lsimodel.html

	:param list bag_of_words: bag of words representation of corpus. [ [ (term_index,term_freq), ... N_term_in_doc ] ... N_doc ]
	:param gensim.corpora.dictionary.Dictionary() corpus_dictionary: dictionary of corpus { term_index : term_token ]
	:param int num_topics: number of LDA topics
	:param int chunksize: size of chunks per pass
	:param bool onepass: True if one pass only
	:param int power_iters: power iterations for multi-pass
	:param int extra_samples: oversampling factor for multipass
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: LDA model
	:rtype: gensim.models.lsimodel.LsiModel
	"""

	if not isinstance( bag_of_words, list ) :
		raise Exception( 'invalid bag_of_words' )
	if not isinstance( corpus_dictionary, gensim.corpora.dictionary.Dictionary ) :
		raise Exception( 'invalid corpus_dictionary' )
	if not isinstance( num_topics, int ) :
		raise Exception( 'invalid num_topics' )
	if not isinstance( chunksize, int ) :
		raise Exception( 'invalid chunksize' )
	if not isinstance( onepass, bool ) :
		raise Exception( 'invalid onepass' )
	if not isinstance( power_iters, int ) :
		raise Exception( 'invalid power_iters' )
	if not isinstance( extra_samples, int ) :
		raise Exception( 'invalid extra_samples' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if dict_lexicon_config['logger'] != None :
		dict_lexicon_config['logger'].info( 'running LSA chunksize {0} power iterations {1} oversampling {2}'.format( chunksize, power_iters,extra_samples ) )

	return gensim.models.lsimodel.LsiModel( corpus=bag_of_words, id2word=corpus_dictionary, num_topics=num_topics, chunksize=chunksize, onepass=onepass, power_iters=power_iters, extra_samples=extra_samples )


def build_tfidf_model( bag_of_words, corpus_dictionary, dict_lexicon_config = None ) :
	"""
	build a TF-IDF model for a corpus
	| see https://radimrehurek.com/gensim/models/tfidfmodel.html

	:param list bag_of_words: bag of words representation of corpus. [ [ (term_index,term_freq), ... N_term_in_doc ] ... N_doc ]
	:param gensim.corpora.dictionary.Dictionary() corpus_dictionary: dictionary of corpus { term_index : term_token ]
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: TF-IDF model
	:rtype: gensim.models.TfidfModel
	"""

	if not isinstance( bag_of_words, list ) :
		raise Exception( 'invalid bag_of_words' )
	if not isinstance( corpus_dictionary, gensim.corpora.dictionary.Dictionary ) :
		raise Exception( 'invalid corpus_dictionary' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if dict_lexicon_config['logger'] != None :
		dict_lexicon_config['logger'].info( 'running TF-IDF' )

	return gensim.models.TfidfModel( corpus=bag_of_words, id2word=corpus_dictionary, normalize=False )

def generate_topic_set( model, corpus_dictionary, threshold_score = -1.0, top_n = 100, num_topics = 100, dict_lexicon_config = None ) :
	"""
	construct a topic set of filtered terms using a pre-calculated gensim model (LDA or LSA)

	:param gensim.models.ldamodel.LdaModel or gensim.models.lsimodel.LsiModel model: pre-computed topic model
	:param gensim.corpora.dictionary.Dictionary() corpus_dictionary: dictionary of corpus { term_index : term_token ]
	:param float threshold_score: minimum threshold score for a term to be added to a topic. A value < 0 means the current default threshold score is used for LDA or LSI.
	:param int top_n: maximum number of terms per topic. there might be less than this number if terms fail thrshold check or there are simply insufficient available for a topic.
	:param int num_topics: number of topics in pre-computed model
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: list of topics, each being a list of terms for that topic
	:rtype: list
	"""

	if not isinstance( model, (gensim.models.ldamodel.LdaModel,gensim.models.lsimodel.LsiModel) ) :
		raise Exception( 'invalid model = ' + repr(type(model)) )
	if not isinstance( corpus_dictionary, gensim.corpora.dictionary.Dictionary ) :
		raise Exception( 'invalid corpus_dictionary' )
	if not isinstance( threshold_score, float ) :
		raise Exception( 'invalid threshold_score' )
	if not isinstance( num_topics, int ) :
		raise Exception( 'invalid num_topics' )
	if not isinstance( top_n, int ) :
		raise Exception( 'invalid top_n' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# get threshold values
	if isinstance( model, gensim.models.ldamodel.LdaModel ) :
		if threshold_score < 0 :
			nLDAThreshold = 0.001
		else :
			nLDAThreshold = threshold_score
	else :
		if threshold_score < 0 :
			nLSAThreshold = 0.01
		else :
			nLSAThreshold = threshold_score

	#
	# get topic sets of co-occuring words from LDA
	#
	listTopicSets = []
	for nTopic in range(num_topics) :

		if dict_lexicon_config['logger'] != None :
			dict_lexicon_config['logger'].info( 'topic = {0}'.format(num_topics) )

		listFilterSet = []
		listTermScores = []

		# LDA
		if isinstance( model, gensim.models.ldamodel.LdaModel ) :

			listTermIndexProb = model.get_topic_terms( nTopic, top_n )
			for (nTermIndex,nProb) in listTermIndexProb :
				if nProb >= nLDAThreshold :
					listTermScores.append( ( corpus_dictionary[nTermIndex],nProb ) )

		# LSI
		else :

			listTermIndexScore = model.show_topic( nTopic, top_n )
			for (strTerm,nScore) in listTermIndexScore :
				if math.fabs( nScore ) >= nLSAThreshold :
					listTermScores.append( ( strTerm,nScore ) )

		listTermScores = sorted( listTermScores, key=lambda entry: math.fabs( entry[1] ), reverse=True )

		for entry in listTermScores[0:top_n] :
			nLDAScore = entry[1]
			strTerm = entry[0]
			if dict_lexicon_config['logger'] != None :
				dict_lexicon_config['logger'].info( '\t {0} = {1}'.format( entry[0],entry[1] ) )

			listFilterSet.append( strTerm )

		listTopicSets.append( listFilterSet )

	return listTopicSets


def bootstrap_lexicon( seed_lexicon, topic_sets = None, tfidf_model = None, corpus_dictionary = None, threshold_score = -1.0, bootstrap_iterations = 1, term_degree = 1, stemmer = nltk.stem.porter.PorterStemmer(), hypo_depth = 3, hyper_depth = 1, entail_depth = 3, dict_lexicon_config = None ) :
	"""
	run bootstrapping algorithm to expand a lexicon using WordNet. on each iteration optionally filter tokens using pre-computed topic sets or a TF-IDF model to improve lexicon precision.
	seed lexicon can contain plain text tokens (without any period characters), which will be kept but not expanded. this allows specialist vocabulary outside WordNet to be added to the lexicon.

	:param set seed_lexicon: set of seed WordNet synset names OR plain text for lexicon e.g. set( [ 'red.s.01', 'ruby red' ] ). synsets will be expanded, plain text will not.
	:param list topic_sets: topic set calculated using lexicon_bootstrap_lib.generate_topic_set(). if None no topic model filtering will be applied
	:param gensim.models.TfidfModel tfidf_model: pre-computed topic model for filtering. if None no TF-IDF filtering will be applied
	:param gensim.corpora.dictionary.Dictionary corpus_dictionary: dictionary of corpus { term_index : term_token ] to be used with tf-idf model
	:param float threshold_score: minimum TF-IDF threshold score for a term to be added to a topic. A value < 0 means no threshold to be applied.
	:param int bootstrap_iterations: number of bootstrap iterations. each iteration will use the expanded lexicon as a seed. iterations beyond 1 risk losing lexicon precision but increase recall.
	:param int term_degree: use 1st or 2nd degree terms as calculated by lexicon_bootstrap_lib.calc_topic_degree_lists()
	:param nltk.stem.api.StemmerI stemmer: stemmer to us. A value of None will mean stemming is not applied to tokens.
	:param int hypo_depth: how deep to follow WordNet inherited hyponyms
	:param int hyper_depth: how deep to follow WordNet inherited hypernyms
	:param int entail_depth: how deep to follow WordNet inherited entailments
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: expanded sey of WordNet synset names OR plain text for lexicon e.g. set( [ 'ruby red', 'red.s.01','reddish.s.01' ] )
	:rtype: set
	"""

	if not isinstance( seed_lexicon, set ) :
		raise Exception( 'invalid seed_lexicon' )
	if (topic_sets != None) and (not isinstance( topic_sets, list )) :
		raise Exception( 'invalid topic_sets' )
	if not isinstance( bootstrap_iterations, int ) :
		raise Exception( 'invalid bootstrap_iterations' )
	if (tfidf_model != None) and (not isinstance( tfidf_model, gensim.models.TfidfModel )) :
		raise Exception( 'invalid tfidf_model' )
	if (corpus_dictionary != None) and (not isinstance( corpus_dictionary,gensim.corpora.dictionary.Dictionary )) :
		raise Exception( 'invalid corpus_dictionary' )
	if not isinstance( threshold_score, float ) :
		raise Exception( 'invalid threshold_score' )
	if not isinstance( term_degree, int ) :
		raise Exception( 'invalid term_degree' )
	if (stemmer != None) and (not isinstance( stemmer, nltk.stem.api.StemmerI )) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( hypo_depth, int ) :
		raise Exception( 'invalid hypo_depth' )
	if not isinstance( hyper_depth, int ) :
		raise Exception( 'invalid hyper_depth' )
	if not isinstance( entail_depth, int ) :
		raise Exception( 'invalid entail_depth' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	setLexicon = copy.deepcopy( seed_lexicon )

	#
	# bootstrap lexicon using WordNet to expand seed set of terms
	#
	for nIteration in range( bootstrap_iterations ) :

		# for this specific set of seed terms calc a set of allowed terms from the topic model
		setTermsAllowed = None
		if topic_sets != None :
			setTermsAllowed = calc_topic_degree_lists( set_lexicon = setLexicon, list_topic_sets = topic_sets, term_degree = term_degree, stemmer = stemmer, dict_lexicon_config = dict_lexicon_config )
			'''
			dict_lexicon_config['logger'].info( 'ALLOWED' )
			dict_lexicon_config['logger'].info( repr(setTermsAllowed) )
			sys.exit()
			'''

		#
		# token expansion using wordnet and verbnet
		#
		setLexiconExpanded = copy.deepcopy( setLexicon )
		for strTerm in setLexicon :

			setLexiconCandidates = set([])
			listTermComponents = strTerm.split('.')

			# WORDNET
			# http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
			# WordNet POS filter = # ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
			#listSyn = wordnet.synsets( strSeedTerm, pos=strPOSFilter, lang='eng' )
			if len( listTermComponents ) >= 3 :
				strSyn = '.'.join( listTermComponents[0:3] )
				syn = soton_corenlppy.lexico.wordnet_lib.get_synset( wordnet_synset_name = strSyn, dict_lexicon_config = dict_lexicon_config )

				#if strSeedTerm == 'statue' :
				#	print 'T0 = ', repr(listSyn)

				# word
				soton_corenlppy.lexico.wordnet_lib.get_lemma( set_lexicon = setLexiconCandidates, syn = syn, lang = 'eng', dict_lexicon_config = dict_lexicon_config )

				'''
				if strSeedTerm == 'green' :
					print strPOSFilter
					print syn.pos()
					print repr(syn)
					print 'T1 = ', repr(setLemmaNames)
				'''

				# broader sense of word (n deep) and sisters
				# if 1st iteration allow sisters, deeper iterations stick to inherited hypernyms only to avoid going too far off topic
				if nIteration == 0 :
					soton_corenlppy.lexico.wordnet_lib.expand_hypernyms( set_lexicon = setLexiconCandidates, syn = syn, lang = 'eng', pos=syn.pos(), max_depth=hyper_depth, dict_lexicon_config = dict_lexicon_config )
				else :
					soton_corenlppy.lexico.wordnet_lib.inherited_hypernyms( set_lexicon = setLexiconCandidates, syn = syn, lang = 'eng', pos=syn.pos(), max_depth=hyper_depth, dict_lexicon_config = dict_lexicon_config )

				'''
				if strSeedTerm == 'green' :
					print 'T2 = ', repr(setLemmaNames)
				'''

				# narrower sense of word
				soton_corenlppy.lexico.wordnet_lib.inherited_hyponyms( set_lexicon = setLexiconCandidates, syn = syn, lang = 'eng', pos=syn.pos(), max_depth=hypo_depth, dict_lexicon_config = dict_lexicon_config )

				'''
				if strSeedTerm == 'green' :
					print 'T3 = ', repr(setLemmaNames)
				'''

				soton_corenlppy.lexico.wordnet_lib.inherited_entailments( set_lexicon = setLexiconCandidates, syn = syn, lang = 'eng', pos=syn.pos(), max_depth=entail_depth, dict_lexicon_config = dict_lexicon_config )

				'''
				if strSeedTerm == 'green' :
					print 'T4 = ', repr(setLemmaNames)
				'''

			'''
			if strSeedTerm == 'green' :
				print 'T5 = ', repr(setLemmaNames)
				sys.exit()
			'''

			#print strSeedTerm, ' == ', setLemmaNames, '\n'

			#
			# token filtering using a topic filter
			#
			for strTerm in setLexiconCandidates :
				if not strTerm in setLexiconExpanded :

					# parse WordNet or VerbNet term
					listTermComponents = strTerm.split('.')

					# add sysets or plain text entries without any checks so they can be used as seeds for future iterations
					if len(listTermComponents) < 4 :
						setLexiconExpanded.add( strTerm )
						continue

					# check lemma against the LDA topic sets
					strTermClean = listTermComponents[3].lower().replace('_',' ')
					strTermAlt = strTermClean.lower().replace('-','')
					if stemmer != None :
						strTermClean = stemmer.stem( strTermClean )
						strTermAlt = stemmer.stem( strTermAlt )

					bRejectToken = False

					#
					# token filtering using LDA or LSI calculated topic sets
					#

					if topic_sets != None :

						bFilter = True
						for strTopicTerm in setTermsAllowed :
							if (strTermClean == strTopicTerm) or (strTermAlt == strTopicTerm) :
								bFilter = False
								break

						if bFilter == True :
							bRejectToken = True

					#
					# token filtering using TF-IDF model directly
					#

					if (tfidf_model != None) and (corpus_dictionary != None) and (threshold_score >= 0) :

						bFilter = True
						for strTermToCheck in (strTermClean,strTermAlt) :
							if strTermToCheck in list(corpus_dictionary.values()) :

								# vectorDoc = [ (term_index, term_freq), ... ]
								vectorDoc = corpus_dictionary.doc2bow( [ strTermToCheck ] )

								# vectorTFIDF = [ (term_index, tf-idf_score), ... ]
								vectorTFIDF = tfidf_model[ vectorDoc ]

								# only allow discriminating terms for seed values
								if vectorTFIDF[0][1] > threshold_score :
									bFilter = False

						if bFilter == True :
							bRejectToken = True

					# add lemma that appear in a topic set
					if bRejectToken == False :
						setLexiconExpanded.add( strTerm )

		# update lexicon for next iteration of bootstrapping
		setLexicon = setLexiconExpanded
	
	return setLexicon


'''
# removed for python3
def frequent_itemset_mining( list_phrase_sets, min_support = -2, dict_lexicon_config = None ) :
	"""
	run fpgrowth to compute a frequent item set from a set of phrase tokens

	:param list list_phrase_sets: list of sents, each a list of phrases = [ [ 'golden', 'statue', ... ] ]
	:param int min_support: fpgrowth minimum support (frequency of phrase in corpus) for use as a candidate
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: frequent item set = [ (phrase,support), ... ] e.g. [ ('golden', 'statue'), 2, ... ]
	:rtype: set
	"""

	if not isinstance( list_phrase_sets, list ) :
		raise Exception( 'invalid list_phrase_sets' )
	if not isinstance( min_support, int ) :
		raise Exception( 'invalid min_support' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# Frequent itemset mining (FIM)
	# software - PyFIM Christian Borgelt MIT license
	# library - http://www.borgelt.net/pyfim.html
	# examples - https://github.com/lucidfrontier45/pyarules/blob/master/pyfim/ex/chkfim.py
	# CITE> Christian Borgelt. 2005. An implementation of the FP-growth algorithm. In Proceedings of the 1st international workshop on open source data mining: frequent pattern mining implementations (OSDM '05). ACM, New York, NY, USA, 1-5. DOI=http://dx.doi.org/10.1145/1133905.1133907

	# get frequent item sets from this phrase set
	listItemSets = lexicopy.fim.fpgrowth( list_phrase_sets, supp = min_support, zmin = 2 )

	# sort in order of support
	listItemSets = sorted( listItemSets, key=lambda entry: math.fabs( entry[1] ), reverse=True )

	# return list
	return listItemSets

'''
