from typing import List, Dict, Union

from pandas import DataFrame
from watson_machine_learning_client.experiment.autoai.optimizers.local_auto_pipelines import LocalAutoPipelines
from watson_machine_learning_client.helpers import DataConnection
from watson_machine_learning_client.utils.autoai.utils import prepare_cos_client

from .base_auto_pipelines_runs import BaseAutoPipelinesRuns

__all__ = [
    "LocalAutoPipelinesRuns"
]


class LocalAutoPipelinesRuns(BaseAutoPipelinesRuns):
    """
    LocalAutoPipelinesRuns class is used to work with historical Optimizer runs (local optimizer and
    with with data from COS, without WML API interaction).

    Parameters
    ----------
    filter: str, optional
        Filter, user can choose which runs to fetch specifying experiment name. (option not yet available)
    """

    def __init__(self, filter: str = None) -> None:
        self.experiment_name = filter
        self.training_data_reference = None

    def __call__(self, *, filter: str) -> 'LocalAutoPipelinesRuns':
        raise NotImplementedError("Not yet implemented in the local scenario.")

    def list(self) -> 'DataFrame':
        raise NotImplementedError("Not yet implemented in the local scenario.")

    def get_params(self, run_id: str = None) -> dict:
        raise NotImplementedError("Not yet implemented in the local scenario.")

    def get_run_details(self, run_id: str = None) -> dict:
        raise NotImplementedError("Not yet implemented in the local scenario.")

    def get_optimizer(self,
                      run_id: str = None,
                      metadata: Dict[str, Union[List['DataConnection'],  'DataConnection', str, int]] = None
                      ) -> 'LocalAutoPipelines':
        """
        Get historical optimizer from historical experiment.

        Parameters
        ----------
        run_id: str, optional
            ID of the local historical experiment run. (option not yet available)

        metadata: dict, optional
            Option to pass information about COS data reference

        Example
        -------
        >>> metadata = dict(
        >>>        prediction_type ='classification',
        >>>        prediction_column='species',
        >>>        test_size=0.2,
        >>>        scoring='roc_auc',
        >>>        max_number_of_estimators=1,
        >>>        training_data_reference = [DataConnection(
        >>>            connection=S3Connection(
        >>>                api_key='dncf92ubnpo-asocm0890-2om0c-2nc02nci',
        >>>                auth_endpoint='https://iam.stage1.ng.bluemix.net/oidc/token',
        >>>                endpoint_url='https://s3-api.us-geo.objectstorage.softlayer.net'
        >>>            ),
        >>>            location=S3Location(
        >>>                bucket='autoai-bucket',
        >>>                path='iris_dataset.csv',
        >>>            )
        >>>        )],
        >>>        training_result_reference = DataConnection(
        >>>            connection=S3Connection(
        >>>                api_key='dncf92ubnpo-asocm0890-2om0c-2nc02nci',
        >>>                auth_endpoint='https://iam.stage1.ng.bluemix.net/oidc/token',
        >>>                endpoint_url='https://s3-api.us-geo.objectstorage.softlayer.net'
        >>>            ),
        >>>            location=S3Location(
        >>>                bucket='autoai-bucket',
        >>>                path='.',
        >>>                model_location="0a8266be-0f3e-4ef9-af89-856022b7c1c9/data/automl/global_output/",
        >>>                training_status="./75eec2e0-2600-4b7e-bcf2-ea54f2471400/9236e3ab-25e2-4daa-86a8-fd009d4e1e7d/training-status.json",
        >>>            )
        >>>        )
        >>>    )
        >>> optimizer = AutoAI().runs.get_optimizer(metadata)
        """

        if run_id is not None:
            raise NotImplementedError("run_id option is not yet implemented in the local scenario.")

        else:
            # note: save training connection to be able to further provide this data via get_data_connections
            self.training_data_reference: List['DataConnection'] = metadata.get('training_data_reference')

            # note: fill experiment parameters to be able to recreate holdout split
            for data in self.training_data_reference:
                data._fill_experiment_parameters(
                    prediction_type=metadata.get('prediction_type'),
                    prediction_column=metadata.get('prediction_column'),
                    test_size=metadata.get('test_size'),
                    csv_separator=metadata.get('csv_separator', ','),
                    excel_sheet=metadata.get('excel_sheet', 0)
                )
            # --- end note

            data_clients, result_client = prepare_cos_client(
                training_data_references=metadata.get('training_data_reference'),
                training_result_reference=metadata.get('training_result_reference'), )

            optimizer = LocalAutoPipelines(
                name='Auto-gen notebook from COS',
                prediction_type=metadata.get('prediction_type'),
                prediction_column=metadata.get('prediction_column'),
                scoring=metadata.get('scoring'),
                test_size=metadata.get('test_size'),
                max_num_daub_ensembles=metadata.get('max_number_of_estimators'),
                _data_clients=data_clients,
                _result_client=result_client
            )
            optimizer._training_data_reference = self.training_data_reference

            return optimizer

    def get_data_connections(self, run_id: str) -> List['DataConnection']:
        raise NotImplementedError("Not yet implemented in the local scenario.")
