import logging
import os
import sys
import time
from functools import partial
from multiprocessing import Process

import pyscreenshot as ImageGrab

import wx
from render import RENDER_DIR

logger = logging.getLogger(__name__)


def capture_screenshots(delay):
    logger.debug("Screenshots configuring...")
    path = RENDER_DIR / 'screens'
    path.mkdir(exist_ok=True)
    wx.App()  # Need to create an App instance before doing anything

    wx_filename = path / f'wx-screen.png'
    grab_filename = path / f'grab-screen.png'

    im = ImageGrab.grab()
    im.save(str(grab_filename))

    screen = wx.ScreenDC()
    size = screen.GetSize()
    bmp = wx.EmptyBitmap(size[0], size[1])
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
    del mem  # Release bitmap
    bmp.SaveFile(str(wx_filename), wx.BITMAP_TYPE_PNG)


    from time import sleep

    from easyprocess import EasyProcess
    from pyvirtualdisplay import Display

    import pyscreenshot as ImageGrab

    with Display(size=(100, 60)) as disp:  # start Xvfb display
        # display is available
        with EasyProcess(["xmessage", "hello"]):  # start xmessage
            sleep(1)  # wait for diplaying window
            img = ImageGrab.grab()
    img.save("xmessage.png")

def main():
    delay = int(sys.argv[1])
    capture_screenshots(delay)


if __name__ == '__main__':
    main()
