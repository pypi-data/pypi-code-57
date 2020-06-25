import os
from typing import Any, Optional

from overrides import overrides

from .config import Config


class ConfigWithSaving(Config):
    def __init__(self, saving_folder_prefix: str, logs_dir: str, **kwargs: Any) -> None:
        super().__init__(logs_dir=logs_dir)
        self._saving_folder_prefix = saving_folder_prefix
        self._saving_folder: Optional[str] = None

    @property
    def saving_folder(self) -> str:
        if self._saving_folder is not None:
            return self._saving_folder
        raise ValueError("Saving folder was not set!")

    @overrides  # type: ignore
    def set_attributes_from_path(self, config_path: str) -> None:
        super().set_attributes_from_path(config_path)
        assert self._path_suffix is not None, "You should set path_suffix before creating a folder."
        self._saving_folder = os.path.join(self._saving_folder_prefix, self._path_suffix)
        if not os.path.exists(self.saving_folder):
            os.makedirs(self.saving_folder)
