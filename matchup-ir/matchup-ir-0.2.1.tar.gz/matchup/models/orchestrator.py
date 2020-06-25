"""
    The brain of IR algorithms. This module are responsible to execute one model and return the resulted
    scored document list.
"""
from typing import List

from matchup.structure.solution import Result
from matchup.structure.weighting.idf import InverseFrequency
from matchup.structure.weighting.tf import LogNormalization

from matchup.models.model import Model
from matchup.models.algorithms.vector_space import Vector

from matchup.presentation.text import Term


class NoSuchInputException(RuntimeError):
    pass


class ModelMissingParameters(RuntimeError):
    pass


class Orchestrator:

    def __init__(self, vocabulary):
        self._vocabulary = vocabulary

    def search(self, query, model: Model = None, idf=None, tf=None) -> List[Result]:
        """
            Core function. Execute one IR model based in vocabulary and input(query)
        :param query: Query for IR model
        :param model: IR model to execute
        :param idf: IDF class to weighting IR model
        :param tf: TF class to weighting IR model
        :return: list of solution -> (document, score)
        """

        # setting algorithms IDF weighting
        self._configure_weighting(idf, tf)
        model = model if model else Vector()

        if query.search_input:
            return model.run(query, self._vocabulary)
        else:
            raise NoSuchInputException("You should to put some search. Try again!")

    def _configure_weighting(self, idf=None, tf=None):
        if not tf:
            if not self._vocabulary.tf:
                self._vocabulary.tf = LogNormalization()
        else:
            self._vocabulary.tf = tf

        if not idf:
            if not self._vocabulary.idf:
                self._vocabulary.idf = InverseFrequency()
        else:
            self._vocabulary.idf = idf

