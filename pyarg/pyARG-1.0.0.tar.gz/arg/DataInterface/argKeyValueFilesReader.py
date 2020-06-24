#HEADER
#               arg/DataInterface/argKeyValueFilesReader.py
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
argKeyValueFilesReader_module_aliases = {}
for m in [
    "os",
    "sys",
    "csv",
    "re",
    ]:
    has_flag = "has_" + m.replace('.', '_')
    try:
        module_object = __import__(m)
        if m in argKeyValueFilesReader_module_aliases:
            globals()[argKeyValueFilesReader_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

from arg.DataInterface.argDataInterfaceBase import *

########################################################################
class argKeyValueFilesReader(argDataInterfaceBase):
    """A concrete data interface to a CSV partition in a directory
    """

    ####################################################################
    def __init__(self, *args, sep = '='):
        """Constructor allows for multiple matching files in directory
        """

        # Error out on incorrect constructor signature
        if len(args) != 2:
            print("** ERROR: incorrect parameters for {} constructor. Exiting.".format(
                type(self)))
            sys.exit(1)
        
        # Handle case of empty second parameter
        elif not args[1]:
            # Full file name signature
            full_name = args[0]
            self.Readers = [os.path.basename(full_name)]

            # Retrieve corresponding dictionary
            self.Dictionaries = [self.parse_key_value_file(full_name, sep)]

        # Otherwise search for a collection of files
        else:
            # Retrieve directory name
            dir_name = args[0]

            # Ensure that specified directory exists
            try:
                list_in_dir = os.listdir(dir_name)
            except OSError:
                print("** ERROR: specified directory {} was not found. Exiting.".format(dir_name))
                sys.exit(1)

            # Check type of second pattern
            if not isinstance(args[1], re.Pattern):
                # If not a regexp, assume it is an extension
                re_file_names = re.compile(r"(.*)\.{}".format(args[1]))
            else:
                # Otherwise use regexp as-is
                re_file_names = args[1]

            # Initialize storage for all matching files
            self.Readers = []

            # Initialize storage for retrieved countents
            self.Dictionaries = []

            # Iterate over all files in specified directory
            for base_name in list_in_dir:
                # Assemble full name and ignore directories
                full_name = os.path.join(dir_name, base_name)
                if not os.path.isfile(full_name):
                    continue

                # Try to match file name with regular expression
                if re_file_names.match(base_name):
                    # File name matches regular expression
                    self.Readers.append(base_name)

                    # Append current dictionary to list of existing ones
                    self.Dictionaries.append(self.parse_key_value_file(full_name, sep))

    ####################################################################
    def parse_key_value_file(self, full_name, sep):
        """Parse file with provided name and given separator
        """

        # Initialize storage for key<sep>values in this file
        d = {}

        # Parse file as CSV file with specified separator
        try:
            with open(full_name, "r") as f:
                reader = csv.reader(f, delimiter = sep)
                for r in reader:
                    if len(r) == 2:
                        # Store key<value> pair
                        d[r[0].strip()] = r[1].strip()
        except:
            print("*  WARNING: could not file with name {}.".format(
                os.path.basename(full_name)))

        # Return retrieved directory
        return d

    ####################################################################
    def get_accessors(self):
        """Return list of base file names
        """

        return self.Readers

    ####################################################################
    def get_meta_information(self):
        """Retrieve meta-information from data
        """

        # Initialize global meta-information
        meta = []

        # Iterate over all readers and dictionaries
        for r, d in zip(self.Readers, self.Dictionaries):
            # Initialize meta-information for this reader
            r_meta = {}

            # Keep track of file name
            r_meta["file name"] = r
            
            # Retrieve number of keys
            r_meta["number of keys"] = len(d)

            # Compute number of unique values
            r_meta["number of unique values"] = len(set(d.values()))

            # Append local meta-information to global list
            meta.append(r_meta)
            
        # Return global meta-information
        return meta

    ####################################################################
    def get_property_information(self, prop_type, _=None):
        """Retrieve all information about given sproperty from key/value file
           NB: Sub-property is not supported for this type of files
        """

        # Return requested property across all accessors
        return [prop_type,
                {f: d.get(prop_type)
                 for f, d in zip(self.Readers, self.Dictionaries)},
                prop_type]

########################################################################
