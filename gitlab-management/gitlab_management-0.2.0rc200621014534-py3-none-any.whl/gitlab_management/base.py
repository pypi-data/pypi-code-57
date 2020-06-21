#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, getopt

class GitlabManagement:
  """
  No Fuss Computing's Gitlab Config Management python module.

  """
 
  import gitlab
  import gitlab.v4.objects
  import traceback
  import logging
  from enum import Enum


  _GitlabSession:gitlab.Gitlab = None

  @property
  def GitlabSession(self) -> gitlab.Gitlab:
    
    if self._GitlabSession == None:

      return None

    else:
      
      return self._GitlabSession


  @GitlabSession.setter
  def GitlabSession(self, oSession):

    if type(oSession) is self.gitlab.Gitlab or type(oSession) is None:

      self._GitlabSession = oSession

    else:
      raise TypeError("GitlabSession can only be type 'None' or 'gitlab.Gitlab' [{}] is neither".format(str(oSession)))



  _DesiredOutputLevel:int = None

  @property
  def DesiredOutputLevel(self) -> int:

    return self._DesiredOutputLevel

  @DesiredOutputLevel.setter
  def DesiredOutputLevel(self, Object):

    if type(Object) is not self.OutputSeverity:
      raise TypeError('{} must be of type OutputSeverity'.format(str(Object)))

    self._DesiredOutputLevel = Object

  _Config:dict = None

  @property
  def Config(self):

    if self._Config == None:
      if self.GetConfig():
        return self._Config
      else:
        raise RuntimeError('Unable to get config')

    else:
      return self._Config

  class OutputSeverity(Enum):

    Emergency:int = 0
    Alert:int = 1
    Critical:int = 2
    Error:int	= 3
    Warning:int = 4
    Notice:int = 5
    Informational:int = 6
    Debug:int = 7

  _GitlabObjectCache:dict = None
  """Cache the objects fetched via the GitLab API"""

  @property
  def GitlabObjectCache(self) -> dict:
    """Cache the objects fetched via the GitLab API
    
    See Also
    --------
    `Dependent Methods`:
      Nil
    
    `issue #8 <https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues/8>`_
      Feature: Groups now cached
    
    """

    return self._GitlabObjectCache




  def __init__(self, GitLab_URL:str, GitLab_PrivateToken:str, Authenticate:bool = True):

    self.DesiredOutputLevel = self.OutputSeverity.Informational

    if not self.GitlabLoginAuthenticate(GitLab_URL, GitLab_PrivateToken, Authenticate):
        self.Output(self.OutputSeverity.Critical, 'could not logon to ' + GitLab_URL)

    if not self.GetConfig():

        self.Output(self.OutputSeverity.Critical, "Couldn't load config yml")

    else:

        self.Output(self.OutputSeverity.Notice, 'config loaded')

        CacheINIT:dict = {}

        CacheINIT['Groups']:dict = None

        self._GitlabObjectCache = CacheINIT


  def GitlabLoginAuthenticate(self, URL:str, PrivateToken:str, Authenticate:bool = True) -> bool:
    """
    Establish the Gitlab instance to connect to and authenticate.


    Parameters
    ----------
    URL : str
      The url of the gitlab instance to connect to.

    PrivateToken : str
      The private token of the user that will be used to authenticate against the gitlab instance.


    Raises
    ------
    gitlab.GitlabAuthenticationError
      Returns text output of the failed authentication issue that occured when attemping to authenticate.

    Exception
      Generic catch all exception.


    Returns
    -------
    bool
      Returns `bool` to denote success/failure of the connection and authentication.

    See Also
    --------
    `Dependent Methods`:
      `Output <#gitlab_management.base.GitlabManagement.Output>`_

    """
    GitlabLoginAuthenticate = False

    try:
      GitlabLogin = self.gitlab.Gitlab(URL, private_token=PrivateToken)

      GitlabLogin.headers['User-Agent'] = "%s/%s %s" % (self.get_detail('title'), self.get_detail('version'), self.get_detail('doc'))

      if Authenticate:
        GitlabLogin.auth()

      self.GitlabSession = GitlabLogin

      GitlabLoginAuthenticate = True

    except self.gitlab.GitlabAuthenticationError as e:

      self.Output(self.OutputSeverity.Error, str(e))

    except Exception as e:

      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return GitlabLoginAuthenticate


  def Output(self, OutputLevel:OutputSeverity, OutputMessage:str) -> None:
    """
    Method to output commands to the console.


    Parameters
    ----------
    OutputLevel : GitlabManagement.OutputSeverity(Enum)
      The output leval that the message is categorised as.

    OutputMessage : str
      The text to output.
        

    Raises
    ------
    Exception
      None raised.
      # ToDo: do proper error and exception handling.


    Returns
    -------
    None
      This method does not require output as it is part of the error handling of the application.

    See Also
    --------
    `Dependent Methods`: 
      Nil

    """
    if OutputLevel.value <= self.DesiredOutputLevel.value:
      print(str(OutputLevel.name) + ': ' + OutputMessage)


  def GetConfig(self) -> bool:
    """
    Read all of the `config.yml` config file to an object in this class.
        

    Raises
    ------
    yaml.YAMLError
      any error with the yml, will return the text output

    Exception
      Generic catch all exception. if this exception occurs, please log an issue ticket.


    Returns
    -------
    bool
      returns success/failure on reading the config and adding to the class object `self.Config`

    See Also
    --------
    `Dependent Methods`:
       `Output <#gitlab_management.base.GitlabManagement.Output>`_
    
    `Help`
      `config.yml <../pages/configuration.html#config.yml>`_
    
    """
    import yaml

    GetConfig = False

    with open("config.yml", 'r') as stream:

      try:

        self._Config = dict(yaml.safe_load(stream))
        GetConfig = True

      except yaml.YAMLError as exc:

        self.Output(self.OutputSeverity.Error, str(exc))

      except Exception as e:
        self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return GetConfig


  def CreateGroupLabel(self, Group:gitlab.v4.objects.Group, Name:str, Description:str, Color:str) -> bool:
    """Create a group label within the specified group
    
    Parameters
    ----------
    Group : gitlab.v4.objects.Group
      A gitlab group Object
    
    Name : str
      The name of the label to create

    Description : str
      The description for the label. the description will be prefixed with [Managed Label] to denote this script created the label.

    Color : str
      the colour that the label shoud be in format '#RRGGBB'

    Raises
    ------
    Exception
      Generic catch all Exception is returned, however the exception will be printed to the console

    gitlab.GitlabHttpError
      A http error occured, the output should denote what the issue is

    gitlab.GitlabCreateError
      a check for '409: label exists', as no attempt should be made to create a label when the check has already been done.

      Warning
      -------
      if any other status is returned, then an issue should be raised.


    Returns
    -------
    bool
      if the string was successfully created, true is returned. false will be returned when there was an exception
    
    See Also
    --------
    `Dependent Methods`:
      `GetLabelByName <#gitlab_management.base.GitlabManagement.GetLabelByName>`_
      `Output <#gitlab_management.base.GitlabManagement.Output>`_
    

    """
    NewLabelString = {}
    CreateGroupLabel = False

    if type(Group) == self.gitlab.v4.objects.Group:

      try:

        if self.GetLabelByName(Group, Name) is None:

          NewLabelString['name'] = Name
          NewLabelString['description'] = '[Managed Label] ' + Description
          NewLabelString['color'] = Color

          Group.labels.create(NewLabelString)

          self.Output(self.OutputSeverity.Notice, 'Created label {} in group {}'.format(NewLabelString['name'], Group.attributes['name']))

        else:

          self.Output(self.OutputSeverity.Debug, 'Label {} exists in group {}'.format(Name, Group.attributes['name']))

        CreateGroupLabel = True

      except self.gitlab.GitlabHttpError as e:

          self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

      except self.gitlab.GitlabCreateError as e:

          if e.response_code == 409:

              self.Output(self.OutputSeverity.Critical, ' attempted to create a label that exists. please report this error')

          else:

              self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

      except Exception as e:

        self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return CreateGroupLabel


  def GetGroupByName(self, GroupName:str) -> gitlab.v4.objects.Group:
    """
    Find and return a group by name.

    Workflow
    1. Find all groups that the current user (the one authorized in this module) has maintainer access to
    2. check if the group has been cached, if not cach the groups for subsequent use so that additional API calls don't have to be made.
    3. create an empty Labels group in the group object so that if a request for group labels is made, this can be checked for `None` if they haven't been fetched before.
    4. iterate through all returned groups until the group is found that matches the string.

    Parameters
    ----------
    GroupName : str
      description
        

    Raises
    ------
    Exception
      Generic catch all exception. if this method returns an exception please log an issue.

      # ToDo: add proper error checking and exception checking.


    Returns
    -------
    gitlab.v4.objects.Group
      The Group that matches the search string will be returned.
    
    None
      Returned if nothing found
    
    See Also
    --------
    `Dependent Methods`:
      `Output <#gitlab_management.base.GitlabManagement.Output>`_

    `issue #8 <https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues/8>`_
      Feature: Groups now cached

    """
    GetGroupByName = None

    try:

      if self.GitlabObjectCache['Groups'] is None:

        Groups = self.GitlabSession.groups.list(min_access_level = self.gitlab.MAINTAINER_ACCESS)

        self.GitlabObjectCache['Groups'] = {}

        for Group in Groups:

            groupID = str(Group.attributes['id'])

            self.Output(self.OutputSeverity.Debug, 'Caching group "{}" with an id of {}'.format(Group.attributes['name'], Group.attributes['id']))

            self.GitlabObjectCache['Groups'][groupID] = {
                'GroupObject': Group,
                'Labels': None,
                }

        Groups = self.GitlabObjectCache['Groups']

      else:

          Groups = self.GitlabObjectCache['Groups']

      for GroupID in Groups:

        if Groups[GroupID]['GroupObject'].attributes['name'] == GroupName:

          GetGroupByName = Groups[GroupID]['GroupObject']

    except Exception as e:

      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return GetGroupByName


  def GetLabelByName(self, Group:gitlab.v4.objects.Group, LabelName:str) -> gitlab.v4.objects.GroupLabel:
    """
    Finds a label by human readable name and returns a `gitlab.v4.objects.GroupLabel` object.

    Workflow:
    1. Check if the labels for the group have been cached, if not cache them. 
    1. iterate through each label in the group until the `LabelName` matches.
    2. return the label as a `gitlab.v4.objects.GroupLabel`


    Parameters
    ----------
    Group : gitlab.v4.objects.Group
      The group that is being searched.
    
    LabelName : str
      The group name to search for.
    
    
    Raises
    ------
    Exception
      Generic catch all exception. if this method returns an exception please log an issue.


    Returns
    -------
    gitlab.v4.objects.GroupLabel
      returns the object that has a name that matches what was searched for.

    None
      Only returned if no group is found.
    
    
    See Also
    --------
    `Dependent Methods`:
      `ProcessConfigLabels <gitlab_management.base.html#gitlab_management.base.GitlabManagement.ProcessConfigLabels>`_
      `Output <#gitlab_management.base.GitlabManagement.Output>`_

    `Help`
      `Labels <../pages/labels.html>`_
    
    `issue #8 <https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues/8>`_
      Feature: Labels now cached 

    """
    GetLabelByName = None

    try:

        if type(Group) is self.gitlab.v4.objects.Group:

            CachedGroupLabels = self.GitlabObjectCache['Groups'][str(Group.attributes['id'])]['Labels']

            if CachedGroupLabels is None:

                Labels = Group.labels.list(all=True)

                LabelCount:int = 0

                for LabletoCount in Labels:
                    LabelCount += 1
                    self.Output(self.OutputSeverity.Debug, 'Caching label "{}", id "{}" from group {}'.format(LabletoCount.attributes['name'], LabletoCount.attributes['id'], Group.attributes['name']))

                self.GitlabObjectCache['Groups'][str(Group.attributes['id'])]['Labels'] = Labels

                self.Output(self.OutputSeverity.Informational, 'caching "{}" labels for group "{}"'.format(str(LabelCount), str(Group.attributes['name'])))

            for Label in self.GitlabObjectCache['Groups'][str(Group.attributes['id'])]['Labels']:

                if Label.attributes['name'] == LabelName:

                    GetLabelByName = Label

                    exit

    except Exception as e:

      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return GetLabelByName 


  def ProcessConfigLabels(self, ConfigGroups:list) -> bool:
    """
    Process the provided configuration labels.

    load the labels from the `config` file and create for each group that has been specified for the label.

    The array that is passed to the function is processed as follows.

    1. iterates through list of labels
    2. finds the group id that the label is for 
    3. confirms that label attributes are in the config file Group, Name, Description and color.
    4. creates the label in each group that the label is intended for. `CreateGroupLabel()` does the check to see if it exists before creating it.
    

    Parameters
    ----------
    ConfigGroups : list
      The labels array from the config.yml file  


    Raises
    ------
    Exception
      currently is a catch all exception. if this function returns an exception, an issue needs to be raised.


    Returns
    -------
    bool
      returns bool denoting success/failure for the processing of the labels provided.


    See Also
    --------
    `Dependent Methods`:
      `GetGroupByName <#gitlab_management.base.GitlabManagement.GetGroupByName>`_
      `GetLabelByName <#gitlab_management.base.GitlabManagement.GetLabelByName>`_
      `Output <#gitlab_management.base.GitlabManagement.Output>`_
    
    `Help`
      `configuration <../pages/configuration.html>`_
      `Labels <../pages/labels.html>`_
    
    `issue #8 <https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues/8>`_
      Feature: Labels now cached

    """
    ProcessConfigGroups = False

    try:

      self.Output(self.OutputSeverity.Notice, 'Processing Config: labels')

      for Label in ConfigGroups:

        if 'Group' in Label and 'Name' in Label and 'Description' in Label and 'Color' in Label:

          if type(Label['Group']) is list:

            for Group in Label['Group']:

              Group = self.GetGroupByName(Group)

              self.CreateGroupLabel(Group, Label['Name'], Label['Description'], Label['Color'])

          else:

            self.CreateGroupLabel(self.GetGroupByName(Label['Group']), Label['Name'], Label['Description'], Label['Color'])

        else:
          self.Output(self.OutputSeverity.Error, 'missing the Group for the label')

      ProcessConfigGroups = True

    except Exception as e:
      self.Output(self.OutputSeverity.Critical, logging.error(traceback.format_exc()))

    return ProcessConfigGroups


  def get_detail(self, ItemName:str):
    with open("gitlab_management/__init__.py") as f:
        for line in f:
            if line.startswith("__" + ItemName + "__"):
                return(str(line.split("=")[-1]).replace('"', '').replace("\n", '').replace(" ", ''))
