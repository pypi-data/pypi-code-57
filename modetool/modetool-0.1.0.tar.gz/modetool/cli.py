import argparse
import multiprocessing

from .modetool import MODETool


def main():
    parser = argparse.ArgumentParser(description="MODE Tool")
    parser.add_argument(
        "-i", "--input", type=str, help="Directory containing compressed images."
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Directory for extracting images too."
    )
    parser.add_argument(
        "-r", "--regions", type=str, help="Comma-separated list of regions to filter by."
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=int(multiprocessing.cpu_count()),
        help="The number of worker threads to use.",
    )
    parser.add_argument(
        "-s", "--sort", help="Extract images to subdirectories based on region.", action="store_true",
    )

    args = parser.parse_args()

    regions = []

    if args.regions:
        regions = args.regions.split(",")

    mode = MODETool(
        input=args.input,
        output=args.output,
        regions=regions,
        workers=args.workers,
        sort=args.sort,
    )

    mode.run()
