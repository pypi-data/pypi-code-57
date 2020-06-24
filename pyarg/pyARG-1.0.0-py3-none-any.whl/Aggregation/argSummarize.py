#HEADER
#                     arg/Aggregation/argSummarize.py
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
argSummarize_module_aliases = {"matplotlib.pylab": "mpl"}
for m in [
    "os",
    "yaml"
    ]:
    has_flag = "has_" + m.replace('.', '_')
    try:
        module_object = __import__(m)
        if m in argSummarize_module_aliases:
            globals()[argSummarize_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

# Import ARG modules
from arg.Tools  import Utilities

########################################################################
# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported VTK-based visualizations
comparison_thresholds = supported_types.get(
    "ComparisonThresholds")

########################################################################
def summarize_exodus_topology(meta_info):
    """Create a summary of Exodus II mesh topology in the form of a
    table abstraction with a header list and a dict of contents
    """

    # Iterate over all readers to aggregate topological properties
    n_nodes = 0
    n_elems = 0
    for r in meta_info:
        n_nodes += r.get("nodes")
        n_elems += r.get("elements")

    # Keep track of first reader which contains all shared information
    reader_meta = meta_info[0]

    # Create table header
    header_list = ["item", "number"]

    # Build table body
    body_dict = {
        "Exodus II files": [len(meta_info)],
        "nodes"          : [n_nodes],
        "elements"       : [n_elems]
        }

    # Retrieve block IDs if any
    n = len(reader_meta.get("block IDs"))
    if n:
        body_dict["element blocks"] = [n]

    # Retrieve number of node sets if any
    n = len(list(reader_meta.get("node sets")))
    if n:
        body_dict["node sets"] = [n]

    # Retrieve number of side sets if any
    n = len(list(reader_meta.get("side sets")))
    if n:
        body_dict["side sets"] = [n]

    # Retrieve number of time-steps if any
    n = reader_meta.get("time-steps")
    if n > 1:
        body_dict["time-steps"] = [n]

    # Retrieve number of node fields if any
    n = len(list(reader_meta.get("node fields")))
    if n:
        body_dict["node fields"] = [n]

    # Retrieve number of element fields if any
    n = len(list(reader_meta.get("element fields")))
    if n:
        body_dict["element fields"] = [n]

    # Return summary table
    return header_list, body_dict

########################################################################
def summarize_exodus_blocks(meta_info):
    """Create a summary of Exodus II mesh blocks in the form of a
    table abstraction with a header list and a dict of contents
    """

    # Keep track of first reader which contains all shared information
    reader_meta = meta_info[0]

    # Retrieve list of block names and bail out early if empty
    block_names = reader_meta.get("block names")
    if not block_names:
        return None, None

    # Block types must be aggregated across all distributed files
    #block_types = reader_meta.get("block types")
    #for r in meta_info[1:]:
    #    current_types = r.get("block types")
    #    i_list = [i for i, v in enumerate(block_types) if v == "NULL"]
    #    if i_list:
    #        # Update NULL values
    #        for i in i_list:
    #            block_types[i] = current_types[i]
    #    else:
    #        # Block types list is complete break out early
    #        break

    # Generate block ID, name, and type rows
    body_dict = {i: [v]
                for i, v in zip(
                     reader_meta.get("block IDs"), block_names)}

    # Return summary table
    return ["block ID", "block name"], body_dict

    # Generate block ID, name, and type rows
    #body_dict = {i: [v, t]
    #            for i, v, t in zip(
    #                 reader_meta.get("block IDs"), block_names, block_types)}

    # Return summary table
    #return ["block ID", "block name", "block type"], body_dict

########################################################################
def summarize_exodus_sets(meta_info, set_type):
    """Create a summary of Exodus II node or side sets in the form of a
    table abstraction with a header list and a dict of contents
    """

    # Sanity check
    if set_type not in ("node", "side"):
        return None, None

    # Keep track of first reader which contains all shared information
    reader_meta = meta_info[0]

    # Retrieve list of node or side sets and bail out early if empty
    set_names = reader_meta.get("{} sets".format(set_type))
    if not set_names:
        return None, None

    # Generate node/side set ID, and name
    set_IDs = reader_meta.get("{} set IDs".format(set_type))
    body_dict = {i: [v]
                for i, v in zip(set_IDs, set_names)}

    # Return summary table
    return ["{} set ID".format(set_type), "{} set name".format(set_type)], body_dict

########################################################################
def summarize_exodus_variable(meta_info):
    """Create a summary of Exodus II mesh variables in the form of a
    table abstraction with a header list and a dict of contents
    """

    # Keep track of first reader which contains all shared information
    reader_meta = meta_info[0]

    # Retrieve node-based variables
    body_list = [[v, "NODAL"]
                 for v in sorted(reader_meta.get("node fields"))]

    # Retrieve element-based variables
    for v in sorted(reader_meta.get("element fields")):
        body_list.append([v, "ELEMENT"])

    # Retrieve global variables
    for v in sorted(reader_meta.get("global variables")):
        body_list.append([v, "GLOBAL"])

    # Return summary table
    return ["variable", "type"], body_list

########################################################################
