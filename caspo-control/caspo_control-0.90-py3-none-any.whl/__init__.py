"""
TODO
"""

from .iface import caspo_control

from colomoto.types import PartialState
from algorecell_types import *

from colomoto.minibn import BooleanNetwork

class CaspoControl(object):
    """
    TODO
    """
    def __init__(self, bn, fixed={}):
        self.bn = BooleanNetwork.auto_cast(bn)
        self.fixed = fixed

    def reprogramming_to_attractor(self, *goal_spec,
            exclude_goal=False, maxsize=0, **goal_kwspec):
        """
        TODO
        """
        goal = PartialState(*goal_spec, **goal_kwspec)
        interventions = caspo_control(self.bn, goal, self.fixed,
                allow_goal_intervention=not exclude_goal,
                maxsize=maxsize)
        strategies = ReprogrammingStrategies()
        for control in interventions:
            p = PermanentPerturbation(control)
            st = FromCondition("input", p) if self.fixed else FromAny(p)
            strategies.add(st)
        if self.fixed:
            strategies.register_alias("input", self.fixed)
        return strategies

def load(bn, fixed={}):
    """
    TODO
    """
    return CaspoControl(bn, fixed)

