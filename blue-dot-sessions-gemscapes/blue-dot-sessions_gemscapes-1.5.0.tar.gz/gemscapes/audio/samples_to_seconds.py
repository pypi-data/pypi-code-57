import typing

def samples_to_seconds(
    samples: typing.Union[float, int],
    samplerate: typing.Union[float, int]
) -> float:
    time_per_sample = 1.0 / samplerate
    return time_per_sample * samples
