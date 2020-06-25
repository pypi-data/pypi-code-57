import requests
import json
import datetime

class ZephyrTestUpdate:
    def __init__(self, jira_server, username, password, projectKey, version_name, cyclename, foldername=None):
        self.jira_server = jira_server
        self.username = username
        self.password = password
        self.projectKey = projectKey
        self.cyclename = cyclename
        self.foldername = foldername
        self.version_name = version_name
        self.executionCountUri = '/rest/zapi/latest/zql/executeSearch'
        self.bulkUpdateUri = '/rest/zapi/latest/execution/updateBulkStatus'
        self.singleUpdateUri = 'https://jira.dev.labs.att.com/rest/zapi/latest/execution/id/execute'
        self.auth = (self.username, self.password)
        self.projectId = self.get_project_id_from_project_key()
        self.versionId = self.get_version_id()
        time=str(datetime.datetime.now())
        self.fileNamesiffix = (time.replace('-', '_').replace(' ', '_').replace(':', '_').replace('.', '_'))
        #self.cycleId = self.get_cycle_information()
        #import pdb; pdb.set_trace()
        #if foldername:
        #    self.folderId = self.get_folder_id_by_folder_name_from_cycle()
        if foldername:
            self.zqlQuery = 'project="' + self.projectKey + '" AND cycleName="' + self.cyclename + '" AND folderName="' + self.foldername +'" AND  fixVersion="' + self.version_name + '"'
        else:
            self.zqlQuery = 'project="' + self.projectKey + '" AND cycleName="' + self.cyclename + '" AND  fixVersion="' + self.version_name + '"'


    def _generate_issue_ids(self):
        issues = {}
        #zqlQuery = 'project="' + self.projectid + '" AND cycleName="' + self.cyclename + '" AND folderName="' + self.foldername +'"'
        url = self.jira_server + self.executionCountUri + '?zqlQuery=' + self.zqlQuery + '&maxRecords=9999'
        resp = requests.get(url, auth=self.auth)
        #import pdb; pdb.set_trace()
        resp_json = json.loads(resp.text)
        for testcase in resp_json['executions']:
            issues[testcase['issueKey']] = testcase['id']
        return (issues)


    def _get_status_number(self, status):
        if status.upper() == 'PASS':
            number = 1
        elif  status.upper() == 'FAIL':
            number =2
        elif  status.upper() == 'WIP':
            number =3
        elif  status.upper() == 'BLOCKED':
            number =4
        elif  status.upper() == 'DEFERRED':
            number =5
        elif  status.upper() == 'OUT OF SCOPE':
            number =6
        elif  status.upper() == 'UNEXECUTED':
            number =7
        else:
            number = 7
        return str(number)

    def logAttach(self, executionId, logFilePath):
        url = self.jira_server + '/rest/zapi/latest/attachment'
        filename = logFilePath.split('/')[-1]
        files = {
            'file': (filename, open(logFilePath, 'rb'), "multipart/form-data"),
        }
        headers = {
            'X-Atlassian-Token': 'nocheck',
            'Accept': 'application/json'
        }
        params = (
            ('entityId', executionId),
            ('entityType', 'execution'),
        )
        response = requests.post(url, headers=headers, params=params, files=files, auth=self.auth)
        return (response.status_code, response.content)

    def updateExecution(self, issueKey, status, logFilePath=None):
        issues=self._generate_issue_ids()
        id = issues[issueKey]
        status_number = self._get_status_number(status)
        singleUpdateUri = self.singleUpdateUri.replace('id', str(id))
        data = '{"status": "' +status_number +'"}'
        headers = {'content-type': 'application/json'}
        try:
           resp = requests.put(singleUpdateUri, headers=headers, data=data, auth=self.auth)
           if resp.status_code != 200:
               raise Exception (resp.content)
           else:
               if logFilePath:
                   resp_upload, body_upload = self.logAttach(id, logFilePath)
                   if resp_upload != 200:
                       raise Exception ('Unable upload content :' + body_upload)
        except Exception as exp:
            raise Exception (str(exp))

    def bulkUpdateExecution(self, status, *issueKeys):
        issues = self._generate_issue_ids()
        issueListString = ''
        for issueKey in issueKeys:
            issueListString = issueListString + '"' + str(issues[issueKey])+ '",'
        status_number = self._get_status_number(status)
        bulk_data = '{"executions":[' + issueListString[:-1] +'], "status": "' + str(status_number) + '"}'
        url = self.jira_server + self.bulkUpdateUri +'?zqlQuery=' + self.zqlQuery
        headers = {'content-type': 'application/json'}
        try:
           resp = requests.put(url, headers=headers, data=bulk_data, auth=self.auth)
           if resp.status_code != 200:
               raise Exception (resp.content)
        except Exception as exp:
            raise Exception (str(exp))

    def get_testcases(self, label):
        testcaseKeys = []
        jira_server = self.jira_server
        project = self.projectKey
        url = jira_server + '/rest/api/2/search?jql=project%20%3D%20' + project + '%20AND%20issuetype%20%3D%20Test%20AND%20labels%20%3D%20' + label
        resp2 = requests.get(url + '&maxResults=-1', auth=self.auth)
        keys = json.loads(resp2.text)['issues']
        for key in keys:
            testcaseKeys.append(key['key'])
        return (testcaseKeys)


    def get_project_id_from_project_key(self):
        jira_server = self.jira_server
        url = jira_server + '/rest/api/2/project/' + self.projectKey
        project = requests.get(url, headers={'accept': 'application/json'}, auth=self.auth)
        return project.json()['id']

    def get_version_id(self, version_name=None):
        jira_server = self.jira_server
        projectId = self.projectId
        #projectId = self.get_project_id_from_project_key()
        url = jira_server + '/rest/zapi/latest/util/versionBoard-list?projectId=' + projectId
        headers = {'accept': 'application/json'}
        project = requests.get(url, headers=headers, auth=self.auth)
        if version_name:
            vname = version_name
        else:
            vname = self.version_name
        for version in project.json()['unreleasedVersions']:
            if version['label'] == vname:
                    return version['value']


    def createTestCycle(self, cycleName, startdate, endDate, description=None):
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/cycle'
        versionId = self.versionId
        projectId = self.projectId
        #versionId = self.get_version_id()
        #projectId = self.get_project_id_from_project_key()

        headers = {'content-type': 'application/json'}
        newCycleValues = json.dumps({
            "clonedCycleId": "",
            "name": cycleName,
            "build": "",
            "environment": "",
            "description": description,
            "startDate": startdate,
            "endDate": endDate,
            "projectId": projectId,
            "versionId": versionId
        })
        resp = requests.post(url, data=newCycleValues, headers=headers, auth=self.auth)
        return resp.json()['id']

    def get_cycle_information(self, cyclename=None):
        projectId = self.projectId
        versionId = self.versionId
        #projectId = self.get_project_id_from_project_key()
        #print(projectId)
        #versionId=self.get_version_id()
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/cycle?projectId=' + projectId + '&versionId=' + versionId
        resp = requests.get(url, auth=self.auth)
        if cyclename:
            cname = cyclename
        else:
            cname = self.cyclename
        #import pdb; pdb.set_trace()
        for key, value in resp.json().items():
            #import pdb; pdb.set_trace()
            try:
                if cname.strip() == value['name'].strip():
                    return (key)
            except Exception as exp:
                raise Exception('Cycle name not foubd {}' + str(exp))

    def get_folder_id_by_folder_name_from_cycle(self, cyclename=None, foldername=None):
        if cyclename:
            cycle_id = self.get_cycle_information(cyclename)
        else:
            cycle_id = self.get_cycle_information(self.cyclename)
        projectId = self.projectId
        versionId = self.versionId
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/cycle/' + cycle_id + '/folders?projectId=' + projectId + '&versionId=' + versionId
        resp = requests.get(url, auth=self.auth)
        #import pdb; pdb.set_trace()
        if foldername:
            fname = foldername
        else:
            fname = self.foldername
        for folder in resp.json():
            if folder['folderName'] == fname:
                return (folder['folderId'])

    def AddTestCasesToCycle(self,testcaseLabel, cyclename=None, folderName=None):
        if cyclename:
            cycle_id = self.get_cycle_information(cyclename)
            cyclename = cyclename
        else:
            cycle_id = self.get_cycle_information(self.cyclename)
            cyclename = self.cyclename
        #print ("Cycle ID : " + str(cycle_id))
        projectId = self.projectId
        folderId = ''
        if folderName:
            folderId = self.get_folder_id_by_folder_name_from_cycle(cyclename, folderName)
        versionId=self.versionId
        testsToAdd = self.get_testcases(testcaseLabel)
        #import pdb;pdb.set_trace()
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/execution/addTestsToCycle/'
        addTestValues = json.dumps({
            "issues": testsToAdd,
            "versionId": versionId,
            "cycleId": cycle_id,
            "projectId": projectId,
            "method": "1",
            "folderId": folderId
        })
        headers = {'content-type': 'application/json'}
        #import pdb;pdb.set_trace()
        resp = requests.post(url, data=addTestValues, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            print ('Tests Added Succesfully')
        else:
            raise Exception ("Tests could not be added..{}".format(resp.content))



    def bulkUpdateCompleteFolder(self, status):
        issues = self._generate_issue_ids()
        #print (issues)
        issueListString = ''
        for issueKey, issueId in issues.items():
            issueListString = issueListString + '"' + str(issueId)+ '",'
        status_number = self._get_status_number(status)
        bulk_data = '{"executions":[' + issueListString[:-1] +'], "status": "' + str(status_number) + '"}'
        url = self.jira_server + self.bulkUpdateUri
        headers = {'content-type': 'application/json'}
        #import pdb;pdb.set_trace()
        try:
           resp = requests.put(url, headers=headers, data=bulk_data, auth=self.auth)
           if resp.status_code != 200:
               raise Exception (resp.content)
        except Exception as exp:
            raise Exception (str(exp))

    def Create_Folder_under_cycle(self, cyclename, folderName):
        if cyclename.lower() != self.cyclename.lower():
            cycle_id = self.get_cycle_information(cyclename)
        else:
            cycle_id = self.get_cycle_information(self.cyclename)
        projectId = self.projectId
        versionId=self.versionId
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/folder/create'
        addTestValues = json.dumps({
            "versionId": versionId,
            "cycleId": cycle_id,
            "projectId": projectId,
            "name": folderName,
            "description": "created test folder for this cycle",
            "clonedFolderId": 1
        })
        headers = {'content-type': 'application/json'}
        resp = requests.post(url, data=addTestValues, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            return (self.get_folder_id_by_folder_name_from_cycle(cyclename, folderName))
        else:
            raise Exception ('Unable to create Folder {}'.format(resp.content))

    def get_color(self, status):
        if status.lower() == 'pass':
            color = 'green'
        elif status.lower() == 'fail':
             color = 'red'
        elif status.lower() == 'wip':
            color = 'orange'
        elif status.lower() == 'blocked':
            color = 'lightskyblue'
        elif status.lower() == 'deferred':
            color = 'mediumpurple'
        elif status.lower() == 'out of scope':
            color = 'gold'
        else:
            color = 'darkgray'
        return color

    def GetExecutionStatus(self):
        projectId = self.projectId
        cycle_id = self.get_cycle_information(self.cyclename)
        versionId = self.versionId
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        jira_server = self.jira_server
        url = jira_server + '/rest/zapi/latest/execution/executionsStatusCountByCycle?projectId=' + str(
            projectId) + '&versionId=' + str(versionId) + '&cycles=' + str(cycle_id)
        if self.foldername:
            folder_id = self.get_folder_id_by_folder_name_from_cycle(self.cyclename, self.foldername)
            url = url + '&folders=' + str(folder_id)
        resp = requests.get(url, headers=headers, auth=self.auth)
        execution_status = {}
        for status in resp.json():
            execution_status[status['statusName']] = status['statusCount']
        #print(execution_status)
        return (execution_status)