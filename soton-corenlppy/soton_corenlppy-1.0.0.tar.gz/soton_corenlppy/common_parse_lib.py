# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
..
	/////////////////////////////////////////////////////////////////////////
	//
	// (c) Copyright University of Southampton IT Innovation, 2015
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
	// Created Date : 2015/11/10
	// Created for Project : REVEAL
	//
	/////////////////////////////////////////////////////////////////////////
	//
	// Dependancies : Source code derived from ITINNO copyright code in TRIDEC
	//
	/////////////////////////////////////////////////////////////////////////
	'''

common parse lib supporting tokenization, POS tagging and sentence management

| POS tagger information
|  http://www-nlp.stanford.edu/links/statnlp.html#Taggers

| Standard POS tagger
|  http://nlp.stanford.edu/software/tagger.shtml
|  license = GPL v2
|  NLTK support for python via remote Java exec
|  English, Arabic, Chinese, French, German

| TreeTagger
|  http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
|  http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/Tagger-Licence
|  https://github.com/miotto/treetagger-python
|  https://courses.washington.edu/hypertxt/csar-v02/penntable.html
|  license = BSD style free for research/eval/teaching but NOT commercial (need to buy it for that)
|  NLTK support for python
|  German, English, French, Italian, Dutch, Spanish, Bulgarian, Russian, Portuguese, Galician, Chinese, Swahili, Slovak, Latin, Estonian, Polish and old French

| Language codes
|  http://tools.ietf.org/html/bcp47

"""

import os, re, sys, copy, collections, codecs, string, traceback, datetime, time, math, subprocess, queue, threading, multiprocessing, logging
import nltk, nltk.corpus, pkg_resources, nltk.tag.stanford
from nltk.util import ngrams

# url and namespace entities regex
# captures: sem@it-innovation.ac.uk http://www.co.uk/blah?=stuff&more+stuff www.co.uk http://user:pass@www.co.uk
# ignores: S.E. Middleton, $5.13, #hashtag, @user_name
# ignores \u2026 which is ... unicode character used by twitter to truncate tweets (which might truncate a URI)
# matches <token>.<token>.<token>... as many tokens as needed as long as there are 2 .'s
# where tokens are at least 2 char long (to avoid matching sets of legitimate initials 'a.b. jones')

namespace_entity_extract = r'\A.*?(?P<NAMESPACE>([a-zA-Z0-9_@\-]){2,}[.](([a-zA-Z0-9_@\-]){1,}[.]){1,5}([a-zA-Z0-9_@\-]){1,})'
url_entity_extract = r'\A.*?(?P<URI>[\w]{3,}\:\/\/[^ \t\n\r\f\v\u2026]*)'

namespace_entity_extract_regex = re.compile( namespace_entity_extract, re.IGNORECASE | re.UNICODE | re.DOTALL)
url_entity_extract_regex = re.compile( url_entity_extract, re.IGNORECASE | re.UNICODE | re.DOTALL)

# currency and number regex
# e.g. 56, 56.76, $54.23, $54 but NOT 52.com
numeric_extract_regex = re.compile(r'\A\D?\d+\.?\d*\Z', re.IGNORECASE | re.UNICODE)

apostrophe_preserve_sub_regex = [
	# stuart's -> stuart-APOS-s, stuart 's -> stuart -APOS-s
	#( re.compile(ur'\A(.*?\S)(\'|\u2019)([sS]\Z|[sS]\s.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), ur'\1-APOS-\3' ),
	( re.compile(r'\A(.*?)(\'|\u2019)([sS]\Z|[sS]\s.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), r'\1-APOS-\3' ),
	# l'plaza -> l-APOS-plaza
	( re.compile(r'\A(.*?\S)(\'|\u2019)(\S*.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), r'\1-APOS-\3' ),
	]

apostrophe_strip_sub_regex = [
	# stuart's -> stuarts, stuart 's -> stuarts
	#( re.compile(ur'\A(.*?\S)(\'|\u2019)([sS]\Z|[sS]\s.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), ur'\1\3' ),
	( re.compile(r'\A(.*?)(\'|\u2019| \'| \u2019)([sS]\Z|[sS]\s.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), r'\1\3' ),
	# l'plaza -> l plaza
	( re.compile(r'\A(.*?\S)(\'|\u2019)(\S*.*\Z)', re.IGNORECASE | re.UNICODE | re.DOTALL), r'\1 \3' ),
	]

# stanford default escaping
list_escape_tuples = [
	( '(', '-LRB-' ),
	( ')', '-RRB-' ),
	( '[', '-LSB-' ),
	( ']', '-RSB-' ),
	( '{', '-LCB-' ),
	( '}', '-RCB-' )
	]


def get_common_config( **kwargs ) :
	"""
	return a common config object for this specific set of languages. the config object contains an instantiated NLTK stemmer, tokenizer and settings tailored for the chosen language set. all available language specific corpus will be read into memory, such as stoplists.
	common config settings are below:
		* *stemmer* = NLTK stemmer, default is no stemming = nltk.stem.RegexpStemmer('', 100000)
		* *t_word* = NLTK word tokenizer for chosen language. default is nltk.tokenize.treebank.TreebankWordTokenizer()
		* *t_sent* = NLTK sent tokenizer for chosen language. default is nltk.tokenize.treebank.PunktSentenceTokenizer()
		* *regex_namespace* = regre.RegexObject, regex to match namespaces e.g. www.bbc.co.uk
		* *regex_url* = regre.RegexObject, regex to match URIs e.g. http://www.bbc.co.uk
		* *regex_numeric_extract* = regre.RegexObject, regex to match numeric strings e.g. 56, 56.76, $54.23, $54 but NOT 52.com
		* *lang_codes* = list, list of ISO 639-1 2 character language codes e.g. ['en','fr']
		* *stoplist* = list, aggregated set of stopwords for languages selected
		* *logger* = logging.Logger, logger object
		* *whitespace* = str, string containing whitespace characters that will be removed prior to tokenization. default is "\\\\u201a\\\\u201b\\\\u201c\\\\u201d
		* *punctuation* = str, string containing punctuation characters that will be forced into thier own token. default is ,;\\\\/:+-#~&*=!?
		* *corpus_dir* = str, directory where common_parse_lib language specific corpus files are located
		* *max_gram* = int, maximum size of n-grams for use in create_ngram_tokens() function. default if 4
		* *first_names* = set, aggragated language specific set of first names
		* *lower_tokens* = bool, if True text will be converted to lower() before tokenization. default is False
		* *sent_token_seps* = list, unicode sentence termination tokens. default is [\\\\n, \\\\r\\\\n, \\\\f, \\\\u2026]
		* *stanford_tagger_dir* = base dir for stanfard POS tagger (e.g. c:\stanford-postagger-full)
		* *treetagger_tagger_dir* = base dir for TreeTagger (e.g. c:\treetagger)
		* *lang_pos_mapping* = dict, set of langauge to PSO tagger mappings. e.g. { 'en' : 'stanford', 'ru' : 'treetagger' }
		* *pos_sep* = tuple, POS separator character and a safe replacement. the default POS separator char is '/' and usually POS tagged sentences become 'term/POS term/POS ...'. when tagging a token containing this character e.g. 'one/two' the POS separator character will be replaced prior to serialization to avoid an ambiguous output.
		* *token_preservation_regex* = dict of key name for regre.RegexObject objects to identify tokens that should be preserved and a unique POS token name (e.g. { 'regex_namespace' : 'NAMESPACE', 'regex_url' : 'URI' } ). POS token name must be unique for chosen POS tagger and safe for POS serialization without characters like ' ' or '/'. this dict argument allows additional POS tokens to be added in the future without the need to change the common_parse_lib code.

	| note: a config object approach is used, as opposed to a global variable, to allow common_parse_lib functions to work in a multi-threaded environment

	:param kwargs: variable argument to override any default config values

	:return: configuration settings to be used by all common_parse_lib functions
	:rtype: dict
	"""

	# use a shallow copy as cannot seem to deepcopy variable args
	dictArgs = copy.copy( kwargs )

	# default corpus directory is where the python lib package has been installed to
	if not 'corpus_dir' in dictArgs :
		if pkg_resources.resource_exists( __name__, 'common_parse_lib.py' ) :
			# if run as an installed python lib
			strCorpusDir = os.path.dirname( pkg_resources.resource_filename( __name__, 'common_parse_lib.py' ) )
		else :
			# if run as a standalone file in a dir
			strCorpusDir = os.path.dirname( __file__ )
		dictArgs['corpus_dir'] = strCorpusDir

	# setup default values
	dictCommonConfig = {
		'stemmer' : nltk.stem.RegexpStemmer('', 100000),
		't_word' : nltk.tokenize.treebank.TreebankWordTokenizer(),
		't_sent' : nltk.tokenize.punkt.PunktSentenceTokenizer(),
		'regex_namespace' : namespace_entity_extract_regex,
		'regex_url' : url_entity_extract_regex,
		'regex_numeric_extract' : numeric_extract_regex,
		'lang_codes' : [],
		'lang_codes_ISO639_2' : [],
		'stoplist' : [],
		'logger' : None,
		'whitespace' : '"\u201a\u201b\u201c\u201d',
		'punctuation' : """,;\/:+-#~&*=!?""",
		'max_gram' : 4,
		'first_names' : set([]),
		'lower_tokens' : False,
		'apostrophe_handling' : 'preserve',
		'sent_token_seps' : [ '.', '\n', '\r', '\f', '\u2026' ],
		'corpus_dir' : None,
		'stanford_tagger_dir' : None,
		'treetagger_tagger_dir' : None,
		'lang_pos_mapping' : {},
		'pos_sep' : ('/','|'),
		'token_preservation_regex' : [ ('regex_url','URI'), ('regex_namespace','NAMESPACE') ]
		}

	# override all defaults with provided args
	for k,v in kwargs.items():
		dictCommonConfig[k] = v

	# use None not '' for POS tagger filenames
	if dictCommonConfig['stanford_tagger_dir'] == '' :
		dictCommonConfig['stanford_tagger_dir'] = None
	if dictCommonConfig['treetagger_tagger_dir'] == '' :
		dictCommonConfig['treetagger_tagger_dir'] = None

	# validate special POS tag dict before its used
	listReplacementRegexName = dictCommonConfig['token_preservation_regex']
	for (strRegexName,strPOSTokenName) in listReplacementRegexName :
		if not strRegexName in dictCommonConfig :
			raise Exception( 'regex pattern ' + strRegexName + ' not in common config but is in pos_replacement_regex' )
		if ' ' in strPOSTokenName :
			raise Exception( 'regex pattern ' + strRegexName + ' has an invalid POS tag (spaces)' )
		if '/' in strPOSTokenName :
			raise Exception( 'regex pattern ' + strRegexName + ' has an invalid POS tag (forward slash)' )

	"""
	rePOSPattern = re.compile( ur'[^' + dictCommonConfig['pos_sep'][0] + ']*' +  dictCommonConfig['pos_sep'][0] + '\S*' , re.UNICODE )
	dictCommonConfig['regex_pos_parse'] = rePOSPattern
	"""


	# POS mapping example
	# lang_pos_mapping = { 'en' : 'stanford', 'ru' : 'treetagger' }
	# pos_sep = ('/','|') ==> sep char and its replacement
	#   ... so that TreeTagger POS tag 'IN/that' becomes 'IN|that' which can then be serialized OK using / separator char to 'that/IN_that'
	#   ... also will change tokens for same reason

	# sent_token_seps = ['\n','\r\n', '\f', u'\u2026']
	# characters that always denote a new sentence like a newline. do NOT include period . in this as you can have numbers like 8.34 

	# note: NLTK3 PunktSentenceTokenizer() leave periods on words (e.g. some sentence.)
	#       TreebankWordTokenizer treats # as a token in itself (e.g. # tag) as well as %5.67 (e.g. # 5.67) and 

	#
	# create a stoplist based on the languages used
	# - NLTK language stoplists
	# - NLTK names (en)
	#
	listStoplistFinal = []

	# stopwords from NLTK based on language
	for strCode in dictCommonConfig['lang_codes'] :
		# note: NLTK stopwords are stored in language named files so do a quick convert from lang code to lang name
		strLanguage = None
		strISO639 = None
		if strCode == 'da' :
			strLanguage = 'danish'
			strISO639 = 'dan'
		elif strCode == 'en' :
			strLanguage = 'english'
			strISO639 = 'eng'
		elif strCode == 'fi' :
			strLanguage = 'finnish'
			strISO639 = 'fin'
		elif strCode == 'fr' :
			strLanguage = 'french'
			strISO639 = 'fra'
		elif strCode == 'de' :
			strLanguage = 'german'
			strISO639 = 'deu'
		elif strCode == 'hu' :
			strLanguage = 'hungarian'
			strISO639 = 'hun'
		elif strCode == 'it' :
			strLanguage = 'italian'
			strISO639 = 'ita'
		elif strCode == 'no' :
			strLanguage = 'norwegian'
			strISO639 = 'nor'
		elif strCode == 'pt' :
			strLanguage = 'portuguese'
			strISO639 = 'por'
		elif strCode == 'ru' :
			strLanguage = 'russian'
			strISO639 = 'rus'
		elif strCode == 'es' :
			strLanguage = 'spanish'
			strISO639 = 'spa'
		elif strCode == 'se' :
			strLanguage = 'swedish'
			strISO639 = 'swe'
		elif strCode == 'tr' :
			strLanguage = 'turkish'
			strISO639 = 'tur'
		elif strCode == 'ar' :
			strLanguage = 'arabic'
			strISO639 = 'ara'
		elif strCode == 'zh' :
			strLanguage = 'chinese'
			strISO639 = 'zho'

		if strISO639 != None :
			dictCommonConfig['lang_codes_ISO639_2'].append( strISO639 )

		if strLanguage != None :
			listStoplist = nltk.corpus.stopwords.words( strLanguage )
			for strTerm in listStoplist :
				strText = strTerm

				# clean and stem stoplist words as this is what will happen to all tokens
				# we match against the stoplist
				# note: if cleaned and stemmed word disappears then ignore it!
				# note: clean_text does NOT use the stoplist so its OK to call it here
				strTextClean = clean_text( strText, dictCommonConfig )
				strStem = dictCommonConfig['stemmer'].stem( strTextClean )
				if len(strStem) > 0 :
					if not strStem in listStoplistFinal :
						listStoplistFinal.append( strStem )

	# common names (as locations often match common names such as Chelsea)
	if 'en' in dictCommonConfig['lang_codes'] :
		listNames = nltk.corpus.names.words()
		for strName in listNames :
			strText = strName

			# add name to name list
			strTextClean = clean_text( strText, dictCommonConfig )
			dictCommonConfig['first_names'].add( strTextClean )

	dictCommonConfig['stoplist'] = listStoplistFinal

	# specify the lang to POS tagger mapping making sure we do not override any settings provided explicitly by caller
	# note: default POS tagger is NLTK treebank which is not very good for anything but English !!
	dictPOS = {}

	if dictCommonConfig['stanford_tagger_dir'] != None :
		# stanford is better choice (from literature anyway) than treetagger where both can do a language
		if not 'ar' in dictPOS :
			dictPOS['ar'] = 'stanford'
		if not 'en' in dictPOS :
			dictPOS['en'] = 'stanford'
		if not 'zh' in dictPOS :
			dictPOS['zh'] = 'stanford'
		if not 'fr' in dictPOS :
			dictPOS['fr'] = 'stanford'
		if not 'es' in dictPOS :
			dictPOS['es'] = 'stanford'
		if not 'de' in dictPOS :
			dictPOS['de'] = 'stanford'

	if dictCommonConfig['treetagger_tagger_dir'] != None :
		# better choice than treebank is the multi-lingual treetagger
		if not 'bg' in dictPOS :
			dictPOS['bg'] = 'treetagger'
		if not 'nl' in dictPOS :
			dictPOS['nl'] = 'treetagger'
		if not 'en' in dictPOS :
			dictPOS['en'] = 'treetagger'
		if not 'et' in dictPOS :
			dictPOS['et'] = 'treetagger'
		if not 'fi' in dictPOS :
			dictPOS['fi'] = 'treetagger'
		if not 'fr' in dictPOS :
			dictPOS['fr'] = 'treetagger'
		if not 'de' in dictPOS :
			dictPOS['de'] = 'treetagger'
		if not 'it' in dictPOS :
			dictPOS['it'] = 'treetagger'
		if not 'pl' in dictPOS :
			dictPOS['pl'] = 'treetagger'
		if not 'ru' in dictPOS :
			dictPOS['ru'] = 'treetagger'
		if not 'sk' in dictPOS :
			dictPOS['sk'] = 'treetagger'
		if not 'es' in dictPOS :
			dictPOS['es'] = 'treetagger'

	dictCommonConfig['lang_pos_mapping'] = dictPOS

	# all done
	return dictCommonConfig

def ngram_tokenize_microblog_text( text, dict_common_config ) :
	"""
	tokenize a microblog entry (e.g. tweet) into all possible combinations of N-gram phrases keeping the linear sentence structure intact
	text will be cleaned and tokenized. URL's and namespaces are explicitly preserved as single tokens. a set of all possible n-gram tokens is returned up to max-gram

	:param unicode text: UTF-8 text to tokenize
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: list of n-gram token sets e.g. [ [('one',),('two',),('three',),('four',)], [('one','two'), ('two','three'), ('three','four')], [('one','two','three'),('two','three','four')] ]
	:rtype: list
	"""

	# check args without defaults
	if (not isinstance( text, str )) and (not isinstance( text, str )) :
		raise Exception( 'invalid text' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )


	# tokenize text into 1g tokens
	listTokensAll = unigram_tokenize_text( text, dict_common_config )

	# create ngram token set from this
	listTokenAllg = create_ngram_tokens( listTokensAll, dict_common_config['max_gram'], dict_common_config['sent_token_seps'] )

	# all done
	return listTokenAllg

def unigram_tokenize_text( text = None, include_char_offset = False, dict_common_config = None ) :
	"""
	tokenize a text entry (e.g. tweet) into unigram tokens
	text will be cleaned and tokenized. URL's and namespaces are explicitly preserved as single tokens.

	:param unicode text: UTF-8 text to tokenize
	:param include_char_offset bool: if True result is a list of [ list_tokens, list_char_offset_for_tokens ]
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: list of unigram tokens e.g. [ 'one','two','three' ]
	:rtype: list
	"""

	# check args without defaults
	if not isinstance( text, str ) :
		raise Exception( 'invalid text' )
	if not isinstance( include_char_offset, bool ) :
		raise Exception( 'invalid include_char_offset' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	if include_char_offset == True :
		[ listSents, listSentCharOffsets ] = unigram_tokenize_text_with_sent_breakdown(
			text = text,
			include_char_offset = include_char_offset,
			dict_common_config = dict_common_config )

		listTokensAll = []
		for listTokens in listSents :
			listTokensAll.extend( listTokens )

		listOffsetsAll = []
		for listOffsets in listSentCharOffsets :
			listOffsetsAll.extend( listOffsets )

		return [ listTokensAll, listOffsetsAll ]

	else :
		listSents = unigram_tokenize_text_with_sent_breakdown(
			text = text,
			include_char_offset = include_char_offset,
			dict_common_config = dict_common_config )

		listTokensAll = []
		for listTokens in listSents :
			listTokensAll.extend( listTokens )

		return listTokensAll


def unigram_tokenize_text_with_sent_breakdown( text = None, include_char_offset = False, dict_common_config = None ) :
	"""
	tokenize a microblog entry (e.g. tweet) into unigram tokens broken down into individual sents. sent token removed at end of each sent.
	text will be cleaned and tokenized. URL's and namespaces are explicitly preserved as single tokens.

	:param unicode text: UTF-8 text to tokenize
	:param include_char_offset bool: if True result is a list of [ list_token_set, list_char_offset_for_token_set ]
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: list of sents, each itself a list of unigram tokens e.g. [ [ 'one','two','three' ], ... ]
	:rtype: list
	"""

	# check args without defaults
	if not isinstance( text, str ) :
		raise Exception( 'invalid text' )
	if not isinstance( include_char_offset, bool ) :
		raise Exception( 'invalid include_char_offset' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	# 
	# tokenize text
	#
	# strategy for handling tweet text and making 1..6g tokens for subsequent matching
	# (1) preserve URLs and NS with placeholder tokens
	# (2) clean whitespace from text 
	# (3) remove stop list words
	# (4) stem text
	# (5) tokenize <text> and create all 1..6g tokens
	# (6) optionally add a sent_token separator at the end of every parsed token set
	# (7) restore URLs and NS
	#

	if dict_common_config['t_word'] == None :
		raise Exception( 'word tokenizer None' )
	listSentToken = dict_common_config['sent_token_seps']

	# find any URL, NS etc entities and replace them with a __URL1__ token
	# so we can treat them as single tokens later on
	# e.g.
	# find any namespace entities like emails and web address fragments and replace them with a space
	# this avoids joe@co.nz ==> joe@co nz and then matching new zealand
	# and www.news.nz (without the http protocol)
	# note: execute regex in strict list order so we can add most permissive patterns last to avoid overmatching
	dictReplacementTokens = {}

	strTextAfterReplace = text
	listReplacementRegexName = dict_common_config['token_preservation_regex']
	nIndex = 0
	for (strRegexName,strPOSTokenName) in listReplacementRegexName :
		rePattern = dict_common_config[ strRegexName ]

		bMore = True
		while bMore == True :
			matchInstance = rePattern.match( strTextAfterReplace )
			if matchInstance != None :
				if strPOSTokenName not in matchInstance.groupdict() :
					raise Exception( 'regex pattern ' + strRegexName + ' does not create named group ' + strPOSTokenName )

				strEntity = matchInstance.groupdict()[strPOSTokenName]
				strPlaceholder = '__' + strPOSTokenName + str(nIndex+1) + '__'
				nIndex = nIndex + 1

				# replace 1st match with the token (so it will not match again and be kept whole in tokenization)
				# insert ' __<name>__' with a space in case the regex matched within a token (e.g. 'some;' -> 'some __SEMI_COLON__').
				nPosStart = matchInstance.start( strPOSTokenName )
				nPosEnd = matchInstance.end( strPOSTokenName )
				strTextAfterReplace = strTextAfterReplace[:nPosStart] + ' ' + strPlaceholder + strTextAfterReplace[nPosEnd:]

				# remember each tokens true value so it can be replaced later
				dictReplacementTokens[strPlaceholder] = strEntity
			else :
				bMore = False

	# clean the text field
	strTextClean = clean_text( strTextAfterReplace, dict_common_config )

	# tokenize - sentences
	listSentences = []
	if dict_common_config['t_sent'] != None :
		listSentText = []
		if len(listSentToken) > 0 :
			# convert all sep chars to 1st sep char
			if len(listSentToken) > 1 :
				for strTokenSep in listSentToken[1:] :
					strTextClean = strTextClean.replace( strTokenSep, listSentToken[0] )

			# split using 1st sep char
			listSentText = strTextClean.split( listSentToken[0] )
		else :
			listSentText = [strTextClean]
 
		# use sent tokenizer on sent broken down by newline
		# to get sent broken down by . etc
		# note: PunktSentenceTokenizer will break up stuff like 'Dell Corp. has' -> 'Dell Corp.', 'has' so use a custom regex patten to do better
		for strSentText in listSentText :
			listSentences.extend( dict_common_config['t_sent'].tokenize( strSentText ) )
	else :
		listSentences = [ strTextClean ]

	# tokenize words
	listSents = []
	for strSentence in listSentences :
		# use word tokenizer
		listTokens = tokenize_sentence( strSentence, dict_common_config )

		# restore replacement tokens (e.g. URI's and NS) to their original values preserving them from bring broken up via tokenization
		for nIndex in range(len(listTokens)) :
			if listTokens[nIndex] in dictReplacementTokens :
				listTokens[nIndex] = dictReplacementTokens[ listTokens[nIndex] ]

		# record final result
		listSents.append( listTokens )

	# lookup the character offset for each token and replace the text entry with a tuple (text,char_offset)
	# tokens (from cleaned text) should always appear in text somewhere even if there are whitespace chars between token entries
	# see clean_text() for details
	if include_char_offset == True :
		listSentCharOffsets = []

		if dict_common_config['lower_tokens'] == True :
			strOriginalText = text.lower()
		else :
			strOriginalText = text

		nNextChar = 0
		for listTokens in listSents :
			listOffsets = []
			for strToken in listTokens :
				try :
					if dict_common_config['lower_tokens'] == True :
						nTokenPos = strOriginalText.index( strToken.lower(), nNextChar )
					else :
						nTokenPos = strOriginalText.index( strToken, nNextChar )
				except :
					raise Exception( 'post-tokenized token ' + repr(strToken) + ' not found in original text during char offset lookup :' + repr(strOriginalText) )

				listOffsets.append( nTokenPos )
				nNextChar = nTokenPos + len(strToken)

			listSentCharOffsets.append( listOffsets )

		return [ listSents, listSentCharOffsets ]
	
	else :
		return listSents


def tokenize_sentence( sent, dict_common_config ) :
	"""
	tokenizes a single sentence into stemmed tokens.
	if nltk.tokenize.treebank.TreebankWordTokenizer is used then tokens will be corrected for embedded punctuation within tokens and embedded periods within tokens unless they are numeric values

	:param unicode sent: UTF-8 text sentence to tokenize
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: list of unigram tokens e.g. [ 'one','two','three' ]
	:rtype: list
	"""

	# check args without defaults
	if (not isinstance( sent, str )) and (not isinstance( sent, str )) :
		raise Exception( 'invalid sent' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	if dict_common_config['t_word'] == None :
		raise Exception( 'word tokenizer None' )

	strCharPunctuation = dict_common_config['punctuation']
	regex_numeric = dict_common_config['regex_numeric_extract']

	# tokenize using the chosen tokenizer into 1-gram tokens
	listTokens = dict_common_config['t_word'].tokenize( sent )

	# clean whitespace from start and end of each token
	for nIndex in range(len(listTokens)) :
		listTokens[nIndex] = listTokens[nIndex].strip()

	if isinstance( dict_common_config['t_word'],nltk.tokenize.treebank.TreebankWordTokenizer ) :
		# the TreebankWordTokenizer sentence tokenizer will work for 'london.oxford' but make a '...' token if we have multiple periods
		# ':' and '#' will get a token on its own
		# tokens like 'corp.' will be kept intact. Deliberately break up a period right at end of sent, as this is mostly the sent terminating '.' 

		nIndex = 0
		while nIndex < len(listTokens) :

			# TreebankWordTokenizer internal punctuation cannot handle missing spaces with punctuation
			# e.g. will parse 'one ,two' but not 'one,two'
			# and will leave punctuation attached
			# e.g. will parse 'one, two' ==> 'one,', 'two'
			# therefore expand punctuation by adding spaces then insert the new tokens
			strTokenExpanded = listTokens[nIndex]
			if len(strTokenExpanded) > 1 :
				for cPunctuation in strCharPunctuation :
					strTokenExpanded = strTokenExpanded.replace( cPunctuation, ' ' + cPunctuation + ' ' )
				listTokenNew = strTokenExpanded.strip().split(' ')
				if len(listTokenNew) > 1 :
					# insert N tokens just after current token (insert in reverse order)
					for nNew in range(len(listTokenNew)-1,-1,-1) :
						listTokens.insert( nIndex+1, listTokenNew[nNew].strip() )

					# delete current token (keep index the same so it now points to start of added token set
					del listTokens[nIndex]
				else :
					listTokens[nIndex] = listTokenNew[0]

			# handle period (at end) and sequences of periods
			# TreebankWordTokenizer does this:
			# corp. -> corp. [unless its at the end of a sent]
			# one.two -> one.two
			# one..two -> one..two
			# one...two -> one ... two
			# one....two -> one ... .two
			# and we might get a period at the end as a valid sent terminator
			strToken = listTokens[nIndex]
			if strToken.count('.') > 0 :

				'''
				NOT NEEDED
				# is this a single period? if so merge it back into the preceeding token unless its at the end of the sent, or the preceeding token is period(s)
				if (strToken == '.') and (nIndex != len(listTokens) - 1) :
					if (nIndex > 0) and (listTokens[nIndex-1].count('.') != len(listTokens[nIndex-1])) :
						listTokens[nIndex-1] = listTokens[nIndex-1] + '.'
						del listTokens[nIndex]
						nIndex = nIndex - 1
				'''

				if (strToken.endswith('.')) and (strToken.count('.') == 1) :
					# avoid corp. -> 'corp','.'
					pass

				# break it up if its not a number pattern
				elif regex_numeric.match( strToken ) == None :

					# .stuff
					# ..stuff
					# s.e.middleton
					# bad..grammar
					# ...

					# split text using . as its not a number
					# ... -> '','','',''
					# ..yeah -> '','','yeah'
					# . -> '',''

					listTokenSplit = strToken.split('.')
					listTokensToAdd = []

					# merge sequential periods (not the last period IF its also the last token in the sent however)
					nCount = 0
					for strSplit in listTokenSplit :
						if strSplit == '' :
							nCount = nCount + 1
						else :
							if nCount > 0 :
								listTokensToAdd.append( '.' * nCount )
							listTokensToAdd.append( strSplit )
							nCount = 1
					if nCount > 1 :
						# last token? ensure we have a last period
						if nIndex == len(listTokens) - 1 :
							if nCount > 2 :
								listTokensToAdd.append( '.' * (nCount-2) )
							listTokensToAdd.append( '.' )
						else :
							listTokensToAdd.append( '.' * (nCount-1) )

					# replace original token with the new ones
					for nIndexNew in range(len(listTokensToAdd)) :
						if nIndexNew == 0 :
							listTokens[nIndex] = listTokensToAdd[nIndexNew]
						else :
							listTokens.insert( nIndex + nIndexNew, listTokensToAdd[nIndexNew] )
					nIndex = nIndex + nIndexNew

			'''
			if regex_numeric.match( strToken ) == None :
				bNum = False
			else :
				bNum = True

			if bNum == False :
				# split text using . as its not a number
				listTokenNew = strToken.strip().split('.')

				# if we have a split then expand the token set
				# otherwise leave it alone completely (keep tokens like '.')
				if len(listTokenNew) > 1 :

					listTokens[nIndex] = listTokenNew[0]
					for nNew in range(1,len(listTokenNew)) :
						# insert will add token BEFORE index so we make sure its 1 after current pos
						# also we need to increment the index anyway as the list has just expanded

						# add period
						nIndex = nIndex + 1
						listTokens.insert( nIndex, '.' )

						# add token (if its not '' which it might be if period at end e.g. 'hello.' ==> ['hello',''])
						strTokenToAdd = listTokenNew[nNew].strip()

						if len(strTokenToAdd) > 0 :
							nIndex = nIndex + 1
							listTokens.insert( nIndex, strTokenToAdd )
				else :
					listTokens[nIndex] = listTokenNew[0]
			'''

			# next token
			nIndex = nIndex + 1

	# stem the resulting tokens
	if dict_common_config['stemmer'] != None :
		stemmer = dict_common_config['stemmer']
		for nIndex in range(len(listTokens)) :
			if len( listTokens[nIndex] ) > 1 :
				strStem = stemmer.stem( listTokens[nIndex] )
				listTokens[nIndex] = strStem.strip()

	# remove all empty string entries from list
	while listTokens.count( '' ) > 0 :
		listTokens.remove( '' )

	return listTokens

def create_ngram_tokens( list_tokens, max_gram = 4, sent_temination_tokens = None ) :
	"""
	compile n-gram phrase sets keeping the linear sequence of tokens intact up to a maximum gram size
	the optional sent_temination_tokens prevents n-gram tokens spanning sent terminator tokens (e.g. newlines)

	:param list list_tokens: unigram token list
	:param int max_gram: max gram size to create
	:param list sent_temination_tokens: list of sent terminator tokens

	:return: set of n-gram tokens e.g. [ [('one',),('two',),('three',),('four',)], [('one','two'), ('two','three'), ('three','four')], [('one','two','three'),('two','three','four')] ]
	:rtype: list
	"""

	# check args without defaults
	if not isinstance( list_tokens, list ) :
		raise Exception( 'invalid list_tokens' )

	# get a set of sentence end indexes (i.e. index of any sent tokens)
	listIndexSent = []
	if sent_temination_tokens != None :
		for nIndexToken in range(len(list_tokens)) :
			if list_tokens[nIndexToken] in sent_temination_tokens :
				listIndexSent.append( nIndexToken )

	# ensure 1 token past end is a sentence end index
	listIndexSent.append( len(list_tokens) )

	# process each sentence and aggregate the results
	listTokensAllg = []
	for nGram in range( max_gram ) :
		listGramTokens = []

		# get 1g tokens for each sent and calc ngrams for them
		nLastSentIndex = -1
		for nSentIndex in listIndexSent :
			listTokens1gSent = list_tokens[ nLastSentIndex + 1 : nSentIndex ]
			nLastSentIndex = nSentIndex

			# calc ngram tokens
			# note: this is nltk.util.ngrams BUT we cannot import nltk.utils (not a package in itself)
			listGramTokens.extend( list( ngrams( listTokens1gSent, nGram + 1 ) ) )

		# add all ngram tokens for all sents to a single list (keeping the strict sequential nature)
		listTokensAllg.append( listGramTokens )

	# all done
	return listTokensAllg

def clean_text( original_text, dict_common_config, whitespace_chars = None ) :
	"""
	clean a block of unicode text ready for tokenization.
	replace sequences of whitespace with a single space.
	if config[lower_tokens] = True then make text lowercase.
	if config[apostrophe_handling] = 'preserve' then ensure appos entries are preserved (even if appos is a whitespac character)
	if config[apostrophe_handling] = 'strip' then ensure appos entries are removed

	:param unicode original_text: UTF-8 text to clean
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 
	:param unicode whitespace_chars: whitespace characters. if None the configuration setting will be used in dict_common_config

	:return: clean text
	:rtype: unicode
	"""

	# check args without defaults
	if not isinstance( original_text, str ) and not isinstance( original_text, str ) :
		raise Exception( 'invalid original_text' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	strText = copy.deepcopy( original_text )
	if whitespace_chars == None :
		strCharWhitespace = dict_common_config['whitespace']
	else :
		strCharWhitespace = whitespace_chars

	# convert to lower case as tweets are pretty random about using cases so its not very useful
	# (e.g. in formal docs named entities use capitals but for tweets this is useless)
	# note: this will prevent accurate POS and NE later so not always a good thing!
	if dict_common_config['lower_tokens'] == True :
		strText = str( strText ).lower()
	else :
		strText = str( strText );

	# remove ' since they cause problems later when processing
	# as tokens wont match (e.g. dont != don't for simple matching)
	# and John's -> John since its not actually a plural
	# special case for 's (english plural) and l' (french le abbreviaton)
	if dict_common_config['apostrophe_handling'] == 'preserve' :
		for tupleRegex in apostrophe_preserve_sub_regex :
			strText = tupleRegex[0].sub( tupleRegex[1], strText )
	elif dict_common_config['apostrophe_handling'] == 'strip' :
		for tupleRegex in apostrophe_strip_sub_regex :
			strText = tupleRegex[0].sub( tupleRegex[1], strText )
	elif dict_common_config['apostrophe_handling'] == 'none' :
		pass
	else :
		raise Exception( 'invalid config apostrophe_handling value : ' + repr(dict_common_config['apostrophe_handling']) + ' : expected preserve|strip|none' )

	# remove user defined whitespace
	# note: do this AFTER checking for apostrophe handling
	for cWhitespace in strCharWhitespace :
		strText = strText.replace( cWhitespace,' ' )

	# replace sequences of space and tabs with a single space
	# strip normal whitespace (space, tab, newline) from start and end of text
	# strText = re.sub( r'\s+', " ", strText ).strip()
	strText = re.sub( r'[ \t]+', " ", strText ).strip()

	# preserve apostrophe (if chosen)
	if dict_common_config['apostrophe_handling'] == 'preserve' :
		strText = strText.replace('-APOS-',"'")

	# all done
	return strText

def check_retweet( original_text ) :
	"""
	check for rwteeets (assumes raw unprocessed text e.g. 'RT @username ...')

	:param unicode original_text: UTF-8 text to clean

	:return: true if text contains a retweet pattern
	:rtype: bool
	"""

	# check args without defaults
	if not isinstance( original_text, str ) :
		raise Exception( 'invalid original_text' )

	bRetweet = False

	# the official Twitter retweet protocol is to add 'RT @username' in front of a retweet
	# this is not mandatory but most people follow this
	strText = original_text.lower()
	if strText.startswith( 'rt @' ) :
		bRetweet = True

	# also support these variants
	if strText.startswith( 'rt "@' ) :
		bRetweet = True
	if strText.startswith( 'rt :@' ) :
		bRetweet = True
	if strText.startswith( 'rt ''@' ) :
		bRetweet = True

	# also check for the matches WITHIN the string itself as people often retweet by putting a comment at front manually
	if ' rt @' in strText :
		bRetweet = True
	if ' rt "@' in strText :
		bRetweet = True
	if ' rt :@' in strText :
		bRetweet = True
	if ' rt ''@' in strText :
		bRetweet = True

	return bRetweet

#
# check to see if tokens are only stoplist tokens
# listTokens = tokens to check against a stoplist
# dictCommonConfig = dict <- common_parse_lib.get_common_config()
# return = True if ALL tokens match the stoplist (i.e. token set is useless as a phrase)
#
def is_all_stoplist( list_tokens, dict_common_config ) :
	"""
	check to see if tokens are only stoplist tokens

	:param list list_tokens: list of unigram tokens
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: True if ALL tokens match the stoplist (i.e. token set is useless as a phrase)
	:rtype: bool
	"""

	# check args without defaults
	if not isinstance( list_tokens, list ) :
		raise Exception( 'invalid list_tokens' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	listStoplist = dict_common_config['stoplist']

	for strToken in list_tokens :
		if listStoplist.count(strToken) == 0 :
			return False

	return True


def pos_tag_tokenset_batch( document_token_set, lang, dict_common_config, max_processes = 4, timeout = 300 ) :
	"""
	POS tag a batch of tokenized sentences for a specific langauge. it is more efficient to POS tag in large batches as the POS tagger is a separate process that must be invoked using an OS exec and a Python subprocess command. there is a fixed overhead for sub-process and pipe setup time (e.g. 1-2 seconds) so processing text in bulk is more efficient than many small separate sentences.
	use multiprocess spawning to maximize the CPU usage as this is a slow process that is CPU intensive.

	| note: the POS tagger used is chosen from TreeTagger, Stanford and Treebank based on language code
	| note: URL's and namespaces matching regex patterns provided in dict_common_config will get a POS tag of 'URI' or 'NAMESPACE' regardless of which POS tagger is used
	| note: tokens matching characters in dict_common_config['sent_token_seps'] will be labelled with a POS tag 'NEWLINE'

	:param dict document_token_set: { docID : [ token_set for each document sent ] }
	:param list lang_codes: list of ISO 639-1 2 character language codes (e.g. ['en','fr'])
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int timeout: timeout in seconds for POS tagger process in the unlikely event the POS tagger hangs

	:return: dict of POS tagged documents { docID : [ tagged_token_set for each document sent ] }
	:rtype: dict
	"""

	# check args without defaults
	if not isinstance( document_token_set, dict ) :
		raise Exception( 'invalid document_token_set' )
	if (not isinstance( lang, str )) and (not isinstance( lang, str )) :
		raise Exception( 'invalid lang' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )
	if not isinstance( max_processes, int ) :
		raise Exception( 'invalid max_processes' )
	if not isinstance( timeout, int ) :
		raise Exception( 'invalid int' )

	# create (queueIn, queueOut, queueError) for each process
	listQueue = []
	listQueueInput = []
	listQueueResultsPending = []
	for nProcess in range(max_processes) :
		listQueue.append( ( multiprocessing.Queue(), multiprocessing.Queue(), multiprocessing.Queue() ) )
		listQueueInput.append( [] )
		listQueueResultsPending.append(0)

	# chunk up the documents and put in queues to be processed
	nProcess = 0
	for strDocumentID in document_token_set:
		listSentTokens = document_token_set[strDocumentID]

		if len(listSentTokens) == 0 :
			listQueueInput[nProcess].append( ( strDocumentID, None ) )
			listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] + 1

			# round robin assignment to queues
			nProcess = nProcess + 1
			if nProcess >= max_processes :
				nProcess = 0

		else :
			listQueueInput[nProcess].append( ( strDocumentID, listSentTokens ) )
			listQueueResultsPending[nProcess] = listQueueResultsPending[nProcess] + 1

			# round robin assignment to queues
			nProcess = nProcess + 1
			if nProcess >= max_processes :
				nProcess = 0

	# multiprocess cannot pickle logger objects so run without logger
	# each worker thread will make a logger within its own process
	# use copy as regex and logger will not deepcopy. nltk word and sent tokenizers are all regex based, and regex is very likely to be thread safe the way its used
	dictConfigCopy = copy.deepcopy( dict_common_config )
	dictConfigCopy['logger'] = None

	# setup a process pool as the template generation is very CPU intensive so we need to use all cores on a machine to speed it up
	listProcesses = []
	for nProcess in range(max_processes) :
		if 'logger' in dict_common_config :
			dict_common_config['logger'].info( 'starting process ' + str(nProcess) + ' [POS tagger]' )

		processWorker = multiprocessing.Process(
			target = pos_tag_tokenset_batch_worker,
			args = (
				listQueue[nProcess],
				lang,
				dictConfigCopy,
				1,
				timeout,
				nProcess )
			)
		listProcesses.append( processWorker )

	# tell each process how many documents to expect
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

	if 'logger' in dict_common_config :
		dict_common_config['logger'].info( 'input data written OK [POS tagger]' )

	# write input and process output together to ensure queue sizes do not grow too large (which will cause errors and dropped data)
	dictOutputResults = {}
	try :

		# download the results from each process queue in a round robin way until they are all read in
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

						if 'logger' in dict_common_config :
							dict_common_config['logger'].info( '\tprocess ' + str(nProcess) + ' [POS tagger] failure > ' + strErrorMsg )

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
						( strDocumentID, listPOSSet ) = listQueue[nProcess][1].get( False )

						#if 'logger' in dict_common_config :
						#	dict_common_config['logger'].info( 'result from p' + str(nProcess) + ' : ' + strDocumentID )

						# process result
						if not strDocumentID in dictOutputResults :
							dictOutputResults[strDocumentID] = []

						if listPOSSet != None :
							dictOutputResults[strDocumentID] = listPOSSet

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

		if 'logger' in dict_common_config :
			dict_common_config['logger'].info( 'results aggregated OK [POS tagger]' )

	finally :
		# pause for 2 seconds to allow subprocesses with 0 documents to process enough time to complete
		# otherwise we will remove the num docs from the input quete before
		time.sleep(2)

		# do cleanup
		if 'logger' in dict_common_config :
			dict_common_config['logger'].info( 'tidying up from worker processes [POS tagger]' )
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
				listQueue[nProcess][nQueue].close()

		if 'logger' in dict_common_config :
			dict_common_config['logger'].info( 'tidy up complete [POS tagger]' )

	# all done
	return dictOutputResults


def pos_tag_tokenset_batch_worker( tuple_queue = None, lang = 'en', dict_common_config = None, pause_on_start = 0, timeout = 300, process_id = 0 ) :
	"""
	worker thread for comp_sem_lib.pos_tag_tokenset_batch()

	:param tuple tuple_queue: tuple of queue (queueIn, queueOut, queueError). queueIn has tuples of ( doc_id, [ token_set for each document sent ] ). queueOut has tuples of ( doc_id, [ tagged_token_set for each document sent ] ).
	:param list lang_codes: list of ISO 639-1 2 character language codes (e.g. ['en','fr'])
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 
	:param int max_processes: number of worker processes to spawn using multiprocessing.Process
	:param int pause_on_start: number of seconds to delay thread startup before CPU intensive work begins (to allow other workers to startup also)
	:param int timeout: timeout in seconds for POS tagger process in the unlikely event the POS tagger hangs
	:param int process_id: ID of process for logging purposes
	"""

	if not isinstance( tuple_queue, tuple ) :
		raise Exception( 'invalid tuple_queue' )
	if (not isinstance( lang, str )) and (not isinstance( lang, str )) :
		raise Exception( 'invalid lang' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )
	if not isinstance( process_id, int ) :
		raise Exception( 'invalid process_id' )
	if not isinstance( pause_on_start, int ) :
		raise Exception( 'invalid pause_on_start' )
	if not isinstance( timeout, int ) :
		raise Exception( 'invalid int' )

	try :
		# make a config with a valid logger (created within this process)
		dictConfigCopy = copy.deepcopy( dict_common_config )

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
		logger.info('worker process started (' + str(process_id) + ') [POS tagger]' )

		# get number of documents to process
		nDocumentsMax = tuple_queue[0].get()

		# loop on input queue and build a large set of tokens to POS tag
		listCorpusTokenSet = []
		listDocMeta = []
		listDocEmpty = []
		for nDocument in range(nDocumentsMax) :

			# get tokens to POS tag
			( strDocumentID, listDocTokenSet ) = tuple_queue[0].get()

			# remember the start and end index in corpus token set so we can create the document dict later
			if listDocTokenSet != None :
				listDocMeta.append( ( strDocumentID, len(listCorpusTokenSet), len(listDocTokenSet) ) )
				listCorpusTokenSet.extend( listDocTokenSet )
			else :
				listDocEmpty.append( strDocumentID )

		logger.info('documents read in OK (' + str(process_id) + ') = ' + str(nDocumentsMax) + ' [POS Tagger]')

		# POS tag massive batch of tokens
		listTaggedCorpusTokenSet = pos_tag_tokenset(
								token_set = listCorpusTokenSet,
								lang = lang,
								dict_common_config = dictConfigCopy,
								timeout = timeout )

		# logger.info('tagged corpus size (' + str(process_id) + ') = ' + str(len(listTaggedCorpusTokenSet)) + ' [POS Tagger]')

		# compile result (empty docs)
		nCount = 0
		for nIndexEntry in range(len(listDocEmpty)) :
			tuple_queue[1].put( ( listDocEmpty[nIndexEntry], None ) )
			nCount = nCount + 1

			#logger.info('queue OUT empty (' + str(process_id) + ') ' + repr( listDocEmpty[nIndexEntry] ) + ' [POS tagger]' )

			# check for output queue overload (which can cause multiprocess Queue handling errors and lost results).
			# pause until the queue is smaller if this is the case.
			while tuple_queue[1].qsize() > 100 :
				time.sleep( 1 )

		# compile result (docs with tokens)
		for nIndexEntry in range(len(listDocMeta)) :
			listTaggedDocTokenSet = listTaggedCorpusTokenSet[ listDocMeta[nIndexEntry][1] : listDocMeta[nIndexEntry][1] + listDocMeta[nIndexEntry][2] ]
			tuple_queue[1].put( ( listDocMeta[nIndexEntry][0], listTaggedDocTokenSet ) )
			nCount = nCount + 1

			#logger.info('queue OUT tokens (' + str(process_id) + ') ' + repr( listDocMeta[nIndexEntry][0] ) + ' [POS tagger]' )

			# check for output queue overload (which can cause multiprocess Queue handling errors and lost results).
			# pause until the queue is smaller if this is the case.
			while tuple_queue[1].qsize() > 100 :
				time.sleep( 1 )

		# logger.info('doc OUT (' + str(process_id) + ') ' + repr( nCount ) + ' [POS tagger]' )

		logger.info('process ended (' + str(process_id) + ') [POS Tagger]')

	except :
		# error result with a stack trace
		listTrace = []
		if sys.exc_info()[2] != None :
			for tupleStack in traceback.extract_tb( sys.exc_info()[2] ) :
				if tupleStack != None :
					listTrace.append( repr(tupleStack[0]) + '\t' + repr(tupleStack[1]) + '\t' + repr(tupleStack[2]) + '\t' + repr(tupleStack[3]) )
		strTrace = '\n'.join( listTrace )
		tuple_queue[2].put( 'pos_tag_tokenset_batch_worker process error : ' + repr( sys.exc_info()[0] ) + '\n' + repr( sys.exc_info()[1] ) + '\n' + strTrace )



def pos_tag_tokenset( token_set, lang, dict_common_config, timeout = 300 ) :
	"""
	POS tag a batch of tokenized sentences for a specific langauge. it is more efficient to POS tag in large batches as the POS tagger is a separate process that must be invoked using an OS exec and a Python subprocess command. there is a fixed overhead for sub-process and pipe setup time (e.g. 1-2 seconds) so processing text in bulk is more efficient than many small separate sentences.

	| note: the POS tagger used is chosen from TreeTagger, Stanford and Treebank based on language code
	| note: URL's and namespaces matching regex patterns provided in dict_common_config will get a POS tag of 'URI' or 'NAMESPACE' regardless of which POS tagger is used
	| note: tokens matching characters in dict_common_config['sent_token_seps'] will be labelled with a POS tag 'NEWLINE'

	:param list token_set: list of tokens for a set of sentences. each sentence has a token set, which is itself a list of either tokenized phrase tuples or tokenized phrase strings. e.g. [ [ ('london',),('attacks',),('are',) ... ], ... ] e.g. [ [ 'london','attacks','are', ... ], ... ]
	:param list lang_codes: list of ISO 639-1 2 character language codes (e.g. ['en','fr'])
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 
	:param int timeout: timeout in seconds for POS tagger process in the unlikely event the POS tagger hangs

	:return: list of POS tagged sentences e.g. [ [ ('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('completely', 'RB'), ('different', 'JJ') ], ... ]
	:rtype: list
	"""

	# check args without defaults
	if not isinstance( token_set, list ) :
		raise Exception( 'invalid token_set' )
	if (not isinstance( lang, str )) and (not isinstance( lang, str )) :
		raise Exception( 'invalid lang' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )
	if not isinstance( timeout, int ) :
		raise Exception( 'invalid int' )

	# POS tagger is an external EXEC unless we use the NLTK default POS tagger (good for english only!)
	listCMD = None
	strType = 'treebank'
	listNewlineChars = dict_common_config['sent_token_seps']

	# apply known sub-language mappings to primary language (e.g. uk -> ru)
	strLangBase = lang.lower()
	if strLangBase == 'uk' :
		strLangBase = 'ru'

	# get POS mapping type to use for this base language
	# OR use the default POS tagger (treebank)
	if strLangBase in dict_common_config['lang_pos_mapping'] :
		strType = dict_common_config['lang_pos_mapping'][strLangBase]

	# get command line to exec POS tagger
	if strType == 'treetagger' :
		if strLangBase == 'bg' :
			strPARFile = 'bulgarian-utf8.par'
		elif strLangBase == 'nl' :
			strPARFile = 'dutch-utf8.par'
		elif strLangBase == 'en' :
			strPARFile = 'english-utf8.par'
		elif strLangBase == 'et' :
			strPARFile = 'estonian.par'
		elif strLangBase == 'fi' :
			strPARFile = 'finnish-utf8.par'
		elif strLangBase == 'fr' :
			strPARFile = 'french.par'
		elif strLangBase == 'de' :
			strPARFile = 'german-utf8.par'
		elif strLangBase == 'it' :
			strPARFile = 'italian-utf8.par'
		elif strLangBase == 'pl' :
			strPARFile = 'polish-utf8.par'
		elif strLangBase == 'ru' :
			strPARFile = 'russian.par'
		elif strLangBase == 'sk' :
			strPARFile = 'slovak-utf8.par'
		elif strLangBase == 'es' :
			strPARFile = 'spanish-utf8.par'
		else :
			raise Exception( 'unsupported language for treetagger : ' + repr(strLangBase) )

		if sys.platform == "win32" :
			# windows
			listCMD = [
				dict_common_config['treetagger_tagger_dir'] + os.sep + 'bin' + os.sep + 'tree-tagger.exe',
				dict_common_config['treetagger_tagger_dir'] + os.sep + 'lib' + os.sep + strPARFile,
				'-token'
				]
		else :
			# linux
			listCMD = [
				dict_common_config['treetagger_tagger_dir'] + os.sep + 'bin' + os.sep + 'tree-tagger',
				dict_common_config['treetagger_tagger_dir'] + os.sep + 'lib' + os.sep + strPARFile,
				'-token'
				]

		strWorkingDir = dict_common_config['treetagger_tagger_dir']

	elif strType == 'stanford' :

		if strLangBase == 'zh' :
			strModelFile = 'models' + os.sep + 'chinese-distsim.tagger'
			strOutputFormat = 'penn'
		elif strLangBase == 'ar' :
			strModelFile = 'models' + os.sep + 'arabic.tagger'
			strOutputFormat = 'penn'
		elif strLangBase == 'en' :
			strModelFile = 'models' + os.sep + 'english-caseless-left3words-distsim.tagger'
			strOutputFormat = 'penn'
		elif strLangBase == 'fr' :
			strModelFile = 'models' + os.sep + 'french.tagger'
			strOutputFormat = 'penn'
		elif strLangBase == 'de' :
			strModelFile = 'models' + os.sep + 'german-dewac.tagger'
			strOutputFormat = 'penn'
		elif strLangBase == 'es' :
			strModelFile = 'models' + os.sep + 'spanish-distsim.tagger'
			strOutputFormat = 'penn'
		else :
			raise Exception( 'unsupported language for stanford POS : ' + repr(strLangBase) )

		# java so works for windows and linux
		listCMD = [
			'java',
			'-mx2048m',
			'-classpath',
			'stanford-postagger.jar',
			'edu.stanford.nlp.tagger.maxent.MaxentTagger',
			'-model',
			strModelFile,
			'-sentenceDelimiter',
			'null',
			'-tokenize',
			'false',
			'-outputFormat',
			'slashTags'
			]

		# TODO test other languages than english
		# language = 'english', 'polish', 'french', 'chinese', 'arabic', 'german'

		strWorkingDir = dict_common_config['stanford_tagger_dir']

	elif strType == 'treebank' :
		listCMD = None

	else :
		raise Exception( 'unknown POS tagger type : ' + strType )

	# exec command or use NLTK treebank POS
	if listCMD == None :
		# default POS is nltk Penn Treebank
		# listResult = [ [(token,pos),...], ... ]
		# e.g. [ [('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('completely', 'RB'), ('different', 'JJ')] ]
		listResult = []
		for listSentTokens in token_set :
			if len(listSentTokens) > 0 :
				if isinstance( listSentTokens[0],tuple ) :
					listSentAsString = []
					for tupleToken in listSentTokens :
						# Stanford style escape brackets so they get POS tagged correctly
						listSentAsString.append( escape_token( tupleToken[0] ) )
				else :
					listSentAsString = listSentTokens

				listPOS = nltk.pos_tag( listSentAsString )

				# micro delay to allow CPU balancing
				time.sleep( 0.001 )

				# force any tokens matching a URL or namespace to have a LINK post tag
				# and escape out the POS delimiter character to make sure serialized POS tags are not like //SYM
				for nTokenIndex in range(len(listPOS)) :
					strToken = listPOS[nTokenIndex][0]
					strPOS = listPOS[nTokenIndex][1]

					if strToken in listNewlineChars :
						strPOS = 'NEWLINE'
					else :

						listReplacementRegexName = dict_common_config['token_preservation_regex']
						for (strRegexName,strPOSTokenName) in listReplacementRegexName :
							rePattern = dict_common_config[ strRegexName ]
							if rePattern.match( strToken ) != None :
								strPOS = strPOSTokenName
								break

					listPOS[nTokenIndex] = (strToken,strPOS)

				listResult.append( listPOS )

		return listResult

	else :

		# tagger process handle
		p = None

		try :
			# create a single set of tokens to POS tag
			# but remember the sentence index so we can re-construct the tokenset afterwards
			listTokens = []
			listSentIndex = []
			nCount = 0
			for listSentTokens in token_set :
				if len(listSentTokens) > 0 :
					if isinstance( listSentTokens[0],tuple ) :
						listSentAsString = []
						for tupleToken in listSentTokens :
							listSentAsString.append( tupleToken[0] )
					else :
						listSentAsString = listSentTokens

					listTokens.extend( listSentAsString )
					nCount = nCount + len( listSentAsString )

				listSentIndex.append( nCount )

			#dict_common_config['logger'].info( 'tokens to POS = ' + str(len(listTokens)) )

			listOutputPOS = []
			if len(listTokens) > 0 :

				# treetagger OR stanford run as an external process using PIPE's
				p = subprocess.Popen( listCMD, cwd=strWorkingDir,shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )

				# read in a thread to avoid PIPE deadlocks (see popen() and all the pipe horrors for python!)
				queueBufferOut = queue.Queue()
				threadOut = threading.Thread( target = read_pipe_stdout, args=(p.stdout,queueBufferOut,len(listTokens)) )
				threadOut.setDaemon( True )
				threadOut.start()

				queueBufferErr = queue.Queue()
				threadErr = threading.Thread( target = read_pipe_stderr, args=(p.stderr,queueBufferErr) )
				threadErr.setDaemon( True )
				threadErr.start()

				bFinished = False
				nCountOut = 0
				nCountIn = 0
				dateExpire = None
				while bFinished == False :

					# do not allow a stdin and stdout differential to be more then 8192 characters, ensuring we pause before overloading stdin too much (we pipe buffers do have limits)
					if (nCountIn - nCountOut < 8192) and (nCountIn < len(listTokens)) :

						# check tagger process is still alive and there are no errors
						if p.poll() != None :
							# raise exception with the errors (process dead)
							listError = []
							while queueBufferErr.empty() == False :
								listError.append( queueBufferErr.get().strip() )
							raise Exception( 'POS failed : ' + '\n'.join( listError ) )

						elif queueBufferErr.empty() == False :
							# sleep to allow all the errors to be generated
							time.sleep(1)

							# raise exception with the errors (process alive)
							listError = []
							while queueBufferErr.empty() == False :
								listError.append( queueBufferErr.get().strip() )
							raise Exception( 'POS failed : ' + '\n'.join( listError ) )

						# send newline delimited set of tokens to the POS tagger
						strToken = listTokens[nCountIn]
						nCountIn = nCountIn + 1

						#dict_common_config['logger'].info( 'count IN = ' + str(nCountIn) )

						# has tagger process failed? no point sending data if its dead
						nErrorCode = p.poll()
						if nErrorCode != None :
							raise Exception( 'POS tagger process failed before all tokens written to pipe : ' + repr(nErrorCode) )

						# note: if we get a newline token \n or \r we will NOT get a response from the POS tagger so this special case is handled later
						if not strToken in listNewlineChars :
							# Stanford style escape brackets so they get POS tagged correctly
							strText = escape_token( strToken ) + '\n'
							p.stdin.write( strText.encode( 'utf8' ) )
							p.stdin.flush()

						else :
							# newline tokens are not sent, so do not expect it on output (and increment the out count so we match in count)
							nCountOut = nCountOut + 1

						if nCountIn == len(listTokens) :
							# close STDIN to force entire PIPE to be flushed when processing
							# if left open (e.g. for more data) some text in PIPE will sit in an internal buffer and not get processed. cannot find a solution to this - lots of effort looking
							p.stdin.close()

							# set a timeout (5 mins) after which we give up trying to read from stdout (in case of error on last token)
							dateExpire = datetime.datetime.now() + datetime.timedelta( seconds = 300 )

							#dict_common_config['logger'].info( 'STDIN finished = ' + str(nCountIn) )

					else :
						# small pause to let stdout catch up with stdin
						time.sleep(1)
						#dict_common_config['logger'].info( 'POS pause' )

					# process whatever is available on the output queue (so it does not get too large - queues over 1000 items are not a good idea as queues are limited)
					while queueBufferOut.empty() == False :
						listOutputPOS.append( queueBufferOut.get() )
						nCountOut = nCountOut + 1
						#dict_common_config['logger'].info( 'count OUT = ' + str(nCountOut) )

					# are we finished?
					if nCountOut == len(listTokens) :
						bFinished = True

					# are we timed out?
					if (dateExpire != None) and (datetime.datetime.now() > dateExpire) :
						raise Exception( 'POS tagger timeout waiting on last stdout results' )

				# read all the stderr output. there is always some non-error output there such as the words per second report. the error queue must be clear for the thread to join
				# we will discard this stderr text as it has no use for a successful outcome
				listError = []
				while queueBufferErr.empty() == False :
					listError.append( queueBufferErr.get().strip() )
				#dict_common_config['logger'].info( 'STDERR output (success) = ' + '\n'.join( listError ) )

				# wait for the read thread to terminate
				# timeout = seconds (float) worse case
				threadOut.join( timeout )
				threadErr.join( timeout )

				# ensure process has been terminated (closing STDIN should do this)
				# manually poll for timeout in case of obscure fails (e.g. PIPE problems)
				nReturnCode = None
				nTimeWait = 0.0
				while (nReturnCode != None) or (nTimeWait > timeout) :
						nReturnCode = p.poll()
						if nReturnCode == None :
							nTimeWait = nTimeWait + 1.0
							thread.sleep(1)
				if nTimeWait > timeout :
					raise Exception( 'POS tagger timeout waiting for response : ' + repr(listTokens) )

				# micro delay to allow CPU balancing
				time.sleep( 0.001 )


			# parse result and reconstruct the token set
			# tagger result = term \t pos \n
			listResult = []
			nCount = 0
			nIndexPos = 0
			for listSentTokens in token_set :

				listTaggedSent = []

				for nIndexOriginal in range(len(listSentTokens)) :

					if not listSentTokens[nIndexOriginal] in listNewlineChars :

						# get next POS
						strPOS = listOutputPOS[nIndexPos]
						nIndexPos = nIndexPos + 1

						# parse tagger result
						# treetagger is <original_token><tab><pos>
						# stanford is <original_token>_<pos>
						# note: stanford POS tagger does not always return the original token when token has a space in it.
						#       usually this cannot happen, but space characters might be introduced if a custom POS token replacement is used i.e. dict_common_config['token_preservation_regex']
						#       the stanford POS tagger has some sort of numeric processing when spaces appear with numbers in tokens e.g. 'Fig. 99' -> ('Fig._NN','99_CD') so use the original token later NOT the return token in output
						if strType == 'treetagger' :
							listPOS = strPOS.strip().rsplit('\t',1)
						else :
							listPOS = strPOS.strip().rsplit('_',1)

						if len(listPOS) != 2 :
							raise Exception( 'POS failed : ' + repr(strPOS) )
						else :

							# force any tokens matching a URL or namespace to have a LINK post tag
							# and escape out the POS delimiter character to make sure serialized POS tags are not like //SYM
							strToken = listSentTokens[nIndexOriginal]
							strPOS = listPOS[1]

							if strToken in listNewlineChars :
								strPOS = 'NEWLINE'
							else :

								listReplacementRegexName = dict_common_config['token_preservation_regex']
								for (strRegexName,strPOSTokenName) in listReplacementRegexName :
									rePattern = dict_common_config[ strRegexName ]
									if rePattern.match( strToken ) != None :
										strPOS = strPOSTokenName
										break

							listPOS = (strToken,strPOS)

							# add tuple to token set
							listTaggedSent.append( tuple(listPOS) )

					else :
						# add newline chat in without expecting a POS tag
						# label newlines as NEWLINE
						listTaggedSent.append( ( listSentTokens[nIndexOriginal],'NEWLINE' ) )

				# add POS tagged set even if its empty (e.g. emoty string)
				listResult.append( listTaggedSent )

			return listResult
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


def read_pipe_stdout( pipe_handle, queue_buffer, lines_expected = 1 ) :
	"""
	internal POS tagger process pipe callback function

	:param file file_handle: pipe handle to POS tagger output
	:param Queue.Queue() queue_buffer: queue where pipe output can be stored
	:param int lines_expected: number of lines expected so we do not read other sentences from pipe
	"""

	try :

		nCount = 0
		while nCount < lines_expected :
			# read UTF-8 data from TreeTagger
			strLine = pipe_handle.readline().decode( 'utf-8' )
			if len(strLine) > 0 :
				queue_buffer.put( strLine )
				nCount = nCount + 1
			else :
				return
	except :
		# PIPE work should be hard to fail
		return

def read_pipe_stderr( pipe_handle, queue_buffer ) :
	"""
	internal POS tagger process pipe callback function

	:param file file_handle: pipe handle to POS tagger errors
	:param Queue.Queue() queue_buffer: queue where pipe errors can be stored
	"""
	try :
		strLine = pipe_handle.read()
		if len(strLine) > 0 :
			queue_buffer.put( strLine )
	except :
		# PIPE work should be hard to fail
		return

def create_sent_trees( list_pos, list_sent_addr_offsets = None, dict_common_config = None ) :
	"""
	create a set of nltk.Tree structures for sentences. sent delimiter characters are taken from dict_common_config['sent_token_seps'] and the period character

	:param list list_pos: POS tagged sentence e.g. [ ('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('completely', 'RB'), ('different', 'JJ') ]
	:param list list_sent_addr_offsets: list which (if not None) will be populated with the start address of each sent (address within the original POS tagged sent)
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: list of nltk.Tree sentence structures e.g. [ nltk.Tree(S And/CC now/RB for/IN something/NN completely/RB different/JJ), ... ]
	:rtype: list
	"""

	if not isinstance( list_pos, list ) :
		raise Exception( 'invalid list_pos' )
	if not isinstance( list_sent_addr_offsets, (list,type(None)) ) :
		raise Exception( 'invalid list_sent_addr_offsets' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	listSentSep = dict_common_config['sent_token_seps']

	# replace bracket chars in POS tag list
	listPOS = copy.deepcopy( list_pos )

	listTrees = []
	nIndexLast = 0
	nIndexTarget = 0
	while( nIndexTarget < len(listPOS) ) :
		if listPOS[nIndexTarget][0] in listSentSep :
			# make a sent unless its a single . character
			if nIndexTarget != nIndexLast :

				# make a tree from POS
				strPOSSerialized = serialize_tagged_list(
					listPOS[ nIndexLast:nIndexTarget ],
					dict_common_config = dict_common_config,
					serialization_style = 'tree' )

				strTreeSerialized = '(S ' + strPOSSerialized + ')'
				treeObj = parse_serialized_tagged_tree( strTreeSerialized, dict_common_config = dict_common_config )
				listTrees.append( treeObj )
				if list_sent_addr_offsets != None :
					list_sent_addr_offsets.append( nIndexLast )

			nIndexLast = nIndexTarget + 1
		nIndexTarget = nIndexTarget + 1
	
	if (nIndexLast < nIndexTarget) and (nIndexLast < len(listPOS)) :
		# make a tree from POS
		strPOSSerialized = serialize_tagged_list(
			listPOS[ nIndexLast: ],
			dict_common_config = dict_common_config,
			serialization_style = 'tree' )

		strTreeSerialized = '(S ' + strPOSSerialized + ')'
		treeObj = parse_serialized_tagged_tree( strTreeSerialized, dict_common_config = dict_common_config )
		listTrees.append( treeObj )
		if list_sent_addr_offsets != None :
			list_sent_addr_offsets.append( nIndexLast )

	return listTrees

def serialize_tagged_list( list_pos, dict_common_config, serialization_style = 'pos' ) :
	"""
	serialize POS tagged tokens (list)
	| note: the POS separator (e.g. '/') is replaced in all tokens and POS tags so it is always good for a separator in the serialization

	:param list list_pos: POS tagged sentence e.g. [ ('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('completely', 'RB'), ('different', 'JJ') ]
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 
	:param str serialization_style: either POS tag list style (pos) or sentence tree style (tree). pos style is 'and/CC now/RB ...'. tree style is '(CC and) (RB now) ...'

	:return: serialized POS tagged sentence in style requested e.g. 'new/NN york/NN' 
	:rtype: unicode
	"""

	if not isinstance( list_pos, list ) :
		raise Exception( 'invalid list_pos' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	strPOSsep = dict_common_config['pos_sep'][0]
	strPOSreplacement = dict_common_config['pos_sep'][1]

	# replace bracket chars in POS tag list
	listPOS = copy.deepcopy( list_pos )
	for nIndexPOS in range(len(listPOS)) :
		if not isinstance( listPOS[nIndexPOS], tuple ) :
			raise Exception( 'list_pos member not a tuple : ' + repr(type(listPOS[nIndexPOS])) )
		listPOS[nIndexPOS] = escape_tagged_token( listPOS[nIndexPOS] )

	listSerialized = []
	for nIndex in range(len(listPOS)) :
		strToken = listPOS[nIndex][0]
		strPOS = listPOS[nIndex][1]
		if serialization_style == 'pos' :
			# replace / character as is used to indicate a POS tag
			strToken = strToken.replace( strPOSsep,strPOSreplacement )
			strPOS = strPOS.replace( strPOSsep,strPOSreplacement )

			if nIndex == 0 :
				listSerialized.extend( [strToken,strPOSsep,strPOS] )
			else :
				listSerialized.extend( [' ',strToken,strPOSsep,strPOS] )
		elif serialization_style == 'tree' :
			if nIndex == 0 :
				listSerialized.extend( ['(',strPOS,' ',strToken,')'] )
			else :
				listSerialized.extend( [' (',strPOS,' ',strToken,')'] )
		elif serialization_style == 'token' :
			# just return tokens
			if nIndex == 0 :
				listSerialized.extend( [strToken] )
			else :
				listSerialized.extend( [' ',strToken] )
		else :
			raise Exception( 'unknown serialization style : ' + str(serialization_style) )

	# return serialized list
	# note: spaces already in list at right places
	return ''.join( listSerialized )

def serialize_tagged_tree( tree_sent, dict_common_config ) :
	"""
	serialize POS tagged tokens (tree). this function will go recursive if the tree has one or more subtrees.
	| note: all tokens are escaped using escape_token()

	:param nltk.Tree tree_sent: POS tagged sentence e.g. (S And/CC now/RB for/IN something/NN completely/RB different/JJ) or (S (CC And) (RB now) ... )
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: serialized POS tagged sentence e.g. '(S new/NN york/NN -LRB-man-made location-RRB-/PARENTHETICAL_MATERIAL)' or '(S (NP New) (NP York) (PARENTHETICAL_MATERIAL -LRB-man-made location-RRB-))'
	:rtype: unicode
	"""

	if not isinstance( tree_sent, nltk.tree.Tree ) :
		raise Exception( 'invalid tree_sent')
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	strSerialized = '(' + escape_token( tree_sent.label() )
	listPOS = []
	for leaf in tree_sent :
		if isinstance( leaf, nltk.tree.Tree ) :
			if len(listPOS) > 0 :
				strSerialized = strSerialized + ' ' + ' '.join( listPOS )
				listPOS = []
			strSerialized = strSerialized + ' ' + serialize_tagged_tree( leaf, dict_common_config )
		else :
			# note: POS is already in serialized form e.g. 'London/NP' or '(NP London)' or for label 'PARENTHETICAL_MATERIAL' leaf might be '(any stuff we like)'
			# so escape the string for safe serialization
			#if (len(leaf) > 2) and (leaf[0] == '(') and (leaf[-1] == ')') :
			#	listPOS.append( '(' + escape_token( leaf[1:-1] ) + ')' )
			#else :
			listPOS.append( escape_token( leaf ) )
	if len(listPOS) > 0 :
		strSerialized = strSerialized + ' ' + ' '.join( listPOS )
	strSerialized = strSerialized + ')'

	# escape all tokens so the tree in string is safe to parse back in (i.e. brackets are escaped)
	return strSerialized

def parse_serialized_tagged_tree( serialized_tree, dict_common_config ) :
	"""
	parse a previously serialized tree
	| note: tokens unescaped using replacement characters defined in list_escape_tuples

	:param unicode serialized_tree: serialized tree structure containing POS tagged leafs from common_parse_lib.serialize_tagged_tree()
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: tree representing POS tagged sentence e.g. (S And/CC now/RB for/IN something/NN completely/RB different/JJ)
	:rtype: nltk.Tree
	"""

	if not isinstance( serialized_tree, str) :
		raise Exception( 'invalid serialized_tree')
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	# leaf = tree children (e.g. (CAT_INDEX Cat. No.).
	# there might be any characters after the POS tag (inc whitespace). make sure leaf match is preceeded by a non bracket character and a space.
	reLeaf = r'(?<=[^()] )[^()]*'
	listBrackets = '()'

	# use NLTK parse function with this custom regex
	treeSent = nltk.Tree.fromstring( serialized_tree, brackets=listBrackets, node_pattern=None, leaf_pattern=reLeaf )

	# unescape all tokens so the tree in memory has the original tokens
	unescape_tree( treeSent )

	# all done
	return treeSent

def flattern_sent( tree_sent, dict_common_config ) :
	"""
	flatten a sent so it has no subtrees. subtrees are flattened to make phrases.
	this is useful for subsequent processing that requires a tagged list, such as dependency parsing

	:param nltk.Tree tree_sent: sentence tree with any number of subtrees (S (CC And) (RB now) (VP (NP New) (NP York)) ... )
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:return: flattened sent tree with phrases for subtrees e.g. (S (CC And) (RB now) (VP New York) ... )
	:rtype: nltk.Tree
	"""

	if not isinstance( tree_sent, nltk.tree.Tree ) :
		raise Exception( 'invalid tree_sent')
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'invalid dict_common_config' )

	if tree_sent.label() != 'S' :
		raise Exception( 'tree_sent does not start with a S root' )

	treeResult = copy.deepcopy( tree_sent )

	# replace all child trees with a flat version
	for nChildIndex in range(len(treeResult)) :
		if isinstance( treeResult[nChildIndex], nltk.Tree ) :
			# concat leaf tokens into a single phrase
			treeResult[nChildIndex] = nltk.Tree(
				treeResult[nChildIndex].label(),
				[ ' '.join( treeResult[nChildIndex].leaves() ) ]
				)
		else :
			raise Exception( 'sent child not a tree - invalid sent structure' )

	# all done
	return treeResult

def flattern_tree_with_heads( tree ) :
	"""
	flattern a nltk.Tree preserving the head node, so all tokens are returned (unlike nltk.Tree.leaves()).

	:param nltk.Tree tree: tree to flatten

	:return: list of tokens under tree, including the head
	:rtype: list
	"""
	listResult = []
	if isinstance( tree, nltk.Tree ) :
		listResult.append( tree.label() )
		for child in tree :
			listResult.extend( flattern_tree_with_heads( child ) )
	else :
		listResult.append( str( tree ) )
	return listResult

def escape_tagged_token( tuple_pos ) :
	"""
	escape open and close brackets in a POS token to make it nltk.Tree safe

	:param tuple tuple_pos: tuple of tagged POS entry = (token, pos)

	:return: escaped POS token = (token, pos)
	:rtype: tuple
	"""

	listEntry = []
	listEntry.append( escape_token( tuple_pos[0] ) )
	listEntry.append( escape_token( tuple_pos[1] ) )
	return tuple( listEntry )

def unescape_tagged_token( tuple_pos ) :
	"""
	unescape open and close brackets in a POS token

	:param tuple tuple_pos: tuple of tagged POS entry = (token, pos)

	:return: unescaped POS token = (token, pos)
	:rtype: tuple
	"""

	listEntry = []
	listEntry.append( unescape_token( tuple_pos[0] ) )
	listEntry.append( unescape_token( tuple_pos[1] ) )
	return tuple( listEntry )

def escape_token( token_str ) :
	"""
	escape open and close brackets in a token to make it nltk.Tree safe

	:param unicode token_str: token text to process

	:return: unescaped text
	:rtype: unicode
	"""

	strText = token_str
	for tupleReplacement in list_escape_tuples :
		strText = strText.replace( tupleReplacement[0], tupleReplacement[1] )
	return strText

def unescape_token( token_str ) :
	"""
	unescape open and close brackets in a token

	:param unicode token_str: token text to process

	:return: unescaped text
	:rtype: unicode
	"""

	strText = token_str
	for tupleReplacement in list_escape_tuples :
		strText = strText.replace( tupleReplacement[1], tupleReplacement[0] )
	return strText

def unescape_tree( tree, depth = 0 ) :
	"""
	unescape a nltk.Tree open and close brackets

	:param nltk.Tree tree: tree to process
	:param int depth: recursion depth (internal variable)

	:return: unescaped tree
	:rtype: nltk.Tree
	"""

	if depth > 50 :
		raise Exception( 'tree recursion depth too large (50 deep) : ' + repr(tree) )

	for nIndex in range(len(tree)) :
		if isinstance( tree[nIndex], nltk.Tree ) :
			unescape_tree( tree[nIndex], depth = depth + 1 )
		elif isinstance( tree[nIndex], str ) :
			tree[nIndex] = unescape_token( tree[nIndex] )
		else :
			raise Exception( 'tree leaf unknown type : ' + repr(type(tree[nIndex])) )


'''

def extract_matches( list_pos, pattern_dict, list_linguistic_labels, dict_common_config = None ) :
	"""
	extract entity patterns from a set of regex patterns operating applied to POS tagged text
	return all matches
	RELIC

	:param list list_pos: tagged sent = [ (t1,p1),(t2,p2), ... ]
	:param dict pattern_dict: dict pattern for relationships = { 'pattern_type' : [ ( NE_type, ... ) | None, ( NE_type, ... ) | None, RegexObject,re.IGNORECASE | re.UNICODE | ... ] }
	:param dict list_linguistic_labels: list of lingistic labels so they can be differntiated from POS labels in sent trees (e.g. SOURCE)
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:returns : dict of rel types. each rel type entry is itself a dict of regex named group data { match_type : [ match1, match2 ... ] }. rel dict entry will be {} if regex does not have any named groups. the actual text returned is entirely dependant on the regex pattern.
	:rtype : dict
	"""

	if not isinstance( pattern_dict, dict ) :
		raise Exception( 'pattern_dict not a dict' )
	if not isinstance( list_linguistic_labels, list ) :
		raise Exception( 'list_linguistic_labels not a list' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'dict_common_config not a dict' )
	if not isinstance( list_pos, list ) :
		raise Exception( 'list_pos not a list' )

	# get a list of all sents (there might be a few if newline delimiter is present in text) in this text
	listTrees = create_sent_trees( list_pos, dict_common_config = dict_common_config )

	# run patterns on all sent trees
	# listMatch = [(strMatch,nPosMatchStart,nPosMatchEnd,strGroupName ), ...]
	# listSentMatches = [ listMatch, ... ]
	listSentMatches = match_linguistic_patterns(
		list_sent_trees = listTrees,
		pattern_dict = pattern_dict,
		dict_common_config = dict_common_config )

	#dict_common_config['logger'].info('LIST_MATCH = ' + repr( listSentMatches ) )

	# apply sent match results to sent tree to make a linguistically annotated tree for each sent
	# this will handle match subsumption and overlaps
	listSentTreesAnnotated = annotate_sent_with_pattern_matches(
		list_sent_trees = listTrees,
		list_sent_matches = listSentMatches,
		dict_common_config = dict_common_config
		)

	#dict_common_config['logger'].info('LIST_TREE = ' + repr( listSentTreesAnnotated ) )

	# provide an aggregated list of top level match entities that have been identified in all the sents
	dictMatches = {}
	for treeSent in listSentTreesAnnotated :

		#dict_common_config['logger'].info('SENT = ' + repr( u' '.join( treeSent.leaves() ) ) )
		#dict_common_config['logger'].info('TREE = ' + serialize_tagged_tree( treeSent, dict_common_config = dict_common_config ) )

		walk_evidence_tree( treeSent, list_linguistic_labels, dict_common_config = dict_common_config, dict_matches = dictMatches )

	return dictMatches


def walk_evidence_tree( tree_sent, list_linguistic_labels, dict_common_config = None, dict_matches = {} ) :
	"""
	walk sent tree for looking for known evidence labels. the tree will be recursively walked.
	RELIC

	:param nltk.Tree tree_sent: NLTK tree for sent annotated with POS tags and linguistic labels
	:param dict dict_matches: match results (data in this dict will be changed by recursive calls to this function)
	:param dict list_linguistic_labels: list of lingistic labels so they can be differntiated from POS labels in sent trees (e.g. SOURCE)
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:returns : dict of rel types. each rel type entry is itself a dict of regex named group data { match_type : [ match1, match2 ... ] }. rel dict entry will be {} if regex does not have any named groups. the actual text returned is entirely dependant on the regex pattern.
	:rtype : dict
	"""

	# debug
	#dict_common_config['logger'].info('TREE = ' + common_parse_lib.serialize_tagged_tree( tree_sent, dict_common_config = dict_common_config ) )

	for leaf in tree_sent :

		if isinstance( leaf, nltk.tree.Tree ) :

			# check entity type is a linguistic entity and not a POS label
			strEntityType = leaf.label()
			if strEntityType in list_linguistic_labels :

				# serialized text without POS tags
				strEntity = ' '.join( leaf.leaves() )

				# DEBUG
				#dict_common_config['logger'].info('SENT = ' + repr( u' '.join( tree_sent.leaves() ) ) )
				#dict_common_config['logger'].info('TREE = ' + serialize_tagged_tree( tree_sent, dict_common_config = dict_common_config ) )
				#dict_common_config['logger'].info('TYPE = ' + repr(strEntityType) )
				#dict_common_config['logger'].info('MATCH = ' + repr(strEntity) )

				# add entity to match list
				if not strEntityType in dict_matches :
					dict_matches[ strEntityType ] = []
				dict_matches[ strEntityType ].append( strEntity )
			
			# recurse into tree to see if we have sub-labels to find
			walk_evidence_tree( leaf, list_linguistic_labels, dict_common_config, dict_matches )


def match_linguistic_patterns( list_sent_trees, pattern_dict, dict_common_config = None ) :
	"""
	for each sent tree execute a provided set of regex patterns to extract linguistic patterns.
	return all matches ready for sent annotation
	RELIC

	:param list list_sent_trees: list of sent trees to process = [nltk.Tree, ...]
	:param dict pattern_dict: dict pattern = { 'pattern_type' : [ RegexObject, ... }
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:returns : list of pattern matches for each sent = [ [ ( matched text, start index in original text, end index in original text, LINGUISTIC_LABEL, PATTERN_TYPE ), ... ], ... ]. length of this list == length of list_sent_trees
	:rtype : list
	"""

	if not isinstance( pattern_dict, dict ) :
		raise Exception( 'pattern_dict not a dict' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'dict_common_config not a dict' )
	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'list_sent_trees not a list' )

	# label entities within each sent
	listResultSet = []
	for nTreeIndex in range(len(list_sent_trees)) :

		treeObj = list_sent_trees[ nTreeIndex ]
		if not isinstance( treeObj, nltk.Tree ) :
			raise Exception( 'sent tree index ' + str(nTreeIndex) + ' not a nltk.Tree object : ' + str(type(treeObj)) )

		# debug
		#dict_common_config['logger'].info('TREE = ' + repr( treeObj ) )

		strTree = serialize_tagged_tree( treeObj, dict_common_config )

		# debug
		#dict_common_config['logger'].info('TREE_STR = ' + repr( strTree ) )

		# apply regex removing matches from text as we go to avoid duplicate matches
		listResult = []
		for strPatternName in pattern_dict :

			# each pattern type gets a fresh copy of the text to try to match against
			strTextToMatch = copy.deepcopy( strTree )

			# loop sequentially on patterns so most permissive patterns can be put last
			for rePattern in pattern_dict[ strPatternName ] :

				# nothing to do?
				#if len(strTextToMatch) == 0 :
				#	break;

				bOK = True
				while bOK == True :
					matchObj = rePattern.match( strTextToMatch )
					if matchObj == None :
						bOK = False
					else :
						# get all named matches from this pattern
						# if a named match is optional it might have a None value
						for strGroupName in matchObj.groupdict() :

							strMatch = matchObj.group( strGroupName )
							if strMatch != None :

								# replace matched text with filler characters to avoid it matching again (do not delete it as you might artifically create a new viable text from fragments)
								# unichr( 0xFFFF ) = unicode noncharacter
								# not providing any POS tag with the noncharacter sequence will (a) keep the length of the text identical and (b) make it very likely no further matches will occur with this removed text

								nPosMatchStart = matchObj.start( strGroupName )
								nPosMatchEnd = matchObj.end( strGroupName )
								nSize = (nPosMatchEnd - nPosMatchStart) + 1

								# need a replacement that will not match BUT will not prevent other matches, so keep the sent structure
								if nSize > 4 :
									strReplacement = '(- ' + '-'*(nSize-4) + ')'
								else :
									raise Exception( 'text match < 5 characters (invalid sent tree?) : ' + repr(strTree) )

								strTextToMatch = strTextToMatch[:nPosMatchStart] + strReplacement + strTextToMatch[nPosMatchEnd+1:]

								# add match to result
								listResult.append( (strMatch, nPosMatchStart, nPosMatchEnd, strGroupName, strPatternName ) )

								# debug
								#dict_common_config['logger'].info('PATTERN ' + strPatternName + ' = ' + rePattern.pattern )
								#dict_common_config['logger'].info('TREE_STR = ' + repr( strTree ) )
								#dict_common_config['logger'].info('MATCHED = ' + repr(strMatch) )
								#dict_common_config['logger'].info('RESULT = ' + repr((nPosMatchStart,nPosMatchEnd,strGroupName )) )
								#dict_common_config['logger'].info('TEXT LEFT = ' + repr(strTextToMatch) )

		listResultSet.append( listResult )

	# return list of linguistic patterns found in each sent ([] if none)
	return listResultSet

def annotate_sent_with_pattern_matches( list_sent_trees, list_sent_matches, dict_common_config = None ) :
	"""
	process a set of sent patterns and create sent annotations as nltk.Tree entries
	provided heuristics to handle conflicts where annotations apply to the same (or partially overlapping) tokens:
		*first process matches that are completely subsumed by other matches. subsumed matched will appear as subtrees
		*second resolve matches with identical tokens (choose first match option in list)
		*third resolve matches that overlap but do not subsume (choose left-most match in text)
		*remove void matches
	return a set of sent trees with sub-trees for all matches provided
	RELIC

	:param list list_sent_trees: list of sent trees to process = [nltk.Tree, ...]
	:param list list_sent_matches: list of matches for each sent from common_parse_lib.match_linguistic_patterns()
	:param dict dict_common_config: config object returned from common_parse_lib.get_common_config() 

	:returns : list of sent trees with known entities labelled as sub-trees = [nltk.Tree ...]
	:rtype : list
	"""

	if not isinstance( list_sent_trees, list ) :
		raise Exception( 'list_sent_trees not a list' )
	if not isinstance( dict_common_config, dict ) :
		raise Exception( 'dict_common_config not a dict' )
	if not isinstance( list_sent_matches, list ) :
		raise Exception( 'list_sent_matches not a list' )

	listAnnotatedSentTrees = []

	# label entities within each sent
	for nTreeIndex in range(len(list_sent_trees)) :

		treeObj = list_sent_trees[ nTreeIndex ]
		if not isinstance( treeObj, nltk.Tree ) :
			raise Exception( 'sent tree index ' + str(nTreeIndex) + ' not a nltk.Tree object : ' + str(type(treeObj)) )
		listMatches = copy.deepcopy( list_sent_matches[ nTreeIndex ] )

		# create a serialized sent e.g. (S (CD 12) (PM Ronin))
		strTree = serialize_tagged_tree( treeObj, dict_common_config )

		# handle conflicts of matches sharing identical text
		# (a) process matches that are completely subsumed by other matches first
		# (b) resolve matches with identical text (simply choose first match option)
		# (c) resolve matches that overlap but do not subsume (simply choose left-most match in text)
		# remove matches and order list as per above (without actually changing text yet)
		# match = ( matched text, start index in original text, end index in original text, LINGUISTIC_LABEL )

		#listMatches = sorted( listMatches, key=lambda entry: entry[1], reverse=True )

		#dict_common_config['logger'].info( 'MATCHES1 ' + repr(listMatches) )

		# identical token check
		for nIndexMatch1 in range(len(listMatches)) :
			if listMatches[nIndexMatch1] != None :

				nPosMatchStart1 = listMatches[nIndexMatch1][1]
				nPosMatchEnd1 = listMatches[nIndexMatch1][2]

				for nIndexMatch2 in range(nIndexMatch1+1,len(listMatches)) :
					if listMatches[nIndexMatch2] != None :

						nPosMatchStart2 = listMatches[nIndexMatch2][1]
						nPosMatchEnd2 = listMatches[nIndexMatch2][2]

						# remove identical matches (keeping the first to appear in the list)
						if (nPosMatchStart2 == nPosMatchStart1) and (nPosMatchEnd2 == nPosMatchEnd1) :
							listMatches[nIndexMatch2] = None
							#dict_common_config['logger'].info( 'PRUNE identical ' + repr(nIndexMatch2) )

		#dict_common_config['logger'].info( 'MATCHES2 ' + repr(listMatches) )

		# subsumption of token check
		nIndexMatch1 = 0
		while nIndexMatch1 < len(listMatches) :
			if listMatches[nIndexMatch1] != None :

				nPosMatchStart1 = listMatches[nIndexMatch1][1]
				nPosMatchEnd1 = listMatches[nIndexMatch1][2]

				nIndexMatch2 = nIndexMatch1 + 1
				while nIndexMatch2 < len(listMatches) :
					if listMatches[nIndexMatch2] != None :

						nPosMatchStart2 = listMatches[nIndexMatch2][1]
						nPosMatchEnd2 = listMatches[nIndexMatch2][2]

						# subsumption - check if match 2 is subsumed by match 1
						if (nPosMatchStart2 >= nPosMatchStart1) and (nPosMatchEnd2 <= nPosMatchEnd1) :
							# swap position so subsumed match comes first
							entryTemp = listMatches[nIndexMatch2]
							listMatches[nIndexMatch2] = listMatches[nIndexMatch1]
							listMatches[nIndexMatch1] = entryTemp

							#dict_common_config['logger'].info( 'SWAP ' + repr( (nIndexMatch1,nIndexMatch2) ) )

							# recheck this position using the new match
							break

						# subsumption - check if match 1 is subsumed by match 2
						elif (nPosMatchStart1 >= nPosMatchStart2) and (nPosMatchEnd1 <= nPosMatchEnd2) :
							# subsumption but in right order - dont check for overlaps
							#dict_common_config['logger'].info( 'SUBSUMPTION NOOP ' + repr( (nIndexMatch1,nIndexMatch2) ) )
							pass

						# overlap check (keep the first to appear in the list) - no need to consider subsumption as its checked previously
						elif ((nPosMatchStart2 < nPosMatchStart1) and (nPosMatchEnd2 >= nPosMatchStart1)) or ((nPosMatchStart2 <= nPosMatchEnd1) and (nPosMatchEnd2 > nPosMatchEnd1)) :
							listMatches[nIndexMatch2] = None
							#dict_common_config['logger'].info( 'PRUNE overlap ' + repr( (nIndexMatch1,nIndexMatch2) ) )

					# increment
					nIndexMatch2 = nIndexMatch2 + 1

			# increment
			nIndexMatch1 = nIndexMatch1 + 1

		#dict_common_config['logger'].info( 'MATCHES3 ' + repr(listMatches) )

		# prune matches
		nIndexMatch1 = 0
		while nIndexMatch1 < len(listMatches) :
			if listMatches[nIndexMatch1] == None :
				listMatches.pop(nIndexMatch1)
			else :
				nIndexMatch1 = nIndexMatch1 + 1

		#dict_common_config['logger'].info( 'MATCHES4 ' + repr(listMatches) )
		#dict_common_config['logger'].info( 'TREE1 ' + repr(strTree) )

		# loop on each match and replace matched POS tagged text with a tree structure representing the entity
		# change all text position offsets when we make these changes so the next set of matches are inserted in the correct position
		for nIndexMatch1 in range(len(listMatches)) :

			tupleMatch = listMatches[nIndexMatch1]
			nPosMatchStart1 = tupleMatch[1]
			nPosMatchEnd1 = tupleMatch[2]
			strEntityType = tupleMatch[3]

			# note: compute match text again we might get embedded matches within it
			strMatch = strTree[nPosMatchStart1:nPosMatchEnd1]

			# debug
			#dict_common_config['logger'].info('T1 = ' + repr((strMatch,nPosMatchStart1,nPosMatchEnd1,strEntityType )) )
			#dict_common_config['logger'].info('T2 = ' + repr(strTree) )
			#dict_common_config['logger'].info('T3 = ' + repr(strTree[:nPosMatchStart1]) )
			#dict_common_config['logger'].info('T4 = ' + repr(strTree[nPosMatchEnd1:]) )

			strTree = '{:s}({:s} {:s}){:s}'.format(
				strTree[:nPosMatchStart1],
				strEntityType,
				strMatch,
				strTree[nPosMatchEnd1:] )

			nExtraCharacters = 3 + len(strEntityType)
			for nIndexMatch2 in range(nIndexMatch1+1,len(listMatches)) :
				nPosMatchStart2 = listMatches[nIndexMatch2][1]
				nPosMatchEnd2 = listMatches[nIndexMatch2][2]
				# no overlap (i.e. subsumption as we delete overlaps earlier), offset both start and end character index
				if nPosMatchStart2 > nPosMatchEnd1 :
					tupleMatchEntry = (
						listMatches[nIndexMatch2][0],
						listMatches[nIndexMatch2][1] + nExtraCharacters,
						listMatches[nIndexMatch2][2] + nExtraCharacters,
						listMatches[nIndexMatch2][3] )
					listMatches[nIndexMatch2] = tupleMatchEntry
				# overlap (i.e. subsumption as we delete overlaps earlier), offset end character index
				elif nPosMatchEnd2 >= nPosMatchStart1 :
					tupleMatchEntry = (
						listMatches[nIndexMatch2][0],
						listMatches[nIndexMatch2][1],
						listMatches[nIndexMatch2][2] + nExtraCharacters,
						listMatches[nIndexMatch2][3] )
					listMatches[nIndexMatch2] = tupleMatchEntry


		#dict_common_config['logger'].info( 'MATCHES6 ' + repr(listMatches) )
		#dict_common_config['logger'].info( 'TREE2 ' + repr(strTree) )
		#if 'Fashionista_com' in strTree :
		#	sys.exit()

		# parse the next tree text to make a NLTK tree structure
		treeSent = parse_serialized_tagged_tree( strTree, dict_common_config = dict_common_config )

		#dict_common_config['logger'].info( 'TREE3 ' + repr(treeSent) )

		# add to output list
		listAnnotatedSentTrees.append( treeSent )

	# return list of NLTK trees for this tagged text with the linguistic annotations inserted as subtrees
	return listAnnotatedSentTrees

'''
