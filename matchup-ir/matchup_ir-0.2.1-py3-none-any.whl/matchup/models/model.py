"""
    First abstraction that represents IR models
        Model, IterModel
"""

import abc

from typing import List, Tuple, DefaultDict
from collections import defaultdict

from matchup.structure.solution import Result
from matchup.structure.vocabulary import Vocabulary
from matchup.structure.occurrence import Occurrence

from matchup.presentation.text import Term


class NoSuchModelException(RuntimeError):
    pass


class ModelExecutionError(RuntimeError):
    pass


class Model(abc.ABC):
    """
        IR Models base class.
    """

    @abc.abstractmethod
    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
            Define the principal method of IR models.
        :param query: List of all entry terms
        :param vocabulary: Vocabulary pre-processed
        :return:
        """
        ...

    @classmethod
    def cast_solution(cls, structure: List[tuple]) -> List[Result]:
        return [Result(item[0], round(item[1], 3)) for item in structure]

    @classmethod
    def process_vocabulary_query_based(cls, query: List[Term], vocabulary: Vocabulary) \
            -> DefaultDict[str, List[Occurrence]]:
        """
            Generate document scores based in query
        :param query: query representation
        :param vocabulary: vocabulary structure
        :return: List of occurrences
        """
        target = defaultdict(list)

        idf = vocabulary.idf
        tf = vocabulary.tf

        maximum_frequencies_per_document = vocabulary.maximum_frequencies_per_document()

        for key in query:
            if key.word in vocabulary:
                occurrences = vocabulary[key.word]
                for occurrence in occurrences:
                    score = idf[key.word] * \
                            tf.calculate(key.word, occurrence, maximum_frequencies_per_document[occurrence.doc()])
                    occurrence.score = score
                target[key.word] = occurrences
        return target


class IterModel(Model):
    """
        Describe one variation of Model classes : IterModel classes have some features for help his works
        Pointers and occurrences are implemented here.
    """

    def __init__(self):
        super(IterModel, self).__init__()
        self._term_occurrences = defaultdict(list)
        self._pointers = defaultdict(int)

    @abc.abstractmethod
    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
            Define the principal method of IR models.
        :param query: List of all entry terms
        :param vocabulary: Vocabulary pre-processed
        :return:
        """
        ...

    def initialize(self, query: List[Term], vocabulary: Vocabulary):
        """
            Initialize query-based
        """
        self.initialize_occurrences(query, vocabulary)
        self.initialize_pointers()

    def iter(self) -> Tuple[str, DefaultDict[str, float]]:
        """
            Define one iteration of this iter model algorithm
        :return: doc, doc_repr (keyword -> score)
        """
        doc = self.next_doc()
        doc_repr = self.doc_repr(doc)
        return doc, doc_repr

    def doc_repr(self, doc: str) -> DefaultDict[str, float]:
        """
            Process doc generating it representation
        :param doc: Str represents the lowest document
        :return: doc repr. Dictionary with all term scores by doc. That is the document vector.
        """
        doc_repr = defaultdict(float)
        for key in self._term_occurrences.keys():
            try:
                occ = self._term_occurrences[key][self._pointers[key]]
                if occ.doc() == doc:
                    self._pointers[key] += 1
                    doc_repr[key] = occ.score
            except ValueError:
                continue
            except IndexError:
                continue
        return doc_repr

    def initialize_occurrences(self, query: List[Term], vocabulary: Vocabulary) -> None:
        """
            Create another data structure _term_occurrences that represents the vocabulary with just query
            keywords.
        :param query: original query
        :param vocabulary: original vocabulary
        :return: None
        """
        for key in query:
            if key.word in vocabulary:
                self._term_occurrences[key.word] = vocabulary[key.word]
                
    def initialize_pointers(self) -> None:
        """
            Initialize pointers to model algorithm
        :return: None
        """
        for query_term in self._term_occurrences.keys():
            self._pointers[query_term] = 0

    def next_doc(self) -> str:
        """
            Return the lowest doc pointer by pointers
        :return: lowest document
        """
        lowest = None
        for key in self._term_occurrences.keys():
            try:
                doc = self._term_occurrences[key][self._pointers[key]].doc()
                if lowest and doc < lowest:
                    lowest = doc
                elif not lowest:
                    lowest = doc
            except ValueError:
                continue
            except IndexError:
                continue
        return lowest

    def stop(self) -> bool:
        """
            Given a dictionary with all pointers by keyword and another dictionary with all occurrences by keyword,
            this function calculate if the algorithm is over
        :return: boolean flag indicates if algorithm stops
        """
        for key in self._pointers.keys():
            if self._pointers[key] < len(self._term_occurrences[key]):
                return False
        return True

    def process_vocabulary_query_based(self, query: List[Term], vocabulary: Vocabulary) \
            -> DefaultDict[str, List[Occurrence]]:
        """
            Generate document scores based in query
        :param query: query representation
        :param vocabulary: vocabulary structure
        :return: List of occurrences
        """
        self._term_occurrences = super().process_vocabulary_query_based(query, vocabulary)
        return self._term_occurrences

    @classmethod
    def query_repr(cls, query, vocabulary_idf, vocabulary_tf) -> DefaultDict[str, float]:
        """
            Construct query representation
        :param query: list of all terms
        :param vocabulary_idf: structure IDF for vocabulary
        :param vocabulary_tf: structure TF for vocabulary
        :return: query representation
        """
        maximum_frequency = 0
        occurrences = dict()

        query_terms = query.search_input
        query_tf = query.tf if query.tf else vocabulary_tf
        query_idf = query.idf if query.idf else vocabulary_idf

        for term in query_terms:
            if term.word in occurrences:
                occurrences[term.word].add()
            else:
                occurrences[term.word] = Occurrence()
            f = occurrences[term.word].frequency
            maximum_frequency = f if f > maximum_frequency else maximum_frequency

        query_repr = defaultdict(float)
        for key in query_terms:
            query_repr[key.word] = query_idf[key.word] * query_tf.calculate(key.word, occurrences[key.word],
                                                                            maximum_frequency, persist=False)
        return query_repr
