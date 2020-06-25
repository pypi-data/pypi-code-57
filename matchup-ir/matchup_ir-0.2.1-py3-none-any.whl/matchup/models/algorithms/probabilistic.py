"""
    Classic IR model. Probabilistic model are implemented here, based in Interface Model
"""
from collections import defaultdict
from typing import List
from math import log

from matchup.models.model import IterModel, Term, Vocabulary
from matchup.structure.solution import Result


class Probabilistic(IterModel):

    RANGE = 5

    def __init__(self):
        super(Probabilistic, self).__init__()
        self._V = list()
    
    def run(self, query, vocabulary: Vocabulary):
        """
            Principal method that represents IR probabilistic model.
        :param query: list of all query terms
        :param vocabulary: data structure that represents the vocabulary
        :return:
        """
        query_terms = query.search_input

        self.initialize(query_terms, vocabulary)

        self.process_vocabulary_query_based(query_terms, vocabulary)

        rank = self.probabilistic_iterative_perform(vocabulary)

        return rank

    def probabilistic_iterative_perform(self, vocabulary) -> List[Result]:
        """
            Perform the algorithm iterations.
        :param vocabulary:
        :return:
        """
        while True:
            rank = self.iter_rank(vocabulary)
            n_rank = self.__take(rank, self.RANGE)

            if self._V == n_rank:
                return rank

            self.initialize_pointers()  # restart pointers
            self._V = n_rank.copy()

    def iter_rank(self, vocabulary) -> List[Result]:
        """
            One iteration of Probabilistic model execute.
        :return: ranked list of documents, scores
        """
        term_scores = self.process_terms(vocabulary)

        scores = defaultdict(float)
        while not self.stop():
            doc = self.next_doc()

            scores[doc] = self.calculate(doc, term_scores)

        scores = sorted(scores.items(), key=lambda v: v[1], reverse=True)

        return self.cast_solution(scores)

    def process_terms(self, vocabulary):
        """
            Generate scores for all mapped terms.
        :param vocabulary:
        :return:
        """
        term_scores = defaultdict(float)
        for key in self._term_occurrences:
            term_scores[key] = self.score(key, vocabulary)
        return term_scores

    def calculate(self, doc: str, term_scores) -> float:
        """
            Sum the scores of the mapped representation.
        :param doc:
        :param term_scores:
        :return:
        """
        score = 0.0
        for key in self._term_occurrences.keys():
            try:
                occ = self._term_occurrences[key][self._pointers[key]]
                if occ.doc() == doc:
                    score += term_scores[key]
                    self._pointers[key] += 1
            except ValueError:
                continue
            except IndexError:
                continue
        return score

    def score(self, key: str, vocabulary: Vocabulary) -> float:
        """
            Apply probabilistic concepts to calculate the score of one keyword in vocabulary.
        :param key: keyword to generate score
        :param vocabulary: base collection
        :return: float score
        """
        ni = len(vocabulary[key])
        n = len(vocabulary.file_names)

        if self._V:
            vi = self.number_docs_with_key(vocabulary[key])
            v = len(self._V)

            prob_ki_given_r = (vi + (ni / n)) / (v + 1)
            prob_ki_given_not_r = (ni - vi + (ni / v)) / (n - v + 1)
            
        else:
            prob_ki_given_r = 0.5
            prob_ki_given_not_r = ni / n
            
        try:
            score = log(prob_ki_given_r / (1 - prob_ki_given_r), 10) + log((1 - prob_ki_given_not_r)
                                                                           / prob_ki_given_not_r, 10)
        except:
            score = 0.0

        return score

    def number_docs_with_key(self, occurrences) -> int:
        """
            Return the vi_value : number of documents with key
        :param occurrences: Occurrences
        :return:
        """
        doc = 0
        for oc in occurrences:
            if oc.doc() in [t.document for t in self._V]:
                doc += 1
        return doc

    @classmethod
    def __take(cls, rank, n) -> List[Result]:
        """
            Take the first n elements of this list copying to another structure
        :param rank: list of document, score
        :param n: number of elements to take
        :return: sliced list
        """
        cont = 0
        copy = list()
        for i in rank:
            if cont == n:
                return copy
            cont += 1
            copy.append(i)
        return copy
