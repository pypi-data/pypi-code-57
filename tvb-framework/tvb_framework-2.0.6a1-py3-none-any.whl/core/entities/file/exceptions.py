# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and 
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#
"""
Exceptions for File Storage layer. 
   
.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""
from tvb.basic.exceptions import TVBException


class FileStructureException(TVBException):
    """
    Exception to be thrown in case of a problem 
    related to File Structure Storage.
    """

    def __init__(self, message):
        TVBException.__init__(self, message)


class FileStorageException(TVBException):
    """
    Generic exception when storing in data in files.
    """

    def __init__(self, message):
        TVBException.__init__(self, message)


class MissingDataSetException(FileStorageException):
    """
    Exception when a dataset is accessed, but no written entry exists in HDF5 file for it.
    we will consider the attribute None.
    """

    def __init__(self, message):
        FileStorageException.__init__(self, message)


class MissingDataFileException(FileStorageException):
    """
    Exception when the file associated to some manager does not exist on disk for some reason.
    """

    def __init__(self, message):
        FileStorageException.__init__(self, message)


class FileVersioningException(TVBException):
    """
    A base exception class for all TVB file storage version conversion custom exceptions.
    """

    def __init__(self, message):
        TVBException.__init__(self, message)


class IncompatibleFileManagerException(FileVersioningException):
    """
    Exception that should be raised in case a file is handled by some filemanager which
    is incompatible with that version of TVB file storage.
    """

    def __init__(self, message):
        FileVersioningException.__init__(self, message)
