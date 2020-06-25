import unittest

from matchup.models.algorithms import Probabilistic
from matchup.structure.solution import Result

from . import set_up_txt_test, set_up_pdf_test


class ProbabilisticTest(unittest.TestCase):

    def test_txt_search_known_response(self):
        self._vocabulary, self._query = set_up_txt_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=Probabilistic())
        some_expected_results = [Result("./tests/static/files/d1.txt", 5.811),
                                 Result("./tests/static/files/d3.txt", 5.811),
                                 Result("./tests/static/files/d15.txt", 4.358),
                                 Result("./tests/static/files/d11.txt", 3.353)]

        for expected in some_expected_results:
            self.assertTrue(expected in response)

    def test_pdf_search_known_response(self):
        self._vocabulary, self._query = set_up_pdf_test()
        self._query.ask(answer="artilheiro brasil 1994 gols")
        response = self._query.search(model=Probabilistic())

        some_expected_results = [Result("./tests/static/pdf-files/d1.pdf", 5.811),
                                 Result("./tests/static/pdf-files/d3.pdf", 5.811),
                                 Result("./tests/static/pdf-files/d15.pdf", 4.358),
                                 Result("./tests/static/pdf-files/d11.pdf", 3.353)]
        for expected in some_expected_results:
            self.assertTrue(expected in response)
