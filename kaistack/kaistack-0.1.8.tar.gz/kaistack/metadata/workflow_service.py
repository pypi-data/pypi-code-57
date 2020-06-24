from json import JSONEncoder

from kaistack.auth import token
from kaistack.clients.openapi_clients.workflow.configuration import Configuration
from kaistack.clients.openapi_clients.workflow.api_client import ApiClient
from kaistack.clients.openapi_clients.workflow.models import CodegenRun
from kaistack.clients.openapi_clients.workflow.api.workflow_service_api import WorkflowServiceApi


class CodegenMetricEncoder(JSONEncoder):
    def default(self, o):
        return {'runId': o.run_id,
                'pipelineRunId': o.pipeline_run_id,
                'name': o.name,
                'value': o.value}


class CodegenParamEncoder(JSONEncoder):
    def default(self, o):
        return {'runId': o.run_id,
                'pipelineRunId': o.pipeline_run_id,
                'name': o.name,
                'value': o.value}


class CodegenArtifactMetaEncoder(JSONEncoder):
    def default(self, o):
        return {'runId': o.run_id,
                'name': o.name,
                'type': o.type,
                'properties': o.properties}


_codeMetricEncoder = CodegenMetricEncoder()
_codeParamEncoder = CodegenParamEncoder()


class WorkflowService:
    def __init__(self, api_base=None):
        if api_base is None:
            # In cluster
            self.configuration = Configuration("http://kaistackapiserver:8888")
            self.ApiClient = ApiClient(self.configuration, header_name="x-user", header_value="anonymous")
            self.workflowApi = WorkflowServiceApi(self.ApiClient)
        elif api_base.startswith("http://localhost"):
            self.configuration = Configuration(api_base)
            self.ApiClient = ApiClient(self.configuration)
            self.workflowApi = WorkflowServiceApi(self.ApiClient)
        else:
            self.access_token = token.get_access_token()
            self.configuration = Configuration(api_base, api_key=self.access_token['access_token'],
                                               api_key_prefix="Bearer")
            self.ApiClient = ApiClient(self.configuration, header_name="Authorization",
                                       header_value="Bearer {0}".format(self.access_token['access_token']))
            self.workflowApi = WorkflowServiceApi(self.ApiClient)

    def get_run_by_name(self, name):
        response = self.workflowApi.get_run_by_name(name)
        return response.run

    def create_run(self, name):
        run = CodegenRun()
        run.name = name
        response = self.workflowApi.create_run(run)
        return response.run

    def log_metrics(self, metrics):
        response = self.workflowApi.log_metrics(_codeMetricEncoder.encode(metrics))
        return response.num_of_writes

    def log_params(self, params):
        response = self.workflowApi.log_params(_codeParamEncoder.encode(params))
        return response.num_of_writes

    def log_artifact_meta(self, meta):
        response = self.workflowApi.log_artifact_meta(meta)
        return response.artifact
