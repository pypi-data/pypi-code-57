from kaistack.metadata import context
from kaistack.clients.openapi_clients.workflow.models import CodegenMetric, CodegenParam, CodegenArtifactMeta
from datetime import datetime

ARTIFACT_TYPE_MODEL = "MODEL"
_MODEL_NAME_PROP_NAME = "Model_Name"
_MODEL_FRAMEWORK_PROP_NAME = "Model_Framework"
_MODEL_VERSION_PROP_NAME = "Model_Version"
_MODEL_FRAMEWORKVERSION_PROP_NAME = "Model_FrameworkVersion"

def log_param(key, value):
    context.ensure_init()
    p = CodegenParam(run_id=context.get_run_id(), pipeline_run_id=context.get_pipeline_run_id(), name=key, value=value)
    context.workflowservice().log_params([p])


def log_params(params):
    context.ensure_init()
    vals = []
    for k, v in params.items():
        vals.append(CodegenParam(run_id=context.get_run_id(),
                                 pipeline_run_id=context.get_pipeline_run_id(),
                                 name=k,
                                 value=v))
    return context.workflowservice().log_params(vals)


def log_metrics(metrics):
    context.ensure_init()
    vals = []
    for k, v in metrics.items():
        vals.append(CodegenParam(run_id=context.get_run_id(),
                                 pipeline_run_id=context.get_pipeline_run_id(),
                                 name=k,
                                 value=v))
    return context.workflowservice().log_metrics(vals)


def log_metric(key, value):
    context.ensure_init()
    m = CodegenMetric(run_id=context.get_run_id(),
                      pipeline_run_id=context.get_pipeline_run_id(),
                      name=key, value=value)
    context.workflowservice().log_metrics([m])


def log_artifact_meta(artifact_path=None, artifact_type=None, properties=None):
    context.ensure_init()
    meta = CodegenArtifactMeta(run_id=context.get_run_id(), path=artifact_path, type=artifact_type,
                               properties=properties)
    context.workflowservice().log_artifact_meta(meta)


def log_model(artifact_path=None, model_name="", version=None, framework="", framework_version="", properties={}):
    '''
    Log an model. This is a simple wrapper around the log_artifact_meta
    '''
    context.ensure_init()
    if version is None:
        version = datetime.utcnow().isoformat(timespec='seconds')
    default_props = {
        _MODEL_NAME_PROP_NAME: model_name,
        _MODEL_VERSION_PROP_NAME: version,
        _MODEL_FRAMEWORK_PROP_NAME: framework,
        _MODEL_FRAMEWORKVERSION_PROP_NAME: framework_version
    }

    properties.update(default_props)
    log_artifact_meta(artifact_path=artifact_path, artifact_type=ARTIFACT_TYPE_MODEL, properties=properties)
