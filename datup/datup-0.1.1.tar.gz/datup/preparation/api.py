'''
The api take the preparation methods and send it to the root datup folder
'''

from datup.preparation.data_preparation import (
    col_cast, 
    featureselection_correlation, 
    Error,
    CorrelationError,
    remove_chars_metadata,
    to_lowercase_metadata,
    profile_dataset,
    replace_categorical_na,
    replace_numeric_na
) 