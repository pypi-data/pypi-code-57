import logging
import typing
import random

import numpy as np

from ..audio_visualizer import AudioVisualizer


__all__ = [
    "compute_stats"
]


module_logger = logging.getLogger(__name__)


def compute_stats(
    file_path,
    image_width: int = 500,
    image_height: int = 171,
    fft_size: int = 2048,
    peak_width: int = 1
) -> typing.Dict[str, float]:
    """
    Get statistics from .wav file

    Args:
        file_path: Input .wav file path
        image_width: Output image width
        image_height: Output image height
        fft_size: Size of FFT to use in generating PNG output.
            If None or -1 is specified, FFT length will be calculated based on
            `image_width` and `peak_width`
        peak_width: Width of peaks in output PNG

    Returns:
        dictionary with statistics data about track
    """
    visualizer = AudioVisualizer(
        file_path,
        image_width=image_width,
        image_height=image_height,
        fft_size=fft_size,
        peak_width=peak_width
    )

    visualizer.calculate_stats()

    return {
        "mean": np.mean(visualizer.spectral_stats),
        "std": np.std(visualizer.spectral_stats)
    }
