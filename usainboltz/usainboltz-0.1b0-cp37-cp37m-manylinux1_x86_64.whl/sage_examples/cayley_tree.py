# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""
Cayley trees
============

Cayley trees are non-ordered labeled trees. We can use SageMath
`LabelledRootedTree <http://doc.sagemath.org/html/en/reference/combinat/sage/combinat/rooted_tree.html>`_ # noqa
to build them.
We describe here how to write a grammar for Cayley trees in UsainBoltz
and how to generated sage objects.

The grammar of Cayley trees of size given by their number of vertices,
can be written as follows:

>>> from usainboltz import *
>>> from usainboltz.generator import seed
>>> seed(0xDEADBEEF)  # For reproducibility

>>> z = Atom()
>>> C = RuleName("C")
>>> grammar = Grammar({C: z * Set(C)}, labelled=True)
>>> grammar
C -> Product(z, Set(C))

To obtain a generator for this grammar, one must write:

>>> generator = Generator(grammar, C, singular=True)

But by default, UsainBoltz generates tuples:

>>> generator.sample((10, 20))
(9,
     [(4, [(2, [(6, [(10, [(3, [(11, [(5, [])]), (7, [(1, [(8, [])])])])])])])])])

Even if the default data structure generated use list it should be interpreted
as unordered.

Sage LabelledRootedTree can be obtained using the builders feature: we must tell the
generator how to build `C` objects:

>>> from sage.combinat.rooted_tree import LabelledRootedTree

A Cayley tree is a labeled root whose children are Cayley trees

>>> def build_tree(tupl):
...     z, sub_trees = tupl
...     return LabelledRootedTree(sub_trees, label=z)
>>> generator.set_builder(C, build_tree)

Now, the generator directly generates LabelledRootedTree objects:

>>> tree = generator.sample((10, 20))
>>> tree.parent()
Labelled rooted trees

>>> from sage.all import ascii_art
>>> ascii_art(tree)
          ____9______
         /          /   
        2         _4__
        |        / / / 
      __11__    3 6 13
     /     /   
    12   _5__  
        /   /  
       8   10  
           |   
           14  
          / /  
         1 7
"""
