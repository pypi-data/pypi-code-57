import logging
import contextlib
import typing
import shutil
import math
import random
import logging
import itertools
import xml.etree.ElementTree as ET

from .util import Dim1FloatType, Dim2FloatType, Dim3FloatType
from . import util

module_logger = logging.getLogger(__name__)

__all__ = [
    "added_vertices_polygon",
    "jagged_line_polygon",
    "rounded_corner_polygon",
    "curved_paths2svg",
    "straight_paths2svg",
    "added_vertices_polygon2svg",
    "jagged_line_polygon2svg",
    "rounded_corner_polygon2svg",
    "get_root",
    "modify_svg",
    "polygon2svg_lookup"
]


RotateIfType = typing.Callable[[float], bool]


def rotate_if_polygon(
    vertices: Dim2FloatType,
    min_rotation: float = 0.0,
    max_rotation: float = 15.0,
    rotate_if_fn: typing.Optional[RotateIfType] = None
) -> Dim2FloatType:
    """
    Rotate some polygon by some angle between `min_rotation` and `max_rotation`
    if `rotate_if_fn` returns True. `rotate_if_fn` takes as argument the current
    angle of the shape relative to its centroid.

    Args:
        vertices_flat
        min_rotation:
        max_rotation:
        rotate_if_fn:
    Returns:

    """
    angle = util.orientation(vertices)
    to_rotate = True
    if rotate_if_fn is not None:
        to_rotate = rotate_if_fn(angle)

    if to_rotate:
        centroid = util.calc_centroid(vertices)
        translated = [util.translate(vertex, centroid) for vertex in vertices]
        rotate_angle = math.radians(random.uniform(min_rotation, max_rotation))
        sin_theta = math.sin(rotate_angle)
        cos_theta = math.cos(rotate_angle)
        rotated = [util.rotate(vertex, sin_theta, cos_theta) for vertex in translated]
        translated = [util.translate(vertex, [-centroid[0], -centroid[1]]) for vertex in rotated]
        return translated
    return vertices



def added_vertices_polygon(
    vertices: Dim2FloatType,
    vertices_per_side: int,
    convex_concave_factor: float
) -> Dim2FloatType:
    module_logger.debug(f"added_vertices_polygon: vertices_per_side={vertices_per_side}")
    module_logger.debug(f"added_vertices_polygon: convex_concave_factor={convex_concave_factor}")

    module_logger.debug(f"added_vertices_polygon: vertices={vertices}")
    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.append(vertices[0])

    paths = []

    # centroid = _calc_centroid(vertices)
    # module_logger.debug(f"added_vertices_polygon: centroid={centroid}")

    # def _find_intersection(l0: Dim1FloatType, l1: Dim1FloatType) -> Dim1FloatType:
    #     m0 = util.slope(l1, l0)
    #     m1 = -1.0 / m0
    #
    #     x0, y0 = l0
    #     x1, y1 = centroid.copy()
    #
    #     xi = (m0*x0 - m1*x1 + y1 - y0)/(m0 - m1)
    #     yi = m1*(xi - x1) + y1
    #     intersect = [xi, yi]
    #     module_logger.debug(f"_find_intersection: translated intersection: [{(xi):.2f}, {(yi):.2f}]")
    #     return intersect, util.dist(l0, intersect), util.dist(intersect, l1)
    #
    # fig, axes = plt.subplots(2, 2)
    # axes = axes.flatten()
    for idx in range(n_vertices):
        sl = vertices_overlap[idx: idx + 2]
        dist = util.dist(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        sin_theta = util.calc_sin_theta(sl[0], sl[1])

        # start, end = sl[0].copy(), sl[1].copy()
        # mid_point = dist/2.0
        # _, pre_midpoint_incre, post_midpoint_incre = _find_intersection(start, end, axes[idx])
        # module_logger.debug(f"added_vertices_polygon: idx={idx}, "
        #                     f"dist={dist}, "
        #                     f"pre_midpoint_incre={pre_midpoint_incre:.2f}, "
        #                     f"post_midpoint_incre={post_midpoint_incre:.2f}")

        pre_rotate = [[0.0, 0.0]]

        x_val = 0.0
        y_val = 0.0

        half = int(vertices_per_side + 1) / 2
        x_incre = dist / (vertices_per_side + 1)

        for idy in range(1, vertices_per_side + 1):
            if idy >= half:
                # x_val += pre_midpoint_incre
                y_val += convex_concave_factor / idy
            else:
                # x_val += post_midpoint_incre
                y_val -= convex_concave_factor / idy
            x_val += x_incre
            # module_logger.debug(f"added_vertices_polygon: idx={idx}, [{x_val:.2f}, {y_val:.2f}]")
            _rot = util.rotate([x_val, 0.0], sin_theta, cos_theta)
            module_logger.debug(f"added_vertices_polygon: idx={idx},<circle cx=\"{(_rot[0] + sl[0][0]):.2f}\" cy=\"{(_rot[1] + sl[0][1]):.2f}\" r=\"2\"/>")
            pre_rotate.append(
                [x_val, y_val])

        for pair in pre_rotate:
            post_rotate = util.rotate(pair, sin_theta, cos_theta)
            paths.append([post_rotate[0] + sl[0][0], post_rotate[1] + sl[0][1]])
        # paths.append(sl[0])
        # paths.append(centroid)

    # plt.show()
    return paths


def jagged_line_polygon(
    vertices: Dim2FloatType,
    noise: float
) -> Dim2FloatType:
    """
    Rotation Matrix:

    cos(theta) -sin(theta)
    sin(theta) cos(theta)

    """
    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.append(vertices[0])

    paths = []

    for idx in range(n_vertices):

        sl = vertices_overlap[idx: idx + 2]
        pre_rotate = [[0.0, 0.0]]
        dist = util.dist(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        sin_theta = util.calc_sin_theta(sl[0], sl[1])

        x_dist = 0.0

        while dist - x_dist > noise:
            if x_dist < noise:
                ru_y = random.uniform(0, noise)
            else:
                ru_y = random.uniform(-noise, noise)
            x_dist += random.uniform(0.5*noise, noise)
            pre_rotate.append([x_dist, ru_y])

        pre_rotate.append([dist, 0.0])
        post_rotate_translate = [
            [sl[0][0] + pair[0]*cos_theta - pair[1]*sin_theta,
             sl[0][1] + pair[0]*sin_theta + pair[1]*cos_theta] for pair in pre_rotate
        ]
        paths.extend(post_rotate_translate)

    return paths


def rounded_corner_polygon(
    vertices: Dim2FloatType,
    radius: float
) -> Dim3FloatType:

    n_vertices = len(vertices)
    vertices_overlap = vertices.copy()
    vertices_overlap.insert(0, vertices[-1])
    vertices_overlap.append(vertices[0])


    paths = []
    for idx in range(1, n_vertices + 1):
        sl = vertices_overlap[idx - 1:idx + 2]
        sin_theta = util.calc_sin_theta(sl[0], sl[1])
        cos_theta = util.calc_cos_theta(sl[0], sl[1])
        x0 = sl[1][0] - cos_theta * radius
        y0 = sl[1][1] - sin_theta * radius

        sin_theta = util.calc_sin_theta(sl[1], sl[2])
        cos_theta = util.calc_cos_theta(sl[1], sl[2])
        x2 = sl[1][0] + cos_theta * radius
        y2 = sl[1][1] + sin_theta * radius
        paths.append(
            [[x0, y0], sl[1], [x2, y2]]
        )

    return paths


def curved_paths2svg(paths: Dim3FloatType) -> str:

    svg_str = []
    end_point = paths[0][0]
    control = "M"
    for idx in range(len(paths)):
        [x0, y0], [x1, y1], [x2, y2] = paths[idx]
        if idx > 0:
            control = "L"
        svg_str.append(
            f'{control} {x0} {y0} Q {x1} {y1}, {x2} {y2} '
        )
    svg_str.append(f"L {end_point[0]} {end_point[1]}")

    return "".join(svg_str)


def straight_paths2svg(paths: Dim2FloatType) -> str:

    svg_str = [f"M {paths[0][0]} {paths[0][1]} "]
    for idx in range(1, len(paths)):
        x0, y0 = paths[idx]
        svg_str.append(f'L {x0} {y0} ')
    return "".join(svg_str)


_primitive_prefix = "http://www.w3.org/2000/svg"
_primitive_prefix_g = "{" + _primitive_prefix + "}"


def _vertices_from_points_str(points_str: str) -> Dim2FloatType:
    """
    Convert SVG polygon element `points` field string to list of vertices
    """
    if " " in points_str:
        points = []
        for pair in points_str.split(" "):
            for sub in pair.split(","):
                points.append(float(sub))
    else:
        points = [float(val) for val in points_str.split(",")]

    return util.flat2pair(points)


def _vertices_from_d_str(d_str: str) -> Dim2FloatType:
    """
    Convert SVG path `d` field containing M and L elements to list of vertices.
    """
    disallowed = ["q", "c", "s", "t", "a"]

    d_str = d_str.lower()

    for ch in disallowed:
        if ch in d_str:
            raise RuntimeError(f"_vertices_from_d_str unable to process SVG path containing {ch}")

    if d_str.count("m") > 1:
        raise RuntimeError(f"_vertices_from_d_str unable to process SVG paths with multiple move comands")

    d_str = d_str.replace("m", "")

    points = []
    for sub in d_str.split("l"):
        points.append([float(val) for val in sub.strip().split(" ")])
    points_str = ", ".join([f"[{x:.2f}, {y:.2f}]" for x, y in points])
    module_logger.debug(f"_vertices_from_d_str: points=[{points_str}]")

    return points


class PrimitiveElement:
    """
    Custom extension of ET.Element because I got seriously tired of writing
    f"{{{_primitive_prefix}}}tag" everytime I wanted to access some XML element.
    """
    def __init__(self, element):
        self._element = element

    def __getattr__(self, attr):
        return getattr(self._element, attr)

    def __str__(self):
        return f"<PrimitiveElement '{self.tag}' at {hex(id(self))}>"

    @property
    def tag(self):
        return self._element.tag.replace(f"{{{_primitive_prefix}}}", "")

    @tag.setter
    def tag(self, new_tag):
        self._element.tag = f"{{{_primitive_prefix}}}{new_tag}"

    def find(self, name, **kwargs):
        name = f"{{{_primitive_prefix}}}{name}"
        return PrimitiveElement(self._element.find(name, **kwargs))

    def findall(self, name, **kwargs):
        name = f"{{{_primitive_prefix}}}{name}"
        return [PrimitiveElement(elem) for elem in self._element.findall(name, **kwargs)]

    def iter(self, name, **kwargs):
        name = f"{{{_primitive_prefix}}}{name}"
        for elem in self._element.iter(name, **kwargs):
            yield PrimitiveElement(elem)


@contextlib.contextmanager
def get_root(file_path: str, output_file_path: str = None):
    """
    Get ET root for a given file path
    """
    ET.register_namespace("", _primitive_prefix)
    tree = ET.parse(file_path)
    root = PrimitiveElement(tree.getroot())

    yield root

    if output_file_path is None:
        tree.write(file_path)
    else:
        tree.write(output_file_path)


def polygon_iter(file_path: str, output_file_path: str = None):
    """
    Return a generator that will iterate through all the polygons in a primitive
    generated SVG.
    """
    ET.register_namespace("", _primitive_prefix)
    tree = ET.parse(file_path)
    root = PrimitiveElement(tree.getroot())

    with get_root(file_path, output_file_path=output_file_path) as root:
        g = root.find("g")
        if g is None:
            raise ValueError("Cannot find group element!")

        for child in itertools.chain(
            g.findall("polygon"),
            g.findall("path")
        ):
            yield child


PolygonModifyFnType = typing.Callable[
    [Dim2FloatType], typing.Any]

def modify_svg(file_path: str,
               *polygon_modify_fns: PolygonModifyFnType,
               output_file_path: str = None) -> str:
    """
    Modify some primitive generated SVG with `polygon_modify_fns`

    Args:
        file_path: path to primitive generated SVG
        polygon_modify_fns: modification functions. Only the last one can return
            vertices for creating curved SVG paths
    Returns:
        `file_path`
    """
    # polygon_tag = f"{_primitive_prefix_g}polygon"
    # path_tag = f"{_primitive_prefix_g}path"

    module_logger.debug((f"modify_svg: file_path={file_path}, "
                         f"len(polygon_modify_fns)={len(polygon_modify_fns)}"))
    for idx, polygon in enumerate(polygon_iter(file_path, output_file_path=output_file_path)):
        module_logger.debug(f"modify_svg: polygon {idx}, polygon.tag={polygon.tag}")
        # print(ET.dump(polygon))
        if polygon.tag == "polygon":
            points_str = polygon.attrib["points"]
            paths = typing.cast(typing.Any, _vertices_from_points_str(points_str))
        if polygon.tag == "path":
            d_str = polygon.attrib["d"]
            paths = typing.cast(typing.Any, _vertices_from_d_str(d_str))

        for fn in polygon_modify_fns:
            module_logger.debug(f"modify_svg: polygon {idx}, fn={fn.__name__}, len(paths[0])={len(paths[0])}")
            if len(paths[0]) == 3:
                raise RuntimeError(f"Only last function in polygon_modify_fns can return {Dim3FloatType}")
            paths = fn(paths)

        if len(paths[0]) == 3:
            module_logger.debug(f"modify_svg: polygon {idx}, using curved_paths2svg")
            paths_str = curved_paths2svg(paths)
        else:
            module_logger.debug(f"modify_svg: polygon {idx}, using straight_paths2svg")
            paths_str = straight_paths2svg(paths)
        polygon.tag = "path"
        polygon.attrib["d"] = paths_str
        if "points" in polygon.attrib:
            del polygon.attrib["points"]

    if output_file_path is None:
        return file_path
    else:
        return output_file_path


polygon2svg_lookup = {
    "rotate_if": rotate_if_polygon,
    "added_vertices": added_vertices_polygon,
    "jagged_line": jagged_line_polygon,
    "rounded_corner": rounded_corner_polygon
}
