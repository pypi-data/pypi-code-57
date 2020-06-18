from typing import TYPE_CHECKING, Any, Dict, Union, List, Optional

from .base_deployment import BaseDeployment
from watson_machine_learning_client.workspace import WorkSpace
from watson_machine_learning_client.wml_client_error import WMLClientError

from pandas import DataFrame

if TYPE_CHECKING:
    from sklearn.pipeline import Pipeline
    from pandas import DataFrame
    from numpy import ndarray

__all__ = [
    "WebService"
]


class WebService(BaseDeployment):
    """
    An Online Deployment class aka. WebService.
    With this class object you can manage any online (WebService) deployment.

    Parameters
    ----------
    wml_credentials: dictionary, required
        Credentials to Watson Machine Learning instance.

    project_id: str, optional
        ID of the Watson Studio project.

    space_id: str, optional
        ID of the Watson Studio Space.
    """

    def __init__(self, wml_credentials: Union[dict, 'WorkSpace'] = None, project_id: str = None, space_id: str = None):
        # note: as workspace is not clear enough to understand, there is a possibility to use pure
        # wml credentials with project and space IDs, but in addition we
        # leave a possibility to use a previous WorkSpace implementation, it could be passed as a first argument
        super().__init__(deployment_type='online')
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
        return f"name: {self.name}, id: {self.id}, scoring_url: {self.scoring_url}, asset_id: {self.asset_id}"

    def __str__(self):
        return f"name: {self.name}, id: {self.id}, scoring_url: {self.scoring_url}, asset_id: {self.asset_id}"

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
        >>> from watson_machine_learning_client.deployment import WebService
        >>>
        >>> deployment = WebService(
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
        return super().create(model=model,
                              deployment_name=deployment_name,
                              metadata=metadata,
                              training_data=training_data,
                              training_target=training_target,
                              experiment_run_id=experiment_run_id,
                              deployment_type='online')

    @BaseDeployment._project_to_space_to_project
    def get_params(self) -> Dict:
        """Get deployment parameters."""
        return super().get_params()

    @BaseDeployment._project_to_space_to_project
    def score(self, payload: 'DataFrame') -> Dict[str, List]:
        """
        Online scoring on WML. Payload is passed to the WML scoring endpoint where model have been deployed.

        Parameters
        ----------
        payload: pandas.DataFrame, required
            DataFrame with data to test the model.

        Returns
        -------
        Dictionary with list od model output/predicted targets.

        Example
        -------
        >>> predictions = deployment.score(payload=test_data)
        >>> print(predictions)
            {'predictions':
                [{
                    'fields': ['prediction', 'probability'],
                    'values': [['no', [0.9221385608558003, 0.07786143914419975]],
                              ['no', [0.9798324002736079, 0.020167599726392187]]
                }]}
        """
        return super().score(payload=payload)

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
        >>> deployment = WebService(workspace=...)
        >>> # Delete current deployment
        >>> deployment.delete()
        >>> # Or delete a specific deployment
        >>> deployment.delete(deployment_id='...')
        """
        super().delete(deployment_id=deployment_id, deployment_type='online')

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
        >>> deployment = WebService(workspace=...)
        >>> deployments_list = deployment.list()
        >>> print(deployments_list)
                             created_at  ...  status
            0  2020-03-06T10:50:49.401Z  ...   ready
            1  2020-03-06T13:16:09.789Z  ...   ready
            4  2020-03-11T14:46:36.035Z  ...  failed
            3  2020-03-11T14:49:55.052Z  ...  failed
            2  2020-03-11T15:13:53.708Z  ...   ready
        """
        return super().list(limit=limit, deployment_type='online')

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
        >>> deployment = WebService(workspace=...)
        >>> deployment.get(deployment_id="...")
        """
        super().get(deployment_id=deployment_id, deployment_type='online')

    @BaseDeployment._project_to_space_to_project
    def _deploy(self,
                pipeline_model: 'Pipeline',
                deployment_name: str,
                meta_props: Dict,
                training_data: Union['DataFrame', 'ndarray'],
                training_target: Union['DataFrame', 'ndarray'],
                result_client=None) -> Dict:
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

        result_client: Tuple['DataConnection', 'resource'] required
            Tuple with Result DataConnection object and initialized COS client.
        """
        deployment_details = {}
        if result_client is not None:
            asset_uid = self._publish_model_from_notebook(pipeline_model=pipeline_model,
                                                          meta_props=meta_props,
                                                          result_client=result_client)

        else:
            asset_uid = self._publish_model(pipeline_model=pipeline_model,
                                            meta_props=meta_props,
                                            training_data=training_data,
                                            training_target=training_target)

        self.asset_id = asset_uid

        deployment_props = {
            self._workspace.wml_client.deployments.ConfigurationMetaNames.NAME: deployment_name,
            self._workspace.wml_client.deployments.ConfigurationMetaNames.ONLINE: {},
            "hardware_spec": {
                "name": "M",
            }
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
