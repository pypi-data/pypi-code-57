#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This file is part of SysPass Client
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os
from colorama import init, Fore, Style
import syspassclient

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
init(autoreset=True)


class SyspassApi(syspassclient.Object):
    def __init__(self):
        syspassclient.Object.__init__(self)
        self.__api_directory = None
        self.__api_filename = None
        self.__api_filename_ext = None
        self.__api_file = None
        self.__api_version = None
        self.__api_data = None

        self.api_directory = None
        self.api_filename_ext = None
        self.api_version = None

    @property
    def api_data(self):
        """
        Return the config file as Python dictionary structure

        :return: Config as a big dictionary
        :rtype: dict
        """
        return self.__api_data

    @api_data.setter
    def api_data(self, parameters):
        """
        set en data and raise in case of error

        :param parameters: something it like a dictionary key
        :type parameters: dict
        :raise TypeError: 'parameters' is not a dict type
        """
        if self.api_data != parameters:
            self.__api_data = parameters

    @property
    def api_version(self):
        if 'DD_SYSPASS_CLIENT_API_VERSION' in os.environ:
            print(
                Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_API_VERSION: {0}".format(
                    os.environ['DD_SYSPASS_CLIENT_API_VERSION'])
            )
            return os.environ['DD_SYSPASS_CLIENT_API_VERSION']

        return self.__api_version

    @api_version.setter
    def api_version(self, version=None):
        if version is None:
            version = '3.1'
        if type(version) != str:
            raise TypeError('"version" must be a str type or None')
        if self.api_version != version:
            self.__api_version = version

    @property
    def api_filename_ext(self):
        """
        Return the api_filename_extension property

        :return: the filename extension like '.yaml'
        :rtype: str
        """
        return self.__api_filename_ext

    @api_filename_ext.setter
    def api_filename_ext(self, extension=None):
        """
        Set the api_filename_ext property

        :param extension: a extension like '.yaml' or None for restore default one ('.yaml')
        :type extension: str or None
        :raise TypeError: When 'extension' is not a str type
        """
        if extension is None:
            extension = ".yaml"

        if not isinstance(extension, str):
            raise TypeError("'extension' must be a str type")

        if self.__api_filename_ext != extension:
            self.__api_filename_ext = extension

    @property
    def api_directory(self):
        return self.__api_directory

    @api_directory.setter
    def api_directory(self, directory=None):
        """
        Return the directory path where is store API yaml file(s)

        :param directory: in case you want force a special directory
        :type directory: str
        :return: the absolute path of the api_directory
        :rtype: str
        """
        if directory is None:
            if self.__api_directory != os.path.join(os.path.dirname(os.path.abspath(__file__)), "api"):
                self.__api_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")

        else:
            if type(directory) != str:
                raise TypeError('"directory" must be a str type or None')
            if self.__api_directory != directory:
                self.__api_directory = directory

    @property
    def api_filename(self):
        """
        Return the api_filename)

        :return: the filename to load
        :rtype: str
        """
        return self.api_version + self.api_filename_ext

    @property
    def api_file(self):
        """
        Return the absolute path of the API yaml file to load

        :return: path of the API yaml file to load
        :rtype: str
        """
        return os.path.join(self.api_directory, self.api_filename)

    def read_api(self):
        """
        Read the API file
        """

        # if api_file is None:
        #     api_file = self.api_file

        with open(self.api_file) as f:
            self.api_data = load(f, Loader=Loader)
            f.close()
            if self.debug and self.debug_level > 1:
                print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end='')
                print(Fore.WHITE + Style.BRIGHT + "{0} ".format("Load API File"))

                print(Fore.WHITE + Style.BRIGHT + "File: ", end='')
                print(self.api_file)

                if self.debug and self.debug_level > 2:
                    for line in dump(self.api_data).split("\n"):
                        if self.verbose and self.verbose_level > 2:
                            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.RESET + Style.RESET_ALL + str(line))

