import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

module_logger = logging.getLogger(__name__)


def _make_ax():
    fig, ax = plt.subplots(1, 1)
    return fig, ax


def make_fitted_histogram(
    spectral_centroids: np.ndarray,
    ax: matplotlib.axes.Axes = None,
    bar_colors: list = None,
    plot_stats: bool = True,
    **kwargs
) -> None:
    if ax is None:
        fig, ax = _make_ax()

    if bar_colors is not None:
        kwargs["bins"] = len(bar_colors)
        N, bins, patches = ax.hist(spectral_centroids, **kwargs)
        for idx in range(len(patches)):
            color_tuple = bar_colors[idx]
            if any([c > 1.0 for c in color_tuple]):
                color_tuple = tuple([c/256.0 for c in color_tuple])
            patches[idx].set_facecolor(color_tuple)
    else:
        ax.hist(spectral_centroids, **kwargs)

    if plot_stats:
        mu, sigma = np.mean(spectral_centroids), np.std(spectral_centroids)
        sigma_2 = sigma**2
        x = np.linspace(np.amin(spectral_centroids), np.amax(spectral_centroids), 200)
        y = (1.0/np.sqrt(2*np.pi*sigma_2))*np.exp(-0.5*(x-mu)**2/sigma_2)

        lo, hi = ax.get_ylim()

        ax.plot(x, y, color="black")
        for idx in range(1, 4):
            ax.vlines(mu + idx*sigma, lo, hi, color="red")
            ax.vlines(mu - idx*sigma, lo, hi, color="red")

    ax.grid(True)


def make_3d_spectrograph(
    spectra: np.ndarray,
    ax: matplotlib.axes.Axes = None
) -> None:
    x = np.arange(spectra.shape[0])
    y = np.arange(spectra.shape[1])

    xx, yy = np.meshgrid(x, y)
    module_logger.debug(f"make_3d_spectrograph: xx.shape={xx.shape}")
    module_logger.debug(f"make_3d_spectrograph: yy.shape={yy.shape}")
    module_logger.debug(f"make_3d_spectrograph: spectra.shape={spectra.shape}")

    ax.plot_surface(xx, yy, spectra.T)


def make_spectrogram_heatmap(
    spectra: np.ndarray,
    samplerate: float = 44100.0,
    nframes: float = None,
    ax: matplotlib.axes.Axes = None
) -> None:

    xlabel = "Time"
    ax.imshow(spectra.T, aspect="auto", origin="lower")

    if nframes is not None:
        xlabel = "Time (s)"
        xticklabels = ax.get_xticks()
        xticklabels_new = np.linspace(0, nframes/samplerate, len(xticklabels))
    #     xlim = [0, nframes / samplerate]
        ax.set_xticklabels([f"{int(val)}" for val in xticklabels_new])

    if samplerate is not None:
        yticklabels = ax.get_yticks()
        yticklabels_new = np.linspace(0, samplerate/2.0, len(yticklabels))
        ax.set_yticklabels([f"{int(val)}" for val in yticklabels_new])


    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel(xlabel)
    ax.set_title("Audio Spectrogram")
