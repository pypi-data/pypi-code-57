import os
import logging
from kaistack.metadata.workflow_service import WorkflowService

_INITIALIZED_ = False

_POD_NAME = ''
_POD_NAME_ENV = 'KFP_POD_NAME'
_PIPELINE_RUN_ID = ''
_PIPELINE_RUN_ID_ENV = 'PIPELINE_RUN_ID'
_WORKFLOW_NAME = ''
_WORKFLOW_NAME_ENV = 'ARGO_WORKFLOW_NAME'
_PIPELINE_TEMPLATE_NAME = ''
_PIPELINE_TEMPLATE_NAME_ENV = 'PIPELINE_TEMPLATE_NAME'
_WorkFlow_Service = None
_CURRENT_RUN = None


def check_and_get_env(name):
    if name not in os.environ:
        logging.error("Cannot find environment variable {}", name)
        return ''
    else:
        return os.environ[name]


def init():
    global _INITIALIZED_
    global _PIPELINE_RUN_ID
    global _POD_NAME
    global _WORKFLOW_NAME
    global _PIPELINE_TEMPLATE_NAME
    global _WorkFlow_Service
    global _CURRENT_RUN

    # Initialize from the environment
    _PIPELINE_RUN_ID = check_and_get_env(_PIPELINE_RUN_ID_ENV)
    _POD_NAME = check_and_get_env(_POD_NAME_ENV)
    _WORKFLOW_NAME = check_and_get_env(_WORKFLOW_NAME_ENV)
    _PIPELINE_TEMPLATE_NAME = check_and_get_env(_PIPELINE_TEMPLATE_NAME_ENV)
    if "KAISTACKSEVER_URL" in os.environ:
        _WorkFlow_Service = WorkflowService(os.environ["KAISTACKSEVER_URL"])
    else:
        _WorkFlow_Service = WorkflowService()

    _CURRENT_RUN = _WorkFlow_Service.get_run_by_name("{}.{}".format(_WORKFLOW_NAME, _PIPELINE_TEMPLATE_NAME))
    _INITIALIZED_ = True


def ensure_init():
    global _INITIALIZED_
    if _INITIALIZED_:
        return
    init()


def get_run_id():
    global _CURRENT_RUN
    return _CURRENT_RUN.run_id


def get_pipeline_run_id():
    global _PIPELINE_RUN_ID
    return _PIPELINE_RUN_ID


def workflowservice():
    global _WorkFlow_Service
    return _WorkFlow_Service
