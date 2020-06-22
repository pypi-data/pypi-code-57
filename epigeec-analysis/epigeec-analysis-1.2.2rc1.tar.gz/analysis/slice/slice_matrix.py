class SliceMatrix(object):
    @staticmethod
    def slice(matrix, wanted_file_names):
        """
        matrix The Matrix to slice
        wanted_datasets The list of datasets name to keep
        return Sliced Matrix
        """
        return matrix.sub_matrix(
            filter(
                lambda filename: filename in matrix.get_file_names(),
                wanted_file_names
            )
        )
