# internal
from .wrappers import experiment_path


# version
__version__ = '0.0.4'


# fix skopt MaskedArray incompatibility
try:
    import sklearn.utils.fixes
    from numpy.ma import MaskedArray

    sklearn.utils.fixes.MaskedArray = MaskedArray
except:
    pass
