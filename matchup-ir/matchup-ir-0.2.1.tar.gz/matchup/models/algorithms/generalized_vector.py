"""
    IR modern model. Vector space concepts considering term co-relations
"""
from typing import List, DefaultDict, Set, Tuple
from collections import defaultdict, namedtuple
from math import sqrt
from operator import add

from matchup.models.model import IterModel
from matchup.presentation.text import Term
from matchup.structure.solution import Result
from matchup.structure.vocabulary import Vocabulary

Correlation = namedtuple("Correlation", "keyword cir")
Minterm = namedtuple("Minterm", "correlations id")


class GeneralizedVector(IterModel):
    """
        Class that implements the 'run' method of Generalized Vector IR model.
    """
    def __init__(self):
        super(GeneralizedVector, self).__init__()
        self.minterms = list()

    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
            Run generalized vector model.
        :param query: List of terms.
        :param vocabulary: Vocabulary with a collection.
        :return: Query results
        """

        query_terms = query.search_input

        self.initialize(query_terms, vocabulary)
        self.process_vocabulary_query_based(query_terms, vocabulary)

        query_weight = self.query_repr(query, vocabulary.idf, vocabulary.tf)

        actived_minterms = self.__reduce_correlations(self.__map_correlations(query_weight, vocabulary))

        term_repr, base_len = self.term_repr(actived_minterms)

        doc_repr = self.generalized_doc_repr(term_repr, base_len)
        query_repr = self.generalized_query_repr(query_weight, term_repr, base_len)

        scores = defaultdict(float)
        for doc in doc_repr:
            scores[doc] = self.generalized_calculate(doc_repr[doc], query_repr)

        scores = sorted(scores.items(), key=lambda v: v[1], reverse=True)
        return self.cast_solution(scores)

    @classmethod
    def generalized_calculate(cls, doc: List[float], query: List[float]) -> float:
        """
            Calculate the similarity based on cosine of two vectors: doc vector and query vector.
        :param doc: doc vector
        :param query: query vector
        :return: score of doc
        """
        norm_doc = 0
        norm_query = 0

        for i in range(len(doc)):
            norm_doc += doc[i] ** 2
            norm_query += query[i] ** 2

        norm_query = sqrt(norm_query)
        norm_doc = sqrt(norm_doc)

        intern_prod = 0
        for i in range(len(doc)):
            intern_prod += doc[i] * query[i]

        try:
            cos = intern_prod / (norm_query * norm_doc)
        except:
            cos = 0.0

        return cos

    def generalized_doc_repr(self, term_repr: DefaultDict[str, List[float]], base_len: int) \
            -> DefaultDict[str, List[float]]:
        """
            Generate vectors for all documents.
        :param term_repr: vector of all keys
        :param base_len: len of these vectors
        :return: All document representations
        """
        doc_repr = defaultdict(lambda: [0]*base_len)
        for key in self._term_occurrences:
            for oc in self._term_occurrences[key]:
                kv = list(map(lambda x: x * oc.score, term_repr[key]))
                doc_repr[oc.doc()] = list(map(add, doc_repr[oc.doc()], kv))
        return doc_repr

    @classmethod
    def generalized_query_repr(cls, query_weight: DefaultDict[str, float],  term_repr: DefaultDict[str, List[float]],
                               base_len: int) -> List[float]:
        """
            Generate query vector.
        :param query_weight: query weighting based in keys.
        :param term_repr: term vectors
        :param base_len: base len of term vectors
        :return:
        """
        query_repr = [0]*base_len
        for key in query_weight.keys():
            kv = list(map(lambda x: x * query_weight[key], term_repr[key]))
            query_repr = list(map(add, query_repr, kv))
        return query_repr

    @classmethod
    def term_repr(cls, minterms: List[Minterm]) -> Tuple[DefaultDict[str, List[float]], int]:
        """
            Generate vectors for all terms based in minterms.
        :param minterms:
        :return:
        """
        term_repr = defaultdict(lambda: [0.0]*len(minterms))
        normalization = defaultdict(float)

        count = 0
        for minterm in sorted(minterms, key=lambda x: x.id):
            for correlation in minterm.correlations:
                term_repr[correlation.keyword][count] = correlation.cir
                normalization[correlation.keyword] += correlation.cir**2
            count += 1

        for term in term_repr:
            norm = normalization[term] if normalization[term] != 0 else 1.0
            term_repr[term] = [score / sqrt(norm) for score in term_repr[term]]

        return term_repr, len(minterms)

    @classmethod
    def __map_correlations(cls, query_repr: DefaultDict[str, float], vocabulary: Vocabulary) \
            -> DefaultDict[str, Set[Correlation]]:
        """
            For each document, get the set of minterms that includes it based in query keywords.
        :param query_repr:
        :param vocabulary:
        :return:
        """
        doc_correlations = defaultdict(set)
        for kw in query_repr.keys():
            documents = [(occ.doc(), occ.score) for occ in vocabulary[kw]] if kw in vocabulary else []
            for doc in documents:
                doc_correlations[doc[0]].add(Correlation(kw, doc[1]))
        return doc_correlations

    @classmethod
    def __reduce_correlations(cls, mapped_correlations: DefaultDict[str, Set[Correlation]]) -> List[Minterm]:
        """
            Reduce the mapped collections structure
        :param mapped_correlations:
        :return:
        """
        results = list()
        mtid = 0
        for doc in mapped_correlations:
            element = mapped_correlations[doc]  # elem = set(correlation)
            flag = True
            for result in results:
                if cls.__compare_minterm(result[0], element):
                    flag = False
                    new_correlations = cls.__join(result[0], mapped_correlations[doc])
                    results[results.index(result)] = Minterm(new_correlations, result[1])
            if flag:
                results.append(Minterm(element, mtid))
                mtid += 1
        return results

    @classmethod
    def __compare_minterm(cls, first: Set[Correlation], second: Set[Correlation]) -> bool:
        """
            True if two minterms are similar.
        :param first: first Minterm
        :param second: second Minterm
        :return: Flag that indicates the comparison result.
        """
        return {correlation.keyword for correlation in first} == \
                        {correlation.keyword for correlation in second}

    @classmethod
    def __join(cls, actual: Set[Correlation], other: Set[Correlation]) -> Set[Correlation]:
        """
            Join two minterms.
        :param actual: actual minterm
        :param other: other minterm
        :return:  (actual + other) minterm
        """
        r = set()
        for act_cor in actual:
            for oth_cor in other:
                if oth_cor.keyword == act_cor.keyword:
                    r.add(Correlation(act_cor.keyword, act_cor.cir + oth_cor.cir))
        return r
