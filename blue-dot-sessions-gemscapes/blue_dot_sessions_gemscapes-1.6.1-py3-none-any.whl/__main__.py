# __main__.py
import os
import functools
import argparse
import logging

import tqdm
import toml

from .pipeline import (
    pipeline,
    pipeline_stage_names,
    pipeline_stage_count,
    process_pipeline_stages,
    convert,
    wav2png,
    post_wav2png,
    primitive,
    post_primitive)
from .color import (
    interpolate_colors_fn_lookup,
    COLOR_SCHEMES,
    DEFAULT_COLOR_SCHEME_KEY)
from . import __version__

module_logger = logging.getLogger(__name__)

gemscapes_dir = os.path.dirname(os.path.abspath(__file__))

def create_parser():
    interpolate_colors_fn_names = ", ".join([f"'{name}'" for name in interpolate_colors_fn_lookup])
    color_scheme_names = ["'{}'".format(key) for key in COLOR_SCHEMES.keys()]
    color_scheme_str = ", ".join(color_scheme_names)

    pipeline_stage_names_str = ", ".join(pipeline_stage_names)

    parser = argparse.ArgumentParser(description="Create gemscapes from audio files")

    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files from which to create gemscapes")
    parser.add_argument("-d", "--outdir", action="store", dest="output_dir",
                        help="Put output files in this directory")
    parser.add_argument("-c", "--config", action="store",
                        help="Configuration file to use to modify output gemscapes")
    parser.add_argument("--wav2png.width", dest="image_width", type=int,
                        help="image width in pixels")
    parser.add_argument("--wav2png.height",  dest="image_height", type=int,
                        help="image height in pixels")
    parser.add_argument("--wav2png.fft", dest="fft_size", type=int,
                        help="fft size, power of 2 for increased performance")
    parser.add_argument("--wav2png.peak-width", dest="peak_width", type=int,
                        help="Peak width in resulting images")
    parser.add_argument("--wav2png.color-scheme-file", action="store",
                        dest="color_scheme_file_path", type=str,
                        help="path to file containing color scheme configurations")
    parser.add_argument("--wav2png.color-scheme", action="store", dest="color_scheme", type=str,
                        help="name of the color scheme to use (one of: {})".format(color_scheme_str))
    parser.add_argument("--wav2png.color-space", dest="color_space", type=str,
                        help=("Color space in which to do interpolation. "
                              f"Available values are {interpolate_colors_fn_names}."))
    parser.add_argument("--wav2png.color-range", dest="color_range", type=float,
                        help="Percentage of color palette to use")
    parser.add_argument("--wav2png.mu-cut", dest="mu_cut", type=float,
                        help=("Don't consider spectral centroid values above this when "
                              "interpolating between spectral centroid and color palette"))
    parser.add_argument("--post-wav2png.v-scale",  dest="v_wssf", type=float,
                        help="Vertical white space scaling factor")
    parser.add_argument("--post-wav2png.h-scale",  dest="h_wssf", type=float,
                        help="Horizontal white space scaling factor")
    parser.add_argument("--primitive.primitive-exec", action="store", dest="primitive_exec", type=str,
                        help="Specify path to primitive executable.")
    parser.add_argument("--primitive.primitive-args", action="store", dest="primitive_args", type=str,
                        help="Specify arguments to pass to primitive executable. Must include '-n <int>' argument")
    parser.add_argument("--post-primitive.black-thresh", action="store", dest="thresh", type=float,
                        help="Specify a RGB distance threshold below which to set a shape's color to transparent")

    parser.add_argument("--pipeline-range", action="store", dest="pipeline_stage", type=str,
                        default="0:", help=("Specify which range of pipeline stages to compute. "
                                            "Uses Python range/slice syntax, eg if 1:3 is specified, then the second and third stage are done. "
                                            "If a single number is specified, the pipeline will do up to specified number, ie :{number}. "
                                             f"Total number of stages is {pipeline_stage_count}. "
                                             f"Pipeline stages are {pipeline_stage_names_str}. "
                                             "(default %(default)s)"))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    parser.add_argument('--version', action='version', version=f"{__version__}")

    return parser


def load_config(file_path: str) -> dict:
    with open(file_path, "r") as fd:
        config = toml.load(fd)
    return config


def main():
    parser = create_parser()
    parsed = parser.parse_args()


    default_color_scheme_file_path = os.path.join(
        os.path.dirname(gemscapes_dir),
        "blue_dot_sessions.color.toml"
    )

    default_config = {
        "convert": {},
        "wav2png": {
            "fft_size": 32768,
            "image_width": 1000,
            "image_height": 301,
            "peak_width": 2,
            "color_scheme": "blue_dot_sessions",
            "color_scheme_file_path": default_color_scheme_file_path,
            "color_space": "snap_to",
            "color_range": 0.7,
            "mu_cut": 2.5
        },
        "post_wav2png": {
            "v_wssf": 1.0,
            "h_wssf": 1.1
        },
        "primitive": {
            "primitive_args": "-n 30 -m 8 -bg #ffffff00 -kt 0.35 -at 0.3",
            "primitive_exec": "primitive"
        },
        "post_primitive": {
            "thresh": 0.35
        },
        "output_dir": None
    }


    log_level = logging.ERROR
    if parsed.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("eyed3").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)

    vars_parsed = vars(parsed)
    configs = default_config.copy()

    pipeline_stage = parsed.pipeline_stage

    if parsed.config:
        loaded_config = load_config(parsed.config)
        for func_key in default_config:
            if default_config[func_key] is None:
                continue
            module_logger.debug(f"main: func_key={func_key}")
            func_config = loaded_config.get(func_key, {})
            func_config = {key: func_config[key] for
                           key in func_config if key in default_config[func_key]}
            configs[func_key].update(func_config)

        if "output_dir" in loaded_config:
            configs["output_dir"] = loaded_config["output_dir"]

    if vars_parsed["output_dir"] is not None:
        configs["output_dir"] = vars_parsed["output_dir"]

    module_logger.debug(f"main: (before) configs={configs}")
    for func_key in default_config:
        if default_config[func_key] is None:
            continue
        for key in default_config[func_key]:
            if vars_parsed[key] is not None:
                configs[func_key][key] = vars_parsed[key]
    module_logger.debug(f"main: (after) configs={configs}")

    if "h_wssf" in configs["post_wav2png"]:
        configs["post_primitive"]["h_wssf"] = 1.0/configs["post_wav2png"]["h_wssf"]

    if "v_wssf" in configs["post_wav2png"]:
        configs["post_primitive"]["v_wssf"] = 1.0/configs["post_wav2png"]["v_wssf"]


    pipeline_stages = process_pipeline_stages(parsed.pipeline_stage)

    gemscape_gen = pipeline(
        lambda file_path, **kwargs: convert(
            file_path, output_dir=configs["output_dir"], **configs["convert"], **kwargs),
        lambda file_path, **kwargs: wav2png(
            file_path, normalize=True, **configs["wav2png"], **kwargs
        ),
        functools.partial(post_wav2png, **configs["post_wav2png"]),
        lambda file_path, **kwargs: primitive(
            file_path, **configs["primitive"], **kwargs
        ),
        functools.partial(post_primitive, **configs["post_primitive"])
    )

    def progress(iterable):
        if len(iterable) > 1 and not parsed.verbose:
            return tqdm.tqdm(iterable)
        else:
            return iterable


    for file_path in progress(parsed.file_paths):
        for i, res in enumerate(gemscape_gen(file_path, stages=pipeline_stages)):
            pass
            # if i == pipeline_stage:
            #     break
    # plt.show()
main()
