'''_4910.py

MonteCarloDistribution
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MONTE_CARLO_DISTRIBUTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'MonteCarloDistribution')


__docformat__ = 'restructuredtext en'
__all__ = ('MonteCarloDistribution',)


class MonteCarloDistribution(Enum):
    '''MonteCarloDistribution

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MONTE_CARLO_DISTRIBUTION
    __hash__ = None

    NORMAL_DISTRIBUTION = 1
    UNIFORM_DISTRIBUTION = 2
