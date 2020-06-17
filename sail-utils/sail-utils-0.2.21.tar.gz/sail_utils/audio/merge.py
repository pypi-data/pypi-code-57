# -*- coding: utf-8 -*-
"""
module for audio merge
"""

from sail_utils.utilities import _merge


def audio_merge(start_epoch: int,
                end_epoch: int,
                merged_file: str,
                used_files: list):
    """
    merge audio files
    :param start_epoch:
    :param end_epoch:
    :param merged_file:
    :param used_files:
    :return:
    """
    _merge(start_epoch, end_epoch, merged_file, used_files)
