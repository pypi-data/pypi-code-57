from copy import deepcopy
from typing import TYPE_CHECKING, List, Union

from numpy import ndarray
from pandas import DataFrame

from watson_machine_learning_client.helpers.connections import DataConnection, S3Location, FSLocation, DSLocation
from watson_machine_learning_client.utils.autoai.utils import try_import_lale
from watson_machine_learning_client.utils.autoai.errors import FitNotCompleted
from watson_machine_learning_client.utils.autoai.enums import (
    RunStateTypes, PipelineTypes, TShirtSize, ClassificationAlgorithms, RegressionAlgorithms)
from .base_auto_pipelines import BaseAutoPipelines

if TYPE_CHECKING:
    from watson_machine_learning_client.experiment.autoai.engines import WMLEngine
    from watson_machine_learning_client.utils.autoai.enums import Metrics, PredictionType
    from sklearn.pipeline import Pipeline

__all__ = [
    "RemoteAutoPipelines"
]


class RemoteAutoPipelines(BaseAutoPipelines):
    """
    RemoteAutoPipelines class for pipeline operation automation on WML.

    Parameters
    ----------
    name: str, required
        Name for the AutoPipelines

    prediction_type: PredictionType, required
        Type of the prediction.

    prediction_column: str, required
        name of the target/label column

    scoring: Metrics, required
        Type of the metric to optimize with.

    desc: str, optional
        Description

    test_size: float, optional
        Percentage of the entire dataset to leave as a holdout. Default 0.1

    max_num_daub_ensembles: int, optional
        Maximum number (top-K ranked by DAUB model selection) of the selected algorithm, or estimator types,
        for example LGBMClassifierEstimator, XGBoostClassifierEstimator, or LogisticRegressionEstimator
        to use in pipeline composition.  The default is 1, where only the highest ranked by model
        selection algorithm type is used.

    train_sample_rows_test_size: float, optional
        Training data sampling percentage

    daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']], optional
        List of estimators to include in computation process.

    csv_separator: Union[List[str], str], optional
            The separator, or list of separators to try for separating
            columns in a CSV file.  Not used if the file_name is not a CSV file.
            Default is ','.

    excel_sheet: Union[str, int], optional
        Name or number of the excel sheet to use. Only use when xlsx file is an input.
        Default is 0.

    positive_label: str, optional
            The positive class to report when binary classification.
            When multiclass or regression, this will be ignored.

    t_shirt_size: TShirtSize, optional
        The size of the remote AutoAI POD instance (computing resources). Only applicable to a remote scenario.

    engine: WMLEngine, required
        Engine for remote work on WML.

    """

    def __init__(self,
                 name: str,
                 prediction_type: 'PredictionType',
                 prediction_column: str,
                 scoring: 'Metrics',
                 engine: 'WMLEngine',
                 desc: str = None,
                 test_size: float = 0.1,
                 max_num_daub_ensembles: int = 1,
                 t_shirt_size: 'TShirtSize' = TShirtSize.M,
                 train_sample_rows_test_size: float = None,
                 daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']] = None,
                 csv_separator: Union[List[str], str] = ',',
                 excel_sheet: Union[str, int] = 0,
                 positive_label: str = None,
                 notebooks=False,
                 autoai_pod_version=None):
        self.params = {
            'name': name,
            'desc': desc if desc else '',
            'prediction_type': prediction_type,
            'prediction_column': prediction_column,
            'scoring': scoring,
            'test_size': test_size,
            'max_num_daub_ensembles': max_num_daub_ensembles,
            't_shirt_size': t_shirt_size,
            'train_sample_rows_test_size': train_sample_rows_test_size,
            'daub_include_only_estimators': daub_include_only_estimators,
            'csv_separator': csv_separator,
            'excel_sheet': excel_sheet,
            'positive_label': positive_label,
            'notebooks': notebooks,
            'autoai_pod_version': autoai_pod_version
        }
        self._engine: 'WMLEngine' = engine
        self._engine.initiate_remote_resources(params=self.params)
        self.best_pipeline = None
        self._workspace = None

    def _get_engine(self) -> 'WMLEngine':
        """Return WMLEngine for development purposes."""
        return self._engine

    ####################################################
    #   WML Pipeline Part / Parameters for AUtoAI POD  #
    ####################################################
    def get_params(self) -> dict:
        """
        Get configuration parameters of AutoPipelines.

        Returns
        -------
        Dictionary with AutoPipelines parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.get_params()
            {
                'name': 'test name',
                'desc': 'test description',
                'prediction_type': 'classification',
                'prediction_column': 'y',
                'scoring': 'roc_auc',
                'test_size': 0.1,
                'max_num_daub_ensembles': 1,
                't_shirt_size': 'm',
                'train_sample_rows_test_size': 0.8,
                'daub_include_only_estimators': ["ExtraTreesClassifierEstimator",
                                                "GradientBoostingClassifierEstimator",
                                                "LGBMClassifierEstimator",
                                                "LogisticRegressionEstimator",
                                                "RandomForestClassifierEstimator",
                                                "XGBClassifierEstimator"]
            }
        """
        _params = self._engine.get_params().copy()
        del _params['autoai_pod_version']
        del _params['notebooks']

        return _params

    ###########################################################
    #   WML Training Part / Parameters for AUtoAI Experiment  #
    ###########################################################
    def fit(self,
            train_data: 'DataFrame' = None,
            *,
            training_data_reference: List['DataConnection'],
            training_results_reference: 'DataConnection' = None,
            background_mode=False) -> dict:
        """
        Run a training process on WML of autoai on top of the training data referenced by DataConnection.

        Parameters
        ----------
        train_data: pandas.DataFrame, optional
            You can pass a training data to AutoAI fit, it will be stored in your first training_data_reference
            DataConnection COS storage under the bucket and path specified there.
            If there is already some data stored under the specified 'path' and 'bucket',
            this pandas DataFrame will override stored CSV in your COS.

        training_data_reference: List[DataConnection], required
            Data storage connection details to inform where training data is stored.

        training_results_reference: DataConnection, optional
            Data storage connection details to store pipeline training results. Not applicable on CP4D.

        background_mode: bool, optional
            Indicator if fit() method will run in background (async) or (sync).

        Returns
        -------
        Dictionary with run details.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> from watson_machine_learning_client.helpers import DataConnection, S3Connection, S3Location
        >>>
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.fit(
        >>>     training_data_connection=[DataConnection(
        >>>         connection=S3Connection(
        >>>             endpoint_url="https://s3.us.cloud-object-storage.appdomain.cloud",
        >>>             access_key_id="9c92n0scodfa",
        >>>             secret_access_key="0ch827gf9oiwdn0c90n20nc0oms29j"),
        >>>         location=S3Location(
        >>>             bucket='automl',
        >>>             path='german_credit_data_biased_training.csv')
        >>>         )
        >>>     )],
        >>>     DataConnection(
        >>>         connection=S3Connection(
        >>>             endpoint_url="https://s3.us.cloud-object-storage.appdomain.cloud",
        >>>             access_key_id="9c92n0scodfa",
        >>>             secret_access_key="0ch827gf9oiwdn0c90n20nc0oms29j"),
        >>>         location=S3Location(
        >>>             bucket='automl',
        >>>             path='')
        >>>         )
        >>>     ),
        >>>     background_mode=False)
        """

        # note: update each training data connection with pipeline parameters for holdout split recreation
        for data_connection in training_data_reference:
            data_connection.auto_pipeline_params = self._engine._auto_pipelines_parameters

        if isinstance(train_data, DataFrame):
            training_data_reference[0].write(data=train_data,
                                             remote_name=training_data_reference[0].location.path)
        elif train_data is None:
            pass

        else:
            raise TypeError("train_data should be of type pandas.DataFrame")

        for training_connection in training_data_reference:
            # note: set project id when we are working on CP4D and using Data Assets Location
            if isinstance(training_connection.location, DSLocation):
                if self._workspace.WMLS:
                    training_connection.location.href = training_connection.location.href.format(
                        option='space_id',
                        id=self._engine._wml_client.default_space_id)
                else:
                    training_connection.location.href = training_connection.location.href.format(
                        option='project_id',
                        id=self._engine._wml_client.default_project_id)
            # -- end note
        # note: if user did not provide results storage information, use default ones
        if training_results_reference is None:
            if isinstance(training_data_reference[0].location, S3Location):
                training_results_reference = DataConnection(
                    connection=training_data_reference[0].connection,
                    location=S3Location(bucket=training_data_reference[0].location.bucket,
                                        path='')
                )

            else:
                location = FSLocation()
                if self._workspace.WMLS:
                    location.path = location.path.format(option='spaces',
                                                         id=self._engine._wml_client.default_space_id)
                else:
                    location.path = location.path.format(option='projects',
                                                         id=self._engine._wml_client.default_project_id)
                training_results_reference = DataConnection(
                    connection=None,
                    location=location
                )
        # -- end note

        run_params = self._engine.fit(training_data_reference=training_data_reference,
                                      training_results_reference=training_results_reference,
                                      background_mode=background_mode)

        return run_params

    #####################
    #   Run operations  #
    #####################
    def get_run_status(self) -> str:
        """
        Check status/state of initialized AutoPipelines run if ran in background mode

        Returns
        -------
        Dictionary with run status details.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.get_run_status()
            'completed'
        """
        return self._engine.get_run_status()

    def get_run_details(self) -> dict:
        """
        Get fit/run details.

        Returns
        -------
        Dictionary with AutoPipelineOptimizer fit/run details.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.get_run_details()
        """
        return self._engine.get_run_details()

    #################################
    #   Pipeline models operations  #
    #################################
    def summary(self) -> 'DataFrame':
        """
        Prints AutoPipelineOptimizer Pipelines details (autoai trained pipelines).

        Returns
        -------
        Pandas DataFrame with computed pipelines and ML metrics.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.summary()
                           training_normalized_gini_coefficient  ...  training_f1
            Pipeline Name                                        ...
            Pipeline_3                                 0.359173  ...     0.449197
            Pipeline_4                                 0.359173  ...     0.449197
            Pipeline_1                                 0.358124  ...     0.449057
            Pipeline_2                                 0.358124  ...     0.449057
        """
        return self._engine.summary()

    def get_pipeline_details(self, pipeline_name: str = None) -> dict:
        """
        Fetch specific pipeline details, eg. steps etc.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name eg. Pipeline_1, if not specified, best pipeline parameters will be fetched

        Returns
        -------
        Dictionary with pipeline parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> remote_optimizer.get_pipeline_details()
        >>> remote_optimizer.get_pipeline_details(pipeline_name='Pipeline_4')
            {
                'composition_steps': ['TrainingDataset_full_4521_16', 'Split_TrainingHoldout',
                                      'TrainingDataset_full_4068_16', 'Preprocessor_default', 'DAUB'],
                'pipeline_nodes': ['PreprocessingTransformer', 'GradientBoostingClassifierEstimator']
            }
        """
        return self._engine.get_pipeline_details(pipeline_name=pipeline_name)

    def get_pipeline(self,
                     pipeline_name: str = None,
                     astype: 'PipelineTypes' = PipelineTypes.LALE,
                     persist: 'bool' = False) -> Union['Pipeline', 'TrainablePipeline']:
        """
        Download specified pipeline from WML.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name, if you want to see the pipelines names, please use summary() method.
            If this parameter is None, the best pipeline will be fetched.

        astype: PipelineTypes, optional
            Type of returned pipeline model. If not specified, lale type is chosen.

        persist: bool, optional
            Indicates if selected pipeline should be stored locally.

        Returns
        -------
        Scikit-Learn pipeline.

        See also
        --------
        RemoteAutoPipelines.summary()

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(credentials, ...)
        >>> remote_optimizer = experiment.optimizer(...)
        >>>
        >>> pipeline_1 = remote_optimizer.get_pipeline(pipeline_name='Pipeline_1')
        >>> pipeline_2 = remote_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=AutoAI.PipelineTypes.LALE)
        >>> pipeline_3 = remote_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=AutoAI.PipelineTypes.SKLEARN)
        >>> type(pipeline_3)
            <class 'sklearn.pipeline.Pipeline'>
        >>> pipeline_4 = remote_optimizer.get_pipeline(pipeline_name='Pipeline_1', persist=True)
            Selected pipeline stored under: "absolute_local_path_to_model/model.pickle"

        """
        # note: lale should be installed first as lightgbm is sometimes needed during sklearn pipeline load
        if astype == PipelineTypes.LALE:
            try_import_lale()
        # --- end note

        if pipeline_name is None:
            pipeline_model = self._engine.get_best_pipeline(persist=persist)

        else:
            pipeline_model = self._engine.get_pipeline(pipeline_name=pipeline_name, persist=persist)

        if astype == PipelineTypes.SKLEARN:
            return pipeline_model

        elif astype == PipelineTypes.LALE:
            from lale.helpers import import_from_sklearn_pipeline
            return import_from_sklearn_pipeline(pipeline_model)

        else:
            raise ValueError('Incorrect value of \'astype\'. '
                             'Should be either PipelineTypes.SKLEARN or PipelineTypes.LALE')

    # note: predict on top of the best computed pipeline, best pipeline is downloaded for the first time
    def predict(self, X: Union['DataFrame', 'ndarray']) -> 'ndarray':
        """
        Predict method called on top of the best fetched pipeline.

        Parameters
        ----------
        X: numpy.ndarray or pandas.DataFrame, required
            Test data for prediction

        Returns
        -------
        Numpy ndarray with model predictions.
        """
        if self.best_pipeline is None:
            # note: automatically download the best computed pipeline
            if self.get_run_status() == RunStateTypes.COMPLETED:
                self.best_pipeline = self._engine.get_best_pipeline()
            else:
                raise FitNotCompleted(self._engine._current_run_id,
                                      reason="Please check the run status with run_status() method.")
            # --- end note

        if isinstance(X, DataFrame) or isinstance(X, ndarray):
            return self.best_pipeline.predict(X if isinstance(X, ndarray) else X.values)
        else:
            raise TypeError("X should be either of type pandas.DataFrame or numpy.ndarray")

    # --- end note

    def get_data_connections(self) -> List['DataConnection']:
        """
        Create DataConnection objects for further user usage
            (eg. to handle data storage connection or to recreate autoai holdout split).

        Returns
        -------
        List['DataConnection'] with populated optimizer parameters
        """
        optimizer_parameters = self.get_params()
        training_data_references = self.get_run_details()['entity']['training_data_references']

        data_connections = [
            DataConnection._from_dict(_dict=data_connection) for data_connection in training_data_references]

        for data_connection in data_connections:  # note: populate DataConnections with optimizer params
            data_connection.auto_pipeline_params = deepcopy(optimizer_parameters)
            data_connection._wml_client = self._engine._wml_client
            data_connection._run_id = self._engine._current_run_id

        return data_connections
