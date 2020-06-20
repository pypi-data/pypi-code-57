import numpy as np

from .Fuel import Fuel

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Coal(Fuel):
    """Base class for diesel.

    Parameters
    ----------
    cost : float or callable
        Cost per unit [$/kg] of fuel. Can be a callable function that returns
        fuel cost starting from year zero to end of project lifetime.
    fl_infl : float
        Discount rate of fuel.
    lhv : float
        Lower heating value [MJ/kg] of the fuel.
    cost_ret : float or callable
        Savings per unit [$/kg] of fuel produced. Can be a callable function
        that returns fuel cost starting from year zero to end of project
        lifetime.

    """

    def __init__(self, cost=0.09, fl_infl=0.03, lhv=17.89, cost_ret=0):
        """Initializes the base class."""

        # initialize base class
        super().__init__(
            cost, fl_infl, 1.0, lhv, cost_ret,
            'Coal', '#333333', False
        )

    def _rec_fl(self, fl_rec, hr):
        """Records fuel use at a specified time step.

        Parameters
        ----------
        fl_rec : ndarray
            Fuel use [u] to be recorded.
        hr : int
            Time [h] in the simulation.

        """

        # default
        super()._rec_fl(fl_rec, hr)
