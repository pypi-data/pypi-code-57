# How to use
# from pyOpenRPA.Tools import Terminator
# Terminator.Init(inLogger=None)
# Terminator.IsSignalClose() # True - WM_CLOSE SIGNAL has come
# Terminator.SessionLogoff() # Logoff the session

import win32con
import win32gui
import os
gIsSignalCloseBool = False
gLogger = None
gWindowTitleStr = "PythonTerminator" # Title of the phantom window
gWindowDescriptionStr = "pyOpenRPA library for safe turn off the program (by send the WM_CLOSE signal from task kill)" # Description of the phantom window

# Init the terminator
def Init(inLogger=None):
    global gLogger
    global gIsSignalCloseBool
    gIsSignalCloseBool = False # Init default
    gLogger = inLogger
    #import sys
    #import time
    #import atexit
    import threading
    #atexit.register(print, 'PYTHON SPAM APP: SHUTDOWN')
    shutdown_thread = threading.Thread(target=shutdown_monitor)
    shutdown_thread.start()
    #shutdown_thread.join()
    #shutdown_monitor()
    
# Terminator.IsSignalClose() # True - WM_CLOSE SIGNAL has come
def IsSignalClose():
    global gIsSignalCloseBool # Init the global variable
    return gIsSignalCloseBool # Return the result

# Terminator.SessionLogoff() # Logoff the session
def SessionLogoff():
    os.system("shutdown /l")

# Technical function
def shutdown_monitor():
    global gIsSignalCloseBool # Init the global variable
    global gLogger
    def wndproc(hwnd, msg, wparam, lparam):
        if msg == win32con.WM_CLOSE:
            win32gui.DestroyWindow(hwnd)
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = gWindowTitleStr
    wc.lpfnWndProc = wndproc
    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(gWindowTitleStr, gWindowDescriptionStr,
                0, 0, 0, 0, 0, 0, 0, 0, None)
    win32gui.PumpMessages()
    gIsSignalCloseBool = True # WM_CLOSE message has come
    if gLogger:
        gLogger.info(f"Terminator: Program has recieve the close signal - safe exit")
    
