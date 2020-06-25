from pathlib import Path
from typing import List, Union

import forge_template.paths as file_paths
import forge_template.util.file_util as file_util
import forge_template.util.log_util as log_util
from forge_template.handler.handler import BaseHandler
from forge_template.tool_info import ToolInfo

GITHUB_ACTION_HANDLER_NAME = "github_actions"


class GithubActionsHandler(BaseHandler):
    def __init__(self, tool_info: ToolInfo) -> None:
        self._tool = tool_info.name

        self._output_paths = [file_paths.SCRIPT_OUTPUT_DIR, file_paths.WORKFLOW_OUTPUT_DIR]
        self._output_paths_to_create: List[Path] = []
        self._output_paths_created: List[Path] = []

        self._files_to_add: List[Union[Path, None]] = [
            tool_info.github_actions_script_path,
            tool_info.github_actions_template_path,
        ]  # type: ignore
        self._files_added: List[Path] = []

        super().__init__(config={}, tool_info=tool_info)

    def create_preview(self) -> None:
        self._output_paths_to_create = [path for path in self._output_paths if not path.exists()]

    def print_preview(self) -> None:
        log_util.print_resource_to_add(list(map(str, self._output_paths_to_create)), "Directory")
        log_util.print_resource_to_add(list(map(str, map(lambda x: Path(str(x)).name, self._files_to_add))), "File")

    def setup(self) -> None:
        self._create_paths(self._output_paths_to_create)
        for path, folder in zip(self._files_to_add, self._output_paths):
            self._copy_file(Path(str(path)), folder)

    def rollback(self) -> None:
        if self._files_added:
            log_util.print_rollback("Files")
            self._delete_paths(self._files_added)

    def delete_all_resources(self):
        self._delete_paths(self._output_paths)

    def _copy_file(self, path: Path, destination_folder: Path) -> None:
        file_util.copy_file(path, destination_folder)
        self._files_added.append(destination_folder / path.name)
        log_util.print_success_added(destination_folder, "Directory", path.name, "File")

    @staticmethod
    def _create_paths(paths: List[Path]) -> None:
        for path in paths:
            file_util.create_directory(path, exist_ok=True, parents=True)
            log_util.print_success_created(path.name, "Directory")

    @staticmethod
    def _delete_paths(paths: List[Path]) -> None:
        for path in paths:
            if path.exists():
                file_util.delete_path(path)
                log_util.print_success_deleted(path, "Directory/File")
