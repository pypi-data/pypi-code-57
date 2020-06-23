# stats.py
import math
import typing
import json
import os
import functools
import argparse
import logging

import tqdm
import toml
import matplotlib.pyplot as plt

from .pipeline import (
    compute_stats_pipeline,
    convert,
    compute_stats)
from . import __version__

module_logger = logging.getLogger(__name__)

gemscapes_dir = os.path.dirname(os.path.abspath(__file__))



def save_stats(stats: typing.List[typing.Dict[str, float]], file_path: str) -> None:

    fields = list(stats[0].keys())
    stats_reshaped = {}
    for key in fields:
        stats_reshaped[key] = [val[key] for val in stats]

    with open(file_path, "w") as fd:
        json.dump(stats_reshaped, fd)


def get_res_from_gen(compute_stats_gen, file_path):
    for i, res in enumerate(compute_stats_gen(file_path)):
        pass
    return res


def compute_callback(parsed):

    default_config = {
        "convert": {},
        "compute_stats": {
            "fft_size": 32768,
            "image_width": 1000,
            "image_height": 301,
            "peak_width": 2,
        },
        "output_dir": "."
    }


    vars_parsed = vars(parsed)
    configs = default_config.copy()

    if vars_parsed["output_dir"] is not None:
        configs["output_dir"] = vars_parsed["output_dir"]

    if parsed.output_file is None:
        output_file_path = os.path.join(configs["output_dir"], "out.json")
    else:
        output_file = parsed.output_file
        if os.path.isabs(output_file):
            output_file_path = output_file
        else:
            output_file_path = os.path.join(configs["output_dir"], output_file)

    module_logger.debug(f"main: (before) configs={configs}")
    for func_key in default_config:
        if not hasattr(default_config[func_key], "keys"):
            continue
        for key in default_config[func_key]:
            if vars_parsed[key] is not None:
                configs[func_key][key] = vars_parsed[key]
    module_logger.debug(f"main: (after) configs={configs}")

    compute_stats_gen = compute_stats_pipeline(
        lambda file_path, **kwargs: convert(
            file_path, output_dir=configs["output_dir"], **configs["convert"], **kwargs),
        lambda file_path, **kwargs: compute_stats(
            file_path, **configs["compute_stats"], **kwargs)
    )

    results = []

    def progress(iterable):
        if len(iterable) > 1 and not parsed.verbose:
            return tqdm.tqdm(iterable)
        else:
            return iterable

    for file_path in progress(parsed.file_paths):
        for i, res in enumerate(compute_stats_gen(file_path)):
            pass
        results.append(res)

    save_stats(results, output_file_path)


def hist_callback(parsed):

    def create_histogram(file_path, keys):
        with open(file_path, "r") as fd:
            results = json.load(fd)
        nrows = int(math.sqrt(len(keys)))
        ncols = math.ceil(len(keys) / nrows)

        fig, axes = plt.subplots(nrows, ncols)
        if not hasattr(axes, "__getitem__"):
            axes = np.array(axes)
        axes = axes.reshape((nrows, ncols))

        for row in range(nrows):
            for col in range(ncols):
                idx = col + ncols*row
                ax = axes[row, col]
                if idx >= len(keys):
                    ax.axis("off")
                    continue
                ax.hist(results[keys[idx]])
                ax.set_title(keys[idx].capitalize())
                ax.grid(True)

        return fig, axes

    for file_path in parsed.file_paths:
        fig, axes = create_histogram(file_path, parsed.keys)

    plt.show()


def create_parser():
    parser = argparse.ArgumentParser(description="Compute and visualize audio file statistics")

    subparsers = parser.add_subparsers()

    compute_parser = subparsers.add_parser("compute", help="Compute Statistics")

    compute_parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files from which to create gemscapes")
    compute_parser.add_argument("-d", "--outdir", action="store", dest="output_dir",
                        help="Put output files in this directory")
    compute_parser.add_argument("-o", "--outfile", action="store", dest="output_file",
                        help="Name of output file to store statistics. Should be .json file")
    compute_parser.add_argument("--compute-stats.width", dest="image_width", type=int,
                        help="image width in pixels")
    compute_parser.add_argument("--compute-stats.height",  dest="image_height", type=int,
                        help="image height in pixels")
    compute_parser.add_argument("--compute-stats.fft", dest="fft_size", type=int,
                        help="fft size, power of 2 for increased performance")
    compute_parser.add_argument("--compute-stats.peak-width", dest="peak_width", type=int,
                        help="Peak width in resulting images")

    compute_parser.set_defaults(func=compute_callback)

    hist_parser = subparsers.add_parser("hist", help="Create Histogram")

    hist_parser.add_argument("file_paths", metavar="file-paths", nargs="+",
                             help="Create histogram from these JSON files")

    hist_parser.add_argument("-k", "--keys", action="store", dest="keys", nargs="+",
                             help="Key(s) from JSON from which to create histograms")

    hist_parser.set_defaults(func=hist_callback)

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    return parser


def main():
    parsed = create_parser().parse_args()

    level = logging.INFO
    if parsed.verbose:
        level = logging.DEBUG

    logging.basicConfig(level=level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("eyed3").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)

    parsed.func(parsed)


main()
