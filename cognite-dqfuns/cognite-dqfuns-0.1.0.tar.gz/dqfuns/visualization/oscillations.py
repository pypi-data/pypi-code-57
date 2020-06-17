"""
Functions used to visualize data from Oscillations Data Quality Metrics
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec


def plot_lpc_roots(threshold, time, data, predicted, f, Pxx, roots, distance):
    """
    Visualization of Linear Predictive Coding (LPC) Analysis of a signal to detect oscillations
    :param threshold: Threshold Radius of the circle to determine if a signal has harmonics
    :param time: time vector of the signal
    :param data: raw data
    :param predicted: predicted polynomial obtained form the LPC analysis
    :param f: Frequency vector from the power spectral density analysis
    :param Pxx: Power spectral density of the signal
    :param roots: Roots of the LPC coefficient
    :param distance: Distance to the unit circle for each root
    :return: Figure
    """
    fig = plt.figure(constrained_layout=True, figsize=(9, 6))
    fig.tight_layout()

    gs = GridSpec(2, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, :-1])
    ax3 = fig.add_subplot(gs[1, 2])

    ax1.plot(time, data, marker=".", label="Raw")
    ax1.plot(time, predicted, "-", label="LPC prediction")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude (Volts)")
    ax1.set_title("Signal")
    ax1.legend()

    ax2.semilogx(f, Pxx)
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("Power (Watts)")
    ax2.set_title("Power Spectral Density")

    # Unit circle and oscillation threshold
    # If there are roots inside the threshold the signal present oscillations
    # A root with a distance to unit circle less than 0.2 is label as data with oscillations
    ang = np.linspace(0, np.pi * 2, 100)
    x_unit = np.cos(ang)
    y_unit = np.sin(ang)
    x_threshold = threshold * np.cos(ang)
    y_threshold = threshold * np.sin(ang)
    # For filling area in plot
    xf = np.concatenate((x_unit, x_threshold[::-1]))
    yf = np.concatenate((y_unit, y_threshold[::-1]))
    ax3.plot(x_unit, y_unit, linewidth=1, color="r")
    ax3.plot(x_threshold, y_threshold, linewidth=1, color="r")
    ax3.axvline(x=0, color="k", linewidth=0.5)
    ax3.axhline(y=0, color="k", linewidth=0.5)
    # Plot roots
    for root, D in zip(roots, distance):
        if D > (1 - threshold):
            ax3.plot(root.real, root.imag, "ro", markersize=7)
        else:
            ax3.plot(root.real, root.imag, "go", markersize=7)

    ax3.set_xlabel("Real Part")
    ax3.set_ylabel("Imaginary Part")
    ax3.set_title("LPC Roots in z-plane")

    ax3.fill_between(xf, yf, color="r", alpha=0.05)
    ax3.set_aspect("equal", adjustable="box")

    fig_handles = {"fig": fig, "ax1": ax1, "ax2": ax2, "ax3": ax3}

    return fig_handles
