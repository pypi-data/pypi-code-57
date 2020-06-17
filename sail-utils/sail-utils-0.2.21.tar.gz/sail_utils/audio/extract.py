# -*- coding: utf-8 -*-
"""
module for audio extraction
"""

from ffmpy import FFmpeg


def extract_audio(input_path: str, output_path: str, sample_rate: int = 16000):
    """
    extract audio from the video
    :param input_path:
    :param output_path:
    :param sample_rate:
    :return:
    """

    ff_cmd = FFmpeg(global_options=['-y'],
                    inputs={input_path: None},
                    outputs={output_path: ['-f', 'wav', '-ar', f'{sample_rate}', '-ac', '1']})
    ff_cmd.run()
