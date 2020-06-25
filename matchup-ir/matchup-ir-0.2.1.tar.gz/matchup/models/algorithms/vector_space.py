"""
    Classic IR model. Vector model are implemented here, based in Interface Model
"""
from math import sqrt

from collections import defaultdict
from typing import List, DefaultDict

from matchup.models.model import IterModel, Term, Vocabulary
from matchup.structure.weighting.tf import DoubleNormalization
from matchup.structure.weighting.idf import InverseFrequency
from matchup.structure.solution import Result


class Vector(IterModel):

    def __init__(self):
        super(Vector, self).__init__()

    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
           Principal method that represents IR vector space model.
        :param query: list of all query terms
        :param vocabulary: data structure that represents the vocabulary
        :return: list of solution -> (document, score)
        """
        query_terms = query.search_input

        self.initialize(query_terms, vocabulary)

        query_repr = self.query_repr(query, vocabulary.idf, vocabulary.tf)

        self.process_vocabulary_query_based(query_terms, vocabulary)

        scores = defaultdict(float)

        while not self.stop():
            doc, doc_repr = self.iter()
            scores[doc] = self.generate_scores(doc_repr, query_repr)

        scores = sorted(scores.items(), key=lambda v: v[1], reverse=True)
        return self.cast_solution(scores)

    @classmethod
    def generate_scores(cls, doc_repr: DefaultDict[str, float], query_repr: DefaultDict[str, float]) -> float:
        """
            Calculate the similarity between one doc and one query by its representations
        :param doc_repr: doc repr
        :param query_repr: query repr
        :return: similarity
        """
        norm_query = 0
        norm_doc = 0
        intern_product = 0

        for key in query_repr.keys():
            intern_product += (doc_repr[key] * query_repr[key])
            norm_doc += doc_repr[key] ** 2
            norm_query += query_repr[key] ** 2

        norm_query = sqrt(norm_query)
        norm_doc = sqrt(norm_doc)

        if norm_doc and norm_query:
            return intern_product / (norm_doc * norm_query)
        else:
            return 0.0
