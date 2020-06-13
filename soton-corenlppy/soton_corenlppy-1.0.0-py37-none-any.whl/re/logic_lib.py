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

Logical proposition library

"""

import array,sys,codecs,os,re,copy,math
import numpy, nltk.corpus
import soton_corenlppy.re

# TODO provide an alternative function to compute on-the-fly DRT and execute it using DRTParser (see strategy). this allows amorpha resolution and much more complex lexico patterns
# TODO compare results of two methods directly


def compute_logical_proposition_from_relations( list_sent_trees, lex_verb, lex_entity, dict_openie_config = None ) :
	"""
	for each sent extract component patterns for relations found, and associated lexio-pos patterns

	:param list list_sent_trees: list of nltk.Tree representing the sents in that doc after pos annotation
	:param dict lex_verb: dict of verb types, each with a set of TERMS
	:param dict lex_entity: dict of entity types, each with a set of TERMS
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: dict of logical propositions and a frequency count = { (subject,predicate,object) : freq_in_corpus }
	:rtype: dict
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'invalid list_sent_trees' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	dictPropositions = {}
	for treeSent in list_sent_trees :
		for leaf in treeSent :

			if leaf.label() == 'RELATION' :

				# get components for this relation
				listComponents = soton_corenlppy.re.comp_sem_lib.extract_components_from_relation( leaf, dict_openie_config = dict_openie_config )

				# calculate logical proposition
				strPredicate = None
				strSubject = None
				strObject = None

				#dict_openie_config['logger'].info( repr(listComponents) )

				for tupleComponent in listComponents :

					if tupleComponent[0] == 'VERB_P' :
						strMatchTarget = ' ' + tupleComponent[1] + ' '
						for strRelType in lex_verb :
							for strRelToken in lex_verb[strRelType] :
								# consider stemming here
								if ' ' + strRelToken + ' ' in strMatchTarget :
									strPredicate = strRelToken
									break

					if tupleComponent[0] in ['ENTITY','ENTITY_LIST'] :
						strMatchTarget = ' ' + tupleComponent[1] + ' '
						for strEntityType in lex_entity :
							for strEntityToken in lex_entity[strEntityType] :
								# consider stemming here
								if ' ' + strEntityToken + ' ' in strMatchTarget :
									if strPredicate == None :
										strSubject = strEntityType
									else :
										strObject = strEntityType

					#dict_openie_config['logger'].info( repr(tupleComponent) )
					#dict_openie_config['logger'].info( repr((strSubject,strPredicate,strObject)) )

				if strPredicate != None :
					tupleProposition = (strSubject,strPredicate,strObject)
					if not tupleProposition in dictPropositions :
						dictPropositions[ tupleProposition ] = 1
					else :
						dictPropositions[ tupleProposition ] = dictPropositions[ tupleProposition ] + 1

	return dictPropositions

	# OLD
	#   for phrase sequence in list_positive
	#     list_positive_components = list of main components of phrase sequence created by removing auxillary verbs, adjectives, adverbs (allow adv negative?)
	#   for phrase sequence in list_negative
	#     list_negative_components = list of main components of phrase sequence created by removing auxillary verbs, adjectives, adverbs (allow adv negative?)
	#   ??? apply FIM and refine list_positive and list_negative
	#   set_positive_components =- set( list_positive_components )
	#   set_negative_components =- set( list_negative_components )
	#   for components in set_positive_components
	#     support_pos = count( components ) in list_positive_components
	#     support_neg = count( components ) in list_negative_components
	#     confidence = support_pos / ( support_pos + support_neg )
	#     if confidence > threshold
	#       dict_final_patterns = { components : { lex_type : confidence } }


