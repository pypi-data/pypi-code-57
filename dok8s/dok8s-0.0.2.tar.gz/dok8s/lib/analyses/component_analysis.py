"""Component module for Analyses.

  Typical usage example:

  component_analyser = ComponentAnalyser(directory=directory, output=output)
  component_analyser.analyse()
"""
from pathlib import Path

from tabulate import tabulate

from dok8s.lib.analyses.kubernetes_analyser import KubernetesAnalyser
from dok8s.lib.helpers.component_loader import generate_component_output
from dok8s.settings import BIN_DIR


class ComponentAnalyser(KubernetesAnalyser):
    """
    Initialise component analyser.
    """

    def __init__(self, directory: str = "", output: str = ""):
        super(ComponentAnalyser, self).__init__()
        self.name = "component-analysis"
        self.directory = directory
        self.output = output
        self.parsed_data = []
        self.tabular_data = ""

    def _construct_table(self):
        """_construct_table
        """
        if not self.parsed_data:
            return ""

        headers = ["Component", "Value", "Details"]
        table = []
        for obj in self.parsed_data:
            output = generate_component_output(obj)
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
