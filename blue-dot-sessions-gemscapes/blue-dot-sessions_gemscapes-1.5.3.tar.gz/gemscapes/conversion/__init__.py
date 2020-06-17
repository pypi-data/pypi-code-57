import logging
import json
import typing
import sys
import signal
import os
import shlex
import subprocess

module_logger = logging.getLogger(__name__)

from ..exceptions import AudioProcessingException


__all__ = [
    "stereofy_and_find_info",
    "convert_to_mp3",
    "convert_to_ogg",
    "convert_using_ffmpeg",
    "convert_to_pcm",
    "convert_to_wav"
]


def stereofy_and_find_info(stereofy_executble_path, input_filename, output_filename):
    """
    converts a pcm wave file to two channel, 16 bit integer
    """

    if not os.path.exists(input_filename):
        raise AudioProcessingException("file %s does not exist" % input_filename)

    cmd = [stereofy_executble_path, "--input", input_filename, "--output", output_filename]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()

    if process.returncode != 0 or not os.path.exists(output_filename):
        if "No space left on device" in stderr + " " + stdout:
            raise NoSpaceLeftException
        raise AudioProcessingException("failed calling stereofy data:\n" + " ".join(cmd) + "\n" + stderr + "\n" + stdout)

    stdout = (stdout + " " + stderr).replace("\n", " ")

    duration = 0
    m = re.match(r".*#duration (?P<duration>[\d\.]+).*",  stdout)
    if m != None:
        duration = float(m.group("duration"))

    channels = 0
    m = re.match(r".*#channels (?P<channels>\d+).*", stdout)
    if m != None:
        channels = float(m.group("channels"))

    samplerate = 0
    m = re.match(r".*#samplerate (?P<samplerate>\d+).*", stdout)
    if m != None:
        samplerate = float(m.group("samplerate"))

    bitdepth = None
    m = re.match(r".*#bitdepth (?P<bitdepth>\d+).*", stdout)
    if m != None:
        bitdepth = float(m.group("bitdepth"))
    else:
        # If there is no information of bitdepth we set it to 0
        bitdepth = 0

    bitrate = (os.path.getsize(input_filename) * 8.0) / 1024.0 / duration if duration > 0 else 0
    bitrate = int(round(bitrate))

    return dict(duration=duration, channels=channels, samplerate=samplerate, bitrate=bitrate, bitdepth=bitdepth)


def convert_to_mp3(input_filename, output_filename, quality=70):
    """
    converts the incoming wave file to a mp3 file
    """

    if not os.path.exists(input_filename):
        raise AudioProcessingException("file %s does not exist" % input_filename)

    command = ["lame", "--silent", "--abr", str(quality), input_filename, output_filename]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()

    if process.returncode != 0 or not os.path.exists(output_filename):
        raise AudioProcessingException(stdout)


def convert_to_ogg(input_filename, output_filename, quality=1):
    """
    converts the incoming wave file to n ogg file
    """

    if not os.path.exists(input_filename):
        raise AudioProcessingException("file %s does not exist" % input_filename)

    command = ["oggenc", "-q", str(quality), input_filename, "-o", output_filename]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()

    if process.returncode != 0 or not os.path.exists(output_filename):
        raise AudioProcessingException(stdout)


def convert_using_ffmpeg(input_filename, output_filename):
    """
    converts the incoming wave file to stereo pcm using fffmpeg
    """
    TIMEOUT = 3 * 60

    def alarm_handler(signum, frame):
        raise AudioProcessingException("timeout while waiting for ffmpeg")

    if not os.path.exists(input_filename):
        raise AudioProcessingException("file %s does not exist" % input_filename)

    command = ["ffmpeg", "-y", "-i", input_filename, "-acodec", "pcm_s16le", "-ar", "44100", output_filename]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(TIMEOUT)
    (stdout, stderr) = process.communicate()
    signal.alarm(0)
    if process.returncode != 0 or not os.path.exists(output_filename):
        raise AudioProcessingException(stdout)


def convert_to_pcm(input_filename, output_filename):
    """
    converts any audio file type to pcm audio
    """

    if not os.path.exists(input_filename):
        raise AudioProcessingException("file %s does not exist" % input_filename)

    sound_type = get_sound_type(input_filename)

    if sound_type == "mp3":
        cmd = ["lame", "--decode", input_filename, output_filename]
    elif sound_type == "ogg":
        cmd = ["oggdec", input_filename, "-o", output_filename]
    elif sound_type == "flac":
        cmd = ["flac", "-f", "-d", "-s", "-o", output_filename, input_filename]
    elif sound_type == "m4a":
        cmd = ["faad", "-o", output_filename, input_filename]
    else:
        return False

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()

    if process.returncode != 0 or not os.path.exists(output_filename):
        if "No space left on device" in stderr + " " + stdout:
            raise NoSpaceLeftException
        raise AudioProcessingException("failed converting to pcm data:\n" + " ".join(cmd) + "\n" + stderr + "\n" + stdout)

    return True


def convert_to_wav(
    input_file_path: str,
    output_file_path: str = None,
    overwrite: bool = True
) -> str:
    """
    Convert some input file to wav format using ffmpeg.
    """
    TIMEOUT = 3 * 60

    def alarm_handler(signum, frame):
        raise RuntimeError("convert_to_wav: timeout while waiting for ffmpeg")

    if not os.path.exists(input_file_path):
        raise RuntimeError("{} doesn't exist".format(input_file_path))
    module_logger.debug((f"convert_to_wav: input_file_path={input_file_path}, "
                         f"output_file_path={output_file_path}, "
                         f"overwrite={overwrite}"))
    if output_file_path is None:
        output_file_path = os.path.splitext(input_file_path)[0] + ".wav"

    if not overwrite and os.path.exists(output_file_path):
        raise RuntimeError("convert_to_wav: {} already exists".format(output_file_path))

    cmd_str = "ffmpeg -y -i \"{}\" \"{}\"".format(input_file_path, output_file_path)
    module_logger.debug("convert_to_wav: issuing command {}".format(cmd_str))
    cmd = shlex.split(cmd_str)
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(TIMEOUT)
    (stdout, stderr) = process.communicate()
    signal.alarm(0)
    if process.returncode != 0 or not os.path.exists(output_file_path):
        module_logger.error("convert_to_wav: Error when calling ffmpeg: stdout: {}, stderr: {}".format(stdout, stderr))
        raise RuntimeError(stdout)

    return output_file_path
