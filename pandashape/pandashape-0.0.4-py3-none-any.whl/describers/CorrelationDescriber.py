import numpy as np
from .Describer import Describer


class CorrelationDescriber(Describer):
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def get_section_header(self):
        return "Correlated columns"

    def describe(self, df):
        # thanks to Chris Albon: https://chrisalbon.com/machine_learning/feature_selection/drop_highly_correlated_features/
        # Create correlation matrix
        corr_matrix = df.corr().abs()

        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1) > 0)

        # Find index of feature columns with correlation greater than 0.95
        correlated_columns = [column for column in upper.columns if any(upper[column] > self.threshold)]

        if len(correlated_columns) == 0:
            return f"No highly correlated columns (checked with a threshold of f{self.threshold})."

        return f"The following columns are highly correlated (r² > {self.threshold}): {correlated_columns}"
