"""
    Module that represents one weighting param for IR models: Term Frequency (TF).
"""


from abc import ABC
from math import log
from collections import defaultdict

TF_ALGORITHMS = {"Binary", "TermFrequency", "LogNormalization", "DoubleNormalization", "DoubleNormalizationK"}


class TFFactory:
    """
        Factory for TF based on String values.
    """
    @staticmethod
    def create_tf_by_str(value: str) -> "TF":
        """
            Evaluate one string and return the correspondent TF.
        :param value:
        :return:
        """
        if value in TF_ALGORITHMS:
            return eval(value)


class TF(ABC):
    """
        Abstract base class who represents TF param.
    """

    def __init__(self, **kwargs):
        """
            Initialize TF structure.
        :param kwargs:
        """
        self._tfs = defaultdict(float)

    def __repr__(self):
        string = ""
        for key in self._tfs:
            string += f"{key} : {self._tfs[key]}\n"
        return string

    def take(self, *,  value: int = 0, reverse: bool = True):
        if value != 0:
            return sorted(self._tfs.items(), key=lambda v: v[1], reverse=reverse)[:value]
        return sorted(self._tfs.items(), key=lambda v: v[1], reverse=reverse)

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True) -> float:
        """
           Generate TF based in TFType
        :param keyword: keyword to calculate tf
        :param occurrence: keyword occurrence in it document
        :param document_maximum_frequency: maximum frequency in its document
        :param persist: persists in-memory or not the tf score generated.
        :return:float tf
        """
        ...

    def _fij(self, occurrence, document_maximum_frequency):
        return occurrence.frequency / document_maximum_frequency

    def _persist(self, key, tf) -> float:
        self._tfs[key] = tf
        return tf


class Binary(TF):

    def __init__(self, **kwargs):
        super(Binary, self).__init__(**kwargs)

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True):
        """
            Model to calculate TF based in binary values (0,1)
        :return: float tf
        """
        fij = self._fij(occurrence, document_maximum_frequency)

        if fij > 0:
            return self._persist((keyword, occurrence.doc()), 1.0) if persist else 1.0
        else:
            return self._persist((keyword, occurrence.doc()), 0.0) if persist else 0.0


class TermFrequency(TF):

    def __init__(self, **kwargs):
        super(TermFrequency, self).__init__(**kwargs)

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True) -> float:
        """
            Model to calculate TF based in fij
        :return: float fij
        """
        fij = self._fij(occurrence, document_maximum_frequency)
        return self._persist((keyword, occurrence.doc()), float(fij)) if persist else float(fij)


class LogNormalization(TF):

    def __init__(self, **kwargs):
        super(LogNormalization, self).__init__(**kwargs)

    def _fij(self, occurrence, document_maximum_frequency):
        return occurrence.frequency

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True) -> float:
        """
            Model to calculate TF based in : 1 + log fij
        :return: float fij
        """

        fij = self._fij(occurrence, document_maximum_frequency)
        tf = 1 + log(fij, 2)

        return self._persist((keyword, occurrence.doc()), tf) if persist else tf


class DoubleNormalization(TF):
    def __init__(self, **kwargs):
        super(DoubleNormalization, self).__init__(**kwargs)

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True) -> float:
        """
            Model to calculate TF based in fij
        :return: float fij
        """
        fij = self._fij(occurrence, document_maximum_frequency)

        tf = 0.5 + 0.5 * (fij / document_maximum_frequency)

        return self._persist((keyword, occurrence.doc()), tf) if persist else tf


class DoubleNormalizationK(TF):
    def __init__(self, **kwargs):
        super(DoubleNormalizationK, self).__init__(**kwargs)
        self._K = kwargs.get("K")

    def calculate(self, keyword: str, occurrence, document_maximum_frequency, persist: bool = True) -> float:
        """
            Model to calculate TF based in fij
        :return: float fij
        """
        fij = self._fij(occurrence, document_maximum_frequency)

        K = self._K if self._K is not None else 0.5
        tf = K + (1-K) * (fij / document_maximum_frequency)

        return self._persist((keyword, occurrence.doc()), tf) if persist else tf
