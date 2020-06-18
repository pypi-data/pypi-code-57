from abc import ABC, abstractmethod
from functools import wraps
from typing import TYPE_CHECKING, Union, Dict, Tuple

from watson_machine_learning_client.experiment import AutoAI
from watson_machine_learning_client.utils.deployment.errors import (
    WrongDeploymnetType, ModelTypeNotSupported, NotAutoAIExperiment)
from watson_machine_learning_client.utils.autoai.utils import (prepare_auto_ai_model_to_publish, remove_file,
                                                               prepare_auto_ai_model_to_publish_notebook,
                                                               download_experiment_details_from_file)

from pandas import DataFrame

if TYPE_CHECKING:
    from watson_machine_learning_client.helpers.connections import DataConnection
    from ibm_boto3 import resource
    from sklearn.pipeline import Pipeline
    from numpy import ndarray

__all__ = [
    "BaseDeployment"
]


class BaseDeployment(ABC):
    """
    Base abstract class for Deployment.
    """

    def __init__(self, **kwargs):
        self._workspace = None
        self.name = None
        self.id = None
        if kwargs['deployment_type'] == 'online':
            self.scoring_url = None

    def __repr__(self):
        return f"name: {self.name}, id: {self.id}"

    def __str__(self):
        return f"name: {self.name}, id: {self.id}"

    @abstractmethod
    def create(self, **kwargs):
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
        """

        # note: This section is only for deployments with specified experiment_id
        if kwargs['experiment_run_id'] is not None:
            run_params = self._workspace.wml_client.training.get_details(training_uid=kwargs['experiment_run_id'])
            wml_pipeline_details = self._workspace.wml_client.pipelines.get_details(
                run_params['entity']['pipeline']['id'])

            if 'autoai' not in str(wml_pipeline_details):
                raise NotAutoAIExperiment(
                    kwargs['experiment_run_id'], reason="Currently WebService class supports only AutoAI models.")

            print("Preparing an AutoAI Deployment...")

            optimizer = AutoAI(self._workspace).runs.get_optimizer(run_id=kwargs['experiment_run_id'])

            # note: check if user passed a pipeline name instead of object,
            # applicable only for pipelines from experiment
            if isinstance(kwargs['model'], str):
                model = optimizer.get_pipeline(pipeline_name=kwargs['model'], astype=AutoAI.PipelineTypes.SKLEARN)
            else:
                # note: check if model is of lale type, if yes, convert it back to scikit
                try:
                    model = kwargs['model'].export_to_sklearn_pipeline()

                except AttributeError:
                    model = kwargs['model']
                # --- end note
            # --- end note

            # note: download training data to pass it with deployment
            training_data = optimizer.get_data_connections()[0].read()
            training_target = training_data[optimizer.params['prediction_column']]
            training_data = training_data.drop([optimizer.params['prediction_column']], axis=1)
            # --- end note

            model_props = {
                self._workspace.wml_client.repository.ModelMetaNames.NAME: f"{kwargs['deployment_name']} Model",
                self._workspace.wml_client.repository.ModelMetaNames.TYPE: "wml-hybrid_0.1",
                self._workspace.wml_client.repository.ModelMetaNames.RUNTIME_UID: "hybrid_0.1",
            }

            if not self._workspace.wml_client.ICP:
                path = prepare_auto_ai_model_to_publish(
                    pipeline_model=model,
                    run_params=run_params,
                    run_id=kwargs['experiment_run_id'])

                artifact_name = f"{path}model.pickle"

            else:
                schema, artifact_name = prepare_auto_ai_model_to_publish(
                    pipeline_model=model,
                    run_params=run_params,
                    run_id=kwargs['experiment_run_id'],
                    wml_client=self._workspace.wml_client)

                model_props[self._workspace.wml_client.repository.ModelMetaNames.INPUT_DATA_SCHEMA] = [schema]


            deployment_details = self._deploy(
                pipeline_model=artifact_name,
                deployment_name=kwargs['deployment_name'],
                meta_props=model_props,
                training_data=training_data,
                training_target=training_target
            )

            remove_file(filename=artifact_name)

            self.name = kwargs['deployment_name']
            self.id = deployment_details.get('metadata').get('guid')
            if kwargs['deployment_type'] == 'online':
                self.scoring_url = self._workspace.wml_client.deployments.get_scoring_href(deployment_details)
        # --- end note

        # note: This section is for deployments from auto-gen notebook with COS connection
        else:
            # note: only if we have COS connections from the notebook
            if kwargs.get('metadata') is not None:
                if self._workspace.wml_client.ICP:
                    raise NotImplementedError("Deployment of autoai model from auto-gen notebooks from COS "
                                              "not yet supported in CP4D and WML Server")

                print("Preparing an AutoAI Deployment...")

                optimizer = AutoAI().runs.get_optimizer(metadata=kwargs['metadata'])

                # note: check if user passed a pipeline name instead of object,
                # applicable only for pipelines from experiment
                if isinstance(kwargs['model'], str):
                    model = optimizer.get_pipeline(pipeline_name=kwargs['model'], astype=AutoAI.PipelineTypes.SKLEARN)
                else:
                    # note: check if model is of lale type, if yes, convert it back to scikit
                    try:
                        model = kwargs['model'].export_to_sklearn_pipeline()

                    except AttributeError:
                        model = kwargs['model']
                    # --- end note
                # --- end note

                # note: download training data to pass it with deployment
                training_data = optimizer.get_data_connections()[0].read()
                training_target = training_data[optimizer.params['prediction_column']]
                training_data = training_data.drop([optimizer.params['prediction_column']], axis=1)
                # --- end note

                model_props = {
                    self._workspace.wml_client.repository.ModelMetaNames.NAME: f"{kwargs['deployment_name']} Model",
                    self._workspace.wml_client.repository.ModelMetaNames.TYPE: "wml-hybrid_0.1",
                    self._workspace.wml_client.repository.ModelMetaNames.RUNTIME_UID: "hybrid_0.1",
                }

                if not self._workspace.wml_client.ICP:
                    path = prepare_auto_ai_model_to_publish_notebook(
                        pipeline_model=model,
                        result_connection=optimizer._result_client[0],
                        cos_client=optimizer._result_client[1])

                    artifact_name = f"{path}model.pickle"

                    deployment_details = self._deploy(
                        pipeline_model=artifact_name,
                        deployment_name=kwargs['deployment_name'],
                        meta_props=model_props,
                        training_data=training_data,
                        training_target=training_target,
                        result_client=optimizer._result_client
                    )

                    remove_file(filename=artifact_name)

                    self.name = kwargs['deployment_name']
                    self.id = deployment_details.get('metadata').get('guid')
                    if kwargs['deployment_type'] == 'online':
                        self.scoring_url = self._workspace.wml_client.deployments.get_scoring_href(deployment_details)

                else:
                    raise NotImplementedError("Deployment of autoai model from auto-gen notebooks from COS "
                                              "not yet supported in CP4D and WML Server")
            # --- end note

            else:
                raise ModelTypeNotSupported(type(kwargs['model']),
                                            reason="Currently WebService class supports only AutoAI models.")

    @abstractmethod
    def get_params(self):
        """Get deployment parameters."""
        return self._workspace.wml_client.deployments.get_details(self.id)

    @abstractmethod
    def score(self, **kwargs):
        """
        Scoring on WML. Payload is passed to the WML scoring endpoint where model have been deployed.

        Parameters
        ----------
        payload: pandas.DataFrame, required
            DataFrame with data to test the model.
        """
        import pandas as pd

        if isinstance(kwargs['payload'], DataFrame):
            fields = kwargs['payload'].columns.tolist()
            values = kwargs['payload'].values

            # note: scoring endpoint could not recognize NaN values, convert NaN to None
            try:
                values[pd.isnull(values)] = None

            # note: above code fails when there is no null values in a dataframe
            except TypeError:
                pass
            # --- end note

            values = values.tolist()
            # --- end note

            payload = {'fields': fields, 'values': values}
        else:
            raise TypeError('X should be of type pandas.DataFrame.')

        scoring_payload = {self._workspace.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [payload]}

        score = self._workspace.wml_client.deployments.score(self.id, scoring_payload)

        return score

    @abstractmethod
    def delete(self, **kwargs):
        """
        Delete deployment on WML.

        Parameters
        ----------
        deployment_id: str, optional
            ID of the deployment to delete. If empty, current deployment will be deleted.

        deployment_type: str, required
            Type of the deployment: [online, batch]
        """
        if kwargs['deployment_id'] is None:
            self._workspace.wml_client.deployments.delete(self.id)
            self.name = None
            self.scoring_url = None
            self.id = None

        else:
            deployment_details = self._workspace.wml_client.deployments.get_details(
                deployment_uid=kwargs['deployment_id'])
            if deployment_details.get('entity', {}).get(kwargs['deployment_type']) is not None:
                self._workspace.wml_client.deployments.delete(kwargs['deployment_id'])

            else:
                raise WrongDeploymnetType(
                    f"{kwargs['deployment_type']}",
                    reason=f"Deployment with ID: {kwargs['deployment_id']} is not of \"{kwargs['deployment_type']}\" type!")

    @abstractmethod
    def list(self, **kwargs):
        """
        List WML deployments.

        Parameters
        ----------
        limit: int, optional
            Set the limit of how many deployments to list. Default is None (all deployments should be fetched)

        deployment_type: str, required
            Type of the deployment: [online, batch]
        """
        deployments = self._workspace.wml_client.deployments.get_details(limit=kwargs['limit'])
        columns = [
            'created_at',
            'modified_at',
            'id',
            'name',
            'status'
        ]

        data = [
            [deployment.get('metadata')['created_at'],
             deployment.get('metadata')['modified_at'],
             deployment.get('metadata')['guid'],
             deployment.get('metadata')['name'],
             deployment.get('entity')['status']['state'],
             ] for deployment in deployments.get('resources', []) if
            isinstance(deployment.get('entity', {}).get(kwargs['deployment_type']), dict)
        ]

        deployments = DataFrame(data=data, columns=columns).sort_values(by=['created_at'], ascending=False)
        return deployments.head(n=kwargs['limit'])

    @abstractmethod
    def get(self, **kwargs):
        """
        Get WML deployment.

        Parameters
        ----------
        deployment_id: str, required
            ID of the deployment to work with.

        deployment_type: str, required
            Type of the deployment: [online, batch]
        """
        deployment_details = self._workspace.wml_client.deployments.get_details(deployment_uid=kwargs['deployment_id'])
        if deployment_details.get('entity', {}).get(kwargs['deployment_type']) is not None:
            self.name = deployment_details.get('metadata').get('name')
            self.id = deployment_details.get('metadata').get('guid')
            if kwargs['deployment_type'] == 'online':
                self.scoring_url = self._workspace.wml_client.deployments.get_scoring_href(deployment_details)

        else:
            raise WrongDeploymnetType(
                f"{kwargs['deployment_type']}",
                reason=f"Deployment with ID: {kwargs['deployment_id']} is not of \"{kwargs['deployment_type']}\" type!")

    @abstractmethod
    def _deploy(self, **kwargs):
        """Protected method to create a deployment."""
        pass

    def _publish_model(self,
                       pipeline_model: Union['Pipeline', str],
                       meta_props: Dict,
                       training_data: Union['DataFrame', 'ndarray'],
                       training_target: Union['DataFrame', 'ndarray']) -> str:
        """
        Publish model into WML.

        Parameters
        ----------
        pipeline_model: Pipeline or str, required
            Model of the pipeline to publish

        training_data: Union['pandas.DataFrame', 'numpy.ndarray'], required
            Training data for the model

        training_target: Union['pandas.DataFrame', 'numpy.ndarray'], required
            Target/label data for the model

        meta_props: dictionary, required
            Model meta properties.

        Returns
        -------
        String with asset_id.
        """
        import time

        published_model_details = self._workspace.wml_client.repository.store_model(model=pipeline_model,
                                                                                    training_data=training_data,
                                                                                    training_target=training_target,
                                                                                    meta_props=meta_props)

        asset_uid = self._workspace.wml_client.repository.get_model_uid(published_model_details)

        # note: wait until model upload completes
        asset_details = {}
        while (asset_details.get('entity', {'content_status': {}}).get(
                'content_status', {}).get('state', '') != 'persisted'):
            asset_details = self._workspace.wml_client.repository.get_model_details(asset_uid)
            time.sleep(3)
        # --- end note

        print(f"Published model uid: {asset_uid}")
        return asset_uid

    def _publish_model_from_notebook(self,
                                     pipeline_model: Union['Pipeline', str],
                                     meta_props: Dict,
                                     result_client: Tuple['DataConnection', 'resource']) -> str:
        """
        Publish model into WML.

        Parameters
        ----------
        pipeline_model: Pipeline or str, required
            Model of the pipeline to publish

        meta_props: dictionary, required
            Model meta properties.

        result_client: Tuple['DataConnection', 'resource'] required
            Tuple with Result DataConnection object and initialized COS client.

        Returns
        -------
        String with asset_id.
        """
        import time
        import requests
        from watson_machine_learning_client.models import API_VERSION, RUNTIMES

        # note: download treining details from COS (json)
        details = download_experiment_details_from_file(result_client)
        # --- end note

        # note: get the client specific object to be able to call different clients variables
        models = self._workspace.wml_client.repository._client._models

        # note: preparing final metadata to store model in repository
        model_meta = models.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            client=models._client
        )

        if models.ConfigurationMetaNames.RUNTIME_UID in meta_props:
            model_meta.update({models.ConfigurationMetaNames.RUNTIME_UID: {
                "href": API_VERSION + RUNTIMES + "/" + meta_props[
                    models._client.repository.ModelMetaNames.RUNTIME_UID]}})

        model_meta.update({"import": details["entity"]["results_reference"]})
        model_meta["import"]["location"]["path"] = pipeline_model
        # --- end note

        # note: send request to store model with all needed information
        if not self._workspace.wml_client.ICP:
            creation_response = requests.post(
                models._wml_credentials['url'] + '/v4/models',
                headers=models._client._get_headers(),
                json=model_meta
            )

        else:
            raise NotImplementedError("Deployment of autoai model from auto-gen notebooks from COS "
                                      "not yet supported in CP4D and WML Server")

        model_details = models._handle_response(202, u'creating new model', creation_response)
        asset_uid = model_details['metadata']['guid']
        # --- end note

        # note: wait until model upload completes
        asset_details = {}
        while (asset_details.get('entity', {'content_status': {}}).get(
                'content_status', {}).get('state', '') != 'persisted'):
            asset_details = self._workspace.wml_client.repository.get_model_details(asset_uid)
            time.sleep(3)
        # --- end note

        print(f"Published model uid: {asset_uid}")
        return asset_uid

    @staticmethod
    def _project_to_space_to_project(method):
        @wraps(method)
        def _method(self, *method_args, **method_kwargs):
            self._workspace.wml_client.set.default_space(
                self._workspace.space_id) if self._workspace.wml_client.ICP else None

            try:
                method_output = method(self, *method_args, **method_kwargs)

            except Exception as e:
                if not self._workspace.WMLS:
                    self._workspace.wml_client.set.default_project(
                        self._workspace.project_id) if self._workspace.wml_client.ICP else None
                raise e

            else:
                if not self._workspace.WMLS:
                    self._workspace.wml_client.set.default_project(
                        self._workspace.project_id) if self._workspace.wml_client.ICP else None

            return method_output

        return _method
