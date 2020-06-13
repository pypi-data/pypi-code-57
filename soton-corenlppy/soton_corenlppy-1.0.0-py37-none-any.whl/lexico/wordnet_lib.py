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

Wordnet lexicon processing

"""

import array,sys,codecs,os,re,copy,math
import nltk.corpus
from nltk.corpus import wordnet
from nltk.corpus import verbnet

# VERBNET http://www.nltk.org/howto/corpus.html#word-lists-and-lexicons
# WORDNET http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
# WordNet POS filter = # ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
# hyponyms = narrower term
# hypernyms = broader term
# inherited_hypernyms = hypernym of hypernym ...
# sister = hyponyms of hypernym ...

def get_synset( wordnet_synset_name, dict_lexicon_config = None ) :
	"""
	lookupword in wordnet and return the synset match (or None)

	:param str wordnet_synset_name: valid wordnet name such as dog.n.01
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: wordnet synset
	:rtype: nltk.corpus.reader.wordnet.Synset
	"""

	if not isinstance( wordnet_synset_name, str ) :
		raise Exception( 'invalid wordnet_synset_name' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	return wordnet.synset( wordnet_synset_name )

def get_synset_names( lemma, pos='asrnv', lang='eng', dict_lexicon_config = None ) :
	"""
	lookup lemma and return all possible synset names

	:param unicode lemma: lemma to lookup
	:param str pos: WordNet POS filter
	:param str lang: WordNet language
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: list of nltk.corpus.reader.wordnet.Synset (empty if none found) e.g. [Synset('dog.n.01'), Synset('frump.n.01'), Synset('dog.n.03'), Synset('cad.n.01')]
	:rtype: list
	"""

	if not isinstance( lemma, str ) :
		raise Exception( 'invalid lemma' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	return wordnet.synsets( lemma, pos=pos, lang=lang )

def get_lemma( set_lexicon, syn, lang='eng', pos='asrnv', dict_lexicon_config = None ) :
	"""
	get all lemma (direct and derived) for a WordNet synset and add them to set_lexicon. 

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# check syn is of right type
	if not syn.pos() in pos :
		return

	for lemma in syn.lemmas( lang=lang ) :

		# add names of direct lemmas
		# wordnet serialization = <syn-name>.<lemma-name>
		set_lexicon.add( syn.name() + '.' + lemma.name() )

		# add derived lemmas also if they match pos filter
		for lemmaDerived in lemma.derivationally_related_forms() :
			synDerived = lemmaDerived.synset()

			# check syn is right type
			if not synDerived.pos() in pos :
				continue

			set_lexicon.add( synDerived.name() + '.' + lemmaDerived.name() )

def get_lemma_with_freq( set_lexicon, syn, lang='eng', pos='asrnv', dict_lexicon_config = None ) :
	"""
	get all lemma with a freq count

	:param set set_lexicon: set of tuples = ( nltk.corpus.reader.wordnet.Lemma, count )
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# check syn is of right type
	if not syn.pos() in pos :
		return

	for lemma in syn.lemmas( lang=lang ) :
		# add names of direct lemmas
		# wordnet serialization = <syn-name>.<lemma-name>
		set_lexicon.add( ( syn.name() + '.' + lemma.name(), lemma.count() ) )

		# add derived lemmas also if they match pos filter
		for lemmaDerived in lemma.derivationally_related_forms() :
			synDerived = lemmaDerived.synset()

			# check syn is of right type
			if not synDerived.pos() in pos :
				return

			set_lexicon.add( ( synDerived.name() + '.' + lemmaDerived.name(), lemmaDerived.count() ) )


def inherited_hypernyms( set_lexicon, syn, lang = 'eng', pos='asrnv', max_depth=3, depth=0, dict_lexicon_config = None ) :
	"""
	get all inherited wordnet hypernym synsets and add them to set_lexicon. 
	hypernyms: Y is a hypernym of X if every X is a (kind of) Y (canine is a hypernym of dog)

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param int max_depth: maximum depth for inherited search
	:param int depth: current depth (internal recursive use only)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( max_depth, int ) :
		raise Exception( 'invalid max_depth' )
	if not isinstance( depth, int ) :
		raise Exception( 'invalid depth' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# limit depth of inheritance to avoid very abstract terms being added
	if depth > max_depth :
		return

	for synHyper in syn.hypernyms() :
		if synHyper.pos() in pos :
			inherited_hypernyms( set_lexicon=set_lexicon, syn=synHyper, lang=lang, pos=synHyper.pos(), max_depth=max_depth, depth=depth+1, dict_lexicon_config=dict_lexicon_config )
			get_lemma( set_lexicon=set_lexicon, syn=synHyper, lang=lang, pos=pos, dict_lexicon_config=dict_lexicon_config  )


def inherited_hyponyms( set_lexicon, syn, lang = 'eng', pos='asrnv', max_depth=3, depth=0, dict_lexicon_config = None ) :
	"""
	get all inherited wordnet hyponym synsets and add them to set_lexicon. 
	hyponyms: Y is a hyponym of X if every Y is a (kind of) X (dog is a hyponym of canine)
	troponym: the verb Y is a troponym of the verb X if the activity Y is doing X in some manner (to lisp is a troponym of to talk)
	in NLTK WordNet hyponyms (nouns) == troponym (verbs)

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param int max_depth: maximum depth for inherited search
	:param int depth: current depth (internal recursive use only)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( max_depth, int ) :
		raise Exception( 'invalid max_depth' )
	if not isinstance( depth, int ) :
		raise Exception( 'invalid depth' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# limit depth of inheritance to avoid very abstract terms being added
	if depth > max_depth :
		return

	for synHypo in syn.hyponyms() :
		if synHypo.pos() in pos :
			inherited_hyponyms( set_lexicon=set_lexicon, syn=synHypo, lang=lang, pos=synHypo.pos(), max_depth=max_depth, depth=depth+1, dict_lexicon_config=dict_lexicon_config )
			get_lemma( set_lexicon, syn=synHypo, lang=lang, pos=pos, dict_lexicon_config=dict_lexicon_config )


def expand_hypernyms( set_lexicon, syn, lang = 'eng', pos='asrnv', max_depth=3, depth=0, dict_lexicon_config = None ) :
	"""
	get all inherited wordnet hypernym synsets and sisters (immediate hyponyms), and add them to set_lexicon. 
	hyponyms: Y is a hyponym of X if every Y is a (kind of) X (dog is a hyponym of canine)
	troponym: the verb Y is a troponym of the verb X if the activity Y is doing X in some manner (to lisp is a troponym of to talk)
	in NLTK WordNet hyponyms (nouns) == troponym (verbs)

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param int max_depth: maximum depth for inherited search
	:param int depth: current depth (internal recursive use only)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( max_depth, int ) :
		raise Exception( 'invalid max_depth' )
	if not isinstance( depth, int ) :
		raise Exception( 'invalid depth' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# limit depth of inheritance to avoid very abstract terms being added
	if depth > max_depth :
		return

	inherited_hypernyms( set_lexicon=set_lexicon, syn=syn, lang=lang, pos=syn.pos(), max_depth=max_depth, depth=depth+1, dict_lexicon_config=dict_lexicon_config )

	for synHyper in syn.hypernyms() :
		if synHyper.pos() in pos :
			for synHypo in synHyper.hyponyms() :
				if synHypo.pos() == synHyper.pos() :
					get_lemma( set_lexicon=set_lexicon, syn=synHypo, lang=lang, pos=pos, dict_lexicon_config=dict_lexicon_config )


def inherited_entailments( set_lexicon, syn, lang = 'eng', pos='asrnv', max_depth=3, depth=0, dict_lexicon_config = None ) :
	"""
	get all inherited wordnet entailments synsets and add them to set_lexicon. 
	entailment: the verb Y is entailed by X if by doing X you must be doing Y (to sleep is entailed by to snore)

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param int max_depth: maximum depth for inherited search
	:param int depth: current depth (internal recursive use only)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( max_depth, int ) :
		raise Exception( 'invalid max_depth' )
	if not isinstance( depth, int ) :
		raise Exception( 'invalid depth' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# limit depth of inheritance to avoid very abstract terms being added
	if depth > max_depth :
		return

	for synEntail in syn.entailments() :
		if synEntail.pos() in pos :
			inherited_entailments( set_lexicon=set_lexicon, syn=synEntail, lang=lang, pos=synEntail.pos(), max_depth=max_depth, depth=depth+1, dict_lexicon_config=dict_lexicon_config )
			get_lemma( set_lexicon=set_lexicon, syn=synEntail, lang=lang, pos=pos, dict_lexicon_config=dict_lexicon_config )

def verb_groups( set_lexicon, syn, lang = 'eng', pos='v', dict_lexicon_config = None ) :
	"""
	get verb group for a synset and add them to set_lexicon. 
	verb group = Some similar senses of verbs have been grouped (manually) by the lexicographers

	:param set set_lexicon: set of WordNet lexicon synsets and lemma names
	:param nltk.corpus.reader.wordnet.Synset syn: WordNet synset
	:param str lang: WordNet language
	:param str pos: WordNet POS filter
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()
	"""

	if not isinstance( set_lexicon, set ) :
		raise Exception( 'invalid set_lexicon' )
	if not isinstance( syn, nltk.corpus.reader.wordnet.Synset ) :
		raise Exception( 'invalid syn' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	for synVerb in syn.verb_groups() :
		if synVerb.pos() in pos :
			get_lemma( set_lexicon=set_lexicon, syn=synVerb, lang=lang, pos=pos, dict_lexicon_config=dict_lexicon_config )


'''
# calculate lemmas in same verb class
# NOTE: only really useful to extract (from VNClass XML) the syntax e.g. NP[Agent] VERB NP[Source]
def lookup_verb( strTerm ) :
	listClassIDs = verbnet.classids( lemma = strTerm )
	for strClassID in listClassIDs :
		print strTerm
		print strClassID
		print 'LEMMA = ', repr( verbnet.lemmas( classid=strClassID )  )
		print 'VNCLASS = ', verbnet.pprint( verbnet.vnclass( fileid_or_classid=strClassID )  )
		print 'WN = ', repr( verbnet.wordnetids( classid=strClassID )  )
	sys.exit()
'''

def find_base_word_form( lemma = None, morphy_pos_list = None, dict_lexicon_config = None ) :
	"""
	use wordnet to find the base form of a word. original lemma case is preserved where possible.

	:param unicode lemma: lemma to lookup
	:param str morphy_pos_list: WordNet POS_LIST entry (see morphy) or None
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config()

	:return: base phrase after WordNet lookup, or None if none found
	:rtype: unicode
	"""
	strWordToCheck = lemma.lower()
	strBase = wordnet.morphy( form = strWordToCheck, pos = morphy_pos_list )
	if strBase == None :
		return None
	else :
		# in order to preserve the original case we will edit the original word so it fits the base form from morphy
		if strWordToCheck.startswith( strBase ) :
			# return the original characters (in original case) that match the word
			return lemma[:len(strBase)]
		else :
			# base word is not a simply suffix removal, so just return it in its lower case form
			return strBase
