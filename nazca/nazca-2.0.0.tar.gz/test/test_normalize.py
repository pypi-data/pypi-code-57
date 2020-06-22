# -*- coding:utf-8 -*-
#
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest
from os import path

from nazca.utils.normalize import (
    BaseNormalizer,
    UnicodeNormalizer,
    JoinNormalizer,
    SimplifyNormalizer,
    TokenizerNormalizer,
    LemmatizerNormalizer,
    RoundNormalizer,
    RegexpNormalizer,
    NormalizerPipeline,
    lunormalize,
    lemmatized,
    roundstr,
    rgxformat,
    tokenize,
    simplify,
)
from nazca.data import FRENCH_LEMMAS


TESTDIR = path.dirname(__file__)


class NormalizerFunctionTestCase(unittest.TestCase):
    def test_unormalize(self):
        self.assertEqual(lunormalize("bépoèàÀêùï"), "bepoeaaeui")

    def test_simplify(self):
        self.assertEqual(
            simplify("J'aime les frites, les pommes et les" " scoubidous !", FRENCH_LEMMAS),
            "aimer frites pomme scoubidou",
        )

    def test_tokenize(self):
        self.assertEqual(tokenize("J'aime les frites !"), ["J'", "aime", "les", "frites", "!",])

    def test_lemmatizer(self):
        self.assertEqual(lemmatized("sacré rubert", FRENCH_LEMMAS), "sacré rubert")
        self.assertEqual(lemmatized("J'aime les frites !", FRENCH_LEMMAS), "je aimer le frite")
        self.assertEqual(lemmatized(", J'aime les frites", FRENCH_LEMMAS), "je aimer le frite")

    def test_round(self):
        self.assertEqual(roundstr(3.14159, 2), "3.14")
        self.assertEqual(roundstr(3.14159), "3")
        self.assertEqual(roundstr("3.14159", 3), "3.142")

    def test_format(self):
        string = "[Victor Hugo - 26 fev 1802 / 22 mai 1885]"
        regex = (
            r"\[(?P<firstname>\w+) (?P<lastname>\w+) - "
            r"(?P<birthdate>.*) \/ (?P<deathdate>.*?)\]"
        )
        output = "%(lastname)s, %(firstname)s (%(birthdate)s - %(deathdate)s)"
        self.assertEqual(
            rgxformat(string, regex, output), "Hugo, Victor (26 fev 1802 - 22 mai 1885)"
        )

        string = "http://perdu.com/42/supertop/cool"
        regex = r"http://perdu.com/(?P<id>\d+).*"
        output = "%(id)s"
        self.assertEqual(rgxformat(string, regex, output), "42")


class NormalizerObjectTestCase(unittest.TestCase):
    def test_normalizer(self):
        normalizer = BaseNormalizer(lunormalize)
        self.assertEqual(normalizer.normalize("bépoèàÀêùï"), "bepoeaaeui")

    def test_normalizer_record(self):
        normalizer = BaseNormalizer(lunormalize, attr_index=1)
        record = ("a1", "bépoèàÀêùï")
        self.assertEqual(normalizer.normalize(record), ["a1", "bepoeaaeui"])

    def test_normalizer_dataset(self):
        normalizer = BaseNormalizer(lunormalize, attr_index=1)
        dataset = [("a1", "bépoèàÀêùï"), ("a2", "tàtà")]
        results = normalizer.normalize_dataset(dataset)
        self.assertEqual([["a1", "bepoeaaeui"], ["a2", "tata"]], results)
        self.assertNotEqual(results, dataset)

    def test_normalizer_dataset_inplace(self):
        normalizer = BaseNormalizer(lunormalize, attr_index=1)
        dataset = [("a1", "bépoèàÀêùï"), ("a2", "tàtà")]
        normalizer.normalize_dataset(dataset, inplace=True)
        self.assertEqual([["a1", "bepoeaaeui"], ["a2", "tata"]], dataset)

    def test_unormalize(self):
        normalizer = UnicodeNormalizer()
        self.assertEqual(normalizer.normalize("bépoèàÀêùï"), "bepoeaaeui")

    def test_unormalize_record(self):
        normalizer = UnicodeNormalizer(attr_index=1)
        record = ("a1", "bépoèàÀêùï")
        self.assertEqual(["a1", "bepoeaaeui"], normalizer.normalize(record))

    def test_simplify(self):
        normalizer = SimplifyNormalizer(lemmas=FRENCH_LEMMAS)
        self.assertEqual(
            normalizer.normalize("J'aime les frites, les pommes et les scoubidous !"),
            "aimer frites pomme scoubidou",
        )

    def test_simplify_record(self):
        normalizer = SimplifyNormalizer(attr_index=1, lemmas=FRENCH_LEMMAS)
        self.assertEqual(
            ["a1", "aimer frites pomme scoubidou"],
            normalizer.normalize(["a1", "J'aime les frites, les pommes et les scoubidous !"]),
        )

    def test_tokenize(self):
        normalizer = TokenizerNormalizer()
        self.assertEqual(
            ["J'", "aime", "les", "frites", "!",], normalizer.normalize("J'aime les frites !")
        )

    def test_tokenize_record(self):
        normalizer = TokenizerNormalizer(attr_index=1)
        self.assertEqual(
            ["a1", ["J'", "aime", "les", "frites", "!",]],
            normalizer.normalize(["a1", "J'aime les frites !"]),
        )

    def test_lemmatizer(self):
        normalizer = LemmatizerNormalizer(FRENCH_LEMMAS)
        self.assertEqual(normalizer.normalize("sacré rubert"), "sacré rubert")
        self.assertEqual(normalizer.normalize("J'aime les frites !"), "je aimer le frite")
        self.assertEqual(normalizer.normalize(", J'aime les frites"), "je aimer le frite")

    def test_lemmatizer_record(self):
        normalizer = LemmatizerNormalizer(FRENCH_LEMMAS, attr_index=1)
        self.assertEqual(["a1", "sacré rubert"], normalizer.normalize(["a1", "sacré rubert"]))
        self.assertEqual(
            ["a1", "je aimer le frite"], normalizer.normalize(["a1", "J'aime les frites !"])
        )
        self.assertEqual(
            ["a1", "je aimer le frite"], normalizer.normalize(["a1", ", J'aime les frites"])
        )

    def test_round(self):
        normalizer = RoundNormalizer()
        self.assertEqual(normalizer.normalize(3.14159), "3")
        normalizer = RoundNormalizer(ndigits=2)
        self.assertEqual(normalizer.normalize(3.14159), "3.14")
        normalizer = RoundNormalizer(ndigits=3)
        self.assertEqual(normalizer.normalize(3.14159), "3.142")

    def test_round_record(self):
        normalizer = RoundNormalizer(attr_index=1)
        self.assertEqual(["a1", "3"], normalizer.normalize(["a1", 3.14159]))
        normalizer = RoundNormalizer(attr_index=1, ndigits=2)
        self.assertEqual(["a1", "3.14"], normalizer.normalize(["a1", 3.14159]))
        normalizer = RoundNormalizer(attr_index=1, ndigits=3)
        self.assertEqual(["a1", "3.142"], normalizer.normalize(["a1", 3.14159]))

    def test_regexp(self):
        normalizer = RegexpNormalizer(r"http://perdu.com/(?P<id>\d+).*", "%(id)s")
        self.assertEqual(normalizer.normalize("http://perdu.com/42/supertop/cool"), "42")

    def test_regexp_record(self):
        normalizer = RegexpNormalizer(r"http://perdu.com/(?P<id>\d+).*", "%(id)s", attr_index=1)
        self.assertEqual(
            ["a1", "42"], normalizer.normalize(["a1", "http://perdu.com/42/supertop/cool"])
        )

    def test_join(self):
        normalizer = JoinNormalizer((1, 2))
        self.assertEqual(normalizer.normalize((1, "ab", "cd", "e", 5)), [1, "e", 5, "ab, cd"])


class NormalizerPipelineTestCase(unittest.TestCase):
    def test_normalizer(self):
        regexp = r'(?P<id>\d+);{["]?(?P<firstname>.+[^"])["]?};{(?P<surname>.*)};{};{};(?P<date>.*)'
        n1 = RegexpNormalizer(regexp, "%(id)s\t%(firstname)s\t%(surname)s\t%(date)s")
        n2 = BaseNormalizer(callback=lambda x: x.split("\t"))
        n3 = UnicodeNormalizer(attr_index=(1, 2, 3))
        pipeline = NormalizerPipeline((n1, n2, n3))
        r1 = '1111;{"Toto tàtà"};{Titi};{};{};'
        self.assertEqual(["1111", "toto tata", "titi", ""], pipeline.normalize(r1))


if __name__ == "__main__":
    unittest.main()
