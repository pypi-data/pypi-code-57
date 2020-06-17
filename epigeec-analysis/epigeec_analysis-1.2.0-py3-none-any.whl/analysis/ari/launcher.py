from __future__ import absolute_import, division, print_function

from .ariapp_builder import AriAppBuilder

class EvaluateLauncher(object):
    @staticmethod
    def run(args):
        ab = AriAppBuilder()
        ab.set_matrix_filename(args.matrix)
        ab.set_metadata_filename(args.metadata)
        ab.set_linkage_method(args.linkage)
        ab.set_breakdown_categories(args.b)
        ab.set_restriction_categories(args.r)
        ab.set_title(args.title)
        ab.set_ignore_user(args.i)
        ab.set_md5sum(args.md5sum)

        print(ab.build().run())
