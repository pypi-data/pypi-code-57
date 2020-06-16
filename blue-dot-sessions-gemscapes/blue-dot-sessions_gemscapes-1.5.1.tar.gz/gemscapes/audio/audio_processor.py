# audio_processor.py
import math

import numpy as np

from .sndfile import Sndfile
from .get_max_level import get_max_level


class AudioProcessor(object):
    """
    The audio processor processes chunks of audio an calculates the spectrac centroid and the peak
    samples in that chunk of audio.
    """
    def __init__(self, input_filename, fft_size, window_fn=np.hanning):
        max_level = get_max_level(input_filename)

        self.audio_file = Sndfile(input_filename, 'r')
        self.fft_size = fft_size
        self.window = window_fn(self.fft_size)
        self.window_fn = window_fn
        self.spectrum_range = None
        self.lower = 100
        self.higher = 22050
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))

        # figure out what the maximum value is for an FFT doing the FFT of a DC signal
        fft = np.fft.rfft(np.ones(fft_size) * self.window)
        max_fft = (np.abs(fft)).max()
        # set the scale to normalized audio and normalized FFT
        self.scale = 1.0/max_level/max_fft if max_level > 0 else 1

    def read(self, start, size, resize_if_less=False):
        """ read size samples starting at start, if resize_if_less is True and less than size
        samples are read, resize the array to size and fill with zeros """
        # module_logger.debug(f"AudioProcessor.read: start={start}, size={size}, resize_if_less={resize_if_less}")
        # number of zeros to add to start and end of the buffer
        add_to_start = 0
        add_to_end = 0

        if start < 0:
            # the first FFT window starts centered around zero
            if size + start <= 0:
                return np.zeros(size) if resize_if_less else np.array([])
            else:
                self.audio_file.seek(0)

                add_to_start = -start # remember: start is negative!
                to_read = size + start

                if to_read > self.audio_file.nframes:
                    add_to_end = to_read - self.audio_file.nframes
                    to_read = self.audio_file.nframes
        else:
            self.audio_file.seek(start)

            to_read = size
            if start + to_read >= self.audio_file.nframes:
                to_read = self.audio_file.nframes - start
                add_to_end = size - to_read

        try:
            samples = self.audio_file.read_frames(to_read)
            # module_logger.debug("AudioProcessor.read: samples.dtype={}".format(samples.dtype))
        except RuntimeError:
            # this can happen for wave files with broken headers...
            return np.zeros(size) if resize_if_less else np.zeros(2)

        # convert to mono by selecting left channel only
        if self.audio_file.channels > 1:
            samples = samples[:,0]

        if resize_if_less and (add_to_start > 0 or add_to_end > 0):
            # module_logger.debug("AudioProcessor.read: type(add_to_start)={}".format(type(add_to_start)))
            if add_to_start > 0:
                samples = np.concatenate((np.zeros(int(add_to_start)), samples), axis=0)

            if add_to_end > 0:
                # module_logger.debug(f"AudioProcessor.read: add_to_end={add_to_end}, samples.shape[0]={samples.shape[0]}")
                samples = np.resize(samples, size)
                samples[:-int(add_to_end)] = 0

        return samples


    def get_spectrum(self,
         start: int = None,
         end: int = None,
         spec_range: float = 110.0,
         fft_fn: callable = np.fft.rfft
    ) -> np.ndarray:
        """
        Get spectrum from `start` to `end`. If `end` is None, get until the end of the track.
        If `start` is None, then get from the beginning.
        """
        if start is None:
            start = 0
        if end is None:
            end = self.audio_file.nframes

        samples = self.read(start, end)
        nsamples = samples.shape[0]

        window_nsamples = self.window_fn(nsamples)

        samples *= window_nsamples

        spectrum = np.abs(fft_fn(samples))
        spectrum /= np.amax(spectrum) # normalize the FFT

        db_spectrum = ((20*(np.log10(spectrum + 1e-60))).clip(-spec_range, 0.0) + spec_range)/spec_range

        return spectrum, db_spectrum

    def spectral_centroid(self, seek_point, spec_range=110.0):
        """ starting at seek_point read fft_size samples, and calculate the spectral centroid """
        # module_logger.debug(f"AudioProcessor.spectral_centroid: seek_point={seek_point}, spec_range={spec_range}")
        samples = self.read(seek_point - self.fft_size/2, self.fft_size, True)

        samples *= self.window
        fft = np.fft.rfft(samples)
        spectrum = self.scale * np.abs(fft) # normalized abs(FFT) between 0 and 1
        length = np.float64(spectrum.shape[0])
        # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
        db_spectrum = ((20*(np.log10(spectrum + 1e-60))).clip(-spec_range, 0.0) + spec_range)/spec_range

        energy = spectrum.sum()
        spectral_centroid = 0

        if energy > 1e-60:
            # calculate the spectral centroid

            if self.spectrum_range is None:
                self.spectrum_range = np.arange(length)

            spectral_centroid = (spectrum * self.spectrum_range).sum() / (energy * (length - 1)) * self.audio_file.samplerate * 0.5

            # clip > log10 > scale between 0 and 1
            spectral_centroid = (math.log10(self.clip(spectral_centroid, self.lower, self.higher)) - self.lower_log) / (self.higher_log - self.lower_log)

        return (spectral_centroid, db_spectrum, spectrum)


    def spectral_sigma(self, seek_point, spec_range=110.0):
        """ starting at seek_point read fft_size samples, and calculate the spectral centroid """
        # module_logger.debug(f"AudioProcessor.spectral_centroid: seek_point={seek_point}, spec_range={spec_range}")
        samples = self.read(seek_point - self.fft_size/2, self.fft_size, True)

        samples *= self.window
        fft = np.fft.rfft(samples)
        spectrum = self.scale * np.abs(fft) # normalized abs(FFT) between 0 and 1
        length = np.float64(spectrum.shape[0])
        # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
        db_spectrum = ((20*(np.log10(spectrum + 1e-60))).clip(-spec_range, 0.0) + spec_range)/spec_range

        spectral_sigma = np.std(spectrum)

        return (spectral_sigma, db_spectrum)


    def peaks(self, start_seek, end_seek, block_size=4096):
        """ read all samples between start_seek and end_seek, then find the minimum and maximum peak
        in that range. Returns that pair in the order they were found. So if min was found first,
        it returns (min, max) else the other way around. """

        max_index = -1
        max_value = -1
        min_index = -1
        min_value = 1

        if start_seek < 0:
            start_seek = 0

        if end_seek > self.audio_file.nframes:
            end_seek = self.audio_file.nframes

        if end_seek <= start_seek:
            samples = self.read(start_seek, 1)
            return (samples[0], samples[0])

        if block_size > end_seek - start_seek:
            block_size = end_seek - start_seek

        for i in range(start_seek, end_seek, block_size):
            samples = self.read(i, block_size)

            local_max_index = np.argmax(samples)
            local_max_value = samples[local_max_index]

            if local_max_value > max_value:
                max_value = local_max_value
                max_index = local_max_index

            local_min_index = np.argmin(samples)
            local_min_value = samples[local_min_index]

            if local_min_value < min_value:
                min_value = local_min_value
                min_index = local_min_index

        return (min_value, max_value) if min_index < max_index else (max_value, min_value)
