"""
    IR modern model. Combination with Boolean and Vector Space concepts.
"""

from math import pow

from typing import List
from collections import defaultdict

from matchup.presentation.text import Term
from matchup.models.model import IterModel, Vocabulary


class ExtendedBoolean(IterModel):

    def __init__(self, p: float):
        super(ExtendedBoolean, self).__init__()
        self.p = p

    def run(self, query, vocabulary: Vocabulary):
        """
            Needs weighting <TF <TermFrequency> x IDF <InverseFrequency>>
        :param query:
        :param vocabulary:
        :return:
        """
        query_terms = query.search_input

        self.initialize_occurrences(query_terms, vocabulary)
        self.initialize_pointers()

        self._term_occurrences = self.process_vocabulary_query_based(query_terms, vocabulary)

        scores = defaultdict(float)

        while not self.stop():
            doc, doc_repr = self.iter()
            scores[doc] = self.generate_scores(doc_repr, len({term.word for term in query_terms}))  # group keys

        scores = sorted(scores.items(), key=lambda v: v[1], reverse=True)
        return self.cast_solution(scores)

    def generate_scores(self, doc_repr, m) -> float:
        """
            Generate scores with Extended Boolean Model
        :param doc_repr: vector that represents one scores of terms in one document
        :param m: size of query (group by key)
        :return:
        """
        score = 0.0
        for key in doc_repr:
            score += pow((1 - doc_repr[key]), self.p)
            
        compensation = m - len(doc_repr)
        if compensation:
            score += compensation

        score /= m

        try:
            score = pow(score, 1/self.p)
        except ValueError:
            score = 0.0

        return 1.0 - score






