import logging
import os
import shutil
import math
import xml.etree.ElementTree as ET

import colour
import pyclipper

from .. import svg_tools
from ..metadata import BDSMetaDataType
from ..audio_visualizer import map_range_factory

module_logger = logging.getLogger(__name__)


def union_factory():
    """
    Not sure why this works
    """
    pc = pyclipper.Pyclipper()
    def union(*vertices):
        total_union = vertices[0]
        for idx in range(1, len(vertices)):
            pc.AddPath(total_union, pyclipper.PT_CLIP, True)
            pc.AddPath(vertices[idx], pyclipper.PT_SUBJECT, True)
            res = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            total_union = res[0]
        pc.Clear()

        return total_union
    return union


def intersection_factory():
    pc = pyclipper.Pyclipper()
    def intersection(vertices0, vertices1):
        pc.AddPath(vertices0, pyclipper.PT_CLIP, True)
        pc.AddPath(vertices1, pyclipper.PT_SUBJECT, True)
        solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        pc.Clear()
        # module_logger.debug(f"intersection_factory.intersection: len(solution)={len(solution)}")
        return solution
    return intersection



def _hex_dist(hex0: str, hex1: str) -> float:
    """
    Get the normalized distance between two RGB hex color values

    Args:

    """
    def cut_alpha(hex_val):
        if len(hex_val) > 7:
            return hex_val[:7]
        return hex_val

    c0 = colour.Color(cut_alpha(hex0))
    c1 = colour.Color(cut_alpha(hex1))

    unnorm = math.sqrt(
        sum([(val0 - val1)**2 for val0, val1 in zip(c0.rgb, c1.rgb)]))
    norm_factor = math.sqrt(3)

    return unnorm/norm_factor


def _adjust_svg_scale(
    file_path: str,
    h_wssf: float,
    v_wssf: float
) -> str:

    module_logger.debug(f"_adjust_svg_scale: h_wssf={h_wssf}, v_wssf={v_wssf}")
    with svg_tools.get_root(file_path) as root:
        width = float(root.attrib["width"])
        height = float(root.attrib["height"])
        g = root.find("g")
        transform = g.attrib["transform"]

        module_logger.debug(f"_adjust_svg_scale: svg dim ({width}, {height})")
        module_logger.debug(f"_adjust_svg_scale: g transform {transform}")

        def in_between(target, begin, end):
            idx_start = target.find(begin)
            idx_end = target[idx_start+len(begin):].find(end)
            val = target[idx_start+len(begin):][:idx_end]
            return val

        scale_val = 1.0
        trans = []

        if "scale" in transform:
            scale_val = float(in_between(transform, "scale(", ")"))

        module_logger.debug(f"_adjust_svg_scale: scale_val={scale_val}")

        if "translate" in transform:
            translate_str = in_between(transform, "translate(", ")")
            trans = [float(val) for val in translate_str.split(" ")]
        module_logger.debug(f"_adjust_svg_scale: trans=({trans[0]}, {trans[1]})")

        cur_dim = [width, height]
        scales = [h_wssf, v_wssf]
        new_dims = []
        new_trans = []
        for idx in range(len(scales)):
            scale = scales[idx]
            new_dims.append(scale * cur_dim[idx])
            delta = new_dims[idx] - cur_dim[idx]

            new_trans.append(trans[idx] + (delta*0.5)/scale_val)

        module_logger.debug(f"_adjust_svg_scale: new_dims=({new_dims[0]}, {new_dims[1]})")
        module_logger.debug(f"_adjust_svg_scale: new_trans=({new_trans[0]}, {new_trans[1]})")

        g.attrib["transform"] = f"scale({scale_val:.4f}) translate({new_trans[0]}, {new_trans[1]})"
        root.attrib["width"] = str(int(new_dims[0]))
        root.attrib["height"] = str(int(new_dims[1]))


def post_primitive(
    file_path: str,
    thresh: float = 0.05,
    track_metadata: BDSMetaDataType = None,
    h_wssf: float = 1.0,
    v_wssf: float = 1.0,
    knock_out: bool = False,
    dry_run: bool = False
) -> str:
    """
    This function is run after primitive, to do any post-primitive SVG modification

    Right now this gets rid of any dark shapes and applies an `svg_tools` utility
    to modify the primtive SVG output.

    Args:
        file_path: Input .svg file path
        modify_svg_fn: SVG
        dry_run: Run without modifying anything

    Returns:
        output .svg file path
    """
    output_file_path = "{}.post_primitive.svg".format(os.path.splitext(file_path)[0])

    if not dry_run:
        target = "fill=\""
        black = "#000000"
        shutil.copyfile(file_path, output_file_path)

        _adjust_svg_scale(
            output_file_path,
            h_wssf=h_wssf,
            v_wssf=v_wssf)


        if not knock_out:
            with svg_tools.get_root(output_file_path) as root:
                rect = root.find("rect")
                rect.attrib["fill"] = "none"
                g = root.find("g")
                polygons = g.findall("polygon")
                for idx, polygon in enumerate(polygons):
                    hexval = polygon.attrib["fill"]
                    if hexval == "none":
                        continue
                    points_str = polygon.attrib["points"]
                    paths = pyclipper.scale_to_clipper(
                        svg_tools._vertices_from_points_str(points_str))

                    delta = _hex_dist(hexval, black)
                    if delta <= thresh:
                        polygon.attrib["fill"] = "none"

        else:
            dark_idxs = []
            dark_paths = []
            non_dark_paths = []

            with svg_tools.get_root(output_file_path) as root:
                rect = root.find("rect")
                rect_fill = rect.attrib["fill"]
                rect.attrib["fill"] = "none"

                g = root.find("g")
                polygons = g.findall("polygon")
                for idx, polygon in enumerate(polygons):
                    hexval = polygon.attrib["fill"]
                    if hexval == "none":
                        continue
                    points_str = polygon.attrib["points"]
                    paths = pyclipper.scale_to_clipper(
                        svg_tools._vertices_from_points_str(points_str))

                    delta = _hex_dist(hexval, black)
                    if delta <= thresh:
                        dark_idxs.append(idx)
                        dark_paths.append(paths)
                        # polygon.attrib["fill"] = "none"
                    else:
                        non_dark_paths.append(paths)

                union_fn = union_factory()

                total_union = union_fn(*non_dark_paths)
                module_logger.debug(f"post_primitive: len(total_union)={len(total_union)}")

                intersect_fn = intersection_factory()
                for idx in range(len(dark_idxs)):
                    dark_idx = dark_idxs[idx]
                    dark_path = dark_paths[idx]
                    intersects = intersect_fn(total_union, dark_path)
                    sub_g = ET.Element("g")
                    for intersect in intersects:
                        scaled = pyclipper.scale_from_clipper(intersect)
                        scaled_str = svg_tools.straight_paths2svg(scaled)
                        new_path = ET.Element("path")
                        new_path.attrib["d"] = scaled_str
                        new_path.attrib["fill"] = g._element[dark_idx].attrib["fill"]
                        new_path.attrib["fill-opacity"] = g._element[dark_idx].attrib["fill-opacity"]
                        sub_g.append(new_path)
                    g._element[dark_idx] = sub_g

                scaled = pyclipper.scale_from_clipper(total_union)
                scaled_str = svg_tools.straight_paths2svg(scaled)
                new_path = ET.Element("path")
                new_path.attrib["d"] = scaled_str
                new_path.attrib["fill"] = rect_fill
                new_path.attrib["stroke"] = "green"
                new_path.attrib["stroke-width"] = "1.0"
                g._element.insert(0, new_path)

        if track_metadata is not None:
            polygon_modify_fns = []

            # if "Tension" in track_metadata:
            #     map_range = map_range_factory([0, 9], [0, 10])
            #     mapped = map_range(track_metadata["Tension"])
            #     module_logger.debug(f"post_primitive: Tension value {track_metadata['Tension']}, mapped value {mapped}")
            #     polygon_modify_fns.append(
            #         lambda paths: svg_tools.rotate_if_polygon(
            #             paths,
            #             min_rotation=mapped,
            #             max_rotation=mapped+0.1,
            #             rotate_if_fn=lambda angle: angle < 15.))

            if "Mood" in track_metadata:
                map_range = map_range_factory([0, 9], [1, 4.5])
                mapped = map_range(track_metadata["Mood"])
                module_logger.debug(f"post_primitive: Mood value {track_metadata['Mood']}, mapped value {mapped}")
                polygon_modify_fns.append(
                    lambda paths: svg_tools.rounded_corner_polygon(paths, mapped))

            # svg_tools.modify_svg(
            #     output_file_path,
            #     *polygon_modify_fns
            # )

    return output_file_path
