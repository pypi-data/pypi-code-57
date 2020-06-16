import requests
from Digo import SystemMetrics
import sys
import os
import json
import random
import numpy as np
from PIL import Image
import string
from Digo.AzureCloud import AzureCloudService
from collections import OrderedDict

DIGO_WEB = 'http://digo.ai:7777/digo-server'
# DIGO_WEB = 'http://localhost:8080'

azure_cloud_service = AzureCloudService()
imageLogStep = 0
modelFileStep = 0


def login(api_key, workspace_name):
    conn = requests.get(DIGO_WEB + "/SignInUseAPI",
                        params={'api_key': api_key, 'workspace_name': workspace_name})

    return conn.json()


def updateLog(api_key, account_id, experiment_id, log):
    conn = requests.post(DIGO_WEB + "/UpdateLog", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'log': log, 'system_metrics': SystemMetrics.getSystemMetrics()})


def updatePrintLog(api_key, account_id, experiment_id, log):
    conn = requests.post(DIGO_WEB + "/UpdatePrintLog", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'print_log': log})


def updateHyperParameter(api_key, account_id, experiment_id, hyper_parameter):
    conn = requests.post(DIGO_WEB + "/UpdateHyperParameter", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'hyper_parameter': hyper_parameter})


def uploadModelFile(api_key, account_id, experiment_name, azure_id, azure_key, container_name, project_name, experiment_id, model_path):
    global modelFileStep
    current_dir = os.getcwd()
    origin_file_name = model_path.split('/')[-1]
    file_name = str(modelFileStep) + "_" + origin_file_name
    os.rename

    if model_path.startswith('/'):
        full_path = current_dir + model_path
    else:
        full_path = current_dir + os.sep + model_path

    convert_full_path = full_path.split(origin_file_name)[0] + file_name

    os.rename(full_path, convert_full_path)

    print(convert_full_path)

    blob_id = azure_cloud_service.upload_model_file(convert_full_path,
                                           file_name,
                                           azure_id,
                                           azure_key,
                                           container_name,
                                           project_name,
                                           experiment_name,
                                           experiment_id)

    model_blob = OrderedDict()
    model_blob[file_name] = blob_id
    os.rename(convert_full_path, full_path)
    conn = requests.post(DIGO_WEB + "/ModelFileAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'model_blob': json.dumps(model_blob)})
    modelFileStep +=1
def uploadSourceCode(api_key, account_id, experiment_name, azure_id, azure_key, container_name, project_name, experiment_id):

    local_file_name = sys.argv[0]
    directory, file_name = os.path.split(local_file_name)
    current_dir = os.getcwd()
    full_path = current_dir + os.sep + local_file_name
    print(full_path)

    blob_id = azure_cloud_service.upload_source_file(full_path,
                                           file_name,
                                           azure_id,
                                           azure_key,
                                           container_name,
                                           project_name,
                                           experiment_name,
                                           experiment_id)

    conn = requests.post(DIGO_WEB + "/SourceCodeAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'azure_blob_id': blob_id})


def uploadRequirementsFile(api_key, account_id, experiment_id, requirements):
    conn = requests.post(DIGO_WEB + "/UploadRequirements", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'requirements': requirements})


def uploadImageLog(api_key, account_id,azure_id,
                                           azure_key, experiment_id, container_name, project_name, experiment_name, imageLog):
    global imageLogStep

    local_file_name = sys.argv[0]
    directory, file_name = os.path.split(local_file_name)
    current_dir = os.getcwd()
    full_path = current_dir + os.sep + local_file_name
    print(full_path)

    result_image_log = OrderedDict()

    if os.path.isdir(current_dir+ os.sep + 'temp') is False :
        os.mkdir(current_dir+ os.sep + 'temp')


    for key in imageLog:
        if type(imageLog[key]) is np.ndarray:
            image_data = Image.fromarray(imageLog[key])
        else:
            image_data = imageLog[key]
        image_name: str = key + "_" + str(imageLogStep)
        image_data.save(current_dir+ os.sep + 'temp' + os.sep + image_name + '.png', 'PNG')
        full_path = current_dir + os.sep + 'temp' + os.sep + image_name+'.png'
        result_image_log[key] = azure_cloud_service.upload_image(full_path, image_name+'.png', azure_id,
                                         azure_key, container_name, project_name, experiment_name, experiment_id)
                                         
        os.remove(current_dir+ os.sep + 'temp' + os.sep + image_name + '.png')

    conn = requests.post(DIGO_WEB + "/ImageAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id, 'image_blob_id': json.dumps(result_image_log)})

    imageLogStep += 1
