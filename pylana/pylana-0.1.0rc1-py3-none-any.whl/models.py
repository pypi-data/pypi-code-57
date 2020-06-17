import abc
import json

import pandas as pd
import requests


class ModelsAPI(abc.ABC):

    headers = ''
    userInfo = dict()
    url = ''

    def uploadTargetModel(self, targetModel, modelName):
        uploadModelEndpoint = "api/process-models"
        file = {'file': open(targetModel, 'rb')}
        data = {'fileName': modelName}
        model_response = requests.post(self.url + uploadModelEndpoint, files=file, data=data,
                                       headers=self.headers, verify=False).json()
        return model_response

    def connectModelToLog(self, logId, modelId):
        connectModelToLogEndpoint = "api/addLogModelMapping"
        json = {"name": str(modelId) + "_" + str(logId), "bpmnFileId": modelId, "logId": logId}
        r = requests.post(self.url + connectModelToLogEndpoint, json=json, headers=self.headers, verify=False)
        modelMappingId = r.text
        return modelMappingId

    def addEventActivityMapping(self, logId, modelId, modelMappingId):
        eventClassesEndpoint = "api/eventClasses"
        activitiesEndpoint = "api/activities"
        mappingEndpoint = "api/addActivityEventMappings"

        activities = requests.get(self.url + activitiesEndpoint + str(modelId), headers=self.headers, verify=False)
        event = requests.get(self.url + eventClassesEndpoint + str(logId), headers=self.headers, verify=False)

        act_json = json.loads(activities.text)
        evt_json = json.loads(event.text)
        joint = set(act_json).intersection(evt_json)

        mapping_id = [modelMappingId] * len(joint)

        df = pd.DataFrame([])
        df['logModelMappingId'] = mapping_id
        df.logModelMappingId = pd.to_numeric(df.logModelMappingId, errors='coerce')
        df['eventClass'] = joint
        df['activity'] = joint

        mapping_json = df.to_json(orient='records')
        mapping_json = json.loads(mapping_json)

        requests.post(self.url + mappingEndpoint, headers=self.headers, json=mapping_json, verify=False)
