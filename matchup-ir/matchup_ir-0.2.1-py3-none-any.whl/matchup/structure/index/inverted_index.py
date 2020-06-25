"""
    Module that implements the index structure to storage and process collections.
"""

import pickle
from os import path
from collections import defaultdict
from typing import List, Set, DefaultDict

from matchup.structure.occurrence import Occurrence
from matchup.structure.index.base_index import Index

from matchup.presentation.sanitizer import Sanitizer
from matchup.presentation.text import Term
from matchup.presentation.formats import ExtensionNotSupported, get_file


class InvertedIndex(Index):
    """
        Simple structure based in a inverted file.
    """
    def __init__(self):
        self._inverted_file = defaultdict(list)

    def __str__(self) -> str:
        """
            Transform an index object in an String
        :return: String that represents the structure of index
        """
        index = ""
        for key in self._inverted_file.keys():
            index += str(key + ":" + str(self._inverted_file[key]) + "\n")
        return index

    def __contains__(self, item: str) -> bool:
        """
            This function enables the user to make the associative operation with 'in'
        :param item: keyword
        :return: boolean flag that return true if the keyword are in index
        """
        return item in self._inverted_file

    def __getitem__(self, item: str) -> List[Occurrence]:
        """
            Get some occurrences by item, or init it on data structure
        :param item: keyword
        :return: Occurrences of keyword
        """
        return self._inverted_file[item]

    def load(self, **kwargs) -> Set[str]:
        """
            This is a function that recover the index previously generated.
            Needs the keyword param 'path' that indicates the path to load the index.
        :return: set of files retrieved
        """
        file_path = kwargs.get("path")
        if file_path and path.exists(file_path):
            self._inverted_file.clear()
            with open(file_path, mode='rb') as file:
                self._inverted_file = pickle.load(file)
                return self.__retrieve_file_names()
        raise FileNotFoundError

    def save(self, **kwargs) -> bool:
        """
            Persist data structure on disc.
            Needs the keyword param 'path' that indicates the path to save the index.
        :return: boolean flag that indicates if the data structure can be persisted.
        """
        file_path = kwargs.get("path")
        if file_path and self._inverted_file:
            self.__sort()
            with open(file_path, mode='wb') as file:
                pickle.dump(self._inverted_file, file)
            return True
        raise ReferenceError("You should to process some collection files")

    @property
    def keys(self) -> list:
        """
            Get all keywords presents in index
        :return: list of all keywords
        """
        return list(self._inverted_file.keys())

    def documents_with_keywords(self, kwds: Set[str]) -> Set[str]:
        answer = list()
        for key in self._inverted_file:
            if key in kwds:
                answer += [oc.doc() for oc in self._inverted_file[key]]

        incomplete = {elem for elem in answer if answer.count(elem) != len(kwds)}

        return set(answer) - incomplete

    def maximum_frequencies_per_document(self) -> DefaultDict[str, float]:
        """
            Return one dictionary with structure : Document -> Maximum frequency of one term in it document.
        :return:
        """
        map_docs = defaultdict(float)
        for key in self._inverted_file:
            for occurrence in self._inverted_file[key]:
                if map_docs[occurrence.doc()] < occurrence.frequency:
                    map_docs[occurrence.doc()] = occurrence.frequency
        return map_docs

    def process(self, files: Set[str], **kwargs) -> None:
        """
            This function try to process all content of files that have been inserted before, generating
            the index data structure ready for use.
            Needs the param 'sanitizer' that indicates the sanitizer object to clean the collection.
        :return: None
        """
        sanitizer = kwargs.get("sanitizer")
        sanitizer = sanitizer if sanitizer else Sanitizer()

        for file_name in files:
            try:
                file = get_file(file_name)
            except ExtensionNotSupported:
                continue
            try:
                text_io = file.open()
                self.__process_file(file_name, text_io, sanitizer)
            except ExtensionNotSupported:
                continue
            finally:
                file.close()

    def __process_file(self, filename, content_file, sanitizer) -> None:
        """
            Process one file line by line
        :param filename: name of file
        :param content_file: text file content
        :param sanitizer: sanitizer object
        :return:
        """
        number_line = 1
        for content_line in content_file:
            terms = sanitizer.sanitize_line(content_line, number_line)
            self.__push(terms, filename)
            number_line += 1

    def __push(self, terms: List[Term], file_name: str) -> None:
        """
            Function that push all file terms in index
        :param terms: list with all file terms
        :param file_name: path of file
        :return: None
        """
        for term in terms:
            try:
                idx = self._inverted_file[term.word].index(file_name)
                occurrence = self._inverted_file[term.word][idx]
                occurrence.add(position=term.position)

            except ValueError:
                occurrence = Occurrence(file_name, term)
                self._inverted_file[term.word].append(occurrence)

    def __retrieve_file_names(self) -> Set[str]:
        """
            Iterate the data structure retrieving the file names that generated it index
        :return: set of files retrieved
        """
        files = set()
        for keyword in self._inverted_file:
            for occurrence in self._inverted_file[keyword]:
                files.add(occurrence.doc())
        return files

    def __sort(self) -> None:
        """
            Order the documents in index structure.
        :return: None
        """
        for key in self._inverted_file:
            self._inverted_file[key] = sorted(self._inverted_file[key], key=Occurrence.doc)
