from PIL import ImageColor

from .interpolate_colors import *
from .color_schemes import COLOR_SCHEMES, DEFAULT_COLOR_SCHEME_KEY, load_from_file
from .util import desaturate, color_from_value

__all__ = [
    "InterpolateColorsArgType",
    "InterpolateColorsRetType",
    "snap_to_colors"
    "interpolate_colors_rgb",
    "interpolate_colors_hsl",
    "COLOR_SCHEMES",
    "DEFAULT_COLOR_SCHEME_KEY",
    "load_from_file",
    "desaturate",
    "color_from_value"
]
