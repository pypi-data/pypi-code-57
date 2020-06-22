from __future__ import absolute_import, division, print_function

from analysis.shared.util.string_builder import StringBuilder
from .annotateapp_builder import AnnotateAppBuilder


class AnnotateLauncher(object):
    @staticmethod
    def run(args):
        ab = AnnotateAppBuilder()
        ab.set_reordered_matrix_filename(args.rmat)
        ab.set_matrix_filename(args.matrix)
        ab.set_metadata_filename(args.metadata)
        ab.set_desired_nb_clusters(args.k)
        ab.set_groups(args.categories)
        ab.set_pdf_file(args.pdf)
        ab.set_title(StringBuilder(args.title))
        ab.set_tsv_file(args.tsv)
        ab.set_seed(args.seed)
        ab.set_mds(args.mds)
        ab.set_linkage_method(args.linkage)
        ab.set_rescale(args.rescale)
        ab.set_md5sum(args.md5sum)

        ab.build().run()
