#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.insert(0, "../gitlab_management")
sys.path.insert(0, "./gitlab_management")
sys.path.insert(0, "./")

from base import GitlabManagement

import unittest, xmlrunner
from enum import Enum
import gitlab

import gitlab_management

from cli import main as cli
from unittest.mock import patch

class GitlabManagement_Functional(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.ClassToTest = GitlabManagement

        cls.Gitlab_Instance_URL = 'http://gitlab.com'
        cls.Gitlab_Instance_TOKEN = 'Token'

        ConfigFileContents = """Group:
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
        #create config.yml
        with open('config.yml', 'w') as ConfigFile:
            ConfigFile.write(ConfigFileContents)
            

        cls.ClassToTest = GitlabManagement(cls.Gitlab_Instance_URL, cls.Gitlab_Instance_TOKEN, False)



    def test_cli_NoArgs(self):
        
        #No args should display help and exit non-zero to denotee error
        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
            with unittest.mock.patch('sys.argv', []):
                cli()

        self.assertEqual(ExitCode.exception.code, 1, msg="noargs should exit 1")
        
    
    def test_cli_Help(self):
    
        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
            with unittest.mock.patch('sys.argv', ['DummyFileName', "-h"]):
                cli()
            
        self.assertEqual(ExitCode.exception.code, 0, msg="Help should exit on 0")

        # ToDo assert output matches
        

    def test_cliLogonSuccess(self):
        
        
        with unittest.mock.patch('gitlab_management.base.GitlabManagement.GitlabLoginAuthenticate') as mock_authenticate:
            # Set auth to true, as this method is to only return bool
            mock_authenticate.return_value = True

            with unittest.mock.patch('gitlab_management.base.GitlabManagement._GitlabSession', unittest.mock.Mock()) as Session:
                Session = 'NotNoneMeansAuthenticated'

                #Mock Config Labels
                with unittest.mock.patch('gitlab_management.base.GitlabManagement.ProcessConfigLabels', unittest.mock.Mock()):
                
                    # specify all parameters for a connection, including host, verbose 3 and process labels, should exit 0
                    with unittest.mock.patch('sys.argv', ['DummyFileName', '-H', 'http://127.0.0.1', '-T', 'invalidtoken', '-v', '3', '-l']):
                        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
                            cli()
                        self.assertEqual(ExitCode.exception.code, 0, msg="connection should exit with code 0")
                    
                    # same test as above, however, don't specify host and http://gitlab.com will be used.
                    with unittest.mock.patch('sys.argv', ['DummyFileName', '-T', 'invalidtoken', '-v', '3']):
                        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
                            cli()
                        self.assertEqual(ExitCode.exception.code, 0, msg="connection should exit with code 0")
                
                    # same test as above, however, don't specify host and http://gitlab.com will be used and verbose above max of 7.
                    with unittest.mock.patch('sys.argv', ['DummyFileName', '-T', 'invalidtoken', '-v', '8', '-l']):
                        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
                            cli()
                        self.assertEqual(ExitCode.exception.code, 0, msg="connection should exit with code 0")

            
            # Test a failed authenticate.
            with unittest.mock.patch('gitlab.Gitlab') as GitLabNone:
                GitLabNone.return_value = None
                mock_authenticate.return_value = False

                with unittest.mock.patch('sys.argv', ['DummyFileName', '-T', 'invalidtoken', '-v', '8', '-l']):
                    with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
                        cli()
                        
                    self.assertNotEqual(ExitCode.exception.code, 0, msg="failed login should exit non zero")


    @patch('gitlab_management.base.GitlabManagement.GitlabLoginAuthenticate')
    def test_cli_LogonFail(self, mock_authenticate):

        #self.skipTest('ToDo: Implement an exit code for failed logon')

        # Set auth to true, as this method is to only return bool
        mock_authenticate.return_value = False

        # specify all parameters for a connection, including host, verbose 3 and process labels, should exit 0
        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
            with unittest.mock.patch('sys.argv', ['DummyFileName', '-H', 'http://127.0.0.1', '-T', 'invalidtoken']):
                cli()
        
        #ToDo Assert output to notify user

        self.assertNotEqual(ExitCode.exception.code, 0, msg="connection should exit with code non zero")


    @patch('gitlab_management.base.GitlabManagement.GitlabLoginAuthenticate')
    def test_cliProcessLabels(self, mock_authenticate):
        
        # Set auth to true, as this method is to only return bool
        mock_authenticate.return_value = True

        # specify all parameters for a connection, including host, verbose 3 and process labels, should exit 0
        with self.assertRaises(SystemExit, msg="When cli exits, an `ExitCode` must be present") as ExitCode:
            with unittest.mock.patch('sys.argv', ['DummyFileName', '-H', 'http://127.0.0.1', '-T', 'invalidtoken', '-l']):
                with unittest.mock.patch('gitlab_management.base.GitlabManagement.GitlabSession', unittest.mock.Mock()): # Must be a session available, so mock it
                    with unittest.mock.patch('gitlab_management.base.GitlabManagement.ProcessConfigLabels', unittest.mock.Mock()): #ToDo, change this to patch decoration so that the return can be set as the cli should output success/failure and exitcode to match
                        cli()
                        
        self.assertEqual(ExitCode.exception.code, 0, msg="connection should exit with code 0")
      


    @classmethod
    def tearDownClass(cls):
        
        pass



if __name__ == '__main__':
    with open('Function.JUnit.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
