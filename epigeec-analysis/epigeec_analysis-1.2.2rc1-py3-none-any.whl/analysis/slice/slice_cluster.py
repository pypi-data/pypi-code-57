from __future__ import absolute_import, division, print_function

import re

from analysis.shared.matrix import Matrix
from analysis.annotate.report.annotate_tsv import AnnotateTsv
from analysis.shared.util.labels import letter_label_to_int_label, int_label_to_letter_label
from .slice_matrix import SliceMatrix

NAMES_REGEX = '[A-Z]+(-[A-Z]+)?(\\,[ ]?[A-Z]+(-[A-Z]+)?)*'
CLUSTER_REGEX = 'cluster\\([0-9]+\\)'

class SliceCluster(object):
    def __init__(self, matrix, annotate_tsv, clustersnames):
        self.matrix = matrix
        self.annotate_tsv = annotate_tsv
        self.clustersnames = clustersnames

    def parse_cluster_names(self, raw_names):
        """
        names raw list of names
        return list of cluster names
        raise Exception
        """
        names_str = ' '.join(raw_names)

        if not re.match(NAMES_REGEX, names_str):
            raise Exception('Bad format for the clusters groups. Must be something like that: "A-C, E"')

        names_subgroups = [sbg.strip() for sbg in names_str.split(',')]

        result = []
        for subgroup in names_subgroups:
            result.extend(self.convert_relative_clusters_to_explicit_list(subgroup))

        if len(result) != len(set(result)):
            raise Exception('Some clusters groups are prensent multiple times')

        return result

    def convert_relative_clusters_to_explicit_list(self, subcluster):
        indvidual_letters = subcluster.split('-')

        if len(indvidual_letters) == 1:
            return indvidual_letters
        elif len(indvidual_letters) == 2:
            return self.make_letter_range(*indvidual_letters)
        else:
            raise Exception('Bad format for the clusters groups catched too late')

    def make_letter_range(self, first_s, second_s):
        first = letter_label_to_int_label(first_s)
        second = letter_label_to_int_label(second_s)

        if second <= first:
            raise Exception('Bad letters range: ' + first_s + '-' + second_s)

        return [int_label_to_letter_label(x) for x in range(first, second + 1)]

    def extract_wanted_file_names(self, annotate_tsv, names):
        cluster_header = self.find_cluster_header(annotate_tsv)
        row_indexes = annotate_tsv.make_filter(cluster_header, lambda x: x in names)
        return annotate_tsv.list_items(annotate_tsv.unique_identifier, row_indexes)

    def find_cluster_header(self, annotate_tsv):
        regex = re.compile(CLUSTER_REGEX)

        for header in annotate_tsv.list_headers():
            matched = regex.match(header)

            if matched:
                return header

        raise Exception('The annotate tsv file contains no cluster')

    def run(self):
        matrix = Matrix.parse_matrixfile(self.matrix)
        annotate_tsv = AnnotateTsv.load_annotate_tsv(self.annotate_tsv)
        names = self.parse_cluster_names(self.clustersnames)
        wanted_file_names = self.extract_wanted_file_names(annotate_tsv, names)

        print(SliceMatrix.slice(matrix, wanted_file_names), end='')
