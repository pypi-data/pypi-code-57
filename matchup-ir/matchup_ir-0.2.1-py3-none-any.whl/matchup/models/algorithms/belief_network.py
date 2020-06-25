"""
    Belief Network module.
    Defines a IR modern model network-based. Classic probabilistic and vector space concepts are important here.
"""

from math import sqrt
from typing import List, DefaultDict
from collections import defaultdict

from matchup.models.model import IterModel, Term, Result, Vocabulary


class BeliefNetwork(IterModel):

    def __init__(self):
        super(BeliefNetwork, self).__init__()

    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
            Belief Network algorithm.
        :param query: list of all query terms
        :param vocabulary: data structure that represents the vocabulary
        :return: list of solution -> (document, score)
        """

        query_terms = query.search_input

        self.initialize(query_terms, vocabulary)  # initialize query and vocabulary pointers

        query_repr = self.query_repr(query, vocabulary.idf, vocabulary.tf)  # generate first query abstraction

        self.process_vocabulary_query_based(query_terms, vocabulary)  # process vocabulary based in query keywords

        scores = defaultdict(float)

        t = len(self._term_occurrences) if len(self._term_occurrences) <= 10 else 10

        prob_k = (1/2) ** t  # prob_k : belief_network model.

        while not self.stop():
            doc, doc_repr = self.iter()   # pointer-based document choose
            scores[doc] = self.generate_scores(doc_repr, query_repr, prob_k)  # generate score : belief_network

        scores = sorted(scores.items(), key=lambda v: v[1], reverse=True)
        return self.cast_solution(scores)

    @classmethod
    def generate_scores(cls, doc_repr: DefaultDict[str, float], query_repr: DefaultDict[str, float], prob_k: float)\
            -> float:
        """
            Calculate similarity between one document and query based in Belief Network IR model.
        :param doc_repr: Document vector space representation
        :param query_repr: Query vector space representation
        :param prob_k: Probability that a random key 'k' is relevant
        :return Relevant score of document based in query.
        """
        wij_square_sum = 0.0
        for key in doc_repr.keys():
            wij_square_sum += doc_repr[key] ** 2
        wij_square_sum = sqrt(wij_square_sum)

        wiq_square_sum = 0.0
        for key in query_repr.keys():
            wiq_square_sum += query_repr[key] ** 2
        wiq_square_sum = sqrt(wiq_square_sum)

        score = 0.0
        for key in doc_repr.keys():
            prob_query = query_repr[key] / wiq_square_sum if wiq_square_sum != 0.0 else 0.0
            prob_document = doc_repr[key] / wij_square_sum if wij_square_sum != 0.0 else 0.0
            score += prob_document * prob_query * prob_k

        return score

