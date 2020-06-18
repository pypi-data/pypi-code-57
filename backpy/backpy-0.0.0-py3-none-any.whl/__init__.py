"""
A Python interface to run functions in the background.

Functions:
    background - run a function in the background

Usage:
    >>> import backpy
    >>> def myFunction(text):
            while 1:
                print(text)

    >>> thread = backpy.background(target = myFunction, args = ("hello!")) # run
    >>> # the function myFunction in the background with args ("hello!")
    >>> thread._stop() # stop the thread.
    >>> def myEndFunction(data):
            print('Finished', data)

    >>> thread = backpy.background(mode = 'basic+finish',
                                   target = myFunction, args = ("hello!"),
                                   finish = myEndFunction, fargs = ("data"))
    >>> thread._stop() # stop the thread.  
"""

import sys
import threading
from inspect import stack, getframeinfo

def background(mode = 'basic', target = None, args = None, kw = None, **kwargs):
    args = args or ()
    kw = kw or {}
    if mode == 'basic':
        locals()['thread'] = threading.Thread(target = target, args = args, kwargs = kw,
                              daemon = True)
    elif mode == 'basic+finish':
        start = target
        finish = kwargs['finish']
        fargs = kwargs.get('fargs')
        fkw = kwargs.get('fkw')
        
        def func(start, finish, args, kw, fargs, fkw):
            start(*args, **kw)
            finish(*fargs, **fkw)

        locals()['thread'] = threading.Thread(target = func, args = \
                                                        (start, finish,
                                                         args, kw,
                                                         fargs, fkw),
                                  daemon = True)
    else:
        info = getframeinfo(stack()[1][0])
        filename = info.filename
        lineno = info.lineno
        function = info.function
        code_context = info.code_context if info.code_context else ''
        index = info.index or 0
        spaces = ' '*index
        lline = spaces+'^'
        lines = ['Traceback (most recent call last):',
                 f'  File "{filename}", line {lineno}, in {function}',
                 f'    {code_context}',
                 "ValueError: background() mode must be 'basic' or \
'basic+finish'"]
        lines = '\n'.join(lines)
        lines = [lines]

        sys.stderr.writelines(lines)
        return

    locals()['thread'].start()
    return locals()['thread']
