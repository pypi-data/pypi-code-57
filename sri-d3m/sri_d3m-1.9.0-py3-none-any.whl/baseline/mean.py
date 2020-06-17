import typing

from d3m import container
from d3m.metadata import base as meta_base
from d3m.metadata import hyperparams as meta_hyperparams
from d3m.metadata import params as meta_params
from d3m.primitive_interfaces import base as pi_base
from d3m.primitive_interfaces import unsupervised_learning as pi_unsupervised_learning

from sri.common import config
from sri.common import constants
from sri.common import util

Inputs = container.DataFrame
Outputs = container.DataFrame

class MeanBaselineHyperparams(meta_hyperparams.Hyperparams):
    pass

class MeanBaselineParams(meta_params.Params):
    target_name: str
    categorical_prediction: bool
    prediction: str

class MeanBaseline(pi_unsupervised_learning.UnsupervisedLearnerPrimitiveBase[Inputs, Outputs, MeanBaselineParams, MeanBaselineHyperparams]):
    """
    A simple baseline that just predicts the mean/plurality.
    This is not meant to be used in production, just a way to get quick and reasonable answers for debugging.
    """

    def __init__(self, *, hyperparams: MeanBaselineHyperparams, random_seed: int = 0) -> None:
        super().__init__(hyperparams = hyperparams, random_seed = random_seed)

        self._target_name = None
        self._categorical_prediction = None
        self._prediction = None

    def set_training_data(self, *, inputs: Inputs) -> None:
        labels, average, target_name = self._validate_training_input(inputs)
        self._target_name = target_name
        self._prediction, self._categorical_prediction = self._process_data(labels, average)

    def fit(self, *, timeout: float = None, iterations: int = None) -> pi_base.CallResult[None]:
        return pi_base.CallResult(None)

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> pi_base.CallResult[Outputs]:
        self.logger.debug("Starting produce")

        ids = self._validate_test_input(inputs)
        ids = [int(id) for id in ids]

        predictions = [self._prediction for id in ids]

        results = container.DataFrame(
            data = {constants.D3M_INDEX: ids, self._target_name: predictions},
            columns = [constants.D3M_INDEX, self._target_name],
            generate_metadata = True,
        )

        results = util.prep_predictions(results, ids, metadata_source = self, missing_value = self._prediction)

        self.logger.debug("Produce complete")

        return pi_base.CallResult(results)

    def get_params(self) -> MeanBaselineParams:
        return MeanBaselineParams({
            'target_name': self._target_name,
            'categorical_prediction': self._categorical_prediction,
            'prediction': str(self._prediction),
        })

    def set_params(self, *, params: MeanBaselineParams) -> None:
        self._target_name = params['target_name']
        self._categorical_prediction = params['categorical_prediction']

        if (self._categorical_prediction):
            self._prediction = params['prediction']
        else:
            self._prediction = float(params['prediction'])

    def _validate_training_input(self, inputs: Inputs):
        target_column = None
        average = False

        # Skip types without columns.
        if (constants.TABLE_TYPE not in inputs.metadata.query(tuple())['semantic_types']):
            raise ValueError("Expecting a table.")

        numCols = int(inputs.metadata.query((meta_base.ALL_ELEMENTS, ))['dimension']['length'])
        for i in range(numCols):
            column_info = inputs.metadata.query((meta_base.ALL_ELEMENTS, i))

            if (constants.TRUE_TARGET_TYPE not in column_info['semantic_types']):
                continue

            target_column = column_info['name']
            average = (constants.FLOAT_TYPE in column_info['semantic_types'])
            break

        if (target_column is None):
            raise ValueError("Could not figure out target column.")

        labels = list(inputs[target_column])

        if (average):
            labels = [float(value) for value in labels]

        return labels, average, target_column

    # Just get the d3mIndexes
    def _validate_test_input(self, inputs: Inputs):
        return list(inputs[constants.D3M_INDEX])

    def _process_data(self, labels, average):
        self.logger.debug("Processing data")

        predicted_value = None
        categorical_prediction = None

        if (average):
            predicted_value = self._calc_mean(labels)
            categorical_prediction = False
        else:
            predicted_value = self._calc_plurality(labels)
            categorical_prediction = True

        self.logger.debug("Data processing complete")

        return predicted_value, categorical_prediction

    def _calc_mean(self, labels):
        mean = 0.0
        for label in labels:
            mean += label
        mean /= len(labels)

        return mean

    def _calc_plurality(self, labels):
        counts = {}

        for label in labels:
            if (label not in counts):
                counts[label] = 0
            counts[label] += 1

        best_count = 0
        best_label = None

        for (label, count) in counts.items():
            if (count > best_count):
                best_count = count
                best_label = label

        return best_label

    metadata = meta_base.PrimitiveMetadata({
        # Required
        'id': '36d5472c-e0a4-4ed6-a1d0-2665feacff39',
        'version': config.VERSION,
        'name': 'Mean Baseline',
        'description': 'A baseline primitive that just predicate the mean/plurality. Not indented for production, only debugging.',
        'python_path': 'd3m.primitives.learner.mean_baseline.MeanBaseline',
        'primitive_family': meta_base.PrimitiveFamily.LEARNER,
        'algorithm_types': [
            meta_base.PrimitiveAlgorithmType.COMPUTER_ALGEBRA,
        ],
        'source': config.SOURCE,

        # Optional
        'keywords': [ 'preprocessing', 'primitive', 'dataset'],
        'installation': [ config.INSTALLATION ],
        'location_uris': [],
        'preconditions': [ meta_base.PrimitiveEffect.NO_MISSING_VALUES ],
        'effects': [ meta_base.PrimitiveEffect.NO_MISSING_VALUES ],
        'hyperparms_to_tune': []
    })
