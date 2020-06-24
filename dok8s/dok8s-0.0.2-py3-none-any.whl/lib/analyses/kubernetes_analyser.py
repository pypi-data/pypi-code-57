"""kubernetes_analyser
"""
import traceback
from operator import attrgetter
from pathlib import Path
from typing import List

import yaml

from dok8s.lib.base_analyser import BaseAnalyser
from dok8s.lib.helpers.component_loader import identify_kubernetes_object
from dok8s.logger import LOGGER


class KubernetesAnalyser(BaseAnalyser):
    """KubernetesAnalyser
    """

    def __init__(self, directory: str = "", output: str = ""):
        super(KubernetesAnalyser, self).__init__()
        self.name = "kubernetes-analysis"
        self.directory = directory
        self.output = output
        self._parsed_data = []
        self._tabular_data = ""

    @property
    def parsed_data(self) -> List:
        """Getter for parsed data attribute.

        Returns:
            The value of the parsed data attribute.
        """
        return self._parsed_data

    @parsed_data.setter
    def parsed_data(self, value: List) -> None:
        """Setter for parsed data attribute.

        Args:
            value: The value to set the parsed data attribute.
        """
        self._parsed_data = value

    def _parse_yaml_files(self):
        """_parse_yaml_files
        """
        documents = []
        yaml_files = list(Path(self.directory).glob("**/*.yaml"))

        for yaml_file in yaml_files:
            with open(yaml_file, "r") as stream:
                try:
                    documents.extend(yaml.safe_load_all(stream))
                except yaml.YAMLError as error:
                    track = traceback.format_exc()
                    LOGGER.error(error)
                    LOGGER.debug(track)

        LOGGER.debug(f"YAML Documents: {len(documents)}")
        return documents

    def _parse_data(self):
        """_parse_data
        """
        all_data = self._parse_yaml_files()
        all_objects = []
        for data in all_data:
            obj = identify_kubernetes_object(data)
            if obj:
                all_objects.append(obj)

        all_objects = sorted(all_objects, key=attrgetter("kind", "metadata.name"))
        return all_objects
