from copy import deepcopy
from functools import lru_cache
from typing import Callable, List, Optional, Union

from .config import ModuleConfig
from .curves import CurveConfig
from .decision import Decisions
from .node import Node
from .team import Team
from .tree import Tree


class Module(object):
    CONST_ROUND: int = 8
    CONST_TEAMS = "teams"
    CONST_CURVE_A = "curve_assignments"

    def __init__(self, period_input):
        self.__check_input(period_input)

        # initialze module configurations & settings
        self.config = ModuleConfig(period_input)
        self.curves = CurveConfig(period_input)

        # create decisions, sum and average i.e. the market
        self.decisions: Decisions = deepcopy(self.teams[0].decisions)
        self.sum: Tree = deepcopy(self.teams[0].t0)
        self.average: Tree = deepcopy(self.teams[0].t0)

        # compute market and decision average
        self.compute_market()
        self.compute_decision_avg()

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            if self.CONST_TEAMS not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_TEAMS
                    )
                )
            if self.CONST_CURVE_A not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_CURVE_A
                    )
                )

            # extract curve assignments & teams from json
            self.from_dict(period_input)
        else:
            raise TypeError(
                "Expected: period_input <class 'dict'>, Received: {0}".format(
                    type(period_input)
                )
            )

    def from_dict(self, period_input: dict):
        # create a Team per team input
        self.teams = [Team(team) for team in period_input[self.CONST_TEAMS]]

    def to_dict(self) -> dict:
        return {"teams": [team.to_dict() for team in self.teams]}

    def compute_market(self):
        """compute the average of all leaf nodes across the teams
        """
        # get the leaf_names from a team to ensure that
        # if they have changed -> changes are reflected in market too
        # or at least an error is raised
        leaf_names = self.teams[0].t0.leaf_names

        # compute the average of all leaf nodes across the teams
        # use leaf names to find relevant nodes
        for name in leaf_names:
            # average the values of all teams for each leaf node (name)
            scores = [team.node_t0(name).value for team in self.teams]
            sum_ = sum(scores)

            # assign the value to the market leaf
            self.sum.node(name).value = sum_
            self.average.node(name).value = sum_ / len(scores)

    def compute_decision_avg(self):
        """compute the average of all decisions across the teams
        """
        # get the key names from a team to ensure that
        # if they have changed -> changes are reflected in market too
        all_decision_keys: List[str] = [
            decision.key for decision in self.teams[0].decisions.decisions
        ]

        # compute the average of all decisions across the teams
        for key in all_decision_keys:
            scores = [team.decision(key).value for team in self.teams]
            average = sum(scores) / len(scores)

            self.decisions.decision(key).value = average

    def index_from_id(self, id_: int) -> int:
        team = list(filter(lambda team: team.id == id_, self.teams))[0]
        return self.teams.index(team)

    def node_t0(self, id_: int, name: str) -> Node:
        """returns the node with name: {name}
        from subtree t0 of team with id: {id_}
        """
        index = self.index_from_id(id_)
        return self.teams[index].node_t0(name)

    def node_t1(self, id_: int, name: str) -> Node:
        """returns the node with name: {name}
        from subtree t1 of team with id: {id_}
        """
        index = self.index_from_id(id_)
        return self.teams[index].node_t1(name)

    @lru_cache(maxsize=None)
    def get_curve(self, name: str) -> Callable:
        return self.curves.curves[name]

    @lru_cache(maxsize=None)
    def get_config(self, leaf: str, effect: str, value: str) -> Union[float, str, None]:
        try:
            # try to get the value of the EffectConfig
            return self.config.value(leaf, effect, value)
        except KeyError:
            # if it doesn't exist -> return None instead of raising a KeyError
            # the keys: 'MAX', 'MIN', 'WEIGHT' are allowed to not exist
            if value in ["MAX", "MIN", "WEIGHT"]:
                return None
            else:
                raise

    def _sum_product_leaf_decision(
        self, leafs: List[str], decisions: List[str], team_id: int
    ) -> float:
        """computes the sum of the multiplication of two arrays.
        multiplies the leaf value with the associated decision value
        and returns the sum.

        inputs:
        - leafs: List[str] - names of tree leafs
        - decisions: List[str] - names of decisions which influence leafs
        """
        result: float = 0.0

        for leaf, decision in zip(leafs, decisions):
            leaf_value = self.node_t0(team_id, leaf).value

            index = self.index_from_id(team_id)
            decision_value = self.teams[index].decision(decision).value

            value = leaf_value * decision_value
            result += round(value, self.CONST_ROUND)

        return result

    def _sum_product_leaf_config(
        self, leafs: List[str], effect: str, config: str, team_id: int
    ) -> float:
        result: float = 0.0

        for leaf in leafs:
            weight = float(self.config.value(leaf, effect, config))
            value = self.node_t1(team_id, leaf).value
            result += weight * value
        return result

    def min_max_weight(self, leaf: str, effect: str, input_: float) -> float:
        # try to get the min_, max_, weight config values
        max_: Optional[float] = self.get_config(leaf, effect, "MAX")  # type: ignore
        min_: Optional[float] = self.get_config(leaf, effect, "MIN")  # type: ignore
        weight: Optional[float] = self.get_config(leaf, effect, "WEIGHT")  # type: ignore # noqa: E501

        # if they don't exist -> None is returned
        # use default value instead of None
        if max_ is None:
            max_ = float("inf")
        if min_ is None:
            min_ = float("-inf")
        if weight is None:
            weight = 1.0

        # ensure the input_ is within bounds and weight factor adjusted
        return min(max(input_, min_), max_) * weight

    def _curve(self, leaf: str, effect: str, input_: float) -> float:
        # get the correct sensitivity curve
        curve_name = self.get_config(leaf, effect, "CURVE")
        curve = self.get_curve(curve_name)

        # compute the value on the sensitivity curve
        return curve(input_)

    def _value_change(
        self, decision: str, leaf: str, effect: str, input_: float,
    ) -> float:
        # compute the value on the sensitivity curve
        value = self._curve(leaf, effect, input_)

        # ensure the input_ is within bounds and weight factor adjusted
        return self.min_max_weight(leaf, effect, value)

    def _delta_change(
        self, decision: str, leaf: str, effect: str, team_id: int
    ) -> float:
        # compute the delta of the team's decisions compared to the market average
        index = self.index_from_id(team_id)
        team_decision = self.teams[index].decision(decision).value
        average = self.decisions.decision(decision).value
        delta = round(team_decision - average, self.CONST_ROUND)

        # compute the value on the sensitivity curve
        value = self._curve(leaf, effect, delta)

        # ensure the result is within bounds and weight factor adjusted
        return self.min_max_weight(leaf, effect, value)
