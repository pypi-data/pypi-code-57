from dataclasses import dataclass, field
from typing import List, TypeVar

Token = TypeVar("Token", str, float)


@dataclass(order=True)
class DataNode:
    """ A class to hold tokens and children of a node tree structure.

        `tokens` is a list of strings or floats found in the line
        `children` is a list of DataNodes found on indented lines below

        token1 token2 "very long token 3"
            child1_token # ignored_comment
            "child2 with tokens" 2 3 4
            `child3 with '"' in the token`
        not_a_child_of_token1
    """

    tokens: List[Token] = field(default_factory=list)
    children: List["DataNode"] = field(default_factory=list)

    def filter_first(self, token):
        """ Return the children whose first token matches `token` """
        return filter(lambda n: n.tokens[0] == token, self.children)

    def filter(self, tokens):
        """ Return the children whose tokens match `tokens` """
        return filter(lambda n: n.tokens == tokens, self.children)
