#HEADER
#                      arg/Applications/Assembler.py
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
ARG_VERSION         = "1.0.0"

DEBUG_ARG_YAML      = False
DEBUG_ARG_PYTHON    = True
DEBUG_ARG_LATEX     = True
app                 = "Assembler"

########################################################################
assembler_module_aliases = {}
for m in [
    "distutils",
    "distutils.spawn",
    "os",
    "sys",
    "time",
    "yaml",
    ]:
    has_flag = "has_" + m
    try:
        module_object = __import__(m)
        if m in assembler_module_aliases:
            globals()[assembler_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

# Import ARG modules
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append("..")
from arg.Common.argReportParameters         import argReportParameters
from arg.Backend.argBackendBase             import argBackendBase
from arg.Tools                              import Utilities

########################################################################
# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)

########################################################################
def main(app, types, version=None):
    """ Assembler main method
    """

    # Start timer
    t_start = time.time()

    # Print startup information
    sys_version = sys.version_info
    print("[{}] ### Started with Python {}.{}.{}".format(
        app,
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    # Instantiate parameters object from command line arguments
    parameters = argReportParameters(app, version=version, types=types)

    # Parse command line arguments to get parameters file value
    if parameters.parse_line():

        # Additional debug information when requested
        ARG.print_debug(app, DEBUG_ARG_PYTHON, DEBUG_ARG_LATEX, parameters.LatexProcessor)
        # Execute
        execute(app, parameters)

    # Print error message if something went wrong
    else:
        print("*  ERROR: cannot parse parameters. Exiting.")

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    success_apps = parameters.get_successful_apps(app)
    print("[{}] Ran {} successfully.".format(
        app,
        success_apps))
    print("[{}] Process completed in {} seconds. ###".format(
        app,
        dt))

########################################################################
def execute(app, parameters):
    """ Assembler execute method
    """

    # Check structure file location
    file = parameters.StructureFile
    if (not os.path.exists(parameters.StructureFile)
        and os.path.exists(os.path.join(parameters.OutputDir, parameters.StructureFile))):
        file = os.path.join(parameters.OutputDir, parameters.StructureFile)
    report_map = Utilities.read_yml_file(file, parameters.Application)

    # Have backend assemble the report and stop timer
    parameters.Backend.assemble(
        report_map,
        parameters.Version,
        parameters.LatexProcessor)

    # Log execution status
    parameters.log_execution_status(app, "{}".format(os.path.dirname(parameters.OutputDir)))

########################################################################
if __name__ == '__main__':
    """ Main report assembler routine
    """

    main(app, Types, ARG_VERSION)

########################################################################
