from .iai import _IAI, _requires_iai_version
from .iaibase import SupervisedLearner


class RewardEstimationLearner(SupervisedLearner):
    """Abstract type encompassing all Reward Estimation learners."""

    def fit_predict(self, *args, **kwargs):
        """Fit a reward estimation model on features `X`, treatments
        `treatments`, and outcomes `outcomes`, and return predicted counterfactual rewards for each observation.

        Julia Equivalent:
        `IAI.fit_predict! <https://docs.interpretable.ai/v1.2.0/IAIBase/reference/#IAI.fit_predict!>`

        Examples
        --------
        >>> lnr.fit_predict(X, treatments, outcomes)

        Compatibility
        -------------
        Requires IAI version 2.0 or higher.
        """
        _requires_iai_version("2.0.0", "fit_predict")
        return _IAI.fit_predict_convert(self._jl_obj, *args, **kwargs)

    def score(self, *args, **kwargs):  # pragma: no cover
        raise AttributeError(
            "'RewardEstimationLearner' object has no attribute 'fit_predict'")


class RewardEstimator(RewardEstimationLearner):
    """Learner for conducting Reward Estimation.

    Julia Equivalent:
    `IAI.RewardEstimator <https://docs.interpretable.ai/v1.2.0/RewardEstimation/reference/#IAI.RewardEstimator>`

    Examples
    --------
    >>> RewardEstimator(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.0 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.0.0", "RewardEstimator")
        jl_obj = _IAI.RewardEstimator_convert(*args, **kwargs)
        super().__init__(jl_obj)
