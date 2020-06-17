from analysis.annotate.annotateapp import AnnotateApp
from analysis.shared.exception.geecanalysisexception import GeecAnalysisException

class AnnotateAppBuilderException(GeecAnalysisException):
    pass

class ParameterAnnotateAppBuilderException(AnnotateAppBuilderException):
    pass

class AnnotateAppBuilder:
    def __init__(self):
        self.params = {
            'matrix_filename':None,
            'metadata_filename':None,
            'groups':None,
            'title':None,
            'linkage_method':None,
            'desired_nb_clusters':None,
            'pdf_file':None,
            'tsv_file':None,
            'reordered_matrix_filename':None,
            'seed':None,
            'mds':False,
            'rescale':False,
            'md5sum':False
        }
        self.needed = ['matrix_filename', 'metadata_filename', 'groups', 'title', 'linkage_method']

    def set_title(self, title):
        self.params['title'] = title

    def set_matrix_filename(self, matrix_filename):
        self.params['matrix_filename'] = matrix_filename

    def set_metadata_filename(self, metadata_filename):
        self.params['metadata_filename'] = metadata_filename

    def set_desired_nb_clusters(self, desired_nb_clusters):
        self.params['desired_nb_clusters'] = desired_nb_clusters

    def set_groups(self, groups):
        self.params['groups'] = groups

    def set_pdf_file(self, pdf_file):
        self.params['pdf_file'] = pdf_file

    def set_tsv_file(self, tsv_file):
        self.params['tsv_file'] = tsv_file

    def set_linkage_method(self, linkage_method):
        self.params['linkage_method'] = linkage_method

    def set_reordered_matrix_filename(self, reordered_matrix_filename):
        self.params['reordered_matrix_filename'] = reordered_matrix_filename

    def set_seed(self, seed):
        self.params['seed'] = seed

    def set_mds(self, mds):
        self.params['mds'] = mds

    def set_rescale(self, rescale):
        self.params['rescale'] = rescale

    def set_md5sum(self, md5sum):
        self.params['md5sum'] = md5sum

    def build(self):
        for p in self.needed:
            if self.params.get(p) is None:
                raise ParameterAnnotateAppBuilderException('The parameter:\'' + p + '\' is not specified.')

        return AnnotateApp(self.params)
