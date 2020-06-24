import json
import logging
import os
import nbformat
from nbconvert import HTMLExporter

import papermill as pm

PREFIX = "KAISTACK_NOTEBOOK_PARAM"
CLOUDPROVIDER = "KAISTACK_CLOUD_PROVIDER"
OUTPUTSTORAGEURI = "KAISTACK_OUTPUT_STORAGE_URI"
NOTEBOOKJOBNAME = "KAISTACK_NOTEBOOK_JOB_NAME"
PODNAME = "POD_NAME"
logger = logging.getLogger("Notebook Runner")
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def get_value(v: str):
    '''
    The value is passed via environment variables. Support str, boolean and number now
    The rules is string will have double quotes around string. Otherwise will try to parse as boolean
    or number
    '''
    logger.info(v)
    try:
        result = json.loads(v.lower())
    except json.decoder.JSONDecodeError:
        return v
    if type(result) is str:
        return v  # result is in lower case
    else:
        return result


def generate_parameters() -> dict:
    ret = {}
    for k, v in os.environ.items():
        if k.startswith(PREFIX) and len(k) > len(PREFIX) + 1:
            ret[k[len(PREFIX) + 1:]] = get_value(v)
    return ret


def convert_to_html(input_file):
    '''Invoke nbconvert to export html'''
    nb = nbformat.read(input_file, 4)
    html_exporter = HTMLExporter()
    logger.info("Exporting output as html")
    (output, resources) = html_exporter.from_notebook_node(nb)
    with open(input_file + ".html", "w") as f:
        f.write(output)


def main():
    parameters = generate_parameters()
    logger.info("Parameters is {0}".format(parameters))
    INPUT = os.environ["KAISTACK_INPUT_NOTEBOOK"]
    logger.info("INPUT is {0}".format(parameters))
    OUTPUT = os.environ["KAISTACK_OUTPUT_NOTEBOOK"]
    logger.info("OUTPUT is {0}".format(parameters))
    cloudProvider = os.environ[CLOUDPROVIDER]
    outputuri = os.environ[OUTPUTSTORAGEURI]
    jobName = os.environ[NOTEBOOKJOBNAME]
    podName = os.environ[PODNAME]
    logger.info("Cloudprovider is {0}. Output is {1}. JobName is {2}. Run Name is {3}".format(cloudProvider,
                                                                                              outputuri, jobName,
                                                                                              podName))

    pm.execute_notebook(INPUT, OUTPUT, parameters, log_output=True)
    convert_to_html(OUTPUT)
