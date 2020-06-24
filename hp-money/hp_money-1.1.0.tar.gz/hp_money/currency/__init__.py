# -*- coding: utf-8 -*-


class Currency(object):

    def __init__(self, iso_code, numric_code, accuracy):

        self._iso_code = iso_code
        self._numric_code = numric_code
        self._accuracy = accuracy

    def __str__(self):
        return f'{self._iso_code}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Currency):
            return (
                self._iso_code == other.iso_code
            ) and (
                self._numric_code == other.numric_code
            ) and (
                self._accuracy == other.accuracy
            )
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(
            (self._iso_code, self._numric_code, self._accuracy)
        )

    @property
    def iso_code(self):
        return self._iso_code

    @property
    def numric_code(self):
        return self._numric_code

    @property
    def accuracy(self):
        return self._accuracy
