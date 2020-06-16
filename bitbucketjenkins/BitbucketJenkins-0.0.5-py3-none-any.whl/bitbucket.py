#! /usr/bin/env python

import json
import requests
from .client import Client

class Bitbucket:
    def __init__(self, base_url, username, password):
        self.client = Client(base_url, username, password)
        self.client.session.headers.update({'Content-Type': 'application/json'})
        self.project = Project(self.client)
        self.branchRestriction = BranchRestriction(self.client)
        self.permission = Permission(self.client)
    
class Project:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/api/1.0/projects/"

    def get(self, project_key):
        """
        Retrieve the project matching the supplied key
        """
        return self.client.get(self.resource_path + project_key)

    def create(self, project_key, project_name, description):
        """
        Create a project in bitbucket server
        """
        data = json.dumps(dict(project_key=key, project_name=name, description=description))
        return self.client.post(self.resource_path, data)

class BranchRestriction:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/branch-permissions/2.0/projects/{}/restrictions"
        self.data = []
        self.branch_types = ["fast-forward-only", "no-deletes", "pull-request-only"]
    
    def get(self, project_key):
        """
        Retrieve branch restriction by key
        """
        return self.client.get(self.resource_path.format(project_key))
    
    def create(self, project_key, *argv):
        """
        Create branch restriction to a project
        """
        self.index = 0
        for i in range(0, len(argv)):
            for branch_type in self.branch_types:
                self.data.append({})
                self.data[self.index]['type'] = branch_type
                self.data[self.index]['matcher'] = {}
                self.data[self.index]['matcher']['id'] = argv[i]
                self.data[self.index]['matcher']['displayId'] = argv[i]
                self.data[self.index]['matcher']['type'] = {}
                self.data[self.index]['matcher']['type']['id'] = "BRANCH"
                self.data[self.index]['matcher']['type']['name'] = "Branch"
                self.data[self.index]['matcher']['active'] = True
                self.data[self.index]['users'] = []
                self.data[self.index]['groups'] = []
                self.data[self.index]['accessKeys'] = []
                self.index += 1
        data = json.dumps(self.data)
        return self.client.post(self.resource_path.format(project_key.upper()), data, headers={'Content-Type':'application/vnd.atl.bitbucket.bulk+json'})

def Permission:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/rest/api/1.0/projects/{}/permissions/{}/all?allow=true"

    def create(self, project_key, permission):
        """
        Create/grant default permission to a bitbucket project.
        Permissions are :
        - PROJECT_READ
        - PROJECT_WRITE
        - PROJECT_ADMIN
        """
        return self.client.post(self.resource_path.format(project_key, permission))



