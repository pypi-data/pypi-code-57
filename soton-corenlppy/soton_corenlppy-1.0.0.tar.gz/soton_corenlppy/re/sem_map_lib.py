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
	// Created Date : 2017/07/23
	// Created for Project: GRAVITATE
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies: None
	//
	/////////////////////////////////////////////////////////////////////////
	'''

Semantic mapping for openie library

"""

import array,sys,codecs,os,re,copy,math,urllib.request,urllib.parse,urllib.error
import nltk, nltk.stem
import soton_corenlppy

# TODO encode in semantic mapping pattern the fact that its the 1st sent (for implied patterns)? seperate semantic mapping file entirely to be run only on 1st extractions?
#      use DRS for semantic mapping to generate productions?

# TODO how do we use lexicon and WordNet hypernyms? phrase expansion?

# TODO given a set of seed production triples (e.g. artifact made_of terracotta) can the semantic mapping patterns be learnt and then applied to other artifacts?

# TODO look at discourse analysis to resolve productions across sents e.g. statue of zeus; red fired clay; broken toes; thought to be created by scultpture of rhoads A1
#      (artifact == statue) (statue -> of zeus) (statue -> red fired clay) (statue -> broken toes) (statue -> thought to be created by scultpture of rhoads A1)

# see TODO's in file also


# regex for parsing semantic mapping variables
# e.g. {arg1:schema=<uri>|<uri>}
#      {prep2:phrase=result_of|from|of|by}
#      {rel1:skos=<uri>}
#      {arg3:}
regexSemanticMappingCondition = re.compile( r'\A\{(?P<TYPE>[a-zA-z]+)(?P<INDEX>[0-9]+)\:(schema\=(?P<SCHEMA>[^}]+)|phrase\=(?P<PHRASE>[^}]+)|skos\=(?P<SKOS>[^}]+)|)\}\Z', re.IGNORECASE | re.UNICODE )

# regex for parsing triple production
# e.g. {this;crm:P45_consists_of;arg2}
#      {arg1;<uri>;arg2}
regexSemanticMappingProduction = re.compile( r'\A\{(?P<SUBJECT>[^ ]+);(?P<PREDICATE>[^ ]+);(?P<OBJECT>[^ ]+)\}\Z', re.IGNORECASE | re.UNICODE )

def map_encoded_extraction_to_lexicon( extraction_vars = None, lex_phrase_index = None, lex_uri_index = None, only_best_matches = False, stemmer = None, max_gram = 5, dict_openie_config = None ) :
	"""
	for an extraction map variable phrases to lexicon phrases. this will semantically ground extracted phrases in the sent to lexicon URIs.
	a phrase gram size is associated with each variable semantic mapping. all potential mappings are returned but the highest gram size matches are most likely to be a good mapping.
	the confidence score is based on the precentage of tokens in an extracted variable that match the lexicon phrase.
	variables without a semantic mapping are removed from the final extraction list.
	the returned var_phrase and matched_phrase entries are lower() and have had tokens stemmed.

	:param list extraction_vars: extraction var produced from soton_corenlppy.re.comp_sem_lib.parse_encoded_extraction()
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param bool only_best_matches: only return variable matches with the highest confidence score for that variable
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param int max_gram: maximum phrase gram size to check for matches in lexicon. larger gram sizes means more lexicon checks, which is slower.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: semantically mapped sent extractions = [ [ (var_name, var_phrase, var_gram_size, [lexicon_uri, schema_uri, matched_phrase, phrase_gram_size, confidence_score] ), ... ]
	:rtype: list
	"""

	if not isinstance( extraction_vars, list ) :
		raise Exception( 'invalid extraction_vars' )
	if not isinstance( lex_uri_index, dict ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, dict ) :
		raise Exception( 'invalid lex_phrase_index' )
	if not isinstance( only_best_matches, bool ) :
		raise Exception( 'invalid only_best_matches' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( max_gram, int ) :
		raise Exception( 'invalid max_gram' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	# map each variable to lexicon
	listMappedVars = []
	for ( strVarName, strVarHead, strVarPhrase, tupleNegated, dictConnections, nAddr ) in extraction_vars :

		if strVarPhrase != None :
			listTokens = strVarPhrase.lower().split(' ')
		else :
			listTokens = []

		if strVarHead != None :
			strHeadToken = strVarHead.lower()
		else :
			strHeadToken = None

		if stemmer != None :
			for nIndex in range(len(listTokens)) :
				listTokens[nIndex] = stemmer.stem( listTokens[nIndex] )
			if strHeadToken != None :
				strHeadToken = stemmer.stem( strHeadToken )

		nVarGramSize = len(listTokens)

		if len(listTokens) > 0  :

			# match lexicon to phrase ngrams
			# listLexiconMatch = [ ( lexicon_uri, schema_uri, matched_phrase, match_gram_size, confidence_score ), ... ]
			listLexiconMatch = soton_corenlppy.lexico.lexicon_lib.phrase_lookup(
				phrase_tokens = listTokens,
				head_token = strHeadToken,
				lex_phrase_index = lex_phrase_index,
				lex_uri_index = lex_uri_index,
				max_gram = max_gram,
				dict_lexicon_config = dict_openie_config )

			# remove all but the highest confidence score results
			if only_best_matches == True :

				# get top confidence value
				nBestScore = None
				for nIndex in range(len(listLexiconMatch)) :
					if (nBestScore == None) or (listLexiconMatch[nIndex][4] > nBestScore) :
						nBestScore = listLexiconMatch[nIndex][4]

				# filter out anything with less than the top confidence score
				nIndex = 0
				while nIndex < len(listLexiconMatch) :
					if listLexiconMatch[nIndex][4] < nBestScore :
						del listLexiconMatch[nIndex]
					else :
						nIndex = nIndex + 1

			# add variable and any lexicon matches it might have (can be [] if none)
			listMappedVars.append( ( strVarName, strVarPhrase, nVarGramSize, listLexiconMatch ) )

	# all done
	return listMappedVars


def apply_semantic_mappings_to_extractions( mapped_extracted_vars = None, list_parsed_semantic_patterns = None, this_uri = None, stemmer = None, binding_strategy = 'best_one', namespace_unknown_vocab = 'unknown_vocab', dict_openie_config = None ) :
	"""
	apply a list of parsed semantic patterns to a set of mapped extraction variables (originating from a sent) to generate a set of resulting RDF productions in the form (subj pred obj).
	each extraction is checked against the mapping patterns. the extracted variables are bound to mapping pattern variables, and if all variables are successfully bound the associated production is generated.
	where multiple binding options exist, all the the top confidence value, either a single production is generated (best_one strategy) or all possibile productions are generated (best_all strategy).

	:param list mapped_extracted_vars: list of extraction variables mapped using sem_map_lib.map_extractions_to_lexicon()
	:param list list_parsed_semantic_patterns: list of parsed semantic mapping patterns from sem_map_lib.import_semantic_mapping_patterns()
	:param str this_uri: optional uri value for 'this' semantic pattern production entry (default is None). this allows productions to be generated that reference an implied subject uri. for example text for a physical object description where the physical object is not explicitly mentioned but implied.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param str binding_strategy: strategy for choosing variable bindings where multiple options exist = best_one|best_all. best_one will generate a production with the first occuring binding with the highest confidence value (i.e. a single production is generated). best_all will generate a production with all occuring bindings with the highest confidence value (i.e. many productions are generated).
	:param str namespace_unknown_vocab: namespace to use for production URIs for text that matches the semantic mapping pattern conditions, but for which there are no lexicon matches. a None value will disable use of such non-lexicon text in output productions.
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: set of RDF production triples = [ (subj pred obj), ... ]
	:rtype: list
	"""

	if not isinstance( mapped_extracted_vars, list ) :
		raise Exception( 'invalid mapped_extracted_vars' )
	if not isinstance( list_parsed_semantic_patterns, list ) :
		raise Exception( 'invalid list_parsed_semantic_patterns' )
	if not isinstance( this_uri, (str, type(None)) ) :
		raise Exception( 'invalid this_uri' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( binding_strategy, str ) :
		raise Exception( 'invalid binding_strategy' )
	if not isinstance( namespace_unknown_vocab, (str, type(None)) ) :
		raise Exception( 'invalid namespace_unknown_vocab' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if not binding_strategy in ['best_one','best_all'] :
		raise Exception( 'unknown binding strategy : ' + binding_strategy )

	# TODO THIS MIGHT BE A RELIC AS map_encoded_extraction_to_lexicon() does what we need really
	#      creating a mapping language might be better done another way (e.g. feature grammar)

	# TODO REVISIT CODE AND USE map_encoded_extraction_to_lexicon output (no var type) 


	# mapped_extracted_vars = [ [ (var_type, var_name, var_phrase, var_gram_size, [lexicon_uri, schema_uri, matched_phrase, phrase_gram_size, confidence_score]), ... ]
	# list_parsed_semantic_patterns = (    [ ( var_type, var_name, schema_uri, phrase, skos_uri ), ... ],     [ ( subject, object, predicate ), ... ]    )
	# note: phrases in semantic mapping pattern are lower(), phrases from mapped extracted vars are also lower()
	listResult = []

	'''

	# make a copy of the patterns and replace any phrases (in phrase list condition) with
	# a list of stemed phrase tokens for quick matching later
	listPatternSet = copy.deepcopy( list_parsed_semantic_patterns )
	if stemmer != None :
		for nIndex1 in range(len(listPatternSet)) :
			for nIndex2 in range(len(listPatternSet[nIndex1][0])) :
				# convert to list so we can change it
				listComponents = list( listPatternSet[nIndex1][0][nIndex2] )
				listPhrase = listComponents[3]

				for nIndex3 in range(len(listPhrase)) :
					# tokenize, stem and make back into a phrase
					listTokens = listPhrase[nIndex3].split(' ')
					for nIndex4 in range(len(listPhrase)) :
						listTokens[nIndex4] = stemmer.stem( listTokens[nIndex4].lower() )
					listPhrase[nIndex3] = listTokens

				listComponents[3] = listPhrase
				# convert back to tuple
				listPatternSet[nIndex1][0][nIndex2] = tuple( listComponents )


	# loop on each extraction
	for listExtraction in mapped_extracted_vars :

		#dict_openie_config['logger'].info( 'T1 = ' + repr(listExtraction) )

		# loop on all the semantic mapping patterns
		for listPattern in listPatternSet :

			listComponents = listPattern[0]
			listProductions = listPattern[1]
			listBindings = []

			# skip extraction if # vars in extraction < # vars in pattern
			if len(listExtraction) < len(listComponents) :
				continue

			#dict_openie_config['logger'].info( 'T2 = ' + repr(listComponents) )

			nIndexVar = 0
			for ( strVarType, strVarName, listSchema, listPhrase, listSKOS ) in listComponents :

				listBindingOptions = []
				strLiteralBinding = None
				nBestConfidence = 0.0

				# loop on each variable in each extraction
				# note: semantic mapping pattern variable names (e.g. arg1) != extracted variable names (e.g. arg1) so we just match on type
				listMatchedVar = listExtraction[nIndexVar]

				# TODO handle case where an argument is split {arg1} blah {arg1}
				#      need to revisot the asumption that num of variables = num of pattern components in this case (i.e. cannot share an index, need to look for arg1 numeric)

				strVarTypeEx = listMatchedVar[0]
				strVarNameEx = listMatchedVar[1]

				# get extraction phrase tokens (for later matching). these would have been stemmed already by map_extractions_to_lexicon()
				listVarPhraseEx = listMatchedVar[2].split(' ')

				# check variable type is correct
				if strVarType == strVarTypeEx :

					#dict_openie_config['logger'].info( 'T3 = ' + repr(strVarType) )

					# get the highest confidence lexicon uri mapping that also matches the (schema,phrase,skos) mapping conditions
					for listMatchInstance in listMatchedVar[4] :
						strLexiconURIEx = listMatchInstance[0]
						strSchemaURIEx = listMatchInstance[1]
						strPhraseEx = listMatchInstance[2]
						nConfidenceEx = listMatchInstance[4]

						listPhraseEx = strPhraseEx.split(' ')

						# skos condition only allows a specific uri for a lexicon match
						if len(listSKOS) > 0 :
							if not strLexiconURIEx in listSKOS :
								continue

						# schema condition only allows a specific skos:schema for a lexicon match
						if len(listSchema) > 0 :
							if not strSchemaURIEx in listSchema :
								continue

						# make sure the lexicon phrase is subsumed by one of the phrases in the variable condition allowed phrase list
						# e.g. lexicon='carved' OK when phrase='carved from'
						if len(listPhrase) > 0 :
							bFound = False
							for listTokenCondition in listPhrase :
								for nIndexToken in range(len(listTokenCondition)) :
									if listTokenCondition[ nIndexToken : nIndexToken + len(listPhraseEx) ] == listPhraseEx :
										bFound = True
							if bFound == False :
								continue

						#dict_openie_config['logger'].info('T5 = ' + repr(strPhraseEx) + ' > ' + repr(strLexiconURIEx) )

						# remember match
						listBindingOptions.append( ( nConfidenceEx, strLexiconURIEx ) )
						if nConfidenceEx > nBestConfidence :
							nBestConfidence = nConfidenceEx

					# if there are no constraints at all (schema, skos, phrase) then apply a literal match as anything will do
					bAddLiteral = False
					if (len(listSchema) == 0) and (len(listPhrase) == 0) and (len(listSKOS) == 0) :
						bAddLiteral = True

					# if variable contains one of the allowed set of phrases then provide a string literal binding in addition to any lexicon binding we might have
					# e.g. variable='roughly carved from' OK when phrase='carved from'
					if len(listPhrase) > 0 :
						for listTokenCondition in listPhrase :
							for nIndexToken in range(len(listVarPhraseEx)) :
								if listVarPhraseEx[ nIndexToken : nIndexToken + len(listTokenCondition) ] == listTokenCondition :
									bAddLiteral = True
					
					# add string literal value as a binding
					if bAddLiteral == True :
						strLiteralBinding = '"' + listMatchedVar[2] + '"^^xsd:string'

				#dict_openie_config['logger'].info('T6 = ' + repr(listBindingOptions) )

				# keep only the best confidence bindings
				# and replace the tuple (conf,uri) with a string uri
				nIndex = 0
				while nIndex < len(listBindingOptions) :
					if listBindingOptions[nIndex][0] != nBestConfidence :
						del listBindingOptions[nIndex]
					else :
						listBindingOptions[nIndex] = listBindingOptions[nIndex][1]
						nIndex = nIndex + 1

				# if best_one delete all except the first one
				if binding_strategy == 'best_one' :
					if len(listBindingOptions) > 0 :
						listBindingOptions = listBindingOptions[:1]

				# add literal as a binding
				if strLiteralBinding != None :
					listBindingOptions.append( strLiteralBinding )

				#dict_openie_config['logger'].info('T7 = ' + repr(listBindingOptions) )

				# does the variable have at least 1 binding option? if not abort and try the next semantic mapping pattern
				if len(listBindingOptions) == 0 :
					break

				# remember all binding options for this variable
				listBindings.append( listBindingOptions )
				nIndexVar = nIndexVar + 1

			#dict_openie_config['logger'].info('T8 = ' + repr(listBindings) )

			# if we have an incomplete set of bindings move on to the next semantic mapping pattern
			if len(listBindings) != len(listComponents) :
				continue

			#dict_openie_config['logger'].info('T9 = ' + repr(len(listBindings)) )

			# generate all possible productions using all possible binding combinations
			for (strSubj, strPred, strObj) in listProductions :

				listEntries = [ strSubj, strPred, strObj ]
				for nEntryIndex in range(len(listEntries)) :

					# subject production variants
					listEntryBindings = []
					if listEntries[nEntryIndex] == 'this' :
						listEntryBindings.append( this_uri )
					else :
						# is subject a variable name? if so add a value for each of its bindings
						bVarName = False
						for nIndexVar in range(len(listBindings)) :
							strVarName = listComponents[nIndexVar][1]
							if listEntries[nEntryIndex] == strVarName :
								listEntryBindings = listBindings[nIndexVar]
								bVarName = True
								break

						# if not just treat is as a literal (e.g. <uri> or namespace:concept)
						if bVarName == False :
							listEntryBindings.append( listEntries[nEntryIndex] )

					# replace string value with the correct binding list
					listEntries[nEntryIndex] = listEntryBindings

				# make all possible triple variants based on the available bindings
				for nIndexSub in range(len(listEntries[0])) :

					if listEntries[0][nIndexSub].endswith('^^xsd:string') :
						if namespace_unknown_vocab != None :
							strTripleSubj = generate_uri_for_literals( literal_value = listEntries[0][nIndexSub][1:-13], namespace = namespace_unknown_vocab, dict_openie_config = dict_openie_config )
						else :
							continue
					else :
						strTripleSubj = listEntries[0][nIndexSub]

					for nIndexPred in range(len(listEntries[1])) :

						if listEntries[1][nIndexPred].endswith('^^xsd:string') :
							if namespace_unknown_vocab != None :
								strTriplePred = generate_uri_for_literals( literal_value = listEntries[1][nIndexPred][1:-13], namespace = namespace_unknown_vocab, dict_openie_config = dict_openie_config )
							else :
								continue
						else :
							strTriplePred = listEntries[1][nIndexPred]

						for nIndexObj in range(len(listEntries[2])) :

							# TODO if we have a lexicon object match already, do we allow the literal entry?

							if listEntries[2][nIndexObj].endswith('^^xsd:string') :
								if namespace_unknown_vocab != None :
									strTripleObj = generate_uri_for_literals( literal_value = listEntries[2][nIndexObj][1:-13], namespace = namespace_unknown_vocab, dict_openie_config = dict_openie_config )
								else :
									continue
							else :
								strTripleObj = listEntries[2][nIndexObj]

							tupleTriple = ( strTripleSubj, strTriplePred, strTripleObj )
							listResult.append( tupleTriple )

	'''

	# remove any duplicate productions
	listResult = list( set( listResult ) )

	# all done
	return listResult

def generate_uri_for_literals( literal_value = None, namespace = None, dict_openie_config = None ) :
	"""
	generate a safe RDF TTL entry for literal values which do not have any lexicon SKOS URI

	:param unicode literal_value: literal text
	:param unicode namespace: namespace for RDF node
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: TTL formatted RDF node
	:rtype: unicode
	"""

	if not isinstance( literal_value, str ) :
		raise Exception( 'invalid literal_value' )
	if not isinstance( namespace, str ) :
		raise Exception( 'invalid namespace' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	strText = namespace + ':' + urllib.parse.unquote_plus( literal_value )
	return strText

def import_semantic_mapping_patterns( filename_patterns = None, dict_openie_config = None ) :
	"""
	import from disk a set of serialized semantic mapping patterns (newline delimited).
	see sem_map_lib.parse_semantic_mapping_pattern() for pattern format.

	:param str filename_patterns: filename of semantic patterns to import
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: list of tuple_pattern's from sem_map_lib.parse_semantic_mapping_pattern()
	:rtype: list
	"""

	# TODO THIS MIGHT BE A RELIC AS map_encoded_extraction_to_lexicon() does what we need really

	if not isinstance( filename_patterns, str ) :
		raise Exception( 'invalid filename_patterns' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	if not os.path.exists( filename_patterns ) :
		raise Exception( 'file does not exist : ' + filename_patterns )

	listResult = []

	readHandle = codecs.open( filename_patterns, 'r', 'utf-8', errors = 'replace' )

	# read patterns one by one
	strLine = '#'
	while len(strLine) != 0 :

		# read line (will have newline at end, or 0 length if EOF)
		strLine = readHandle.readline()
		if len( strLine ) == 0 :
			break

		# remove newline at end
		strPattern = strLine.strip()

		# ignore empty lines
		if len(strPattern) == 0 :
			continue

		# ignore comments
		if strPattern.startswith('#') == True :
			continue

		# parse line
		tuplePattern = parse_semantic_mapping_pattern( str_pattern = strPattern, dict_openie_config = dict_openie_config )
		listResult.append( tuplePattern )

	# all done
	readHandle.close()
	return listResult

def parse_semantic_mapping_pattern( str_pattern = None, dict_openie_config = None ) :
	"""
	parse a serialized semantic mapping pattern into a structure suitable for efficient mapping on demand.
	phrase constraints must have spaces replaced with the '_' token to avoid parsing ambiguity.

	example patterns below ::

		{arg1:schema=<http://collection.britishmuseum.org/id/thesauri/object>|<http://collection.britishmuseum.org/id/thesauri/subject>} -> {this rso:PX_object_type arg1}
		{arg1:schema=<http://collection.britishmuseum.org/id/thesauri/object>} {rel1:phrase=carved|weaved|sculpted} {prep1:phrase=from} {arg2:schema=<http://collection.britishmuseum.org/id/thesauri/material>} -> {this crm:P45_consists_of arg2}
		{arg1:schema=<http://collection.britishmuseum.org/id/thesauri/object>} {rel1:skos=<http://collection.britishmuseum.org/id/thesauri/script/carved>} {prep1:phrase=from} {arg2:schema=<http://collection.britishmuseum.org/id/thesauri/material>} -> {this crm:P45_consists_of arg2}

	:param unicode str_pattern: serialized semantic mapping pattern
	:param dict dict_openie_config: config object returned from soton_corenlppy.re.openie_lib.get_openie_config()

	:return: tuple_pattern = ( list_conditions, tuple_production ). list_conditions = [ ( var_type, var_name, schema_uri[], phrase[], skos_uri[] ), ... ]. tuple_production == [ ( subject, object, predicate ), ... ].
	:rtype: tuple
	"""

	# TODO THIS MIGHT BE A RELIC AS map_encoded_extraction_to_lexicon() does what we need really

	if not isinstance( str_pattern, str ) :
		raise Exception( 'invalid str_pattern' )
	if not isinstance( dict_openie_config, dict ) :
		raise Exception( 'invalid dict_openie_config' )

	listConditions = []
	listProductions = []
	bFoundArrow = False

	listPattern = str_pattern.split(' ')
	for strEntry in listPattern :

		# check for arrow
		if strEntry == '->' :
			bFoundArrow = True
			continue

		# parse left side of mapping pattern (mapping conditions)
		if bFoundArrow == False :

			matchObj = regexSemanticMappingCondition.match( strEntry )
			if matchObj != None :

				strType = None
				nIndexVar = None
				listSchema = []
				listPhrase = []
				listSkos = []
				if 'TYPE' in matchObj.groupdict() :
					strType = matchObj.groupdict()['TYPE']

				if 'INDEX' in matchObj.groupdict() :
					strIndex = matchObj.groupdict()['INDEX']
					if strIndex != None :
						nIndexVar = int( strIndex )

				if 'SCHEMA' in matchObj.groupdict() :
					strSchemaList = matchObj.groupdict()['SCHEMA']
					if strSchemaList != None :
						listSchema = strSchemaList.split('|')
						for nIndex in range(len(listSchema)) :
							if (listSchema[nIndex][0] == '<') and (listSchema[nIndex][-1]=='>') :
								listSchema[nIndex] = listSchema[nIndex][1:-1]
							else :
								raise Exception( 'parse error : schema uri not bounded by <> : ' + strEntry )

				if 'PHRASE' in matchObj.groupdict() :
					strPhraseList = matchObj.groupdict()['PHRASE']
					if strPhraseList != None :
						strPhraseList = strPhraseList.lower().replace('_',' ')
						listPhrase = strPhraseList.split('|')

				if 'SKOS' in matchObj.groupdict() :
					strSkoslist = matchObj.groupdict()['SKOS']
					if strSkoslist != None :
						listSkos = strSkoslist.split('|')
						for nIndex in range(len(listSkos)) :
							if (listSkos[nIndex][0] == '<') and (listSkos[nIndex][-1]=='>') :
								listSkos[nIndex] = listSkos[nIndex][1:-1]
							else :
								raise Exception( 'parse error : skos uri not bounded by <> : ' + strEntry )

				if (nIndexVar != None) and (strType != None) :
					tupleEntry = ( strType, strType + str(nIndexVar), listSchema, listPhrase, listSkos )
				else :
					raise Exception( 'parse error : null type or index on variable : ' + strEntry )

			else :
				raise Exception( 'parse error : invalid condition : ' + repr(nIndex) )

			listConditions.append( tupleEntry )

		# parse right side of mapping pattern (triple production)
		else :

			matchObj = regexSemanticMappingProduction.match( strEntry )
			if matchObj != None :

				strSubject = None
				strPredicate = None
				strObject = None

				if 'SUBJECT' in matchObj.groupdict() :
					strSubject = matchObj.groupdict()['SUBJECT']

				if 'PREDICATE' in matchObj.groupdict() :
					strPredicate = matchObj.groupdict()['PREDICATE']

				if 'OBJECT' in matchObj.groupdict() :
					strObject = matchObj.groupdict()['OBJECT']

				tupleEntry = ( strSubject, strPredicate, strObject )

			else :
				raise Exception( 'parse error : invalid production : ' + repr(strEntry) )

			listProductions.append( tupleEntry )
	
	return ( listConditions, listProductions )
