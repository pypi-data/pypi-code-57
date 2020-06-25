"""Component module for CLI.

  Typical usage example:

  component_command = ComponentCommand()
  component_command.run()
"""
from dok8s.cli.commands.kubernetes import KubernetesCommand
from dok8s.lib.analyses import ComponentAnalyser
from dok8s.logger import LOGGER


class ComponentCommand(KubernetesCommand):
    """Initialise component command.

    Example:
        dok8s component -f <json_file>
    """

    def __init__(self):
        super(ComponentCommand, self).__init__()
        self.name = "component"

    @staticmethod
    def analyse(directory: str = "", output: str = "") -> None:
        """Calls the component analysis with the provided kubernetes data.

        Execute analysis, write output.

        Args:
            file: The kubernetes deployment file for the input of the command.
            output: The filename for the output of the command.
        """
        analyser = ComponentAnalyser(directory=directory, output=output)
        LOGGER.debug(f'Use "{analyser.name}" analyser with directory: "{directory}"')
        analyser.analyse()
