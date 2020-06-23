import logging
import shlex
import subprocess
import os

from ..metadata import BDSMetaDataType

module_logger = logging.getLogger(__name__)


def primitive(
    file_path: str,
    primitive_args: str = "-n 30",
    primitive_exec: str = "primitive",
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Call `primitive` command on some input file. Return the path to the output SVG
    `primitive` command must be on the PATH for this to work correctly.

    Args:
        file_path: Input file path
        primitive_args: Additional arguments to pass to `primitive`. Must at minimum contain `-n <int>`
        primitive_exec: Path to primitive executable
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    if "-n" not in primitive_args:
        raise RuntimeError(
            "primitive: Need to specify number of shapes (\"-n\") when calling primitive executable")

    output_file_path = "{}.svg".format(os.path.splitext(file_path)[0])

    if not dry_run:
        cmd_str = "{} -i \"{}\" -o \"{}\" {}".format(
            primitive_exec, file_path, output_file_path, primitive_args)
        module_logger.debug("primitive: Running command {}".format(cmd_str))
        cmd = shlex.split(cmd_str)
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        if proc.returncode == 0:
            return output_file_path
        else:
            module_logger.error("primitive: stdout={}".format(proc.stdout))
            module_logger.error("primitive: stderr={}".format(proc.stderr))
            raise RuntimeError(
                "primitive exited with code={}".format(proc.returncode))
    else:
        return output_file_path
