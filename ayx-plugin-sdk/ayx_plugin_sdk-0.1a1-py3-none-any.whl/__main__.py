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
"""Alteryx Python SDK - Main program."""
import importlib.util
import json
import os
import tempfile
from enum import Enum
from pathlib import Path
from typing import Any

from ayx_plugin_sdk.cli.environment_helpers import environment_requires_update
from ayx_plugin_sdk.cli.workspace import Workspace
from ayx_plugin_sdk.cli.yxi_launcher import YxiLauncher
from ayx_plugin_sdk.providers.file_provider.file_provider import FileProvider
from ayx_plugin_sdk.providers.file_provider.tool_input import ToolInput

import typer

app = typer.Typer(
    help="Run a tool using file inputs and outputs in a pure Python environment."
)


class TemplateToolTypes(str, Enum):
    """Installation Type of Designer."""

    Input = "input"
    MultipleInputs = "multiple-inputs"
    MultipleOutputs = "multiple-outputs"
    Optional = "optional"
    Output = "output"
    Passthrough = "passthrough"
    MultipleInputConnections = "multianchor"
    Doubler = "doubler"


name_to_tool = {
    TemplateToolTypes.Input: "AyxSdkInput",
    TemplateToolTypes.MultipleInputs: "AyxSdkMultipleInputAnchors",
    TemplateToolTypes.MultipleOutputs: "AyxSdkMultiConnectionsMultiOutputAnchor",
    TemplateToolTypes.Optional: "AyxSdkOptionalInputAnchor",
    TemplateToolTypes.Output: "Output",
    TemplateToolTypes.Passthrough: "PassThrough",
    TemplateToolTypes.MultipleInputConnections: "AyxSdkMultiConnectionsMultiOutputAnchor",
    TemplateToolTypes.Doubler: "Doubler",
}

DEFAULT_YXI_NAME = "package"
INSTALL_YXI_FUNCTION = "install-yxis"
ALTERYX_PATH_PARAMETER = "--alteryx-path"
UNINSTALL_PREVIOUS_FLAG = "--uninstall-previous"
KEEP_PREVIOUS_FLAG = "--keep-previous"
SKIP_ANACONDA_FLAG = "--skip-anaconda"
INSTALL_ANACONDA_FLAG = "--install-anaconda"

# This is a workaround for unit tests
USER_INSTALL_TYPE = "User"


@app.command()
def run(
    tool: str = typer.Option(
        ...,
        help="JSON file that specifies the input and output information needed for the file provider to run",
    ),
) -> None:
    """
    Run a tool using file inputs and outputs in a pure Python environment.

    Parameters
    ----------
    tool
        Specifies the path to the JSON file that contains the tool plugin, configuration files, input files, and output files.
    """
    try:
        with open(tool) as fd:
            json_dict = json.load(fd)
    except FileNotFoundError:
        raise RuntimeError(f"Couldn't find tool information file {tool}.")

    tool_input = ToolInput(**json_dict)
    tool_classname = tool_input.tool.plugin
    tool_path = Path(tool_input.tool.path)

    file_provider = FileProvider(
        tool_input.tool_config,
        tool_input.workflow_config,
        inputs=tool_input.inputs or [],
        outputs=tool_input.outputs or [],
        update_tool_config=tool_input.update_tool_config,
    )

    tool_class = _load_user_plugin_class(tool_classname, tool_path)

    # Initialize and run the plugin
    plugin = tool_class(file_provider)
    for input_anchor in file_provider.input_anchors:
        for input_anchor_connection in input_anchor.connections:
            plugin.on_input_connection_opened(input_anchor_connection)
            # TODO Support multiple calls to on_record_packet
            plugin.on_record_packet(input_anchor_connection)
    plugin.on_complete()


def _load_user_plugin_class(tool_classname: str, tool_path: Path) -> Any:
    """Load the plugin and get a reference to its class."""
    root = Path(__file__).resolve().parent
    tool_full_path = root / tool_path
    os.chdir(tool_full_path)
    spec: Any = importlib.util.spec_from_file_location("main", "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, tool_classname)


@app.command()
def create_ayx_plugin(
    name: str = typer.Option(
        ..., prompt="Tool Name", help="Name of the tool to create."
    ),
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to put this tool in. "
        "Workspace directory will be created if it doesn't exist.",
    ),
    tool_type: TemplateToolTypes = typer.Option(
        ...,
        prompt="Tool type",
        help=f"The type of tool to create. Must be one of: {', '.join(name_to_tool.keys())}",
    ),
) -> None:
    """Create a new plugin plugin for Alteryx Designer."""
    typer.echo("Creating Alteryx Plugin...")

    example_tool_name = name_to_tool[tool_type]

    if not workspace_directory.is_dir():
        Workspace.setup_workspace_directory(workspace_directory)

    workspace = Workspace.initialize_workspace(workspace_directory)
    workspace.add_tool(name, example_tool_name)

    typer.echo(f"Created new tool in directory: {workspace.tools[-1].tool_directory}")


@app.command()
def delete_ayx_plugin(
    name: str = typer.Option(
        ..., prompt="Tool Name", help="Name of the tool to delete."
    ),
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to delete this tool from. ",
    ),
) -> None:
    """Delete the Alteryx Plugin Tool in the workspace."""
    workspace = Workspace.initialize_workspace(workspace_directory)

    if name not in [tool.name for tool in workspace.tools]:
        typer.echo(f"ERROR: No tool folder found for {name}")
        raise typer.Exit(code=1)

    typer.echo(f"Deleting Plugin: {name}")
    workspace.delete_tool(name)
    typer.echo(f"Tool successfully deleted.")


@app.command()
def create_yxi(
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to package into a YXI.",
    ),
) -> None:
    """Create a YXI from a tools directory."""
    typer.echo("Creating YXI...")

    workspace = Workspace.initialize_workspace(workspace_directory)

    typer.echo(f"Creating yxi file: {workspace.yxi_name}")
    yxi_path = workspace.build_yxi()
    typer.echo(f"\n Created YXI file at: {yxi_path.resolve()}")


@app.command()
def designer_build(
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to install into Designer.",
    ),
    force: bool = typer.Option(
        False, help="Skip installation of Anaconda environment."
    ),
    clean: bool = typer.Option(default=False, help="Remove previous install."),
) -> None:
    """Build the tools into designer."""
    typer.echo("Building tools into Alteryx Designer...")

    workspace = Workspace.initialize_workspace(workspace_directory)

    if not workspace.tools:
        typer.echo("ERROR: No tools to build.")
        raise typer.Exit(code=1)

    if force:
        typer.echo("Force updating anaconda.")
        update_venv = True
    else:
        update_venv = environment_requires_update(workspace)
        if update_venv:
            typer.echo(
                "Virtual Environment has changed. Updating Anaconda environments."
            )
        else:
            typer.echo("Anaconda environments are up to date.")

    with tempfile.TemporaryDirectory() as temporary_yxi_directory:
        yxi_path = workspace.build_yxi(
            Path(temporary_yxi_directory), include_dependencies=update_venv
        )
        yxi_launcher = YxiLauncher(
            [yxi_path],
            clean=clean,
            update_conda=update_venv,
            alteryx_path=workspace.designer_path,
        )
        yxi_launcher.execute_install_command()


@app.command()
def docs() -> None:
    """Open the ayx-plugin-sdk documentation in a browser."""
    import webbrowser

    docs_index_html = Path(os.path.dirname(__file__)) / "docs" / "index.html"
    webbrowser.open(str(docs_index_html), new=2)


def main() -> None:
    """Define the main Entry point to typer."""
    app()


if __name__ == "__main__":
    main()
