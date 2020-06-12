import argparse
import logging
import subprocess

import PIL
import matplotlib
import matplotlib.pyplot as plt

from .interpolate_colors import (
    interpolate_colors_rgb,
    interpolate_colors_hsl,
    snap_to_colors,
    interpolate_colors_fn_lookup)
from .color_schemes import COLOR_SCHEMES, DEFAULT_COLOR_SCHEME_KEY, load_from_file


module_logger = logging.getLogger(__name__)


def create_color_scheme_image(
    colors: list,
    image_width: int = 256,
    image_height: int = 256,
    num_colors: int = None,
    interpolate_fn: callable = interpolate_colors_rgb
) -> PIL.Image:
    """
    Visualize color schemes by creating PNG file with lines corresponding
    """
    if num_colors is None:
        num_colors = image_width
    module_logger.debug(
        f"create_color_scheme_image: using interpolate_fn {interpolate_fn}")

    palette_lookup = interpolate_fn(colors, num_colors=num_colors)

    image = PIL.Image.new("RGB", (image_width, image_height), tuple([0, 0, 0]))

    image_width = image_width
    image_height = image_height

    draw = PIL.ImageDraw.Draw(image)

    lines_per_color = int(image_width / num_colors)

    for idx in range(num_colors):
        line_color = palette_lookup[idx]
        for idy in range(lines_per_color):
            image_idx = lines_per_color*idx + idy
            draw.line([image_idx, image_height, image_idx, 0], line_color)

    return image


def create_parser():

    color_scheme_keys = ", ".join(COLOR_SCHEMES.keys())
    interpolate_fn_keys = ", ".join(interpolate_colors_fn_lookup.keys())

    parser = argparse.ArgumentParser(description="Visualize gemscape color scheme")
    parser.add_argument(
        "-k", "--key", type=str, help=f"Color Scheme key. Available keys are {color_scheme_keys}")
    parser.add_argument("--color-scheme-file", action="store",
                        dest="color_scheme_file_path", type=str,
                        help="path to file containing color scheme configurations")
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path")
    parser.add_argument(
        "--color-space",
        dest="color_space",
        type=str, default="rgb",
        help=("Color space in which to do interpolation. "
              f"Available values are {interpolate_fn_keys}. "
              "Defaults to %(default)s."))

    parser.add_argument("--width", dest="image_width", type=int, default=256,
                        help="image width in pixels (default %(default)s)")
    parser.add_argument("--num-colors", dest="num_colors", type=int,
                        help="Number of colors to create")
    parser.add_argument("--height",  dest="image_height", type=int, default=256,
                        help="image height in pixels (default %(default)s)")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output")

    return parser


def main():
    parser = create_parser()
    parsed = parser.parse_args()

    log_level = logging.INFO
    if parsed.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)

    output_file_path = parsed.output
    if output_file_path is None:
        output_file_path = f"{parsed.key}.png"

    if not parsed.color_scheme_file_path:
        if parsed.key in COLOR_SCHEMES:
            colors = COLOR_SCHEMES.get(parsed.key)['wave_colors'][1:]
    else:
        palettes = load_from_file(parsed.color_scheme_file_path)
        colors = palettes[parsed.key]["palette"]

    interpolate_fn = interpolate_colors_fn_lookup[parsed.color_space]

    image = create_color_scheme_image(
        colors,
        image_width=parsed.image_width,
        image_height=parsed.image_height,
        num_colors=parsed.num_colors,
        interpolate_fn=interpolate_fn
    )

    image.save(output_file_path)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.imshow(PIL.Image.open(output_file_path))
    plt.show()


main()
