import logging
import os
import typing

import numpy as np
import matplotlib.pyplot as plt
import colour
import PIL

from .audio import Sndfile, AudioProcessor, samples_to_seconds
from .image import WaveformImage, SpectrogramImage
from .plotting import make_fitted_histogram, make_spectrogram_heatmap
from .color import (
    COLOR_SCHEMES,
    DEFAULT_COLOR_SCHEME_KEY,
    interpolate_colors_rgb,
    snap_to_colors,
    InterpolateColorsArgType,
    InterpolateColorsRetType,
    load_from_file)

__all__ = [
    "map_range_factory",
    "AudioVisualizer"
]

module_logger = logging.getLogger(__name__)


def map_range_factory(
    rnge0: typing.List[float],
    rnge1: typing.Optional[typing.List[float]] = None
) -> typing.Callable[[float], float]:
    """
    Create function that will map values from range of values to another.

    Args:
        rnge0: Map values from this range
        rnge1: Map values to this range
    Return:
        callable: Takes as argument a value from rnge0 and returns a
            mapped value in rnge1
    """
    if rnge1 is None:
        rnge1 = [0, 1.0]
    diff0 = rnge0[1] - rnge0[0]
    diff1 = rnge1[1] - rnge1[0]
    factor = diff1/diff0

    def map_range(val):
        if val > rnge0[1]:
            return rnge1[1]
        elif val < rnge0[0]:
            return rnge1[0]
        else:
            return factor*(val - rnge0[0]) + rnge1[0]

    return map_range



class AudioVisualizer:

    def __init__(self,
                 input_filename: str, *,
                 image_width: int,
                 image_height: int,
                 fft_size: int,
                 peak_width: int):

        self._input_filename = input_filename

        self._image_width = image_width
        self.image_height = image_height

        self._peak_width = peak_width

        audio_file = Sndfile(input_filename, 'r')
        self._samplerate = audio_file.samplerate
        self._nframes = audio_file.nframes
        audio_file.close()

        self._adjusted_width = int(self._image_width / float(self._peak_width))
        self._samples_per_pixel = self._nframes / float(self._adjusted_width)

        if fft_size is None or fft_size == -1:
            fft_size = int(self._samples_per_pixel)
            if fft_size % 2 != 0:
                fft_size -= 1
        self._fft_size = fft_size

        self._db_spectra = None
        self._spectra = None
        self._spectral_stats = None
        self._peaks = None

        module_logger.debug(f"AudioVisualizer.__init__: fft_size={fft_size}")
        module_logger.debug(f"AudioVisualizer.__init__: image_width={self.image_width}, image_height={self.image_height}")


    @property
    def input_filename(self):
        return self._input_filename

    @property
    def image_width(self):
        return self._image_width

    @property
    def peak_width(self):
        return self._peak_width

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def nframes(self):
        return self._nframes

    @property
    def adjusted_width(self):
        return self._adjusted_width

    @property
    def samples_per_pixel(self):
        return self._samples_per_pixel

    @property
    def fft_size(self):
        return self._fft_size

    @property
    def spectra(self):
        return self._spectra

    @property
    def db_spectra(self):
        return self._db_spectra

    @property
    def spectral_stats(self):
        return self._spectral_stats

    @property
    def peaks(self):
        return self._peaks

    def smooth(self, x, window_len=11, window='hanning'):
        """smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.

        input:
            x: the input signal
            window_len: the dimension of the smoothing window; should be an odd integer
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.

        output:
            the smoothed signal

        example:

        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

        see also:

        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter

        TODO: the window parameter could be the window itself if an array instead of a string
        NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
        """
        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")

        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")

        if window_len<3:
            return x

        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

        module_logger.debug(f"AudioVisualizer.smooth: window={window}")

        s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
        if window == 'flat': #moving average
            w = np.ones(window_len,'d')
        else:
            window_fn = getattr(np, window)
            w = window_fn(window_len)

        y = np.convolve(w/w.sum(), s, mode='valid')
        window_len_2 = int(window_len/2)
        module_logger.debug(f"AudioVisualizer.smooth: y.shape={y.shape}, window_len_2={window_len_2}")
        return y[window_len_2:-window_len_2]


    def get_palette(
        self,
        color_scheme: str,
        color_scheme_key: str = "wave_colors",
        color_scheme_file_path: str = None,
        color_slice: typing.List[float] = None,
        interpolate_fn: typing.Callable[[InterpolateColorsArgType], InterpolateColorsRetType] = None,
        **interpolate_fn_kwargs
    ) -> typing.Tuple[typing.Tuple[int], InterpolateColorsRetType]:
        """

        Get background color and color palette

        Args:
            color_scheme (str): Name of the color scheme
            color_scheme_key (str): Name of the key in COLOR_SCHEMES[color_scheme].
                Can either be "spec_colors" or "wave_colors"
            color_scheme_file_path (str): Path to JSON or TOML file containing
                externally defined color scheme
            color_slice: slice of color palette to use, expressed as floats between 0.0 and 1.0.
            interpolate_fn (callable): Function to use to interpolate between
                values
            interpolate_fn_kwargs: keyword arguments for `interpolate_fn`
        Returns:
            tuple: background color as RGB tuple, and color palette as list of RGB tuples
        """
        if interpolate_fn is None:
            interpolate_fn = interpolate_colors_rgb

        module_logger.debug(f"AudioVisualizer.get_palette: interpolate_fn={interpolate_fn}")

        if color_slice is None:
            color_slice = [0.0, 1.0]

        if color_slice[0] >= color_slice[1]:
            raise RuntimeError(f"AudioVisualizer.get_palette: second element "
                               f"({color_slice[1]}) in `color_slice` must be "
                               f"greater than first element ({color_slice[0]})")

        if color_scheme_file_path is None:
            colors = COLOR_SCHEMES[color_scheme]
            colors = colors[color_scheme_key]
            background_color = colors[0]
            palette = colors[1:]
        else:
            color_palettes = load_from_file(color_scheme_file_path)
            if color_scheme not in color_palettes:
                raise KeyError(f"{color_scheme} not found in {color_scheme_file_path}")

            background_color = color_palettes[color_scheme]["background"]
            palette = color_palettes[color_scheme]["palette"]
            def to256(val):
                return tuple([int(v*256.0) for v in val])
            background_color = to256(background_color)

        min_idx, max_idx = [int(val*len(palette)) for val in color_slice]
        module_logger.debug(f"AudioVisualizer.get_palette: color_slice={color_slice}")
        module_logger.debug(f"AudioVisualizer.get_palette: len(palette)={len(palette)}")
        module_logger.debug(f"AudioVisualizer.get_palette: [min_idx, max_idx]=[{min_idx}, {max_idx}]")
        palette = palette[min_idx: max_idx]
        palette = interpolate_fn(palette, **interpolate_fn_kwargs)

        return background_color, palette

    def calculate_stats(self, window_fn: typing.Any = np.hanning):
        """
        Calculate spectral centroids, spectra, and peaks, setting corresponding
        internal attributes
        """
        processor = AudioProcessor(
            self.input_filename,
            self.fft_size,
            window_fn
        )

        spectral_stats = np.zeros(self.adjusted_width)
        spectra = np.zeros((self.adjusted_width, int(self.fft_size/2) + 1))
        db_spectra = spectra.copy()
        peaks = np.zeros((self.adjusted_width, 2))

        for x in range(self.adjusted_width):
            seek_point = int(x * self.samples_per_pixel)
            next_seek_point = int((x + 1) * self.samples_per_pixel)

            (spectral_centroid, db_spectrum, spectrum) = processor.spectral_centroid(seek_point)
            spectral_stats[x] = spectral_centroid

            # (spectral_sigma, db_spectrum) = processor.spectral_sigma(seek_point)
            # spectral_stats[x] = spectral_sigma

            db_spectra[x, :] = db_spectrum
            spectra[x, :] = spectrum

            peaks[x, :] = processor.peaks(seek_point, next_seek_point, block_size=4096)

        self._spectral_stats = spectral_stats
        self._db_spectra = db_spectra
        self._spectra = spectra
        self._peaks = peaks

    def _compute_transform_rnge(
        self,
        spectral_centroids,
        peaks,
        mu_cut: int = 3,
        peaks_cut: float = 0.01
    ):
        module_logger.debug(f"AudioVisualizer._compute_transform_rnge: mu_cut={mu_cut}, peaks_cut={peaks_cut}")
        mean, mu = np.mean(spectral_centroids), np.std(spectral_centroids)
        module_logger.debug(f"AudioVisualizer._compute_transform_rnge: spectral centroids mean={mean}, mu={mu}")
        abs_peaks = np.abs(peaks)
        idx_centroids = spectral_centroids >= (mean + mu_cut*mu)
        if peaks_cut > 0.0:
            idx_peaks = np.logical_or(
                abs_peaks[:, 0] < peaks_cut,
                abs_peaks[:, 1] < peaks_cut)
            idx = np.logical_not(np.logical_and(idx_centroids, idx_peaks))
        else:
            idx = np.logical_not(idx_centroids)
        filtered = spectral_centroids[idx]
        return [np.amin(filtered), np.amax(filtered)]

    # def create_waveform_image_alt_0(
    #     self,
    #     palette: typing.List[typing.Tuple[int]],
    #     output_filename: str = None,
    #     dry_run: bool = False
    # ) -> str:
    #     if output_filename is None:
    #         splitted = os.path.splitext(self.input_filename)
    #         output_filename = splitted[0] + ".waveform_alt_0.png"
    #     if dry_run:
    #         return output_filename
    #
    #     if self.spectral_stats is None:
    #         self.calculate_stats()
    #
    #     image = PIL.Image.new(
    #         "RGB", (self.image_width, self.image_height), tuple([0, 0, 0]))
    #
    #     draw = PIL.ImageDraw.Draw(image)
    #
    #     transform_rnge = [np.amin(self.spectral_stats), np.amax(self.spectral_stats)]
    #     spectral_centroid_transform_fn = map_range_factory(transform_rnge)
    #
    #     # peaks_flat = self.peaks.flatten()
    #     peaks_flat = np.abs(self.peaks[:, 0])
    #     transform_rnge = [np.amin(peaks_flat), np.amax(peaks_flat)]
    #     # transform_rnge = [np.amax(peaks_flat), np.amin(peaks_flat)]
    #     # peaks_transform_fn = map_range_factory(transform_rnge, [0.05, 0.6])
    #
    #     # fig, ax = plt.subplots(1, 1)
    #     sigmas = np.std(self.spectra, axis=1)
    #     # sigmas = np.mean(self.spectra, axis=1)
    #     # ax.plot(sigmas)
    #     # plt.show()
    #     transform_rnge = [np.amin(sigmas), np.amax(sigmas)]
    #     sigma_transform_fn = map_range_factory(transform_rnge)
    #
    #     previous_x, previous_y = None, None
    #
    #     def colour2PIL(col):
    #         return tuple([int(val*256.0) for val in col.rgb])
    #
    #     def PIL2colour(col):
    #         return colour.Color(rgb=tuple([val/256.0 for val in col]))
    #
    #     for idx in range(len(self.peaks)):
    #         peak_idx = np.abs(self.peaks[idx, 0])
    #         # print(self.peaks[idx])
    #         stat_idx = self.spectral_stats[idx]
    #         sigma_idx = sigma_transform_fn(sigmas[idx])
    #         # print(sigma_idx)
    #
    #         color_idx = PIL2colour(palette[min(int(spectral_centroid_transform_fn(stat_idx)*255.0), 255)])
    #         peaks_transform_fn = map_range_factory(transform_rnge, [0.05, color_idx.get_luminance()])
    #         luminance_idx = np.abs(peaks_transform_fn(peak_idx))
    #         # print(peak_idx, luminance_idx)
    #
    #         color_idx.set_luminance(
    #             luminance_idx
    #         )
    #         color_idx = colour2PIL(color_idx)
    #
    #         sigma_idx_scaled = sigma_idx * (self.image_height - 4) * 0.5
    #         y1 = self.image_height * 0.5 - sigma_idx_scaled
    #         y2 = self.image_height * 0.5 + sigma_idx_scaled
    #
    #         if previous_y != None:
    #             draw.line([previous_x, previous_y, idx, y1, idx, y2], color_idx)
    #         else:
    #             draw.line([idx, y1, idx, y2], color_idx)
    #         previous_x, previous_y = idx, y2
    #
    #     image.save(output_filename)
    #
    #     return output_filename
    # def draw_peaks(self, x, peaks, spectral_centroid, peak_width=1, transform_fn=None):
    #     """ draw 2 peaks at x using the spectral_centroid for color """
    #     if transform_fn is None:
    #         def transform_fn(spectral_centroid):
    #             return spectral_centroid
    #     # module_logger.debug(f"WaveformImage.draw_peaks: x={x}, peaks={peaks}, spectral_centroid={spectral_centroid}")
    #     y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
    #     y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5
    #
    #     # line_color = self.palette[min(int((spectral_centroid-.02)*355.0), 255)]
    #     line_color = self.palette[min(int(transform_fn(spectral_centroid)*255.0), 255)]
    #
    #     if peak_width == 1:
    #         if self.previous_y != None:
    #             self.draw.line([self.previous_x, self.previous_y, x, y1, x, y2], line_color, width=peak_width)
    #         else:
    #             self.draw.line([x, y1, x, y2], line_color, width=peak_width)
    #         self.previous_x, self.previous_y = x, y2
    #         self.draw_anti_aliased_pixels(x, y1, y2, line_color)
    #     else:
    #         x *= peak_width
    #         self.draw.rectangle([
    #             (x, y2), (x + peak_width, y1)
    #         ], fill=line_color, width=0)

    @staticmethod
    def create_waveform_image_default_output_filename(
        input_filename: str
    ) -> str:
        splitted = os.path.splitext(input_filename)
        output_filename = splitted[0] + ".waveform.png"
        return output_filename

    def create_waveform_image(
        self,
        palette: typing.List[typing.Tuple[int]],
        output_filename: str = None,
        background_color: typing.Tuple[int] = None,
        peaks_cut: float = 0.05,
        mu_cut: int = 3,
        smooth: bool = False,
        normalize: bool = False
    ) -> str:

        if output_filename is None:
            output_filename = AudioVisualizer.create_waveform_image_default_output_filename(
                self.input_filename)

        if background_color is None:
            background_color = tuple(0, 0, 0)

        if self.spectral_stats is None:
            module_logger.debug("AudioVisualizer.create_wave_images: calculating spectral statistics")
            self.calculate_stats()

        waveform = WaveformImage(
            self.image_width,
            self.image_height,
            palette,
            background_color)

        peaks = self.peaks.copy()
        if smooth:
            module_logger.debug(f"AudioVisualizer.create_wave_images: smoothing peaks data")
            peaks[:, 0] = self.smooth(peaks[:, 0], window_len=7, window="blackman")
            peaks[:, 1] = self.smooth(peaks[:, 1], window_len=7, window="blackman")

        if normalize:
            module_logger.debug(f"AudioVisualizer.create_wave_images: normalizing peaks data")
            for idx in range(2):
                peaks[:, idx] = peaks[:, idx] / np.amax(peaks[:, idx])

        module_logger.debug(f"AudioVisualizer.create_wave_images: np.amax(peaks[:, 0])={np.amax(peaks[:, 0])}")
        module_logger.debug(f"AudioVisualizer.create_wave_images: np.amax(peaks[:, 1])={np.amax(peaks[:, 1])}")

        transform_rnge = self._compute_transform_rnge(
            self.spectral_stats, peaks, peaks_cut=peaks_cut, mu_cut=mu_cut)
        transform_fn = map_range_factory(transform_rnge)

        module_logger.debug(f"AudioVisualizer.create_wave_images: transform_rnge={transform_rnge}")

        for x in range(self.adjusted_width):

            waveform.draw_peaks(x, peaks[x, :], self.spectral_stats[x],
                                peak_width=self.peak_width,
                                transform_fn=transform_fn)

        waveform.save(output_filename)
        return output_filename

    @staticmethod
    def create_spectrogram_image_default_output_filename(
        input_filename: str
    ) -> str:
        splitted = os.path.splitext(input_filename)
        output_filename = splitted[0] + ".spectrogram.png"
        return output_filename

    def create_spectrogram_image(
        self,
        palette: typing.List[typing.Tuple[int]],
        output_filename: str = None
    ) -> str:
        if output_filename is None:
            output_filename = AudioVisualizer.create_spectrogram_image_default_output_filename(
                self.input_filename)

        if self.spectra is None:
            self.calculate_stats()

        spectrogram = SpectrogramImage(
            self.image_width,
            self.image_height,
            self.fft_size,
            palette)

        for idx in range(self.spectra.shape[0]):
            spectrogram.draw_spectrum(idx, self.db_spectra[idx, :],
                                      peak_width=self.peak_width)

        spectrogram.save(output_filename)
        return output_filename

    @staticmethod
    def create_debug_plots_default_output_filename(
        input_filename: str
    ) -> str:
        splitted = os.path.splitext(input_filename)
        output_filename = splitted[0] + ".hist_spectrogram.png"
        return output_filename


    def create_debug_plots(
        self,
        palette: typing.List[typing.Tuple[int]],
        output_filename: str = None,
        peaks_cut=0.05,
        mu_cut=3
    ) -> str:

        if output_filename is None:
            output_filename = AudioVisualizer.create_debug_plots_default_output_filename(
                self.input_filename)
        if self.spectra is None:
            self.calculate_stats()

        # fig = plt.figure(figsize=(10, 10))
        # ax0 = fig.add_subplot(311)
        # ax1 = fig.add_subplot(312)
        # ax2 = fig.add_subplot(313)
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))

        transform_rnge = self._compute_transform_rnge(
            self.spectral_stats, self.peaks, peaks_cut=peaks_cut, mu_cut=mu_cut)

        cut_stats = self.spectral_stats[
            np.logical_and(
                self.spectral_stats > transform_rnge[0],
                self.spectral_stats < transform_rnge[1]
            )
        ]


        ax0 = axes[0, 0]
        make_fitted_histogram(
            self.spectral_stats, ax=ax0, bins=20, density=True)
        ax0.set_xlabel("Spectral Centroid value")
        ax0.set_ylabel("Frequency")
        ax0.set_title("Spectral Centroid Histogram")

        ax1 = axes[0, 1]
        make_fitted_histogram(
            cut_stats, bar_colors=palette, ax=ax1, density=True, plot_stats=False)
        ax1.set_xlabel("Spectral Centroid value")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Cut Spectral Centroid Histogram")

        processor = AudioProcessor(
            self.input_filename,
            self.fft_size,
            np.hanning
        )

        ax2 = axes[1, 0]
        spectrum, db_spectrum = processor.get_spectrum()
        ax2.plot(db_spectrum)
        # make_fitted_histogram(
        #     np.abs(self.peaks.flatten()), ax=ax2, bins=20, density=True)
        ax2.set_xlabel("Frequency")
        ax2.set_ylabel("dB")
        ax2.set_title("Spectrum of entire track")
        ax2.grid(True)

        ax3 = axes[1, 1]
        make_spectrogram_heatmap(
            self.spectra,
            nframes=self.nframes,
            samplerate=self.samplerate,
            ax=ax3)
        ax3.set_title("Spectrogram")

        fig.tight_layout()
        fig.savefig(output_filename)
        # plt.show()
        return output_filename
