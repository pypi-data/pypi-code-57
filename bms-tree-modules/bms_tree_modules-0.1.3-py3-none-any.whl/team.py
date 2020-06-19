from copy import deepcopy

from .node import Node
from .tree import Tree


class Team(object):
    CONST_ID = "team_id"
    CONST_DEC = "decisions"
    CONST_TREE = "tree_input"

    def __init__(self, period_input):
        # initialize empty decisions dict
        self.decisions: dict = {}
        self.__check_input(period_input)

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            if self.CONST_ID not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_ID
                    )
                )

            if self.CONST_DEC not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_DEC
                    )
                )

            if self.CONST_TREE not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_TREE
                    )
                )

            # convert dict to object
            self.from_dict(period_input)
        else:
            raise TypeError(
                "Expected: period_input <class 'dict'>, Received: {0}".format(
                    type(period_input)
                )
            )

    def from_dict(self, period_input: dict):
        # assign id
        self.id = int(period_input[self.CONST_ID])

        # transform decisions input into dict
        for decision in period_input[self.CONST_DEC]:
            self.decisions[decision["key"]] = decision["value"]

        # create tree from tree_input (current state t0)
        self.t0 = Tree(period_input)

        # create a copy of the tree t0 (next state t1)
        self.t1 = deepcopy(self.t0)

    def to_dict(self) -> dict:
        return {"team_id": self.id, "tree": self.t1.root.to_dict()}

    def node_t0(self, name: str) -> Node:
        return self.t0.node(name)

    def node_t1(self, name: str) -> Node:
        return self.t1.node(name)
