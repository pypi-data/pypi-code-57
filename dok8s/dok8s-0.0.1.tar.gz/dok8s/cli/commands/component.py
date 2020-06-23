"""Component module for CLI.

  Typical usage example:

  component_command = ComponentCommand()
  component_command.run()
"""
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path
from timeit import default_timer

from dok8s.cli.base_command import BaseCommand
from dok8s.lib.analyses import ComponentAnalyser
from dok8s.logger import LOGGER


class ComponentCommand(BaseCommand):
    """Initialise component command.

    Example:
        dok8s component -f <json_file>
    """

    def __init__(self):
        super(ComponentCommand, self).__init__()
        self.name = "component"

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-d",
            "--directory",
            required=True,
            help="The directory of the Helm generated Chart template files of the deployment",
        )

        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=time.strftime("%Y%m%d-%H%M%S"),
            help="The filename to use as the output file",
        )

    def validate_args(self, args: Namespace) -> None:
        """Check command given argument, template.

        Requires a non-empty directory with valid YAML files.

        Raises:
            Exception: If template directory does not exist.
            Exception: If template directory does not include any YAML files.
        """
        path = Path(args.directory)
        if not path.exists():
            raise Exception(f'File "{args.directory}" does not exists!')

        yaml_files = list(Path(args.directory).glob("**/*.yaml"))
        if len(yaml_files) == 0:
            raise Exception(
                f'No YAML files found in template directory "{args.directory}"'
            )

        LOGGER.debug(f"YAML files found: {len(yaml_files)}")

    def execute(self, args: Namespace) -> None:
        start_time = default_timer()
        self.analyse(args.directory, args.output)
        elapsed_time = default_timer() - start_time
        LOGGER.debug(f'Command "{self.name}" took {elapsed_time:.2f} seconds.')

    @staticmethod
    def analyse(directory: str = "", output: str = "") -> None:
        """Calls the component analysis with the provided kubernetes data.

        Execute analysis, write output.

        Args:
            file: The kubernetes deployment file for the input of the command.
            output: The filename for the output of the command.
        """
        analyser = ComponentAnalyser(directory=directory, output=output)
        LOGGER.debug(f'Use "{analyser.name}" crawler with directory: "{directory}"')
        analyser.analyse()
