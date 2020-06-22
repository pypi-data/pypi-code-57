import os
import logging
import datetime


from ..conversion import convert_to_wav
from ..metadata import BDSMetaDataType


module_logger = logging.getLogger(__name__)

def _get_formatted_output_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    endpoint = os.path.basename(output_dir)
    if "%" in endpoint:
        module_logger.debug(f"_get_formatted_output_dir: detected datetime output dir")
        now = datetime.datetime.now()
        endpoint = now.strftime(endpoint)
        module_logger.debug(f"_get_formatted_output_dir: endpoint={endpoint}")
    output_dir = os.path.join(output_dir_dir, endpoint)
    return output_dir


def _get_most_recent_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    module_logger.debug(f"_get_most_recent_dir: "
                        f"output_dir parent dir {output_dir_dir}")
    sub_dirs = []
    for path in os.listdir(output_dir_dir):
        path = os.path.join(output_dir_dir, path)
        if os.path.isdir(path):
            sub_dirs.append([os.path.getmtime(path), path])

    sorted_sub_dirs = sorted(sub_dirs, key=lambda val: val[0])
    most_recent = sorted_sub_dirs[-1][1]
    module_logger.debug((f"_get_most_recent_dir: most recently "
                         f"modified dir in parent dir {most_recent}"))

    return most_recent


def convert(
    file_path: str,
    output_dir: str = None,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Convert mp3 files to wav.

    Args:
        file_path: Input .mp3 file path
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    output_file_path = None
    if output_dir is not None:
        if dry_run:
            output_dir = _get_most_recent_dir(output_dir)
        else:
            output_dir = _get_formatted_output_dir(output_dir)
            if not os.path.exists(output_dir):
                module_logger.debug(f"convert: {output_dir} didn't exist; creating")
                os.makedirs(output_dir)
        file_name = os.path.basename(file_path)
        output_file_path = os.path.splitext(os.path.join(output_dir, file_name))[0] + ".wav"

    if not dry_run:
        if file_path.endswith(".mp3"):
            output_file_path = convert_to_wav(file_path, output_file_path=output_file_path)
        elif file_path.endswith(".wav"):
            output_file_path = file_path

    return output_file_path
