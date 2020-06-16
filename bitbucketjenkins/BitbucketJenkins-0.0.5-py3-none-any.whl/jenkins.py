#! /usr/bin/env python

import json
import requests
from .client import Client

class Jenkins:
    def __init__(self, base_url, username, password):
        self.client = Client(base_url, username, password)
        self.crumb = self.client.getCrumb()
        self.client.session.headers.update({'Content-Type': 'text/xml; charset=utf-8', 'Jenkins-Crumb': self.crumb})
        self.job = Job(self.client)
    
class Job:
    def __init__(self, client):
        self.client = client
        self.resource_path = "/createItem?name="
        self.config_xml = '''<?xml version='1.1' encoding='UTF-8'?>
<jenkins.branch.OrganizationFolder plugin="branch-api@2.5.6">
  <actions/>
  <description></description>
  <properties>
    <org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty plugin="config-file-provider@3.4.1">
      <configs class="sorted-set">
        <comparator class="org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty$1"/>
      </configs>
    </org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty>
    <jenkins.branch.OrganizationChildHealthMetricsProperty>
      <templates>
        <com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric plugin="cloudbees-folder@6.13">
          <nonRecursive>false</nonRecursive>
        </com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric>
      </templates>
    </jenkins.branch.OrganizationChildHealthMetricsProperty>
    <jenkins.branch.OrganizationChildOrphanedItemsProperty>
      <strategy class="jenkins.branch.OrganizationChildOrphanedItemsProperty$Inherit"/>
    </jenkins.branch.OrganizationChildOrphanedItemsProperty>
    <jenkins.branch.OrganizationChildTriggersProperty>
      <templates>
        <com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger plugin="cloudbees-folder@6.13">
          <spec>H H/4 * * *</spec>
          <interval>86400000</interval>
        </com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger>
      </templates>
    </jenkins.branch.OrganizationChildTriggersProperty>
    <org.jenkinsci.plugins.pipeline.modeldefinition.config.FolderConfig plugin="pipeline-model-definition@1.3.2">
      <dockerLabel></dockerLabel>
      <registry plugin="docker-commons@1.13"/>
    </org.jenkinsci.plugins.pipeline.modeldefinition.config.FolderConfig>
    <jenkins.branch.NoTriggerOrganizationFolderProperty>
      <branches>BRANCH_PATTERN</branches>
    </jenkins.branch.NoTriggerOrganizationFolderProperty>
  </properties>
  <folderViews class="jenkins.branch.OrganizationFolderViewHolder">
    <owner reference="../.."/>
  </folderViews>
  <healthMetrics>
    <com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric plugin="cloudbees-folder@6.13">
      <nonRecursive>false</nonRecursive>
    </com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric>
  </healthMetrics>
  <icon class="jenkins.branch.MetadataActionFolderIcon">
    <owner class="jenkins.branch.OrganizationFolder" reference="../.."/>
  </icon>
  <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy" plugin="cloudbees-folder@6.13">
    <pruneDeadBranches>true</pruneDeadBranches>
    <daysToKeep>-1</daysToKeep>
    <numToKeep>5</numToKeep>
  </orphanedItemStrategy>
  <triggers>
    <com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger plugin="cloudbees-folder@6.13">
      <spec>H/5 * * * *</spec>
      <interval>600000</interval>
    </com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger>
  </triggers>
  <disabled>false</disabled>
  <navigators>
    <com.cloudbees.jenkins.plugins.bitbucket.BitbucketSCMNavigator plugin="cloudbees-bitbucket-branch-source@2.7.0">
      <serverUrl>BITBUCKET_URL</serverUrl>
      <credentialsId>BITBUCKET_CREDENTIAL_ID</credentialsId>
      <repoOwner>PROJECT_ID</repoOwner>
      <traits>
        <com.cloudbees.jenkins.plugins.bitbucket.BranchDiscoveryTrait>
          <strategyId>1</strategyId>
        </com.cloudbees.jenkins.plugins.bitbucket.BranchDiscoveryTrait>
        <com.cloudbees.jenkins.plugins.bitbucket.OriginPullRequestDiscoveryTrait>
          <strategyId>1</strategyId>
        </com.cloudbees.jenkins.plugins.bitbucket.OriginPullRequestDiscoveryTrait>
        <com.cloudbees.jenkins.plugins.bitbucket.ForkPullRequestDiscoveryTrait>
          <strategyId>1</strategyId>
          <trust class="com.cloudbees.jenkins.plugins.bitbucket.ForkPullRequestDiscoveryTrait$TrustTeamForks"/>
        </com.cloudbees.jenkins.plugins.bitbucket.ForkPullRequestDiscoveryTrait>
        <com.cloudbees.jenkins.plugins.bitbucket.SSHCheckoutTrait>
          <credentialsId>BITBUCKET_SSH_CREDENTIAL_ID</credentialsId>
        </com.cloudbees.jenkins.plugins.bitbucket.SSHCheckoutTrait>
      </traits>
    </com.cloudbees.jenkins.plugins.bitbucket.BitbucketSCMNavigator>
  </navigators>
  <projectFactories>
    <org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProjectFactory plugin="workflow-multibranch@2.20">
      <scriptPath>Jenkinsfile</scriptPath>
    </org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProjectFactory>
  </projectFactories>
  <buildStrategies/>
</jenkins.branch.OrganizationFolder>'''
    
    def create(self, project_id, **kwargs):
        """
        Create a jenkins job with bitbucket team/project plugin
        """
        self.config_xml = self.config_xml.replace('PROJECT_ID', project_id.upper())
        for key, value in kwargs.items(): 
          self.config_xml = self.config_xml.replace(key.upper(), value)
        self.data = self.config_xml.encode('utf-8')
        return self.client.post(self.resource_path + project_id, self.data)