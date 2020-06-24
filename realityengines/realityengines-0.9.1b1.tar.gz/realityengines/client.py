import inspect
import io
import logging
import requests
import time

from packaging import version

from .api_key import ApiKey
from .batch_prediction import BatchPrediction
from .bucket_verification import BucketVerification
from .bucket_verification_instructions import BucketVerificationInstructions
from .bucket_verification_result import BucketVerificationResult
from .schema import Schema
from .dataset import Dataset
from .dataset_upload import DatasetUpload
from .dataset_version import DatasetVersion
from .deployment import Deployment
from .deployment_auth_token import DeploymentAuthToken
from .model import Model
from .model_metrics import ModelMetrics
from .model_version import ModelVersion
from .project import Project
from .project_dataset import ProjectDataset
from .project_validation import ProjectValidation
from .refresh_pipeline_run import RefreshPipelineRun
from .refresh_policy import RefreshPolicy
from .streaming_auth_token import StreamingAuthToken
from .training_config_options import TrainingConfigOptions
from .use_case import UseCase
from .use_case_requirements import UseCaseRequirements


class ApiException(Exception):
    def __init__(self, message, http_status, exception=None):
        self.message = message
        self.http_status = http_status
        self.exception = exception or 'ApiException'

    def __str__(self):
        return f'{self.exception}({self.http_status}): {self.message}'


class ReClient():
    client_version = '0.9.1'

    def __init__(self, api_key=None, server='https://realityengines.ai'):
        self.api_key = api_key
        self.server = server
        # Connection and version check
        try:
            documentation = self._call_api('documentation', 'GET')
            web_version = documentation['version']
            if version.parse(web_version) > version.parse(self.client_version):
                logging.warning(
                    'A new version of the RealityEngines.AI library is available')
                logging.warning(
                    f'Current Version: {version} -> New Version: {web_version}')
            if api_key is not None:
                self.user = self._call_api('getUser', 'GET')
        except Exception:
            logging.error('Failed to connect to RealityEngines.AI server')
            raise

    def _call_api(
            self, action, method, query_params=None,
            body=None, files=None, parse_type=None):
        headers = {'apiKey': self.api_key,
                   'clientVersion': self.client_version, 'client': 'python'}
        url = self.server + '/api/v0/' + action

        response = self._request(
            url, method, query_params=query_params, headers=headers, body=body, files=files)
        result = None
        success = False
        error_message = None
        error_type = None
        try:
            json_data = response.json()
            success = json_data['success']
            error_message = json_data.get('error')
            error_type = json_data.get('errorType')
            result = json_data.get('result')
            if success and parse_type:
                result = self._build_class(parse_type, result)
        except Exception:
            error_message = response.text
        if not success:
            if response.status_code > 502 and response.status_code not in (501, 503):
                error_message = 'Internal Server Error, please contact dev@realityengines.ai for support'
            raise ApiException(error_message, response.status_code, error_type)
        return result

    def _build_class(self, return_class, values):
        if values is None:
            return None
        if isinstance(values, list):
            return [self._build_class(return_class, val) for val in values if val is not None]
        type_inputs = inspect.signature(return_class.__init__).parameters
        return return_class(self, **{key: val for key, val in values.items() if key in type_inputs})

    def _request(self, url, method, query_params=None, headers=None,
                 body=None, files=None):
        if method == 'GET':
            return requests.get(url, params=query_params, headers=headers)
        elif method == 'POST':
            return requests.post(url, params=query_params, json=body, headers=headers, files=files, timeout=90)
        elif method == 'PUT':
            return requests.put(url, params=query_params, data=body, headers=headers, files=files, timeout=90)
        elif method == 'PATCH':
            return requests.patch(url, params=query_params, data=body, headers=headers, timeout=90)
        elif method == 'DELETE':
            return requests.delete(url, params=query_params, data=body, headers=headers)
        else:
            raise ValueError(
                'HTTP method must be `GET`, `POST`, `PATCH`, `PUT` or `DELETE`'
            )

    def _poll(self, obj, wait_states, delay=5, timeout=300):
        start_time = time.time()
        while obj.get_status() in wait_states:
            if timeout and time.time() - start_time > timeout:
                raise TimeoutError(f'Maximum wait time of {timeout}s exceeded')
            time.sleep(delay)
        return obj.describe()

    def predict(self, deployment_token: str, deployment_id: str, query_data: dict = {}, **kwargs):
        '''    '''
        return self._call_api('predict', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, **kwargs})

    def create_project(self, name: str, use_case: str):
        '''Creates a project with your specified project name and use case.    '''
        return self._call_api('createProject', 'GET', query_params={'name': name, 'useCase': use_case}, parse_type=Project)

    def list_use_cases(self):
        '''Retrieves a list of all use cases    '''
        return self._call_api('listUseCases', 'GET', query_params={}, parse_type=UseCase)

    def describe_use_case_requirements(self, use_case: str):
        '''Describes a Use Case    '''
        return self._call_api('describeUseCaseRequirements', 'GET', query_params={'useCase': use_case}, parse_type=UseCaseRequirements)

    def describe_project(self, project_id: str):
        '''Retrieves a full description of the specified project.    '''
        return self._call_api('describeProject', 'GET', query_params={'projectId': project_id}, parse_type=Project)

    def list_projects(self):
        '''Retrieves a list of all projects in the organization.    '''
        return self._call_api('listProjects', 'GET', query_params={}, parse_type=Project)

    def list_project_datasets(self, project_id: str):
        '''Retrieves the datasets attached to the specified project.    '''
        return self._call_api('listProjectDatasets', 'GET', query_params={'projectId': project_id}, parse_type=ProjectDataset)

    def get_schema(self, project_id: str, dataset_id: str):
        '''Returns a schema given a specific dataset in a project. The schema of the dataset consists of the columns in the dataset, the dataType of the column, and the column's columMapping.    '''
        return self._call_api('getSchema', 'GET', query_params={'projectId': project_id, 'datasetId': dataset_id}, parse_type=Schema)

    def rename_project(self, project_id: str, name: str):
        '''Renames the project    '''
        return self._call_api('renameProject', 'PATCH', body={'projectId': project_id, 'name': name})

    def set_column_data_type(self, project_id: str, dataset_id: str, column: str, data_type: str):
        '''Set a Dataset column's dataType    '''
        return self._call_api('setColumnDataType', 'POST', body={'projectId': project_id, 'datasetId': dataset_id, 'column': column, 'dataType': data_type}, parse_type=Schema)

    def set_column_mapping(self, project_id: str, dataset_id: str, column: str, column_mapping: str):
        '''Set a column's columnMapping    '''
        return self._call_api('setColumnMapping', 'POST', body={'projectId': project_id, 'datasetId': dataset_id, 'column': column, 'columnMapping': column_mapping}, parse_type=Schema)

    def validate_project(self, project_id: str):
        '''Validates that the project has all required datasets for its Use Case, and that all datasets attached to the project have all the required columns set.    '''
        return self._call_api('validateProject', 'GET', query_params={'projectId': project_id}, parse_type=ProjectValidation)

    def remove_column_mapping(self, project_id: str, dataset_id: str, column: str):
        '''Removes a columnMapping from a column in the dataset.    '''
        return self._call_api('removeColumnMapping', 'DELETE', query_params={'projectId': project_id, 'datasetId': dataset_id, 'column': column}, parse_type=Schema)

    def delete_project(self, project_id: str):
        '''Deletes a specified project from your organization.    '''
        return self._call_api('deleteProject', 'DELETE', query_params={'projectId': project_id})

    def create_dataset(self, name: str, location: str, file_format: str = None, project_id: str = None, dataset_type: str = None):
        '''Creates a Dataset from a file located in cloud storage such as Amazon AWS S3 using the specified dataset name and dataset location.    '''
        return self._call_api('createDataset', 'POST', body={'name': name, 'location': location, 'fileFormat': file_format, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=Dataset)

    def create_dataset_version(self, dataset_id: str, location: str = None, file_format: str = None):
        '''Creates a new version of the specified Dataset    '''
        return self._call_api('createDatasetVersion', 'POST', body={'datasetId': dataset_id, 'location': location, 'fileFormat': file_format}, parse_type=DatasetVersion)

    def create_dataset_from_local_file(self, name: str, file_format: str = None, project_id: str = None, dataset_type: str = None):
        '''Creates a dataset from local file    '''
        return self._call_api('createDatasetFromLocalFile', 'POST', body={'name': name, 'fileFormat': file_format, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=DatasetUpload)

    def create_dataset_version_from_local_file(self, dataset_id: str, file_format: str = None):
        '''Creates a new version of the specified Dataset using a local file upload    '''
        return self._call_api('createDatasetVersionFromLocalFile', 'POST', body={'datasetId': dataset_id, 'fileFormat': file_format}, parse_type=DatasetUpload)

    def create_streaming_dataset(self, project_id: str):
        '''Creates a Streaming Dataset    '''
        return self._call_api('createStreamingDataset', 'POST', body={'projectId': project_id}, parse_type=Dataset)

    def get_data_connector_verification(self, bucket: str, write_permission: bool = False):
        '''Retrieves the verification information to create the data connector.    '''
        return self._call_api('getDataConnectorVerification', 'GET', query_params={'bucket': bucket, 'writePermission': write_permission}, parse_type=BucketVerificationInstructions)

    def list_data_connector_verifications(self):
        '''Retrieves a list of all connected services in the organization and their current verification status.    '''
        return self._call_api('listDataConnectorVerifications', 'GET', query_params={}, parse_type=BucketVerification)

    def add_aws_role(self, bucket: str, role_arn: str):
        '''Attaches the specified AWS Role ARN to the S3 bucket    '''
        return self._call_api('addAWSRole', 'POST', body={'bucket': bucket, 'roleArn': role_arn}, parse_type=BucketVerificationResult)

    def verify_data_connector(self, bucket: str):
        '''Checks to see if RealityEngines.AI can access the data connector    '''
        return self._call_api('verifyDataConnector', 'POST', body={'bucket': bucket}, parse_type=BucketVerificationResult)

    def remove_data_connector(self, bucket: str):
        '''Removes a connected service from the Organization    '''
        return self._call_api('removeDataConnector', 'DELETE', query_params={'bucket': bucket})

    def create_streaming_token(self):
        '''Creates a streaming token for the specified project.    '''
        return self._call_api('createStreamingToken', 'POST', body={}, parse_type=StreamingAuthToken)

    def list_streaming_tokens(self):
        '''Retrieves a list of all streaming tokens    '''
        return self._call_api('listStreamingTokens', 'GET', query_params={}, parse_type=StreamingAuthToken)

    def delete_streaming_token(self, streaming_token: str):
        '''Deletes the specified streaming token.    '''
        return self._call_api('deleteStreamingToken', 'DELETE', query_params={'streamingToken': streaming_token})

    def list_uploads(self):
        '''Lists all dataset uploads and their current status    '''
        return self._call_api('listUploads', 'GET', query_params={}, parse_type=DatasetUpload)

    def describe_upload(self, dataset_upload_id: str):
        '''Retrieves the current status and list of file parts uploaded if the upload is in progress    '''
        return self._call_api('describeUpload', 'GET', query_params={'datasetUploadId': dataset_upload_id}, parse_type=DatasetUpload)

    def upload_file_part(self, dataset_upload_id: str, part_number: int, part_data: io.TextIOBase):
        '''Upload a dataset part up to 5GB in size for a total file size of up to 5TB    '''
        return self._call_api('uploadFilePart', 'POST', query_params={'datasetUploadId': dataset_upload_id, 'partNumber': part_number}, files={'partData': part_data})

    def complete_upload(self, dataset_upload_id: str):
        '''Completes the file upload    '''
        return self._call_api('completeUpload', 'POST', body={'datasetUploadId': dataset_upload_id}, parse_type=Dataset)

    def list_datasets(self):
        '''Retrieves a list of all of the datasets in the organization.    '''
        return self._call_api('listDatasets', 'GET', query_params={}, parse_type=Dataset)

    def describe_dataset(self, dataset_id: str):
        '''Retrieves a full description of the specified dataset.    '''
        return self._call_api('describeDataset', 'GET', query_params={'datasetId': dataset_id}, parse_type=Dataset)

    def list_dataset_versions(self, dataset_id: str = None):
        '''Retrieves a list of all of the dataset version for the specified dataset    '''
        return self._call_api('listDatasetVersions', 'GET', query_params={'datasetId': dataset_id}, parse_type=DatasetVersion)

    def attach_dataset_to_project(self, dataset_id: str, project_id: str, dataset_type: str):
        '''Attaches the dataset to the project.    '''
        return self._call_api('attachDatasetToProject', 'POST', body={'datasetId': dataset_id, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=Schema)

    def remove_dataset_from_project(self, dataset_id: str, project_id: str):
        '''Removes a dataset from a project    '''
        return self._call_api('removeDatasetFromProject', 'POST', body={'datasetId': dataset_id, 'projectId': project_id})

    def delete_dataset(self, dataset_id: str):
        '''Deletes the specified dataset from the organization.    '''
        return self._call_api('deleteDataset', 'DELETE', query_params={'datasetId': dataset_id})

    def get_training_config_options(self, project_id: str):
        '''Retrieves the full description of the model training configuration options available for the specified project.    '''
        return self._call_api('getTrainingConfigOptions', 'GET', query_params={'projectId': project_id}, parse_type=TrainingConfigOptions)

    def train_model(self, project_id: str, name: None = None, training_config: dict = {}):
        '''Trains a model for the specified project.    '''
        return self._call_api('trainModel', 'POST', body={'projectId': project_id, 'name': name, 'trainingConfig': training_config}, parse_type=Model)

    def list_models(self, project_id: str):
        '''Retrieves the list of models in the specified project.    '''
        return self._call_api('listModels', 'GET', query_params={'projectId': project_id}, parse_type=Model)

    def describe_model(self, model_id: str):
        '''Retrieves a full description of the specified model.    '''
        return self._call_api('describeModel', 'GET', query_params={'modelId': model_id}, parse_type=Model)

    def get_model_metrics(self, model_id: str, model_version: str = None, baseline_metrics: bool = False):
        '''Retrieves a full list of the metrics for the specified model.    '''
        return self._call_api('getModelMetrics', 'GET', query_params={'modelId': model_id, 'modelVersion': model_version, 'baselineMetrics': baseline_metrics}, parse_type=ModelMetrics)

    def list_model_versions(self, model_id: str):
        '''Retrieves a list of all model version for a given model.    '''
        return self._call_api('listModelVersions', 'GET', query_params={'modelId': model_id}, parse_type=ModelVersion)

    def retrain_model(self, model_id: str):
        '''Retrains the specified model    '''
        return self._call_api('retrainModel', 'POST', body={'modelId': model_id}, parse_type=Model)

    def cancel_model_training(self, model_id: str):
        '''Cancels the training process for the specified model.    '''
        return self._call_api('cancelModelTraining', 'DELETE', query_params={'modelId': model_id})

    def delete_model(self, model_id: str):
        '''Deletes the specified model and all its versions    '''
        return self._call_api('deleteModel', 'DELETE', query_params={'modelId': model_id})

    def create_deployment(self, model_id: str, name: str = None, description: str = None, deployment_config: dict = None):
        '''Creates a deployment with the specified name and description for the specified model.    '''
        return self._call_api('createDeployment', 'POST', body={'modelId': model_id, 'name': name, 'description': description, 'deploymentConfig': deployment_config}, parse_type=Deployment)

    def create_deployment_token(self, project_id: str):
        '''Creates a deployment token for the specified project.    '''
        return self._call_api('createDeploymentToken', 'POST', body={'projectId': project_id}, parse_type=DeploymentAuthToken)

    def describe_deployment(self, deployment_id: str):
        '''Retrieves a full description of the specified deployment.    '''
        return self._call_api('describeDeployment', 'GET', query_params={'deploymentId': deployment_id}, parse_type=Deployment)

    def list_deployments(self, project_id: str):
        '''Retrieves a list of all deployments in the specified Project.    '''
        return self._call_api('listDeployments', 'GET', query_params={'projectId': project_id}, parse_type=Deployment)

    def list_deployment_tokens(self, project_id: str):
        '''Retrieves a list of all deployment tokens in the specified Project.    '''
        return self._call_api('listDeploymentTokens', 'GET', query_params={'projectId': project_id}, parse_type=DeploymentAuthToken)

    def update_deployment(self, deployment_id: str, name: str = None, description: str = None):
        '''Updates a deployments name and/or description.    '''
        return self._call_api('updateDeployment', 'PATCH', body={'deploymentId': deployment_id, 'name': name, 'description': description})

    def record(self, deployment_token: str, deployment_id: str, interactions: list):
        '''Record interactions    '''
        return self._call_api('record', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'interactions': interactions})

    def start_deployment(self, deployment_id: str):
        '''Restarts the specified deployment that was previously suspended.    '''
        return self._call_api('startDeployment', 'GET', query_params={'deploymentId': deployment_id})

    def stop_deployment(self, deployment_id: str):
        '''Stops the specified deployment.    '''
        return self._call_api('stopDeployment', 'GET', query_params={'deploymentId': deployment_id})

    def delete_deployment(self, deployment_id: str):
        '''Deletes the specified deployment. The deployment's models will not be affected.    '''
        return self._call_api('deleteDeployment', 'DELETE', query_params={'deploymentId': deployment_id})

    def delete_deployment_token(self, deployment_token: str):
        '''Deletes the specified deployment token.    '''
        return self._call_api('deleteDeploymentToken', 'DELETE', query_params={'deploymentToken': deployment_token})

    def predict_lead(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Returns a list of predictions (if user is a lead or not) for the specified leads scoring project deployment.    '''
        return self._call_api('predictLead', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_churn(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Returns a list of predictions for the specified customer churn project deployment.    '''
        return self._call_api('predictChurn', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_takeover(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Retrieves the predictions for the specified account takeover project deployment.    '''
        return self._call_api('predictTakeover', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_fraud(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Returns a list of predictions for the specified transaction fraud project deployment.    '''
        return self._call_api('predictFraud', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_anomalies(self, deployment_token: str, deployment_id: str, threshold: float = None, histogram: bool = False):
        '''Returns a list of anomalies from the training dataset    '''
        return self._call_api('getAnomalies', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'threshold': threshold, 'histogram': histogram})

    def is_anomaly(self, deployment_token: str, deployment_id: str, query_data: dict = None):
        '''Returns a list of anomalies    '''
        return self._call_api('isAnomaly', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_forecast(self, deployment_token: str, deployment_id: str, query_data: dict, future_data: dict = None, num_predictions: int = None, prediction_start: str = None):
        '''Returns a list of predictions for the specified forecasting project deployment.    '''
        return self._call_api('getForecast', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'futureData': future_data, 'numPredictions': num_predictions, 'predictionStart': prediction_start})

    def get_recommendations(self, deployment_token: str, deployment_id: str, query_data: dict, num_items: int = 50, page: int = 1, include_filters: list = [], exclude_filters: list = []):
        '''Returns a list of recommendations for a given userId under the specified project deployment.    '''
        return self._call_api('getRecommendations', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'numItems': num_items, 'page': page, 'includeFilters': include_filters, 'excludeFilters': exclude_filters})

    def get_personalized_ranking(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Returns a list of predictions for the specified personalized re-ranking project deployment.    '''
        return self._call_api('getPersonalizedRanking', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_ranked_items(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''Returns a list of predictions for the specified project deployment.    '''
        return self._call_api('getRankedItems', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_related_items(self, deployment_token: str, deployment_id: str, query_data: dict, num_items: int = 50, page: int = 1, include_filters: list = [], exclude_filters: list = []):
        '''Retrieves the list of related items for the specified deployment.    '''
        return self._call_api('getRelatedItems', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'numItems': num_items, 'page': page, 'includeFilters': include_filters, 'excludeFilters': exclude_filters})

    def batch_predict(self, deployment_id: str, input_location: str = None, output_location: str = None, name: str = None):
        '''Starts a batch prediction task with the specified deployment ID, input location, output location and batch prediction job name.    '''
        return self._call_api('batchPredict', 'POST', body={'deploymentId': deployment_id, 'inputLocation': input_location, 'outputLocation': output_location, 'name': name}, parse_type=BatchPrediction)

    def list_batch_predictions(self, deployment_id: str):
        '''Retrieves a list for the batch prediction jobs for the specified deployment    '''
        return self._call_api('listBatchPredictions', 'GET', query_params={'deploymentId': deployment_id}, parse_type=BatchPrediction)

    def describe_batch_prediction(self, batch_prediction_id: str):
        '''Retrieves the status of the specified batch prediction job.    '''
        return self._call_api('describeBatchPrediction', 'GET', query_params={'batchPredictionId': batch_prediction_id}, parse_type=BatchPrediction)

    def add_user_data(self, streaming_token: str, dataset_id: str, timestamp: int, user_id: str, data: dict):
        '''Record data to streaming dataset    '''
        return self._call_api('addUserData', 'POST', body={'streamingToken': streaming_token, 'datasetId': dataset_id, 'timestamp': timestamp, 'userId': user_id, 'data': data})

    def add_user_to_organization(self, email: str):
        '''Invites a user to your organization.    '''
        return self._call_api('addUserToOrganization', 'POST', body={'email': email})

    def list_api_keys(self):
        '''List all of the API keys created by the current in the user's Organization    '''
        return self._call_api('listApiKeys', 'GET', query_params={}, parse_type=ApiKey)

    def list_organization_users(self):
        '''Retrieves a list of all users in the organization.    '''
        return self._call_api('listOrganizationUsers', 'GET', query_params={})

    def get_user(self):
        '''Get the current User's info    '''
        return self._call_api('getUser', 'GET', query_params={})

    def set_user_as_admin(self, email: str):
        '''Sets the specified user as an Organization Administrator.    '''
        return self._call_api('setUserAsAdmin', 'POST', body={'email': email})

    def delete_api_key(self, api_key_id: str):
        '''Delete a specified API Key.    '''
        return self._call_api('deleteApiKey', 'DELETE', query_params={'apiKeyId': api_key_id})

    def remove_user_from_organization(self, email: str):
        '''Removes the specified user from the Organization.    '''
        return self._call_api('removeUserFromOrganization', 'DELETE', query_params={'email': email})
