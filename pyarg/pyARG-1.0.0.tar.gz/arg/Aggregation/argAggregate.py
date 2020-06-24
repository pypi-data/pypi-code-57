#HEADER
#                     arg/Aggregation/argAggregate.py
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
DEBUG_ARG_AGGREGATE = False

########################################################################
# Workaround for MatPlotLib backend limitations
from arg.Aggregation import argSummarize
import matplotlib
matplotlib.use("Agg")

########################################################################
argAggregate_module_aliases = {
    "math"            : "mt",
    }
for m in [
    "math",
    "matplotlib.pylab",
    "os",
    "paraview.vtk",
    "re",
    "yaml",
    ]:
    has_flag = "has_" + m.replace('.', '_')
    try:
        module_object = __import__(m)
        if m in argAggregate_module_aliases:
            globals()[argAggregate_module_aliases[m]] = module_object
        else:
            globals()[m] = module_object
        globals()[has_flag] = True
    except ImportError as e:
        print("*  WARNING: Failed to import {}. {}.".format(m, e))
        globals()[has_flag] = False

# Import additional Python package
from collections                        import OrderedDict

# Import ARG modules
from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface  import *
from arg.Generation                      import argPlot, argVTK

# Import VTK module
import vtkmodules.vtkFiltersExtraction  as vtkFiltersExtraction

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
def map_composite_keys(in_dict, key1, separator):
    """Retrieve key1@...@keyN keys and corresponding values from input dict
       and build output dict with the form {key2:[key3, ..., keyN, value]}
       where @ denotes a 1-character separator
    """

    # Initialize top-level dict
    out_dict = {}

    # Iterate over input dict and filter by prefix with form key1@
    prefix = key1 + separator
    n = len(prefix)
    # for key in filter(lambda l: l[:n] == prefix, in_dict):
    for key in [l for l in in_dict if l[:n] == prefix]:
        # Make sure that at least 2 keys were retrieved
        subkeys = key.split(separator)
        if len(subkeys) < 2:
            # Ignore non-composite keys
            continue

        # Use key2 as output dict key
        key2 = subkeys[1].strip().lower()
        out_dict[key2] = subkeys[2:] + [in_dict[key]]

    # Return result
    return out_dict

########################################################################
def aggregate_descriptive_statistics(s_1, s_2):
    """Aggregate two sets of descriptive statistics (min/mean/max/M2/card)
       It is assumed that second set is an initialized 5-vector
    """

    # Nothing to aggregate if first set of statistics is empty
    if not s_1:
        return s_2[:]

    # Compute global cardinality and its inverse
    n_1 = s_1[4]
    n_2 = s_2[4]
    n_tot = n_1 + n_2
    inv_n_tot = 1. / n_tot

    # Compute means difference
    m_1 = s_1[1]
    m_2 = s_2[1]
    d_21 = m_2 - m_1

    # Retrieve M2 aggregates and compute global one
    M2_1 = s_1[3]
    if n_1 > 1:
        # Assume that unbiased estimator is used
        M2_1 *= (n_1 - 1)
    M2_2 = s_2[3]
    if n_2 > 1:
        # Assume that unbiased estimator is used
        M2_2 *= (n_2 - 1)
    M2 = M2_1 + M2_2 + n_1 * n_2 * d_21 * d_21 * inv_n_tot

    # Return aggregated statistics
    return [
        min(s_1[0], s_2[0]),
        m_1 + n_2 * d_21 * inv_n_tot,
        max(s_1[2], s_2[2]),
        M2 / (n_tot - 1) if n_tot > 1 else M2,
        n_tot]

########################################################################
def aggregate_histograms(h_1, h_2):
    """Aggregate two histograms
       It is assumed that second histogram is a non-void dict
    """

    # Nothing to aggregate if first histogram is empty
    if not h_1:
        return dict(h_2)

    # Build set union of histogram keys
    s_keys = set(h_1) | set(h_2)

    # Return aggregated histogram
    return {
        k: h_1.get(k, 0) + h_2.get(k, 0) for k in s_keys}

########################################################################
def update_or_create_dict_in_dict(dict_of_dicts, key1, key2, value, update_fct):
    """Update or create dict entry in a dict with given primary and
       secondary keys, and value to be used by provided updating function
    """

    # Fetch possibly empty dict in dict of dicts
    sub_dict = dict_of_dicts.get(key1, {})

    # Invoke update function
    sub_dict[key2] = update_fct(sub_dict.get(key2), value)

    # Save current block quality stats
    return sub_dict

########################################################################
def show_mesh_surface(backend, fig_params, data, file_name, do_clip=False):
    """Add surface rendering figure of a dataset to the document
       for a specified point or cell data, scalar or vector variable
    """

    # If argVTK module is missing, do not do anything
    if not argVTK.has_paraview_vtk:
        return

    # Create artifact generator variable
    variable = argVTK.argVTKAttribute(data, fig_params.get("time_step", -1))

    # Execute artifact generator
    output_base_name, caption = argVTK.four_surfaces(
        backend.Parameters,
        fig_params,
        data,
        variable,
        file_name,
        do_clip)

    # Include figure in report
    backend.add_figure({
        "figure_file"   : output_base_name + ".png",
        "caption_string": caption,
        "width"         : fig_params.get("width", "12cm")})

########################################################################
def create_plot(parameters, base_plot_params, data_map, title, data_key, func_prop, pt_marker=None):
    """Retrieve and prepare data to invoke plotting function
    """
    # Create specific plot parameters
    plot_params = dict(base_plot_params)

    # Retrieve plot data
    data_key_lower = data_key.lower()
    try:
        plot_params["data"] = data_map[data_key]
    except:
        try:
            plot_params["data"] = data_map[data_key_lower]
        except:
            print("*  WARNING: no data found for {}".format(data_key))
            return None

    # Retrieve variable names depending on function properties
    var_x_name = ''
    var_y_name = ''
    if isinstance(func_prop, str):
        var_x_name = data_key
        var_y_name = func_prop
    else:
        for p in func_prop:
            # Look for requested function name
            if p[0] in (data_key, data_key_lower):
                # Retrieve abscissa and/or ordinates when defined
                xy_names = p[1]
                if xy_names[0]:
                    var_x_name = xy_names[0]
                if xy_names[1]:
                    var_y_name = xy_names[1]
                break

    # Set other plot parameters
    plot_params["title"]      = title
    plot_params["label"]      = data_key
    plot_params["var_x_name"] = var_x_name
    plot_params["var_y_name"] = var_y_name
    plot_params["marker"]     = pt_marker

    # Execute artifact generator and return its results
    return argPlot.execute_request(parameters, plot_params)

########################################################################
def show_CAD_metadata(backend, request_params, metadata):
    """Add CAD metadata
    """

    # Instantiate interface to CAD properties data
    parameters_root = request_params.get("parameters_root")
    regexp = re.compile(r"(.*)_parameters\.txt")
    cad_metadata = argDataInterface.factory(
        "key-value",
        os.path.join(backend.Parameters.DataDir, parameters_root),
        regexp)

    # Initialize body_lists
    all_body_lists = {}

    # Iterate over metadata items
    for metadatum in metadata:
        prop_item, prop_dict, _ = cad_metadata.get_property_information(metadatum)

        # Iterate over retrieved metadata
        for file_name, value in prop_dict.items():
            # Initialize default values
            color, style = None, "default"

            # Handle particular values
            if value in ('', '-'):
                color, value = "orange", "UNDEFINED"
            elif not value:
                color, value = "red", "NOT FOUND"
            else:
                style = "typewriter"
                
            # Update body list for this parameter file and value
            row = [argMultiFontStringHelper(backend),
                   argMultiFontStringHelper(backend)]
            row[0].append(prop_item, "typewriter")
            row[1].append("{}".format(value), style, color)
            all_body_lists.setdefault(file_name, []).append(row)

    # Issue table
    for file_name, body_list in all_body_lists.items():
        backend.add_table(
            ["CAD parameter", "parameter value"],
            body_list,
            "CAD metadata for part {}. ".format(
                file_name.replace("_parameters.txt", '')))

########################################################################
def show_all_blocks(backend, fig_params, data, file_names, verbose):
    """Add surface rendering figures to the document for each mesh block
       for a specified point or cell data, scalar or vector variable
    """

    # If argVTK module is missing, do not do anything
    if not argVTK.has_paraview_vtk:
        return

    # Compute histograms only if argPlot module is available
    if has_matplotlib_pylab:
        do_histograms = True
        # All histogram plots have identical sizes and aspects
        histo_plot_params = {}
        histo_plot_params["type"] = "histogram"
        histo_plot_params["xyratio"] = 3.5
    else:
        do_histograms = False

    # Retrieve mandatory figure parameters
    try:
        model_data = data["model"]
        model_file = file_names["model"]
    except:
        print("*  WARNING: ignoring request: not enough parameters to show all blocks of input model")
        return

    # Get handle on input data in VTK form
    vtk_data = model_data.get_VTK_reader_output_data(0)
    if not vtk_data:
        print("*  WARNING: ignoring request: could not read VTK data from input model",model_file)
        return

    # Retrieve or create block names and IDs
    meta_data = model_data.get_meta_information()[0]
    block_names = meta_data.get("block names", [])
    block_IDs   = meta_data.get("block IDs", [])

    # Retrieve comments if provided
    comments = map_composite_keys(
        fig_params, "string", backend.Parameters.KeySeparator)

    # Get handle on material and model properties when available
    block_materials = {}
    deck_file = file_names.get("deck")
    if deck_file:
        # Get handle on input deck data
        deck_data = data["deck"]

        # Select and retrieve material
        block_materials = dict(
            deck_data.get_property_information("block"))

    # No deck file was specified
    else:
        print("*  WARNING: no deck file specified when showing all blocks of input model")

    # Generate block visualizations as needed
    variable = argVTK.argVTKAttribute(
        model_data, fig_params.get("time_step", -1))
    block_id_to_flat, block_images_and_captions = argVTK.all_blocks(
        backend.Parameters,
        fig_params,
        model_data,
        variable,
        model_file)

    # Build reverse lookup from flat to block indices
    block_flat_to_id = dict(
        (v, k) for k, vals in block_id_to_flat.items() for v in vals)

    # Storage for topological counts and values
    n_verts, n_elems, t_elems, q_stats, q_histo = ({} for _ in range(5))

    # Iterate over non-empty blocks and extract those
    it = vtk_data.NewIterator()
    it.GoToFirstItem()
    while not it.IsDoneWithTraversal():
        # Retrieve flat index of current non-empty leaf
        idx = it.GetCurrentFlatIndex()

        # Skip ignored blocks
        if idx not in block_flat_to_id:
            if DEBUG_ARG_AGGREGATE:
                print("# Ignoring block with flat index {}".format(
                    idx))
        else:
            # Retrieve corresponding block ID and image file name
            b_id = block_flat_to_id[idx]

            # Extract mesh block
            extract = vtkFiltersExtraction.vtkExtractBlock()
            extract.SetInputData(vtk_data)
            extract.AddIndex(idx)
            extract.Update()
            mesh_block = extract.GetOutput().GetBlock(0)

            # Retrieve mesh block information and append it to global meta
            n_verts[b_id] = n_verts.get(b_id, 0) + mesh_block.GetNumberOfPoints()
            n_e_cur = n_elems.get(b_id, 0)
            n_e_blk = mesh_block.GetNumberOfCells()
            n_elems[b_id] = n_e_cur + n_e_blk
            elem_type_str, elem_q_type = argVTK.get_element_types(mesh_block)
            if True or elem_type_str:
                t_elems.setdefault(b_id, elem_type_str)

            # Append mesh block quality when relevant
            if elem_q_type:
                # Compute all desired quality statistics
                for q_name, q_vtk in argVTK.quality_functions.items():
                    # Compute current block quality statistics and histogram
                    q_s_blk, q_h_blk = argVTK.get_mesh_quality(
                        mesh_block, q_vtk, elem_q_type, do_histograms)

                    # Update or create quality statistics for current block
                    q_stats[b_id] = update_or_create_dict_in_dict(
                        q_stats, b_id, q_name, q_s_blk,
                        aggregate_descriptive_statistics)

                    if do_histograms:
                        # Update or create quality histogram for current block
                        q_histo[b_id] = update_or_create_dict_in_dict(
                            q_histo, b_id, q_name, q_h_blk,
                            aggregate_histograms)

            # Iterate to next non-empty leaf
            it.GoToNextItem()

    # Report about ignored blocks if any
    ignored_block_keys = fig_params.get("ignore_blocks")
    if ignored_block_keys:
        # Insert paragraph on ignored blocks
        ignored_string = argMultiFontStringHelper(backend)
        ignored_string.append("N.B.: ", "bold")
        ignored_string.append("Blocks with ranks or names in ", "default")
        ignored_string.append("{}".format(", ".join(ignored_block_keys)), "typewriter")
        ignored_string.append(" are ignored in this section.", "default")
        backend.add_paragraph({"string": ignored_string})

    # Create per-block pages
    for b_id, (base_name, caption) in sorted(block_images_and_captions.items()):
        # Retrieve block ID and name
        block_name = block_names[block_IDs.index(b_id)]

        # Start new block summary page
        backend.add_page_break()
        block_string = argMultiFontStringHelper(backend)
        block_string.append("Block ", "default")
        block_string.append("{}".format(b_id), "typewriter")
        block_string.append(" (", "default")
        block_string.append(block_name, "typewriter")
        block_string.append(") summary", "default")
        backend.add_subtitle({"title" : block_string})

        # Initialize storage for block properties table body
        body = [
            ["number of nodes", "{}".format(n_verts[b_id])],
            ["number of elements", "{}".format(n_elems[b_id])]]

        # Start with input deck data if available
        if deck_file:
            # Look for block key in materials map
            for b_key in (block_name,
                          block_name.lower(),
                          "{}".format(b_id),
                          "block_{}".format(b_id)):
                m_b = block_materials.get(b_key)
                if m_b:
                    # Block was found, append corresponding material info
                    if m_b[0]:
                        material_string = argMultiFontStringHelper(backend)
                        material_string.append(m_b[0], "typewriter")
                        body.append([
                            "prescribed material name",
                            material_string])
                    if len(m_b) > 1 and m_b[1]:
                        model_string = argMultiFontStringHelper(backend)
                        model_string.append(m_b[1], "typewriter")
                        body.append([
                            "prescribed material model",
                            model_string])
                    # Break out as soon as block was found
                    break
            else:
                print("*  WARNING: no material properties {} found in {}".format(
                    block_name,
                    deck_file))

        # Add block images only when element type is known
        if b_id in t_elems:
            # Add block images and element type to table body
            type_string = argMultiFontStringHelper(backend)
            type_string.append(t_elems.get(b_id), "typewriter")
            body.append([
                "type of first element in block",
                type_string])
            backend.add_figure({
                "figure_file"    : base_name + ".png",
                "caption_string" : caption,
                "width"          : fig_params.get("width", "12cm")})
        else:
            # Block element type is unknown
            body.append(["type of first element in block", "unknown"])

        # Generate table of block properties
        caption_string = argMultiFontStringHelper(backend)
        caption_string.append("Properties of block ", "default")
        caption_string.append(block_name, "typewriter")
        if verbose:
            caption_string.append(" defined in ", "default")
            caption_string.append(model_file, "typewriter")
            if deck_file:
                caption_string.append(" and ", "default")
                caption_string.append(deck_file, "typewriter")
        caption_string.append('.', "default")
        backend.add_table(
            ["property", "value"],
            body,
            caption_string,
            False, # Do not do verbatim
            "hb!") # Put table at bottom of page
        # Append per-block mesh quality information when available
        eqs = q_stats.get(b_id)
        if not eqs:
            # Mesh element type not supported by Verdict VTK
            print("*  WARNING: element type of block {} not supported by Verdict mesh quality library".format(b_id))
        else:
            # Start new block quality statistics page
            backend.add_page_break()
            quality_string = argMultiFontStringHelper(backend)
            quality_string.append("Block ", "default")
            quality_string.append("{}".format(b_id), "typewriter")
            quality_string.append(" (", "default")
            quality_string.append(block_name, "typewriter")
            quality_string.append(") element quality", "default")
            backend.add_subtitle({"title" : quality_string})

            # Create mesh quality table body
            body = []
            for q_n, q_s in eqs.items():
                # Bail out if no quality statistics were provided
                if not q_s:
                    continue

                # Show standard deviation instead of variance
                stdev = mt.sqrt(q_s[3]) if q_s[3] > 0. else 0.
                q_s[3] = stdev

                # Compute coefficient of variation
                q_s[4] = stdev / q_s[1] if q_s[1] > 1e-8 else float("inf")

                # Create new row for current quality name
                body.append([q_n] + ["{:.4g}".format(q) for q in q_s])

            # Generate table of block properties
            head = [argMultiFontStringHelper(backend) for _ in range(6)]
            head[0].append("Q", "calligraphic")
            head[1].append("min(", "default")
            head[1].append("Q", "calligraphic")
            head[1].append(')', "default")
            head[2].append("mu", "greek")
            head[2].append('(', "default")
            head[2].append("Q", "calligraphic")
            head[2].append(')', "default")
            head[3].append("max(", "default")
            head[3].append("Q", "calligraphic")
            head[3].append(')', "default")
            head[4].append("sigma", "greek")
            head[4].append('(', "default")
            head[4].append("Q", "calligraphic")
            head[4].append(')', "default")
            head[5].append("sigma", "greek")
            head[5].append('/', "default")
            head[5].append("mu", "greek")
            head[5].append('(', "default")
            head[5].append("Q", "calligraphic")
            head[5].append(')', "default")
            stat_string = argMultiFontStringHelper(backend)
            stat_string.append("Element quality statistics of block ", "default")
            stat_string.append(block_name, "typewriter")
            stat_string.append('.', "default")
            backend.add_table(
                head,
                body,
                stat_string)

            # Create and add histogram plot when requested and appropriate
            if do_histograms:
                histo_map = q_histo.get(b_id, {})
                for q_n, q_h in histo_map.items():
                    # Bail out if no quality histogram was provided
                    if not q_h:
                        continue

                    # Decide whether to show histogram depending on CoV
                    cv = q_stats.get(b_id).get(q_n)[4]
                    if cv < 1e-3:
                        # Quality spread is too tight for histogram
                        print("*  WARNING: coefficient of variation of block {} {} too small ({}) for histogram".format(
                            b_id,
                            q_name, cv))
                    else:
                        # Generate and insert histogram plot
                        histo_name = create_plot(
                            backend.Parameters,
                            histo_plot_params,
                            histo_map,
                            "block {}".format(b_id),
                            q_n,
                            'element count',
                            'o')
                        if histo_name:
                            histo_string = argMultiFontStringHelper(backend)
                            histo_string.append("Histogram of {} element quality in block ".format(
                                q_n), "default")
                            histo_string.append(block_name, "typewriter")
                            histo_string.append('.', "default")
                            backend.add_figure({
                                "figure_file"    : "{}.png".format(histo_name[0]),
                                "caption_string" : histo_string,
                                "width"          : fig_params.get("histogram_width", "12cm")})

        # Append comment when defined for current block
        if not backend.add_comment(comments, block_name):
            backend.add_comment(comments, b_id)

    # Clear page after last block
    backend.add_page_break()

########################################################################
def show_all_modes(backend, fig_params, data, file_name):
    """Add surface rendering figures for all mode shapes
       for the Disp variable,
       with a normalized displacement with given factor,
       laid out in n_cols columns by n_rows rows
    """

    # If argVTK module is missing, do not do anything
    if not argVTK.has_paraview_vtk:
        return

    # Bail out early if no modes are present
    times = data.get_available_times()
    if not times:
        return

    # Get handle on input data in VTK form
    vtk_data = data.get_VTK_reader_output_data(0)
    if not vtk_data:
        print("*  WARNING: could not read VTK data from input model {}".format(
            file_name))
        return

    # Retrieve first sought mode
    times = data.get_available_times()

    # Determine extreme modes
    mode_min = fig_params.get("mode_min")
    if mode_min:
        mode_min = float(mode_min)
        for i_min, m in enumerate(times):
            if m > mode_min:
                break
    else:
        i_min = 0
    mode_max = fig_params.get("mode_max")
    if mode_max:
        mode_max = float(mode_max)
        for i_max, m in enumerate(reversed(times)):
            if m < mode_max:
                break
        i_max = len(times) - 1 - i_max
    else:
        i_max = len(times) - 1

    # Determine numbers of complete images and of remaining modes
    n_modes_per_image = fig_params.get("n_cols", 1) * fig_params.get("n_rows", 1)
    n_images = i_max - i_min + 1
    n_figs, n_rem = divmod(n_images, n_modes_per_image)

    # Generate images and captions for each for each block of modes
    all_base_names, all_captions = [], []
    variable = argVTK.argVTKAttribute(data, )
    mode_range = [i_min, i_min + n_modes_per_image - 1]

    # Start with all complete images
    for _ in range(n_figs):
        fig_params["range"] = mode_range
        base_name, caption = argVTK.many_modes(
            backend.Parameters,
            fig_params,
            data,
            variable,
            file_name)
        all_base_names.append(base_name)
        all_captions.append(caption)
        mode_range[0] += n_modes_per_image
        mode_range[1] += n_modes_per_image

    # Create incomplete image if modes remain
    if n_rem:
        mode_range[1] = mode_range[0] + n_rem - 1
        fig_params["range"] = mode_range
        base_name, caption = argVTK.many_modes(
            backend.Parameters,
            fig_params,
            data,
            variable,
            file_name)
        all_base_names.append(base_name)
        all_captions.append(caption)

    # Add corresponding modal frequencies table
    modes = []
    for i, m in enumerate(times):
        # Retain only those modes that are in range
        if i < i_min:
            continue
        if i > i_max:
            break

        # Append mode to table body list
        mode_string = argMultiFontStringHelper(backend)
        mode_string.append("{:.1f}".format(m), "typewriter")
        modes.append(["{}".format(i), mode_string])

    # Assemble frequency string
    freq_string = argMultiFontStringHelper(backend)
    freq_string.append("Modal frequencies", "default")
    if mode_min:
        freq_string.append(" greater than {:.1f}Hz".format(mode_min), "default")
    if mode_min and mode_max:
        freq_string.append(" and", "default")
    if mode_max:
        freq_string.append(" less than {:.1f}Hz".format(mode_max), "default")
    freq_string.append('.', "default")
    backend.add_table(
        ["mode number", "frequency (Hz)"],
        modes,
        freq_string)

    # Create figures
    fig_width = fig_params.get("width")
    for base_name, caption_string in zip(all_base_names, all_captions):
        backend.add_figure({
                 "figure_file"    : base_name + ".png",
                 "caption_string" : caption_string,
                 "width"          : fig_width})

########################################################################
def show_enumerated_fields(backend, fig_params, data, file_name):
    """Add surface rendering figures to the document for a
       specified set of point or cell data, scalar or vector variables
    """

    # If argVTK module is missing, do not do anything
    if not argVTK.has_paraview_vtk:
        return

    # Set default figure width
    fig_params.setdefault("width", "12cm")

    # Create per-field pages
    for d in data:
        # Generate page header
        var_desc = "element" if d.AttributeBinding == "cell" else "node"
        var_desc += "-based {}".format(d.AttributeType)

        # Iterate over all available time
        for i, t in enumerate(d.get_available_times()):
            # Start with a new page for each time-step
            backend.add_page_break()

            # Create variable page title
            variable_string = argMultiFontStringHelper(backend)
            variable_string.append("Variable ", "default")
            variable_string.append(d.AttributeName, "typewriter")
            variable_string.append(" (" + var_desc, "default")

            # Append time when more than one time-step is availanle
            if len(d.get_available_times()) > 1:
                variable_string.append(" at time ", "default")
                variable_string.append("{:.6g}".format(t), "typewriter")

            # Create un-numbered subsection
            variable_string.append(')', "default")
            backend.add_subtitle({"title" : variable_string})

            # Get handle on input data in VTK form
            vtk_data = d.get_VTK_reader_output_data(i)
            if not vtk_data:
                print("*  WARNING: could not read VTK data from input model".format(
                    file_name))
                return

            # Generate clipped mesh surface view
            fig_params["time_step"] = i
            show_mesh_surface(backend, fig_params, d, file_name, True)

    # Clear page after last field
    backend.add_page_break()

########################################################################
def arg_aggregate(backend, request_params):
    """Decide which aggregation operation is to be performed
    """

    # Switch between different aggregation types
    request_name  = request_params["name"]
    print("[argAggregate] Processing {} request".format(
        request_name))

    # Operation show_all_blocks: one 4-view figure and one table per mesh block
    if request_name.startswith("show_all_blocks"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())

        # Retrieve model file
        model_file = request_params.get("model")
        file_names = {"model": model_file}

        # Try to retrieve model data
        if model_file:
            model_data = argDataInterface.factory(
                "ExodusII",
                os.path.join(backend.Parameters.DataDir, model_file),
                request_params.get("var_name", ''))
        else:
            model_data = None
        data = {"model": model_data}

        # Aggregate
        if model_data:
            show_all_blocks(backend,
                            request_params,
                            data,
                            file_names,
                            (int(request_params.get("verbosity", 0)) > 0))

    # Operation show_enumerated_fields: one figure page per field
    elif request_name == "show_enumerated_fields":
       # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())
        var_names = request_params.get("var_names")
        if not var_names:
            print("*  WARNING: no variable names provided for {}".format(
                request_name))
            return

        # Get handle on data
        file_name = request_params["model"]
        data = [argDataInterface.factory(
            "ExodusII",
            os.path.join(backend.Parameters.DataDir, file_name), v, False)
                for v in var_names]

        # Aggregate
        if data:
            show_enumerated_fields(backend,
                                   request_params,
                                   data,
                                   file_name)

    # Operation show_all_modes: one figure every n_cols x n_rows modes
    elif request_name.startswith("show_all_modes"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())
        request_params.setdefault("displacement", 2.)
        request_params.setdefault("n_cols", 4)
        request_params.setdefault("n_rows", 4)

        # Get handle on data
        file_name = request_params["model"]
        data = argDataInterface.factory(
            "ExodusII",
            os.path.join(backend.Parameters.DataDir, file_name),
            request_params.get("var_name", "Disp"),
            False)

        # Aggregate
        show_all_modes(backend,
                       request_params,
                       data,
                       file_name)

    # Operation show_mesh_surface: create one figure for the entire mesh
    elif request_name.startswith("show_mesh_surface"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())

        # Get handle on data
        file_name = request_params["model"]
        file_type = request_params["type"]
        if file_type == "ExodusII":
            third_param = request_params.get("var_name", '')
        elif file_type == "vtkSTL":
            third_param = request_params.get("merge", "True")
        else:
            third_param = None
        data = argDataInterface.factory(
            file_type,
            os.path.join(backend.Parameters.DataDir, file_name),
            third_param)

        # Aggregate
        if data:
            show_mesh_surface(backend,
                              request_params,
                              data,
                              file_name)

    # Operation show_CAD_metadata: create one table per reported CAD metadata
    elif request_name == "show_CAD_metadata":

        # Get handle on data and ensure it has the right type
        metadata = request_params.get("metadata")

        # Aggregate
        if metadata:
            show_CAD_metadata(backend, request_params, metadata)

########################################################################
