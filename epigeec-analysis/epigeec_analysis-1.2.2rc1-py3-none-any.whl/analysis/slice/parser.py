from __future__ import print_function, division, absolute_import

from .launcher import SliceFilenameLauncher, SliceClusterLauncher

class SliceFilenameParser(object):
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser(
            'slice-filename',
            description='Slice the matrix to keep specified filename(s).',
            help='Slice the matrix to keep specified filename(s).'
        )
        parser.set_defaults(func=SliceFilenameLauncher.run)

        parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
        parser.add_argument('file_names', help='The input file_names text file.', type=str)

class SliceClusterParser(object):
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser(
            'slice-cluster',
            description='Slice the matrix to keep specified cluster(s).',
            help='Slice the matrix to keep specified cluster(s).'
        )
        parser.set_defaults(func=SliceClusterLauncher.run)

        parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
        parser.add_argument('annotate_tsv', help='The input annotate tsv file.', type=str)
        parser.add_argument('clustersnames', help='The clusters names (e.g. "A-E, H").', type=str)
