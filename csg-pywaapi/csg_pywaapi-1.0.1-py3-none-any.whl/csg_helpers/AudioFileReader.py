import wave as wv

def OpenAudioFile(filename):
    #audiofile = sf.SoundFile(filename)
    audiofile = wv.open(filename,"rb")
    return audiofile

def GetChannels(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.getnchannels()

def GetSamplerate(filename):
    audiofile = OpenAudioFile(filename)
    return audiofile.getframerate()


