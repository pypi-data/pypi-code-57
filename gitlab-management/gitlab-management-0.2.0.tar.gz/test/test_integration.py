#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, "../gitlab_management")
sys.path.insert(0, "./gitlab_management")
sys.path.insert(0, "./")

from base import GitlabManagement

import unittest, xmlrunner
from unittest.mock import patch
import enum
import gitlab

import requests_mock

import gitlab_management
import yaml

class GitlabManagement_Unit(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        
        cls.ConfigFileContents = """Group:
    Labels:
        -
            Group: "ExampleGroup1"
            Name: "Stage::Planning"
            Description: "example description for the label"
            Color: "#FF0000"

        -
            Group: 
                - "ExampleGroup1"
                - "ExampleGroup2"
            Name: "Stage::RequireFeedback"
            Description: "example description for the label"
            Color: "#FF0000"
"""

        cls.ConfigFileContents_InvalidYML = """Group:
    Labels:
        -
            Group "This Group label is missing the ':' so it's invalid"
            Name: "Stage::Planning"
            Description: "example description for the label"
            Color: "#FF0000"

        -
            Group: 
                - "ExampleGroup1"
                - "ExampleGroup2"
            Name: "Stage::RequireFeedback"
            Description: "example description for the label"
            Color: "#FF0000"
"""
        
        cls.Gitlab_Instance_URL = 'http://mock_gitlab_url'
        cls.Gitlab_Instance_TOKEN = 'Gitlab token'

        with open('config.yml', 'w') as ConfigFile:
            ConfigFile.write(cls.ConfigFileContents)
        ConfigFile.close()

        # login and class init needs to be done for each test
        #cls.ClassToTest = GitlabManagement(cls.Gitlab_Instance_URL, cls.Gitlab_Instance_TOKEN, False)
        #The integration tests will be done against a gitlab instance


       
    def test_CreateGroupLabel(self):
        self.skipTest('implement')


    def test_GetGroupByName(self):
        
        self.skipTest('implement')


    def test_GetLabelByName(self):

        self.skipTest('implement')


    def test_GitlabLoginAuthenticate(self):

        self.skipTest('implement')



    @classmethod
    def tearDownClass(cls):
        
        pass




if __name__ == '__main__':
    #unittest.main()
    
    with open('Integration.JUnit.xml', 'wb') as output:

        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)