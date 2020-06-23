import json

import yaml
from kfp.components._components import load_component_from_text

from kaistack.auth import token
from kaistack.clients.openapi_clients.pipelinecomponents.api.pipeline_component_service_api import \
    PipelineComponentServiceApi
from kaistack.clients.openapi_clients.pipelinecomponents.api_client import ApiClient
from kaistack.clients.openapi_clients.pipelinecomponents.configuration import Configuration
from kaistack.clients.openapi_clients.pipelinecomponents.models.codegen_pipeline_component import \
    CodegenPipelineComponent
from kaistack.components.exceptions import MissingTemplateException

KFP_COMPONENT_SPEC_ANNOTATION = "pipelines.kubeflow.org/component_spec"


def create_from_template(spec: str):
    c = CodegenPipelineComponent()
    wf = yaml.safe_load(spec)
    if 'spec' in wf and 'templates' in wf['spec']:
        templates = wf['spec']['templates']
        if len(templates) > 0:
            template = templates[0]
            if 'container' in template:
                c.image = template['container']['image']
            elif 'script' in template:
                c.image = template['script']['image']
            if 'metadata' in template and \
                    'annotations' in template['metadata'] and \
                    KFP_COMPONENT_SPEC_ANNOTATION in template['metadata']['annotations']:
                annotation_val = template['metadata']['annotations'][KFP_COMPONENT_SPEC_ANNOTATION]
                kfp_pipeline_spec = json.loads(annotation_val)
                c.name = kfp_pipeline_spec['name']
                c.description = kfp_pipeline_spec.get('description')
            else:
                c.name = template.get('name')
        else:
            raise MissingTemplateException
    return c


class ComponentStore:
    def __init__(self, service=None, api_base=None):
        if service is None and api_base is None:
            # In cluster
            self.configuration = Configuration("http://kaistackapiserver:8888")
            self.ApiClient = ApiClient(self.configuration, header_name="x-user", header_value="anonymous")
            self.componentApi = PipelineComponentServiceApi(self.ApiClient)
        elif service.startswith("http://localhost"):
            self.configuration = Configuration(api_base)
            self.ApiClient = ApiClient(self.configuration)
            self.componentApi = PipelineComponentServiceApi(self.ApiClient)
        else:
            self.access_token = token.get_access_token()
            self.configuration = Configuration(api_base, api_key=self.access_token['access_token'],
                                               api_key_prefix="Bearer")
            self.ApiClient = ApiClient(self.configuration, header_name="Authorization",
                                       header_value="Bearer {0}".format(self.access_token['access_token']))
            self.componentApi = PipelineComponentServiceApi(self.ApiClient)

    def list_components(self):
        return self.componentApi.list_components().components

    def create_component(self, spec: str, name: str = None, help_link=None, source_url=None):
        c = create_from_template(spec)
        if name is not None:
            c.name = name
        c.spec = spec
        c.help_link = help_link
        c.source_url = source_url
        return self.componentApi.create_component(c)

    def update_component(self, spec: str, name: str = None, help_link=None, source_url=None):
        c = create_from_template(spec)
        if name is not None:
            c.name = name
        c.spec = spec
        c.help_link = help_link
        c.source_url = source_url
        return self.componentApi.update_component(c)

    def get_component(self, id: str):
        ret = self.componentApi.get_component(id)
        if ret is not None:
            return ret.component
        return None

    def get_component_by_name(self, name: str):
        ret = self.componentApi.get_component_by_name(name)
        if ret is not None:
            return ret.component
        return None

    def get_component_by_name_and_version(self, name: str, version: str):
        ret = self.componentApi.get_component_by_name(name, version=version)
        if ret is not None:
            return ret.component
        return None

    def component_op(self, name: str, version: str = None):
        if version is None:
            c = self.get_component_by_name(name)
        else:
            c = self.get_component_by_name_and_version(name, version)
        return load_component_from_text(c.spec)

    def close(self):
        self.ApiClient.close()
