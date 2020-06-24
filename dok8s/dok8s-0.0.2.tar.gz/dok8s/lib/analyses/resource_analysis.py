"""Resource module for Analyses.

  Typical usage example:

  resource_analyser = ResourceAnalyser(directory=directory, output=output)
  resource_analyser.analyse()
"""
from pathlib import Path

from tabulate import tabulate

from dok8s.lib.analyses.kubernetes_analyser import KubernetesAnalyser
from dok8s.lib.helpers.component_loader import generate_resource_output
from dok8s.settings import BIN_DIR


class ResourceAnalyser(KubernetesAnalyser):
    """
    Initialise resource analyser.
    """

    def __init__(self, directory: str = "", output: str = ""):
        super(ResourceAnalyser, self).__init__()
        self.name = "resource-analysis"
        self.directory = directory
        self.output = output
        self.parsed_data = []
        self.tabular_data = ""

    def _construct_table(self):
        """_construct_table
        """
        if not self.parsed_data:
            return ""

        headers = ["Platform/Service", "Name", "Request", "Limit Request", "Notes"]
        table = []
        for obj in self.parsed_data:
            output = generate_resource_output(obj)
            if output:
                table.append(output)
        return tabulate(table, headers, tablefmt="pipe")

    def analyse(self):
        """analyse
        """
        self.parsed_data = self._parse_data()
        self.tabular_data = self._construct_table()

        filepath = Path(~BIN_DIR) / (self.output)
        with open(filepath, "w") as file_handler:
            file_handler.write(self.tabular_data)
