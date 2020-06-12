import numpy as np

from .sndfile import Sndfile

def get_max_level(filename):
    max_value = 0
    buffer_size = 4096
    audio_file = Sndfile(filename, 'r')
    n_samples_left = audio_file.nframes

    while n_samples_left:
        to_read = min(buffer_size, n_samples_left)

        try:
            samples = audio_file.read_frames(to_read)
        except RuntimeError:
            # this can happen with a broken header
            break

        # convert to mono by selecting left channel only
        if audio_file.channels > 1:
            samples = samples[:,0]

        max_value = max(max_value, np.abs(samples).max())

        n_samples_left -= to_read

    audio_file.close()

    return max_value
