import warnings
warnings.filterwarnings("ignore")

from analysis.shared.matrix import Matrix
from analysis.shared.metadata import Metadata
from analysis.ari.breakdowns import Breakdowns

DESCRIPTION = '{matrix_description}, clusteringAlgorithm={clustering_algorithm}, linkageMethod={linkage_method}'

class AriApp:
    def __init__(self, params):
        self.matrix_filename = params['matrix_filename']
        self.metadata_filename = params['metadata_filename']
        self.linkage_method = params['linkage_method']
        self.breakdown_categories = params['breakdown_categories']
        self.restriction_categories = params['restriction_categories']
        self.title = params['title']
        self.ignore_user = params['ignore_user']
        self.md5sum = params['md5sum']

    def run(self):
        # load files
        matrix = self._load_matrix()
        metadata = self._load_metadata()
        
        if self.ignore_user:
            matrix = matrix.sub_matrix(metadata.filenames)

        # parse categories
        restrictions = ['md5sum', 'file_path', 'file_name', 'id', 'virtual', 'assembly']
        ordered_categories = ['assay', 'publishing_group', 'cell_type']

        breakdown_categories = metadata.make_usable_categories(matrix.get_file_names(),
                                                               self.breakdown_categories,
                                                               restrictions,
                                                               ordered_categories)
        restriction_categories = metadata.make_usable_categories(matrix.get_file_names(),
                                                            self.restriction_categories,
                                                            restrictions,
                                                            ordered_categories)

        # Make ARI Annotation
        breakdowns = Breakdowns.make_breakdowns(matrix,
                                                    metadata,
                                                    breakdown_categories,
                                                    restriction_categories,
                                                    self.linkage_method)

        # return report
        return self.breakdowns_to_tsv(breakdowns, matrix.description)

    def breakdowns_to_tsv(self, breakdowns, matrix_description):
        return '\n'.join([self.make_first_line(matrix_description),
                          self.make_ari_lines(breakdowns),
                          self.make_seperator(),
                          self.make_nb_tags_lines(breakdowns)])

    def make_first_line(self, matrix_description):
        return '\t'.join(
            [
                self.title,
                DESCRIPTION.format(
                    matrix_description=matrix_description,
                    clustering_algorithm='hierarchical',
                    linkage_method=self.linkage_method)])

    def make_ari_lines(self, breakdowns):
        header = '\t'.join(['ARI_per_tags_in_category'] +
                           breakdowns.get_restriction_categories() +
                           ['total_nb_datasets'])
        return '\n'.join([header] +
                         [self.make_ari_line(breakdown) for breakdown in breakdowns])

    def make_ari_line(self, breakdown):
        return '\t'.join([breakdown.get_name()] +
                         ['{:.3f}'.format(ari) for ari in breakdown.get_aris()] +
                         [str(breakdown.get_dataset_size())])

    def make_seperator(self):
        return ''

    def make_nb_tags_lines(self, breakdowns):
        header = '\t'.join(['nb_tags_per_category'] + 
                           breakdowns.get_restriction_categories() +
                           ['total_nb_datasets'])
        return '\n'.join([header] +
                         [self.make_nb_tags_line(breakdown) for breakdown in breakdowns])

    def make_nb_tags_line(self, breakdown):
        return '\t'.join([breakdown.get_name()] +
                         [str(nb_clusters) for nb_clusters in breakdown.get_nbs_clusters()] +
                         [str(breakdown.get_dataset_size())])

    def _load_matrix(self):
        return Matrix.parse_matrixfile(self.matrix_filename)

    def _load_metadata(self):
        if self.md5sum:
            unique_identifier = 'md5sum'
        else:
            unique_identifier = 'file_name'

        return Metadata.parse_metadatafile(self.metadata_filename, unique_identifier)
