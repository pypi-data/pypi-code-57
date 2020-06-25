import unittest

from matchup.models.algorithms import BeliefNetwork
from matchup.structure.solution import Result
from matchup.structure.weighting.tf import TermFrequency
from matchup.structure.weighting.idf import InverseFrequency

from . import set_up_pdf_test, set_up_txt_test


class BeliefNetworkTest(unittest.TestCase):

    def test_txt_search_known_response(self):
        self._vocabulary, self._query = set_up_txt_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=BeliefNetwork(), idf=InverseFrequency(), tf=TermFrequency())

        some_expected_results = [Result("./tests/static/files/d1.txt", 0.062),
                                 Result("./tests/static/files/d3.txt", 0.051),
                                 Result("./tests/static/files/d15.txt", 0.046),
                                 Result("./tests/static/files/d11.txt", 0.038)]

        for expected in some_expected_results:
            self.assertTrue(expected in response)

    def test_pdf_search_known_response(self):
        self._vocabulary, self._query = set_up_pdf_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=BeliefNetwork(), idf=InverseFrequency(), tf=TermFrequency())

        some_expected_results = [Result("./tests/static/pdf-files/d1.pdf", 0.062),
                                 Result("./tests/static/pdf-files/d3.pdf", 0.051),
                                 Result("./tests/static/pdf-files/d15.pdf", 0.046),
                                 Result("./tests/static/pdf-files/d11.pdf", 0.038)]

        for expected in some_expected_results:
            self.assertTrue(expected in response)
