# -*- coding: utf-8 -*-
"""
module for audio spectrum analysis
"""

import wave
import numpy as np
import pandas as pd


class FreqAnalysis:
    """
    spectrum analysis class
    """

    def __init__(self, file_name: str):
        wav = wave.open(file_name, 'rb')
        n_frames = wav.getnframes()
        self._frame_rate = wav.getframerate()
        self._duration = n_frames / self._frame_rate
        str_data = wav.readframes(n_frames)
        wave_data = np.frombuffer(str_data, dtype=np.short)
        wave_data.shape = -1, 1
        self._wave_data = wave_data.T
        wav.close()

    def spectrum(self, start_offset: int, window: int, cutoff=5000) -> tuple:
        """
        spectrum of the targeted audio segment
        :param start_offset:
        :param window:
        :param cutoff:
        :return:
        """
        total_samples = self._frame_rate * window
        start = start_offset * self._frame_rate
        data_freq = self._frame_rate / total_samples
        spec = np.fft.fft(self._wave_data[0][start:start + total_samples])
        max_idx = min(int(cutoff / data_freq), int(len(spec) / 2))
        freq = np.arange(0, max_idx) * data_freq
        spec = np.abs(spec[:max_idx])
        spec[0] /= total_samples
        spec[1:] /= total_samples / 2
        return freq, spec

    def freq_feature(self, buckets: list, start_offset: int, window: int, normalized: bool = False,
                     cutoff=5000) -> np.array:
        """
        get the aggregated frequency features from spectrum
        :param buckets: the buckets should not overlap
        :param start_offset:
        :param normalized:
        :param window:
        :param cutoff:
        :return:
        """
        freq, spec = self.spectrum(start_offset, window, cutoff)
        freq_series = pd.Series(data=np.abs(spec), index=freq)
        features = []
        for bucket in buckets:
            width = bucket[1] - bucket[0]
            # the interval's both ends are closed
            selected_freq = freq_series[bucket[0]:bucket[1]]
            features.append(np.sum(selected_freq) / width)

        features = np.array(features)
        if normalized:
            features = features / features.max()
        return features

    def __str__(self):
        return f"frame_rate: {self._frame_rate}\n" \
               f"duration: {self._duration}"
