from typing import TYPE_CHECKING, Any, Dict, Union, List, Optional

from .base_deployment import BaseDeployment
from watson_machine_learning_client.workspace import WorkSpace
from watson_machine_learning_client.helpers import DataConnection
from watson_machine_learning_client.utils import  StatusLogger, print_text_header_h1
from watson_machine_learning_client.wml_client_error import WMLClientError
from watson_machine_learning_client.utils.deployment.errors import EnvironmentNotSupported


from pandas import DataFrame

if TYPE_CHECKING:
    from sklearn.pipeline import Pipeline
    from pandas import DataFrame
    from numpy import ndarray

__all__ = [
    "Batch"
]


class Batch(BaseDeployment):
    """
    The Batch Deployment class.
    With this class object you can manage any batch deployment.

    Parameters
    ----------
    workspace: WorkSpace, required
        a WorkSpace object initialized with WML credentials and optionally with space and project IDs.
    """

    def __init__(self, wml_credentials: Union[dict, 'WorkSpace'] = None, project_id: str = None, space_id: str = None):
        # note: as workspace is not clear enough to understand, there is a possibility to use pure
        # wml credentials with project and space IDs, but in addition we
        # leave a possibility to use a previous WorkSpace implementation, it could be passed as a first argument
        super().__init__(deployment_type='batch')
        if isinstance(wml_credentials, WorkSpace):
            self._workspace = wml_credentials
        else:
            self._workspace = WorkSpace(wml_credentials=wml_credentials.copy(),
                                        project_id=project_id,
                                        space_id=space_id)
        # --- end note

        self.name = None
        self.scoring_url = None
        self.id = None
        self.asset_id = None

    def __repr__(self):
        return f"name: {self.name}, id: {self.id}, asset_id: {self.asset_id}"

    def __str__(self):
        return f"name: {self.name}, id: {self.id}, asset_id: {self.asset_id}"

    def create(self,
               model: Any,
               deployment_name: str,
               metadata: Optional[Dict] = None,
               training_data: Optional[Union['DataFrame', 'ndarray']] = None,
               training_target: Optional[Union['DataFrame', 'ndarray']] = None,
               experiment_run_id: Optional[str] = None) -> None:
        """
        Create deployment from a model.

        Parameters
        ----------
        model: Union[Any, str], required
            Model object to deploy or local path to the model.

        deployment_name: str, required
            Name of the deployment

        training_data: Union['pandas.DataFrame', 'numpy.ndarray'], optional
            Training data for the model

        training_target: Union['pandas.DataFrame', 'numpy.ndarray'], optional
            Target/label data for the model

        metadata: dictionary, optional
            Model meta properties.

        experiment_run_id: str, optional
            ID of a training/experiment (only applicable for AutoAI deployments)

        Example
        -------
        >>> from watson_machine_learning_client.deployment import Batch
        >>>
        >>> deployment = Batch(
        >>>        wml_credentials={
        >>>              "apikey": "...",
        >>>              "iam_apikey_description": "...",
        >>>              "iam_apikey_name": "...",
        >>>              "iam_role_crn": "...",
        >>>              "iam_serviceid_crn": "...",
        >>>              "instance_id": "...",
        >>>              "url": "https://us-south.ml.cloud.ibm.com"
        >>>            },
        >>>         project_id="...",
        >>>         space_id="...")
        >>>
        >>> deployment.create(
        >>>        experiment_run_id="...",
        >>>        model=model,
        >>>        deployment_name='My new deployment'
        >>>    )
        """
        if not self._workspace.wml_client.ICP_30:
            raise EnvironmentNotSupported(reason="Batch deployment is available only for CP4D 3.0 and higher.")

        return super().create(model=model,
                              deployment_name=deployment_name,
                              metadata=metadata,
                              training_data=training_data,
                              training_target=training_target,
                              experiment_run_id=experiment_run_id,
                              deployment_type='batch')

    @BaseDeployment._project_to_space_to_project
    def get_params(self) -> Dict:
        """Get deployment parameters."""
        return super().get_params()

    @BaseDeployment._project_to_space_to_project
    def score(self, payload: Union[DataFrame, List[DataConnection]],
              output_data_filename: 'str' = None, background_mode: 'bool' = True) -> Union[Dict, Dict[str, List], DataConnection]:
        """
        Batch scoring on WML. Payload or Payload data reference is required. It is passed to the WML where model have been deployed.

        Parameters
        ----------
        payload: pandas.DataFrame or List[DataConnection]
            DataFrame with data to test the model or data storage connection details to inform where payload data is stored.

        output_data_filename: str
             Name of csv file where scoring data are saved in the same location as `payload_data_reference`.
             Required when `payload` as type of List[DataConnection] is passed.

        background_mode: bool, optional
            Indicator if score() method will run in background (async) or (sync).

        Returns
        -------
        Dictionary with scoring job details.

        Example
        -------
        >>> score_details = deployment.score(payload=test_data)
        >>> print(score_details['entity']['scoring'])
        {'input_data': [{'fields': ['sepal_length',
                      'sepal_width',
                      'petal_length',
                      'petal_width'],
                     'values': [[4.9, 3.0, 1.4, 0.2]]}],
       'predictions': [{'fields': ['prediction', 'probability'],
                     'values': [['setosa',
                       [0.9999320742502246,
                        5.1519823540224506e-05,
                        1.6405926235405522e-05]]]}]
        >>>
        >>> payload_reference = DataConnection(location=DSLocation(asset_id=asset_id))
        >>> score_details = deployment.score(payload=payload_reference, output_data_filename = "scoring_output.csv")
        """

        if isinstance(payload, DataFrame):
            scoring_payload = {self._workspace.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{'values': payload}]
            }

        elif isinstance(payload, list):
            if isinstance(payload[0], DataConnection):
                payload = [p._to_dict() for p in payload]
            elif isinstance(payload[0], dict):
                pass
            else:
                raise ValueError("Current payload type: list of {} is not supported.".format(type(payload[0])))

            output_data_ref = payload[0].copy()
            if self._workspace.wml_client.ICP_30:
                output_data_ref['location'] = {'name': output_data_filename}
            # elif not self._workspace.wml_client.ICP:
            #     output_data_ref['location'] = {'path': output_data_filename}
            else:
                raise EnvironmentNotSupported(reason="Batch deployment is available only for CP4D 3.0 and higher.")

            scoring_payload = {
                self._workspace.wml_client.deployments.ScoringMetaNames.INPUT_DATA_REFERENCES: payload,
                self._workspace.wml_client.deployments.ScoringMetaNames.OUTPUT_DATA_REFERENCE: output_data_ref}

        else:
            raise ValueError("Incorrect payload type. Required: DataFrame or List[DataConnection], Passed: {}".format(type(payload)))

        scoring_payload['hybrid_pipeline_hardware_specs'] = [{'node_runtime_id': 'auto_ai.kb',
                                                              'hardware_spec': {'name': 'M'}}]
        job_details = self._workspace.wml_client.deployments.create_job(self.id, scoring_payload)

        if background_mode:
            return job_details

        else:
            job_id = self._workspace.wml_client.deployments.get_job_uid(job_details)
            import time
            print_text_header_h1(u'Synchronous scoring for id: \'{}\' started'.format(job_id))

            status = self.get_scoring_status(job_id)['state']

            with StatusLogger(status) as status_logger:
                while status not in ['failed', 'error', 'completed', 'canceled']:
                    time.sleep(10)
                    status = self.get_scoring_status(job_id)['state']
                    status_logger.log_state(status)

            if u'completed' in status:
                print(u'\nScoring job  \'{}\' finished successfully.'.format(job_id))
            else:
                print(u'\nScoring job  \'{}\' failed with status: \'{}\'.'.format(job_id, self.get_scoring_status(job_id)))
                return None

            return self.get_scoring_params(job_id)


    @BaseDeployment._project_to_space_to_project
    def score_rerun(self, scoring_job_id: 'str', background_mode: 'bool' = True) -> Union['dict', 'DataFrame', 'DataConnection']:
        """
        Rerun scoring with the same parameters as job described by 'scoring_job_id'.

        Parameters
        ----------
        scoring_job_id: str
           Id described scoring job.

        background_mode: bool, optional
           Indicator if score_rerun() method will run in background (async) or (sync).

        Returns
        -------
        Dictionary with scoring job details.

        Example
        -------
        >>> scoring_details = deployment.score_rerun(scoring_job_id)
        """
        scoring_params = self.get_scoring_params(scoring_job_id)['entity']['scoring']

        if self._workspace.wml_client.deployments.ScoringMetaNames.INPUT_DATA_REFERENCES in scoring_params:
            payload_ref = [input_ref for input_ref in scoring_params[self._workspace.wml_client.deployments.ScoringMetaNames.INPUT_DATA_REFERENCES]]
            if self._workspace.wml_client.ICP_30:
                output_filename = scoring_params['output_data_reference']['location']['name']
            elif not self._workspace.wml_client.ICP:
                output_filename = scoring_params['output_data_reference']['location']['path']
            else:
                raise EnvironmentNotSupported(reason="Batch deployment is available only for CP4D 3.0 and higher.")

            return self.score(payload=payload_ref, output_data_filename=output_filename, background_mode=background_mode)
        else:
            payload_df = DataFrame.from_dict(scoring_params['input_data'])

            return self.score(payload=payload_df, background_mode=background_mode)


    @BaseDeployment._project_to_space_to_project
    def delete(self, deployment_id: str = None) -> None:
        """
        Delete deployment on WML.

        Parameters
        ----------
        deployment_id: str, optional
            ID of the deployment to delete. If empty, current deployment will be deleted.

        Example
        -------
        >>> deployment = Batch(workspace=...)
        >>> # Delete current deployment
        >>> deployment.delete()
        >>> # Or delete a specific deployment
        >>> deployment.delete(deployment_id='...')
        """
        super().delete(deployment_id=deployment_id, deployment_type='batch')

    @BaseDeployment._project_to_space_to_project
    def list(self, limit=None) -> 'DataFrame':
        """
        List WML deployments.

        Parameters
        ----------
        limit: int, optional
            Set the limit of how many deployments to list. Default is None (all deployments should be fetched)

        Returns
        -------
        Pandas DataFrame with information about deployments.

        Example
        -------
        >>> deployment = Batch(workspace=...)
        >>> deployments_list = deployment.list()
        >>> print(deployments_list)
                             created_at  ...  status
            0  2020-03-06T10:50:49.401Z  ...   ready
            1  2020-03-06T13:16:09.789Z  ...   ready
            4  2020-03-11T14:46:36.035Z  ...  failed
            3  2020-03-11T14:49:55.052Z  ...  failed
            2  2020-03-11T15:13:53.708Z  ...   ready
        """
        return super().list(limit=limit, deployment_type='batch')

    @BaseDeployment._project_to_space_to_project
    def get(self, deployment_id: str) -> None:
        """
        Get WML deployment.


        Parameters
        ----------
        deployment_id: str, required
            ID of the deployment to work with.

        Returns
        -------
        WebService deployment object

        Example
        -------
        >>> deployment = Batch(workspace=...)
        >>> deployment.get(deployment_id="...")
        """
        super().get(deployment_id=deployment_id, deployment_type='batch')

    @BaseDeployment._project_to_space_to_project
    def get_scoring_params(self, scoring_job_id: str = None) -> Dict:
        """Get batch deployment job parameters.

        Parameters
        ----------
        scoring_job_id: str
           Id of scoring job.

        Returns
        -------
        Dictionary with parameters of the scoring job.
           """
        return self._workspace.wml_client.deployments.get_job_details(scoring_job_id)

    @BaseDeployment._project_to_space_to_project
    def get_scoring_status(self, scoring_job_id: str) -> Dict:
        """Get status of scoring job.
        Parameters
        ----------
        scoring_job_id: str
           Id of scoring job.

        Returns
        -------
        Dictionary with state of scoring job (one of: [completed, failed, starting, queued])
            and additional details if they exist.
        """
        return self._workspace.wml_client.deployments.get_job_status(scoring_job_id)

    @BaseDeployment._project_to_space_to_project
    def get_scoring_result(self, scoring_job_id: str) -> Dict:
        """Get batch deployment results of job with id `scoring_job_id`.

        Parameters
        ----------
        scoring_job_id: str
           Id of scoring job which results will be returned.

        Returns
        -------
        Dictionary with predictions for scoring job with inline input data or
            dictionary with data reference to output data if the scoring job has reference to input data.
        In case of incompleted or failed scoring None is returned.
        """
        scoring_params = self.get_scoring_params(scoring_job_id)['entity']['scoring']
        if scoring_params['status']['state'] == 'completed':
            if 'predictions' in scoring_params:
                return scoring_params['predictions']
            else:
                return scoring_params['output_data_reference']
        else:
            return None

    def get_scoring_id(self, batch_scoring_details):
        """Get id from batch scoring details."""
        return self._workspace.wml_client.deployments.get_job_uid(batch_scoring_details)

    def list_scorings(self):
        """Returns pandas DataFrame with list of deployment jobs"""

        resources = self._workspace.wml_client.deployments.get_job_details()['resources']
        columns = [u'job id', u'state', u'creted', u'deployment id']
        values = []
        for scoring_details in resources:
            if 'scoring' in scoring_details['entity']:
                state = scoring_details['entity']['scoring']['status']['state']
                score_values = (scoring_details[u'metadata'][u'guid'], state,
                                scoring_details[u'metadata'][u'created_at'],
                                scoring_details['entity']['deployment']['id'])
                if self.id:
                    if self.id == scoring_details['entity']['deployment']['id']:
                        values.append(score_values)
                else:
                    values.append(score_values)

        return DataFrame(values, columns=columns)

    @BaseDeployment._project_to_space_to_project
    def _deploy(self,
                pipeline_model: 'Pipeline',
                deployment_name: str,
                meta_props: Dict,
                training_data: Union['DataFrame', 'ndarray'],
                training_target: Union['DataFrame', 'ndarray']) -> Dict:
        """
        Deploy model into WML.

        Parameters
        ----------
        pipeline_model: Union['Pipeline', str], required
            Model of the pipeline to deploy

        deployment_name: str, required
            Name of the deployment

        training_data: Union['pandas.DataFrame', 'numpy.ndarray'], required
            Training data for the model

        training_target: Union['pandas.DataFrame', 'numpy.ndarray'], required
            Target/label data for the model

        meta_props: dictionary, required
            Model meta properties.
        """
        deployment_details = {}
        asset_uid = self._publish_model(pipeline_model=pipeline_model,
                                        meta_props=meta_props,
                                        training_data=training_data,
                                        training_target=training_target)

        self.asset_id = asset_uid

        deployment_props = {
            self._workspace.wml_client.deployments.ConfigurationMetaNames.NAME: deployment_name,
            self._workspace.wml_client.deployments.ConfigurationMetaNames.BATCH: {}
        }

        if self._workspace.wml_client.ICP_30:
            asset_href = self._workspace.wml_client.repository.get_model_href(self._workspace.wml_client.repository.get_model_details(asset_uid))

            deployment_props[self._workspace.wml_client.deployments.ConfigurationMetaNames.ASSET] = {
                "href": asset_href
            }
            deployment_props[self._workspace.wml_client.deployments.ConfigurationMetaNames.SPACE_UID] = self._workspace.wml_client.default_space_id

            deployment_props[self._workspace.wml_client.deployments.ConfigurationMetaNames.HYBRID_PIPELINE_HARDWARE_SPECS] = [
                {'node_runtime_id': 'autoai.kb',
                 'hardware_spec': {'name': 'M'}}]
        else:
            deployment_props[self._workspace.wml_client.deployments.ConfigurationMetaNames.COMPUTE] = {
                                                                                        "name": "M",
                                                                                        "nodes": 1
                                                                                      }

        print("Deploying model {} using V4 client.".format(asset_uid))
        try:
            deployment_details = self._workspace.wml_client.deployments.create(
                artifact_uid=asset_uid,
                meta_props=deployment_props)
            self.deployment_id = self._workspace.wml_client.deployments.get_uid(deployment_details)

        except WMLClientError as e:
            raise e

        return deployment_details


