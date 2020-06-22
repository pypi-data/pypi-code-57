import pandas
import csv
from itertools import chain

class AnnotateTsv:
    def __init__(self, headers, matrix):
        self._matrix_index = {h:_Header.make_header(h, i, matrix)
                              for i, h in enumerate(headers)}
        self._matrix = matrix
        self.unique_identifier = headers[0]

    def list_headers(self):
        return self._matrix_index.keys()

    def make_filter(self, header_name, cond):
        header = self._matrix_index[header_name]
        return header.filter_index(cond)

    def list_items(self, header, *filters):
        row_indexes = set(range(len(self._matrix))).intersection(*filters)
        col_index = self._matrix_index[header].get_index_col()
        return [self._matrix[row_index, col_index] for row_index in row_indexes]

    @staticmethod
    def load_annotate_tsv(tsv_filename):
        with open(tsv_filename, 'r') as tsv_file:
            return AnnotateTsv.load_annotate_tsv_file(tsv_file)

    @staticmethod
    def load_annotate_tsv_file(tsv_file):
        dframe = pandas.read_csv(tsv_file,
                                 comment='#',
                                 delimiter='\t',
                                 index_col=False,
                                 keep_default_na=False)

        return AnnotateTsv(dframe.columns.values.tolist(), dframe.values)

    @staticmethod
    def annotation_to_tsv(annotation, categories_names, tsv_file):
        nb_clusters = annotation.get_nb_clusters()
        unique_identifier = annotation.get_metadata().unique_identifier
        filtered_cat_names = [x for x in categories_names if x != unique_identifier]

        description = '# {}'.format(annotation.description)
        datasets = annotation.annotation_datagrid_iter(filtered_cat_names)
        header = [unique_identifier, 'cluster({})'.format(nb_clusters)] + filtered_cat_names
        rows = chain([[description]], [header], datasets)
        
        AnnotateTsv._write_tsv(rows, tsv_file)

    @staticmethod
    def _write_tsv(rows, tsv_file):
        tsv_file.write(
            u'\n'.join(
                [u'\t'.join(
                    [u'{}'.format(cell)
                     for cell in row])
                 for row in rows]).encode('utf-8'))

class _Header:
    def __init__(self, header, index_col, values={}):
        self._header = header
        self._index_col = index_col
        self._values = values

    def get_index_col(self):
        return self._index_col

    def filter_index(self, cond):
        return [idx for value in self._values.values()
                if cond(value.get_name())
                for idx in value.get_indexes()]

    @staticmethod
    def make_header(header, index_col, matrix):
        values = {}
        for row_idx in range(len(matrix)):
            value_name = matrix[row_idx, index_col]
            
            if value_name in values:
                values[value_name].append(row_idx)
            else:
                values[value_name] = _Value(value_name, [row_idx])

        return _Header(header, index_col, values)

class _Value:
    def __init__(self, name, indexes=[]):
        self._name = name
        self._indexes = indexes

    def get_indexes(self):
        return self._indexes

    def get_name(self):
        return self._name

    def append(self, index):
        self._indexes.append(index)
