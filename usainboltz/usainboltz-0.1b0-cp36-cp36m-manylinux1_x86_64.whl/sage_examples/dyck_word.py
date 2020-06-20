# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""Dyck words.

Dyck words is the language over the alphabet ``{'(', ')'}`` described by the
following grammar::

    D ::= <empty word>
        | '(' D ')' D

It is the language of "well-parenthesised" words. In sage, Dyck words are
implemented in the
`dyck_word <https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/dyck_word.html>`_ module. # noqa
The bijection between binary trees and Dyck words allows us to generate directly
Dyck words from the binary tree generator from the
:py:mod:`usainboltz.sage_examples.binary_tree` module using an ad-hoc builder:

>>> from usainboltz import *
>>> from usainboltz.generator import seed
>>> seed(0xDEADBEEF)  # For reproducibility

>>> # The binary tree sampler
>>> z, leave = Atom(), Epsilon()
>>> B = RuleName()
>>> grammar = Grammar(rules={B: leave + z * B * B})
>>> generator = Generator(grammar, B, singular=True)

>>> # Ad-hoc builder
>>> def empty_word_builder(_):
...     return ""
>>> def product_builder(t):
...     _, left, right = t
...     return "(" + left + ")" + right
>>> dyck_word_builder = union_builder(empty_word_builder, product_builder)
>>> generator.set_builder(B, dyck_word_builder)

>>> word = generator.sample((10, 20))
>>> word
'(()(())(()())()()()())'

>>> from sage.all import ascii_art, DyckWord
>>> ascii_art(DyckWord(word))
        /\  /\/\          
     /\/  \/    \/\/\/\/\ 
    /                    \
"""
