# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""A Boltzmann sampler for Set partitions (Bell numbers).

EXAMPLE:
    sage: from usainboltz.examples.expnums import *
    sage: generator.sample((10, 20))
    [[8], [7, 6, 3], [5, 4, 1], [9, 2, 0]]
"""

from math import exp

from usainboltz import Atom, Generator, Grammar, RuleName, Set, build_oracle

z = Atom()
B = RuleName()

grammar = Grammar({B: Set(Set(z, geq=1))}, labelled=True)

# XXX. Paganini does not support Set(z, geq=1) at the moment.
# Expected size is z * exp(z)
# Choose z = 2
oracle = build_oracle({z: 2, B: exp(exp(2) - 1)})
generator = Generator(grammar, B, oracle=oracle)


def build(partition):
    return partition


generator.set_builder(B, build)
