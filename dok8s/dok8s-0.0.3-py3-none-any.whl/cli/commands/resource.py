"""Resource module for CLI.

  Typical usage example:

  resource_command = ResourceCommand()
  resource_command.run()
"""
from dok8s.cli.commands.kubernetes import KubernetesCommand
from dok8s.lib.analyses import ResourceAnalyser
from dok8s.logger import LOGGER


class ResourceCommand(KubernetesCommand):
    """Initialise resource command.

    Example:
        dok8s resource -f <json_file>
    """

    def __init__(self):
        super(ResourceCommand, self).__init__()
        self.name = "resource"

    @staticmethod
    def analyse(directory: str = "", output: str = "") -> None:
        """Calls the resource analysis with the provided kubernetes data.

        Execute analysis, write output.

        Args:
            file: The kubernetes deployment file for the input of the command.
            output: The filename for the output of the command.
        """
        analyser = ResourceAnalyser(directory=directory, output=output)
        LOGGER.debug(f'Use "{analyser.name}" analyser with directory: "{directory}"')
        analyser.analyse()
