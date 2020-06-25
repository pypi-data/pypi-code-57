import re
from typing import Iterable


class PatternTrie:
    """
    Creates a Trie out of a list of words.
    The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union.
    """

    def __init__(self, *words: str):
        self.data = {}
        if words:
            self.add_all(words)

    def add(self, word: str):
        """Add a single word to the pattern"""
        if not word:
            return
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1
        
    def add_all(self, words: Iterable[str]):
        """Add multiple words to the pattern"""
        for word in words:
            self.add(word)

    def dump(self):
        return self.data

    def _escape(self, char):
        return re.escape(char)

    def _pattern(self, pdata):
        data = pdata
        if '' in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self._escape(char) + recurse)
                except:
                    cc.append(self._escape(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = '(?:' + '|'.join(alt) + ')'

        if q:
            if cconly:
                result += '?'
            else:
                result = '(?:%s)?' % result
        return result

    @property
    def pattern(self) -> str:
        """Get pattern created from trie"""
        if len(self.data) == 0:
            raise ValueError('No data to build pattern.')
        return self._pattern(self.dump())
