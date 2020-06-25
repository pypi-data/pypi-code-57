"""
    Module that represents one weighting param for IR models: Inverse Document Frequency (IDF).
"""

from abc import ABC
from math import log
from collections import defaultdict


IDF_ALGORITHMS = {"Unary", "InverseFrequency", "InverseFrequencySmooth", "InverseFrequencyMax",
                  "ProbabilisticInverseFrequency"}


class IDFFactory:
    """
        Factory for IDF based on String values.
    """
    @staticmethod
    def create_idf_by_str(value: str) -> "IDF":
        """
            Evaluate one string and return the correspondent IDF.
        :param value:
        :return:
        """
        if value in IDF_ALGORITHMS:
            return eval(value)


class IDF(ABC):
    """
        Abstract base class who represents IDF param.
    """
    def __init__(self):
        """
            Just initialize IDF structure.
        """
        self._idfs = defaultdict(float)

    def __repr__(self) -> str:
        """
            String representation.
        :return: string
        """
        string = ""
        for key in self._idfs:
            string += f"{key} : {self._idfs[key]}\n"
        return string

    def generate(self, vocabulary) -> None:
        """
            Generate the idf for all keywords in a vocabulary
        :param vocabulary: Vocabulary object
        :return: None
        """
        ...

    def take(self, *, value: int = 0, reverse: bool = True):
        """
            Take the first 'value' elements of IDF dict
        :param value:
        :param reverse : asc or desc.
        :return:
        """
        if value != 0:
            return sorted(self._idfs.items(), key=lambda v: v[1], reverse=reverse)[:value]
        return sorted(self._idfs.items(), key=lambda v: v[1], reverse=reverse)

    def __getitem__(self, item: str) -> float:
        """
            Overload operator [] on idf structure
        :param item: keyword (document)
        :return: float idf value
        """
        return self._idfs[item]


class Unary(IDF):

    def __init__(self):
        super(Unary, self).__init__()

    def generate(self, vocabulary):
        """
            Model to calculate IDF based in unary weight (1)
        :param vocabulary: structure to generate IDF
        :return: None
        """
        for key in vocabulary.keys:
            self._idfs[key] = 1


class InverseFrequency(IDF):

    def __init__(self):
        super(InverseFrequency, self).__init__()

    def generate(self, vocabulary):
        """
             Model to calculate IDF based in inverse frequency : log N / ni
        :param vocabulary:  structure to generate IDF
        :return: None
        """
        for key in vocabulary.keys:
            self._idfs[key] = log(len(vocabulary.file_names) / len(vocabulary[key]), 10)


class InverseFrequencySmooth(IDF):

    def __init__(self):
        super(InverseFrequencySmooth, self).__init__()

    def generate(self, vocabulary):
        """
            Model to calculate IDF based in inverse frequency smooth : log 1 + N / ni
        :param vocabulary: structure to generate IDF
        :return: None
        """
        for key in vocabulary.keys:
            self._idfs[key] = \
                log(1 + (len(vocabulary.file_names) / len(vocabulary[key])), 10)


class InverseFrequencyMax(IDF):

    def __init__(self):
        super(InverseFrequencyMax, self).__init__()

    def generate(self, vocabulary):
        """
                Model to calculate IDF based in max inverse frequency  : log 1 + max ni / ni
        :param vocabulary:  structure to generate IDF
        :return: None
        """
        all_number_docs_by_keyword = [len(vocabulary[key]) for key in vocabulary.keys]
        max_ni = max(all_number_docs_by_keyword)

        for key in vocabulary.keys:
            self._idfs[key] = \
                log(1 + (max_ni / len(vocabulary[key])), 10)


class ProbabilisticInverseFrequency(IDF):
    def __init__(self):
        super(ProbabilisticInverseFrequency, self).__init__()

    def generate(self, vocabulary):
        """
                Model to calculate IDF based in probabilistic inverse frequency  : log N - ni / ni
                This weighting are not so good when N - ni / ni < 1 :: N - ni < ni :: N < 2ni
        :param vocabulary:  structure to generate IDF
        :return: None
        """
        for key in vocabulary.keys:
            n = len(vocabulary.file_names)
            ni = len(vocabulary[key])
            if n >= 2*ni:
                self._idfs[key] = \
                    log((n - ni) / ni, 10)
            else:
                self._idfs[key] = 0.0
