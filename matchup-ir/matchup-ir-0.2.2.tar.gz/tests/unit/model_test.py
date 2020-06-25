import unittest

from matchup.models.model import Model
from matchup.structure.solution import Result


class ModelTest(unittest.TestCase):

    def test_cast_solution(self):
        ipt = [("d1.txt", 1.0), ("d2.txt", 0.421)]
        opt = [Result("d1.txt", 1.0), Result("d2.txt", 0.421)]

        self.assertEqual(Model.cast_solution(ipt), opt)
