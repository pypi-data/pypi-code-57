# import os
# import shutil
# import tempfile
# from os import listdir
# from os.path import isfile, join
# from typing import Dict, List
#
# from azure.devops.connection import Connection
# from azure.devops.exceptions import AzureDevOpsServiceError
# from azure.devops.v5_1.build.models import (
#     AgentPoolQueue,
#     BuildDefinition,
#     BuildDefinitionVariable,
#     BuildRepository,
#     TeamProjectReference,
# )
# from azure.devops.v5_1.git.models import GitRepositoryCreateOptions
# from git import Repo
# from msrest.authentication import BasicAuthentication
#
# import forge_template.handler.git_utils as git_utils
# import forge_template.util.log_utils as print_utils
# from forge_template.handler.handler import BaseHandler
# from forge_template.util.yaml_util import DATABRICKS_CONFIG_NAME, PIPELINES_PATH, POWERBI_CONFIG_NAME
#
# PIPELINE_SERVICES = ["databricks", "powerbi"]
#
#
# class AzureHandler(BaseHandler):
#     """
#     Handler for interacting with Azure DevOps.
#     Currently supporting:
#         - Create Azure Repo
#         - Create Azure Build Definition
#     """
#
#     def __init__(self, name: str, config: Dict):
#         self._databricks_config = config[DATABRICKS_CONFIG_NAME]
#         self._powerbi_config = config[POWERBI_CONFIG_NAME]
#
#         config = config[name]
#         self._organization = config["principal"]
#         self._project_name = config["project_name"]
#         self._repo_name = config["repo_name"]
#
#         url = f"https://dev.azure.com/{self._organization}"
#         credentials = BasicAuthentication("", config["token"])
#         connection = Connection(base_url=url, creds=credentials)
#         self._core_client = connection.clients.get_core_client()
#         self._build_client = connection.clients.get_build_client()
#         self._git_client = connection.clients.get_git_client()
#
#         self._git_tmp_work_dir = tempfile.TemporaryDirectory().name
#         self._local_repo = Repo.init(path=self._git_tmp_work_dir)
#
#         self._project_id: str = ""
#         self._repo_url: str = ""
#         self._repo_ssh_url: str = ""
#         self._definition_ids: Dict[str, str] = {}
#
#         self._build_definitions_to_create: List[_BuildDefinition] = []
#         self._created_build_definitions: List[Dict[str, str]] = []
#
#         self._repos_to_create: List[str] = []
#         self._remotes_to_rename: List[str] = []
#         self._remotes_to_add: List[str] = []
#
#         self._created_repos: Dict[str, str] = {}
#         self._renamed_remotes: List[str] = []
#         self._added_remotes: List[str] = []
#
#         super().__init__(name=name, config=config)
#
#     @property
#     def __project_id(self) -> str:
#         return self._project_id if self._project_id else self.__get_project_id()
#
#     def __get_project_id(self) -> str:
#         project = self._core_client.get_project(project_id=self._project_name)
#         self._project_id = project.id
#         return project.id
#
#     @property
#     def __repo_url(self) -> str:
#         return self._repo_url if self._repo_url else self.__get_repository_urls()
#
#     @property
#     def __repo_ssh_url(self) -> str:
#         return self._repo_ssh_url if self._repo_ssh_url else self.__get_repository_urls(return_ssh=True)
#
#     @property
#     def __repo_id(self) -> str:
#         return self.__get_repository_id()
#
#     @property
#     def __definition_ids(self) -> Dict[str, str]:
#         return self._definition_ids if self._definition_ids else self.__get_existing_definitions(self.__project_id)
#
#     def __get_repository_urls(self, return_ssh: bool = False) -> str:
#         try:
#             repository = self._git_client.get_repository(repository_id=self._repo_name, project=self.__project_id)
#             self._repo_ssh_url = repository.ssh_url
#             self._repo_url = repository.url
#             return repository.ssh_url if return_ssh else repository.url
#         except AzureDevOpsServiceError as e:
#             if e.type_key == "GitRepositoryNotFoundException":
#                 return ""
#             raise e
#
#     def __get_repository_id(self):
#         repository = self._git_client.get_repository(repository_id=self._repo_name, project=self.__project_id)
#         return repository.id
#
#     def create_preview(self) -> None:
#         if not self.__repo_ssh_url:
#             self._repos_to_create.append(self._repo_name)
#         git_utils.check_remotes_to_add
#         (self._local_repo, self._repo_name, self._remotes_to_rename, self._remotes_to_add)
#         self.create_definition_preview(self.__project_id)
#
#     def print_preview(self) -> None:
#         print_utils.print_resource_to_add([self._repo_name], "Repository")
#         print_utils.print_remotes_to_rename(self._remotes_to_rename)
#         print_utils.print_resource_to_add(self._remotes_to_add, "Remote")
#         print_utils.print_resource_to_add(self._build_definitions_to_create, "Build definition")
#
#     def setup(self) -> None:
#         for repo_name in self._repos_to_create:
#             self.create_repo(repo_name, self.__project_id)
#
#         try:
#             remote_name = self._local_repo.remote()
#         except ValueError:
#             remote_name = None
#         if self._repo_ssh_url is not None and remote_name is None:
#             self._local_repo.create_remote("origin", self._repo_ssh_url)
#
#         self.__copy_files_to_repo_dir()
#
#         git_utils.push_content_to_repo(self._local_repo, self._repo_name)
#
#         for definition in self._build_definitions_to_create:
#             self.create_definition(
#                 name=definition.name, variables=definition.build_variables, file_path=definition.file_path
#             )
#
#     def rollback(self) -> None:
#         for definition in self._created_build_definitions:
#             self.delete_definition(definition=definition)
#
#         for repo_id, repo_name in self._created_repos.items():
#             self.delete_repo(name=repo_name, repo_id=repo_id)
#
#         git_utils.remove_remotes(self._added_remotes, self._local_repo)
#         git_utils.rename_remotes(self._renamed_remotes, self._local_repo, [])
#
#     def delete_all_resources(self):
#         self.delete_repo(self._repo_name, self.__repo_id)
#         for def_name, def_id in self.__definition_ids.items():
#             self.delete_definition({"name": def_name, "id": def_id})
#
#     def create_repo(self, repo_name: str, project_id: str) -> None:
#         """
#         Creates a new Azure DevOps Repository
#
#         Args:
#             repo_name: Name of repository
#             project_id: Id of Azure DevOps project where the repository will be created
#         """
#         create_repo = GitRepositoryCreateOptions(name=repo_name)
#         response = self._git_client.create_repository(create_repo, project=project_id)
#         self._created_repos[repo_name] = response.id
#         self._repo_ssh_url = response.ssh_url
#         print_utils.print_success_created(repo_name, "Repository")
#
#     def delete_repo(self, name: str, repo_id: str) -> None:
#         """
#         Deletes an Azure DevOps Repository
#
#         Args:
#             name: Name of repository
#             repo_id: Id of Azure DevOps Repository that will be deleted
#         """
#         self._git_client.delete_repository(repo_id, project=self._project_id)
#         print_utils.print_success_deleted(name, "Repository")
#
#     def create_definition_preview(self, project_id: str):
#         """
#         Checks which build definitions that does not exist. All definition files in the pipelines folder are checked.
#         If a build definition does not exist, it is added to the list of definitions (_build_definitions_to_create)
#         that are to be created.
#         """
#         existing_definitions = self.__get_existing_definitions(project_id=project_id)
#         for file_path in os.listdir(PIPELINES_PATH):
#             service = os.path.splitext(file_path)[0]
#             definition_name = f"{self._project_name}-{service}"
#             if definition_name not in existing_definitions:
#                 self._build_definitions_to_create.append(
#                     _BuildDefinition(
#                         definition_name, self.__get_build_variables(service), os.path.join(PIPELINES_PATH, file_path),
#                     )
#                 )
#
#     def create_definition(self, name: str, variables: Dict[str, BuildDefinitionVariable], file_path: str,) -> None:
#         """
#         Creates a Azure DevOps Build definition
#
#         Args:
#             name: Name of definition
#             variables: Dictionary mapping variable name to its definition (BuildDefinitionVariable)
#             file_path: Path of .yaml/.yml file containing the definition
#         """
#
#         build_repo = BuildRepository(
#             default_branch="refs/heads/master",
#             checkout_submodules=False,
#             name=self._repo_name,
#             url=self.__repo_url,
#             type="TfsGit",
#             properties={"reportBuildStatus": True},
#         )
#
#         queue = AgentPoolQueue(name="Azure Pipelines")
#         triggers = {"settingsSourceType": 2, "batchChanges": False, "triggerType": "continuousIntegration"}
#         project = TeamProjectReference(id=self.__project_id)
#         process = {"type": 2, "yamlFilename": file_path}
#
#         definition = BuildDefinition(
#             name=name,
#             project=project,
#             repository=build_repo,
#             process=process,
#             type="build",
#             variables=variables,
#             queue=queue,
#             triggers=[triggers],
#         )
#
#         response = self._build_client.create_definition(definition, self.__project_id)
#         self._created_build_definitions.append({"name": name, "id": response.id})
#         print_utils.print_success_created(name, "Build definition")
#
#     def delete_definition(self, definition: Dict[str, str]) -> None:
#         """
#         Deletes a definition
#
#         Args:
#             definition: Definition to be deleted as a dictionary with keys:
#                 ``"id"``
#                 Id of definition to delete (str)
#
#                 ``"name"``
#                 Name of definition to delete (str)
#         """
#         self._build_client.delete_definition(self.__project_id, definition["id"])
#         print_utils.print_success_deleted(definition["name"], "Build definition")
#
#     def __get_build_variables(self, service_name: str) -> Dict[str, BuildDefinitionVariable]:
#         if service_name == "databricks":
#             return {
#                 "DatabricksHost": BuildDefinitionVariable(value=self._databricks_config["host"]),
#                 "DatabricksToken": BuildDefinitionVariable(value=self._databricks_config["token"], is_secret=True),
#                 "DatabricksNotebookFolder": BuildDefinitionVariable(value="databricks"),
#                 "DatabricksWorkspaceFolder": BuildDefinitionVariable(
#                     value=self._databricks_config["production"]["workspace_path"]
#                 ),
#             }
#         elif service_name == "powerbi":
#             return {
#                 "POWERBI_TENANT_ID": BuildDefinitionVariable(value=self._powerbi_config["tenant_id"]),
#                 "POWERBI_APPLICATION_ID": BuildDefinitionVariable(value=self._powerbi_config["application_id"]),
#                 "POWERBI_TOKEN": BuildDefinitionVariable(value=self._powerbi_config["token"], is_secret=True),
#                 "POWERBI_WORKSPACE": BuildDefinitionVariable(value=self._powerbi_config["production"]["name"]),
#             }
#         else:
#             raise RuntimeError(f"Unexpected
#             service name. Got {service_name}, but expected on of [databricks, powerbi]")
#
#     def __get_existing_definitions(self, project_id: str) -> Dict[str, str]:
#         """
#         Fetches the existing build definitions for the current project id
#
#         Returns: A list of definition names
#         """
#         definitions = self._build_client.get_definitions(project_id).value
#         return {definition.name: definition.id for definition in definitions}
#
#     def __copy_files_to_repo_dir(self) -> None:
#         working_dir = os.getcwd()
#
#         pipelines_path = os.path.join(working_dir, "pipelines")
#         template_databricks_path = os.path.join(working_dir, "template", "databricks")
#         template_powerbi_path = os.path.join(working_dir, "template", "powerbi")
#         template_infra_path = os.path.join(working_dir, "template", "infra_scripts")
#         config_path = os.path.join(working_dir, "config.yaml")
#         requirements_path = os.path.join(working_dir, "requirements.txt")
#
#         self.__handle_copy_dir_files(pipelines_path, "pipelines")
#         self.__handle_copy_dir_files(template_databricks_path, "databricks")
#         self.__handle_copy_dir_files(template_powerbi_path, "powerbi")
#         self.__handle_copy_dir_files(template_infra_path, "infra_scripts")
#
#         shutil.copy(config_path, self._git_tmp_work_dir)
#         shutil.copy(requirements_path, self._git_tmp_work_dir)
#
#     def __handle_copy_dir_files(self, source_dir: str, file_type: str) -> None:
#         files = [
#             join(source_dir, f) for f in listdir(source_dir) if isfile(join(source_dir, f)) and f != "." and f != ".."
#         ]
#         dest_path = os.path.join(self._git_tmp_work_dir, file_type)
#         os.mkdir(dest_path)
#         for file in files:
#             shutil.copy(file, dest_path)
#
#
# class _BuildDefinition:
#     def __init__(self, name: str, build_variables: Dict[str, BuildDefinitionVariable], file_path: str):
#         self.name = name
#         self.build_variables = build_variables
#         self.file_path = file_path
