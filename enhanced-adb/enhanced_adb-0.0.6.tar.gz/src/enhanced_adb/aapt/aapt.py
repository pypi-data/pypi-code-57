import logging
import subprocess

from .._utils import get_aapt_exe


class AAPT:

    @staticmethod
    def cmd(args=None):
        logging.debug([get_aapt_exe()] + args)
        return subprocess.run([get_aapt_exe()] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
