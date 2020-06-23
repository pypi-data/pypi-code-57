import logging
import random

import numpy as np

from ..audio_visualizer import AudioVisualizer, map_range_factory
from ..color import DEFAULT_COLOR_SCHEME_KEY, COLOR_SCHEMES, interpolate_colors_fn_lookup
from ..metadata import BDSMetaDataType


__all__ = [
    "wav2png"
]


module_logger = logging.getLogger(__name__)


def wav2png(
    file_path,
    image_width: int = 500,
    image_height: int = 171,
    fft_size: int = 2048,
    peak_width: int = 1,
    color_scheme: str = None,
    color_scheme_file_path: str = None,
    color_space: str = "rgb",
    color_range: float = None,
    mu_cut: float = 2.5,
    normalize: bool = True,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Generate a .png image representation of a .wav file

    Args:
        file_path: Input .wav file path
        image_width: Output image width
        image_height: Output image height
        fft_size: Size of FFT to use in generating PNG output.
            If None or -1 is specified, FFT length will be calculated based on
            `image_width` and `peak_width`
        peak_width: Width of peaks in output PNG
        color_scheme: Name of color scheme
        color_scheme_file_path: Path to TOML file containing color scheme
        color_space: Interpolate in RGB, HSL or use "snap to" colors
        color_range: percentage of color chosen palette to use.
            If None is provided than use whole color palette.
        mu_cut: Apply *upper* sigma cutting to colors when translating from spectral
            centroid values to color palette values. This makes it so outliers
            don't unduely dominate the image. This value should be expressed in
            terms of number (including fractions) of standard deviations above
            which to clip. This will only result in clipping above the spectral centroid mean.
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    if dry_run:
        return AudioVisualizer.create_waveform_image_default_output_filename(file_path)

    visualizer = AudioVisualizer(
        file_path,
        image_width=image_width,
        image_height=image_height,
        fft_size=fft_size,
        peak_width=peak_width
    )

    transform_rnge_kwargs = {
        "peaks_cut": 0.0,
        "mu_cut": mu_cut
    }
    module_logger.debug(f"wav2png: transform_rnge_kwargs={transform_rnge_kwargs}")

    interpolate_fn = interpolate_colors_fn_lookup[color_space]

    visualizer.calculate_stats()

    # with open("means.txt", "a") as fd:
    #     fd.write(f"{np.mean(visualizer.spectral_stats)},")
    # module_logger.debug(f"wav2png: mean of spectral_centroids: {np.mean(visualizer.spectral_stats)}")



    color_slice = [0.0, 1.0]
    if color_range is not None:
        if color_range != 1.0:
            min_val = random.random() * (1.0 - color_range)
            if track_metadata is not None:
                if "Ensemble" in track_metadata:
                    ensemble_val = track_metadata["Ensemble"]
                    module_logger.debug(f"wav2png: Metadata Ensemble value is {ensemble_val}")
                    map_range_fn = map_range_factory([0, 9], [0, 1.0 - color_range])
                    min_val = map_range_fn(ensemble_val)
            max_val = min_val + color_range
            color_slice = [min_val, max_val]

    module_logger.debug(f"wav2png: color_range={color_range}, color_slice={color_slice}")

    background_color, palette = visualizer.get_palette(
        color_scheme,
        color_scheme_file_path=color_scheme_file_path,
        color_slice=color_slice,
        interpolate_fn=interpolate_fn)

    background_color = tuple([255, 255, 255, 0])
    # _, palette_small = visualizer.get_palette(
    #     color_scheme,
    #     num_colors=20,
    #     color_scheme_file_path=color_scheme_file_path,
    #     interpolate_fn=interpolate_fn)

    waveform_output_filename = visualizer.create_waveform_image(
        palette,
        background_color=background_color,
        **transform_rnge_kwargs,
        smooth=False,
        normalize=normalize
    )

    return waveform_output_filename
