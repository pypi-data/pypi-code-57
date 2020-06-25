"""
    Module that represents the search solution using some IR model in addition to some operations for presentation
"""

from typing import List

from collections import namedtuple

Result = namedtuple("Result", "document score")


class Solution:
    """
        The solution class has the function of properly storing and displaying the responses of the queries
    """
    def __init__(self, results: List[Result]):
        """
            Solution constructor
        :param results: List of (Document, Score).
        """
        self._results = results
        self._idf = None
        self._tf = None

    def __repr__(self) -> str:
        """
            Ranking string
        :return:
        """
        string = ""
        if self._results:
            for terms in self._results:
                doc = terms.document.split('/')[-1]
                string += f"\n{doc} : {terms.score}"
        else:
            string += "No results found."
        return string

    @property
    def results(self) -> List[Result]:
        """
            Ranking List
        :return: List of results
        """
        return self._results

    def __contains__(self, item: Result):
        """
            Boolean flag that indicates if some item are in result list
        :param item:
        :return:
        """
        return item in self._results

    def str_n(self, n) -> str:
        """
            Take the ranking for the first N results.
        :param n:
        :return:
        """
        return str(Solution(self._results[:n]))
