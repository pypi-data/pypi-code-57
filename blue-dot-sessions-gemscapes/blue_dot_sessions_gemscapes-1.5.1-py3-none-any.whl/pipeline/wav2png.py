import logging

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
    normalize: bool = False,
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

    transform_rnge_kwargs = dict(
        peaks_cut=0.0,
        mu_cut=2.5
    )

    interpolate_fn = interpolate_colors_fn_lookup[color_space]

    background_color, palette = visualizer.get_palette(
        color_scheme,
        color_scheme_file_path=color_scheme_file_path,
        interpolate_fn=interpolate_fn)

    background_color = tuple([255, 255, 255, 0])
    _, palette_small = visualizer.get_palette(
        color_scheme,
        num_colors=20,
        color_scheme_file_path=color_scheme_file_path,
        interpolate_fn=interpolate_fn)

    waveform_output_filename = visualizer.create_waveform_image(
        palette,
        background_color=background_color,
        **transform_rnge_kwargs,
        smooth=False,
        normalize=normalize
    )

    return waveform_output_filename
