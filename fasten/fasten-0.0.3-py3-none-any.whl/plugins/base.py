#! /usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
from abc import ABC, abstractmethod


class PluginError(Exception):
    pass


class FastenPlugin(ABC):
    """Base interface for all FASTEN plugins.

    This abstract class provides:

    * Methods for logging (err, log)
    * Methods for declaring the metadata of a plug-in (name, description,
        version)
    * A helper method (free_resource) to free all the resources of a plug-in
    """
    def __init__(self):
        self.errors = sys.stderr
        self.logs = sys.stdout

    def err(self, error):
        """Method to log erros.

        Args:
            error (str): error message
        """
        self.errors.write(error + '\n')

    def log(self, message):
        """Method to log messages.

        Args:
            message (str)
        """
        self.logs.write(message + '\n')

    @abstractmethod
    def name(self):
        """Returns a unique name for the plug-in.

        Returns:
            str: The plugin's fully qualified name
        """

    @abstractmethod
    def description(self):
        """Returns a longer description of the plug-in functionality.

        Returns:
            str: A string describing what the plug-in does
        """

    @abstractmethod
    def version(self):
        """Returns a version of the plug-in.

        Returns:
            str: A string containing a version of the plug-in
        """

    @abstractmethod
    def free_resource(self):
        """The purpose of this method is to release all the resources of a
        plug-in. For example, closing a stream or setting a big object to null.
        """
