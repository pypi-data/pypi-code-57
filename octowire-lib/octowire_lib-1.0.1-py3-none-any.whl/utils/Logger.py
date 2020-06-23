# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import codecs
import shutil

from beautifultable import BeautifulTable
from beautifultable import ALIGN_LEFT
from octowire.utils.Colors import Colors


class _Progress:
    """
    Progress logger is used to dynamically print records.
    """
    def __init__(self, header=''):
        self.header = header
        self.full_msg = ''

    def status(self, msg):
        """
        Dynamically print character on the same line by calling it multiple time.
        :param msg: The text to print.
        :return: Nothing.
        """
        # if msg is a white character, convert it to its hex representation
        if msg.isspace() and msg != " ":
            self.full_msg += '0x{}'.format(codecs.encode(bytes(msg, 'utf-8'), 'hex').decode())
        else:
            self.full_msg += msg
        print('{}: {}'.format(self.header, self.full_msg), end='\r', flush=True)

    def stop(self):
        """
        Stop the dynamic printer process instance.
        :return: Nothing.
        """
        if self.full_msg == '':
            print(end='', flush=False)
        else:
            print(flush=False)


class Logger:
    """
    Manage terminal printing.
    """
    DEFAULT = 0
    ERROR = 1
    SUCCESS = 2
    INFO = 3
    RESULT = 4
    USER_INTERACT = 5
    HEADER = 6
    WARNING = 7

    def __init__(self):
        self.categories = [
            self._print_default,
            self._print_error,
            self._print_success,
            self._print_info,
            self._print_result,
            self._print_user_interact,
            self._print_header,
            self._print_warning
        ]

    def handle(self, text, level=DEFAULT):
        """
        This function prints in different colors a given string.
        :param text: The string to print on the console.
        :param level: The message category.
        :return: Nothing.
        """
        self.categories[level](text) if (level < len(self.categories)) else self.categories[self.DEFAULT](text)

    @staticmethod
    def _print_default(text):
        """
        Print without style.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print(text)

    @staticmethod
    def _print_error(text):
        """
        Beautify error message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}[-]{} {}".format(Colors.FAIL, Colors.ENDC, text))

    @staticmethod
    def _print_success(text):
        """
        Beautify success message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}[+]{} {}".format(Colors.OKGREEN, Colors.ENDC, text))

    @staticmethod
    def _print_info(text):
        """
        Beautify info message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("[*] {}".format(text))

    @staticmethod
    def _print_result(text):
        """
        Beautify result message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}[+] {}{}".format(Colors.OKGREEN, text, Colors.ENDC))

    @staticmethod
    def _print_user_interact(text):
        """
        Beautify user interaction message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}[*] {}{}".format(Colors.OKBLUE, text, Colors.ENDC))

    @staticmethod
    def _print_header(text):
        """
        Beautify header message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}{}{}".format(Colors.BOLD, text, Colors.ENDC))

    @staticmethod
    def _print_warning(text):
        """
        Beautify warning message.
        :param text: Message to be printed.
        :return: Nothing.
        """
        print("{}[!] {}{}".format(Colors.WARNING, text, Colors.ENDC))

    @staticmethod
    def print_tabulate(data, headers):
        """
        Print data in a beautiful tab.
        :param data: List of lists.
        :param headers: The headers of the array table.
        :return: Nothing.
        """
        t_width, _ = shutil.get_terminal_size()
        if t_width >= 95:
            table = BeautifulTable(max_width=95, default_alignment=ALIGN_LEFT)
        else:
            table = BeautifulTable(max_width=t_width, default_alignment=ALIGN_LEFT)

        # Convert dictionary headers into list and bold it
        headers_list = []
        for key, value in headers.items():
            value = Colors.BOLD + value + Colors.ENDC
            headers_list.append(value)
        table.column_headers = headers_list

        # Convert dictionary data to list
        for entry in data:
            row = []
            for key, value in entry.items():
                row.append(value)
            table.append_row(row)

        # change table style
        table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
        table.header_separator_char = '═'
        table.intersect_header_left = '╞'
        table.intersect_header_mid = '╪'
        table.intersect_header_right = '╡'

        # Print table
        print("\n{}\n".format(table))

    @staticmethod
    def progress(header):
        """
        Creates a new progress logger.
        :return: _Progress class instance.
        """
        return _Progress(header)
