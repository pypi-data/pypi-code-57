"""
    Classic IR model. Boolean model are implemented here, based in Interface Model
"""

from collections import defaultdict
from typing import DefaultDict

from matchup.models.model import Model, List, Term, Vocabulary
from matchup.structure.solution import Result


class Boolean(Model):

    def __init__(self):
        super(Boolean, self).__init__()

    def run(self, query, vocabulary: Vocabulary) -> List[Result]:
        """
            Principal method that represents IR boolean model.
        :param query: list of all query terms
        :param vocabulary: data structure that represents the vocabulary
        :return: list of solution -> (document, score)
        """

        query_terms = query.search_input

        scores = self.__map_keywords_in_documents(query_terms, vocabulary)

        maximum_points = len(query_terms)

        rank = defaultdict(float)

        for key in scores.keys():
            w_score = sum(scores[key]) / maximum_points
            if w_score != 0.0:
                rank[key] = w_score

        rank = sorted(rank.items(), key=lambda v: v[1], reverse=True)

        return self.cast_solution(rank)

    @classmethod
    def __map_keywords_in_documents(cls, query: List[Term], vocabulary: Vocabulary) -> DefaultDict[str, list]:
        """
            Given the query and the vocabulary, this function calculates the scores of all words in vocabulary.
        :param query: list of all query terms
        :param vocabulary: data structure that represents the vocabulary
        :return: scores based in document
        """
        scores = defaultdict(list)

        for doc in vocabulary.file_names:
            scores[doc] = []

        for term in query:
            if term.word in vocabulary:
                matched_docs = [occurrence.doc() for occurrence in vocabulary[term.word]]
                for one_doc in matched_docs:
                    scores[one_doc].append(1)
        return scores

