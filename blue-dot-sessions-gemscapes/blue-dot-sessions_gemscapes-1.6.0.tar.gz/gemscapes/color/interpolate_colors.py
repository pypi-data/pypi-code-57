import logging
import typing

import numpy as np
import colour
import skimage.color

__all__ = [
    "InterpolateColorsArgType",
    "InterpolateColorsRetType",
    "snap_to_colors",
    "interpolate_colors_rgb",
    "interpolate_colors_hsl",
    "interpolate_colors_lab",
    "interpolate_colors_fn_lookup"
]


module_logger = logging.getLogger(__name__)

InterpolateColorsArgType = typing.Union[
    typing.List[str],
    typing.List[typing.Tuple[float]]
]

InterpolateColorsRetType = typing.List[typing.Tuple[int]]


def _get_colour_Color(color: typing.Union[str, typing.Tuple[float]]) -> colour.Color:
    """
    Get colour.Color from either hexcode or existing RGB tuple
    """
    if hasattr(color, "format"):
        color = colour.Color(color)
    else:
        if any([c > 1.0 for c in color]):
            color = [c/256.0 for c in color]
        color = colour.Color(rgb=color)
    return color



def snap_to_colors(
    colors: InterpolateColorsArgType,
    flat: bool = False,
    num_colors: int = 256
) -> InterpolateColorsRetType:
    """
    Tile `colors`, such that each entry in `colors` is repeated
    `num_colors/len(colors)` times.

    Example:

    ```
    >>> snap_to_colors([], num_colors=20)
    >>>
    ```

    Args:
        colors ():
        flat ():
        num_colors (int):

    Returns:

    """

    palette = []
    colors_new = []
    for idx in range(len(colors)):
        colors_new.append(tuple([int(256.0*val)
                          for val in _get_colour_Color(colors[idx]).rgb]))

    for idx in range(num_colors):
        index = (idx * (len(colors)))/(num_colors)
        # index = (idx * (len(colors) - 1))/(num_colors - 1)
        index_int = int(index)

        interpolated = colors_new[index_int]

        if flat:
            palette.extend(interpolated)
        else:
            palette.append(interpolated)

    return palette


def interpolate_colors_lab(colors: InterpolateColorsArgType):

    n_colors = len(colors)
    colors_rgb = [list(_get_colour_Color(colors[idx]).rgb) for idx in range(len(colors))]
    colors_rgb = np.asarray(colors_rgb)
    colors_rgb = colors_rgb[np.newaxis, :, :]
    colors_lab = skimage.color.rgb2lab(colors_rgb)
    # print(colors_rgb)
    # print(colors_lab)
    diff = skimage.color.deltaE_ciede2000(colors_lab[:, 1:, :], colors_lab[:, :-1, :])
    print(diff)


def interpolate_colors_hsl(colors: InterpolateColorsArgType,
                           flat: bool = False,
                           num_colors: int = 256) -> InterpolateColorsRetType:
    """
    Interpolate between RGB 3-uples or hex values in `colors` using corresponding
    HSL values for better perceptual progression between colors.
    """
    module_logger.debug("interpolate_colors_hsl")
    palette = []
    colors_new = []
    for idx in range(len(colors)):
        colors_new.append(_get_colour_Color(colors[idx]))


    def hue_interpolate_factory():
        def hue_interpolate(hue, hue_p1, alpha):
            diff = hue_p1 - hue
            diff_counterclockwise = 1.0 - abs(diff)
            if abs(diff_counterclockwise) < abs(diff):
                diff = -diff_counterclockwise
            res = hue + alpha*diff
            if res < 0.0:
                res += 1.0
            return res
            # if hue_p1 == 0.0 and hue >= 0.5:
            #     return hue_interpolate(hue, 1.0, alpha)
            # if hue == 0.0 and hue_p1 >= 0.5:
            #     return hue_interpolate(1.0, hue_p1, alpha)
            # return hue + alpha*(hue_p1 - hue)
        return hue_interpolate

    hue_interpolate = hue_interpolate_factory()

    for i in range(num_colors):
        index = (i * (len(colors) - 1))/(num_colors - 1.0)
        index_int = int(index)
        alpha = index - float(index_int)

        color_idx = colors_new[index_int].hsl
        # print(color_idx)
        if alpha > 0:
            color_idx_p1 = colors_new[index_int + 1].hsl
            hue = hue_interpolate(color_idx[0], color_idx_p1[0], alpha)
            sat = (1.0 - alpha) * color_idx[1] + alpha * color_idx_p1[1]
            lum = (1.0 - alpha) * color_idx[2] + alpha * color_idx_p1[2]
            # color_idx_str = ", ".join([f"{val:.2f}" for val in color_idx])
            # color_idx_p1_str = ", ".join([f"{val:.2f}" for val in color_idx_p1])
            # print(f"({color_idx_str}), ({color_idx_p1_str}) --> ({hue:.2f}, {sat:.2f}, {lum:.2f})")
        else:
            hue = (1.0 - alpha) * color_idx[0]
            sat = (1.0 - alpha) * color_idx[1]
            lum = (1.0 - alpha) * color_idx[2]

        interpolated = tuple([int(256*val) for val in colour.Color(hsl=(hue, sat, lum)).rgb])

        if flat:
            palette.extend(interpolated)
        else:
            palette.append(interpolated)

    return palette


def interpolate_colors_rgb(colors: InterpolateColorsArgType,
                           flat: bool = False,
                           num_colors: int = 256) -> InterpolateColorsRetType:
    """ given a list of colors, create a larger list of colors interpolating
    the first one. If flatten is True a list of numers will be returned. If
    False, a list of (r,g,b) tuples. num_colors is the number of colors wanted
    in the final list """

    palette = []

    colors_copy = [_get_colour_Color(col) for col in colors]

    for i in range(num_colors):
        index = (i * (len(colors) - 1))/(num_colors - 1.0)
        # _index = (i * (len(colors)))/(num_colors)
        index_int = int(index)
        alpha = index - float(index_int)
        color_idx = colors_copy[index_int].rgb
        if alpha > 0:
            color_idx_p1 = colors_copy[index_int + 1].rgb
            r = (1.0 - alpha) * color_idx[0] + alpha * color_idx_p1[0]
            g = (1.0 - alpha) * color_idx[1] + alpha * color_idx_p1[1]
            b = (1.0 - alpha) * color_idx[2] + alpha * color_idx_p1[2]
        else:
            r = (1.0 - alpha) * color_idx[0]
            g = (1.0 - alpha) * color_idx[1]
            b = (1.0 - alpha) * color_idx[2]
            # r = 0.0
            # g = 0.0
            # b = 0.0

        interpolated = tuple([int(256.0*val) for val in [r, g, b]])
        if flat:
            palette.extend(interpolated)
        else:
            palette.append(interpolated)

    return palette


interpolate_colors_fn_lookup = {
    "rgb": interpolate_colors_rgb,
    "snap_to": snap_to_colors,
    "hsl": interpolate_colors_hsl,
    "lab": interpolate_colors_lab
}
