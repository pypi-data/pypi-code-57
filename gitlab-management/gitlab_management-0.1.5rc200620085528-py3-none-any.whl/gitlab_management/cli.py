#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, getopt, logging, traceback
from gitlab_management.base import GitlabManagement


help = """GitLab-Management Help
To run this module the following options are available. There is a short and long version of each option.

Example: python3 gitlab-management -T {GitlabAuthToken}

-H    --Host      (Optional) GitLab host to connect to. include http(s)://. Default: https://gitlab.com
-T    --Token     (Mandatory) GitLab Private token for authentication.
-l    --labels    Process configuration group.labels.

-v    --verbose   (Optional) Verbose command output.

-h    --Help      used to display this help text.

"""


 
def main():

  try:
    
    full_cmd_arguments = sys.argv

    if len(full_cmd_arguments) == 0:
      raise getopt.error('No Arguments specified')
    
    argument_list = full_cmd_arguments[1:]

    short_options = "H:T:hv:l"
    long_options = ["Host=", "Token=" "help", "verbose=", "Labels"]

    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    
    GitlabHost = None
    GitlabPrivateToken = None
    RunCLI = True
    Verbose:int = None

    Option_Labels:bool = False

    for current_argument, current_value in arguments:

      if current_argument in ("-H", "--Host"):

          GitlabHost = current_value

      elif current_argument in ("-T", "--Token"):

          GitlabPrivateToken = current_value

      elif current_argument in ("-l", "--labels"):

          Option_Labels = True

      elif current_argument in ("-v", "--verbose"):

        if int(current_value) <= 7: 
          #ToDo implement a type check (int) on the verbose value as it needs to be an int.
          #   Setting the value to non-int will cause an un-caught exception

          Verbose = current_value

      elif current_argument in ("-h", "--help"):
          
          RunCLI = False

          print (help)

  
    if RunCLI:

      if GitlabHost is None:
        GitlabHost = 'https://gitlab.com'

      print('starting')

      GitlabManagementObject = GitlabManagement(GitlabHost, GitlabPrivateToken)

      if Verbose is not None:
        GitlabManagementObject.DesiredOutputLevel = GitlabManagement.OutputSeverity(int(Verbose))

      if GitlabManagementObject.GitlabSession is not None:

        if Option_Labels:
          GitlabManagementObject.ProcessConfigLabels(GitlabManagementObject.Config['Group']['Labels'])
      else:
        sys.exit(3)

      


  except getopt.error as err:

    print (help)

    print (str(err) + "\n")

    sys.exit(1) #ToDo standardise the exit codes. enum?

  except Exception as e:

    print(logging.error(traceback.format_exc()))
    
    sys.exit(2)
  
  
  sys.exit(0)
  

