"""
A collection of loss functions for use with feyn.

The loss funtions can be specified as arguments to the `QGraph.fit()` and `QGraph.sort()` methods. A good choice of loss function can sometimes speed up the training. For most uses the default loss function, `mean_squared_error` is a fine choice.

Note: Data scientist with experience from other frameworks may be used to thinking that the loss function is very significant. In practice it matters less in QLattices, for reasons that have to do with the large range of initial parameters for the graphs in a QGraph.
"""
from ._lossfunctions import categorical_cross_entropy, mean_absolute_error, mean_squared_error, _get_loss_function

__all__ = [
    "categorical_cross_entropy",
    "mean_absolute_error",
    "mean_squared_error",
]
