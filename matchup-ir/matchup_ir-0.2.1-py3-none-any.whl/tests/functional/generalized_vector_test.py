import unittest

from matchup.models.algorithms import GeneralizedVector
from matchup.structure.solution import Result
from matchup.structure.weighting.tf import TermFrequency
from matchup.structure.weighting.idf import InverseFrequency

from . import set_up_pdf_test, set_up_txt_test


class GeneralizedVectorTest(unittest.TestCase):

    def test_txt_search_known_response(self):
        self._vocabulary, self._query = set_up_txt_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=GeneralizedVector(), idf=InverseFrequency(), tf=TermFrequency())

        some_expected_results = [Result("./tests/static/files/d1.txt", 1.0),
                                 Result("./tests/static/files/d3.txt", 0.975),
                                 Result("./tests/static/files/d15.txt", 0.98),
                                 Result("./tests/static/files/d11.txt", 0.949)]

        for expected in some_expected_results:
            self.assertTrue(expected in response)

    def test_pdf_search_known_response(self):
        self._vocabulary, self._query = set_up_pdf_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=GeneralizedVector(), idf=InverseFrequency(), tf=TermFrequency())

        some_expected_results = [Result("./tests/static/pdf-files/d1.pdf", 1.0),
                                 Result("./tests/static/pdf-files/d3.pdf", 0.975),
                                 Result("./tests/static/pdf-files/d15.pdf", 0.98),
                                 Result("./tests/static/pdf-files/d11.pdf", 0.949)]
        for expected in some_expected_results:
            self.assertTrue(expected in response)
