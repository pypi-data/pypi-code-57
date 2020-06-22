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
"""Wrappers to handle interactions with yxi installer."""
import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Optional

from ayx_plugin_sdk.cli.environment_helpers import get_alteryx_path


class YxiInstallTypes(str, Enum):
    """YXI Executable Install Types."""

    User = "User"
    Admin = "Admin"
    Alteryx = "Alteryx"


class YxiCommands(str, Enum):
    """YXI Executable commands."""

    Install = "install-yxis"
    Uninstall = "uninstall-yxis"


class YxiLauncher:
    """Class wrapping install/uninstall commands from the yxi installer executable."""

    def __init__(
        self,
        yxi_paths: List[Path],
        alteryx_path: Optional[Path] = None,
        clean: bool = False,
        update_conda: bool = False,
        install_type: Optional[YxiInstallTypes] = None,
    ) -> None:
        if len(yxi_paths) < 1:
            raise ValueError("At least one yxi path is required for the yxi installer.")
        self.yxi_paths = yxi_paths
        self.alteryx_path: Path = alteryx_path or get_alteryx_path()
        self.clean = clean
        self.update_virtual_env = update_conda
        self.install_type: YxiInstallTypes = install_type or YxiLauncher.get_static_install_type()

    @staticmethod
    def get_executable_path() -> Path:
        """Get the path to the yxi installer excutable."""
        curr_dir = Path(__file__).parent.parent.resolve()
        return curr_dir / "assets" / "executables" / "yxi-installer.exe"

    @staticmethod
    def get_static_install_type() -> YxiInstallTypes:
        """Get the install type for the yxi."""
        return YxiInstallTypes.User

    def execute_install_command(self) -> None:
        """Execute the install yxi command from the yxi installer executable."""
        run_command = [
            str(self.get_executable_path()),  # executable to run
            YxiCommands.Install,  # yxi-installer installer command
            self._get_yxi_paths(),  # string space separated list of yxis (Req argument)
            "--alteryx-path",  # Path to Alteryx tools
            str(self.alteryx_path),
            self._get_clean_flag(),
            self._get_update_env_flag(),
            "--quiet",
            "--install-type",
            self.install_type,
        ]
        subprocess.run(run_command, stdout=subprocess.PIPE)

    def execute_uninstall_command(self) -> None:
        """Run the uninstall command from the yxi installer."""
        uninstall_command = [
            str(self.get_executable_path()),
            YxiCommands.Uninstall,
            self._get_yxi_paths(),
            str(self.alteryx_path),
            "--quiet",
        ]
        subprocess.run(uninstall_command, stdout=subprocess.PIPE, shell=True)

    def _get_clean_flag(self) -> str:
        """Get the flag for cleaning the previous install."""
        if self.clean:
            return "--uninstall-previous"
        else:
            return "--keep-previous"

    def _get_update_env_flag(self) -> str:
        """Get the flag for updating anaconda environments."""
        if self.update_virtual_env:
            return "--install-anaconda"
        else:
            return "--skip-anaconda"

    def _get_yxi_paths(self) -> str:
        """Get the paths to the yxis as a cli string."""
        if not self.yxi_paths:
            raise ValueError("At least one yxi path is required for the yxi installer.")

        return " ".join([str(path) for path in self.yxi_paths])
