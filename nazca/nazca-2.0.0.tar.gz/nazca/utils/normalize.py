# -*- coding:utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import re
from string import punctuation
from unicodedata import normalize as _uninormalize
from functools import partial

FRENCH_STOPWORDS = set(
    [
        "alors",
        "au",
        "aux",
        "aucuns",
        "aussi",
        "autre",
        "avant",
        "avec",
        "avoir",
        "bon",
        "car",
        "ce",
        "cela",
        "ces",
        "ceux",
        "chaque",
        "ci",
        "comme",
        "comment",
        "dans",
        "de",
        "des",
        "du",
        "dedans",
        "dehors",
        "depuis",
        "deux",
        "devrait",
        "doit",
        "donc",
        "dos",
        "droite",
        "début",
        "elle",
        "elles",
        "en",
        "encore",
        "essai",
        "est",
        "et",
        "eu",
        "eux",
        "fait",
        "faites",
        "fois",
        "font",
        "force",
        "haut",
        "hors",
        "ici",
        "il",
        "ils",
        "je",
        "juste",
        "la",
        "le",
        "les",
        "leur",
        "lui",
        "là",
        "ma",
        "maintenant",
        "mais",
        "me",
        "mes",
        "moi",
        "moins",
        "mon",
        "mot",
        "même",
        "ne",
        "ni",
        "nommés",
        "nos",
        "notre",
        "nous",
        "nouveaux",
        "on",
        "ou",
        "où",
        "par",
        "parce",
        "parole",
        "pas",
        "personnes",
        "peut",
        "peu",
        "pièce",
        "plupart",
        "pour",
        "pourquoi",
        "quand",
        "que",
        "quel",
        "quelle",
        "quelles",
        "quels",
        "qui",
        "sa",
        "sans",
        "se",
        "ses",
        "seulement",
        "si",
        "sien",
        "son",
        "sont",
        "sous",
        "soyez",
        "sujet",
        "sur",
        "ta",
        "tandis",
        "tellement",
        "te",
        "tels",
        "tes",
        "toi",
        "ton",
        "tous",
        "tout",
        "trop",
        "très",
        "tu",
        "un",
        "une",
        "valeur",
        "voie",
        "voient",
        "vont",
        "vos",
        "votre",
        "vous",
        "vu",
        "ça",
        "étaient",
        "état",
        "étions",
        "été",
        "être",
    ]
)

MANUAL_UNICODE_MAP = {
    "\xa1": "!",  # INVERTED EXCLAMATION MARK
    "\u0142": "l",  # LATIN SMALL LETTER L WITH STROKE
    "\u2044": "/",  # FRACTION SLASH
    "\xc6": "AE",  # LATIN CAPITAL LETTER AE
    "\xa9": "(c)",  # COPYRIGHT SIGN
    "\xab": '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\xe6": "ae",  # LATIN SMALL LETTER AE
    "\xae": "(r)",  # REGISTERED SIGN
    "\u0153": "oe",  # LATIN SMALL LIGATURE OE
    "\u0152": "OE",  # LATIN CAPITAL LIGATURE OE
    "\xd8": "O",  # LATIN CAPITAL LETTER O WITH STROKE
    "\xf8": "o",  # LATIN SMALL LETTER O WITH STROKE
    "\xbb": '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\xdf": "ss",  # LATIN SMALL LETTER SHARP S
    "\u2019": "'",  # RIGHT SINGLE QUOTATION MARK
}


###############################################################################
# NORMALIZE FUNCTIONS #########################################################
###############################################################################
def unormalize(ustring, substitute=None):
    """replace diacritical characters with their corresponding ascii characters

    Convert the unicode string to its long normalized form (unicode character
    will be transform into several characters) and keep the first one only.
    The normal form KD (NFKD) will apply the compatibility decomposition, i.e.
    replace all compatibility characters with their equivalents.

    :type substitute: str
    :param substitute: replacement character to use if decomposition fails

    :see: Another project about ASCII transliterations of Unicode text
          http://pypi.python.org/pypi/Unidecode
    """
    res = []
    for letter in ustring[:]:
        try:
            replacement = MANUAL_UNICODE_MAP[letter]
        except KeyError:
            if isinstance(letter, str):
                replacement = _uninormalize("NFKD", letter)[0]
            else:
                replacement = letter
            if ord(replacement) >= 2 ** 7:
                if substitute is None:
                    raise ValueError("can't deal with non-ascii based characters")
                replacement = substitute
        res.append(replacement)
    return "".join(res)


def lunormalize(sentence, substitute=None):
    """ Normalize a sentence (ie remove accents, set to lower, etc) """
    return unormalize(sentence, substitute).lower()


def simplify(sentence, lemmas=None, remove_stopwords=True, stopwords=FRENCH_STOPWORDS):
    """ Simply the given sentence
        0) If remove_stopwords, then remove the stop words
        1) If lemmas are given, the sentence is lemmatized
        2) Set the sentence to lower case
        3) Remove punctuation
    """
    if not isinstance(sentence, str):
        return sentence

    if lemmas:
        sentence = lemmatized(sentence, lemmas)
    sentence = sentence.lower()
    cleansent = "".join([s if s not in punctuation else " " for s in sentence]).strip()
    # comma followed by a space is replaced by two spaces, keep only one
    cleansent = cleansent.replace("  ", " ")

    if not remove_stopwords:
        return cleansent
    else:
        return " ".join([w for w in cleansent.split(" ") if w not in stopwords])


def tokenize(sentence, tokenizer=None, regexp=re.compile(r"[^\s]+")):
    """ Tokenize a sentence.
        Use ``tokenizer`` if given, else try to use the nltk WordPunctTokenizer,
        in case of failure, it just split on spaces.

        Anyway, tokenizer must have a ``tokenize()`` method
    """
    if tokenizer:
        return tokenizer().tokenize(sentence)
    # XXX Unicode, could not use WorkTokenizer.
    # Instead split on whitespaces
    chunks = []
    for chunk in (t for t in regexp.findall(sentence) if t):
        # Deals with '
        if "'" in chunk:
            schunks = chunk.split("'")
            chunks.extend([c + "'" for c in schunks[:-1]])
            chunks.append(schunks[-1])
        else:
            chunks.append(chunk)
    return chunks


def lemmatized(sentence, lemmas, tokenizer=None):
    """ Return the lemmatized sentence
    """
    tokenized_sent = tokenize(sentence, tokenizer)
    tokenized_sentformated = []
    for w in tokenized_sent:
        if w in ".,'" and len(tokenized_sentformated) > 0:
            tokenized_sentformated[-1] += w
        elif w not in punctuation:
            tokenized_sentformated.append(w)
    return " ".join([lemmatized_word(w, lemmas) for w in tokenized_sentformated])


def lemmatized_word(word, lemmas):
    """ Return the lemmatized word
    """
    lemma = lemmas.get(word.lower(), word)
    if "|" in lemma:
        _words = lemma.split("|")
        if word.lower() in _words:
            lemma = word.lower()
        else:
            lemma = _words[0]
    return lemma


def roundstr(number, ndigits=0):
    """Return an unicode string of ``number`` rounded to a given precision
        in decimal digits (default 0 digits)

        If ``number`` is not a float, this method casts it to a float. (An
        exception may be raised if it's not possible)
    """
    return format(round(float(number), ndigits), "0.%df" % ndigits)


def rgxformat(string, regexp, output):
    r""" Apply the regexp to the ``string`` and return a formatted string
    according to ``output``

    eg :
        format(u'[Victor Hugo - 26 fev 1802 / 22 mai 1885]',
               r'\[(?P<firstname>\w+) (?p<lastname>\w+) - '
               r'(?P<birthdate>.*?) / (?<deathdate>.*?)\]',
               u'%(lastname)s, %(firstname)s (%(birthdate)s -'
               u'%(deathdate)s)')

     would return u'Hugo, Victor (26 fev 1802 - 22 mai 1885)'
     """
    match = re.match(regexp, string)
    return output % match.groupdict()


###############################################################################
# NORMALIZER OBJECTS ##########################################################
###############################################################################
class BaseNormalizer(object):
    """ A normalizer object used to provide an abstraction over the different
    normalization functions, and help building Nazca process. """

    def __init__(self, callback, attr_index=None):
        """ Initiate the BaseNormalizer

        Parameters
        ----------
        callback: normalization callback

        attr_index: index of the attribute of interest in a record
                    (i.e. attribute to be normalized).
                    By default, 'attr_index' is None and the whole
                    record is passed to the callback.
                    If given, only the attr_index value of the record
                    is passed to the the callback.
                    Could be a list or an int
        """
        self.callback = callback
        if attr_index is not None:
            self.attr_index = attr_index if isinstance(attr_index, (tuple, list)) else (attr_index,)
        else:
            self.attr_index = attr_index

    def normalize(self, record):
        """ Normalize a record

        Parameters
        ----------
        record: a record (tuple/list of values).

        Returns
        -------

        record: the normalized record.
        """
        if not self.attr_index:
            return self.callback(record)
        else:
            for attr_ind in self.attr_index:
                record = list(
                    r if ind != attr_ind else self.callback(r) for ind, r in enumerate(record)
                )
            return record

    def normalize_dataset(self, dataset, inplace=False):
        """ Normalize a dataset

        Parameters
        ----------
        dataset: a list of record (tuple/list of values).

        inplace: Boolean. If True, normalize the dataset in place.

        Returns
        -------

        record: the normalized dataset.
        """
        if not inplace:
            dataset = [self.normalize(record) for record in dataset]
        else:
            # Change dataset in place
            for ind, record in enumerate(dataset):
                dataset[ind] = self.normalize(record)
        return dataset


class UnicodeNormalizer(BaseNormalizer):
    """ Normalizer that unormalize the unicode
    (i.e. replace accentuating characters by ASCII ones)
    """

    def __init__(self, attr_index=None, substitute=None):
        callback = partial(lunormalize, substitute=substitute)
        super(UnicodeNormalizer, self).__init__(callback, attr_index=attr_index)


class SimplifyNormalizer(BaseNormalizer):
    """ Normalizer that simplify a string
        0) If remove_stopwords, then remove the stop words
        1) If lemmas are given, the sentence is lemmatized
        2) Set the sentence to lower case
        3) Remove punctuation
    """

    def __init__(self, attr_index=None, lemmas=None, remove_stopwords=True):
        callback = partial(simplify, lemmas=lemmas, remove_stopwords=remove_stopwords)
        super(SimplifyNormalizer, self).__init__(callback, attr_index=attr_index)


class TokenizerNormalizer(BaseNormalizer):
    """ Normalizer that tokenize a string
        Use ``tokenizer`` if given, else try to use the nltk WordPunctTokenizer,
        in case of failure, it just split on spaces.
        Anyway, tokenizer must have a ``tokenize()`` method
    """

    def __init__(self, attr_index=None, tokenizer=None, regexp=re.compile(r"[^\s]+")):
        callback = partial(tokenize, tokenizer=tokenizer, regexp=regexp)
        super(TokenizerNormalizer, self).__init__(callback, attr_index=attr_index)


class LemmatizerNormalizer(BaseNormalizer):
    """ Normalizer that lemmatize a string
    """

    def __init__(self, lemmas, attr_index=None, tokenizer=None):
        callback = partial(lemmatized, lemmas=lemmas, tokenizer=tokenizer)
        super(LemmatizerNormalizer, self).__init__(callback, attr_index=attr_index)


class RoundNormalizer(BaseNormalizer):
    """Normalizer that round a string
    Return an unicode string of ``number`` rounded to a given precision
    in decimal digits (default 0 digits)

    If ``number`` is not a float, this method casts it to a float. (An
    exception may be raised if it's not possible)
    """

    def __init__(self, attr_index=None, ndigits=0):
        callback = partial(roundstr, ndigits=ndigits)
        super(RoundNormalizer, self).__init__(callback, attr_index=attr_index)


class RegexpNormalizer(BaseNormalizer):
    r"""Normalizer that normalize a string based on a regexp

     Apply the regexp to the ``string`` and return a formatted string
    according to ``output``

    eg :
        format(u'[Victor Hugo - 26 fev 1802 / 22 mai 1885]',
               r'\[(?P<firstname>\w+) (?p<lastname>\w+) - '
               r'(?P<birthdate>.*?) / (?<deathdate>.*?)\]',
               u'%(lastname)s, %(firstname)s (%(birthdate)s -'
               u'%(deathdate)s)')

     would return u'Hugo, Victor (26 fev 1802 - 22 mai 1885)'
    """

    def __init__(self, regexp, output, attr_index=None):
        callback = partial(rgxformat, regexp=regexp, output=output)
        super(RegexpNormalizer, self).__init__(callback, attr_index=attr_index)


###############################################################################
# JOIN NORMALIZER #############################################################
###############################################################################
class JoinNormalizer(BaseNormalizer):
    """Normalizer that join multiple fields in only one.
    This new field will be put at the end of the new record.
    """

    def __init__(self, attr_indexes, join_car=", "):
        self.attr_indexes = attr_indexes
        self.join_car = join_car

    def normalize(self, record):
        """ Normalize a record

        Parameters
        ----------
        record: a record (tuple/list of values).

        Returns
        -------

        record: the normalized record.
        """
        _record = [r for ind, r in enumerate(record) if ind not in self.attr_indexes]
        _record.append(
            self.join_car.join([r for ind, r in enumerate(record) if ind in self.attr_indexes])
        )
        return _record


###############################################################################
# NORMALIZER PIPELINE #########################################################
###############################################################################
class NormalizerPipeline(BaseNormalizer):
    """ Pipeline of Normalizers
    """

    def __init__(self, normalizers):
        """ Initiate the NormalizerPipeline

        Parameters
        ----------
        normalizers: list (ordered) of Normalizer
        """
        self.normalizers = normalizers

    def normalize(self, record):
        """ Normalize a record

        Parameters
        ----------
        record: a record (tuple/list of values).

        Returns
        -------

        record: the normalized record.
        """
        for normalizer in self.normalizers:
            record = normalizer.normalize(record)
        return record
