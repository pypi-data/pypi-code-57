import pysndfile

class Sndfile:

    __protected = ["_sndfile"]

    def __init__(self, *args, **kwargs):
        self._sndfile = pysndfile.PySndfile(*args, **kwargs)

    @property
    def nframes(self):
        return self._sndfile.frames()

    @property
    def channels(self):
        return self._sndfile.channels()

    @property
    def samplerate(self):
        return self._sndfile.samplerate()

    def __getattr__(self, attr):
        return getattr(self._sndfile, attr)

    def __setattr__(self, attr, val):
        if attr in self.__protected:
            super().__setattr__(attr, val)
        else:
            return setattr(self._sndfile, attr, val)
