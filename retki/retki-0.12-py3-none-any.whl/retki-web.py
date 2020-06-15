# Suomilog
# Copyright (C) 2018 Iikka Hauhio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import re
import itertools
from copy import deepcopy
from collections import defaultdict

class Token:
	def __init__(self, token, alternatives):
		self.token = token
		self.alternatives = alternatives
	def __repr__(self):
		return "Token(" + repr(self.token) + ", " + repr(self.alternatives) + ")"
	def __str__(self):
		return self.token + "[" + "/".join([baseform + "{" + ", ".join(bits) + "}" for baseform, bits in self.alternatives]) + "]"
	def toCode(self):
		return self.token or "/".join([baseform + "{" + ",".join(bits) + "}" for baseform, bits in self.alternatives])
	def containsMatch(self, alternatives):
		return any([any([tbf == baseform and tbits >= bits for tbf, tbits in self.alternatives]) for baseform, bits in alternatives])
	def baseform(self, *tbits):
		tbits = set(tbits)
		for baseform, bits in self.alternatives:
			if tbits <= bits:
				return baseform
		return None
	def bits(self):
		bits = set()
		for _, b in self.alternatives:
			bits.update(b)
		return bits

class PatternRef:
	def __init__(self, name, bits):
		self.name = name
		self.bits = bits
	def __repr__(self):
		return "PatternRef(" + repr(self.name) + ", " + repr(self.bits) + ")"
	def toCode(self):
		return "." + self.name + ("{" + ",".join(self.bits) + "}" if self.bits else "")

class MultiOutput:
	def __init__(self, outputs):
		self.outputs = outputs
	def __repr__(self):
		return "MultiOutput(" + repr(self.outputs) + ")"
	def eval(self, args):
		ans = []
		for i, output in enumerate(self.outputs):
			ans.append(output.eval([arg[i] for arg in args]))
		return ans

class StringOutput:
	def __init__(self, string):
		self.string = string
	def __repr__(self):
		return "StringOutput(" + repr(self.string) + ")"
	def eval(self, args):
		ans = self.string
		for i, a in enumerate(args):
			var = "$"+str(i+1)
			if var not in ans:
				ans = ans.replace("$*", ",".join(args[i:]))
				break
			ans = ans.replace(var, a)
		return ans

class Grammar:
	def __init__(self, patterns=None, names=None):
		self.patterns = patterns or {}
		self.names = names or {}
	def print(self):
		for category in sorted(self.patterns):
			print(category, "::=")
			for pattern in self.patterns[category]:
				print(" " + pattern.toCode())
	def copy(self):
		return Grammar({name: self.patterns[name].copy() for name in self.patterns}, self.names.copy())
	def matchAll(self, tokens, category, bits):
		if category not in self.patterns:
			return []
		
		ans = []
		for pattern in self.patterns[category]:
			ans += pattern.match(self, tokens, bits)
		
		return ans
	def allowsEmptyContent(self, category):
		if category not in self.patterns:
			return False
		return any([pattern.allowsEmptyContent() for pattern in self.patterns[category]])
	def addCategoryName(self, category, name):
		self.names[category] = name
	def refToString(self, ref):
		if ref.name in self.names:
			name = self.names[ref.name]
		else:
			name = ref.name
		if ref.bits:
			name += " (" + ",".join(ref.bits) + ")"
		return name
	def parseGrammarLine(self, line, *outputs):
		if debug_level >= 1:
			print(line)
		tokens = line.replace("\t", " ").split(" ")
		if len(tokens) > 2 and tokens[1] == "::=" and (outputs or "->" in tokens):
			end = tokens.index("->") if "->" in tokens else len(tokens)
			category = tokens[0][1:]
			words = []
			for token in tokens[2:end]:
				if "{" in token and token[-1] == "}":
					bits = set(token[token.index("{")+1:-1].split(","))
					token = token[:token.index("{")]
				else:
					bits = set()
				if token == "":
					continue
				elif token == ".":
					words.append(Token(".", []))
				elif token[0] == ".":
					words.append(PatternRef(token[1:], bits))
				elif bits:
					words.append(Token("", [(token, bits)]))
				else:
					words.append(Token(token, []))
			if category not in self.patterns:
				self.patterns[category] = []
			if "->" in tokens:
				outputs = outputs + (StringOutput(" ".join(tokens[end+1:])),)
			pattern = Pattern(category, words, MultiOutput(outputs) if len(outputs) > 1 else outputs[0])
			self.patterns[category].append(pattern)
			return pattern
		else:
			raise Exception("Syntax error on line `" + line + "'")

debug_level = 0
indent = 0

def setDebug(n):
	global debug_level
	debug_level = n

class ParsingError:
	def __init__(self, grammar, ref, place_string, is_part, causes):
		self.grammar = grammar
		self.ref = ref
		self.place_string = place_string
		self.is_part = is_part
		self.causes = causes
	def print(self, finnish=False, file=sys.stderr):
		global indent
		ref_str = self.grammar.refToString(self.ref)
		if self.is_part:
			string = ("\n"+self.place_string).replace("\n", "\n"+"  "*indent)[1:]
			if finnish:
				print(string + "tämän pitäisi olla " + ref_str, file=file)
			else:
				print(string + "expected " + ref_str, file=file)
		if self.causesContainPartErrors():
			if finnish:
				print("  "*indent+"lauseke ei voi olla "+ref_str+" koska:", file=file)
			else:
				print("  "*indent+ref_str+" does not match because:", file=file)
			indent += 1
			causes = list(filter(ParsingError.containsPartErrors, self.causes))
			for cause in causes[:5]:
				cause.print(finnish=finnish)
				print(file=file)
			if len(causes) > 5:
				if finnish:
					print("  "*indent+"+ " + str(len(self.causes)-5) + " muuta mahdollista virhettä", file=file)
				else:
					print("  "*indent+"+ " + str(len(self.causes)-5) + " more errors", file=file)
			indent -= 1
	def causesContainPartErrors(self):
		return any([cause.containsPartErrors() for cause in self.causes])
	def containsPartErrors(self):
		return self.is_part or self.causesContainPartErrors()

ERROR_STACK = [[]]

def makeErrorMessage(ref, tokens, start, length):
	line1 = ""
	line2 = ""
	line3 = ""
	for i, token in enumerate(tokens):
		inside = start < i < start+length
		char = "~" if inside else " "
		if i != 0:
			line1 += " "
			line2 += char
			if i <= start:
				line3 += " "
		line1 += token.token
		if i == start:
			line2 += "^" + "~" * (len(token.token)-1)
		else:
			line2 += char * len(token.token)
		if i < start:
			line3 += " " * len(token.token)
	return line1 + "\n" + line2 + "\n" + line3

class Pattern:
	def __init__(self, name, words, output):
		self.name = name
		self.words = words
		self.output = output
	def __repr__(self):
		return "Pattern(" + repr(self.name) + ", " + repr(self.words) + ", " + repr(self.output) + ")"
	def toCode(self):
		return " ".join([w.toCode() for w in self.words])# + " -> " + repr(self.output)
	def allowsEmptyContent(self):
		return False
	def match(self, grammar, tokens, bits, i=0, j=0, g=None):
		global indent
		groups = g or {w: [0, []] for w in self.words if isinstance(w, PatternRef)}
		ans = []
		while i <= len(tokens) and j <= len(self.words):
			token = tokens[i] if i < len(tokens) else Token("<END>", [])
			word = self.words[j] if j < len(self.words) else Token("<END>", [])
			if isinstance(word, PatternRef):
				ans += self.match(grammar, tokens, bits, i, j+1, {w: [groups[w][0], groups[w][1].copy()] for w in groups})
				if len(groups[word][1]) == 0:
					groups[word][0] = i
				groups[word][1].append(token)
				i += 1
			else:
				if token.token.lower() == word.token.lower() or token.containsMatch([(wbf, bits if "$" in wbits else wbits) for wbf, wbits in word.alternatives]):
					if debug_level >= 3:
						print(" "*indent+"match:", token, word, bits)
					i += 1
					j += 1
				else:
					if debug_level >= 3:
						print(" "*indent+"no match:", token, word, bits)
					return ans
		if j < len(self.words) or i < len(tokens):
			if debug_level >= 3:
				print(" "*indent+"remainder:", i, tokens, j, self.words)
			return ans
		for w in groups:
			if not groups[w][1] and not grammar.allowsEmptyContent(w.name):
				if debug_level >= 3:
					print(" "*indent+"empty group:", w, self.words, tokens)
				return ans
		
		if debug_level >= 2:
			print(" "*indent, end="")
			for w in self.words:
				print(w.name+"=["+" ".join([str(w2) for w2 in groups[w][1]])+"]" if isinstance(w, PatternRef) else str(w), end=" ")
			print()
			indent += 1
		
		args = []
		for i, w in enumerate([w for w in self.words if isinstance(w, PatternRef)]):
			ERROR_STACK.append([])
			
			match = grammar.matchAll(groups[w][1], w.name, (w.bits-{"$"})|(bits if "$" in w.bits else set()))
			
			errors = ERROR_STACK.pop()
			if len(match) == 0:
				error = ParsingError(
					grammar,
					w,
					makeErrorMessage(w, tokens, groups[w][0], len(groups[w][1])),
					len(groups[w][1]) != len(tokens),
					errors
				)
				ERROR_STACK[-1].append(error)
			
			args.append(match)
		ans = ans+[self.output.eval(c) for c in itertools.product(*args)]
		
		if debug_level >= 2:
			indent -= 1
			print(" "*indent, end="")
			print("->", ans)
		
		return ans
    
# Retki
# Copyright (C) 2018 Iikka Hauhio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import math
import random

# Copyright 2017 Iikka Hauhio
# Contains some minor changes to the original file.

# Copyright 2007 - 2012 Harri Pitkänen (hatapitk@iki.fi)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# This module contains general helper functions and classes for use
# with Python and Voikko.

import codecs
import os
import locale
import sys

# Word classes
NOUN=1
ADJECTIVE=2
VERB=3

# Vowel types
VOWEL_DEFAULT=0
VOWEL_FRONT=1
VOWEL_BACK=2
VOWEL_BOTH=3

# Gradation types
GRAD_NONE = 0
GRAD_SW = 1
GRAD_WS = 2

GRAD_WEAK = 3
GRAD_STRONG = 4

## Remove comments from a given line of text.
def removeComments(line):
	comment_start = line.find(u'#')
	if comment_start == -1:
		return line
	if comment_start == 0:
		return u''
	return line[:comment_start]

## Function that returns the type of vowels that are allowed in the suffixes for
# given simple word.
# The possible values are VOWEL_FRONT, VOWEL_BACK and VOWEL_BOTH.
def _simple_vowel_type(word):
	word = word.lower()
	last_back = max(word.rfind(u'a'), word.rfind(u'o'), word.rfind(u'å'), word.rfind(u'u'))
	last_ord_front = max(word.rfind(u'ä'), word.rfind(u'ö'))
	last_y = word.rfind(u'y')
	if last_back > -1 and max(last_ord_front, last_y) == -1:
		return VOWEL_BACK
	if last_back == -1 and max(last_ord_front, last_y) > -1:
		return VOWEL_FRONT
	if max(last_back, last_ord_front, last_y) == -1:
		return VOWEL_FRONT
	if last_y < max(last_back, last_ord_front):
		if last_back > last_ord_front: return VOWEL_BACK
		else: return VOWEL_FRONT
	else:
		return VOWEL_BOTH

## Returns autodetected vowel type of infection suffixes for a word.
# If word contains character '=', automatic detection is only performed on the
# trailing part. If word contains character '|', automatic detection is performed
# on the trailing part and the whole word, and the union of accepted vowel types is returned.
def get_wordform_infl_vowel_type(wordform):
	# Search for last '=' or '-', check the trailing part using recursion
	startind = max(wordform.rfind(u'='), wordform.rfind(u'-'))
	if startind == len(wordform) - 1: return VOWEL_BOTH # Not allowed
	if startind != -1: return get_wordform_infl_vowel_type(wordform[startind+1:])
	
	# Search for first '|', check the trailing part using recursion
	startind = wordform.find(u'|')
	if startind == len(wordform) - 1: return VOWEL_BOTH # Not allowed
	vtype_whole = _simple_vowel_type(wordform)
	if startind == -1: return vtype_whole
	vtype_part = get_wordform_infl_vowel_type(wordform[startind+1:])
	if vtype_whole == vtype_part: return vtype_whole
	else: return VOWEL_BOTH

## Returns True, if given character is a consonant, otherwise retuns False.
def is_consonant(letter):
	if letter.lower() in u'qwrtpsdfghjklzxcvbnm':
		return True
	else:
		return False

## Function that returns the type of vowels that are allowed in the affixes for given word.
# The possible values are VOWEL_FRONT, VOWEL_BACK and VOWEL_BOTH.
def vowel_type(word):
	word = word.lower()
	last_back = max(word.rfind(u'a'), word.rfind(u'o'), word.rfind(u'å'), word.rfind(u'u'))
	last_ord_front = max(word.rfind(u'ä'), word.rfind(u'ö'))
	last_y = word.rfind(u'y')
	if last_back > -1 and max(last_ord_front, last_y) == -1:
		return VOWEL_BACK
	if last_back == -1 and max(last_ord_front, last_y) > -1:
		return VOWEL_FRONT
	if max(last_back, last_ord_front, last_y) == -1:
		return VOWEL_FRONT
	if last_y < max(last_back, last_ord_front):
		if last_back > last_ord_front: return VOWEL_BACK
		else: return VOWEL_FRONT
	else:
		return VOWEL_BOTH


## Expands capital letters to useful character classes for regular expressions
def capital_char_regexp(pattern):
	pattern = pattern.replace('V', u'(?:a|e|i|o|u|y|ä|ö|é|è|á|ó|â)')
	pattern = pattern.replace('C', u'(?:b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z|š|ž)')
	pattern = pattern.replace('A', u'(?:a|ä)')
	pattern = pattern.replace('O', u'(?:o|ö)')
	pattern = pattern.replace('U', u'(?:u|y)')
	return pattern

# Copyright 2017 Iikka Hauhio
# Contains some minor changes to the original file.

# Copyright 2005-2010 Harri Pitkänen (hatapitk@iki.fi)
# Library for inflecting words for Voikko project.
# This library requires Python version 2.4 or newer.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import codecs
import sys
import re

# Size of the affix file is controlled by the following parameter. Only affix rules
# having priority lower or equal to MAX_AFFIX_PRIORITY are written to the
# affix file. Values from 1 to 3 are currently used.
MAX_AFFIX_PRIORITY=2

class InflectionRule:
	"Rule for word inflection"
	def __init__(self):
		self.name = u""
		self.isCharacteristic = False
		self.rulePriority = 1
		self.delSuffix = u""
		self.addSuffix = u""
		self.gradation = GRAD_WEAK

class InflectionType:
	"Word inflection type"
	def __init__(self):
		self.kotusClasses = []
		self.joukahainenClasses = []
		self.rmsfx = u""
		self.matchWord = u""
		self.gradation = GRAD_NONE
		self.note = u""
		self.inflectionRules = []
	
	"Return the given word with suffix removed"
	def removeSuffix(self, word):
		l = len(self.rmsfx)
		if l == 0: return word
		elif len(word) <= l: return u""
		else: return word[:-l]
	
	"Return the Kotus gradation class for word and gradation class in Joukahainen"
	def kotusGradClass(self, word, grad_type):
		if not grad_type in ["av1", "av2", "av3", "av4", "av5", "av6"]:
			return u""
		word = self.removeSuffix(word)
		if len(word) == 0: return u""
		if is_consonant(word[-1]) and not is_consonant(word[-2]):
			if word[-4:-2] == u'ng': return u'G'
			if word[-4:-2] == u'mm': return u'H'
			if word[-4:-2] == u'nn': return u'J'
			if word[-4:-2] == u'll': return u'I'
			if word[-4:-2] == u'rr': return u'K'
			if word[-3] == u'd': return u'F'
			if word[-3] == u't': return u'C'
			if word[-3] == u'k': return u'A'
			if word[-3] == u'p': return u'B'
			if word[-3] == u'v': return u'E'
		if grad_type == u'av1':
			if word[-3:-1] == u'tt': return u'C'
			if word[-3:-1] == u'kk': return u'A'
			if word[-3:-1] == u'pp': return u'B'
			if word[-3:-1] == u'mp': return u'H'
			if word[-2] == u'p' and not is_consonant(word[-1]):
				return u'E'
			if word[-3:-1] == u'nt': return u'J'
			if word[-3:-1] == u'lt': return u'I'
			if word[-3:-1] == u'rt': return u'K'
			if word[-2] == u't': return u'F'
			if word[-3:-1] == u'nk': return u'G'
			if word[-3:] == u'uku': return u'M'
			if word[-3:] == u'yky': return u'M'
		if grad_type == u'av2':
			if word[-4:-2] == u'ng': return u'G'
			if word[-4:-2] == u'mm': return u'H'
			if word[-4:-2] == u'nn': return u'J'
			if word[-4:-2] == u'll': return u'I'
			if word[-4:-2] == u'rr': return u'K'
			if word[-3] == u'd': return u'F'
			if word[-3] == u't': return u'C'
			if word[-3] == u'k': return u'A'
			if word[-3] == u'p': return u'B'
			if word[-3] == u'b': return u'O' # Unofficial, not in Kotus
			if word[-3] == u'g': return u'P' # Unofficial, not in Kotus
			if word[-3] == u'v': return u'E'
		if grad_type == u'av3': # k -> j
			if word[-2] == u'k': return u'L'
		if grad_type == u'av4': # j -> k
			if word[-2] == u'j': return u'L'
			if word[-3] == u'j': return u'L'
		if grad_type == u'av5': # k -> -
			if word[-2] == u'k': return u'D'
		if grad_type == u'av6': # - -> k
			return u'D'
		return u''

class InflectedWord:
	"Word in inflected form"
	def __init__(self):
		self.formName = u""
		self.inflectedWord = u""
		self.isCharacteristic = False
		self.priority = 1
	def __str__(self):
		return self.formName + u"\t" + self.inflectedWord

## Function to convert a string containing back vowels to an equivalent string containing
# front vowels.
def __convert_tv_ev(text):
	return text.replace('a', u'ä').replace('o', u'ö').replace('u', u'y')


## Applies given gradation type to given word. Returns a tuple in the form
# (strong, weak) or None if this is not possible. Conditional aposthrope
# is represented by $.
def __apply_gradation(word, grad_type):
	if grad_type == u'-':
		return (word, word)
	
	if is_consonant(word[-1]) and not is_consonant(word[-2]) and len(word) >= 3:
		if word[-4:-2] == u'ng':
			return (word[:-4]+u'nk'+word[-2:], word)
		# uvu/yvy->uku/yky not possible?
		if word[-4:-2] == u'mm':
			return (word[:-4]+u'mp'+word[-2:], word)
		if word[-4:-2] == u'nn':
			return (word[:-4]+u'nt'+word[-2:], word)
		if word[-4:-2] == u'll':
			return (word[:-4]+u'lt'+word[-2:], word)
		if word[-4:-2] == u'rr':
			return (word[:-4]+u'rt'+word[-2:], word)
		if word[-3] == u'd':
			return (word[:-3]+u't'+word[-2:], word)
		if word[-3] in u'tkp':
			return (word[:-2]+word[-3:], word)
		if word[-3] == u'v':
			return (word[:-3]+u'p'+word[-2:], word)
	
	if grad_type == u'av1' and len(word) >= 3:
		if word[-3:-1] in (u'tt',u'kk',u'pp'):
			return (word, word[:-2]+word[-1])
		if word[-3:-1] == u'mp':
			return (word, word[:-3]+u'mm'+word[-1])
		if word[-2] == u'p' and not is_consonant(word[-1]):
			return (word, word[:-2]+u'v'+word[-1])
		if word[-3:-1] == u'nt':
			return (word, word[:-3]+u'nn'+word[-1])
		if word[-3:-1] == u'lt':
			return (word, word[:-3]+u'll'+word[-1])
		if word[-3:-1] == u'rt':
			return (word, word[:-3]+u'rr'+word[-1])
		if word[-2] == u't':
			return (word, word[:-2]+u'd'+word[-1])
		if word[-3:-1] == u'nk':
			return (word, word[:-3]+u'ng'+word[-1])
		if word[-3:] == u'uku':
			return (word, word[:-3]+u'uvu')
		if word[-3:] == u'yky':
			return (word, word[:-3]+u'yvy')
	if grad_type == u'av2' and len(word) >= 2:
		if word[-3:-1] == u'ng':
			return (word[:-3]+u'nk'+word[-1], word)
		# uvu/yvy->uku/yky not possible?
		if word[-3:-1] == u'mm':
			return (word[:-3]+u'mp'+word[-1], word)
		if word[-3:-1] == u'nn':
			return (word[:-3]+u'nt'+word[-1], word)
		if word[-3:-1] == u'll':
			return (word[:-3]+u'lt'+word[-1], word)
		if word[-3:-1] == u'rr':
			return (word[:-3]+u'rt'+word[-1], word)
		if word[-2] == u'd':
			return (word[:-2]+u't'+word[-1], word)
		if word[-2] in u'tkpbg':
			return (word[:-1]+word[-2:], word)
		if word[-2] == u'v':
			return (word[:-2]+u'p'+word[-1], word)
	if grad_type == u'av3' and len(word) >= 3: # k -> j
		if word[-2] == u'k':
			if is_consonant(word[-3]):
				return (word, word[:-2]+u'j'+word[-1])
			else:
				return (word, word[:-3]+u'j'+word[-1])
	if grad_type == u'av4' and len(word) >= 3: # j -> k
		if word[-2] == u'j':
			return (word[:-2]+u'k'+word[-1], word)
		if word[-3] == u'j':
			return (word[:-3]+u'k'+word[-2]+word[-1], word)
	if grad_type == u'av5' and len(word) >= 2: # k -> -
		if word[-2] == u'k':
			return (word, word[:-2]+u'$'+word[-1])
	if grad_type == u'av6' and len(word) >= 1: # - -> k
		if is_consonant(word[-1]): # FIXME: hack
			return (word[:-2]+u'k'+word[-2:], word)
		else:
			return (word[:-1]+u'k'+word[-1], word)
	return None


# Read header line from a file. Return value will be a tuple in the form (name, value) or
# None if the end of file was reached.
def __read_header(file):
	while True:
		line = file.readline()
		if not line.endswith('\n'): return None
		strippedLine = removeComments(line).strip()
		if len(strippedLine) == 0: continue
		valStart = strippedLine.find(':')
		if valStart < 1:
			print('Malformed input file: the problematic line was')
			print(line)
			return None
		return (strippedLine[:valStart].strip(), strippedLine[valStart+1:].strip())


# Read an option "name" from string "options". If it does not exist, then default will be returned.
def __read_option(options, name, default):
	parts = options.split(u',');
	for part in parts:
		nameval = part.split(u'=')
		if len(nameval) == 2 and nameval[0] == name: return nameval[1]
		if len(nameval) == 1 and nameval[0] == name: return u'1'
	return default

# Read and return an inflection rule from a file. Returns None, if
# the end of group or file was reached.
def __read_inflection_rule(file):
	while True:
		line = file.readline()
		if not line.endswith('\n'): return None
		strippedLine = removeComments(line).strip()
		if len(strippedLine) == 0: continue
		columns = strippedLine.split()
		if columns[0] == 'end:': return None
		
		r = InflectionRule()
		if columns[0].startswith(u'!'):
			r.name = columns[0][1:]
			r.isCharacteristic = True
		else:
			r.name = columns[0]
			if columns[0] in ['nominatiivi', 'genetiivi', 'partitiivi', 'illatiivi',
				'nominatiivi_mon', 'genetiivi_mon', 'partitiivi_mon', 'illatiivi_mon',
				'infinitiivi_1', 'preesens_yks_1', 'imperfekti_yks_3',
				'kondit_yks_3', 'imperatiivi_yks_3', 'partisiippi_2',
				'imperfekti_pass']: r.isCharacteristic = True
			else: r.isCharacteristic = False
		if columns[1] != u'0': r.delSuffix = columns[1]
		if columns[2] != u'0': r.addSuffix = columns[2]
		if columns[3] == u's': r.gradation = GRAD_STRONG
		if len(columns) > 4:
			if __read_option(columns[4], u'ps', u'') == u'r': continue
			r.rulePriority = int(__read_option(columns[4], u'prio', u'1'))
		
		return r



# Read and return an inflection type from a file.
# If the end of file is reached, this function returns None.
def __read_inflection_type(file):
	header_tuple = __read_header(file)
	if header_tuple == None: return None
	if header_tuple[0] != u'class' or len(header_tuple[1]) == 0:
		print('Class definition expected.')
		return None
	
	t = InflectionType()
	t.kotusClasses = header_tuple[1].split(u",")
	while True:
		header_tuple = __read_header(file)
		if header_tuple == None:
			print('Unexpected end of file.')
			return None
		if header_tuple[0] == u'sm-class': t.joukahainenClasses = header_tuple[1].split(' ')
		if header_tuple[0] == u'rmsfx': t.rmsfx = header_tuple[1]
		if header_tuple[0] == u'match-word': t.matchWord = header_tuple[1]
		if header_tuple[0] == u'consonant-gradation':
			if header_tuple[1] == u'-': t.gradation = GRAD_NONE
			if header_tuple[1] == u'sw': t.gradation = GRAD_SW
			if header_tuple[1] == u'ws': t.gradation = GRAD_WS
		if header_tuple[0] == u'note':
			t.note = header_tuple[1]
		if header_tuple[0] == u'rules':
			rule = __read_inflection_rule(file)
			while rule != None:
				t.inflectionRules.append(rule)
				rule = __read_inflection_rule(file)
		if header_tuple[0] == u'end' and header_tuple[1] == u'class':
			return t


# Convert a Hunspell-fi -style pair of regular expression and replacement string to a list
# of tuples containing corresponding Hunspell affix rule elements (strip_str, affix, condition).
def __regex_to_hunspell(exp, repl):
	# TODO: implement more regular expressions
	rulelist = []
	wchars = u"[a-zäöé]"
	if exp == "": exp = "0"
	if repl == "": repl = "0"
	if exp == "0":
		strip_str = "0"
		condition = "."
		affix = repl
		rulelist.append((strip_str, affix, condition))
		return rulelist
	if re.compile(u"^(?:%s)+$" % wchars).match(exp) != None: # string of letters
		strip_str = exp
		condition = exp
		affix = repl
		rulelist.append((strip_str, affix, condition))
		return rulelist
	m = re.compile(u"^((?:%s)*)\\(\\[((?:%s)*)\\]\\)((?:%s)*)$" % (wchars, wchars, wchars) \
	              ).match(exp)
	if m != None: # exp is of form 'ab([cd])ef'
		start_letters = m.group(1)
		alt_letters = m.group(2)
		end_letters = m.group(3)
		for alt_char in alt_letters:
			strip_str = start_letters + alt_char + end_letters
			condition = start_letters + alt_char + end_letters
			affix = repl.replace('(1)', alt_char)
			rulelist.append((strip_str, affix, condition))
		return rulelist
	m = re.compile("^((?:%s)*)\\[((?:%s)*)\\]((?:%s)*)$" % (wchars, wchars, wchars)).match(exp)
	if m != None: # exp is of form 'ab[cd]ef'
		start_letters = m.group(1)
		alt_letters = m.group(2)
		end_letters = m.group(3)
		for alt_char in alt_letters:
			strip_str = start_letters + alt_char + end_letters
			condition = start_letters + alt_char + end_letters
			affix = repl
			rulelist.append((strip_str, affix, condition))
		return rulelist
	print('Unsupported regular expression: exp=\'' + exp + '\', repl=\'' + repl + '\'')
	return []


# Translates word match pattern to a Perl-compatible regular expression
def __word_pattern_to_pcre(pattern):
	return '.*' + capital_char_regexp(pattern) + '$'


# Public functions

import pyodide

# Reads and returns a list of word classes from a file named file_name.
def readInflectionTypes(file_name):
	inflection_types = []
	inputfile = pyodide.open_url(file_name)
	inftype = __read_inflection_type(inputfile)
	while inftype != None:
		inflection_types.append(inftype)
		inftype = __read_inflection_type(inputfile)
	inputfile.close()
	return inflection_types


def _replace_conditional_aposthrope(word):
	ind = word.find(u'$')
	if ind == -1: return word
	if ind == 0 or ind == len(word) - 1: return word.replace(u'$', u'')
	if word[ind-1] == word[ind+1]:
		if word[ind-1] in [u'i', u'o', u'u', u'y', u'ö']:
			return word.replace(u'$', u'\'')
		if word[ind-1] in [u'a', u'ä'] and ind > 1 and word[ind-2] == word[ind-1]:
			return word.replace(u'$', u'\'')
	return word.replace(u'$', u'')

DERIVS_VOWEL_HARMONY_SPECIAL_CLASS_1 = [u'subst_tO', u'subst_Os']
DERIVS_VOWEL_HARMONY_SPECIAL_CLASS_2 = [u'verbi_AjAA', 'verbi_AhtAA', 'verbi_AUttAA', 'verbi_AUtellA']

def _normalize_base(base):
	if base.find(u'=') != -1:
		base = base[base.find(u'=') + 1:]
	return base.lower()

def _vtype_special_class_1(base):
	base = _normalize_base(base)
	last_back = max(base.rfind(u'a'), base.rfind(u'o'), base.rfind(u'å'), base.rfind(u'u'))
	last_front = max(base.rfind(u'ä'), base.rfind(u'ö'), base.rfind(u'y'))
	if last_front > last_back: return VOWEL_FRONT
	else: return VOWEL_BACK

def _vtype_special_class_2(base):
	base = _normalize_base(base)
	last_back = max(base.rfind(u'a'), base.rfind(u'o'), base.rfind(u'å'), base.rfind(u'u'))
	last_front = max(base.rfind(u'ä'), base.rfind(u'ö'), base.rfind(u'y'))
	if last_front > last_back: return VOWEL_FRONT
	elif last_front < last_back: return VOWEL_BACK
	else:
		# no front or back vowels
		if base.rfind(u'e') >= 0:
			# "hel|istä" -> "heläjää"
			return VOWEL_FRONT
		else:
			# "kih|istä" -> "kihajaa"
			return VOWEL_BACK

def _vtype_meri_partitive(base):
	return VOWEL_BACK

def _removeStructure(word):
	return word.replace(u"=", u"").replace(u"|", u"")

## Returns a list of InflectedWord objects for given word and inflection type.
def inflectWordWithType(word, inflection_type, infclass, gradclass, vowel_type = VOWEL_DEFAULT):
	if not infclass in inflection_type.joukahainenClasses: return []
	word_no_sfx = inflection_type.removeSuffix(word)
	word_grad = __apply_gradation(word_no_sfx, gradclass)
	if word_grad == None: return []
	if gradclass == '-': grad_type = GRAD_NONE
	elif gradclass in ['av1', 'av3', 'av5']: grad_type = GRAD_SW
	elif gradclass in ['av2', 'av4', 'av6']: grad_type = GRAD_WS
	if grad_type != GRAD_NONE and grad_type != inflection_type.gradation: return []
	if not re.compile(__word_pattern_to_pcre(inflection_type.matchWord),
	                  re.IGNORECASE).match(word): return []
	inflection_list = []
	if vowel_type == VOWEL_DEFAULT:
		vowel_type = get_wordform_infl_vowel_type(word)
	for rule in inflection_type.inflectionRules:
		if rule.gradation == GRAD_STRONG: word_base = word_grad[0]
		else: word_base = word_grad[1]
		hunspell_rules = __regex_to_hunspell(rule.delSuffix, rule.addSuffix)
		for hunspell_rule in hunspell_rules:
			if hunspell_rule[0] == '0': word_stripped_base = word_base
			else: word_stripped_base = word_base[:-len(hunspell_rule[0])]
			if hunspell_rule[1] == '0': affix = ''
			else: affix = hunspell_rule[1]
			if hunspell_rule[2] == '.': pattern = ''
			else: pattern = hunspell_rule[2]
			
			infl = InflectedWord()
			infl.formName = rule.name
			infl.isCharacteristic = rule.isCharacteristic
			infl.priority = rule.rulePriority
			
			vowel_harmony_rule = None
			if rule.name in DERIVS_VOWEL_HARMONY_SPECIAL_CLASS_1:
				vowel_harmony_rule = _vtype_special_class_1
			elif rule.name in DERIVS_VOWEL_HARMONY_SPECIAL_CLASS_2:
				vowel_harmony_rule = _vtype_special_class_2
			elif rule.name == u'partitiivi' and infclass == u'meri':
				vowel_harmony_rule = _vtype_meri_partitive
			final_base = _removeStructure(word_stripped_base)
			if vowel_harmony_rule != None:
				if vowel_harmony_rule(word_stripped_base) == VOWEL_FRONT:
					infl.inflectedWord = final_base + __convert_tv_ev(affix)
				else:
					infl.inflectedWord = final_base + affix
				inflection_list.append(infl)
				continue
			
			if vowel_type in [VOWEL_BACK, VOWEL_BOTH] and \
			   word_base.endswith(pattern):
				infl.inflectedWord = _replace_conditional_aposthrope(
				                     final_base + affix)
				inflection_list.append(infl)
				infl = InflectedWord()
				infl.formName = rule.name
				infl.isCharacteristic = rule.isCharacteristic
				infl.priority = rule.rulePriority
			if vowel_type in [VOWEL_FRONT, VOWEL_BOTH] and \
			   word_base.endswith(__convert_tv_ev(pattern)):
				infl.inflectedWord = _replace_conditional_aposthrope(
				                     final_base + __convert_tv_ev(affix))
				inflection_list.append(infl)
	return inflection_list

## Returns a list of InflectedWord objects for given word.
def inflectWord(word, jo_infclass, inflection_types, vowel_type = VOWEL_DEFAULT):
	dash = jo_infclass.find(u'-')
	if dash == -1:
		infclass = jo_infclass
		gradclass = u'-'
	else:
		infclass = jo_infclass[:dash]
		gradclass = jo_infclass[dash+1:]
		if not gradclass in [u'av1', u'av2', u'av3', u'av4', u'av5', u'av6', u'-']:
			return []
	
	for inflection_type in inflection_types:
		inflection = inflectWordWithType(word, inflection_type, infclass, gradclass, vowel_type)
		if len(inflection) > 0: return inflection
	return []

# Copyright 2018 Kielikone Oy
#
# Added generate_forms that can generate alternative forms
# Guessing -ton/-tön inflection class
# Fixed bugs

# Copyright 2017 Iikka Hauhio
#
# Contains some changes to the original file (voikko-inflect-word).
# The file is no longer a stand-alone program, but a library.
# It reads word classes automatically from the sanat.txt file.
# It also tries to guess the word class, if not found in sanat.txt.
# The file was changed to support Python 3.

# Copyright 2005-2007 Harri Pitkänen (hatapitk@iki.fi)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import locale

noun_types = readInflectionTypes('subst.aff')
verb_types = readInflectionTypes('verb.aff')

def word_and_infl_class(fullclass):
	infclass_parts = fullclass.split('-')
	if len(infclass_parts) == 2:
		wordclass = infclass_parts[0]
		infclass = infclass_parts[1]
	elif len(infclass_parts) == 3:
		wordclass = infclass_parts[0]
		infclass = infclass_parts[1]+u'-'+infclass_parts[2]
	else:
		print('Incorrect inflection class')
		sys.exit(1)
	if not wordclass in [u'subst', u'verbi']:
		print('Incorrect word class')
		sys.exit(1)
	return (wordclass, infclass)

def generate_forms(word, infl_classes=None, pos=None):
	"""Generates inflected forms for the given word."""

	global verb_types
	global noun_types
	if infl_classes is None:
		if word in WORD_CLASSES:
			infl_classes = WORD_CLASSES[word]
		elif len(word) > 3 and word[-3:] in ["ttu", "tty"]:
			infl_classes = ["subst-valo-av1"]
		elif len(word) > 3 and word[-3:] in ["uus", "yys"]:
			infl_classes = ["subst-kalleus"]
		elif len(word) > 3 and word[-2:] in ["ja", "jä"]:
			infl_classes = ["subst-kulkija"]
		elif len(word) > 4 and word[-3:] in ["ton", "tön"]:
			infl_classes = ["subst-onneton-av2"]
		else:
			def end_similarity(word2):
				i = 0
				while i < min(len(word), len(word2)):
					if word[-i-1] != word2[-i-1]:
						break
					i += 1
				return (i, -len(word2))
			def right_wclass(word2):
				if pos is None or any([word_class.startswith(pos) for word_class in WORD_CLASSES[word2]]):
					return 1
				else:
					return 0
			def points(word2):
				return (right_wclass(word2), end_similarity(word2))
			mirror = sorted(list(WORD_CLASSES), key=points)[-1]
			infl_classes = WORD_CLASSES[mirror]
			WORD_CLASSES[word] = infl_classes
			#raise(Exception("Unknown word '" + word + "'"))
	ans = []
	for infl_class in infl_classes:
		(wclass, infclass) = word_and_infl_class(infl_class)
		if wclass == u'verbi': itypes = verb_types
		else: itypes = noun_types
		homonym = {}
		for iword in inflectWord(word, infclass, itypes):
			if iword.formName not in homonym:
				homonym[iword.formName] = []
			if iword.inflectedWord not in homonym[iword.formName]:
				homonym[iword.formName].append(iword.inflectedWord)
		ans.append(homonym)
	return ans

def inflect_word(word, classes=None, required_wclass=None):
	"""Deprecated."""

	homonyms = generate_forms(word, infl_classes=classes, pos=required_wclass)
	ans = []
	for homonym in homonyms:
		new_homonym = {}
		for form in homonym:
			new_homonym[form] = homonym[form][0]
		ans.append(new_homonym)
	return ans[0]

WORD_CLASSES = {}

import pyodide

with pyodide.open_url("sanat.txt") as f:
	for line in f:
		line = line.strip()
		i = line.index(";")
		word = line[:i].replace("=", "")
		classes = line[i+1:]
		
		if word not in WORD_CLASSES:
			WORD_CLASSES[word] = []
		
		WORD_CLASSES[word].append(classes)

# Suomilog
# Copyright (C) 2018 Iikka Hauhio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import re

from js import voikko

DICTIONARY = defaultdict(list)

def tokenize(text):
	tokens = []
	for token in voikko.tokens(text):
		if token.type == "WHITESPACE":
			continue
		if "-" in token.text:
			index = token.text.rindex("-")+1
			lastPart = token.text[index:]
			baseformPrefix = token.text[:index].lower()
		else:
			lastPart = token.text
			baseformPrefix = ""
		alternatives = []
		for word in voikko.analyze(token.text):
			word = dict(word)
			if "BASEFORM" in word:
				alternatives.append(baseformAndBits(word))
		# Jos jäsennys epäonnistui, koetetaan jäsennystä vain viimeisen palan kautta
		if len(alternatives) == 0 and baseformPrefix:
			for word in voikko.analyze(lastPart):
				word = dict(word)
				if "BASEFORM" in word:
					alternatives.append(baseformAndBits(word, baseformPrefix))
		# Jos sana löytyy suomilogin omasta sanakirjasta, lisää myös sieltä vaihtoehdot
		if token.text.lower() in DICTIONARY:
			alternatives += DICTIONARY[token.text.lower()]
		tokens.append(Token(token.text, alternatives))
	return tokens

def baseformAndBits(word, baseformPrefix=None):
	bits = set()
	addBits(word, bits, "NUMBER", {"singular": "yksikkö", "plural": "monikko"})
	addBits(word, bits, "SIJAMUOTO")
	addBits(word, bits, "CLASS")
	addBits(word, bits, "PARTICIPLE")
	addBits(word, bits, "PERSON")
	addBits(word, bits, "MOOD", {
		"MINEN-infinitive": "-minen",
		"MA-infinitive": "-ma",
		"E-infinitive": "-e",
		"A-infinitive": "-a",
		"imperative": "imperatiivi",
		"indicative": "indikatiivi",
		"conditional": "konditionaali",
		"potential": "potentiaali"
	})
	if word["CLASS"] == "lukusana" and ("SIJAMUOTO" not in word or not word["SIJAMUOTO"]):
		bits.add("nimento")
	if not baseformPrefix:
		return word["BASEFORM"].lower(), bits
	else:
		return baseformPrefix + word["BASEFORM"].lower(), bits

def addBits(word, bits, name, table=None):
	if name in word:
		if table:
			if word[name] in table:
				bits.add(table[word[name]])
		else:
			bits.add(word[name])

def addNounToDictionary(noun):
	for plural in [False, True]:
		for case in CASES:
			DICTIONARY[inflect(noun, case, plural).lower()].append((noun, {case, "monikko" if plural else "yksikkö"}))

CASES = [
	"nimento",
	"omanto",
	"osanto",
	"olento",
	"tulento",
	"ulkoolento",
	"ulkotulento",
	"ulkoeronto",
	"sisaolento",
	"sisatulento",
	"sisaeronto",
	"vajanto"
]

CASES_LATIN = {
	"nimento": "nominatiivi",
	"omanto": "genetiivi",
	"osanto": "partitiivi",
	"olento": "essiivi",
	"tulento": "translatiivi",
	"ulkotulento": "allatiivi",
	"ulkoolento": "adessiivi",
	"ulkoeronto": "ablatiivi",
	"sisatulento": "illatiivi",
	"sisaolento": "inessiivi",
	"sisaeronto": "elatiivi",
	"vajanto": "abessiivi",
	"keinonto": "instruktiivi",
	"seuranto": "komitatiivi",
	"kerrontosti": "adverbi"
}

CASES_ENGLISH = {
	"nimento": "nominative",
	"omanto": "genitive",
	"osanto": "partitive",
	"olento": "essive",
	"tulento": "translative",
	"ulkotulento": "allative",
	"ulkoolento": "adessive",
	"ulkoeronto": "ablative",
	"sisatulento": "illative",
	"sisaolento": "inessive",
	"sisaeronto": "elative",
	"vajanto": "abessive",
	"keinonto": "instructive",
	"seuranto": "comitative",
	"kerrontosti": "adverb"
}

CASES_A = {
	"nimento": "",
	"omanto": ":n",
	"osanto": ":ta",
	"olento": ":na",
	"tulento": ":ksi",
	"ulkotulento": ":lle",
	"ulkoolento": ":lla",
	"ulkoeronto": ":lta",
	"sisatulento": ":han",
	"sisaolento": ":ssa",
	"sisaeronto": ":sta",
	"vajanto": ":tta",
	"keinonto": ":in",
	"seuranto": ":ineen",
	"kerrontosti": ":sti"
}

CASES_F = {
	"nimento": "",
	"omanto": ":n",
	"osanto": ":ää",
	"olento": ":nä",
	"tulento": ":ksi",
	"ulkotulento": ":lle",
	"ulkoolento": ":llä",
	"ulkoeronto": ":ltä",
	"sisatulento": ":ään",
	"sisaolento": ":ssä",
	"sisaeronto": ":stä",
	"vajanto": ":ttä",
	"keinonto": ":in",
	"seuranto": ":ineen",
	"kerrontosti": ":sti"
}

CASES_ELLIPSI = {
	"nimento": "",
	"omanto": ":n",
	"osanto": ":ä",
	"olento": ":nä",
	"tulento": ":ksi",
	"ulkotulento": ":lle",
	"ulkoolento": ":llä",
	"ulkoeronto": ":ltä",
	"sisatulento": ":iin",
	"sisaolento": ":ssä",
	"sisaeronto": ":stä",
	"vajanto": ":ttä",
	"keinonto": ":ein",
	"seuranto": ":eineen",
	"kerrontosti": ":sti"
}

CASE_REGEXES = {
	"singular": {
		"omanto": r"[^:]+:n",
		"osanto": r"[^:]+:(aa?|ää?|t[aä])",
		"olento": r"[^:]+:(n[aä])",
		"tulento": r"[^:]+:ksi",
		"ulkotulento": r"[^:]+:lle",
		"ulkoolento": r"[^:]+:ll[aä]",
		"ulkoeronto": r"[^:]+:lt[aä]",
		"sisatulento": r"[^:]+:(aan|ään|h[aeiouyäöå]n)",
		"sisaolento": r"[^:]+:ss[aä]",
		"sisaeronto": r"[^:]+:st[aä]",
		"vajanto": r"[^:]+:tt[aä]"
	},
	"plural": {
		"omanto": r"[^:]+:ien",
		"osanto": r"[^:]+:(ia?|iä?|it[aä])",
		"olento": r"[^:]+:(in[aä])",
		"tulento": r"[^:]+:iksi",
		"ulkotulento": r"[^:]+:ille",
		"ulkoolento": r"[^:]+:ill[aä]",
		"ulkoeronto": r"[^:]+:ilt[aä]",
		"sisatulento": r"[^:]+:(iin|ih[aeiouyäöå]n)",
		"sisaolento": r"[^:]+:iss[aä]",
		"sisaeronto": r"[^:]+:ist[aä]",
		"vajanto": r"[^:]+:itt[aä]",
		"keinonto": r"[^:]+:in",
		"seuranto": r"[^:]+:ine[^:]*"
	},
	"": {
		"kerrontosti": "[^:]+:sti"
	}
}

ORDINAL_CASE_REGEXES = {
	"nimento": r"[^:]+:s",
	"omanto": r"[^:]+:nnen",
	"osanto": r"[^:]+:tt[aä]",
	"tulento": r"[^:]+:nneksi",
	"ulkotulento": r"[^:]+:nnelle",
	"ulkoolento": r"[^:]+:nnell[aä]",
	"ulkoeronto": r"[^:]+:nnelt[aä]",
	"sisatulento": r"[^:]+:nteen",
	"sisaolento": r"[^:]+:nness[aä]",
	"sisaeronto": r"[^:]+:nnest[aä]",
	"vajanto": r"[^:]+:nnett[aä]",
	"kerrontosti": r"[^:]+:nnesti"
}

def inflect(word, case, plural):
	case_latin = CASES_LATIN[case]
	if plural:
		case_latin += "_mon"
	
	if re.fullmatch(r"[0-9]+", word):
		if case == "sisatulento":
			if word[-1] in "123560":
				return word + ":een"
			elif word[-1] in "479":
				return word + ":ään"
			else: # 8
				return word + ":aan"
		elif word[-1] in "14579":
			return word + CASES_A[case].replace("a", "ä")
		else:
			return word + CASES_A[case]
	elif len(word) == 1:
		if word in "flmnrsx":
			return word + CASES_F[case]
		elif case == "sisatulento":
			if word in "aeiouyäöå":
				return word + ":h" + word + "n"
			elif word in "bcdgptvw":
				return word + ":hen"
			elif word in "hk":
				return word + ":hon"
			elif word == "j":
				return "j:hin"
			elif word == "q":
				return "q:hun"
			elif word == "z":
				return "z:aan"
		elif word in "ahkoquzå":
			return word + CASES_A[case]
		else:
			return word + CASES_A[case].replace("a", "ä")
	else:
		inflections = inflect_word(word)
		if case_latin not in inflections:
			return word + ":" + case
		return inflections[case_latin]

# Retki
# Copyright (C) 2018 Iikka Hauhio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


def nameToBaseform(tokens, bits, rbits):
	ans = []
	found = False
	for token in reversed(tokens):
		for bf, tbits in token.alternatives:
			if not found:
				if rbits <= tbits:
					ans.append((bf, bits or {"$"}))
					found = True
					break
			else:
				if rbits <= tbits and tbits & {"laatusana", "nimisana_laatusana", "agent", "asemosana", "lukusana"}:
					ans.append((bf, bits or {"$"}))
					break
		else:
			ans.append((token.token, set()))
	return reversed(ans)

def tokensToString(tokens, rbits={"nimento", "yksikkö"}):
	return " ".join([text for text, bits in nameToBaseform(tokens, {}, rbits)])

def tokensToInflectedString(tokens, case, rbits={"nimento", "yksikkö"}):
	return " ".join([inflect(text, case, "monikko" in rbits) if "$" in bit else text for text, bit in nameToBaseform(tokens, {}, rbits)])

def nameToCode(name, bits=None, rbits={"nimento", "yksikkö"}):
	return " ".join([token + ("{" + ",".join(tbits) + "}" if tbits else "") for token, tbits in nameToBaseform(name, bits, rbits)])

def tokensToCode(tokens):
	return " ".join([token.toCode() for token in tokens])


# Bittiluokka

class Bits:
	def __init__(self, bits=None):
		self.bits = bits or set()
	def bitOn(self, bit):
		self.bits.add(bit)
		return self
	def bitOff(self, bit):
		if bit in self.bits:
			self.bits.remove(bit)
		return self
	def bitsOn(self, bits):
		for bit in bits:
			self.bitOn(bit)
		return self
	def bitsOff(self, bits):
		for bit in bits:
			self.bitOff(bit)
		return self

# Evaluominen

def evalOrCall(f, p):
	if isinstance(f, str):
		return eval(f)(*p)
	else:
		return f(*p)

# Ulostulo

class FuncOutput:
	def __init__(self, f):
		self.func = f
	def eval(self, args):
		return lambda: self.func(*[arg() for arg in args])

identity = FuncOutput(lambda x: x)

class SumOutput:
	def __init__(self, f=lambda: 0):
		self.f = f
	def eval(self, args):
		return sum(args) + self.f()

# Pythoniksi muuntamista varten

def toPython(obj):
	if "toPython" in dir(obj):
		return obj.toPython()
	elif isinstance(obj, list):
		return "[" + ", ".join([toPython(val) for val in obj]) + "]"
	elif isinstance(obj, tuple):
		return "(" + ", ".join([toPython(val) for val in obj]) + ("," if len(obj) == 1 else "") + ")"
	else:
		return repr(obj)

# Olioluokka

OBJECTS = None

def saveObjects():
	global OBJECTS
	OBJECTS = {}

def getObjects():
	return OBJECTS.values()
	
OBJECTS_IN_ORDER = []

def searchLastObject(pattern):
	for obj in reversed(OBJECTS_IN_ORDER):
		if pattern.matches(obj):
			return obj
	return None

def searchRandomObject(pattern):
	matching = list(filter(pattern.matches, OBJECTS_IN_ORDER))
	return random.choice(matching)

def forSet(objects, var_name, pattern, f, group, count_var_name):
	pushScope()
	ans = []
	if not group:
		for val in set(objects):
			if pattern.matches(val):
				putVar(var_name, val, to_scope_stack=True)
				ans.append(f())
	else:
		# TODO
		groups = []
		for val in objects:
			if pattern.matches(val):
				for group in groups:
					if group[0].equals(val):
						group.append(val)
						break
				else:
					groups.append([val])
		for group in groups:
				putVar(count_var_name, createIntegerObj(len(group)), to_scope_stack=True)
				putVar(var_name, group[0], to_scope_stack=True)
				ans.append(f())
	popScope()
	return ans

class RObject(Bits):
	def __init__(self, rclass, name, bits=None, obj_id=None, extra=None, name_tokens=None, srules=None, aliases=None, data=None):
		Bits.__init__(self, bits)
		if not obj_id:
			self.id = nextCounter("RObject")
		else:
			self.id = obj_id
		if OBJECTS is not None and not rclass.primitive:
			OBJECTS[self.id] = self
		if not rclass.primitive:
			OBJECTS_IN_ORDER.append(self)
		self.rclass = rclass
		self.data = data or {}
		self.extra = extra or {}
		self.name = name
		self.name_tokens = name_tokens
		self.aliases = aliases or []
		self.selection_rules = srules or []
		if name and "nimi koodissa" not in self.data:
			self.data["nimi koodissa"] = createStringObj(name)
	def __repr__(self):
		return self.asString()
	def copy(self):
		data_copy = {}
		for key in self.data:
			if isinstance(self.data[key], RObject):
				data_copy[key] = self.data[key]
			elif isinstance(self.data[key], dict):
				data_copy[key] = self.data[key].copy()
			elif isinstance(self.data[key], set):
				data_copy[key] = self.data[key].copy()
			else:
				raise Exception("not implemented")
		return RObject(
			self.rclass, self.name, self.bits.copy(),
			extra=self.extra.copy(), name_tokens=self.name_tokens, srules=self.selection_rules.copy(),
			data=data_copy
		)
	def toPythonRef(self):
		if self.rclass.primitive:
			return evalOrCall(self.rclass.primitive, [self])
		else:
			return 'OBJECTS[' + repr(self.id) + ']'
	def toPython(self):
		if self.rclass.primitive:
			return "", ""
		
		var = 'OBJECTS[' + repr(self.id) + ']'
		
		# muodostetaan parserisäännöt aliaksista ja
		names = self.aliases.copy()
		if self.name_tokens:
			names.append(self.name_tokens)
		if self.rclass.name_tokens:
			names.append(self.rclass.name_tokens)
		
		grammar = ""
		for name in names:
			grammar += ";GRAMMAR.parseGrammarLine('.EXPR-%d ::= %s', FuncOutput(lambda: (%s, %s.likeliness())))" % (
				self.rclass.id,
				nameToCode(name, bits={"$"}, rbits={"nimento"}),
				var, var
			)
		
		# ulostulo on tuple, jonka ensimmäinen arvo luo olion ja parserisäännöt, ja toinen arvo luo kentät
		return (
			# ensimmäinen arvo:
			'%s = RObject(CLASSES[%s], %s, %s, %s, %s, %s, %s)' % (
				var,
				repr(self.rclass.name), repr(self.name),
				repr(self.bits), repr(self.id), toPython(self.extra),
				repr(self.name_tokens),
				"[" + ", ".join(self.selection_rules) + "]")
			+ grammar,
			# toinen arvo:
			";".join([
				# olioviittauskentät
				'%s.data[%s] = %s' % (var, repr(key), self.data[key].toPythonRef()) for key in self.data if isinstance(self.data[key], RObject)
			] + [
				# karttakentät
				'%s.data[%s] = {%s}' % (
					var,
					repr(key),
					", ".join([keykey.toPythonRef() + ": " + self.data[key][keykey].toPythonRef() for keykey in self.data[key]])
				)
				for key in self.data if isinstance(self.data[key], dict)
			] + [
				# joukkokentät
				'%s.data[%s] = {%s}' % (var, repr(key), ", ".join([val.toPythonRef() for val in self.data[key]]))
				for key in self.data if isinstance(self.data[key], set)
			])
		)
	def equals(self, obj):
		if self.id == obj.id:
			return True
		if self.name != obj.name:
			return False
		if self.rclass != obj.rclass:
			return False
		if len(self.data) != len(obj.data):
			return False
		for key in self.data:
			if key not in obj.data or not self.data[key].quickEquals(obj.data[key]):
				return False
		if self.extra != obj.extra:
			return False
		return True
	def quickEquals(self, obj):
		return self.id == obj.id or self.rclass == obj.rclass and self.rclass.primitive and self.extra == obj.extra
	def get(self, field_name):
		if field_name not in self.data:
			for clazz in self.rclass.superclasses():
				if field_name in clazz.fields and clazz.fields[field_name].default_value:
					self.data[field_name] = clazz.fields[field_name].default_value
					break
			else:
				self.data[field_name] = None
		return self.data[field_name]
	def set(self, field_name, val):
		self.data[field_name] = val
		if field_name == "nimi koodissa":
			name = val.asString()
			self.name = name
			self.name_tokens = tokenize(name)
	def getMap(self, field_name, key_val):
		key = key_val.toKey()
		if field_name not in self.data:
			self.data[field_name] = {}
		if key not in self.data[field_name]:
			for clazz in self.rclass.superclasses():
				if field_name in clazz.fields and clazz.fields[field_name]:
					return clazz.fields[field_name].default_value
			return None
		return self.data[field_name][key]
	def setMap(self, field_name, key_val, val):
		key = key_val.toKey()
		if field_name not in self.data:
			self.data[field_name] = {}
		self.data[field_name][key] = val
	def appendSet(self, field_name, val):
		if field_name not in self.data:
			self.data[field_name] = set()
		field = self.data[field_name]
		if isinstance(val, RPattern):
			if not self.containsSet(field_name, val):
				field.add(val.newInstance(tokenize("uusi arvo")))
		else:
			field.add(val)
	def removeSet(self, field_name, val):
		if field_name not in self.data:
			return
		field = self.data[field_name]
		if isinstance(val, RPattern):
			for obj in field:
				if val.matches(obj):
					field.remove(obj)
		else:
			if val in field:
				field.remove(val)
	def containsSet(self, field_name, val):
		if field_name not in self.data:
			return False
		field = self.data[field_name]
		if isinstance(val, RPattern):
			if val.obj:
				return val.obj in field and val.matches(val.obj)
			else:
				for obj in field:
					if val.matches(obj):
						return True
				return False
		else:
			return val in field
	def clearSet(self, field_name):
		if field_name not in self.data:
			return
		field = self.data[field_name]
		field.clear()
	def isSetEmpty(self, field_name):
		if field_name not in self.data:
			return
		field = self.data[field_name]
		return len(field) == 0
	def forSet(self, field_name, var_name, pattern, f, group=False, count_var_name=None):
		if field_name not in self.data:
			return []
		return forSet(self.data[field_name], var_name, pattern, f, group, count_var_name)
	def onceSet(self, field_name, var_name, pattern, f):
		if field_name not in self.data:
			return False
		pushScope()
		for val in self.data[field_name]:
			if pattern.matches(val):
				putVar(var_name, val, to_scope_stack=True)
				if f():
					return True
		popScope()
		return False
	def createCopies(self, n, condition=None):
		for i in range(n):
			obj = self.copy()
			if condition:
				condition.doModify(obj)
	def setExtra(self, name, data):
		self.extra[name] = data
		return self
	def addSelectionRule(self, rule):
		self.selection_rules.append(rule)
	def addVariableAlias(self, alias):
		self.aliases.append(alias)
	def likeliness(self):
		ans = 0
		for rule in self.selection_rules:
			ans += evalOrCall(rule, [self])
		return ans
	def asString(self, case="nimento", capitalized=False):
		do_lower = True
		if case != "nimento":
			if self.name_tokens:
				name_tokens = self.name_tokens
			elif self.name:
				name_tokens = tokenize(self.name)
			elif "str" in self.extra:
				name_tokens = tokenize(self.extra["str"])
				do_lower = False
			elif "int" in self.extra:
				name_tokens = tokenize(str(self.extra["int"]))
				do_lower = False
			else:
				name_tokens = self.rclass.name_tokens or tokenize(self.rclass.name)
			ans = tokensToInflectedString(name_tokens, case)
		elif self.name:
			ans = self.name
		elif "str" in self.extra:
			ans = self.extra["str"]
			do_lower = False
		elif "int" in self.extra:
			ans = str(self.extra["int"])
			do_lower = False
		else:
			ans = "[eräs " + self.rclass.name + "]"
		if capitalized:
			return ans.capitalize()
		elif do_lower:
			return ans.lower()
		else:
			return ans
	def toKey(self):
		if "str" in self.extra:
			return self.extra["str"]
		elif "int" in self.extra:
			return self.extra["int"]
		elif "tuple" in self.extra:
			return tuple(v.toKey() for v in self.extra["tuple"])
		else:
			return self

# Luokat

COUNTERS = {}

class Counter:
	def __init__(self):
		self.counter = 0
	
	def __next__(self):
		self.counter += 1
		return self.counter
	
	def __iter__(self):
		return self

def nextCounter(name="default"):
	if name not in COUNTERS:
		COUNTERS[name] = Counter()
	return next(COUNTERS[name])

def resetCounter(name="default"):
	COUNTERS[name] = Counter()

def chooseByCounter(name, then_blocks, else_block=None, loop=False):
	c = nextCounter(name)-1
	if c < len(then_blocks):
		then_blocks[c]()
	else:
		if else_block:
			else_block()
		if loop:
			resetCounter(name)
			then_blocks[nextCounter(name)-1]()

CLASSES = {}
CLASSES_IN_ORDER = []

class RClass(Bits):
	def __init__(self, name, superclass, name_tokens, class_id=None, bit_groups=None, bits=None, primitive=None):
		Bits.__init__(self, bits)
		
		CLASSES[name] = self
		CLASSES_IN_ORDER.append(self)
		
		if class_id:
			self.id = class_id
		else:
			self.id = nextCounter("RClass")
		self.name = name
		self.name_tokens = name_tokens
		self.superclass = superclass
		self.direct_subclasses = []
		self.fields = {}
		self.bit_groups = bit_groups or []
		self.attributePhraseAdders = []
		self.selection_rules = []
		self.primitive = primitive
		
		if superclass:
			self.superclass.direct_subclasses.append(self)
	def toPython(self):
		sc = "None" if self.superclass is None else "CLASSES[" + repr(self.superclass.name) + "]"
		grammar = "" if self.superclass is None else 'GRAMMAR.parseGrammarLine(".EXPR-%d ::= .EXPR-%d{$}", identity)' % (self.superclass.id, self.id)
		return (
			'RClass(%s, %s, %s, %d, %s, %s, %s);%s' % (
				repr(self.name), sc, repr(self.name_tokens), self.id, repr(self.bit_groups), repr(self.bits), self.primitive,
				grammar
			),
			";".join('CLASSES[%s].fields[%s] = %s' % (repr(self.name), repr(field), self.fields[field].toPythonExpr()) for field in self.fields)
		)
	def addField(self, name, field):
		self.fields[name] = field
	def addSelectionRule(self, rule):
		self.selection_rules.append(rule)
	def newInstance(self, name=None, bitsOn=set(), bitsOff=set(), name_tokens=None):
		srules = []
		for clazz in self.superclasses():
			srules += clazz.selection_rules
		return RObject(self, name, (self.allBits()|bitsOn)-bitsOff, name_tokens=name_tokens, srules=srules)
	def superclasses(self):
		if self.superclass == None:
			return [self]
		else:
			return [self] + self.superclass.superclasses()
	def subclasses(self):
		ans = [self]
		for subclass in self.direct_subclasses:
			ans += subclass.subclasses()
		return ans
	def allBits(self):
		bit_groups = []
		for clazz in self.superclasses():
			for bg in clazz.bit_groups:
				bit_groups.append(set(bg[1]))
		
		ans = set()
		for clazz in reversed(self.superclasses()):
			for bit in clazz.bits:
				for bit_group in bit_groups:
					if bit in bit_group:
						ans -= bit_group
						break
				ans |= {bit}
		return ans
	def nameToCode(self, bits):
		if self.name_tokens:
			return nameToCode(self.name_tokens, rbits={"nimento", "yksikkö"}, bits=bits)
		else:
			return self.name + "{" + ",".join(bits) + "}"

class RField:
	def __init__(self, counter, name, vtype, defa=None, is_map=False):
		self.id = counter
		self.name = name
		self.type = vtype
		self.is_map = is_map
		self.default_value = defa
	def toPythonExpr(self):
		defa = "None" if not self.default_value else self.default_value.toPythonRef()
		return 'RField(%d, %s, CLASSES[%s], %s, %s)' % (self.id, repr(self.name), repr(self.type.name), defa, repr(self.is_map))
	def setDefaultValue(self, defa):
		self.default_value = defa
	def copy(self):
		return RField(self.id, self.name, self.type, None, self.is_map)

class RPattern:
	def __init__(self, rclass=None, bitsOn=None, bitsOff=None, conditions=None, obj=None):
		self.rclass = rclass
		self.conditions = conditions or []
		self.my_bitsOn = bitsOn or set()
		self.my_bitsOff = bitsOff or set()
		self.obj = obj
	def toPython(self):
		clazz = "None" if not self.rclass else "CLASSES[" + repr(self.rclass.name) + "]"
		obj = "None" if not self.obj else self.obj.toPythonRef()
		return ("RPattern(" + clazz + ", "
			+ repr(self.my_bitsOn) + ", " + repr(self.my_bitsOff)
			+ ", " + toPython(self.conditions) + ", " + obj + ")")
	def addCondition(self, cond):
		self.conditions.append(cond)
		return self
	def bitOn(self, bit):
		self.my_bitsOn.add(bit)
		return self
	def bitOff(self, bit):
		self.my_bitsOff.add(bit)
		return self
	def bitsOff(self, bits):
		for bit in bits:
			self.bitOff(bit)
		return self
	def newInstance(self, name):
		name_str = tokensToString(name)
		if self.obj:
			obj = self.obj
			obj.bitsOff(self.my_bitsOff)
			obj.bitsOn(self.my_bitsOn)
		else:
			obj = self.rclass.newInstance(name=name_str, name_tokens=name, bitsOn=self.my_bitsOn, bitsOff=self.my_bitsOff)
		for cond in self.conditions:
			cond.doModify(obj)
		return obj
	def modify(self, obj):
		if obj.rclass != self.rclass:
			sys.stderr.write("Yritettiin muuttaa " + obj.asString() + " (" + obj.rclass.name + ") tyyppiin " + self.rclass.name + "\n")
		obj.bitsOff(self.my_bitsOff)
		obj.bitsOn(self.my_bitsOn)
		for cond in self.conditions:
			cond.doModify(obj)
	def matches(self, obj):
		if self.obj:
			if not obj == self.obj:
				return False
		if self.rclass:
			if obj.rclass not in self.rclass.subclasses():
				return False
		for cond in self.conditions:
			if not cond.doCheck(obj):
				return False
		return obj.bits >= self.my_bitsOn and not (obj.bits&self.my_bitsOff)
	def type(self):
		return self.rclass or (self.obj and self.obj.rclass) or CLASSES["asia"]

class RCondition:
	def __init__(self, var, check, modify):
		self.var = var
		self.check = check
		self.modify = modify
	def toPython(self):
		return "RCondition(" + repr(self.var) + ", lambda " + self.var + ": " + self.check + ", lambda " + self.var + ": " + self.modify + ")"
	def doCheck(self, x):
		if isinstance(self.check, str):
			return eval(self.check, globals(), {self.var: x})
		else:
			return self.check(x)
	def doModify(self, x):
		if isinstance(self.modify, str):
			return eval(self.modify, globals(), {self.var: x})
		else:
			return self.modify()

CHECKS = {}
MODIFYS = {}

# Näkyvyysalueet ja muuttujat

class RScope(Bits):
	def __init__(self):
		Bits.__init__(self)
		self.variables = {}
	def __repr__(self):
		return "Scope(" + repr(self.variables) + ")"

ALIASES = {}
GLOBAL_SCOPE = RScope()
SCOPE = []
STACK = []
STACK_NAMES = []
ACTION_STACK = [RScope()]

def pushScope():
	SCOPE.append(RScope())
def popScope():
	SCOPE.pop()
def pushStackFrame(name):
	STACK.append(RScope())
	STACK_NAMES.append(name)
def popStackFrame():
	STACK.pop()
	STACK_NAMES.pop()
def pushAction():
	ACTION_STACK.append(RScope())
def popAction():
	ACTION_STACK.pop()
def visibleScopes():
	return [GLOBAL_SCOPE]+SCOPE+STACK[-1:]
def getVar(name):
	for scope in reversed(visibleScopes()):
		if name in scope.variables:
			return scope.variables[name]
	raise Exception("Muuttujaa ei löytynyt: " + name + "(" + repr(visibleScopes()) + ")\n")
def setVar(name, val):
	scopes = visibleScopes()
	for scope in reversed(scopes):
		if name in scope.variables:
			scope.variables[name] = val
			break
	else:
		scopes[-1].variables[name] = val
def setGlobalVar(name, val):
	GLOBAL_SCOPE.variables[name] = val
def putVar(name, val, to_scope_stack=False):
	if to_scope_stack:
		stack = SCOPE
	else:
		stack = visibleScopes()
	stack[-1].variables[name] = val
def addAlias(name, alias):
	if name not in ALIASES:
		ALIASES[name] = []
	ALIASES[name].append(alias)

# Toiminnot

class RAction:
	def __init__(self, name, a_id=None, srules=None):
		self.id = a_id or nextCounter("RAction")
		self.name = name
		
		ACTIONS[self.id] = self
		ACTIONS_BY_NAME[name] = self
		
		self.commands = []
		self.listeners = []
		self.selection_rules = srules or []
	def toPython(self):
		return ";".join([
			"RAction(" + repr(self.name) + ", " + repr(self.id)
			+ ", [" + ", ".join(["(" + toPython(p) + ", " + r + ")" for p, r in self.selection_rules]) + "])"
		] + [
			("GRAMMAR.parseGrammarLine('.PLAYER-CMD ::= %s', "
			+ "FuncOutput(lambda *x: (lambda: "
			+ "ACTIONS[%d].run([p for p, _ in x]), "
			+ "ACTIONS[%d].likeliness([p for p, _ in x]) + sum([p for _, p in x]), "
			+ "', '.join(p.asString() for p, _ in x)"
			+ ")))")
			% (pattern, self.id, self.id) for pattern in self.commands
		])
	def addPlayerCommand(self, pattern):
		self.commands.append(pattern)
	def addSelectionRule(self, params, rule):
		self.selection_rules.append((params, rule))
	def likeliness(self, args):
		ans = 0
		for params, rule in self.selection_rules:
			if allPatternsMatch(args, params):
				ans += evalOrCall(rule, args)
		return ans
	def run(self, args, in_scope=False):
		listeners = []
		for listener in self.listeners:
			if listener.action is self and allPatternsMatch(args, listener.params) and not listener.disabled:
				listeners.append(listener)
		if not in_scope:
			pushAction()
		scope = ACTION_STACK[-1]
		special_case_found = False
		for listener in sorted(listeners, key=lambda l: l.priority):
			if listener.is_general_case and special_case_found:
				continue
			if listener.is_special_case:
				special_case_found = True
			listener.run(args)
			if "stop action" in scope.bits:
				break
		if not in_scope:
			popAction()

def allPatternsMatch(args, params):
	return all([p.matches(obj) for obj, (_, p, _) in zip(args, params)])

ACTIONS = {}
ACTIONS_BY_NAME = {}

class RListener:
	def __init__(self, action, params, priority, is_special_case, is_general_case, body, name=None):
		self.action = action
		self.params = params
		self.priority = priority
		self.is_special_case = is_special_case
		self.is_general_case = is_general_case
		self.body = body
		self.name = name
		self.disabled = False
		ACTION_LISTENERS.append(self)
		action.listeners.append(self)
	def toPython(self):
		return "".join(['RListener(',
			'ACTIONS[', repr(self.action.id), '], ',
			toPython(self.params), ', ',
			repr(self.priority), ', ',
			repr(self.is_special_case), ', ',
			repr(self.is_general_case), ', ',
			'[', ", ".join(["lambda: " + cmd for cmd in self.body]), '], ',
			repr(self.name),
			')'
		])
	def disable(self):
		self.disabled = True
	def run(self, args):
		pushStackFrame(self.action.name)
		for i, ((c, _, _), a) in enumerate(zip(self.params, args)):
			putVar("_" + str(i), a)
		for cmd in self.body:
			if isinstance(cmd, str):
				eval(cmd)
			else:
				cmd()
			if "stop action" in ACTION_STACK[-1].bits:
				break
		popStackFrame()

# jälkimmäinen sarake kertoo, syrjäytyvätkö tämäntyyppiset säännöt, jos toiseksi jälkimmäisessä sarakkeessa vastaava syrjäyttävä sääntö täsmää

LISTENER_PRIORITIES = [
#	 PRE            CASE      POST       PRI SPECIAL GENERAL
	("ennen",       "osanto", "",        20, False,  True),
	("juuri ennen", "osanto", "",        30, False,  True),
	("",            "omanto", "sijasta", 40, True,   True),
	("",            "omanto", "aikana",  50, False,  True),
	("heti",        "omanto", "jälkeen", 60, False,  True),
	("",            "omanto", "jälkeen", 80, False,  True),
]

ACTION_LISTENERS = []

# Merkkijonon luominen

def createStringObj(x):
	return CLASSES["merkkijono"].newInstance().setExtra("str", x)

# Kokonaisluvun luominen

def createIntegerObj(x):
	return CLASSES["kokonaisluku"].newInstance().setExtra("int", x)

# Monikon luominen

def createTupleObj(c, *x):
	return CLASSES[c].newInstance().setExtra("tuple", tuple(x))

# Tulostaminen

prev_was_newline = True
print_buffer = ""

def say(text):
	global prev_was_newline, print_buffer
	if not text:
		return
	if not prev_was_newline:
		print_buffer += " "
	print_buffer += text
	prev_was_newline = text[-1] == "\n"

# Pelin lopettaminen

game_running = False

def endGame():
	global game_running
	game_running = False

# Pelin komentotulkki

from js import term

def playGame(grammar):
	global prev_was_newline, game_running, print_buffer
	game_running = True
	ACTIONS_BY_NAME["pelin alkaminen"].run([])
	term.echo(print_buffer.strip())
	if game_running:
		print_buffer = ""
		prev_was_newline = True
		term.pushTerm(AsyncPlayGame(grammar), "Retki", "[[;grey;]>> ]")

class AsyncPlayGame():
	def __init__(self, grammar):
		self.grammar = grammar
	def interpret(self, line):
		line = line.strip()
		if line == "lopeta peli":
			term.pop()
			return
		
		global prev_was_newline, game_running, print_buffer
		interpretations = [i() for i in self.grammar.matchAll(tokenize(line), "PLAYER-CMD", set())]
		
		if len(interpretations) == 0:
			term.echo("Ei tulkintaa.")
		else:
			# järjestetään tulkinnat todennäköisyyden mukaan
			interpretations_by_probability = defaultdict(list)
			for i in interpretations:
				interpretations_by_probability[i[1]].append(i)
			
			# mikä on suurin todennäköisyys?
			probability = sorted(interpretations_by_probability.keys())[-1]
			alternatives = interpretations_by_probability[probability]
			
			# jos suurimmalla todennäköisyydellä on useita todennäköisiä tulkintoja: kerro käyttäjälle
			# muussa tapauksessa: suorita jokin todennäköisin tulkinta
			if probability >= 0 and len(alternatives) > 1:
				alternatives_set = set(a[2] for a in alternatives)
				
				# useita tulkintoja on, mutta niiden merkkijonoesitys on sama...
				# suoritetaan siis vain joku niistä, sillä niitä ei voi järkevästi erottaa toisistaan
				if len(alternatives_set) == 1:
					alternatives[0][0]()
				else:
					term.echo("En osaa päättää seuraavien välillä:")
					for i, a in enumerate(sorted(alternatives_set)):
						term.echo(str(i + 1) + "." + a)
			else:
				alternatives[0][0]()

		term.echo(print_buffer.strip())
		
		if not game_running:
			term.pop()
			return
		
		print_buffer = ""
		prev_was_newline = True

def startGame(): playGame(GRAMMAR)

