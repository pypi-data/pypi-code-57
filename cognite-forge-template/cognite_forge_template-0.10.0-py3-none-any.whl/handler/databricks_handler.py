import logging
from pathlib import Path, PosixPath
from typing import Callable, Dict, List

from databricks_api import DatabricksAPI
from requests import HTTPError

import forge_template.util.file_util as file_util
import forge_template.util.log_util as log_util
from forge_template.handler.github_actions_handler import GithubActionsHandler
from forge_template.handler.handler import FORBIDDEN_CODE, NOT_FOUND_CODE, BaseHandler
from forge_template.paths import DATABRICKS_OUTPUT_DIR, DATABRICKS_TEMPLATE_DIR
from forge_template.tool_info import ToolInfo

CONFIG_PATH_PLACEHOLDER = "YAML_CONFIG_PATH_PLACEHOLDER"
DEFAULT_SCOPE_ACCESS = "WRITE"
WORKSPACE = "Workspace"
WORKSPACE_DIRECTORY = "Workspace Directory"
DBFS_DIRECTORY = "DBFS Directory"


class DatabricksHandler(BaseHandler):
    def __init__(self, config: Dict, tool_info: ToolInfo) -> None:
        self.name = tool_info.name
        config = config[self.name]
        self.client = DatabricksAPI(host=config["host"], token=config["token"])

        self._dev_workspace = config["development"]
        self._prod_workspace = config["production"]
        self._dbfs_path = PosixPath(config["config_dbfs_path"])

        self._config_output_path = tool_info.schema_info[0].output_path
        self._config_output_path = tool_info.schema_info[0].output_path

        self.workspaces_to_create: List[PosixPath] = []
        self.groups_to_create: List[str] = []
        self.scopes_to_create: List[Dict[str, str]] = []
        self.dbfs_dirs_to_create: List[PosixPath] = []
        self.users_to_add_to_group: Dict[str, List[str]] = {}
        self.secrets_to_add_to_scope: Dict[str, List[Dict[str, str]]] = {}
        self.groups_to_add_to_scope: Dict[str, List[str]] = {}

        self.created_workspaces: List[PosixPath] = []
        self.created_groups: List[str] = []
        self.created_scopes: List[str] = []
        self.created_dbfs_dirs: List[PosixPath] = []
        self.added_users_to_group: Dict[str, List[str]] = {}
        self.added_groups_to_scope: Dict[str, List[str]] = {}

        self.github_actions_handler = GithubActionsHandler(tool_info=tool_info)

        super().__init__(config=config, tool_info=tool_info)

    def create_preview(self) -> None:
        self.check_dbfs_dir_to_add(self._dbfs_path)
        self.check_workspaces_to_add(
            [PosixPath(self._dev_workspace["workspace_path"]), PosixPath(self._prod_workspace["workspace_path"])]
        )
        self.check_scopes_to_add([self._dev_workspace, self._prod_workspace])
        self.check_groups_to_add([self._dev_workspace["group"], self._prod_workspace["group"]])
        self.github_actions_handler.create_preview()

    def print_preview(self):
        log_util.print_resource_to_add(self.workspaces_to_create, "Workspaces")
        log_util.print_resource_to_add(self.groups_to_create, "Groups")
        log_util.print_resource_to_add(list(map(lambda scope: scope["scope_name"], self.scopes_to_create)), "Scopes")
        log_util.print_resource_to_add(self.dbfs_dirs_to_create, "DBFS Directories")
        logging.info("")
        log_util.print_resources_to_update(self.users_to_add_to_group, "User", "Group")
        log_util.print_resources_to_update(self.secrets_to_add_to_scope, "Secret", "Scope")
        log_util.print_resources_to_update(self.groups_to_add_to_scope, "Group", "Scope")
        logging.info("")
        self.github_actions_handler.print_preview()

    def setup(self):
        self.create_workspaces(self.workspaces_to_create)
        self.create_dbfs_directories(self.dbfs_dirs_to_create)
        self.create_groups(self.groups_to_create)
        self.add_users_to_group(self.users_to_add_to_group)
        self.create_scopes(self.scopes_to_create)
        self.add_groups_to_scope(self.groups_to_add_to_scope)
        self.add_secrets_to_scope(self.secrets_to_add_to_scope)
        self.github_actions_handler.run_setup()

    def rollback(self) -> None:
        if self.created_scopes:
            logging.info("Rolling back all scopes that have been created.")
            self.remove_scopes(self.created_scopes)
        if self.created_groups:
            logging.info("Rolling back all groups that have been added.")
            self.remove_groups(self.created_groups)
        if self.created_workspaces:
            logging.info("Rolling back all workspaces that have been created.")
            self.remove_workspace_directories(self.created_workspaces)
        if self.created_dbfs_dirs:
            logging.info("Rolling back all DBFS directories that have been added.")
            self.remove_dbfs_directories(self.created_dbfs_dirs)
        if self.added_users_to_group:
            groups_with_new_users = self.get_dict_list_subtraction(self.added_users_to_group, self.created_groups)
            if groups_with_new_users:
                logging.info("Rolling back all users that have been added to groups.")
                self.remove_users_from_groups(groups_with_new_users)
        if self.added_groups_to_scope:
            scopes_with_new_groups = self.get_dict_list_subtraction(self.added_groups_to_scope, self.created_scopes)
            if scopes_with_new_groups:
                logging.info("Rolling back all groups that have been added to scopes.")
                self.remove_groups_from_scope(scopes_with_new_groups)

    def delete_all_resources(self) -> None:
        self.remove_groups([self.config["production"]["group"]["name"], self.config["development"]["group"]["name"]])
        self.remove_dbfs_directories([self.config["config_dbfs_path"]])
        self.remove_scopes([self.config["production"]["scope"]["name"], self.config["development"]["scope"]["name"]])
        self.remove_workspace_directories(
            [self.config["production"]["workspace_path"], self.config["development"]["workspace_path"]]
        )

    def upload_config(self) -> None:
        self.check_dbfs_dir_to_add(self._dbfs_path)
        self.create_dbfs_directories(self.dbfs_dirs_to_create)
        for path in self.dbfs_dirs_to_create:
            self.copy_files_to_dbfs(path, self._config_output_path)

    def check_groups_to_add(self, groups: List) -> None:
        """
        Checks which Databricks groups to add, as well as which users to add to the groups

        Args:
            groups: List of groups. See config.yaml for example.
        """
        existing_groups = self.get_existing_groups()
        for group in groups:
            group_name = group["name"]
            users = group["users"]

            if group_name in existing_groups:
                log_util.print_resource_already_exists(group_name, "Group")
                self.check_users_to_add(group_name, users, True)
            else:
                self.check_users_to_add(group_name, users, False)
                self.groups_to_create.append(group_name)

    def check_users_to_add(self, group_name: str, users: List[str], group_exist: bool) -> None:
        if group_exist:
            current_users = self.get_existing_users_in_group(group_name)
            users = list(set(users) - set(current_users))

        self.users_to_add_to_group[group_name] = users

    def check_scopes_to_add(self, configs: List[Dict]) -> None:
        """
        Checks which Databricks scopes to add

        Args:
            configs: List of scope configs. See config.yaml and secrets.yaml for examples.
        """
        existing_scopes = self.get_existing_scopes()
        for config in configs:
            self.check_scope_to_add(config["scope"], existing_scopes, config["group"]["name"])

    def check_scope_to_add(self, scope_config: Dict, existing_scopes: List[str], group_name: str) -> None:
        """
        Checks whether or not to add a given scope, as well as which secrets to add to the scope

        Args:
            scope_config: Scope configuration. See config.yaml for example.
            existing_scopes: List with names of existing scopes
            group_name: Name of group that should have access to scope
        """
        scope_name = scope_config["name"]
        initial_manage_principal = (
            self.config["initial_manage_principal"]
            if (self.config["initial_manage_principal"] != "" and self.config["initial_manage_principal"] is not None)
            else None
        )

        scope_exists = False
        if scope_name in existing_scopes:
            log_util.print_resource_already_exists(scope_name, "Scope")
            scope_exists = True
        else:
            self.scopes_to_create.append(
                {"scope_name": scope_name, "initial_manage_principal": initial_manage_principal}
            )

        self.check_group_to_add_to_scope(scope_name, group_name, scope_exists)
        self.check_secrets_to_add_to_scope(
            scope_name, scope_config["secrets"], scope_config["cdf_api_key"] if "cdf_api_key" in scope_config else ""
        )

    def check_group_to_add_to_scope(self, scope_name: str, group_name: str, scope_exists: bool) -> None:
        if scope_name not in self.groups_to_add_to_scope:
            self.groups_to_add_to_scope[scope_name] = []

        if scope_exists:
            if not self.does_acls_exist_in_scope(scope_name, group_name):
                self.groups_to_add_to_scope[scope_name].append(group_name)
        else:
            self.groups_to_add_to_scope[scope_name].append(group_name)

    def check_secrets_to_add_to_scope(self, scope_name: str, secrets: List[Dict[str, str]], cdf_api_key: str = ""):
        if cdf_api_key:
            secrets.append({"key": "cdf_api_key", "string_value": cdf_api_key})

        if scope_name not in self.secrets_to_add_to_scope:
            self.secrets_to_add_to_scope[scope_name] = []
        self.secrets_to_add_to_scope[scope_name].extend(secrets)

    def check_workspaces_to_add(self, workspace_paths: List[PosixPath]) -> None:
        """
        Checks if the given workspace paths already exists.

        Args:
            workspace_paths: Workspace paths to check
        """
        for workspace_path in workspace_paths:
            if self.does_path_exist(workspace_path, lambda client, path: client.workspace.list(str(path))):
                log_util.print_resource_already_exists(workspace_path, WORKSPACE)
            else:
                self.workspaces_to_create.append(workspace_path)

    def check_dbfs_dir_to_add(self, path: PosixPath) -> None:
        """
        Checks if the given dbfs path already exists. If not, it will be added to a the list of dbfs paths to add

        Args:
            path: Path to check
        """
        if self.does_path_exist(path, lambda client, path: client.dbfs.list(path)):
            log_util.print_resource_already_exists(str(path), DBFS_DIRECTORY)
        else:
            self.dbfs_dirs_to_create.append(path)

    def create_groups(self, group_names: List[str]) -> None:
        """
        Creates Databricks groups

        Args:
            group_names: Names of groups to create
        """
        for name in group_names:
            self.client.groups.create_group(name)
            self.created_groups.append(name)
            log_util.print_success_created(entity_name=name, entity_type="Group")

    def add_users_to_group(self, group_to_users: Dict[str, List[str]]):
        """
        Adds users to a specified group

        Args:
            group_to_users: Group name to list of user names
        """
        for group_name, users in group_to_users.items():
            for name in users:
                self.client.groups.add_to_group(group_name, user_name=name)
                if group_name not in self.added_users_to_group:
                    self.added_users_to_group[group_name] = []
                self.added_users_to_group[group_name].append(name)
                log_util.print_success_added(group_name, "Group", name, "User")

    def create_scopes(self, scopes: List[Dict]) -> None:
        """
        Create Databricks scopes

        Args:
            scopes: List with scope names
        """
        for scope in scopes:
            self.client.secret.create_scope(
                scope=scope["scope_name"], initial_manage_principal=scope["initial_manage_principal"]
            )

            self.created_scopes.append(scope["scope_name"])
            log_util.print_success_created(scope["scope_name"], "Scope")

    def add_secrets_to_scope(self, scope_to_secrets: Dict[str, List[Dict]]) -> None:
        """
        Add secrets to a specified scope

        Args:
            scope_to_secrets: Scope name to list of secrets where each secret is a dictionary with keys:
                ``"key"``
                Key/Identifier of secret (str)

                ``"string_value"``
                The actual secret value (str)
        """
        for scope, secrets in scope_to_secrets.items():
            for secret in secrets:
                self.client.secret.put_secret(scope, secret["key"], secret["string_value"])
                log_util.print_success_added(scope, "Scope", secret["key"], "Token")

    # TODO: Handling of Databricks account that isn't premium
    def add_groups_to_scope(self, scope_to_group: Dict[str, List[str]]) -> None:
        """
        Add groups to a specified scope.

        Args:
            scope_to_group: Scope name to list of group names
        """
        for scope, groups in scope_to_group.items():
            for group in groups:
                try:
                    self.client.secret.put_acl(scope, group, DEFAULT_SCOPE_ACCESS)
                    if scope not in self.added_groups_to_scope:
                        self.added_groups_to_scope[scope] = []
                    self.added_groups_to_scope[scope].append(group)
                    log_util.print_success_added(scope, "Scope", group, "Group")
                except HTTPError as e:
                    if e.response.status_code == FORBIDDEN_CODE:
                        logging.warning(f"Account doesn't support ACL.")
                        continue
                    raise e

    def create_workspaces(self, workspace_paths: List[PosixPath]) -> None:
        """
        Creates Databricks workspaces and add notebook templates to the workspaces

        Args:
            workspace_paths: Paths to add workspace to in Databricks
        """
        dbfs_location = PosixPath("/dbfs") / PosixPath(*self._dbfs_path.parts[1:]) / self._config_output_path
        file_src_to_dest = [
            (path, DATABRICKS_OUTPUT_DIR / path.relative_to(DATABRICKS_TEMPLATE_DIR))
            for path in DATABRICKS_TEMPLATE_DIR.rglob("*.py")
        ]
        file_util.copy_tree_and_replace_placeholders(file_src_to_dest, CONFIG_PATH_PLACEHOLDER, str(dbfs_location))
        for path in workspace_paths:
            self.create_workspace(path)

    def create_workspace(self, base_path: PosixPath) -> None:
        """
        Creates a Databricks workspace and add notebook templates to the workspace

        Args:
            base_path: Path to add workspace to in Databricks
        """
        self.create_workspace_directory(base_path)
        self.created_workspaces.append(base_path)

        for folder_name in file_util.get_rel_folder_paths(DATABRICKS_OUTPUT_DIR):
            workspace_path = PosixPath(base_path / folder_name)
            self.create_workspace_directory(workspace_path)
        self.copy_notebooks_to_workspace(base_path)

    def create_workspace_directory(self, directory_path: PosixPath) -> None:
        self.client.workspace.mkdirs(str(directory_path))
        log_util.print_success_created(directory_path, WORKSPACE_DIRECTORY)

    def copy_notebooks_to_workspace(self, workspace_path: PosixPath) -> None:
        notebook_paths = DATABRICKS_OUTPUT_DIR.rglob("*.py")
        for path in notebook_paths:
            content = file_util.get_base64_encoded_content(path)
            local_path = path.relative_to(DATABRICKS_OUTPUT_DIR)
            upload_path = workspace_path / local_path
            self.client.workspace.import_workspace(
                str(upload_path.as_posix()), language="PYTHON", format="SOURCE", content=content
            )
            log_util.print_success_added(upload_path.parent, WORKSPACE_DIRECTORY, local_path.name, "Notebook")

    def copy_files_to_dbfs(self, dbfs_path: PosixPath, local_path: Path) -> None:
        self.client.dbfs.put(
            str(dbfs_path / local_path.name), contents=file_util.get_base64_encoded_content(local_path)
        )
        log_util.print_success_added(dbfs_path, DBFS_DIRECTORY, local_path.name, "File")

    def create_dbfs_directories(self, directory_paths: List[PosixPath]) -> None:
        """
        Creates Databricks DBFS directories and copies the config.yaml file to those directories

        Args:
            directory_paths: List of DBFS paths to create
        """
        for path in directory_paths:
            self.client.dbfs.mkdirs(str(path))
            self.created_dbfs_dirs.append(path)
            log_util.print_success_created(path, DBFS_DIRECTORY)
            self.copy_files_to_dbfs(path, self._config_output_path)

    def remove_groups(self, groups: List) -> None:
        self.remove_entities(
            groups, "Group", self.get_existing_groups, lambda client, group: client.groups.remove_group(group)
        )

    def remove_users_from_groups(self, group_to_users: Dict) -> None:
        """
        Removes users from a Databricks group

        Args:
            group_to_users: Group name to list of user names
        """
        self.remove_sub_entity_from_entity(
            group_to_users,
            self.get_existing_groups,
            self.get_existing_users_in_group,
            lambda client, group, user: client.groups.remove_from_group(group, user),
            "Group",
            "User",
        )

    def remove_scopes(self, scopes: List[str]) -> None:
        self.remove_entities(
            scopes, "Scope", self.get_existing_scopes, lambda client, scope: client.secret.delete_scope(scope)
        )

    def remove_groups_from_scope(self, scope_to_groups: Dict) -> None:
        """
        Remove group permissions to scope in Databricks

        Args:
            scope_to_groups: Name of scope to list of group names
        """
        self.remove_sub_entity_from_entity(
            scope_to_groups,
            self.get_existing_scopes,
            self.get_existing_acls_in_scope,
            lambda client, scope, group: client.secret.delete_acl(scope, group),
            "Scope",
            "Group",
        )

    def remove_workspace_directories(self, directory_paths: List[PosixPath]) -> None:
        self.remove_paths(
            directory_paths,
            lambda client, path: client.workspace.list(str(path)),
            lambda client, path: client.workspace.delete(str(path), recursive=True),
            WORKSPACE_DIRECTORY,
        )

    def remove_dbfs_directories(self, directory_paths: List[PosixPath]) -> None:
        self.remove_paths(
            directory_paths,
            lambda client, path: client.dbfs.list(str(path)),
            lambda client, path: client.dbfs.delete(str(path), recursive=True),
            DBFS_DIRECTORY,
        )

    def remove_entities(
        self,
        entities: List[str],
        entity_type: str,
        get_existing: Callable[[List[str]], List[str]],
        remove: Callable[[DatabricksAPI, str], None],
    ):
        entities = get_existing(entities)
        for entity in entities:
            remove(self.client, entity)
            log_util.print_success_deleted(entity, entity_type)

    def remove_sub_entity_from_entity(
        self,
        entity_to_sub: Dict[str, List[str]],
        get_existing_entities: Callable[[List[str]], List[str]],
        get_exisiting_sub_entities: Callable[[str, List[str]], List[str]],
        remover: Callable[[DatabricksAPI, str, str], None],
        entity_type: str,
        sub_entity_type: str,
    ) -> None:
        existing_entities = get_existing_entities(list(entity_to_sub.keys()))
        for entity in existing_entities:
            sub_entities = get_exisiting_sub_entities(entity, entity_to_sub[entity])
            for sub_entity in sub_entities:
                remover(self.client, entity, sub_entity)
                log_util.print_success_removed(sub_entity, entity, sub_entity_type, entity_type)

    def remove_paths(
        self,
        paths: List[PosixPath],
        existence_checker: Callable[[DatabricksAPI, PosixPath], None],
        delete_method: Callable[[DatabricksAPI, PosixPath], None],
        path_type: str,
    ) -> None:
        for path in paths:
            if self.does_path_exist(path, existence_checker):
                delete_method(self.client, path)
                log_util.print_success_deleted(str(path), path_type)

    def does_path_exist(self, path: PosixPath, check_function: Callable[[DatabricksAPI, PosixPath], None]) -> bool:
        """
        Check if a directory path already exists in Databricks

        Args:
            path: Path of directory to check
            check_function: Function doing the checking
        """
        try:
            check_function(self.client, path)
            return True
        except HTTPError as e:
            if e.response.status_code == NOT_FOUND_CODE:
                return False
            raise e

    def entity_exist(
        self, entity: str, getter: Callable[[DatabricksAPI], Dict], key: str, dict_to_list: Callable[[Dict], str] = None
    ) -> bool:
        return entity in self.get_existing_entities(getter, key, dict_to_list)

    def get_existing_entities(
        self,
        getter: Callable[[DatabricksAPI], Dict],
        key: str,
        dict_to_list: Callable[[Dict], str] = None,
        entities_to_check=None,
    ) -> List[str]:
        existing_entities_response = getter(self.client)
        existing_entities = self.get_entity_response_to_list(existing_entities_response, key, dict_to_list)
        if entities_to_check is None:
            return existing_entities
        else:
            return list(set(existing_entities).intersection(set(entities_to_check)))

    def get_existing_groups(self, groups: List[str] = None):
        return self.get_existing_entities(
            getter=lambda client: client.groups.get_groups(), key="group_names", entities_to_check=groups
        )

    def get_existing_scopes(self, scopes: List[str] = None):
        return self.get_existing_entities(
            getter=lambda client: client.secret.list_scopes(),
            key="scopes",
            entities_to_check=scopes,
            dict_to_list=lambda d: d["name"],
        )

    def get_existing_users_in_group(self, group_name: str, users: List[str] = None) -> List[str]:
        return self.get_existing_entities(
            getter=lambda client: client.groups.get_group_members(group_name),
            key="members",
            entities_to_check=users,
            dict_to_list=lambda d: d["user_name"],
        )

    def does_acls_exist_in_scope(self, scope_name: str, acl: str) -> bool:
        return acl in self.get_existing_acls_in_scope(scope_name)

    def get_existing_acls_in_scope(self, scope_name: str, acls: List[str] = None) -> List[str]:
        return self.get_existing_entities(
            getter=lambda client: client.secret.list_acls(scope_name),
            key="items",
            entities_to_check=acls,
            dict_to_list=lambda d: d["principal"],
        )

    @staticmethod
    def get_entity_response_to_list(entity_response: Dict, key: str, dict_transformer: Callable[[Dict], str] = None):
        if key not in entity_response:
            return []
        if dict_transformer:
            return [dict_transformer(entity) for entity in entity_response[key]]
        return entity_response[key]
