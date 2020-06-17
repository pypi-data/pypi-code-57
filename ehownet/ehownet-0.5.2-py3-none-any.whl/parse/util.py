#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pylint: disable=invalid-name, no-self-use

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'

from itertools import (
    count as _count,
)

from .node import (
    EhnParseEntityBase as _EhnParseEntityBase,

    EhnParseCoindexEntity as _EhnParseCoindexEntity,
    EhnParseFunctionEntity as _EhnParseFunctionEntity,
    EhnParseTildeEntity as _EhnParseTildeEntity,
)

################################################################################################################################

LOGICAL_FUNCTIONS = [
    'union',
    'and',
    'or',
    'not',
    # 'Ques',
]

################################################################################################################################

def replace_tilde(root, coindex_prefix='x'):
    """Convert all tilde nodes to coindex nodes.

    Arguments
    ---------
        root : :class:`~ehn.parse.node.base.EhnParseNode`
            The output of :class:`~ehn.parse.parser.EhnParser`.

    """
    _TilderReplacer(root, coindex_prefix)
    return root

class _TilderReplacer:

    def __init__(self, root, coindex_prefix):
        coindexs = set(filter(None, map(self.get_coindex, root.descendant())))
        self.gen_coindex = (f'{coindex_prefix}{i}' for i in _count(1) if f'{coindex_prefix}{i}' not in coindexs)
        self.replace(root)

    def replace(self, node, *parents):
        if isinstance(node, _EhnParseTildeEntity):
            target = self.get_tilde_target(*parents)
            assert target, f'Can\'t find target for {node}'

            coindex = self.get_coindex(target)
            if not coindex:
                coindex = self.next_coindex()
                target.anchor.head = coindex
            node = _EhnParseCoindexEntity(coindex)

        # Recursive
        features = node.get_features()
        if features:
            node.features = [self.replace(feature, node, *parents) for feature in features]

        arguments = node.get_arguments()
        if arguments:
            node.arguments = [self.replace(argument, node, *parents) for argument in arguments]

        value = node.get_value()
        if value:
            node.value = self.replace(value, node, *parents)

        function = node.get_function()
        if function:
            node.function = self.replace(function, node, *parents)

        return node

    def get_tilde_target(self, *parents, count=0):
        if not parents:
            return None

        parent = parents[0]
        if isinstance(parent, _EhnParseEntityBase) and \
            not (isinstance(parent, _EhnParseFunctionEntity) and parent.head in LOGICAL_FUNCTIONS):
            count += 1
            if count > 1:
                return parent

        return self.get_tilde_target(parents[1:], count=count)

    def next_coindex(self):
        return next(self.gen_coindex)

    @staticmethod
    def get_coindex(node):
        anchor = node.get_anchor()
        if anchor and anchor.head:
            return anchor.head
        if isinstance(node, _EhnParseCoindexEntity):
            return node.head
        return None
