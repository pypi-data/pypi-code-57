from .iai import _IAI
from .iaitrees import (TreeLearner, ClassificationTreeLearner,
                       RegressionTreeLearner, SurvivalTreeLearner,
                       PrescriptionTreeLearner)


class OptimalTreeLearner(TreeLearner):
    """Abstract type encompassing all optimal tree learners."""
    pass


class OptimalTreeClassifier(OptimalTreeLearner, ClassificationTreeLearner):
    """Learner for training Optimal Classification Trees.

    Julia Equivalent:
    `IAI.OptimalTreeClassifier <https://docs.interpretable.ai/v1.2.0/OptimalTrees/reference/#IAI.OptimalTreeClassifier>`

    Examples
    --------
    >>> OptimalTreeClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreeClassifier_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreeRegressor(OptimalTreeLearner, RegressionTreeLearner):
    """Learner for training Optimal Regression Trees.

    Julia Equivalent:
    `IAI.OptimalTreeRegressor <https://docs.interpretable.ai/v1.2.0/OptimalTrees/reference/#IAI.OptimalTreeRegressor>`

    Examples
    --------
    >>> OptimalTreeRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreeRegressor_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreeSurvivor(OptimalTreeLearner, SurvivalTreeLearner):
    """Learner for training Optimal Survival Trees.

    Julia Equivalent:
    `IAI.OptimalTreeSurvivor <https://docs.interpretable.ai/v1.2.0/OptimalTrees/reference/#IAI.OptimalTreeSurvivor>`

    Examples
    --------
    >>> OptimalTreeSurvivor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreeSurvivor_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreePrescriptionMinimizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to minimize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMinimizer <https://docs.interpretable.ai/v1.2.0/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMinimizer>`

    Examples
    --------
    >>> OptimalTreePrescriptionMinimizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreePrescriptionMinimizer_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalTreePrescriptionMaximizer(OptimalTreeLearner,
                                       PrescriptionTreeLearner):
    """Learner for training Optimal Prescriptive Trees where the prescriptions
    should aim to maximize outcomes.

    Julia Equivalent:
    `IAI.OptimalTreePrescriptionMaximizer <https://docs.interpretable.ai/v1.2.0/OptimalTrees/reference/#IAI.OptimalTreePrescriptionMaximizer>`

    Examples
    --------
    >>> OptimalTreePrescriptionMaximizer(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.
    """
    def __init__(self, *args, **kwargs):
        jl_obj = _IAI.OptimalTreePrescriptionMaximizer_convert(*args, **kwargs)
        super().__init__(jl_obj)
