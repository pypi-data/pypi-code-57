from __future__ import absolute_import, division, print_function

import argparse

from .launcher import EvaluateLauncher

class EvaluateParser(object):
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser(
            'evaluate',
            description='Evaluate the matrix',
            help='Evaluate the matrix')
        parser.set_defaults(func=EvaluateLauncher.run)

        parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
        parser.add_argument('metadata', help='The input metadata json file.', type=str)
        parser.add_argument(
            '--linkage',
            help='The linkage method. By default: "average" Options: "average", "complete", "weighted" or "single".',
            default='average',
            choices=['average', 'complete', 'weighted', 'single'],
            type=str)
        parser.add_argument(
            '--title',
            help='The title of the report.',
            default='epiGeEC Ari 1.0.0',
            type=str)
        parser.add_argument(
            '-b',
            nargs='*',
            help='The breakdown categories. If not specified, it will use all categories in metadata.',
            default=[],
            metavar='category',
            type=str)
        parser.add_argument(
            '-r',
            nargs='*',
            help='The annotation categories restrictions. If not specified, it will use all categories in metadata.',
            default=[],
            metavar='category',
            type=str)
        parser.add_argument(
            '-i',
            help='ignore User',
            action='store_true')
        parser.add_argument(
            '--md5sum',
            help="Set 'md5sum' as the unique identifier for files instead of file_names.",
            action='store_true')
