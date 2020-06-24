#HEADER
#                   arg/Aggregation/argAggregateTools.py
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
DEBUG_ARG_AGGREGATE_TOOLS = False

########################################################################
# Workaround for MatPlotLib backend limitations
from Aggregation                      import argSummarize
import matplotlib
matplotlib.use("Agg")

########################################################################
argAggregateTools_module_aliases = {
    "math"            : "mt",
    "matplotlib.pylab": "mpl",
    }
for m in [
    "math",
    "matplotlib.pylab",
    "os",
    "re",
    ]:
    has_flag = "has_" + m.replace('.', '_')
    try:
        module_object = __import__(m)
        if m in argAggregateTools_module_aliases:
            globals()[argAggregateTools_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

# Import additional Python packages
from pylatex                            import *
from pylatex.utils                      import NoEscape, verbatim

# Import ARG modules
from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface  import *
from arg.Generation                      import argPlot
from arg.Tools                           import Utilities

########################################################################
# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported verbosity levels
verbosity_levels = supported_types.get(
    "VerbosityLevels")

########################################################################
def create_table(backend, body_list, key, value, types):
    """Retrieve and prepare data to invoke table creating function
    """

    # Define a value separator
    sep = ','

    # Iterate over all values
    vals = value.split(sep)
    for i in range(len(vals)):
        # Initiate row
        row = [argMultiFontStringHelper(backend),
               argMultiFontStringHelper(backend)]
        # Add key only if first row
        if i == 0:
            row[0].append(key, types[0])
            row[1].append(vals[i], types[1])
        # Only add value to next rows, for readibility
        else:
            row[0].append('', types[0])
            row[1].append(vals[i], types[1])
        body_list.append(row)

    return body_list

########################################################################
