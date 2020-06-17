from __future__ import absolute_import, division, print_function

import argparse
from .launcher import AnnotateLauncher

class RangeType(object):
    def __init__(self, minv, maxv):
        self.minv = minv
        self.maxv = maxv

    def __call__(self, x):
        value = self.int_type(x)

        if value < self.minv or value > self.maxv:
            raise argparse.ArgumentTypeError('The value "{}" is not between {:,} and {:,}.'.format(value, self.minv, self.maxv))

        return value

    def int_type(self, x):
        try:
            return int(x)
        except ValueError:
            raise argparse.ArgumentTypeError('{!r} is not an integer.'.format(x))

class AnnotateParser(object):
    @staticmethod
    def add_parser(subparsers):
        annotate_parser = subparsers.add_parser(
            'annotate',
            description='Annotate clusters of the matrix',
            help='Annotate clusters of the matrix')
        annotate_parser.set_defaults(func=AnnotateLauncher.run)

        annotate_parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
        annotate_parser.add_argument('--rmat', help='Write a reordered matrix.', type=str)
        annotate_parser.add_argument('--pdf', help='The output pdf file.', type=str)
        annotate_parser.add_argument('--tsv', help='The output tsv file.', type=str)
        annotate_parser.add_argument(
            '--title',
            help='The title of the report.',
            default='epiGeEC Annotate Matrix, k=%(nb_clusters) clusters',
            type=str)
        annotate_parser.add_argument(
            '--mds',
            help='Add a Multidimensional scaling figure (MDS) inside the pdf file.',
            action='store_true')
        annotate_parser.add_argument(
            '--seed',
            help='The seed number to generate the MDS [0-4294967295].',
            type=RangeType(0, 4294967295))
        annotate_parser.add_argument('metadata', help='The input metadata json file.', type=str)
        annotate_parser.add_argument(
            '-k',
            help='The numbers of clusters [1-4294967295]. If not specified, an optimal clustering is used.',
            type=RangeType(1, 4294967295))
        annotate_parser.add_argument(
            '--linkage',
            help='The linkage method. By default: "average" Options: "average", "complete", "weighted" or "single".',
            default='average',
            choices=['average', 'complete', 'weighted', 'single'],
            type=str)
        annotate_parser.add_argument(
            'categories',
            nargs='*',
            help='The categories used inside the reports. If not specified, it will use all categories in metadata.',
            default=[],
            metavar='category',
            type=str)
        annotate_parser.add_argument(
            '--rescale',
            help='Rescale the color of the heatmap with the min and max of the matrix.',
            action='store_true')
        annotate_parser.add_argument(
            '--md5sum',
            help="Set 'md5sum' as the unique identifier for files instead of file_names.",
            action='store_true')
