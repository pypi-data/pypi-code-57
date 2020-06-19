import itertools
import sys
import numpy as np
import scipy.stats
from matplotlib import (offsetbox, pyplot, gridspec)


def create_axes_grid(parameters, labels=None, height_ratios=None,
                     width_ratios=None, no_diagonals=False):
    """
    Taken from gwastro/pycbc
    https://github.com/gwastro/pycbc/blob/master/pycbc/results/scatter_histograms.py

    Given a list of parameters, creates a figure with an axis for
    every possible combination of the parameters.
    Parameters
    ----------
    parameters : list
        Names of the variables to be plotted.
    labels : {None, dict}, optional
        A dictionary of parameters -> parameter labels.
    height_ratios : {None, list}, optional
        Set the height ratios of the axes; see `matplotlib.gridspec.GridSpec`
        for details.
    width_ratios : {None, list}, optional
        Set the width ratios of the axes; see `matplotlib.gridspec.GridSpec`
        for details.
    no_diagonals : {False, bool}, optional
        Do not produce axes for the same parameter on both axes.
    Returns
    -------
    fig : pyplot.figure
        The figure that was created.
    axis_dict : dict
        A dictionary mapping the parameter combinations to the axis and their
        location in the subplots grid; i.e., the key, values are:
        `{('param1', 'param2'): (pyplot.axes, row index, column index)}`
    """
    if labels is None:
        labels = {p: p for p in parameters}
    elif any(p not in labels for p in parameters):
        raise ValueError("labels must be provided for all parameters")
    # Create figure with adequate size for number of parameters.
    ndim = len(parameters)
    if no_diagonals:
        ndim -= 1
    if ndim < 3:
        fsize = (8, 7)
    else:
        fsize = (ndim*3 - 1, ndim*3 - 2)
    fig = pyplot.figure(figsize=fsize)
    # create the axis grid
    gs = gridspec.GridSpec(ndim, ndim, width_ratios=width_ratios,
                           height_ratios=height_ratios,
                           wspace=0.05, hspace=0.05)
    # create grid of axis numbers to easily create axes in the right locations
    axes = np.arange(ndim**2).reshape((ndim, ndim))

    # Select possible combinations of plots and establish rows and columns.
    combos = list(itertools.combinations(parameters, 2))
    # add the diagonals
    if not no_diagonals:
        combos += [(p, p) for p in parameters]

    # create the mapping between parameter combos and axes
    axis_dict = {}
    # cycle over all the axes, setting thing as needed
    for nrow in range(ndim):
        for ncolumn in range(ndim):
            ax = pyplot.subplot(gs[axes[nrow, ncolumn]])
            # map to a parameter index
            px = parameters[ncolumn]
            if no_diagonals:
                py = parameters[nrow+1]
            else:
                py = parameters[nrow]
            if (px, py) in combos:
                axis_dict[px, py] = (ax, nrow, ncolumn)
                # x labels only on bottom
                if nrow + 1 == ndim:
                    ax.set_xlabel('{}'.format(labels[px]), fontsize=18)
                else:
                    pyplot.setp(ax.get_xticklabels(), visible=False)
                # y labels only on left
                if ncolumn == 0:
                    ax.set_ylabel('{}'.format(labels[py]), fontsize=18)
                else:
                    pyplot.setp(ax.get_yticklabels(), visible=False)
            else:
                # make non-used axes invisible
                ax.axis('off')
    return fig, axis_dict


def get_scale_fac(fig, fiducial_width=8, fiducial_height=7):
    """
    Taken from gwastro/pycbc
    https://github.com/gwastro/pycbc/blob/master/pycbc/results/scatter_histograms.py

    Gets a factor to scale fonts by for the given figure. The scale
    factor is relative to a figure with dimensions
    (`fiducial_width`, `fiducial_height`).
    """
    width, height = fig.get_size_inches()
    return (width*height/(fiducial_width*fiducial_height))**0.5


def reduce_ticks(ax, which, maxticks=3):
    """
    Taken from gwastro/pycbc
    https://github.com/gwastro/pycbc/blob/master/pycbc/results/scatter_histograms.py

    Given a pyplot axis, resamples its `which`-axis ticks such that are at most
    `maxticks` left.
    Parameters
    ----------
    ax : axis
        The axis to adjust.
    which : {'x' | 'y'}
        Which axis to adjust.
    maxticks : {3, int}
        Maximum number of ticks to use.
    Returns
    -------
    array
        An array of the selected ticks.
    """
    ticks = getattr(ax, 'get_{}ticks'.format(which))()
    if len(ticks) > maxticks:
        # make sure the left/right value is not at the edge
        minax, maxax = getattr(ax, 'get_{}lim'.format(which))()
        dw = abs(maxax-minax)/10.
        start_idx, end_idx = 0, len(ticks)
        if ticks[0] < minax + dw:
            start_idx += 1
        if ticks[-1] > maxax - dw:
            end_idx -= 1
        # get reduction factor
        fac = int(len(ticks) / maxticks)
        ticks = ticks[start_idx:end_idx:fac]
    return ticks


def create_multidim_plot(parameters, samples, labels=None,
                         mins=None, maxs=None, expected_parameters=None,
                         expected_parameters_color='r',
                         plot_scatter=True,
                         zvals=None, show_colorbar=True, cbar_label=None,
                         vmin=None, vmax=None, scatter_cmap='viridis',
                         fig=None, axis_dict=None, cb_scale=10,
                         scatter_colour='k', scatter_size=5, scatter_marker='o'):
    """
    Taken from gwastro/pycbc
    https://github.com/gwastro/pycbc/blob/master/pycbc/results/scatter_histograms.py

    Generate a figure with several plots and histograms.
    Parameters
    ----------
    parameters: list
        Names of the variables to be plotted.
    samples : np Record Array
        A record array of the samples to plot.
    labels: dict, optional
        A dictionary mapping parameters to labels. If none provided, will just
        use the parameter strings as the labels.
    mins : {None, dict}, optional
        Minimum value for the axis of each variable in `parameters`.
        If None, it will use the minimum of the corresponding variable in
        `samples`.
    maxs : {None, dict}, optional
        Maximum value for the axis of each variable in `parameters`.
        If None, it will use the maximum of the corresponding variable in
        `samples`.
    expected_parameters : {None, dict}, optional
        Expected values of `parameters`, as a dictionary mapping parameter
        names -> values. A cross will be plotted at the location of the
        expected parameters on axes that plot any of the expected parameters.
    expected_parameters_color : {'r', string}, optional
        What color to make the expected parameters cross.
    plot_scatter : {True, bool}
        Plot each sample point as a scatter plot.
    zvals : {None, array}
        An array to use for coloring the scatter plots. If None, scatter points
        will be the same color.
    show_colorbar : {True, bool}
        Show the colorbar of zvalues used for the scatter points. A ValueError
        will be raised if zvals is None and this is True.
    cbar_label : {None, str}
        Specify a label to add to the colorbar.
    vmin: {None, float}, optional
        Minimum value for the colorbar. If None, will use the minimum of zvals.
    vmax: {None, float}, optional
        Maximum value for the colorbar. If None, will use the maxmimum of
        zvals.
    scatter_cmap : {'viridis', string}
        The color map to use for the scatter points. Default is 'viridis'.
    cb_scale : {10, int}
        scale tick size on colour bar
    scatter_colour : {'k', str}
        colour of points if no zvals data given
    scatter_size : {5, int}
        size of points
    scatter_marker : {'o', str}
        marker style for scatter plot
    Returns
    -------
    fig : pyplot.figure
        The figure that was created.
    axis_dict : dict
        A dictionary mapping the parameter combinations to the axis and their
        location in the subplots grid; i.e., the key, values are:
        `{('param1', 'param2'): (pyplot.axes, row index, column index)}`
    """
    if labels is None:
        labels = {p: p for p in parameters}
    # set up the figure with a grid of axes
    # if only plotting 2 parameters, make the marginal plots smaller
    nparams = len(parameters)
    if nparams == 2:
        width_ratios = [3, 1]
        height_ratios = [1, 3]
    else:
        width_ratios = height_ratios = None

    # only plot scatter if more than one parameter
    plot_scatter = plot_scatter and nparams > 1

    # Sort zvals to get higher values on top in scatter plots
    if plot_scatter:
        if zvals is not None:
            sort_indices = zvals.argsort()
            zvals = zvals[sort_indices]
            samples = samples[sort_indices]
        elif show_colorbar:
            raise ValueError("must provide z values to create a colorbar")
        else:
            # just make all scatter points same color
            zvals = scatter_colour

    # convert samples to a dictionary to avoid re-computing derived parameters
    # every time they are needed
    samples = dict([[p, samples[p]] for p in parameters])

    # values for axis bounds
    if mins is None:
        mins = {p: samples[p].min() for p in parameters}
    else:
        # copy the dict
        mins = {p: val for p, val in mins.items()}
    if maxs is None:
        maxs = {p: samples[p].max() for p in parameters}
    else:
        # copy the dict
        maxs = {p: val for p, val in maxs.items()}

    # create the axis grid
    if fig is None and axis_dict is None:
        fig, axis_dict = create_axes_grid(
            parameters, labels=labels,
            width_ratios=width_ratios, height_ratios=height_ratios,
            no_diagonals=True)

    # Off-diagonals...
    for px, py in axis_dict:
        if px == py:
            continue
        ax, _, _ = axis_dict[px, py]
        if plot_scatter:
            alpha = 1.
            plt = ax.scatter(x=samples[px], y=samples[py], c=zvals,
                             s=scatter_size, marker=scatter_marker,
                             edgecolors='none', vmin=vmin, vmax=vmax,
                             cmap=scatter_cmap, alpha=alpha, zorder=2)
        if expected_parameters is not None:
            try:
                ax.axvline(expected_parameters[px], lw=1.5,
                           color=expected_parameters_color, zorder=5)
            except KeyError:
                pass
            try:
                ax.axhline(expected_parameters[py], lw=1.5,
                           color=expected_parameters_color, zorder=5)
            except KeyError:
                pass

        ax.set_xlim(mins[px], maxs[px])
        ax.set_ylim(mins[py], maxs[py])

    # adjust tick number for large number of plots
    if len(parameters) > 3:
        for px, py in axis_dict:
            ax, _, _ = axis_dict[px, py]
            ax.set_xticks(reduce_ticks(ax, 'x', maxticks=3))
            ax.set_yticks(reduce_ticks(ax, 'y', maxticks=3))

    if plot_scatter and show_colorbar:
        # compute font size based on fig size
        scale_fac = get_scale_fac(fig)
        fig.subplots_adjust(right=0.85, wspace=0.03)
        cbar_ax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        cb = fig.colorbar(plt, cax=cbar_ax)
        if cbar_label is not None:
            cb.set_label(cbar_label, fontsize=12*scale_fac)
        cb.ax.tick_params(labelsize=cb_scale*scale_fac)

    return fig, axis_dict
