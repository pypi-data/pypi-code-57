"""
    Module responsible to configure the text representation.
"""

import re
import unicodedata
from typing import List, Set

from matchup.presentation.text import Term, Line


class Sanitizer:
    """
      Responsible to clean and process the text representation.
    """

    def __init__(self, *, stopwords_path: str = None, stemming: bool = False):
        """
            Sanitizer constructor
        :param stopwords_path: Path that contains a file with stopwords. This file can't have special characters.
        """
        self._stopwords = set()
        self._stemmer = None

        self._set_stemming(stemming)

        if stopwords_path:
            self._stopwords_path = stopwords_path
            self._stopwords = self.import_stopwords()

    def sanitize_line(self, line: str, number_line: int) -> List[Term]:
        """
            This function sanitize one line. The number is basically for presentation
        :param line: Complete line to be processed
        :param number_line: number of line
        :return:
        """
        base_line = Line(line, number_line)

        line_cleaned = base_line.content.strip()
        line_cleaned = self.strip_accents(line_cleaned)

        words = line_cleaned.split()
        indexed = self.index_line(words, base_line)

        return indexed

    def import_stopwords(self) -> Set[str]:
        """
            Retrieve stopwords from a file.
        :return: set of stopwords
        """
        with open(self._stopwords_path, mode='r', encoding='utf-8') as file:
            self._stopwords = {line.strip() for line in file}
        return self._stopwords

    def add_stopwords(self, stopwords: Set[str]):
        """
            Add a set of stopwords manually.
        :param stopwords: set of stopwords.
        :return:
        """
        self._stopwords = self._stopwords.union(stopwords)

    @property
    def stopwords_path(self) -> str:
        """
            Property that get the stopwords file path
        :return: Complete stopwords file path
        """
        return self._stopwords_path

    @stopwords_path.setter
    def stopwords_path(self, path: str) -> None:
        """
            Property setter stopwords path
        :param path: New stopwords path
        :return: None
        """
        self._stopwords_path = path

    def is_stemmig(self):
        return self._stemmer is not None

    def index_line(self, words: List[str], base_line: Line) -> List[Term]:
        """
            This function index one line and returning all words sanitized
            The list must be sorted by occurrence in text!
        :param words: base-line stripped and without stopwords
        :param base_line: line to be sanitized
        :return: list of indexed words : list(Term)
        """

        filtered = self._filter_stopwords(words)
        base_line_stripped = Sanitizer.strip_accents(base_line.content).lower()

        indexed_words = []

        acc_value = 0
        for word in filtered:

            word_position = base_line_stripped[acc_value::].find(word)
            acc_value += word_position

            position = str(base_line.number) + "-" + str(acc_value)

            indexed_words.append(Term(self._stemmer.stem(word) if self._stemmer else word, position))

            acc_value += len(word)

        return indexed_words

    @staticmethod
    def strip_accents(text: str) -> str:
        """
            Strip accents of one text
        :param text: old text
        :return: text sanitized
        """
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
        return str(text)

    @staticmethod
    def _remove_special_chars_lower(word: str) -> str:
        """
            Given an word, this function clean this string, removing the special chars
        :param word: string to be sanitized
        :return:
        """
        return re.sub('[^a-zA-Z0-9áéíóúàèìòùãõâêîôû\\-\n]', '', word).lower()

    def _filter_stopwords(self, words: List[str]) -> List[str]:
        filtered = list()
        for word in words:
            cleaned_word = self._remove_special_chars_lower(word)
            if cleaned_word and cleaned_word not in self._stopwords:
                filtered.append(cleaned_word)
        return filtered

    def _set_stemming(self, stemming):
        if stemming:
            from nltk.stem import PorterStemmer
            self._stemmer = PorterStemmer()
