"""Docker module for CLI.

  Typical usage example:

  docker_command = DockerCommand()
  docker_command.run()
"""
from dok8s.cli.commands.kubernetes import KubernetesCommand
from dok8s.lib.analyses import DockerAnalyser
from dok8s.logger import LOGGER


class DockerCommand(KubernetesCommand):
    """Initialise docker command.

    Example:
        dok8s docker -f <json_file>
    """

    def __init__(self):
        super(DockerCommand, self).__init__()
        self.name = "docker"

    @staticmethod
    def analyse(directory: str = "", output: str = "") -> None:
        """Calls the docker analysis with the provided kubernetes data.

        Execute analysis, write output.

        Args:
            file: The kubernetes deployment file for the input of the command.
            output: The filename for the output of the command.
        """
        analyser = DockerAnalyser(directory=directory, output=output)
        LOGGER.debug(f'Use "{analyser.name}" analyser with directory: "{directory}"')
        analyser.analyse()
