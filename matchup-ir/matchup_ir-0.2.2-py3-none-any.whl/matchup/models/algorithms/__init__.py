"""
    All IR algorithms in matchup
"""
from matchup.models.algorithms.extended_boolean import ExtendedBoolean
from matchup.models.algorithms.boolean import Boolean
from matchup.models.algorithms.probabilistic import Probabilistic
from matchup.models.algorithms.vector_space import Vector
from matchup.models.algorithms.generalized_vector import GeneralizedVector
from matchup.models.algorithms.belief_network import BeliefNetwork

__all__ = ["Boolean", "ExtendedBoolean", "Vector", "Probabilistic", "GeneralizedVector", "BeliefNetwork"]
