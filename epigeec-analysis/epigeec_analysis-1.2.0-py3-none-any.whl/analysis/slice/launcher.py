from __future__ import absolute_import, division, print_function

from .slice_cluster import SliceCluster
from .slice_filename import SliceFilename

class SliceFilenameLauncher(object):
    @staticmethod
    def run(args):
        SliceFilename(
            args.matrix, args.file_names
        ).run()

class SliceClusterLauncher(object):
    @staticmethod
    def run(args):
        SliceCluster(
            args.matrix, args.annotate_tsv, args.clustersnames
        ).run()
