from azureml.core.model import Model
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.pipeline.core.graph import PipelineParameter

import yaml
import io
import argparse
import json

def RegisterModel(model_path, description, args):
    run = Run.get_context()

    if not run:
        experiment = Run.get_context(allow_offline=False).experiment
        ws = experiment.workspace

        model = Model.register(model_path = model_path,
                       model_name = args.modelId,
                       description = description,
                       workspace = ws,
                       tags={'userId': args.userId, 
                        'productName': args.productName, 
                        'deploymentName': args.deploymentName, 
                        'apiVersion':args.apiVersion,
                        'subscriptionId':args.subscriptionId})
    
def DownloadModel(model_id, model_path):
    run = Run.get_context()
    if not run:
        experiment = Run.get_context(allow_offline=False).experiment
        ws = experiment.workspace
        model = Model(ws, model_id)
        model.download(target_dir = model_path, exist_ok=True)

def GetModelPath():
    # get model path if the model is deployed using AML
    if os.getenv('AZUREML_MODEL_DIR'):
        return os.getenv('AZUREML_MODEL_DIR')

def ParseArguments(run_type):
    parser = argparse.ArgumentParser(run_type)

    parser.add_argument("--userInput", type=str, help="input data")
    parser.add_argument("--modelId", type=str, help="model key")

    if run_type == 'inference':
        parser.add_argument("--operationId", type=str, help="run id")
    else:
        parser.add_argument("--userId", type=str, help="user id")
        parser.add_argument("--productName", type=str, help="product name")
        parser.add_argument("--deploymentName", type=str, help="deployment name")
        parser.add_argument("--apiVersion", type=str, help="api version")
        parser.add_argument("--subscriptionId", type=str, help="subscription id")

        if run_type == 'deployment':
            parser.add_argument("--endpointId", type=str, help="endpoint id")

    args = parser.parse_args()
    userInput = json.loads(args.userInput)

    return args, userInput

def GetPipelineArguments(mlproject_file_path, run_type):
	with open(mlproject_file_path) as file:
		documents = yaml.full_load(file)
		
		arguments = []
	
		for param in documents['entry_points'][run_type]['parameters']:
			
			pipelineParam = PipelineParameter(
				name=param,
				default_value=documents['entry_points'][run_type]['parameters'][param]['default'])
			
			argumentName = '--' + param
			arguments.append(argumentName)
			arguments.append(pipelineParam)
	
	return arguments