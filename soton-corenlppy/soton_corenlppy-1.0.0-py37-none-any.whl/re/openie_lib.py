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

Open information extraction library

"""

import array,sys,codecs,os,re,copy,math
import soton_corenlppy

#
# treetagger POS tagger default openie patterns
#

dict_pos_phrase_patterns_default_treetagger = {
	'PROPER_NOUN_P' : set( [ 'NP', 'NPS' ] ),
	'NOUN_P' : set( [ 'NN', 'NNS' ] ),
	'VERB_P' : set( [ 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ' ] ),
	'VERB_AUXILLARY_P' : set( [ 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP','VH','VHD','VHG','VHN','VHZ','VHP' ] ),
	'DETERMINER_P' : set( [ 'DT', 'PDT', 'WDT', 'EX' ] ),
	'ADJECTIVE_P' : set( [ 'JJ', 'JJR', 'JJS' ] ),
	'PREPOSITION_P' : set( [ 'IN', 'IN/that', 'TO' ] ),
	'PRONOUN_P' : set( [ 'PP','PP$','WP','WP$' ] ),
	'ADVERB_P' : set( [ 'RB', 'RBR', 'RBS' ] ),
}


#
# stanford POS tagger default openie patterns
#

dict_pos_phrase_patterns_default_stanford = {
	'PROPER_NOUN_P' : set( [ 'NNP', 'NNPS' ] ),
	'NOUN_P' : set( [ 'NN', 'NNS' ] ),
	'VERB_P' : set( [ 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ' ] ),
	'DETERMINER_P' : set( [ 'DT', 'PDT', 'WDT', 'EX' ] ),
	'ADJECTIVE_P' : set( [ 'JJ', 'JJR', 'JJS' ] ),
	'PREPOSITION_P' : set( [ 'IN', 'TO' ] ),
	'PRONOUN_P' : set( [ 'PPR','PRP$','WP','WP$' ] ),
	'ADVERB_P' : set( [ 'RB', 'RBR', 'RBS' ] ),
}

#
# simply NP openie patterns
#

dict_pos_phrase_patterns_noun_phrases_stanford = {
	'PROPER_NOUN_P' : set( [ 'NNP', 'NNPS' ] ),
	'NOUN_P' : set( [ 'NN', 'NNS' ] ),
}



#
# phrase sequence pattern defaults based on ReVerb
# CITE: Anthony Fader, Stephen Soderland, and Oren Etzioni. 2011. Identifying relations for open information extraction. In Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP '11). Association for Computational Linguistics, Stroudsburg, PA, USA, 1535-1545
#

verb_pattern_expecting_preposition = r'(\(VERB_AUXILLARY_P [^)]*\) ){0,1}\(VERB_P [^)]*\)( \(VERB_AUXILLARY_P [^)]*\)){0,1}'
verb_pattern = r'(\((VERB_AUXILLARY_P|RP|MD|ADVERB_P) [^)]*\) ){0,1}\(VERB_P [^)]*\)( \((VERB_AUXILLARY_P|RP|MD|ADVERB_P) [^)]*\)){0,1}'
entities_pattern = r'\((ENTITY|ENTITY_LIST|ENTITY_AND_CONTEXT) [^)]*\)'
entities_and_context_entities_pattern = r'\((ENTITY|ENTITY_AND_CONTEXT|ADJECTIVE_P|ADVERB_P|DETERMINER_P) [^)]*\)'

list_phrase_sequence_patterns_exec_order_default = [ 'ENTITY','ENTITY_LIST','ENTITY_AND_CONTEXT','RELATION' ]

dict_phrase_sequence_patterns_default = {

	# Entity patterns (in strict order of execution from most specific to least)
	'ENTITY' : [
		re.compile( r'\A.*?(?P<ENTITY>\((PROPER_NOUN_P|NOUN_P) [^)]*\)( \((PROPER_NOUN_P|NOUN_P) [^)]*\)){0,5})', re.UNICODE | re.DOTALL ),
		re.compile( r'\A.*?(?P<ENTITY>\(PRONOUN_P [^)]*\))', re.UNICODE | re.DOTALL )
		],

	# List patterns for sets of entities (in strict order of execution from most specific to least)
	'ENTITY_LIST' : [
		re.compile( r'\A.*?(?P<ENTITY_LIST>\((ENTITY) [^)]*\)( (\((\,|\;|and) [^)]*\) ){0,1}\((ENTITY) [^)]*\)){1,5})', re.UNICODE | re.DOTALL )
		],

	# Entity context patterns (in strict order of execution from most specific to least)
	'ENTITY_AND_CONTEXT' : [
		re.compile( r'\A.*?(?P<ENTITY_AND_CONTEXT>\((ENTITY|ENTITY_LIST) [^)]*\) \(PREPOSITION_P [^)]*\)( \(DETERMINER_P [^)]*\)){0,1} \((ENTITY|ENTITY_LIST) [^)]*\))', re.UNICODE | re.DOTALL )
	],

	# Relation patterns (in strict order of execution from most specific to least)
	'RELATION' : [
		re.compile( r'\A.*?(?P<RELATION>' + entities_pattern + r' ' + verb_pattern_expecting_preposition + r'( ' + entities_and_context_entities_pattern + r'){0,5}( \(RP [^)]*\)){0,1} \(PREPOSITION_P [^)]*\)( \(DETERMINER_P [^)]*\)){0,1} ' + entities_pattern + r')', re.UNICODE | re.DOTALL ),
		re.compile( r'\A.*?(?P<RELATION>' + entities_pattern + r' ' + verb_pattern + r' ' + entities_pattern + r')', re.UNICODE | re.DOTALL ),
		re.compile( r'\A.*?(?P<RELATION>' + verb_pattern_expecting_preposition + r'( ' + entities_and_context_entities_pattern + r'){0,5}( \(RP [^)]*\)){0,1} \(PREPOSITION_P [^)]*\)( \(DETERMINER_P [^)]*\)){0,1} ' + entities_pattern + r')', re.UNICODE | re.DOTALL ),
		re.compile( r'\A.*?(?P<RELATION>' + verb_pattern + r' ' + entities_pattern + r')', re.UNICODE | re.DOTALL )
		]
}

#
# lexico-pos pattern rules defining when pattern generator adds
# terms and/or pos wildcards for different phrase sequence occurances
#

dict_lexio_pos_pattern_rule_default = {
	'ENTITY' : ('POS',),
	'ENTITY_LIST' : ('POS',),
	'ENTITY_AND_CONTEXT' : ('POS',),
	'CD' : ('POS',),
	'PREPOSITION_P' : ('POS',),
	'DETERMINER_P' : ('POS',),
	'ADJECTIVE_P' : ('POS',),
	'VERB_AUXILLARY_P' : ('POS',),
	'RP' : ('POS',),
	'ADVERB_P' : ('POS','TERM'),
	'VERB_P' : ('TERM',),
	}


#
# functions
#

def get_openie_config( **kwargs ) :
	"""
	return a openie config object.

	| note: a config object approach is used, as opposed to a global variable, to allow openie_lib functions to work in a multi-threaded environment

	:return: configuration settings to be used by all openie_lib functions
	:rtype: dict
	"""

	dictArgs = copy.copy( kwargs )

	# setup common values
	dictOpenIEConfig = soton_corenlppy.common_parse_lib.get_common_config( **dictArgs )

	# all done
	return dictOpenIEConfig


def calc_inverted_index_pos_phrase_patterns( dict_pos_phrase_patterns = dict_pos_phrase_patterns_default_treetagger, dict_openie_config = None ) :
	"""
	generate an inverted index from a dict of POS phrase patterns.

	:param dict dict_pos_phrase_patterns: definition of the set of POS tags that constitute each phrase pattern. POS tags cannot be shared between phrase patterns. { phrase_name : set( pos_tag, pos_tag ... ) }. default is setup for processing tagged output using TreeTagger.
	:param dict dict_openie_config: config object returned from openie_lib.get_openie_config() 

	:return: inverted POS pattern index = { pos_tag : phrase_name }
	:rtype: dict
	"""

	# generate the inverted index
	dictPhrasePatternInvertedIndex = {}
	for strPOSPattern in dict_pos_phrase_patterns :
		setPOSLabels = dict_pos_phrase_patterns[strPOSPattern]
		for strPOS in setPOSLabels :
			if strPOS in dictPhrasePatternInvertedIndex :
				raise Exception( 'each pos_tag is assigned to a single phrase pattern. pos_tag found assigned to more than one phrase pattern : ' + str(strPOS) )
			dictPhrasePatternInvertedIndex[ strPOS ] = strPOSPattern

	# all done
	return dictPhrasePatternInvertedIndex

