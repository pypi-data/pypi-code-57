"""
    Module that represents the interface of indexer implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Set, DefaultDict

from matchup.structure.occurrence import Occurrence


class Index(ABC):

    @abstractmethod
    def __str__(self) -> str:
        """
            Simple index string representation
        :return:
        """
        pass

    @abstractmethod
    def __contains__(self, item: str):
        """
            This function enables the user to make the associative operation with 'in'
        :param item: One keyword
        :return:
        """
        pass

    @abstractmethod
    def __getitem__(self, item: str) -> List[Occurrence]:
        """
            Get some occurrences by keyword, or init it on data structure
        :param item: keyword
        :return:
        """
        pass

    def process(self, files: Set[str], **kwargs) -> None:
        """
            This function try to process all content of files that have been inserted before, generating
            the index data structure ready for use.
        :return: None
        """
        pass

    def load(self, **kwargs) -> Set[str]:
        """
            This is a function that recover the index previously generated.
        :return: Set of files that generated its index.
        """
        pass

    def save(self, **kwargs) -> bool:
        """
            Persist data structure on disc.
        :return: boolean flag that indicates if the data structure can be persisted.
        """
        pass

    @property
    @abstractmethod
    def keys(self) -> List[str]:
        """
            Get all keywords presents in vocabulary
        :return: list of all keywords
        """
        pass

    @abstractmethod
    def maximum_frequencies_per_document(self) -> DefaultDict[str, float]:
        """
            Return one dictionary with structure : Document -> Maximum frequency of one term in it document.
        :return:
        """
        pass

    @abstractmethod
    def documents_with_keywords(self, kwds: Set[str]) -> Set[str]:
        """
            Return one set of documents that contains the set of keywords passed with param.
        :param kwds: set of keywords
        :return:
        """
        pass




