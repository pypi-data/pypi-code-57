# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helper methods for managing virtual environment."""
import os
import shutil
import subprocess
import xml.etree.ElementTree as Et
from pathlib import Path
from typing import List, TYPE_CHECKING

import typer

if TYPE_CHECKING:
    from ayx_plugin_sdk.cli.workspace import Workspace  # noqa: F401

REQUIREMENTS_FILE_NAME = "requirements.txt"


def download_pip_packages(dest_dir: Path, requirements_path: Path) -> None:
    """Download the pip wheels and store in dest_dir."""
    typer.echo(f"Downloading requirements ({requirements_path}) to path ({dest_dir})")
    shutil.rmtree(dest_dir, ignore_errors=True)
    dest_dir.mkdir()

    pip_executable = get_alteryx_path() / "bin" / "Miniconda3" / "Scripts" / "pip.exe"

    commands = [
        str(pip_executable),
        "download",
        "--platform",
        "win_amd64",
        "--no-deps",
        "--index-url",
        "https://artifactory.alteryx.com/artifactory/api/pypi/PyPi/simple",
        "--trusted-host",
        "artifactory.alteryx.com",
        "-r",
        f"{requirements_path}",
        "-d",
        f"{dest_dir}",
    ]

    subprocess.run(commands)


def environment_requires_update(workspace: "Workspace") -> bool:
    """Determine if the virtual environments for the tools should be updated."""
    if not workspace.tool_family_name:
        raise ValueError("Tool family name hasn't been set.")

    if (
        not _virtual_environment_exists(workspace.tool_family_name)
        or workspace.requirements_tool is None
    ):
        return True

    tool_family_requirements_path = (
        Path(_get_alteryx_tools_path())
        / workspace.requirements_tool
        / REQUIREMENTS_FILE_NAME
    )

    if not tool_family_requirements_path.is_file():
        return True

    workspace_requirements = _get_requirements(
        workspace.workspace_dir / REQUIREMENTS_FILE_NAME
    )
    installed_tool_family_requirements = _get_requirements(
        tool_family_requirements_path
    )
    return workspace_requirements != installed_tool_family_requirements


def get_alteryx_path() -> Path:
    """Get the path to Alteryx Designer."""
    user_designer_install_path = Path(os.getenv("LOCALAPPDATA", "")) / "Alteryx"
    user_designer_install_exe = user_designer_install_path / "bin" / "AlteryxGui.exe"
    if user_designer_install_exe.exists():
        return user_designer_install_path

    admin_designer_install_path = Path(os.getenv("PROGRAMFILES", "")) / "Alteryx"
    admin_designer_install_exe = admin_designer_install_path / "bin" / "AlteryxGui.exe"
    if admin_designer_install_exe.exists():
        return admin_designer_install_path

    raise FileNotFoundError("Alteryx Install Path could not be located.")


def get_tool_family_attribute_from_config(config_xml_path: Path) -> str:
    """Get the ToolFamily attribute from the Config.xml file."""
    with open(str(config_xml_path), "r") as config_file:
        tree = Et.parse(config_file)
        root_node = tree.getroot()
        engine_settings = root_node.find("EngineSettings")
        if engine_settings is None:
            raise ValueError("Config xml doesn't contain engine settings.")

        tool_family = str(engine_settings.attrib["ToolFamily"])
        return tool_family


def _get_alteryx_tools_path() -> Path:
    """Get the path to the Alteryx Tools folder (for 3P plugins)."""
    user_install_path = Path(os.getenv("APPDATA", "")) / "Alteryx" / "Tools"
    if user_install_path.exists():
        return user_install_path

    admin_install_path = (
        Path(os.getenv("PROGRAMFILES", "")) / "Alteryx" / "bin" / "HtmlPlugins"
    )
    if admin_install_path.exists():
        return admin_install_path

    raise FileNotFoundError("Alteryx Tools Path could not be located.")


def _get_requirements(requirements_path: Path) -> List[str]:
    """Get the workspace level requirements file."""
    with open(str(requirements_path), "r") as req_file:
        requirements = req_file.readlines()

    return [line for line in requirements if "--find-links" not in line]


def _virtual_environment_exists(tool_family_name: str) -> bool:
    """Check if the virtual environment exists."""
    venv_name = f"{tool_family_name}_venv"
    designer_venv_path = Path(_get_alteryx_tools_path()) / venv_name
    if not designer_venv_path.is_dir():
        typer.echo(
            f"{venv_name} does not exist. Creating Anaconda Environment in {designer_venv_path}"
        )
        return False
    return True
