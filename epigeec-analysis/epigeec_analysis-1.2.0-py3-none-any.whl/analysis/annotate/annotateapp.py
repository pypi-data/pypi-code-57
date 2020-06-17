from analysis.shared.categories import Categories
from analysis.shared.clustering.clusters import Clusters
from analysis.shared.clustering.hierarchical_clustering import HierarchicalClustering
from analysis.shared.clustering.scipypatch import ScipyPatch
from analysis.shared.matrix import Matrix
from analysis.shared.metadata import Metadata
from analysis.config import VERSION

from .annotation import Annotation, Comparison
from .report import pdf
from .report.annotate_tsv import AnnotateTsv
from .report.rendering import Rendering

class AnnotateApp:
    def __init__(self, params):
        self.matrix_filename = params['matrix_filename']
        self.metadata_filename = params['metadata_filename']
        self.groups = params['groups']
        self.title = params['title']
        self.linkage_method = params['linkage_method']
        self.desired_nb_clusters = params['desired_nb_clusters']
        self.pdf_file = params['pdf_file']
        self.tsv_file = params['tsv_file']
        self.reordered_matrix_filename = params['reordered_matrix_filename']
        self.seed = params['seed']
        self.mds = params['mds']
        self.rescale = params['rescale']
        self.md5sum = params['md5sum']

    def run(self):
        #load files
        matrix = self._load_matrix()
        data = self._load_metadata()

        #base data
        restrictions = ['md5sum', 'file_path', 'file_name', 'id', 'virtual', 'assembly']
        ordered_categories = ['assay', 'publishing_group', 'cell_type']
        groups = data.make_usable_categories(matrix.get_file_names(),
                                             self.groups,
                                             restrictions,
                                             ordered_categories)

        # clustering
        clusters = HierarchicalClustering.make_clusters(matrix, self.linkage_method, self.desired_nb_clusters)

        # Categories
        categories = Categories.make_categories(data, matrix.get_file_names(), groups)

        # Comparison
        remapped_clusters = ScipyPatch.rename_clusters(clusters, matrix)
        comparison = Comparison(remapped_clusters, categories)

        matrix = ScipyPatch.reorder_matrix(remapped_clusters, matrix)

        # Annotation
        annotation = Annotation(matrix, data, comparison)

        # pdf export
        if self.pdf_file is not None:
            self._export_pdf(groups, annotation)

        # tsv export
        if self.tsv_file is not None:
            self._export_tsv(annotation)

        if self.reordered_matrix_filename is not None:
            self._write_reordered_matrix(annotation)

    def _export_pdf(self, groups, annotation):
        cr = Rendering("epiGeEC-Annotate version {}".format(VERSION))

        self.title.set('nb_clusters', annotation.get_nb_clusters())
        files = cr.render(annotation, self.title.build(), self.seed, self.mds, groups, self.rescale)

        pdf.create_pdf(self.pdf_file, files)

    def _export_tsv(self, annotation):
        metadata = annotation.get_metadata()

        restrictions = ['file_path', 'id', 'virtual']
        ordered_categories = ['assay', 'cell_type', 'publishing_group', 'assembly']
        categories_names = metadata.make_usable_categories(annotation.get_file_names(),
                                                          None,
                                                          restrictions,
                                                          ordered_categories)

        with open(self.tsv_file, 'w') as tsv_file:
            AnnotateTsv.annotation_to_tsv(annotation, categories_names, tsv_file)

    def _write_reordered_matrix(self, annotation):
        matrix = annotation.get_matrix()
        with open(self.reordered_matrix_filename, 'w') as rmat_f: 
            matrix.write(rmat_f)

    def _load_matrix(self):
        return Matrix.parse_matrixfile(self.matrix_filename)

    def _load_metadata(self):
        if self.md5sum:
            unique_identifier = 'md5sum'
        else:
            unique_identifier = 'file_name'

        return Metadata.parse_metadatafile(self.metadata_filename, unique_identifier)
