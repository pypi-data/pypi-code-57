# -*- coding: utf-8 -*-
"""Microapp standard application module"""

from __future__ import print_function

from typing import Any

from microapp.app import App
from microapp.utils import appdict

class InputApp(App):
    """Input application"""

    _name_ = "input"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("data", nargs="*", help="input data")

        self.register_forward("data", type=Any, help="forward input data")

    def perform(self, args):

        data = [d["_"] for d in args.data]
        self.add_forward(data=data)


class PrintApp(App):
    """print application"""

    _name_ = "print"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("data", nargs="*", help="data to print")
        self.add_argument("-s", "--strip", action="store_true",
                                 help="strip newline at the end of string")

        self.register_forward("stdout", type=str, help="standard output")

    def perform(self, args):

        end = "" if args.strip else "\n"

        if args.data:
            l = []

            for d in args.data:
                val = d['_']
                if not isinstance(val, str):
                    l.append(str(val))
                else:
                    l.append(val)

            out = "".join(l)
            print(out, end=end)
            stdout = out + end
        else:
            stdout = "No data to print."
            print(stdout)

        self.add_forward(stdout=stdout)


standard_apps = appdict({
    InputApp._name_ : InputApp,
    PrintApp._name_ : PrintApp
})

