import warnings

# asdf extensions and tags
import weldx.asdf
# geometry packages
import weldx.geometry
import weldx.transformations
import weldx.utility
from weldx.constants import WELDX_QUANTITY as Q_

__all__ = ["geometry", "transformations", "utility", "asdf", "Q_"]




with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Q_([])

__version__ = "0.1.0"  # get_versions()["version"]
