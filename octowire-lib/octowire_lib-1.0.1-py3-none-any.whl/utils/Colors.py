# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>

import os
import platform


# Common Colors
class Colors:
    if "Windows" in platform.system() and "WT_SESSION" not in os.environ:
        import colorama
        from colorama import Fore, Style

        colorama.init()
        HEADER = Fore.LIGHTMAGENTA_EX
        OKBLUE = Fore.LIGHTCYAN_EX
        OKGREEN = Fore.LIGHTGREEN_EX
        WARNING = Fore.YELLOW
        FAIL = Fore.LIGHTRED_EX
        ENDC = Fore.RESET
        BOLD = Style.BRIGHT
        MAGENTA = Fore.LIGHTMAGENTA_EX
        UNDERLINE = ""
    else:
        HEADER = '\x1b[95m'
        OKBLUE = '\x1b[94m'
        OKGREEN = '\x1b[92m'
        WARNING = '\x1b[93m'
        FAIL = '\x1b[91m'
        ENDC = '\x1b[0m'
        BOLD = '\x1b[1m'
        MAGENTA = '\x1b[95m'
        UNDERLINE = '\x1b[4m'
