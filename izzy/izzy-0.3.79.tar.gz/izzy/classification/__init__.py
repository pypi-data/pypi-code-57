
from .generic import *
from .logistic import *
from .metrics import *
from .tree import *

# Module contents
__all__ = [
    'accuracy',
    'aic',
    'bic',
    'confusion_matrix',
    'create_engine_from_string',
    'f1',
    'false_negatives',
    'false_positives',
    'GenericModel',
    'gini',
    'hit_rate',
    'ks',
    'LogisticRegression',
    'performance_report',
    'positive_predictive_value',
    'precision',
    'recall',
    'roc',
    'roc_auc',
    'roc_plot',
    'selectivity',
    'sensitivity',
    'specificity',
    'true_negatives',
    'true_negative_rate',
    'true_positives',
    'true_positive_rate',
    'weight_of_evidence'
]


# Create machine learning model engine from string
# TODO find a home for this. It does not belong in __init__
def create_engine_from_string(identifier):
    """
    Create a machine learning model engine from a string

    Parameters
    ----------
    identifier : str
        String identifier of engine

    Returns
    -------
    engine : object
        An instance of an izzy model class.
    """

    # Type check
    assert isinstance(identifier, str), 'identifier must be string'

    # Convert to lowercase for simplicity and strip and white space
    identifier = identifier.lower().replace(' ', '')

    # Create engine (There needs to be a default; what should this be?)
    engine = None
    if identifier in ('lr', 'logisticregression', 'logit'):
        engine = LogisticRegression(penalty='none', solver='lbfgs', class_weight='balanced', warm_start=False)
    elif identifier in ('rf', 'randomforest'):
        engine = RandomForest()

    # Return
    return engine
