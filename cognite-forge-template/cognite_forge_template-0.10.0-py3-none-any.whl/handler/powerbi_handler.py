# import os
# import re
# import shutil
# from typing import Dict, List
#
# from pbiapi import PowerBIAPIClient
#
# import forge_template.util.log_util as log_util
# from forge_template.handler.handler import BaseHandler
# from forge_template.paths import (
#     POWERBI_BASE_DATASET_PATH,
#     POWERBI_BASE_REPORT_PATH,
#     POWERBI_PATH,
#     POWERBI_TEMPLATE_PATH,
# )
# from forge_template.tool_info import ToolInfo
#
#
# class PowerBIHandler(BaseHandler):
#     def __init__(self, config: Dict, tool_info: ToolInfo) -> None:
#         self.name = tool_info.name
#         config = config[self.name]
#         self._client = PowerBIAPIClient(config["tenant_id"], config["application_id"], config["token"])
#
#         self._dev_workspace = config["development"]
#         self._prod_workspace = config["production"]
#
#         self._workspaces_to_create: List[str] = []
#         self._users_to_add_to_workspace: Dict[str, List[str]] = {}
#         self._users_to_update_in_workspace: Dict[str, List[Dict]] = {}
#
#         self._added_workspaces: List[str] = []
#         self._added_users_to_workspace: Dict[str, List[str]] = {}
#
#         super().__init__(config=config, tool_info=tool_info)
#
#     def create_preview(self) -> None:
#         self.check_workspaces_to_add([self._dev_workspace, self._prod_workspace])
#
#     def print_preview(self) -> None:
#         if not self._workspaces_to_create and not self._users_to_add_to_workspace:
#             log_util.print_message("No changes to deploy")
#         log_util.print_resource_to_add(self._workspaces_to_create, "Workspace")
#         log_util.print_resources_to_update(self._users_to_add_to_workspace, "Principal", "Workspace")
#
#     def setup(self) -> None:
#         self.create_workspaces(self._workspaces_to_create)
#         self.add_users_to_workspace(self._users_to_add_to_workspace)
#
#     def rollback(self) -> None:
#         if self._added_workspaces:
#             log_util.print_rollback("workspaces")
#             self.__remove_workspaces(self._added_workspaces)
#
#     def delete_all_resources(self):
#         self.__remove_workspaces([self._dev_workspace["name"], self._prod_workspace["name"]])
#
#     def check_workspaces_to_add(self, workspaces: List) -> None:
#         """
#         Checks which PowerBI workspaces to add, as well as which users to add to the workspace.
#
#         Args:
#             workspaces: List of workspace definitions. See config.yaml for example.
#         """
#         existing_workspaces = self.__get_existing_workspaces()
#         for workspace in workspaces:
#             workspace_name = workspace["name"]
#             if workspace_name not in existing_workspaces.keys():
#                 self._workspaces_to_create.append(workspace_name)
#                 self._users_to_add_to_workspace[workspace_name] = workspace["principals"]
#
#     def __get_existing_workspaces(self) -> Dict:
#         response = self._client.get_workspaces()
#         return {w["name"]: w for w in response}
#
#     def __remove_workspaces(self, workspace_names: List) -> None:
#         for workspace_name in workspace_names:
#             self._client.delete_workspace(workspace_name)
#             log_util.print_success_deleted(workspace_name, "Workspace")
#
#     def create_workspaces(self, workspace_names: List) -> None:
#         """
#         Creates workspaces in PowerBI
#
#         Args:
#             workspace_names: Names of workspaces to create
#         """
#         self.__copy_folders_locally()
#         for name in workspace_names:
#             self.create_workspace(name)
#
#     def create_workspace(self, workspace_name: str) -> None:
#         """
#         Creates a workspace in PowerBI and uploads a dataset to that workspace.
#
#         Args:
#             workspace_name: Name of workspace to create
#         """
#         self._client.create_workspace(workspace_name)
#         self._added_workspaces.append(workspace_name)
#         self.__upload_files_to_workspace(workspace_name)
#         self.__rebind_report_to_dataset(workspace_name)
#         log_util.print_success_created(workspace_name, "Workspace")
#
#     def add_users_to_workspace(self, workspace_name_to_users: Dict[str, List[str]]) -> None:
#         """
#         Add a users to an existing PowerBI workspace.
#
#         Args:
#             workspace_name_to_users: Workspace name to list of users where each user is a dictionary with keys:
#                 ``"identifier"``
#                 Id of user to add (email, group id or app id) (str)
#
#                 ``"access_right"``
#                 Permission level to give to the user (Admin, Member, Contributor) (str)
#         """
#         for workspace_name, users in workspace_name_to_users.items():
#             for user in users:
#                 self.add_user_to_workspace(user, workspace_name)
#
#     def add_user_to_workspace(self, user_id: str, workspace_name: str, access_right: str = "Admin") -> None:
#         """
#         Add a user to an existing workspace and set the permissions of that user
#
#         Args:
#             user_id: Id of user. A user can be a person, group or Power App.
#             workspace_name: Name of workspace where the user will be added
#             access_right: Permission level to give to the user
#         """
#         user = {"identifier": user_id, "groupUserAccessRight": access_right}
#         if self.__assert_is_email(user_id):
#             user["UserEmailAddress"] = user_id
#         self._client.add_user_to_workspace(workspace_name, user)
#         if workspace_name not in self._added_users_to_workspace.keys():
#             self._added_users_to_workspace[workspace_name] = []
#         self._added_users_to_workspace[workspace_name].append(user_id)
#         log_util.print_success_added(workspace_name, "Workspace", user_id, "Principal")
#
#     def __upload_files_to_workspace(self, workspace_name: str) -> None:
#         pbix_paths = [POWERBI_BASE_DATASET_PATH, POWERBI_BASE_REPORT_PATH]
#         for file_path in pbix_paths:
#             display_name = self.get_display_name_from_pbix_path(file_path)
#             skip_report = "dataset" in display_name
#             self.__upload_file_to_workspace(workspace_name, file_path, display_name, skip_report)
#
#     def __upload_file_to_workspace(
#         self, workspace_name: str, local_path: str, display_name: str, skip_report: bool = False
#     ) -> None:
#         self._client.import_file_into_workspace(workspace_name, skip_report, local_path, display_name)
#         log_util.print_success_added(workspace_name, "Workspace", display_name, "PBIX file")
#
#     def __rebind_report_to_dataset(self, workspace_name: str) -> None:
#         dataset_name = self.get_display_name_from_pbix_path(POWERBI_BASE_DATASET_PATH)
#         report_name = self.get_display_name_from_pbix_path(POWERBI_BASE_REPORT_PATH)
#
#         self._client.rebind_report_in_workspace(workspace_name, dataset_name, report_name)
#         self._client.delete_dataset(workspace_name, report_name)
#
#     @staticmethod
#     def __assert_is_email(s: str) -> bool:
#         regex = re.compile(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
#         return re.search(regex, s) is not None
#
#     @staticmethod
#     def __copy_folders_locally() -> None:
#         if not os.path.exists(POWERBI_PATH):
#             shutil.copytree(POWERBI_TEMPLATE_PATH, POWERBI_PATH)
#
#     @staticmethod
#     def get_display_name_from_pbix_path(path: str) -> str:
#         return os.path.splitext(os.path.basename(path))[0]
