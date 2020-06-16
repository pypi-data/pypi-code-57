import os
from kaistack.metadata.workflow_service import WorkflowService
from kaistack.metadata import context
from kaistack.metadata.tracking import *

def quick_tests():
    svc = WorkflowService("http://localhost:8888")
    r = svc.create_run("run-6pb2r.preprocess")
    os.environ[context._WORKFLOW_NAME_ENV] = "run-6pb2r"
    os.environ[context._POD_NAME_ENV] = "testlocal-123"
    os.environ[context._PIPELINE_RUN_ID_ENV] = '047e568d-2948-4153-8aa0-e7cc2482c150'
    os.environ[context._PIPELINE_TEMPLATE_NAME_ENV] = "preprocess"
    os.environ["KAISTACKSEVER_URL"] = "http://localhost:8888"
    log_metric("m1",3.0)
    log_metrics({"m2":2.0,"m1":1.0})
    log_param("p1","val1")
    log_params({"p2":"val2", "p3":"val3"})
    log_artifact_meta(artifact_name='preprocess-output_path', artifact_type='DATASET', properties={'b':'1'})
    #svc.log_artifact_meta(meta)
if __name__=="__main__":
    quick_tests()