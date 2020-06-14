"""
treg utilizes trie structured regex patterns to search texts for a potientially large number of words and phrases.

Basic Example::

    from Treg import Treg

    # Initialize a new pattern
    treg = Treg()
    # Add some phrases
    treg.add_phrases([
        Phrase(phrase='afternoon tea', meta={'fun': 1}),
        Phrase(phrase='tea party', meta={'fun': 3}),
        # ...
    ])
    # Compile the pattern
    treg.compile()
    # Happy searching!
    for match in treg.find_iter(
            "A long collection of afternoon tea party recipes ...",
            overlapped=True):
        print(match)

    # Output
    Match(phrases=[Phrase(phrase='afternoon tea', meta={'fun': 1})], start=16, end=29)
    Match(phrases=[Phrase(phrase='tea party', meta={'fun': 3})], start=26, end=35)
"""

from typing import List, Dict, Iterator, Iterable, Optional
from dataclasses import dataclass
import regex as re
import pickle


@dataclass()
class Phrase:
    """ Data class for search phrases.

        :param phrase: the phrase to be searched for
        :param meta: additional meta data to be returned together with the phrase if found
        :type phrase: str
        :type meta: dict
    """
    phrase: str
    meta: Optional[dict] = None


@dataclass()
class Match:
    """ Data class for found search phrases. Each match refers to a specific snippet of the searched text and all
    phrases that match that snippet.

    :param phrases: matching phrases
    :param start: start character offset
    :param end:  end character offset
    :type phrases: List[Phrase]
    :type start: int
    :type end: int
    """
    phrases: List[Phrase]
    start: int
    end: int


class Treg:
    """
    Treg base class

    :param token_pattern: regex pattern used to differentiate between tokens and whitespace
    :param optional_ws: whether or not to threat whitespaces inside search phrases as optional
    :type token_pattern: str
    :type optional_ws: bool
    """
    _BOUNDARY = object()

    def __init__(self, token_pattern: str = r'\w+', optional_ws: bool = False):
        self._trie = {}
        self._groups = {}   # norm:group
        self._phrases = {}  # group:phrase
        self._token_pattern = re.compile(token_pattern)
        self._ws = ' ?' if optional_ws else ' '
        self.pattern = None

    def _tokenize_text(self, text: str) -> (List[str], Dict[int, int]):
        tokens = []
        offset_map = {}
        norm_offset = 0
        for match in re.finditer(self._token_pattern, text):
            token = match.group()
            tokens.append(token)
            offset_map[norm_offset] = match.start()
            norm_offset += len(token) + 1
        return tokens, offset_map

    def find_iter(self, text: str, overlapped: bool = False) -> Iterator[Match]:
        """ Find search phrases within text. Note that the pattern needs to be compiled first.

            :param text: text to be searched
            :param overlapped: whether overlapping matches or only the left most match should be returned.
                The latter is default.
            :returns: Iterator of found phrases (matches)
            :rtype: Iterator[Match]
        """
        if not self.is_compiled():
            raise TypeError("The pattern needs to be compiled before it can be used for searching.")
        tokens, offset_map = self._tokenize_text(text)
        for match in re.finditer(self.pattern, ' '.join(tokens), overlapped=overlapped):
            start = offset_map[match.start()]
            end = start + len(match.group())
            group = int(match.lastgroup[1:])
            phrases = self._phrases[group]
            yield Match(phrases, start, end)

    def add_phrases(self, phrases: Iterable[Phrase]):
        """ Add multiple phrases at once. See :func:`~add_phrase`.

        :param phrases: Iterable of phrases to be searched for
        """
        for phrase in phrases:
            self.add_phrase(phrase)

    def add_phrase(self, phrase: Phrase):
        """ Add a phrase to be searched for. Note that phrases can only be added
        as long as the pattern is not compiled.

        :param phrase: phrase to be searched for
        """
        if self.is_compiled():
            raise TypeError("An already compiled pattern cannot be modified.")
        norm = self._ws.join(re.findall(self._token_pattern, phrase.phrase))
        node = self._trie
        for char in norm:
            node = node.setdefault(char, {})
        group = self._groups.setdefault(norm, len(self._groups))
        node[self._BOUNDARY] = group
        self._phrases.setdefault(group, []).append(phrase)

    def is_compiled(self):
        """ Return whether the pattern is already compiled. """
        return self.pattern is not None

    def compile(self):
        """ Compile the pattern. Once compiled :func:`~find_iter` can be used to search texts.
        Note that a compiled pattern can't be modified anymore.
        Depending on the number of search phrases compiling can take a while.
        """
        pattern = self._node_to_pattern(self._trie)
        self.pattern = re.compile(pattern)
        # we don't need those attributes anymore
        del self._trie
        del self._groups

    def _node_to_pattern(self, node: dict) -> str:
        subpattern = '|'.join(
            char + self._node_to_pattern(child) if char is not self._BOUNDARY else fr'(?P<_{node[char]}>(?=( |$)))'
            for char, child in sorted(node.items(), key=lambda c: 1 if c[0] is self._BOUNDARY else 0)
        )
        if len(node) > 1:
            subpattern = f'(?:{subpattern})'
        return subpattern

    def save(self, path: str):
        """ Save the Treg object to a file using pickle.
        Note that in order to pickle a Treg object all Phrases in particular their meta data needs to be pickleable.

        :param path: file path
        :type path: str
        """
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> 'Treg':
        """ Load a previously saved / pickled Treg object.

        :param path: file path
        :type path: str
        :returns: Treg object
        :type: Treg
        """
        with open(path, 'rb') as f:
            treg = pickle.load(f)
        if not isinstance(treg, cls):
            raise TypeError(f'{path} has to be a pickle dump of {cls} not {type(treg)}')
        return treg
