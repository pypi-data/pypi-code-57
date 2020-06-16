'''
@Author: YunsangJeong
@Company: Digger
@Digo - Python Logger Module
'''
import requests
import json
import sys
import random
import string
import atexit
import base64

from collections import OrderedDict

from Digo import Project
from Digo import Error
from Digo import Network
from Digo import Utils


class Core():
    __instance = None
    DIGO_WEB = 'http://digo.ai:7777/digo-server'

    @classmethod
    def instance(cls):
        return cls.__instance

    # def __init__(self, api, project_name):
    #     super().__init__()
    #     self.__user = Project.User(api_key=api)
    #     self.__experiment = Project.Experiment()
    #     self.__project = Project.Project(project_name=project_name)
    #     self.__log: OrderedDict = OrderedDict()
    #     self.__project.name = project_name
    #     self.__step: int = 0
    #     __instance = self
    #     self.login()

    def __init__(self, api, workspace_name, project_name):
        super().__init__()
        self.__user = Project.User(api_key=api)
        self.__experiment = Project.Experiment()
        self.__project = Project.Project(
            project_name=project_name, workspace=workspace_name)
        self.__log: OrderedDict = OrderedDict()
        self.__step: int = 0
        self.login()

    def send_log(self, log):
        keys = [key for key in log]
        for key in keys:
            if key not in self.__log:
                value = log[key]
                if type(value) is float:
                    value = round(value, 3)
                self.__log[key] = [value]
            else:
                value = log[key]
                if type(value) is float:
                    value = round(value, 3)
                self.__log[key].append(value)

        self.__log['step'] = self.__step
        self.__step += 1
        log_json = json.dumps(self.__log)

        Network.updateLog(api_key=self.__user.api_key, account_id=self.__user.id,
                          experiment_id=self.__experiment.id,  log=log_json)

    def printLog(self, log):
        Network.updatePrintLog(api_key=self.__user.api_key, account_id=self.__user.id,
                               experiment_id=self.__experiment.id, log=log)

    def send_hyper_parameter(self, hyper_parameter):
        Network.updateHyperParameter(api_key=self.__user.api_key, account_id=self.__user.id,
                                     experiment_id=self.__experiment.id, hyper_parameter=hyper_parameter)

    def login(self):
        json_data = Network.login(
            api_key=self.__user.api_key, workspace_name=self.__project.workspace)

        if 'code' not in json_data:
            raise Error.APIInvalidError
            return

        if json_data['code'] == 0:
            self.__user.id = json_data['account_id']
            self.__user.azure_id = base64.b64decode(
                bytes(json_data['cloud_account_name'])).decode('utf-8')
            self.__user.azure_key = base64.b64decode(
                bytes(json_data['cloud_account_key'])).decode('utf-8')
            self.__user.setContainer(json_data['cloud_container_name'])

            self.create_experiment()
            self.uploadSourceCode()
            self.uploadRequirement()

            print('Login Complete, Welcome {0}'.format(self.__user.id))
        else:
            print(json_data)
            raise Error.APIInvalidError

    def create_experiment(self):
        experiment_name: str = ""
        for i in range(0, 12):
            experiment_name += random.choice(string.ascii_letters)

        conn: requests.Response = None

        if self.__project.workspace is None:
            conn = requests.get(self.DIGO_WEB + "/CreateExperiment", params={
                                'apt_key': self.__user.api_key, 'account_id': self.__user.id, 'project_name': self.__project.name, 'experiment_name': experiment_name})
        else:
            params = {'api_key': self.__user.api_key, 'account_id': self.__user.id, 'project_name': self.__project.name,
                      'experiment_name': experiment_name, 'workspace_name': self.__project.workspace}
            conn = requests.get(
                self.DIGO_WEB + "/CreateExperiment", params=params)

        json_data = conn.json()

        if json_data['code'] == 0:
            self.__experiment.id = json_data['experiment_id']
            self.__experiment.name = experiment_name
            print("Created Experiment : {0}".format(experiment_name))
        else:
            raise Error.FailExperiment

    def uploadSourceCode(self):
        Network.uploadSourceCode(experiment_name=self.__experiment.name,
                                 experiment_id=self.__experiment.id,
                                 azure_id=self.__user.azure_id,
                                 azure_key=self.__user.azure_key,
                                 container_name=self.__user.container,
                                 project_name=self.__project.name, api_key=self.__user.api_key, account_id=self.__user.id)

    def uploadRequirement(self):
        Network.uploadRequirementsFile(api_key=self.__user.api_key, account_id=self.__user.id,
                                       experiment_id=self.__experiment.id, requirements=Utils.getRequirements())

    def imageLog(self, log):
        Network.uploadImageLog(api_key=self.__user.api_key, account_id=self.__user.id, azure_id=self.__user.azure_id,
                               azure_key=self.__user.azure_key,
                               experiment_id=self.__experiment.id, container_name=self.__user.container, project_name=self.__project.name, experiment_name=self.__experiment.name, imageLog=log)

    def uploadModel(self, model_path):
        Network.uploadModelFile(experiment_name=self.__experiment.name,
                                 experiment_id=self.__experiment.id,
                                 azure_id=self.__user.azure_id,
                                 azure_key=self.__user.azure_key,
                                 container_name=self.__user.container,
                                 project_name=self.__project.name, api_key=self.__user.api_key, account_id=self.__user.id
                                 ,model_path=model_path)
