"""Create a matplotlib figure"""

import sys
import datetime as dt
from collections import OrderedDict
from typing import Tuple
import numpy as np
from numpy import ndarray
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
from lcmap_tap.Plotting.plot_specs import PlotSpecs, date_str_to_date
from lcmap_tap.Plotting import plot_functions, plot_specs, NAMES, COLORS
from lcmap_tap.logger import log, exc_handler


sys.excepthook = exc_handler


def get_plot_items(all_lookup, band_lookup, index_lookup, items: list) -> dict:
    """
    Check to see which bands and/or indices were selected to plot.

    Args:
        all_lookup: all spectral bands and indices
        band_lookup: all spectral bands
        index_lookup: all indices
        items: A dict containing the selected bands/indices to plot

    Returns:
        temp_dict:
    """
    set_lists = [
        ("All Spectral Bands and Indices", all_lookup),
        ("All Spectral Bands", band_lookup),
        ("All Indices", index_lookup),
    ]

    set_lists = OrderedDict(set_lists)

    if items:
        temp_dict = [(i, all_lookup[i]) for i in items if i in all_lookup.keys()]

        temp_dict = OrderedDict(temp_dict)  # Turn list of tuples into an OrderedDict

        for a in set_lists.keys():
            if a in items:
                # Update the dictionary to include the user-specified items
                temp_dict = plot_functions.merge_dicts(temp_dict, set_lists[a])

        return temp_dict

    # Do this by default if the user hasn't selected anything from the list
    return band_lookup


def get_legend_handle(**kwargs):
    """
    A helper function to generate legend handles

    Args:
        **kwargs: Line2D keyword arguments

    Returns:
    """
    return mlines.Line2D([], [], **kwargs)


def create_legend_handle_list(leg_config):
    """
    Create a legend handle list.
    """
    empty_leg = get_legend_handle(**leg_config["highlight_pick"])
    obs_leg = get_legend_handle(**leg_config["clear_obs"])
    mask_leg = get_legend_handle(**leg_config["mask_obs"])
    out_leg = get_legend_handle(**leg_config["out_obs"])
    end_leg = get_legend_handle(**leg_config["end_lines"])
    break_leg = get_legend_handle(**leg_config["break_lines"])
    start_leg = get_legend_handle(**leg_config["start_lines"])
    model_leg = get_legend_handle(**leg_config["model_lines"])
    date_leg = get_legend_handle(**leg_config["date_lines"])

    return [
        empty_leg,
        obs_leg,
        mask_leg,
        out_leg,
        end_leg,
        break_leg,
        start_leg,
        model_leg,
        date_leg,
    ]


def get_class_results(class_data):
    """
    Extract classification results from prediction data.
    Args: class_data - list of dictionaries containing classification probabilities.
    Returns: class_results - dictionary of classifiction results with start/end dates.
    """
    if class_data is not None:
        class_results = dict()

        if not isinstance(class_data, list):
            class_data = [class_data]

        for result in class_data:
            class_ind = result["primary-landcover"]
            class_label = NAMES[class_ind]

            if class_label not in class_results:
                class_results[class_label] = {
                    "starts": [dt.datetime.toordinal(date_str_to_date(result["sday"]))],
                    "ends": [dt.datetime.toordinal(date_str_to_date(result["eday"]))],
                }

            else:
                class_results[class_label]["starts"].append(
                    dt.datetime.toordinal(date_str_to_date(result["sday"]))
                )
                class_results[class_label]["ends"].append(
                    dt.datetime.toordinal(date_str_to_date(result["eday"]))
                )
    else:
        class_results = None
    return class_results


def ard_datetimes(ard_dates):
    """
    Return a list of datetime objects from an ARD time series.
    Args: ard_dates - array of ARD dates
    Returns: datetimes - a list of date time objects in the time series.
    """
    # get year values for labeling plots
    year1 = str(dt.datetime.fromordinal(ard_dates[-1]))[:4]
    year2 = str(dt.datetime.fromordinal(ard_dates[0]))[:4]

    # List of years in time series
    years = range(int(year1), int(year2) + 2, 1)

    # list of datetime objects with YYYY-MM-dd pattern using January 1 for month and day
    datetimes = [dt.datetime(yx, 1, 1) for yx in years]

    return datetimes


def get_labels():
    """
    Return the labels list.
    """
    return [
        "Selected",
        "Clear",
        "Masked",
        "Unused",
        "End Date",
        "Break Date",
        "Start Date",
        "Model Fit",
        "Datelines",
    ]


def leg_lines_to_plots(leg, lines):
    """
    Create a mapping of legend lines to plot artists.
    Args: leg - the subplot axes's pyplot legend
          lines - a list of plotting lines
    Returns: a dictionary of legend lines to plot artists
    """
    # Create an empty dict to contain the mapping of legend lines to plot artists
    lines_map = {}

    for legline, origline in zip(leg.get_lines(), lines):
        # Set a tolerance of 5 pixels
        legline.set_picker(5)

        # Map the artist to the corresponding legend line
        lines_map[legline] = origline

    return lines_map


def draw_figure(
    data: PlotSpecs, predict_data: list, items: list, fig_num: int, config: dict
) -> Tuple[matplotlib.figure.Figure, dict, dict, ndarray]:
    """
    Args:
        data: an instance of the PlotSpecs class, contains all of the plotting attributes and data
        predict_data: list of dictionaries with classification probability data.
        items: A list of strings representing the subplots to be plotted
        fig_num: Will be used as a figure identifier
        config: Plot symbology settings

    Returns:
        fig: A matplotlib.figure.Figure object
        artist_map: A dictionary mapping the data series to plot artists,
                    used for referencing and interactivity
        lines_map: A dictionary mapping the legend lines to the plot artists
                   they represent, used for interactivity
        axes: Using squeeze=False, returns a 2D numpy array of matplotlib.axes.Axes objects
    """
    # Extract properties from passed in PlotSpect data object
    datetimes = ard_datetimes(data.dates)
    total_mask = data.qa_mask
    fill_out = data.fill_mask[~data.date_mask]

    class_results = get_class_results(predict_data)

    # plot_data is a dict whose keys are band names, index names, or a combination of both
    # plot_data[key][0] contains the observed values
    # plot_data[key][1] contains the model predicted values
    plot_data = get_plot_items(
        all_lookup=data.all_lookup,
        band_lookup=data.band_lookup,
        index_lookup=data.index_lookup,
        items=items,
    )

    # Create an empty dict to contain the mapping of data series to artists
    # artist_map[key][0] contains the x-series
    # artist_map[key][1] contains the y-series
    # artist_map[key][2] contains the subplot name
    # The keys that are subplot names will contain an empty point used for displaying
    # which point is selected on the plot
    # All other keys are the PathCollections returned by matplotlib.axes.Axes.scatter
    artist_map = {}

    # squeeze=False allows for plt.subplots to have a single subplot,
    # must specify the column index as well
    # when referencing a subplot because will always return a 2D array
    # e.g. axes[num, 0] for subplot 'num'
    plt.style.use("ggplot")
    fig, axes = plt.subplots(
        nrows=len(plot_data),
        ncols=1,
        figsize=(18, len(plot_data) * 5),
        dpi=65,
        squeeze=False,
        sharex="all",
        sharey="none",
        num=f"timeseries_figure_{fig_num}",
    )

    # Define list objects that will contain the matplotlib artist objects within all subplots
    end_lines = list()
    break_lines = list()
    start_lines = list()
    model_lines = list()
    date_lines = list()

    all_obs_points = list()
    all_out_points = list()
    all_mask_points = list()
    all_empty_points = list()

    class_lines = dict()
    class_handles = None

    m_config = config["DEFAULTS"]

    for num, b in enumerate(plot_data.keys()):
        # Make lists to contain references to the specific artist objects for the current subplot.
        obs_points = list()
        out_points = list()
        mask_points = list()
        empty_point = list()
        class_handles = list()

        # Give each subplot a title
        axes[num, 0].set_title("{}".format(b))

        # Create an empty plot to use for displaying which point is clicked later on
        empty_point.append(axes[num, 0].plot([], [], **m_config["highlight_pick"]))

        # Store a reference to the empty point which will be used to display clicked
        # points on the plot
        artist_map[b] = empty_point[0]

        all_empty_points.append(empty_point[0][0])

        # Plot the observed values within the PyCCD time range
        obs = axes[num, 0].scatter(
            x=data.dates_in[total_mask[data.date_mask]],
            y=plot_data[b][0][data.date_mask][total_mask[data.date_mask]],
            **m_config["clear_obs"],
        )

        obs_points.append(obs)
        all_obs_points.append(obs)

        # There's only ever one item in the *_points lists-a PathCollection artist
        # but it makes it easier to use with
        # the 2D Lines because those are lists too.  See the plotwindow.py module.
        artist_map[obs_points[0]] = [
            data.dates_in[total_mask[data.date_mask]],
            plot_data[b][0][data.date_mask][total_mask[data.date_mask]],
            b,
        ]

        # Observed values outside of the PyCCD time range
        out = axes[num, 0].scatter(
            x=data.dates_out[fill_out],
            y=plot_data[b][0][~data.date_mask][fill_out],
            **m_config["out_obs"],
        )

        out_points.append(out)
        all_out_points.append(out)

        artist_map[out_points[0]] = [
            data.dates_out[fill_out],
            plot_data[b][0][~data.date_mask][fill_out],
            b,
        ]

        # Plot the observed values masked out by PyCCD
        mask = axes[num, 0].scatter(
            x=data.dates_in[~total_mask[data.date_mask]],
            y=plot_data[b][0][data.date_mask][~total_mask[data.date_mask]],
            **m_config["mask_obs"],
        )

        mask_points.append(mask)
        all_mask_points.append(mask)

        artist_map[mask_points[0]] = [
            data.dates_in[~total_mask[data.date_mask]],
            plot_data[b][0][data.date_mask][~total_mask[data.date_mask]],
            b,
        ]

        # plot the model start, end, and break dates
        for ind, s in enumerate(data.start_dates):
            lines1 = axes[num, 0].axvline(
                dt.datetime.toordinal(date_str_to_date(s)), **m_config["start_lines"]
            )
            end_lines.append(lines1)

        for ind, e in enumerate(data.end_dates):
            lines3 = axes[num, 0].axvline(
                dt.datetime.toordinal(date_str_to_date(e)), **m_config["end_lines"]
            )
            start_lines.append(lines3)

        for ind, br in enumerate(data.break_dates):
            lines2 = axes[num, 0].axvline(
                dt.datetime.toordinal(date_str_to_date(br)), **m_config["break_lines"]
            )
            break_lines.append(lines2)

        # Draw the predicted curves
        if data.segment_classes is not None:
            for c in range(0, len(data.segment_classes)):
                (lines5,) = axes[num, 0].plot(
                    data.prediction_dates[c * len(plot_specs.bands)],
                    plot_data[b][1][c],
                    **m_config["model_lines"],
                )

                model_lines.append(lines5)

        # Draw horizontal color bars representing class assignments
        if class_results is not None:
            for key in class_results:
                if key not in class_lines:
                    class_lines[key] = list()

                for ind, item in enumerate(class_results[key]["starts"]):
                    lines6 = axes[num, 0].hlines(
                        y=0,
                        xmin=item,
                        xmax=class_results[key]["ends"][ind],
                        linewidth=6,
                        colors=COLORS[key],
                    )

                    class_lines[key].append(lines6)

                class_handles.append(
                    get_legend_handle(linewidth=6, color=COLORS[key], label=key)
                )

        # Set values for the y-axis limits
        if b in data.index_lookup.keys():
            # Potential dynamic range values
            # ymin = min(plot_data[b][0][data.date_mask][total_mask]) - 0.15
            # ymax = max(plot_data[b][0][data.date_mask][total_mask]) + 0.1

            # Preferred static range values
            ymin = -1.01  # Band ratio or index min
            ymax = 1.01  # Band ratio or index max

        elif b == "Thermal":
            ymin = -2500
            ymax = 6500

        else:  # Spectral bands
            # Potential dynamic range values
            # ymin = min(plot_data[b][0][data.date_mask][total_mask]) - 700
            # ymax = max(plot_data[b][0][data.date_mask][total_mask]) + 500

            # Preferred static range values
            ymin = -100
            ymax = 6500

        # Set the y-axis limits
        axes[num, 0].set_ylim([ymin, ymax])

        # Display the x and y values where the cursor is placed on a subplot
        axes[num, 0].format_coord = lambda xcoord, ycoord: "({0:%Y-%m-%d}, ".format(
            dt.datetime.fromordinal(int(xcoord))
        ) + "{0:f})".format(ycoord)

        # Plot a vertical line at January 1 of each year on the time series
        for date in datetimes:
            lines7 = axes[num, 0].axvline(date, visible=False, **m_config["date_lines"])
            date_lines.append(lines7)

        # Set the axis face color
        axes[num, 0].patch.set_facecolor(m_config["background"]["color"])

        # With sharex=True, set all x-axis tick labels to visible
        axes[num, 0].tick_params(
            axis="both", which="both", labelsize=12, labelbottom=True
        )

    # Create custom legend handles
    leg_config = config["LEG_DEFAULTS"]
    handles = create_legend_handle_list(leg_config=leg_config)

    labels = get_labels()

    lines = [
        all_empty_points,
        all_obs_points,
        all_mask_points,
        all_out_points,
        end_lines,
        break_lines,
        start_lines,
        model_lines,
        date_lines,
    ]

    # Add whichever land cover classes are present to the legend handles and labels
    for c in class_handles:
        handles.append(c)

    for cl in class_results:
        labels.append(cl)

    leg = axes[0, 0].legend(
        handles=handles,
        labels=labels,
        ncol=1,
        loc="upper left",
        bbox_to_anchor=(1.00, 1.00),
        borderaxespad=0.0,
    )

    for key in class_lines:
        lines.append(class_lines[key])

    # Create a mapping of legend lines to plot artists
    lines_map = leg_lines_to_plots(leg=leg, lines=lines)

    try:
        # Fill in the figure canvas
        fig.tight_layout()

    except ValueError as e:
        log.error("Exception: %s", e, exc_info=True)

    # Make room for the legend
    fig.subplots_adjust(right=0.9)

    return fig, artist_map, lines_map, axes
