from analysis.ari.ariapp import AriApp

class AriAppBuilder:
    def __init__(self):
        self.params = {
            'matrix_filename':None,
            'metadata_filename':None,
            'linkage_method':None,
            'breakdown_categories':None,
            'restriction_categories':None,
            'title':None,
            'ignore_user':None,
            'md5sum':False
        }

    def set_matrix_filename(self, matrix_filename):
        self.params['matrix_filename'] = matrix_filename

    def set_metadata_filename(self, metadata_filename):
        self.params['metadata_filename'] = metadata_filename

    def set_linkage_method(self, linkage_method):
        self.params['linkage_method'] = linkage_method

    def set_breakdown_categories(self, breakdown_categories):
        self.params['breakdown_categories'] = breakdown_categories

    def set_restriction_categories(self, restriction_categories):
        self.params['restriction_categories'] = restriction_categories

    def set_title(self, title):
        self.params['title'] = title

    def set_ignore_user(self, ignore_user):
        self.params['ignore_user'] = ignore_user

    def set_md5sum(self, md5sum):
        self.params['md5sum'] = md5sum

    def build(self):
        for k, p in self.params.items():
            if p is None:
                raise Exception('The parameter:\'' + k + '\' is not specified.')

        return AriApp(self.params)
