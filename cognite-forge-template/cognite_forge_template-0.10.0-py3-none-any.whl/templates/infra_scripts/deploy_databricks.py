import base64
import os
import sys
from collections import deque
from typing import Dict, List, Tuple
from uuid import uuid1

from databricks_api import DatabricksAPI
from requests.exceptions import HTTPError
from ruamel.yaml import YAML

CONFIG_FILE_PATH = "config.yaml"


def copy_workspace_in_databricks(src: str, dest: str, handler: DatabricksAPI, overwrite: bool = False) -> None:
    print(f"Trying to copy from {src} to {dest} ...")
    if check_path_exists(src, handler):
        exported = handler.workspace.export_workspace(src, format="DBC")
        if overwrite:
            delete_workspace(dest, handler)
        handler.workspace.import_workspace(dest, format="DBC", content=exported["content"])
        print(f"Done copying.")
    else:
        print(f"Workspace with path {src} does not exist.")


def restore_production_workspace(copy_loc: str, dest: str, handler: DatabricksAPI) -> None:
    print("Trying to restore production workspace from copy ...")
    if check_path_exists(copy_loc, handler):
        copy_workspace_in_databricks(copy_loc, dest, handler, overwrite=True)
        print(f"Workspace with path {dest} successfully restored.")
    else:
        print(f"Workspace with path {copy_loc} does not exist. Cannot perform restore. Please do it manually.")


def delete_workspace(path: str, handler: DatabricksAPI) -> None:
    print(f"Trying to delete workspace with path {path} ... ")
    if check_path_exists(path, handler):
        handler.workspace.delete(path, recursive=True)
        print(f"Workspace with path {path} successfully deleted.")
    else:
        print(f"Workspace with path {path} does not exist.")


def check_path_exists(path: str, handler: DatabricksAPI) -> bool:
    try:
        handler.workspace.get_status(path)
        return True
    except HTTPError as e:
        if e.response.status_code == 404:
            return False
        else:
            raise e


def read_config() -> Dict:
    with open(CONFIG_FILE_PATH) as f:
        data = YAML(typ="safe").load(f)["databricks"]

    return data


def get_upload_paths_and_dirs(workspace_path: str) -> Tuple[Tuple[List[str], List[str]], List[str]]:
    stack = deque(["databricks"])
    local_paths = []
    while stack:
        curr_path = stack.pop()
        if os.path.isfile(curr_path):
            local_paths.append(curr_path)
        else:
            sub_paths = list(map(lambda p: os.path.join(curr_path, p), os.listdir(curr_path)))
            stack.extend(sub_paths)

    upload_paths: List[str] = list(map(lambda p: p.replace("databricks", workspace_path), local_paths))
    upload_dirs: List[str] = list(map(lambda p: os.path.dirname(p).replace("databricks", workspace_path), local_paths))
    paths = (local_paths, upload_paths)
    return paths, upload_dirs


def upload_notebooks_and_folders(paths: Tuple[List[str], List[str]], upload_dirs, handler: DatabricksAPI) -> None:
    print("Creating directories ...")
    for d in upload_dirs:
        handler.workspace.mkdirs(d)
        print(f"Created {d} ...")

    print("\nUploading notebooks ...")
    for local_path, upload_path in zip(paths[0], paths[1]):
        with open(local_path, "rb") as f:
            content = f.read()
            encoded_content = base64.b64encode(content).decode()
            handler.workspace.import_workspace(upload_path, language="PYTHON", format="SOURCE", content=encoded_content)
            print(f"Uploaded {local_path} as {upload_path}")


def upload_from_repo(prod_workspace_path: str, handler: DatabricksAPI) -> None:
    paths, dirs = get_upload_paths_and_dirs(prod_workspace_path)
    upload_notebooks_and_folders(paths, dirs, handler)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Expected Databricks token to passed as a command line argument.")

    else:
        config = read_config()
        databricks_handler = DatabricksAPI(host=config["host"], token=sys.argv[1])
        prod_workspace = config["production"]["workspace_path"]

        backup_path = f"{prod_workspace}-backup-{uuid1()}"
        copy_workspace_in_databricks(prod_workspace, backup_path, databricks_handler)
        try:
            delete_workspace(prod_workspace, databricks_handler)
            upload_from_repo(prod_workspace, databricks_handler)
        except [HTTPError, FileNotFoundError]:
            restore_production_workspace(backup_path, prod_workspace, databricks_handler)
        finally:
            delete_workspace(backup_path, databricks_handler)
