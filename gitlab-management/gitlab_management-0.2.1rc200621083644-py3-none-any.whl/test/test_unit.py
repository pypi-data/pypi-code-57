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

        cls.ClassToTest = GitlabManagement(cls.Gitlab_Instance_URL, cls.Gitlab_Instance_TOKEN, False)


            
    def test___init__file(self):
        # Check __init__.py to make sure all of the attributes are available

        self.assertTrue('__title__' in gitlab_management.__dict__, msg="__init__.py missing attribute __titl__")
        self.assertTrue('__version__' in gitlab_management.__dict__, msg="__init__.py missing attribute __version__")
        self.assertTrue('__doc__' in gitlab_management.__dict__, msg="__init__.py missing attribute __doc__")
        self.assertTrue('__author__' in gitlab_management.__dict__, msg="__init__.py missing attribute __author__")
        self.assertTrue('__email__' in gitlab_management.__dict__, msg="__init__.py missing attribute __email__")
        self.assertTrue('__license__' in gitlab_management.__dict__, msg="__init__.py missing attribute __license__")
        self.assertTrue('__copyright__' in gitlab_management.__dict__, msg="__init__.py missing attribute __copyright__")
        self.assertTrue('__source__' in gitlab_management.__dict__, msg="__init__.py missing attribute __source__")
      

    def test_Config(self):
        
        #ToDo fix this variable test, class should not be init before testing, so that it can be confirmed as existing before creating

        self.assertTrue('_Config' in self.ClassToTest.__dict__, msg="_Config Variable missing")

        #Within init, Config should be called, which populates `Config` variable, so this value should not be none
        self.assertFalse(self.ClassToTest.Config is None, msg="Class has been initialized, value should not be `None`")

        # Class has been init, config.yml loaded into `Config` variable.
        self.assertTrue(type(self.ClassToTest.Config) is dict, msg="Config is collected during class init, `Config` should be a `dict` of the config.yml file contents")

        # should not be able to change value
        with self.assertRaises(AttributeError, msg="You should not be able to set this value"):
            self.ClassToTest.Config = "IWontSet"

        #test the property config.getter.Valid yaml
        self.ClassToTest._Config = None
        self.assertTrue(self.ClassToTest._Config == None, msg="precursor test setting '_Config' to None for Config.getter test")

        self.assertTrue(self.ClassToTest.Config == yaml.safe_load(self.ConfigFileContents), msg="yaml file didn't load")

        #invalid yaml
        with open('config.yml', 'w') as ConfigFile:
                ConfigFile.write(self.ConfigFileContents_InvalidYML)
        ConfigFile.close()

         #test the property config.getter. Invalid yaml
        self.ClassToTest._Config = None
        self.assertTrue(self.ClassToTest._Config == None, msg="precursor test setting '_Config' to None for Config.getter test")

        with self.assertRaises(RuntimeError, msg="`RuntimeError` exception should have been thrown as the yaml was invalid"):
            self.ClassToTest.Config

        #Return yaml file t be valid
        with open('config.yml', 'w') as ConfigFile:
                ConfigFile.write(self.ConfigFileContents)
        ConfigFile.close()


    def test_CreateGroupLabel(self):
        #self.skipTest('implement')

        # not a group
        self.assertEqual(self.ClassToTest.CreateGroupLabel(None, Name='boo', Description='boo', Color='000000'), False, msg='Invalid group returns false')

        #is a group
        with requests_mock.Mocker() as m:
            
            with open('test/data/HTTPRequest_api_v4_groups_min_access_level.json', 'r') as Group_API_Call:
            
                m.get(self.Gitlab_Instance_URL + '/api/v4/groups?min_access_level=40', text=Group_API_Call.read(), status_code=200)

                GitLabGroup = self.ClassToTest.GetGroupByName('Documents')

                with open('test/data/HTTPRequest_api_v4_groups_1_labels.json', 'r') as Group_API_Call:
                    
                    m.get(self.Gitlab_Instance_URL + '/api/v4/groups/1/labels', text=Group_API_Call.read(), status_code=200)
                    
                    with unittest.mock.patch('gitlab.v4.objects.GroupLabelManager.create', unittest.mock.Mock()) as Mock_resp:
                        
                        self.assertEqual(self.ClassToTest.CreateGroupLabel(GitLabGroup, Name='feature', Description='boo', Color='000000'), True)

                        #Attempt to create a label that exists
                        self.assertEqual(self.ClassToTest.CreateGroupLabel(GitLabGroup, Name='Bug', Description='Label exists', Color='000000'), True)


    def test_GetConfig(self):
        
        try:
            
            with open('config.yml', 'w') as ConfigFile:
                ConfigFile.write(self.ConfigFileContents_InvalidYML)
            ConfigFile.close()

            self.assertFalse(self.ClassToTest.GetConfig(), msg="invalid yml files cause exception 'yaml.YAMLError' which needs to be handled by the method")
            
            # make a valid Yaml file and test again
            with open('config.yml', 'w') as ConfigFile:
                ConfigFile.write(self.ConfigFileContents)
            ConfigFile.close()

            self.assertTrue(self.ClassToTest.GetConfig(), msg="valid yml files are loaded with the method returning true.")

            #confirm what is in the file is loaded to the '_config' variable
            self.assertTrue(self.ClassToTest._Config == yaml.safe_load(self.ConfigFileContents))

        except yaml.YAMLError:
            self.assertFalse(True, msg="Exception `yaml.YAMLError` needs to be caught by the method") 

        except Exception:
            self.assertFalse(True, msg="Uncaught exceptions must be caught in the method")

    
    def test_GetGroupByName(self):
        #self.ClassToTest.GitlabObjectCache['Groups'] = None

        #Group:gitlab.v4.objects.Group = 
        with requests_mock.Mocker() as m:
            
            with open('test/data/HTTPRequest_api_v4_groups_min_access_level.json', 'r') as Group_API_Call:
            
                m.get(self.Gitlab_Instance_URL + '/api/v4/groups?min_access_level=40', text=Group_API_Call.read(), status_code=200)
            
            self.assertEqual(self.ClassToTest.GetGroupByName('Documents').name, 'Documents', msg='Unable to fetch group "Documents" by name')

            self.assertEqual(self.ClassToTest.GetGroupByName('A Random Name to fail'), None, msg="group doesn't exist, this test should = 'None'")

        #self.ClassToTest.GitlabObjectCache['Groups'] = None
        

    def test_GetLabelByName(self):

        try:
            with requests_mock.Mocker() as m:
                with open('test/data/HTTPRequest_api_v4_groups_1_labels.json', 'r') as Group_API_Call:
                    
                    m.get(self.Gitlab_Instance_URL + '/api/v4/groups/1/labels', text=Group_API_Call.read(), status_code=200)

                    #GroupName = self.ClassToTest.GitlabObjectCache['Groups']['Projects']

                    self.assertEqual(self.ClassToTest.GetLabelByName(self.ClassToTest.GetGroupByName('Documents'), 'Bug').name, 'Bug', msg="Searching for an existing label failed when it should not have")

                    self.assertEqual(self.ClassToTest.GetLabelByName(self.ClassToTest.GetGroupByName('Documents'), 'Non existant label'), None, msg="Searching for a label that doesn't exist should return 'None'")
        except Exception:
            
            self.assertFalse(True, msg="An uncaught exception occured when the method should have caught it")

    
    def test_GitlabLoginAuthenticate(self):

        try:
            
            with unittest.mock.patch('gitlab.Gitlab.auth', unittest.mock.Mock()):
                self.assertTrue(self.ClassToTest.GitlabLoginAuthenticate(self.Gitlab_Instance_URL, self.Gitlab_Instance_TOKEN))

            with requests_mock.Mocker() as m:
                m.get(self.Gitlab_Instance_URL + '/api/v4/user', text='mock test, failed to auth', status_code=401)
                self.assertFalse(self.ClassToTest.GitlabLoginAuthenticate(self.Gitlab_Instance_URL, self.Gitlab_Instance_TOKEN))

        except gitlab.GitlabAuthenticationError:
            self.assertFalse(True, msg="Exception 'gitlab.GitlabAuthenticationError' needs to be caught by the method")

        except Exception:
            self.assertFalse(True, msg="Uncaught exceptions must be caught in the method")


    def test_GitlabSession(self):

        self.assertTrue('_GitlabSession' in self.ClassToTest.__dict__, msg="_GitlabSession Variable missing")

        #self.skipTest("functional")
        ClassNotInit = GitlabManagement

        self.assertTrue(type(ClassNotInit.GitlabSession) is property, msg="Class not initalized, should be a property")
        
        self.assertTrue(type(self.ClassToTest.GitlabSession) == gitlab.Gitlab, msg="property must be type 'gitlab.Gitlab'")
    
        with self.assertRaises(TypeError, msg='Should not be able to set to different type'):
            boo:str = 'NotMe'
            self.ClassToTest.GitlabSession = boo


    def test_DesiredOutputLevel(self):

        self.assertTrue('_DesiredOutputLevel' in self.ClassToTest.__dict__, msg="_DesiredOutputLevel Variable missing")
        
        # Must be an int, however should be a GitlabManagement.OutputSeverity, can be none
        self.assertTrue(type(self.ClassToTest.DesiredOutputLevel) is self.ClassToTest.OutputSeverity, msg="Must be of type `self.ClassToTest.OutputSeverity`")

        #Should not be able to change type
        with self.assertRaises(TypeError, msg="Type Error must be thrown if setting the type doens't equal `self.ClassToTest.OutputSeverity`"):
            self.ClassToTest.DesiredOutputLevel = str('NoString')

        with self.assertRaises(TypeError, msg="Type Error must be thrown if setting the type doens't equal `self.ClassToTest.OutputSeverity`"):
            self.ClassToTest.DesiredOutputLevel = int(1)

        self.assertFalse(self.ClassToTest.GitlabObjectCache is type(None), msg="during class init, a default value needs to be assigned")


    def test_GitlabObjectCache(self):

        self.assertTrue('_GitlabObjectCache' in self.ClassToTest.__dict__, msg="_GitlabObjectCache Variable missing")

        # During init, `dict` is created with the required keys
        self.assertNotIsInstance(self.ClassToTest.GitlabObjectCache, type(None), msg="Item should not be initialized with NoneType")
        
        # Must be of type dict
        self.assertTrue(type(self.ClassToTest.GitlabObjectCache) is dict, msg="Property must be of type `dict`")

        # Must be dict, with Groups key
        self.assertTrue('Groups' in self.ClassToTest.GitlabObjectCache, msg="Group Key Must exist in `dict`")

        # ToDo: the line above test failed as now the getlabelby name makes a mock test. change this test to be a global check to see if the variable exists before the class has been init.

        #Should not be able to change type
        with self.assertRaises(AttributeError, msg="Attribute error should be thrown as no setter is required nor should exist"):
            ListObject:list = []
            self.ClassToTest.GitlabObjectCache = ListObject


    def test_OutputSeverity_Class(self):

        # Must be Enum        
        self.assertTrue(type(self.ClassToTest.OutputSeverity) is enum.EnumMeta, msg="Class must be an `enum`")

        # All Class Properties must be int
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Emergency.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Alert.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Critical.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Error.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Warning.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Notice.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Informational.value) is int, msg="Value must be an int")
        self.assertTrue(type(self.ClassToTest.OutputSeverity.Debug.value) is int, msg="Value must be an int")


    def test_ProcessConfigLabels(self):

        #self.skipTest('implement test')
        
        with requests_mock.Mocker() as m:
            
            with open('test/data/HTTPRequest_api_v4_groups_min_access_level.json', 'r') as Group_API_Call:
            
                m.get(self.Gitlab_Instance_URL + '/api/v4/groups?min_access_level=40', text=Group_API_Call.read(), status_code=200)

                
                with unittest.mock.patch('gitlab_management.base.GitlabManagement.CreateGroupLabel', unittest.mock.Mock()):
                        
                    self.assertEqual(self.ClassToTest.ProcessConfigLabels(self.ClassToTest.Config['Group']['Labels']), True, msg="Process label should return true")


    
    @classmethod
    def tearDownClass(cls):
        
        pass




if __name__ == '__main__':
    #unittest.main()
    
    with open('Unit.JUnit.xml', 'wb') as output:

        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)