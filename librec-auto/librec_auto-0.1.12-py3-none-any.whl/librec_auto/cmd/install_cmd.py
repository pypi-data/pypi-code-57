from librec_auto.cmd import Cmd
from librec_auto.util import Files
from librec_auto import ConfigCmd
import os
import librec_auto

class InstallCmd(Cmd):

    def __str__(self):
        return f'InstallCmd()'

    def setup(self, args):
        pass

    def execute(self, config: ConfigCmd):
        lib_path = os.path.dirname(librec_auto.__file__)
        jar_path = lib_path.partition("\\librec_auto")[0]
        jar_path += '\\jar\\auto.jar'
        import urllib.request
        urllib.request.urlretrieve('https://www.dropbox.com/s/hyemqt99790t16q/auto.jar?dl=1', jar_path, MyProgressBar())


class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()