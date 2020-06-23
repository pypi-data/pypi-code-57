"""Component module for Analyses.

  Typical usage example:

  component_analyser = ComponentAnalyser(directory=directory, output=output)
  component_analyser.analyse()
"""
import traceback
from operator import attrgetter
from pathlib import Path

import yaml
from tabulate import tabulate

from dok8s.lib.base_analyser import BaseAnalyser
from dok8s.lib.helpers.component_loader import (
    generate_component_output,
    identify_kubernetes_object,
)
from dok8s.logger import LOGGER
from dok8s.settings import BIN_DIR


class ComponentAnalyser(BaseAnalyser):
    """
    Initialise component analyser.
    """

    def __init__(self, directory: str = "", output: str = ""):
        super(ComponentAnalyser, self).__init__()
        self.name = "component-analysis"
        self.directory = directory
        self.output = output
        self._parsed_data = []
        self._tabular_data = ""

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

    def _construct_table(self):
        """_construct_table
        """
        if not self._parsed_data:
            return ""

        headers = ["Component", "Value", "Details"]
        table = []
        for obj in self._parsed_data:
            table.append(generate_component_output(obj))
        return tabulate(table, headers, tablefmt="pipe")

    def analyse(self):
        """analyse
        """
        self._parsed_data = self._parse_data()
        self._tabular_data = self._construct_table()

        filepath = Path(~BIN_DIR) / (self.output)
        with open(filepath, "w") as file_handler:
            file_handler.write(self._tabular_data)
