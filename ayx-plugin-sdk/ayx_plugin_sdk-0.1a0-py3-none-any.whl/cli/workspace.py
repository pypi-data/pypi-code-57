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
"""Configurations for managing workspace."""
import json
import os
import shutil
import tempfile
import xml.etree.ElementTree as Et
from pathlib import Path
from typing import List, Optional

from ayx_plugin_sdk.cli.environment_helpers import download_pip_packages
from ayx_plugin_sdk.cli.workspace_tool import WorkspaceTool

from pydantic import BaseModel

import typer

import xmltodict


WORKSPACE_CONFIGURATION_FILE_NAME = "ayx_workspace.json"

REQUIREMENTS_FILE_NAME = "requirements.txt"


class Workspace(BaseModel):
    """Class wrapping all workspace configurations and handling basic workspace functions."""

    workspace_dir: Path = Path(".")
    tools: List[WorkspaceTool] = []
    yxi_name: Optional[str] = None
    designer_path: Optional[Path] = None
    tool_family_name: Optional[str] = None
    requirements_tool: Optional[str] = None

    @classmethod
    def setup_workspace_directory(cls, workspace_directory: Path) -> None:
        """Copy the base configs to the tool directory."""
        cls._copy_base_workspace_config(workspace_directory)
        cls._copy_base_requirements_file_to_workspace(workspace_directory)

        workspace = cls(
            workspace_dir=workspace_directory,
            tools=[],
            yxi_name=workspace_directory.resolve().name,
            tool_family_name=workspace_directory.resolve().name,
        )
        workspace._write()

        typer.echo(f"Created workspace directory: {workspace_directory.resolve().name}")

    @classmethod
    def initialize_workspace(cls, workspace_directory: Path) -> "Workspace":
        """Create a Workspace instance wrapping the configurations for the given workspace_directory."""
        workspace_config_path = workspace_directory / WORKSPACE_CONFIGURATION_FILE_NAME
        if not workspace_config_path.exists():
            typer.echo(
                "ERROR: Specified workspace_directory isn't a workspace directory, "
                f"since a {WORKSPACE_CONFIGURATION_FILE_NAME} file doesn't exist."
                "Please use an existing workspace, or specify a directory that doesn't exist yet."
            )
            raise typer.Exit(code=1)

        with open(
            str(workspace_directory / WORKSPACE_CONFIGURATION_FILE_NAME), "r"
        ) as f:
            raw_config = json.loads(f.read())
            workspace = cls(**raw_config)

            workspace.workspace_dir = workspace_directory
            for tool in workspace.tools:
                tool.tool_directory = workspace_directory / tool.name

            workspace._validate_tool_family_in_config_xml()
            return workspace

    def add_tool(self, tool_name: str, example_tool_name: str) -> None:
        """Add a tool the workspace."""
        new_tool_directory = (self.workspace_dir / tool_name).resolve()
        if new_tool_directory.is_dir():
            typer.echo(
                f'ERROR: Failed to create plugin: the plugin "{tool_name}" '
                f"already exists in {new_tool_directory}."
            )
            raise typer.Exit(code=1)

        if not self.requirements_tool:
            self.requirements_tool = tool_name

        self._setup_workspace_tool(tool_name, example_tool_name)

        tool = WorkspaceTool(name=tool_name)
        tool.tool_directory = new_tool_directory
        self.tools.append(tool)
        self._write()

    def delete_tool(self, tool_name: str) -> None:
        """Remove a tool from the workspace."""
        tool_path = self.workspace_dir / tool_name
        shutil.rmtree(tool_path, ignore_errors=True)

        self.tools = [tool for tool in self.tools if tool.name != tool_name]

        if self.requirements_tool == tool_name:
            if self.tools:
                self.requirements_tool = self.tools[0].name
            else:
                self.requirements_tool = None

        self._write()

    def _write(self) -> None:
        """Write the workspace configurations to the workspace directory."""
        self._write_config(
            config_document=self.json(
                exclude={
                    "workspace_dir": ...,
                    "tools": {"__all__": {"ToolDirectory"}},
                },
                indent=2,
            ),
            workspace_directory=self.workspace_dir,
        )

    def _setup_workspace_tool(self, new_tool_name: str, example_tool_name: str) -> None:
        """Copy the example tool files to the tool folder."""
        example_tool_directory = get_install_dir() / "examples" / example_tool_name
        new_tool_directory = self.workspace_dir / new_tool_name

        shutil.copytree(str(example_tool_directory), str(new_tool_directory))

        self._update_config_file(example_tool_name, new_tool_name)
        self._update_main_py(example_tool_name, new_tool_name)

    @staticmethod
    def _write_config(config_document: str, workspace_directory: Path) -> None:
        workspace_config_path = workspace_directory / WORKSPACE_CONFIGURATION_FILE_NAME
        with open(str(workspace_config_path), "w") as workspace_config_file:
            workspace_config_file.write(config_document)

    def _validate_tool_family_in_config_xml(self) -> None:
        """Ensure the workspace Config.xml and sub tools contains the tool family."""
        config_xml_path = self.workspace_dir / "Config.xml"
        self._set_tool_family_attribute(config_xml_path)

        for tool in self.tools:
            tool_config_path = tool.tool_directory / f"{tool.name}Config.xml"
            self._set_tool_family_attribute(tool_config_path)

    def _set_tool_family_attribute(self, config_xml_path: Path) -> None:
        """Set the ToolFamily attribute on a given Config.xml file."""
        if not self.tool_family_name:
            raise ValueError("Tool family name must be set.")

        with open(str(config_xml_path), "r") as config_file:
            tree = Et.parse(config_file)
            root_node = tree.getroot()
            engine_settings = root_node.find("EngineSettings")

            if engine_settings is None:
                raise ValueError("Config XML doesn't contain EngineSettings tag.")

        engine_settings.attrib["ToolFamily"] = self.tool_family_name
        tree.write(str(config_xml_path))

    def _update_config_file(self, example_tool_name: str, new_tool_name: str) -> None:
        old_config_path = (
            self.workspace_dir / new_tool_name / f"{example_tool_name}Config.xml"
        )
        new_config_path = old_config_path.parent / f"{new_tool_name}Config.xml"

        os.rename(str(old_config_path), str(new_config_path))

        with open(str(new_config_path)) as f:
            config = xmltodict.parse(f.read())

        config["AlteryxJavaScriptPlugin"]["Properties"]["MetaInfo"][
            "Name"
        ] = new_tool_name

        with open(str(new_config_path), "w") as f:
            f.write(xmltodict.unparse(config, pretty=True))

    def _update_main_py(self, example_tool_name: str, new_tool_name: str) -> None:
        """Update the name of the tool in the main.py file."""
        main_filepath = self.workspace_dir / new_tool_name / "main.py"
        with open(str(main_filepath), "r") as f:
            content = f.read()

        content = content.replace(example_tool_name, new_tool_name)
        with open(str(main_filepath), "w") as f:
            f.write(content)

    @staticmethod
    def _copy_base_workspace_config(workspace_directory: Path) -> None:
        install_dir = get_install_dir()
        shutil.copytree(
            str(install_dir / "assets" / "base_tool_config"), str(workspace_directory),
        )

    @staticmethod
    def _copy_base_requirements_file_to_workspace(workspace_directory: Path) -> None:
        install_dir = get_install_dir()
        shutil.copy(
            str(install_dir / "examples" / REQUIREMENTS_FILE_NAME),
            str(workspace_directory),
        )

    def build_yxi(
        self,
        destination_dir: Path = Path("."),
        name_override: Optional[str] = None,
        include_dependencies: bool = True,
    ) -> Path:
        """Build a YXI for the workspace."""
        yxi_name = name_override or self.yxi_name

        if not yxi_name:
            raise ValueError("No YXI name specified.")

        if not self.requirements_tool:
            raise ValueError(
                "No requirements tool found. Have you added any tools to your workspace?"
            )

        with tempfile.TemporaryDirectory() as yxi_temp_folder:
            yxi_folder = create_workspace_yxi_folder(
                self.workspace_dir, Path(yxi_temp_folder)
            )

            if include_dependencies:
                temp_tools_requirements_path = yxi_folder / self.requirements_tool
                copy_requirements_to_tool_and_link_wheels(
                    self.workspace_dir,
                    temp_tools_requirements_path,
                    self.requirements_tool,
                )
                tool_requirements_path = self.workspace_dir / REQUIREMENTS_FILE_NAME
                download_pip_packages(
                    yxi_folder / self.requirements_tool / "wheels",
                    tool_requirements_path,
                )

            delete_pycache_directories(yxi_folder)

            shutil.make_archive(yxi_name, "zip", str(yxi_folder))

        archive_path = Path(f"{yxi_name}.zip")
        dest_path = destination_dir / f"{yxi_name}.yxi"
        shutil.move(str(archive_path), str(dest_path))

        return dest_path


def get_install_dir() -> Path:
    """Get the current directory."""
    return Path(__file__).parent.parent


def copy_requirements_to_tool_and_link_wheels(
    source_directory: Path, destination_directory: Path, requirements_tool: str
) -> None:
    """Copy and overwrite requirements.txt file from the source_directory to the destination_directory."""
    tool_requirements_path = destination_directory / REQUIREMENTS_FILE_NAME
    requirements_path = source_directory / REQUIREMENTS_FILE_NAME
    if tool_requirements_path.exists():
        os.remove(str(tool_requirements_path))
    shutil.copy(str(requirements_path), str(tool_requirements_path))
    # because of the special character formatting here, we have to concat.
    user_install_wheels = (
        '--find-links "${APPDATA}/Alteryx/Tools/' + requirements_tool + '/wheels"\n'
    )
    admin_install_wheels = (
        '--find-links "${ALLUSERSPROFILE}/Alteryx/Tools/'
        + requirements_tool
        + '/wheels"\n'
    )
    with tool_requirements_path.open(mode="r") as requirements_file:
        requirements = requirements_file.readlines()
    full_requirements_list = [user_install_wheels, admin_install_wheels] + requirements
    with tool_requirements_path.open(mode="w") as requirements_file:
        requirements_file.writelines(full_requirements_list)


def create_workspace_yxi_folder(
    workspace_directory: Path,
    temp_folder: Path,
    tools_to_exclude: Optional[List[str]] = None,
) -> Path:
    """Create a temporary yxi folder."""
    # The below statement fails with Path(temp_folder) / "tools
    temp_tools_folder = os.path.join(str(temp_folder), "tools")
    shutil.copytree(str(workspace_directory), str(temp_tools_folder))
    if tools_to_exclude is not None:
        for tool in tools_to_exclude:
            shutil.rmtree(Path(temp_tools_folder) / tool)
    return Path(temp_tools_folder)


def delete_pycache_directories(root_dir: Path) -> None:
    """Delete all the pycache subdirectories of a given root."""
    pycache_dirs = [
        Path(root) / directory
        for root, directories, _ in os.walk(str(root_dir))
        for directory in directories
        if directory == "__pycache__"
    ]
    for directory in pycache_dirs:
        shutil.rmtree(str(directory), ignore_errors=True)
