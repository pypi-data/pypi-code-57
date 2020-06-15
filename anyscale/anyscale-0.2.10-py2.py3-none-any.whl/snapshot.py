import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
from subprocess import STDOUT
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

import click
import ray.ray_constants
import requests

from anyscale.conf import SNAPSHOT_REPO, SNAPSHOT_REPO_PASSWORD, TEST_V2
from anyscale.project import get_project_id
from anyscale.util import (
    confirm,
    get_cluster_config,
    get_requirements,
    send_json_request,
    Timer,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)


class SnapshotRunner:
    def __init__(self) -> None:
        self.snapshot_home = os.path.expanduser("~/.anyscale/snapshot")
        self.password = SNAPSHOT_REPO_PASSWORD
        self.snapshot_repo = SNAPSHOT_REPO

        # Get the right restic executable path depending on the OS.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if sys.platform.startswith("linux"):
            self.snapshot_executable = os.path.join(current_dir, "restic-linux")
        elif sys.platform.startswith("darwin"):
            self.snapshot_executable = os.path.join(current_dir, "restic-darwin")
        else:
            raise NotImplementedError(
                "Restic snapshot not supported on platform {}".format(sys.platform)
            )

    def setup(self) -> None:
        proc = subprocess.Popen(
            [self.snapshot_executable, "init", "-r", self.snapshot_repo],
            env={"RESTIC_PASSWORD": self.password},
        )

        proc.communicate()

    def upload(
        self,
        snapshot_uuid: str,
        project_dir: str,
        additional_files: List[str],
        files_only: bool,
        creds: Dict[str, str],
    ) -> None:
        """This function takes and upload a snapshot to S3. The snapshot
        consists of all the items in project_dir (if specified) and any
        additional_files specified.

        Args:
            snapshot_uuid: uuid of the snapshot to be uploaded to restic repo.
            project_dir: directory of the anyscale project.
            additional_files: additional files to be included with the snapshot (if any).
            creds: credentials used to access S3.
        """
        additional_files_list = tempfile.NamedTemporaryFile()
        with open(additional_files_list.name, "w") as temp:
            for f in additional_files:
                temp.write(f + "\n")

        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password
        print(json.dumps({"snapshot_uuid": snapshot_uuid}))
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "backup",
                "--files-from",
                additional_files_list.name,
                "" if files_only else project_dir,
                "--tag",
                snapshot_uuid,
                "--tag",
                "project_dir=" + project_dir,
                "--verbose",
                "--verbose",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        collecting_output = False
        while True:
            if proc.stdout:
                line = proc.stdout.readline()
                if not line:
                    break

                if b"open repository" in line:
                    timer = Timer("Taking snapshot of all files within this project")
                    timer.start()
                elif b"start backup" in line:
                    timer.stop()
                    timer = Timer("Saving snapshot to Anyscale")
                    timer.start()
                elif b"scan finished" in line:
                    timer.stop()
                    print("\n" + line.decode())
                elif not collecting_output and line == b"\n":
                    collected_out = ""
                    collecting_output = True

                if collecting_output:
                    collected_out += line.decode()
        print(collected_out)

    def download(
        self, name: str, target_directory: Union[str, Path], creds: Dict[str, str],
    ) -> None:
        """This function downloads a snapshot from S3 to a target directory.
        The snapshot could be of a project, in which case it will have all
        project files and possibly output_files. Or it could be of any files
        on the remote cluster.
        Args:
            name: id of the snapshot to download.
            target_directory: directory to download the snapshot to.
            creds: credentials used to download the snapshot.
        """
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        restic_id, project_dir, additional_files = self.get_restic_info(name, new_env)

        with tempfile.TemporaryDirectory() as snapshot_dir:
            proc = subprocess.Popen(
                [
                    self.snapshot_executable,
                    "-r",
                    self.snapshot_repo,
                    "restore",
                    "--tag",
                    name,
                    "latest",
                    "--target",
                    snapshot_dir,
                ],
                env=new_env,
                stderr=STDOUT,
            )

            proc.communicate()

            # Convert absolute path used by restic to relative path
            # Strip the leading "/"
            relative_directory = project_dir[1:]
            current_dir = os.path.join(snapshot_dir, relative_directory)
            if os.path.exists(current_dir):
                # Copy the src directory to dst directory recursively
                # and overwrite if the file already exists
                proc = subprocess.Popen(["rsync", "-a", current_dir, target_directory])
                proc.communicate()

            # Move additional files
            for additional_file in additional_files:
                proc = subprocess.Popen(
                    [
                        "rsync",
                        "-a",
                        os.path.join(snapshot_dir, additional_file[1:]),
                        target_directory,
                    ]
                )
                proc.communicate()

    def delete(self, name: str, creds: Dict[str, str]) -> None:
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        # Getting restic snapshot ID from snapshot_uuid
        # Need this because we cannot delete snapshot with --tag
        restic_id, _, _ = self.get_restic_info(name, new_env)

        # Need this because if a deletion fails, restic repo will be locked.
        proc = subprocess.Popen(
            [self.snapshot_executable, "-r", self.snapshot_repo, "unlock"],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Actual deletion
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "forget",
                restic_id,
                "--prune",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

    def describe(self, name: str, creds: Dict[str, str]) -> List[Dict[str, str]]:
        new_env = os.environ.copy()
        new_env = {**new_env, **creds}
        new_env["RESTIC_PASSWORD"] = self.password

        restic_id, project_dir, _ = self.get_restic_info(name, new_env)
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "ls",
                restic_id,
                "--recursive",
                project_dir,
                "--json",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

        snapshot_items = []
        for element in output.strip().split(b"\n"):
            snapshot_item = json.loads(element)
            path = snapshot_item.get("path")
            if path == project_dir:
                continue
            if path:
                snapshot_item["path"] = path[len(project_dir) :]
                snapshot_items.append(snapshot_item)

        return snapshot_items

    def get_restic_info(
        self, tag: str, new_env: Dict[str, str]
    ) -> Tuple[str, str, List[str]]:
        # Getting restic snapshot ID from snapshot_uuid
        # Need this because we cannot delete snapshot with --tag
        proc = subprocess.Popen(
            [
                self.snapshot_executable,
                "-r",
                self.snapshot_repo,
                "snapshots",
                "--tag",
                tag,
                "--json",
            ],
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = proc.communicate()
        if proc.returncode != 0:
            print(output, error)

        return parse_restic_snapshots_output(output)


snapshot_runner = SnapshotRunner()


def parse_restic_snapshots_output(output: bytes) -> Tuple[str, str, List[str]]:
    """
    This function takes an ouput from the "restic snapshots" cmd
    and extract restic snapshot id and its project_dir
    """
    snapshots_info = json.loads(output.decode())
    assert snapshots_info and len(snapshots_info) >= 1, "Snapshot not found"
    snapshot_info = snapshots_info[0]
    project_dir_prefix = "project_dir="
    project_dir = ""
    for tag in snapshot_info["tags"]:
        if tag.startswith(project_dir_prefix):
            project_dir = tag[len(project_dir_prefix) :]
    assert (
        len(project_dir) > 0
    ), "Project directory not found. Maybe it's not tagged to the snapshot?"

    output_files = []
    for path in snapshot_info["paths"]:
        if not path.startswith(os.path.abspath(project_dir)):
            output_files.append(path)

    return snapshot_info["short_id"], project_dir, output_files


def copy_file(to_s3: bool, source: str, target: Any, download: bool) -> None:
    """Copy a file.

    The file source or target may be on S3.

    Args:
        to_s3 (bool): If this is True, then copy to/from S3, else the local
            disk. If this is True, then the file source or target will be a
            presigned URL to which GET or POST HTTP requests can be sent.
        source (str or S3 URL): Source file local pathname or S3 GET URL. If
            this is an S3 URL, target is assumed to be a local pathname.
        target (str or S3 URL): Target file local pathname or S3 URL with POST
            credentials. If this is an S3 URL, source is assumed to be a local
            pathname.
        download (bool): If this is True, then this will upload from source to
            target, else this will download.
    """
    try:
        if to_s3:
            if download:
                with open(target, "wb") as f:
                    response = requests.get(source)
                    for block in response.iter_content(1024):
                        f.write(block)
            else:
                with open(source, "rb") as f:
                    files = {"file": ("object", f)}
                    resp = requests.post(
                        target["url"], data=target["fields"], files=files
                    )
                    assert resp.ok, resp.text
        else:
            shutil.copyfile(source, target)
    except (OSError, AssertionError) as e:
        logger.warn("Failed to copy file %s , aborting", source)
        raise e


def create_snapshot(
    project_definition: Any,
    yes: bool,
    description: Optional[str] = None,
    include_output_files: bool = False,
    additional_files: List[str] = [],
    files_only: bool = False,
    tags: List[str] = [],
) -> str:
    """Create a snapshot of a project.

    Args:
        project_definition: Project definition.
        yes: Don't ask for confirmation.
        description: An optional description of the snapshot.
        include_output_files: Whether or not to include output files.
        additional_files: Additional files to include in the snapshot.
        files_only: Only include additional files in the snapshot.
        tags: Tags for the snapshot.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
        Exception: If saving the snapshot files fails.
    """
    # Find and validate the current project ID.
    project_dir = project_definition.root
    project_id = get_project_id(project_dir)

    if include_output_files:
        for output_file in project_definition.config.get("output_files", []):
            if output_file[0] == "/" and not output_file.startswith(project_dir):
                additional_files.append(output_file)

    cluster_config = get_cluster_config(
        os.path.join(project_dir, project_definition.cluster_yaml())
    )

    if "requirements" in project_definition.config.get("environment", {}):
        requirements = get_requirements(
            os.path.join(
                project_dir, project_definition.config["environment"]["requirements"]
            )
        )
    else:
        requirements = ""
    if TEST_V2:
        resp = send_json_request(
            "/api/v2/snapshots/",
            {
                "project_id": project_id,
                "project_config": json.dumps(project_definition.config),
                "cluster_config": json.dumps(cluster_config),
                "requirements": requirements,
                "description": description if description else "",
                "tags": tags,
            },
            method="POST",
        )
        snapshot_uuid: str = resp["result"]["id"]
        creds = resp["result"]["credentials"]
    else:
        resp = send_json_request(
            "snapshot_create",
            {
                "project_id": project_id,
                "project_config": json.dumps(project_definition.config),
                "cluster_config": json.dumps(cluster_config),
                "requirements": requirements,
                "description": description if description else "",
                "tags": tags,
            },
            method="POST",
        )
        snapshot_uuid = resp["uuid"]
        creds = resp["credentials"]

    try:
        snapshot_runner.upload(
            snapshot_uuid, project_dir, additional_files, files_only, creds
        )
    except (OSError, AssertionError) as e:
        # Tell the server to delete the snapshot.
        delete_snapshot(project_dir, snapshot_uuid, True)
        raise e
    return snapshot_uuid


def delete_snapshot(project_dir: str, uuid: str, yes: bool) -> None:
    """Delete the snapshot(s) with the given name.

    Delete the snapshot data from disk and the metadata from the database.

    Args:
        project_dir: Project root directory.
        uuid: The UUID of the snapshot to delete.
        yes: Don't ask for confirmation.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)

    # Get the snapshots with the requested name.
    resp = send_json_request(
        "snapshot_list", {"project_id": project_id, "snapshot_uuid": uuid}
    )
    snapshots = resp["snapshots"]
    if snapshots:
        snapshots_str = "\n".join(snapshot["uuid"] for snapshot in snapshots)
        confirm("Delete snapshots?\n{}".format(snapshots_str), yes)
        snapshot_uuids = [snapshot["uuid"] for snapshot in snapshots]
        if TEST_V2:
            resp = send_json_request(
                "/api/v2/snapshots/{}".format(uuid), {}, method="DELETE"
            )
            resp = resp["result"]
        else:
            resp = send_json_request(
                "snapshot_delete", {"snapshot_uuids": snapshot_uuids}, method="POST"
            )

        assert "credentials" in resp

        snapshot_runner = SnapshotRunner()
        for name in snapshot_uuids:
            snapshot_runner.delete(name, resp["credentials"])

    else:
        logger.warn("No snapshots found with UUID %s", uuid)


def describe_snapshot(uuid: str) -> Any:
    if TEST_V2:
        resp = send_json_request("/api/v2/snapshots/{}".format(uuid), {})
        return resp["result"]
    else:
        return send_json_request("snapshot_describe", {"snapshot_uuid": uuid})


def list_snapshots(project_dir: str) -> List[str]:
    """List all snapshots associated with the given project.

    Args:
        project_dir: Project root directory.

    Returns:
        List of Snapshots for the current project.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("snapshot_list", {"project_id": project_id})
    snapshots = resp["snapshots"]
    return [snapshot["uuid"] for snapshot in snapshots]


def get_snapshot_uuid(project_dir: str, snapshot_uuid: str) -> str:
    """Get a snapshot of the given project with the given name.

    Args:
        project_id: The ID of the project.
        snapshot_name: The name of the snapshot to get. If there are multiple
            snapshots with the same name, then the user will be prompted to
            choose a snapshot.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request(
        "snapshot_list", {"project_id": project_id, "snapshot_uuid": snapshot_uuid}
    )
    snapshots = resp["snapshots"]
    if len(snapshots) == 0:
        raise ValueError("No snapshots found with name {}".format(snapshot_uuid))
    snapshot_idx = 0
    if len(snapshots) > 1:
        print(
            "More than one snapshot found with UUID {}. "
            "Which do you want to use?".format(snapshot_uuid)
        )
        for i, snapshot in enumerate(snapshots):
            print("{}. {}".format(i + 1, snapshot["uuid"]))
        snapshot_idx = click.prompt(
            "Please enter a snapshot number from 1 to {}".format(len(snapshots)),
            type=int,
        )
        snapshot_idx -= 1
        if snapshot_idx < 0 or snapshot_idx > len(snapshots):
            raise ValueError("Snapshot index {} is out of range".format(snapshot_idx))
    result: str = snapshots[snapshot_idx]["uuid"]
    return result


def download_snapshot(
    name: str,
    credentials: Dict[str, str],
    target_directory: Optional[str] = None,
    overwrite: bool = False,
) -> str:
    """Download a snapshot to a local target directory.

    This will recreate the original directory structure of the snapshot. Only
    input files (those found in the project directory during the snapshot
    creation) will be downloaded, not output files specified in the
    project.yaml.

    Args:
        snapshot_info: Information about the snapshot as returned by
            snapshot_get.
        credentials: AWS credentials for accessing S3.
        target_directory: Directory this snapshot gets downloaded to.
            If None, the snapshot will be downloaded to a temporary directory.

    Returns:
        str: The directory where the snapshot has been downloaded to.
    """
    if not target_directory:
        target_directory = os.path.join(os.getcwd(), name)
    target_directory = os.path.abspath(target_directory)
    if os.path.exists(target_directory) and not overwrite:
        print(
            'Target directory already exists. Run with "--overwrite" flag to overwrite the target directory.'
        )
        return ""
    snapshot_runner.download(name, target_directory, credentials)

    return target_directory
