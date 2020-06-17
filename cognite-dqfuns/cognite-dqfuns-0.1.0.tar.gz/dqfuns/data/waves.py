# TODO: Move/reorganize time sampler and noise generator functions to features folder
"""
Code to generate oscillatory signals or data
"""
import numpy as np

from .signal_gen import RedNoise, Sinusoidal, TimeSampler, TimeSeries


def sine_wave(amplitude=10, period=50, phase=3.1416, snr_db=10, mean_noise=0, duration=1000, sampling_frequency=1):
    """'
    Generates a sinusoidal wave with with noise. For generic signal processing purposes, units of volts
    and watts are used.

    Parameters
    __________
    amplitude: Wave amplitude in volts
    period: Wave period in seconds
    phase: wave phase in radians
    snr_db: Signal-to-Noise ratio. A high SNR will produce a signal with low (or negligible) noise and viceversa
    mean_noise: Mean level of the noise in volts
    duration: Total duration of the signal in seconds
    sampling_frequency: Frequency in hz used to generate the interval between data points
    """

    t = np.arange(0, duration, 1 / sampling_frequency)
    wave_volts = amplitude * np.sin(2 * np.pi * t / period + phase)
    wave_power_watts = wave_volts ** 2
    # Add noise with a given Signal-to-Noise-Ratio in dB (SNR)
    # Calculate signal power and convert to dB
    sig_avg_watts = np.mean(wave_power_watts)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    # Calculate noise and convert to watts
    noise_avg_db = sig_avg_db - snr_db
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    # Generate an sample of white noise
    noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(wave_power_watts))
    # Return original signal + noise
    return wave_volts + noise_volts, t


def wave_with_brownian_noise(
    duration=14400, resolution=0.5, percentage=100, amplitude=10, mean=200, frequency=0.04, noise=[1, 1]
):
    # Initializing TimeSampler
    time_sampler = TimeSampler(stop_time=duration)
    # Sampling irregular time samples
    time_vector = time_sampler.sample_irregular_time(resolution=resolution, keep_percentage=percentage)

    # Initializing Sinusoidal signal
    sinusoid = Sinusoidal(amplitude=amplitude, frequency=frequency)

    # Initializing Red (Brownian) noise
    red_noise = RedNoise(std=noise[0], tau=noise[1])

    # Initializing TimeSeries class with the signal and noise objects
    timeseries_corr = TimeSeries(sinusoid, noise_generator=red_noise)

    # Sampling using the irregular time samples
    data_points, signals_corr, errors_corr = timeseries_corr.sample(time_vector)
    data_points = data_points + mean

    return time_vector, data_points
