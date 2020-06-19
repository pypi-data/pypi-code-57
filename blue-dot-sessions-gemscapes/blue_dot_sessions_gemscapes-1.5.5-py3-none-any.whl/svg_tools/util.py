import logging
import typing
import math

# import numpy as np
# import matplotlib.pyplot as plt

Dim1FloatType = typing.List[float]
Dim2FloatType = typing.List[Dim1FloatType]
Dim3FloatType = typing.List[Dim2FloatType]


module_logger = logging.getLogger(__name__)

__all__ = [
    "dist",
    "slope",
    "calc_sin_theta",
    "calc_cos_theta",
    "rotate",
    "translate",
    "calc_centroid"
]


def flat2pair(vertices_flat: Dim1FloatType) -> Dim2FloatType:
    """
    Take some flat list of vertices and turn it into a list of pairs, where
    each pair is a vertex.

    Example:

    ```
        >>> print(vertices_flat)
        [-16.0, 81.0, 132.0, 39.0, 271.0, 82.0]
        >>> flat2pair(vertices_flat)
        [[-16.0, 81.0], [132.0, 39.0], [271.0, 82.0]]
    ```

    Args:
        vertices_flat: Flat list of vertices
    Returns:
        List of vertex pairs
    """
    return [vertices_flat[idx:idx+2] for idx
            in range(0, len(vertices_flat), 2)]


def orientation(vertices: Dim2FloatType) -> float:
    """
    Get the orientation of a set of vertices relative to the y-axis

    Args:

    Returns:
    """
    # centroid = calc_centroid(vertices)
    # vertices.append(centroid)
    xvals, yvals = [list(zipped) for zipped in zip(*vertices)]

    min_x, max_x = min(xvals), max(xvals)
    min_y, max_y = min(yvals), max(yvals)

    delta_x = max_x - min_x
    delta_y = max_y - min_y

    angle = math.degrees(math.atan(delta_x / delta_y))

    # fig, ax = plt.subplots(1, 1)
    # ax.scatter(xvals, yvals)
    #
    # # m, b = np.polyfit(xvals, yvals, 1)
    # m, b = np.polyfit(yvals, xvals, 1)
    # angle = math.degrees(math.atan(m))
    #
    # # _xvals = np.linspace(np.amin(xvals), np.amax(xvals), 100)
    # # _yvals = m*_xvals + b
    #
    # _yvals = np.linspace(np.amin(yvals), np.amax(yvals), 100)
    # _xvals = m*_yvals + b
    #
    #
    # ax.plot(_xvals, _yvals)
    # ax.grid(True)
    # # ax.set_aspect("equal")
    #
    # module_logger.debug(f"orientation: m={m:.5f}, b={b:.5f}, angle={angle:.5f}")

    return angle


def dist(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    return math.sqrt((xy2[1] - xy1[1])**2 +  (xy2[0] - xy1[0])**2)


def slope(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    return (xy2[1] - xy1[1])/(xy2[0] - xy1[0])


def calc_sin_theta(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    hyp = dist(xy1, xy2)
    return (xy2[1] - xy1[1]) / hyp


def calc_cos_theta(xy1: Dim1FloatType, xy2: Dim1FloatType) -> float:
    hyp = dist(xy1, xy2)
    return (xy2[0] - xy1[0]) / hyp


def translate(pair: Dim1FloatType, point: Dim1FloatType) -> Dim1FloatType:
    return [pair[0] - point[0], pair[1] - point[1]]
    # return [[pair[0] - point[0], pair[1] - point[1]] for pair in pairs]


def rotate(xy: Dim1FloatType, sin_theta: float, cos_theta: float) -> Dim1FloatType:
    """
    cos(theta) -sin(theta)
    sin(theta) cos(theta)
    """
    return [xy[0]*cos_theta - xy[1]*sin_theta,
            xy[0]*sin_theta + xy[1]*cos_theta]


def calc_centroid(vertices: Dim2FloatType) -> Dim1FloatType:
    """
    Calculate the centroid of some polygon

    Using formula from https://en.wikipedia.org/wiki/Centroid#Of_a_polygon

    """
    vertices_copy = vertices.copy()
    vertices_copy.append(vertices[0])
    area = 0.0
    Cx = 0.0
    Cy = 0.0

    module_logger.debug(f"_calc_centroid: vertices={vertices}")

    for idx in range(len(vertices_copy) - 1):
        xi, yi = vertices_copy[idx]
        xpi, ypi = vertices_copy[idx + 1]

        intermediate = xi*ypi - xpi*yi
        Cx += (xi + xpi)*intermediate
        Cy += (yi + ypi)*intermediate
        area += intermediate

    # area /= 2.0
    Cx /= 3.0*area
    Cy /= 3.0*area
    return [Cx, Cy]
