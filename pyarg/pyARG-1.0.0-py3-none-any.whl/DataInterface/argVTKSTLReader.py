#HEADER
#                   arg/DataInterface/argVTKSTLReader.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
#HEADER

########################################################################
argVTKSTLReader_module_aliases = {
    }
for m in [
    "math",
    "os",
    "paraview.vtk",
    "sys",
    ]:
    has_flag = "has_" + m.replace('.', '_')
    try:
        module_object = __import__(m)
        if m in argVTKSTLReader_module_aliases:
            globals()[argVTKSTLReader_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

from arg.DataInterface.argDataInterfaceBase import *

import vtkmodules.vtkCommonDataModel    as vtkCommonDataModel
import vtkmodules.vtkIOGeometry         as vtkIOGeometry
########################################################################
class argVTKSTLReader(argDataInterfaceBase):
    """A concrete data interface to an STL file based on VTK
    """

    ####################################################################
    def __init__(self, full_name, merge=True):
        """Default constructor: serial reader only, merge duplicates
        """

        # If VTK is not available, do not do anything
        if not has_paraview_vtk:
            self.Times = []
            return

        # Initialize single VTK STL file reader
        self.Reader = vtkIOGeometry.vtkSTLReader()
        self.Reader.SetFileName(full_name)

        # Merge duplicates if and only if requested
        self.Reader.SetMerging(merge)

        # Tag solids with scalars
        self.Reader.ScalarTagsOn()
        self.AttributeName = os.path.splitext(
            os.path.basename(full_name))[0]

        # Update reader meta-information
        self.Reader.UpdateInformation()

    ####################################################################
    def get_accessors(self):
        """Return possibly empty singleton of STL readers
        """

        return [self.Reader]

    ####################################################################
    def get_meta_information(self):
        """Retrieve meta-information from data
        """

        # If VTK is not available, return nothing
        if not has_paraview_vtk:
            return []

        # Initialize global meta-information
        meta = []

        # Return global meta-information
        return meta

    ####################################################################
    def get_property_information(self, prop_type, prop_items=None):
        """Not implemented for STL data yet
        """

        return None

    ####################################################################
    def is_attribute_discrete(self):
        """STL tags are discrete
        """

        return True

    ####################################################################
    def get_attribute_type(self):
        """STL tags are bound to elements
        """

        return "cell"

    ####################################################################
    def get_variable_type(self):
        """STL tags are scalars
        """

        return "scalar"

    ####################################################################
    def get_VTK_reader_output_data(self, _):
        """Get data set as VTK reader output data
        """

        # Update reader
        self.Reader.Update()

        # Store polydata output of reader as single leaf of a composite
        output = vtkCommonDataModel.vtkMultiBlockDataSet()
        output.SetBlock(0, self.Reader.GetOutput())

        # Return constructed multi-block data set
        return output

########################################################################
