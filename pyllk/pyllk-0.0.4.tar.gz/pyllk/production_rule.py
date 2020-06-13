from typing import Dict, List

from pyllk.token import NonTerminalToken, Token


class ProductionRule:
    source: NonTerminalToken
    produced: List

    action = None
    ''' When specified the action is a function that takes am ExecutionContext as parameter'''

    def __init__(self, source: NonTerminalToken, produced: List, action=None):
        self.source = source
        self.produced = produced
        self.action = action

    def __str__(self):
        produced = " ".join([p.__str__() for p in self.produced])
        return "{source}: {produced}".format(source=self.source, produced=produced)


class ExecutionContext:
    parser = None
    rule: ProductionRule
    tokens: List[Token]
    context: Dict

    def __init__(self, parser, rule: ProductionRule, tokens: List[Token], context: Dict):
        self.parser = parser
        self.rule = rule
        self.tokens = tokens
        self.context = context
