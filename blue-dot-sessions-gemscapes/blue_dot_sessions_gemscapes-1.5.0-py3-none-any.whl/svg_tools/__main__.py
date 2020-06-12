import typing
import argparse
import shutil
import math
import random
import os
import logging

from . import (
    polygon2svg_lookup,
    modify_svg
)


def apply_fn(modify_fn, modify_fn_name, file_paths, *args):

    for file_path in file_paths:
        output_file_path = f"{os.path.splitext(file_path)[0]}.{modify_fn_name}.svg"
        shutil.copy(file_path, output_file_path)
        modify_svg(
            output_file_path,
            lambda points: modify_fn(points, *args))


def jagged_line_callback(args):
    name = "jagged_line"
    apply_fn(
        polygon2svg_lookup[name], name, args.file_paths, args.noise)


def rotate_if_callback(args):
    name = "rotate_if"

    def rotate_if_fn(angle):
        if abs(angle) < args.thresh:
            return True
        return False

    apply_fn(
        polygon2svg_lookup[name], name,
        args.file_paths, args.min_angle,
        args.max_angle, rotate_if_fn)


def rounded_callback(args):
    name = "rounded_corner"
    apply_fn(
        polygon2svg_lookup[name], name, args.file_paths, args.radius)


def added_vertices_callback(args):
    name = "added_vertices"
    apply_fn(
        polygon2svg_lookup[name], name, args.file_paths, args.per_side, args.factor)


def create_parser() -> argparse.ArgumentParser:

    modify_fn_names_str = ", ".join(list(polygon2svg_lookup.keys()))

    parser = argparse.ArgumentParser(description="Modify primitive SVG polygons")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    subparsers = parser.add_subparsers(
        help=(f"Modification function to apply to SVG polygons. "
              f"Available functions are {modify_fn_names_str}"))

    jagged_line_parser = subparsers.add_parser("jagged", help="Add jagged line noise to polgyon edges")
    jagged_line_parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                                    help="Files whose polygons to modify")
    jagged_line_parser.add_argument("-n", "--noise", dest="noise", type=float,
                                    default=0.5, help="Noise factor (default %(default)s)")
    jagged_line_parser.set_defaults(func=jagged_line_callback)

    rotate_if_parser = subparsers.add_parser("rotate-if", help="Rotate shapes in SVG if angle it makes with y-axis is less than a threshold")
    rotate_if_parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                                  help="Files whose polygons to modify")
    rotate_if_parser.add_argument("-t", "--thresh", dest="thresh", type=float,
                                    default=15, help="Angle threshold (default %(default)s)")
    rotate_if_parser.add_argument("--min-angle", dest="min_angle", type=float,
                                    default=5, help="Minimum angle by which to rotate (default %(default)s)")
    rotate_if_parser.add_argument("--max-angle", dest="max_angle", type=float,
                                    default=15, help="Maximum angle by which to rotate (default %(default)s)")
    rotate_if_parser.set_defaults(func=rotate_if_callback)

    added_vertices_parser = subparsers.add_parser("added-vertices", help="")
    added_vertices_parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                                       help="Files whose polygons to modify")
    added_vertices_parser.add_argument("-p", "--vertices-per-side", dest="per_side", type=int,
                                       default=1, help="Vertices to add per edge (default %(default)s)")
    added_vertices_parser.add_argument("-c", "--convex-concave-factor", dest="factor", type=int,
                                       default=2, help="Convex/Concave factor (+ for convex, - for concave) (default %(default)s)")

    added_vertices_parser.set_defaults(func=added_vertices_callback)

    rounded_parser = subparsers.add_parser("rounded-corners", help="")
    rounded_parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                                help="Files whose polygons to modify")
    rounded_parser.add_argument("-r", "--radius", action="store", dest="radius", type=float, default=2.0,
                                help="Corner Radius for output SVG paths (default %(default)s.")
    rounded_parser.set_defaults(func=rounded_callback)


    return parser


def main():

    parsed = create_parser().parse_args()

    level = logging.INFO
    if parsed.verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)

    parsed.func(parsed)


main()
