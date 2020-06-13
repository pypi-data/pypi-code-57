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

import array,sys,codecs,os,re,copy,math,json,ast,warnings,urllib.request,urllib.parse,urllib.error
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim, nltk.corpus, soton_corenlppy, nltk.stem

def get_lexicon_config( **kwargs ) :
	"""
	return a lexicon config object.

	| note: a config object approach is used, as opposed to a global variable, to allow lexicon_lib functions to work in a multi-threaded environment

	:return: configuration settings to be used by all lexicon_lib functions
	:rtype: dict
	"""

	dictArgs = copy.copy( kwargs )

	# setup common values
	dictLexiconConfig = soton_corenlppy.common_parse_lib.get_common_config( **dictArgs )

	# all done
	return dictLexiconConfig


def import_skos_lexicon( filename_lemma = None, filename_hypernym = None, filename_related = None, serialized_format = 'json', lower_case = True, stemmer = None, apply_wordnet_morphy = False, allowed_schema_list = None, dict_lexicon_config = None ) :
	"""
	import from file a serialized result of a SPARQL query over a SKOS vocabulary. files can be serialized in JSON or CSV tab delimited format. the result is an in-memory index for lexicon terms.

	| filename_lemma should report SPARQL query variables ?skos_concept ?scheme ?label
	| filename_hypernym should report SPARQL query variables ?skos_concept ?hypernym
	| filename_related should report SPARQL query variables ?skos_concept ?related

	example queries for file_lemma ::

		SELECT DISTINCT ?skos_concept ?scheme ?label
		WHERE {
			?skos_concept rdf:type skos:Concept .
			OPTIONAL {
				?skos_concept skos:inScheme ?scheme
			}
			{ ?skos_concept skos:prefLabel ?label } UNION { ?skos_concept skos:altLabel ?label }
		}
		ORDER BY ?skos_concept ?scheme ?label

	example queries for file_hypernym ::

		SELECT DISTINCT ?skos_concept ?hypernym
		WHERE {
			?skos_concept rdf:type skos:Concept .
			?skos_concept skos:broader ?hypernym
		}
		ORDER BY ?skos_concept ?hypernym

	example queries for file_related ::

		SELECT DISTINCT ?skos_concept ?related
		WHERE {
			?skos_concept rdf:type skos:Concept .
			?skos_concept skos:related ?related
		}
		ORDER BY ?skos_concept ?related

	:param str filename_lemma: file for lemma SPARQL query result
	:param str filename_hypernym: file for hypernym SPARQL query result (can be None)
	:param str filename_related: file for related SPARQL query result (can be None)
	:param str serialized_format: format of files = json|csv
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to find try and base word of a phrase to use in lexicon
	:param list allowed_schema_list: filter list of allowed schema values for imported phrases (default None which allows any schema URI)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: ( dict_uri, dict_phrase ), where dict_uri = { uri : [ scheme_uri, set_hypernym_uri, set_related_uri ] } and dict_phrase = { phrase : set_uri }. several phrases can share a phrase_uri
	:rtype: tuple
	"""

	# check args
	if not isinstance( filename_lemma, str ) :
		raise Exception( 'invalid filename_lemma' )
	if not isinstance( filename_hypernym, (str,type(None)) ) :
		raise Exception( 'invalid filename_hypernym' )
	if not isinstance( filename_related, (str,type(None)) ) :
		raise Exception( 'invalid filename_related' )
	if not isinstance( serialized_format, str ) :
		raise Exception( 'invalid serialized_format' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( allowed_schema_list, (list, type(None)) ) :
		raise Exception( 'invalid allowed_schema_list' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	dictURI = {}
	dictPhrase = {}

	# load and parse lemma file
	dictResult = load_sparql_query_results(
		filename_results = filename_lemma,
		serialized_format = serialized_format,
		list_variable_names = ['skos_concept','scheme','label'],
		dict_lexicon_config = dict_lexicon_config )

	for strSkosURI in dictResult :
		for listValues in dictResult[strSkosURI] :
			strSchemeURI = listValues[0]
			strPhrase = listValues[1]

			if lower_case == True :
				strPhrase = strPhrase.lower()

			if apply_wordnet_morphy == True :
				strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strPhrase, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
				if strBase != None :
					strPhrase = strBase

			if stemmer != None :
				strPhrase = stemmer.stem( strPhrase )
			
			if (allowed_schema_list == None) or (strSchemeURI in allowed_schema_list) :

				if not strPhrase in dictPhrase :
					dictPhrase[strPhrase] = set([])
				dictPhrase[strPhrase].add( strSkosURI )

				if not strSkosURI in dictURI :
					dictURI[strSkosURI] = [ strSchemeURI, set([]), set([]) ]

	# load and parse hypernymn file
	if filename_hypernym != None :
		dictResult = load_sparql_query_results(
			filename_results = filename_hypernym,
			serialized_format = serialized_format,
			list_variable_names = ['skos_concept','hypernym'],
			dict_lexicon_config = dict_lexicon_config )

		for strSkosURI in dictResult :
			for listValues in dictResult[strSkosURI] :
				strHyperURI = listValues[0]

				if not strSkosURI in dictURI :
					dictURI[strSkosURI] = [ None, set([]), set([]) ]
				dictURI[strSkosURI][1].add( strHyperURI )

	# load and parse related file
	if filename_related != None :
		dictResult = load_sparql_query_results(
			filename_results = filename_related,
			serialized_format = serialized_format,
			list_variable_names = ['skos_concept','related'],
			dict_lexicon_config = dict_lexicon_config )

		for strSkosURI in dictResult :
			for listValues in dictResult[strSkosURI] :
				strRelatedURI = listValues[0]

				if not strSkosURI in dictURI :
					dictURI[strSkosURI] = [ None, set([]), set([]) ]
				dictURI[strSkosURI][2].add( strRelatedURI )

	# return the final dict objects
	return ( dictURI, dictPhrase )

def import_plain_lexicon( filename_lemma = None, list_column_names = ['col1','schema','col3', 'col4', 'phrase_list'], phrase_delimiter = '|', lower_case = True, stemmer = None, apply_wordnet_morphy = False, allowed_schema_list = None, dict_lexicon_config = None ) :

	"""
	import from tab delimited CSV file a lexicon. lines beginning with # are ignored
	columns must have a 'schema' and 'phrase_list' entry. phrases are delimited by the phrase_delimiter e.g. 'phase one | phrase two'
	optionally there can also be a 'hypernym' entry, which is a space list of phrase URIs
	phrase URI's are constructed from the schema and phrase tokens applied to ASCII urllib.quote_plus(). e.g. schema 'http://example.org/id/part' + phrase 'left shoulder' == 'http://example.org/id/part#left+shoulder'

	:param str filename_lemma: tab delimited file with schema URI and phrases
	:param list list_column_names: names of the columns. columns other than 'schema', 'phrase_list' and 'hypernym' are ignored
	:param str phrase_delimiter: character delimiting phrases in phrase_list
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to find try and base word of a phrase to use in lexicon
	:param list allowed_schema_list: filter list of allowed schema values for imported phrases (default None which allows any schema URI)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: ( dict_uri, dict_phrase ), where dict_uri = { uri : [ scheme_uri, set_hypernym_uri, set_related_uri ] } and dict_phrase = { phrase : set_uri }. several phrases can share a phrase_uri
	:rtype: tuple
	"""

	# check args
	if not isinstance( filename_lemma, str ) :
		raise Exception( 'invalid filename_lemma' )
	if not isinstance( phrase_delimiter, str ) :
		raise Exception( 'invalid phrase_delimiter' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI,type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( allowed_schema_list, (list, type(None)) ) :
		raise Exception( 'invalid allowed_schema_list' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if not 'schema' in list_column_names :
		raise Exception( 'schema missing from list_column_names' )
	nSchemaIndex = list_column_names.index( 'schema' )

	if not 'phrase_list' in list_column_names :
		raise Exception( 'phrase_list missing from list_column_names' )
	nPhraseIndex = list_column_names.index( 'phrase_list' )

	if not 'hypernym' in list_column_names :
		nHypoIndex = None
	else :
		nHypoIndex = list_column_names.index( 'hypernym' )

	dictURI = {}
	dictPhrase = {}

	# handle possible synonyms that might appear
	# 'right' -> [ right_thing, right_knowledge, right_location ]
	# right_thing -> schema_thing, []
	# right_knowledge -> schema_knowledge, [ schema_thing ]
	# right_location -> schema_location, [ schema_thing ]

	# tab delimited CSV for lemma
	readHandle = codecs.open( filename_lemma, 'rb', 'utf-8', errors = 'replace' )

	# we expect headers so ignore any line that starts with a #
	# note: do not use python csv classes as they do not work well with UTF-8 in the upper bound (e.g. japanese characters)
	strLine = '#'
	while len(strLine) > 0 :
		strLine = readHandle.readline()

		# EOF
		if len(strLine) == 0 :
			break

		# header
		if strLine.startswith('#') :
			continue

		# remove newline at end and ignore empty lines (e.g. at end of file)
		strLine = strLine.strip( '\r\n ' )
		if len(strLine) > 0 :

			listVarValues = strLine.split('\t')
			if len( listVarValues ) != len( list_column_names ) :
				raise Exception( 'variable list size ' + str( len( listVarValues ) )  + ' not expected (lemma) : ' + repr(strLine) )

			# strip <> from any URI's
			for nIndex in range(len(listVarValues)) :
				if listVarValues[nIndex].startswith('<') and listVarValues[nIndex].endswith('>') :
					listVarValues[nIndex] = listVarValues[nIndex][1:-1]

			strSchemaURI = listVarValues[nSchemaIndex]

			strPhraseList = listVarValues[nPhraseIndex]
			listPhrase = strPhraseList.split( phrase_delimiter )

			if nHypoIndex != None :
				strHypoList = listVarValues[nHypoIndex]
				listHyper = strHypoList.split( ' ' )
			else :
				listHyper = []

			# compile the hyper uri set for this phrase group
			setHyper = set([])
			for nIndexPhrase in range(len(listHyper)) :
				strPhraseURI = listHyper[nIndexPhrase].strip()
				setHyper.add( strPhraseURI )

			# create an entry for each phrase
			for nIndexPhrase in range(len(listPhrase)) :
				strPhrase = listPhrase[nIndexPhrase].strip()

				if lower_case == True :
					strPhrase = strPhrase.lower()

				if stemmer != None :
					strPhrase = stemmer.stem( strPhrase )

				if apply_wordnet_morphy == True :
					strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strPhrase, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
					if strBase != None :
						strPhrase = strBase

				strPhraseURI = strSchemaURI + '#' + urllib.parse.quote_plus( strPhrase.encode('utf-8','replace') )

				if not strPhrase in dictPhrase :
					dictPhrase[strPhrase] = set([])
				dictPhrase[strPhrase].add( strPhraseURI )

				dictURI[strPhraseURI] = [ strSchemaURI, setHyper, set([]) ]
		else :
			strLine = '#'

	readHandle.close()

	# return the final dict objects
	return ( dictURI, dictPhrase )

def import_NELL_lexicon( filename_nell = None, lower_case = False, stemmer = None, apply_wordnet_morphy = False, allowed_schema_list = None, dict_lexicon_config = None ) :

	"""
	import from tab delimited NELL KBP CSV file a lexicon.

	:param str filename_nell: tab delimited file from NELL
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to find try and base word of a phrase to use in lexicon
	:param list allowed_schema_list: filter list of allowed schema values for imported phrases (default None which allows any schema URI)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: ( dict_uri, dict_phrase ), where dict_uri = { uri : [ scheme_uri, set_hypernym_uri, set_related_uri ] } and dict_phrase = { phrase : set_uri }. several phrases can share a phrase_uri
	:rtype: tuple
	"""

	# check args
	if not isinstance( filename_nell, str ) :
		raise Exception( 'invalid filename_nell' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI,type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( allowed_schema_list, (list, type(None)) ) :
		raise Exception( 'invalid allowed_schema_list' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	dictURI = {}
	dictPhrase = {}

	# NELL KBP format (2013 version is 800 Mbytes in size)
	# <phrase> [<tab> <nell_type_str> <confidence_float>] x N
	# <phrase> = case sensitive phrase (multiple versions appear if lower case versions are allowed)
	# <nell_type_str> = food | agriculturalproduct | city | drug ...
	# <confidence_float> = 0.0 .. 1.0
	# there are no headers

	# tab delimited CSV for lemma
	readHandle = codecs.open( filename_nell, 'rb', 'utf-8', errors = 'replace' )

	# we do not expect headers but ignore any lines starting with a # anyway
	# note: do not use python csv classes as they do not work well with UTF-8 in the upper bound (e.g. japanese characters)
	strLine = '#'
	while len(strLine) > 0 :
		strLine = readHandle.readline()

		# EOF
		if len(strLine) == 0 :
			break

		# header
		if strLine.startswith('#') :
			continue

		# remove newline at end and ignore empty lines (e.g. at end of file)
		strLine = strLine.strip( '\r\n ' )
		if len(strLine) > 0 :

			listVarValues = strLine.split('\t')

			strPhrase = listVarValues[0]

			setHyper = set([])
			nIndex = 1
			while nIndex < len(listVarValues) :
				strHyper = listVarValues[nIndex]
				strHyperURI = 'http://nell#' + urllib.parse.quote_plus( strHyper.encode('utf-8','replace') )
				setHyper.add( strHyperURI )
				nIndex = nIndex + 2

			if lower_case == True :
				strPhrase = strPhrase.lower()

			if stemmer != None :
				strPhrase = stemmer.stem( strPhrase )

			if apply_wordnet_morphy == True :
				strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strPhrase, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
				if strBase != None :
					strPhrase = strBase

			strPhraseURI = 'http://nell#' + urllib.parse.quote_plus( strPhrase.encode('utf-8','replace') )

			if not strPhrase in dictPhrase :
				dictPhrase[strPhrase] = set([])
			dictPhrase[strPhrase].add( strPhraseURI )

			dictURI[strPhraseURI] = [  'http://nell', setHyper, set([]) ]
		else :
			strLine = '#'

	readHandle.close()

	# return the final dict objects
	return ( dictURI, dictPhrase )

def append_to_lexicon( dict_uri = {}, dict_phrase = {}, phrase_list = [], schema_uri = None, hyponymn_uri_list = [], lower_case = True, stemmer = None, apply_wordnet_morphy = False, dict_lexicon_config = None ) :

	"""
	append an new entry to an existing lexicon. this method will add information to dict_uri and dict_phrase.

	:param dict dict_uri: URI dict structure
	:param dict dict_phrase: phrase dict structure
	:param list phrase_list: list of new phrases to add
	:param unicode schema_uri: schema URI for this phrase list
	:param list hyponymn_uri_list: list of hyponymn phrase URI's for this phrase list
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to find try and base word of a phrase to use in lexicon
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 
	"""

	# check args
	if not isinstance( dict_uri, dict ) :
		raise Exception( 'invalid dict_uri' )
	if not isinstance( dict_phrase, dict ) :
		raise Exception( 'invalid dict_phrase' )
	if not isinstance( phrase_list, list ) :
		raise Exception( 'invalid phrase_list' )
	if not isinstance( schema_uri, str ) :
		raise Exception( 'invalid schema_uri' )
	if not isinstance( hyponymn_uri_list, list ) :
		raise Exception( 'invalid hyponymn_uri_list' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI,type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# compile the hyper uri set for this phrase group
	setHyper = set([])
	for nIndexPhrase in range(len(hyponymn_uri_list)) :
		strPhraseURI = hyponymn_uri_list[nIndexPhrase].strip()
		setHyper.add( strPhraseURI )

	# create an entry for each phrase
	for nIndexPhrase in range(len(phrase_list)) :
		strPhrase = phrase_list[nIndexPhrase].strip()

		if lower_case == True :
			strPhrase = strPhrase.lower()

		if stemmer != None :
			strPhrase = stemmer.stem( strPhrase )

		if apply_wordnet_morphy == True :
			strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strPhrase, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
			if strBase != None :
				strPhrase = strBase

		strPhraseURI = schema_uri + '#' + urllib.parse.quote_plus( strPhrase.encode('utf-8','replace') )

		if not strPhrase in dict_phrase :
			dict_phrase[strPhrase] = set([])
		dict_phrase[strPhrase].add( strPhraseURI )

		dict_uri[strPhraseURI] = [ schema_uri, setHyper, set([]) ]


def export_lexicon( filename_lexicon = None, dict_uri = None, dict_phrase = None, dict_lexicon_config = None ) :
	"""
	export lexicon to file

	:param str filename_lexicon: file to serialize lexicon to
	:param dict dict_uri: URI dict structure
	:param dict dict_phrase: phrase dict structure
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 
	"""

	# check args
	if not isinstance( filename_lexicon, str ) :
		raise Exception( 'invalid filename_lexicon' )
	if not isinstance( dict_uri, dict ) :
		raise Exception( 'invalid dict_uri' )
	if not isinstance( dict_phrase, dict ) :
		raise Exception( 'invalid dict_phrase' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	writeHandle = codecs.open( filename_lexicon, 'w', 'utf-8', errors = 'replace' )

	# serialize phrases
	# note save sets as lists as ast.literal_eval() cannot parse sets
	writeHandle.write( 'serialized lexicon\n' )
	writeHandle.write( '#phrases ' + str(len( dict_phrase )) + '\n' )
	for strPhrase in dict_phrase :
		# use repr() to safely escape out any newlines tabs unicode chars etc
		writeHandle.write( repr( strPhrase ) + '\t' )
		writeHandle.write( repr( list( dict_phrase[strPhrase] ) ) + '\n' )

	# serialize URI
	writeHandle.write( '#uris ' + str(len( dict_uri )) + '\n' )
	for strURI in dict_uri :
		writeHandle.write( strURI + '\t' )
		writeHandle.write( repr( dict_uri[strURI][0] ) + '\t' )
		writeHandle.write( repr( list( dict_uri[strURI][1] ) ) + '\t' )
		writeHandle.write( repr( list( dict_uri[strURI][2] ) ) + '\n' )

	# all done
	writeHandle.close()

def import_lexicon( filename_lexicon = None, dict_lexicon_config = None ) :
	"""
	import lexicon to file from a file serialized using lexicon_lib.export_lexicon()

	:param str filename_lexicon: file to serialize lexicon from
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: ( dict_uri, dict_phrase ), where dict_uri = { uri : [ scheme_uri, set_hypernym_uri, set_related_uri ] } and dict_phrase = { phrase : set_uri }. several phrases can share a phrase_uri
	:rtype: tuple
	"""

	# check args
	if not isinstance( filename_lexicon, str ) :
		raise Exception( 'invalid filename_lexicon' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if not os.path.exists( filename_lexicon ) :
		raise Exception( 'file does not exist : ' + filename_lexicon )

	dictURI = {}
	dictPhrase = {}

	readHandle = codecs.open( filename_lexicon, 'r', 'utf-8', errors = 'replace' )

	# read header
	strLine = readHandle.readline().strip()
	if strLine != 'serialized lexicon' :
		readHandle.close()
		raise Exception( 'filename ' + filename_lexicon + ' not a lexicon file (missing header)' )

	# read number of phrases
	strLine = readHandle.readline().strip()
	if strLine.startswith( '#phrases ' ) :
		nPhrases = int( strLine[9:] )
	else :
		readHandle.close()
		raise Exception( 'filename ' + filename_lexicon + ' not a lexicon file (missing #phrases)' )

	# read all phrases
	# note: convert list to set as ast.literal_eval() cannot handle sets so we serialize as lists
	nCount = 0
	while nCount < nPhrases :
		strLine = readHandle.readline().strip()
		nCount = nCount + 1

		listComponents = strLine.split('\t')
		if len(listComponents) != 2 :
			readHandle.close()
			raise Exception( 'phrase list parse error : ' + strLine)

		strPhrase = ast.literal_eval( listComponents[0] )
		listURI = ast.literal_eval( listComponents[1] )
		if not isinstance( listURI, list ) :
			readHandle.close()
			raise Exception( 'phrase URI set parse error : ' + listComponents[1] )

		dictPhrase[strPhrase] = set( listURI )

	# read number of uris
	strLine = readHandle.readline().strip()
	if strLine.startswith( '#uris ' ) :
		nURIs = int( strLine[6:] )
	else :
		readHandle.close()
		raise Exception( 'filename ' + filename_lexicon + ' not a lexicon file (missing #uris)' )

	# read all uris
	# note: convert list to set as ast.literal_eval() cannot handle sets so we serialize as lists
	nCount = 0
	while nCount < nURIs :
		strLine = readHandle.readline().strip()
		nCount = nCount + 1

		listComponents = strLine.split('\t')
		if len(listComponents) != 4 :
			readHandle.close()
			raise Exception( 'uris list parse error : ' + strLine )

		strURI = listComponents[0]
		strSchemeURI = ast.literal_eval( listComponents[1] )

		listHyper = ast.literal_eval( listComponents[2] )
		if not isinstance( listHyper, list ) :
			readHandle.close()
			raise Exception( 'uris hyper set parse error : ' + listComponents[2] )

		listRelated = ast.literal_eval( listComponents[3] )
		if not isinstance( listRelated, list ) :
			readHandle.close()
			raise Exception( 'uris related set parse error : ' + listComponents[3] )

		dictURI[strURI] = ( strSchemeURI, set( listHyper ), set( listRelated ) )

	# all done
	readHandle.close()
	return ( dictURI, dictPhrase )

def load_sparql_query_results( filename_results = None, serialized_format = 'json', list_variable_names = [], dict_lexicon_config = None ) :
	"""
	load and parse a sparql query result file. internal function called by lexicon_lib.import_skos_lexicon()

	:param str filename_results: filename to load
	:param str serialized_format: format of files = json|csv
	:param list list_variable_names: sparql variable names to expect
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: dict of results indexed by the first variable value. a list is kepts as each 1st variable value might occur more than once. { var1 : [ [var2,var3,...], [var2,var3,...], ... ] }
	:rtype: dict
	"""

	if not isinstance( filename_results, str ) :
		raise Exception( 'invalid filename_results' )
	if not isinstance( serialized_format, str ) :
		raise Exception( 'invalid serialized_format' )
	if not isinstance( list_variable_names, list ) :
		raise Exception( 'invalid list_variable_names' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# check format and file exist
	if not serialized_format in ['json','csv'] :
		raise Exception( 'unknown serialization format : ' + serialized_format )
	if not os.path.exists( filename_results ) :
		raise Exception( 'file does not exist : ' + filename_results )

	# must have at least skos_uri and a second variable (e.g. lemma)
	if len(list_variable_names) < 2 :
		raise Exception( 'list_variable_names < 2' )

	dictResult = {}

	# load and parse lemma file
	if serialized_format == 'json' :

		# read input data into memory
		readHandle = codecs.open( filename_results, 'r', 'utf-8', errors = 'replace' )
		listLines = readHandle.readlines()
		readHandle.close()

		strJSON = '\n'.join( listLines )
		dictJSON = json.loads( strJSON, encoding = 'utf-8' )

		if not 'results' in dictJSON :
			raise Exception( 'input JSON does not have a SPARQL results key' )
		if not 'bindings' in dictJSON['results'] :
			raise Exception( 'input JSON does not have a SPARQL bindings key' )
		
		# extract sents and URIs into simple lists
		for dictBinding in dictJSON['results']['bindings'] :

			listVarValues = []
			for strVariable in list_variable_names :

				if not strVariable in dictBinding :
					raise Exception( 'variable ' + strVariable + ' not found in JSON result binding' )

				strValue = dictBinding[strVariable]['value']
				listVarValues.append( strValue )

			if not listVarValues[0] in dictResult :
				dictResult[ listVarValues[0] ] = []
			dictResult[ listVarValues[0] ].append( listVarValues[ 1: ] )

	elif serialized_format == 'csv' :

		# tab delimited CSV
		readHandle = codecs.open( filename_results, 'rb', 'utf-8', errors = 'replace' )

		# we expect a header with the variable names so ignore this
		# note: do not use python csv classes as they do not work well with UTF-8 in the upper bound (e.g. japanese characters)
		bHeader = True
		strLine = '#'
		while len(strLine) > 0 :
			strLine = readHandle.readline()
			if len(strLine) == 0 :
				break

			# remove newline at end and ignore empty lines (e.g. at end of file)
			strLine = strLine.strip()
			if len(strLine) > 0 :

				listVarValues = strLine.split('\t')
				if len( listVarValues ) != len( list_variable_names ) :
					raise Exception( 'variable list size ' + str( len( listVarValues ) )  + ' not expected' )

				# strip <> from any URI's
				for nIndex in range(len(listVarValues)) :
					if listVarValues[nIndex].startswith('<') and listVarValues[nIndex].endswith('>') :
						listVarValues[nIndex] = listVarValues[nIndex][1:-1]

				if bHeader == False :
					if not listVarValues[0] in dictResult :
						dictResult[ listVarValues[0] ] = [ listVarValues[ 1: ] ]
					else :
						dictResult[ listVarValues[0] ].append( listVarValues[ 1: ] )
				bHeader = False


		readHandle.close()

	# all done
	return dictResult

def calc_corpus_dictionary( list_token_sets, stoplist = [], stemmer = None, dict_lexicon_config = None ) :
	"""
	calculate a corpus dictionary and bag of words representation for corpus

	:param list list_token_sets: list of tokenized sents in corpus, each sent represented as a list of tokens
	:param list stoplist: list of stopwords applied to sent tokens to remove them
	:param nltk.stemmer stemmer: stemmer to use for tokens (or None)
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: (gensim.corpora.dictionary.Dictionary(), list_bag_of_words)
	:rtype: tuple
	"""

	if not isinstance( list_token_sets, list ) :
		raise Exception( 'invalid list_token_sets' )
	if not isinstance( stoplist, list ) :
		raise Exception( 'invalid stoplist' )
	if (stemmer != None) and (not isinstance( stemmer, nltk.stem.api.StemmerI )) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# make a copy and strip all stopwords from sents 
	listTokenSetFiltered = copy.deepcopy( list_token_sets )
	for nIndex1 in range(len(listTokenSetFiltered)) :
		for nIndex2 in range(len(listTokenSetFiltered[nIndex1])) :
			if listTokenSetFiltered[nIndex1][nIndex2] in stoplist :
				listTokenSetFiltered[nIndex1][nIndex2] = ''
			else :
				if stemmer != None :
					listTokenSetFiltered[nIndex1][nIndex2] = stemmer.stem( listTokenSetFiltered[nIndex1][nIndex2] )

		while listTokenSetFiltered[nIndex1].count('') > 0 :
			listTokenSetFiltered[nIndex1].remove('')

	# build the corpus gensim dictionary
	dictGensim = gensim.corpora.dictionary.Dictionary()
	dictGensim.add_documents( list_token_sets )

	# make the bag of words representation
	listBagOfWords = [ dictGensim.doc2bow( strToken ) for strToken in list_token_sets ]

	# return both
	return (dictGensim, listBagOfWords)


def phrase_lookup( phrase_tokens = None, head_token = None, lex_phrase_index = None, lex_uri_index = None, max_gram = 5, stemmer = None, apply_wordnet_morphy = False, hyphen_variant = False, dict_lexicon_config = None ) :
	"""
	perform an n-gram lookup of phrases, optionally based around a head token.
	return the lexicon phrase matches with a confidence score.
	the confidence score is based on the percentage of tokens in an extracted phrase that match the lexicon phrase.

	:param list phrase_tokens: tokenized phrase to lookup in lexicon
	:param unicode head_token: head token in phrase which must be in any ngram lookup. the default None allows all possible ngarms to be looked up.
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param int max_gram: maximum phrase gram size to check for matches in lexicon. larger gram sizes means more lexicon checks, which is slower.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to the last phrase token
	:param bool hyphen_variant: if True lookup phrase as it is, and a version with hypens replaced by space characters.
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: lexicon matches to phrase = [ ( lexicon_uri, schema_uri, matched_phrase, match_gram_size, confidence_score ) ]
	:rtype: list
	"""

	if not isinstance( phrase_tokens, list ) :
		raise Exception( 'invalid phrase_tokens' )
	if not isinstance( head_token, (str,type(None)) ) :
		raise Exception( 'invalid head_token' )
	if not isinstance( lex_uri_index, dict ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, dict ) :
		raise Exception( 'invalid lex_phrase_index' )
	if not isinstance( max_gram, int ) :
		raise Exception( 'invalid max_gram' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( hyphen_variant, bool ) :
		raise Exception( 'invalid hyphen_variant' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )

	# size check
	if len(phrase_tokens) == 0 :
		return []

	listChecklist = []
	listLexiconMatch = []

	# copy phrase tokens into a checklist to process (with and without hyphens)
	listPhraseTokens1 = copy.copy( phrase_tokens )
	strHead1 = copy.copy( head_token )
	listChecklist.append( [listPhraseTokens1,strHead1] )

	if hyphen_variant == True :

		listPhraseTokens2 = copy.copy( phrase_tokens )
		for nIndex in range(len(listPhraseTokens2)) :
			listPhraseTokens2[nIndex] = listPhraseTokens2[nIndex].replace('-',' ').replace('_',' ')
		strHead2 = copy.copy( head_token )
		if strHead2 != None :
			strHead2 = strHead2.replace('-',' ').replace('_',' ')
		if (strHead1 != strHead2) or (listPhraseTokens1 != listPhraseTokens2) :
			listChecklist.append( [listPhraseTokens2,strHead2] )

	# loop on variants and look them all up
	for (listPhraseTokens,strHead) in listChecklist :

		# morphy on last token in phrase
		if apply_wordnet_morphy == True :
			strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = listPhraseTokens[-1], morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
			if strBase != None :
				listPhraseTokens[-1] = strBase

			if strHead != None :
				strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strHead, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
				if strBase != None :
					strHead = strBase

		# stemming
		if stemmer != None :
			listPhraseTokens[-1] = stemmer.stem( listPhraseTokens[-1] )
			if strHead != None :
				strHead = stemmer.stem( strHead )

		# get all n-gram phrases for variable text that also contain the head token
		setPhrases = set([])
		for nGram in range( max_gram ) :
			for nIndex in range(len(listPhraseTokens)) :
				if nIndex + nGram < len(listPhraseTokens) :
					listPhrase = listPhraseTokens[ nIndex : nIndex + nGram + 1 ]

					if strHead != None :
						# make sure head token is in ngram expansion
						if strHead in listPhrase :
							setPhrases.add( ' '.join( listPhrase ) )
					else :
						# allow any ngram
						setPhrases.add( ' '.join( listPhrase ) )

		# lookup each phrase in the lexicon to see if there is a match
		for strPhrase in setPhrases :

			# lookup phrase in lexicon
			if strPhrase in lex_phrase_index :

				# gram size of phrase (higher gram phrase matches are more likely to be correct)
				if not ' ' in strPhrase :
					nGram = 1
				else :
					nGram = 1 + strPhrase.count(' ')
				
				# confidence = # tokens in extraction that appear in lexicon phrase
				nConfidence = ( 1.0 * nGram ) / len(listPhraseTokens)

				setURI = lex_phrase_index[strPhrase]
				for strURI in setURI :
					strSchemaURI = None
					if strURI in lex_uri_index :
						listDetails = lex_uri_index[ strURI ]
						strSchemaURI = listDetails[0]
					listLexiconMatch.append( ( strURI, strSchemaURI, strPhrase, nGram, nConfidence ) )

	# all done
	return listLexiconMatch

def sent_set_lookup( sent_token_set = None, lex_phrase_index = None, lex_uri_index = None, lower_case = True, max_gram = 5, stemmer = None, apply_wordnet_morphy = False, hyphen_variant = False, dict_lexicon_config = None ) :
	"""
	apply phrase_lookup() to all n-gram phrases in a set of sentences, returining True if any phrases match lexicon

	:param list sent_token_set: list of token sets from soton_corenlppy.common_parse_lib.unigram_tokenize_text_with_sent_breakdown()
	:param dict lex_phrase_index: lexicon phrase index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param dict lex_uri_index: lexicon uri index from soton_corenlppy.lexico.lexicon_lib.import_lexicon()
	:param int max_gram: maximum phrase gram size to check for matches in lexicon. larger gram sizes means more lexicon checks, which is slower.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on last phrase token (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to the last phrase token
	:param bool hyphen_variant: if True lookup phrase as it is, and a version with hypens replaced by space characters.
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: True if at least one phrase in the sentence set appears in the lexicon
	:rtype: bool
	"""

	if not isinstance( sent_token_set, list ) :
		raise Exception( 'invalid sent_token_set' )
	if not isinstance( lex_uri_index, dict ) :
		raise Exception( 'invalid lex_uri_index' )
	if not isinstance( lex_phrase_index, dict ) :
		raise Exception( 'invalid lex_phrase_index' )
	if not isinstance( max_gram, int ) :
		raise Exception( 'invalid max_gram' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( hyphen_variant, bool ) :
		raise Exception( 'invalid hyphen_variant' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )

	for listTokens in sent_token_set :

		# make a lower case version for lexicon lookup
		listTokensLower = []
		for strToken in listTokens :
			if lower_case == True :
				listTokensLower.append( strToken.lower() )
			else :
				listTokensLower.append( strToken )

		# compile a set of phrases from sent to check for lexicon matches. any match its OK
		listPhrasesForEachGram = soton_corenlppy.common_parse_lib.create_ngram_tokens(
			list_tokens = listTokensLower,
			max_gram = max_gram,
			sent_temination_tokens = None )

		# from each proposition variable extraction we compute all possible 1/2/3-gram phrases
		# and check them with the lexicon for a match
		for listPhraseSet in listPhrasesForEachGram :
			for tuplePhraseToCheck in listPhraseSet :
				listPhraseToCheck = list( tuplePhraseToCheck )

				# lexicon match using a head token of the last token in a phrase
				# e.g. [rotten,yellow,Bananas] -> head = Bananas
				#      morphy will be applied to last term, so Bananas = Banana
				#      head term must appear in any n-gram phrase to be matched
				#      so a lexicon with Banana in its index will match this target phrase
				listLexiconMatch = phrase_lookup(
					phrase_tokens = listPhraseToCheck,
					head_token = listPhraseToCheck[-1],
					lex_phrase_index = lex_phrase_index,
					lex_uri_index = lex_uri_index,
					max_gram = max_gram,
					stemmer = stemmer,
					apply_wordnet_morphy = apply_wordnet_morphy,
					hyphen_variant = hyphen_variant,
					dict_lexicon_config = dict_lexicon_config )
				
				# any lexicon match is enough to save this proposition
				if len(listLexiconMatch) > 0 :
					return True

	# no lexicon matches so return False
	return False

def merge_lexicon( list_lexicon = None, dict_lexicon_config = None ) :
	"""
	merge N lexicons, aggregating each phrase entry.
	the first schemaURI found in lexicon list (processed top to bottom) is assigned to each phrase URI

	:param list list_lex_phrase_index: list of lexicon tuples = [ ( dict_uri, dict_phrase ), ... ]
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: ( dict_uri, dict_phrase ), where dict_uri = { uri : [ scheme_uri, set_hypernym_uri, set_related_uri ] } and dict_phrase = { phrase : set_uri }. several phrases can share a phrase_uri
	:rtype: tuple
	"""

	if not isinstance( list_lexicon, list ) :
		raise Exception( 'invalid list_lexicon' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	if len(list_lexicon) == 0 :
		return None
	
	dictURIResult = {}
	dictPhraseResult = {}

	for ( dictURI, dictPhrase ) in list_lexicon :
		# set of phraseURIs for each phrase
		for strPhrase in dictPhrase :
			if strPhrase in dictPhraseResult :
				dictPhraseResult[strPhrase].update( dictPhrase[strPhrase] )
			else :
				dictPhraseResult[strPhrase] = copy.deepcopy( dictPhrase[strPhrase] )

		# phraseURI schemaURI, [hyper] and [related] definitions
		for strURI in dictURI :
			if strURI in dictURIResult :
				dictURIResult[strURI][1].update( dictURI[strURI][1] )
				dictURIResult[strURI][2].update( dictURI[strURI][2] )
			else :
				dictURIResult[strURI] = copy.deepcopy( dictURI[strURI] )

	return ( dictURIResult, dictPhraseResult )

def load_plain_vocabulary( filename_vocab = None, phrase_delimiter = ';', lower_case = True, stemmer = None, apply_wordnet_morphy = False, dict_lexicon_config = None ) :
	"""
	import from plan text file a vocabulary. lines beginning with # are ignored
	phrases are delimited by the phrase_delimiter and whitespace at start and end is stripped e.g. 'phase one ; phrase two' -> ['phrase one','phrase two']

	:param str filename_vocab: file with vocabulary
	:param str phrase_delimiter: character delimiting phrases in phrase_list
	:param bool lower_case: if True all lexicon tokens will be converted to lower case. otherwise case is left intact.
	:param nltk.stem.api.StemmerI stemmer: stemmer to use on phrases (default is None)
	:param bool apply_wordnet_morphy: if True apply wordnet.morphy() to find try and base word of a phrase to use in lexicon
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: list of phrases in vocabulary
	:rtype: list
	"""

	# check args
	if not isinstance( filename_vocab, str ) :
		raise Exception( 'invalid filename_vocab' )
	if not isinstance( phrase_delimiter, str ) :
		raise Exception( 'invalid phrase_delimiter' )
	if not isinstance( lower_case, bool ) :
		raise Exception( 'invalid lower_case' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI,type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( stemmer, (nltk.stem.api.StemmerI, type(None)) ) :
		raise Exception( 'invalid stemmer' )
	if not isinstance( apply_wordnet_morphy, bool ) :
		raise Exception( 'invalid apply_wordnet_morphy' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# open file
	readHandle = codecs.open( filename_vocab, 'rb', 'utf-8', errors = 'replace' )

	# we expect comments so ignore any line that starts with a #
	strLine = '#'
	listVocab = []
	while len(strLine) > 0 :
		strLine = readHandle.readline()

		# EOF
		if len(strLine) == 0 :
			break

		# comment
		if strLine.startswith('#') :
			continue

		# remove newline at end and ignore empty lines (e.g. at end of file)
		strLine = strLine.strip()
		if len(strLine) > 0 :
			listPhrase = strLine.split( phrase_delimiter )
			for nIndex in range(len(listPhrase)) :
				strPhrase = listPhrase[nIndex].strip()

				if lower_case == True :
					strPhrase = strPhrase.lower()

				if stemmer != None :
					strPhrase = stemmer.stem( strPhrase )

				if apply_wordnet_morphy == True :
					strBase = soton_corenlppy.lexico.wordnet_lib.find_base_word_form( lemma = strPhrase, morphy_pos_list = None, dict_lexicon_config = dict_lexicon_config )
					if strBase != None :
						strPhrase = strBase

				if not strPhrase in listVocab :
					listVocab.append( strPhrase )

	# close file
	readHandle.close()

	# all done
	return listVocab

def filter_lexicon_wordnet( dict_phrase = None, set_ignore_hyper = set([]), pos='asrnv', lang='eng', count_freq_min = 5, dict_lexicon_config = None ) :
	"""
	filter lexicon to remove all phrases that are Wordnet terms with a common frequency.
	this allows specialist lexicons, with a very specific wordsense, to delete phrases that can have many other wordsenses and thus avoid false positives when using this lexison.
	this method will delete entries from dict_phrase.

	note: if stemming is applied to lexicon then there will be no matches for stemmed words (e.g. 'lotus' > 'lotu' != wordnet match to 'lotus').

	:param dict dict_phrase: phrase dict structure
	:param set set_ignore_hyper: set of hypernymns (wordnet synset names) whose hyponyms should not be used for filtering (e.g. material.n.01)
	:param str pos: WordNet POS filter
	:param str lang: WordNet language
	:param int count_freq_min: minimun WordNet lemma count frequency below which a WordNet lemma is not used as a filter. this is so only common words are filtered out. set to 0 to filter any wordnet word
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 
	"""

	if not isinstance( dict_phrase, dict ) :
		raise Exception( 'invalid dict_phrase' )
	if not isinstance( set_ignore_hyper, set ) :
		raise Exception( 'invalid set_ignore_hyper' )
	if not isinstance( pos, str ) :
		raise Exception( 'invalid pos' )
	if not isinstance( lang, str ) :
		raise Exception( 'invalid lang' )
	if not isinstance( count_freq_min, int ) :
		raise Exception( 'invalid count_freq_min' )
	if not isinstance( dict_lexicon_config, dict ) :
		raise Exception( 'invalid dict_lexicon_config' )

	# make a copy of phrases
	listPhrases = list(dict_phrase.keys())

	# loop on phrases
	for nIndex in range(len(listPhrases)) :
		# get phrase
		strPhraseToLookup = listPhrases[nIndex].lower().strip()

		# lookup phrase synsets in wordnet
		listSynsets = soton_corenlppy.lexico.wordnet_lib.get_synset_names(
			lemma = strPhraseToLookup,
			pos=pos,
			lang=lang,
			dict_lexicon_config = dict_lexicon_config )

		# check hyponyms to avoid
		if len(set_ignore_hyper) > 0 :
			nIndex2 = 0
			while nIndex2 < len(listSynsets) :
				syn = listSynsets[nIndex2]

				setHyper = set([])
				soton_corenlppy.lexico.wordnet_lib.inherited_hypernyms(
					set_lexicon = setHyper,
					syn = syn,
					lang = lang,
					pos=pos,
					max_depth=10,
					depth=0,
					dict_lexicon_config = dict_lexicon_config )

				if len( setHyper.intersection( set_ignore_hyper ) ) > 0 :
					# delete it from possible synsets
					del listSynsets[nIndex2]
				else :
					nIndex2 = nIndex2 + 1

		# get all lemma and sort them by wordnet frequency count
		setLemmaWithFreq = set([])
		for syn in listSynsets :
			# get lemma for synset
			soton_corenlppy.lexico.wordnet_lib.get_lemma_with_freq(
				set_lexicon = setLemmaWithFreq,
				syn = syn,
				pos=pos,
				lang=lang,
				dict_lexicon_config = dict_lexicon_config )

		# phrase not in wordnet?
		if len(setLemmaWithFreq) == 0 :
			continue

		# filter this phrase if we have any lemma with a freq >= the minimum count
		bWordnetMatched = False
		for ( strLemmaID, nFreqLemma ) in setLemmaWithFreq :
			if nFreqLemma >= count_freq_min :
				bWordnetMatched = True
				break

		if bWordnetMatched == True :
			# delete phrase from lexicon
			strPhrase = listPhrases[ nIndex ]
			del dict_phrase[ strPhrase ]


def read_noun_type_ranked_list( filename = None, dict_openie_config = {} ) :
	"""
	read a noun type list for use as an allowed_schema_list (see import_skos_lexicon() and other import functions)

	:param unicode filename: filename for ranked list
	:param dict dict_lexicon_config: config object returned from lexicon_lib.get_lexicon_config() 

	:return: list of 
	:rtype: list
	"""

	readHandle = codecs.open( filename, 'r', 'utf-8', errors = 'replace' )
	listLines = readHandle.readlines()
	readHandle.close()

	listRankedNounType = []

	for strLine in listLines :
		if ( len(strLine) > 0 ) and (strLine[0] != '#') :
			listRankedNounType.append( strLine.strip() )
	
	return listRankedNounType
