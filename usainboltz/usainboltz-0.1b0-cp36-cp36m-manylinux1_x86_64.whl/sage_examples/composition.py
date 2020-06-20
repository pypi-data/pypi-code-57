# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""
Integer compositions
====================

An integer composition of a positive integer :math:`n` is a list of positive
integers :math:`k_1, k_2, \ldots, k_r` such that :math:`\sum_i k_i = n`. Using
the value of an integer as its size, we can identify the class of positive
integers with the class of non-empty sequences of atoms ``Seq(z, geq=1)`` by
identifying ``n`` with the unique list of length ``n``:

>>> from usainboltz import *
>>> from usainboltz.generator import seed
>>> seed(0xDEADBEEF)  # For reproducibility

>>> z = Atom()
>>> Nat = RuleName("Nat")
>>> grammar = Grammar({Nat: Seq(z, geq=1)})

Thus, integer partitions are non-empty sequences of integers:

>>> C = RuleName("C")
>>> grammar.add_rule(C, Seq(Nat, geq=1))
>>> grammar
C -> Seq(Nat, 1 <= .)
Nat -> Seq(z, 1 <= .)

Since the generating function of compositions is rational, one cannot use a
singular sampler. But instead, one can ask the generator to tune its oracle to
target a specific size (in expectation):

>>> generator = Generator(
...     grammar, C, expectations={z: 10}
... )

Finally, we define an appropriate builder that apply the bijection between lists
and integers:

>>> def build_nat(l):
...     return len(l)
>>> generator.set_builder(Nat, build_nat)

>>> from sage.all import Composition
>>> def build_composition(l):
...     return Composition(l)
>>> generator.set_builder(C, build_composition)

Now we can generate sage
`compositions <https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/composition.html>`_: # noqa

>>> composition = generator.sample((10, 20))
>>> composition.parent()
Compositions of non-negative integers
>>> composition
[1, 2, 1, 2, 2, 2]
>>> ascii_art(composition)
       **
      **
     **
     *
    **
    *
"""
