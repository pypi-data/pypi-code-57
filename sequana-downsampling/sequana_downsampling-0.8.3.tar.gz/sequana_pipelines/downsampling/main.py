import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog

col = Colors()

NAME = "downsampling"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)
        so = InputOptions(add_input_readtag=False)
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument("--downsampling-input-format",
            default="fastq", type=str, choices=["fasta", "fastq", "sam"],
            help="set input format (only 'fastq', 'fasta', 'sam' supported for now)")
        pipeline_group.add_argument("--downsampling-method",
            default="random", type=str, choices=["random", "random_pct"],
            help="""set the downsampling method to be random based on read
                counts (random) on read percentage (random_pct))""")
        pipeline_group.add_argument("--downsampling-percent",
            default=10, type=float,
            help="""Percentage of reads to select""")
        pipeline_group.add_argument("--downsampling-max-entries",
            default=1000, type=int,
            help="""max entries (reads, alignement) to select""")
        pipeline_group.add_argument("--downsampling-threads",
            default=4, type=int,
            help="""max threads to use with pigz""")

        pipeline_group.add_argument("--run", default=False, action="store_true",
            help="Execute the pipeline")


def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])


    from sequana.pipelines_common import SequanaManager

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()
    from sequana import logger
    logger.level = options.level

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config
        cfg.input_directory = os.path.abspath(options.input_directory)
        manager.exists(cfg.input_directory)
        cfg.input_pattern = options.input_pattern
        cfg.input_readtag = None

        # --------------------------------------------------- downsampling
        cfg.downsampling.input_format = options.downsampling_input_format
        cfg.downsampling.method = options.downsampling_method
        cfg.downsampling.percent = options.downsampling_percent
        cfg.downsampling.max_entries = options.downsampling_max_entries
        cfg.downsampling.threads = options.downsampling_threads

        # finalise the command and save it; copy the snakemake. update the config
        # file and save it.

        logger.info("Input data should be {}".format(cfg.downsampling.input_format))
        if cfg.downsampling.method == "random":
            logger.info("Your data will be downsampled randomly keeping {} reads".format(
                cfg.downsampling.max_entries))
        elif cfg.downsampling.method == "random_pct":
            logger.info("Your data will be downsampled randomly keeping {}% of the reads".format(
                cfg.downsampling.percent))


    manager.teardown()

    if options.run:
        subprocess.Popen(["sh", "{}.sh".format(NAME)], cwd=NAME)

if __name__ == "__main__":
    main()
