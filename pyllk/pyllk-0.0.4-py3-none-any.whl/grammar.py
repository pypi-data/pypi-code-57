from typing import List

from pyllk.production_rule import ProductionRule


class Grammar:
    '''There is only support for LL(1) grammars in this prototype version'''

    production_rules: List
    lookup_table = {}

    def __init__(self, production_rules: List[ProductionRule]):
        for pr in production_rules:
            if pr.source.name.lower() == 'init':
                break
        else:
            raise Exception('NO_INIT', 'Missing INIT production rule')

        self.production_rules = production_rules
        self.lookup_table = {}

        for pr in production_rules:
            items = self.lookup_table[pr.source.name] if pr.source.name in self.lookup_table else []
            items.append(pr)
            self.lookup_table[pr.source.name] = items
