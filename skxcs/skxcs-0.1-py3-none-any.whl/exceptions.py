class NotPredictedError(AttributeError, ValueError):
    """Exception class to raise if estimator method is used before predicting.

    This class inherits from both ValueError and AttributeError to help with
    exception handling and backward compatibility.

    Examples
    --------
    NotPredictedError("This LinearSVC instance has to predict data first. Call 'predict' with
    appropriate arguments before using this estimator method."...)

    """


class NotTransformedError(AttributeError, ValueError):
    """Exception class to raise if estimator method is used before transforming data.

    This class inherits from both ValueError and AttributeError to help with
    exception handling and backward compatibility.

    Examples
    --------
    NotTransformedError("This LinearSVC instance has to transform data first. Call 'transform_df' with
    appropriate arguments before using this estimator method."...)

    """


class NullValuesError(AttributeError, ValueError):
    """
    """
