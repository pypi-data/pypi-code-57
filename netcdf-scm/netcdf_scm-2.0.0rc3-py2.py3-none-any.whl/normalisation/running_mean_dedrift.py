"""
Module for the normaliser which only removes drift in the pre-industrial control run (drift is calculated using a running-mean)
"""

import logging

from .running_mean import NormaliserRunningMean

LOGGER = logging.getLogger(__name__)


class NormaliserRunningMeanDedrift(NormaliserRunningMean):
    """
    Normaliser which calculates drift in the pre-industrial control using a running mean

    Each normalisation value is the change in a 21-year mean with respect to the running mean at the branch point.
    Each point is centred on the equivalent point in the pre-industrial control simulation. This means that the
    reference values are always zero in their first timestep.

    If there is insufficient data to create a full 21-year window at the edge of the simulation then a linear
    extrapolation of the running-mean is used to extend the normalisation values to cover the required
    full range.

    At present, only a 21-year running mean is implemented.
    """

    def __init__(self):
        self._method_name = "21-yr-running-mean-dedrift"

    @staticmethod
    def _get_reference_values(indata, picontrol, picontrol_branching_time):
        res = NormaliserRunningMean._get_reference_values(
            indata, picontrol, picontrol_branching_time
        )

        time_point_first = res.columns.min()
        res = res.subtract(res.loc[:, time_point_first], axis=0)

        return res
