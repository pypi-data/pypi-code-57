# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""
Binary trees
============

Binary trees are plane trees with nodes of arity two and leaves of arity zero.
In sage binary trees are implemented in the
`binary_tree <https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/binary_tree.html>`_ # noqa
module. We describe here how to write a grammar for binary trees in UsainBoltz
and how to generated sage objects.

The grammar of binary trees where only internal nodes are counted in the size
can be written as follows:

>>> from usainboltz import *
>>> from usainboltz.generator import seed
>>> seed(0xDEADBEEF)  # For reproducibility

>>> z, leave = Atom(), Epsilon()
>>> B = RuleName("B")
>>> grammar = Grammar({B: leave + z * B * B})
>>> grammar
B -> Union(epsilon, Product(z, B, B))

To obtain a generator for this grammar, one must write:

>>> generator = Generator(grammar, B, singular=True)

But by default, UsainBoltz generates tuples:

>>> generator.sample((10, 20))
('z',
     ('z',
      'epsilon',
      ('z',
       ('z', 'epsilon', 'epsilon'),
       ('z',
        ('z', 'epsilon', ('z', 'epsilon', 'epsilon')),
        ('z',
         'epsilon',
         ('z', 'epsilon', ('z', 'epsilon', ('z', 'epsilon', 'epsilon'))))))),
     'epsilon')

Sage binary trees can be obtained using the builders feature: we must tell the
generator how to build `B` objects:

>>> from sage.all import BinaryTree

- A leaf is `None`:

>>> def build_leaf(_):
...     return None

- A node is a call to `BinaryTree`:

>>> def build_node(tupl):
...     z, left, right = tupl
...     return BinaryTree([left, right])

- This two possible cases are combined using the :py:func:`~usainboltz.generator.union_builder` combinator:

>>> build_B = union_builder(build_leaf, build_node)
>>> generator.set_builder(B, build_B)

Now, the generator directly generates BinaryTree objects:

>>> tree = generator.sample((10, 20))
>>> tree.parent()
Binary trees

>>> tree
[[[[., .], [., .]], [., [[[., .], [., .]], .]]], .]

>>> from sage.all import ascii_art
>>> ascii_art(tree)
            o
           /
        __o__
       /     \
      o       o
     / \       \
    o   o       o
               /
              o
             / \
            o   o
"""
