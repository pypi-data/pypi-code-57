import os
import logging
import subprocess
import shlex
import json
import argparse

import tqdm

module_logger = logging.getLogger(__name__)


def ffmpeg_loudnorm(
    input_file_path: str,
    output_file_path: str = None,
    output_dir: str = None,
    overwrite: bool = True
) -> str:
    timeout = 3 * 60

    if not os.path.exists(input_file_path):
        raise RuntimeError(f"{input_file_path} doesn't exist")

    module_logger.debug((f"ffpmeg_loudnorm: input_file_path={input_file_path}, "
                         f"output_file_path={output_file_path}, "
                         f"overwrite={overwrite}"))

    if output_file_path is None:
        splitted = os.path.splitext(input_file_path)
        output_file_path = splitted[0] + ".loudnorm" + splitted[1]
        if output_dir is not None and os.path.exists(output_dir):
            output_file_name = os.path.basename(output_file_path)
            output_file_path = os.path.join(output_dir, output_file_name)

    if not overwrite and os.path.exists(output_file_path):
        raise RuntimeError((f"ffmpeg_loudnorm: {output_file_path} already exists. "
                            "Try setting overwrite to `True`"))

    cmd0_str = "ffmpeg -i \"{}\" -af loudnorm=print_format=json -f null /dev/null".format(input_file_path)
    module_logger.debug("ffmpeg_loudnorm: issuing command {}".format(cmd0_str))
    cmd0 = shlex.split(cmd0_str)
    process = subprocess.run(
        cmd0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if process.returncode != 0:
        module_logger.error((f"ffpmeg_loudnorm: Error when calling ffmpeg, "
                             f"exited with code {process.returncode}"))
        raise RuntimeError(process.stderr)

    stderr_str = process.stderr.decode("utf-8")
    idx = stderr_str.find("Parsed_loudnorm")
    json_begin_idx = stderr_str[idx:].find("{")
    json_output = json.loads(stderr_str[idx:][json_begin_idx:])
    module_logger.debug(f"ffmpeg_loudnorm: json_output={json_output}")

    measured_I = json_output["input_i"]
    measured_LRA = json_output["input_lra"]
    measured_TP = json_output["input_tp"]
    measured_thresh = json_output["input_thresh"]
    # the following is taken from [here](https://superuser.com/questions/1312811/ffmpeg-loudnorm-2pass-in-single-line)

    cmd1_str = (f"ffmpeg -y -i \"{input_file_path}\" -af "
                f"loudnorm=linear=true:"
                f"measured_I={measured_I}:measured_LRA={measured_LRA}:"
                f"measured_TP={measured_TP}:measured_thresh={measured_thresh} "
                f"\"{output_file_path}\"")
    module_logger.debug("ffmpeg_loudnorm: issuing command {}".format(cmd1_str))

    cmd1 = shlex.split(cmd1_str)
    process = subprocess.run(
        cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

    if process.returncode != 0 or not os.path.exists(output_file_path):
        module_logger.error(("ffmpeg_loudnorm: Error when calling ffmpeg, "
                             f"exited with code {process.returncode}"))
        raise RuntimeError(process.stderr)

    return output_file_path


def create_parser():
    parser = argparse.ArgumentParser(description="Apply ffmpeg two pass loudnorm volume normalization")
    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files to normalize")
    parser.add_argument("-d", "--outdir", action="store", dest="output_dir",
                        help="Put output files in this directory. Only used if output-file-paths option is not provided.")
    parser.add_argument("-o", "--output-file-paths", type=str, nargs="+",
                        help="Output file paths, in order of input file paths.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite output file if it exists")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    return parser


def main():
    parser = create_parser()
    parsed = parser.parse_args()

    log_level = logging.INFO
    if parsed.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    input_file_paths = parsed.file_paths
    output_file_paths = parsed.output_file_paths
    output_dir = parsed.output_dir
    overwrite = parsed.force

    def progress(iterable):
        if not parsed.verbose:
            return tqdm.tqdm(iterable)
        else:
            return iterable

    for idx in progress(range(len(input_file_paths))):
        input_file_path = input_file_paths[idx]
        if output_file_paths is not None:
            ffmpeg_loudnorm(
                input_file_path,
                output_file_path=output_file_paths[idx],
                overwrite=overwrite)
        else:
            ffmpeg_loudnorm(
                input_file_path,
                output_dir=output_dir,
                overwrite=overwrite)


if __name__ == "__main__":
    main()
