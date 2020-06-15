import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

from . import utils
from . import datums

_log = logging.getLogger(__name__)
_log_fmt = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=_log_fmt)
logging.getLogger('matplotlib.font_manager').disabled = True

def testfun():
	print('haddock')

def plot_cv(data=None, fig=None, ax=None, labels=None, line=True, scatter=False, errs=False, current_column=1, potential_column=0, err_column=3, xunits='V', yunits=r'$mA/cm^2$', export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	"""
	Plot cyclic voltammetry data

	Parameters
	___________
	data: DataFrame or dict (default=None)
		Either a DataFrame containing CV data or a dict with DataFrames of CV data as values. Designed to be used seamlessly with the output of data.cv_process
	labels: array-like (default=None)
		List of labels to be used in the legend. If unspecified, keys of data are used as labels.
	line: bool (default=True)
		Whether to draw a line connecting the individual data points
	scatter: bool (default=False)
		Whether to draw a marker at each data point
	errs: bool (default=False)
		Whether to include an error bar at each data point
	current_column: int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column: int or str (default=0)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	err_column: int or str (default=3)
		Index or label of the column containing data to draw error bars. Used only if automatic column identification fails. Ignored if errs=False
	xunits: str (default='V')
		Units of the x-axis
	yunits: str (default=r'$mA/cm^2$')
		Units of the y-axis
	export_name: str, path object, or file-like (default=None)
		If specified, the figure will be saved as an image. Can either be a complete file path to save the image in a specific directory or a file name to save the image in the current directory
	export_type: str (default='png')
		File type to save the image as. Only used if export_name is specified and export_name does not include the file type
	fig_kw: dict
		Dict with keywords passed to the plt.subplots function to create the figure
	err_kw: dict
		Dict with keywords passed to the plt.errorbars function used to draw errorbars
	**plot_kw:
		all remaining keyword arguments are passed to the plt.plot or plt.scatter function used to draw the graphs

	Returns
	________
	fig: Figure
		Figure object containing all plot elements
	ax: Axes
		Axes object containing the plotted data
	"""
	if data is None:
		return None
	if not utils.check_dict(data):
		data = {'key':data}
	labels = check_labels(data, labels)
	if fig is None and ax is None:
		fig, ax = plt.subplots(**fig_kw)
	for l, df in zip(labels, list(data.values())):
		df.columns = utils.check_labels(df)
		x = datums.find_col(df, 'potential', potential_column)
		y = datums.find_col(df, 'current', current_column)
		yerr = check_errs(errs, df, 'current_err', err_column)
		plotter(ax, x, y, yerr, l, line, scatter, errs, err_kw, **plot_kw)
	if len(data) > 1:
		ax.legend(loc='best', edgecolor='k')
	ax.set_xlabel(build_axlabel('Potential', xunits))
	ax.set_ylabel(build_axlabel('Current Density', yunits))
	if export_name:
		fig_saver(export_name, export_type)
	return fig, ax

def polcurve(data=None, fig=None, ax=None, labels=None, line=True, scatter=True, errs=False, current_column=0, potential_column=1, err_column=3, xunits=r'$mA/cm^2$', yunits='V', export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	"""
	Plot polarization curves using chronopotentiometry data

	Parameters
	___________
	data: DataFrame or dict (default=None)
		Either a DataFrame containing CP data or a dict with DataFrames of CP data as values. Designed to be used seamlessly with the output of data.cp_process
	labels: array-like (default=None)
		List of labels to be used in the legend. If unspecified, keys of data are used as labels.
	line: bool (default=True)
		Whether to draw a line connecting the individual data points
	scatter: bool (default=False)
		Whether to draw a marker at each data point
	errs: bool (default=False)
		Whether to include an error bar at each data point
	current_column: int or str (default=0)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column: int or str (default=1)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	err_column: int or str (default=3)
		Index or label of the column containing data to draw error bars. Used only if automatic column identification fails. Ignored if errs=False
	xunits: str (default=r'$mA/cm^2$')
		Units of the x-axis
	yunits: str (default='V')
		Units of the y-axis
	export_name: str, path object, or file-like (default=None)
		If specified, the figure will be saved as an image. Can either be a complete file path to save the image in a specific directory or a file name to save the image in the current directory
	export_type: str (default='png')
		File type to save the image as. Only used if export_name is specified and export_name does not include the file type
	fig_kw: dict
		Dict with keywords passed to the plt.subplots function to create the figure
	err_kw: dict
		Dict with keywords passed to the plt.errorbars function used to draw errorbars
	**plot_kw:
		all remaining keyword arguments are passed to the plt.plot or plt.scatter function used to draw the graphs

	Returns
	________
	fig: Figure
		Figure object containing all plot elements
	ax: Axes
		Axes object containing the plotted data
	"""
	if data is None:
		return None
	if not utils.check_dict(data):
		data={'key':data}
	labels = check_labels(data, labels)
	if fig is None and ax is None:
		fig, ax = plt.subplots(**fig_kw)
	for l, df in zip (labels, list(data.values())):
		df.columns = utils.check_labels(df)
		x = datums.find_col(df, 'current', current_column)
		y = datums.find_col(df, 'potential', potential_column)
		yerr = check_errs(errs, df, 'potential_err', err_column)
		plotter(ax, x, y, yerr, l, line, scatter, errs, err_kw, **plot_kw)
	if len(data) > 1:
		ax.legend(loc='best', edgecolor='k')
	ax.set_xlabel(build_axlabel('Current Density', xunits))
	ax.set_ylabel(build_axlabel('Potential', yunits))
	if export_name:
		fig_saver(export_name, export_type)
	return fig, ax

def plot_cp_raw(data=None, fig=None, ax=None, labels=None, line=False, scatter=True, errs=False, current_column=2, potential_column=1,time_column=0, err_column=(4,5), xunits='s', yunits=('mA', 'V'), export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	"""
	Plot raw chronopotentiometry data

	Note: it is strongly reccomended to use this function with data from only a single test and the default values of line, scatter, and errs to avoid overplotting.

	Parameters
	___________
	data: DataFrame or dict (default=None)
		Either a DataFrame containing CP data or a dict with DataFrames of CP data as values. Designed to be used seamlessly with the output of data.cp_raw
	labels: array-like (default=None)
		List of labels to be used in the legend. If unspecified, keys of data are used as labels.
	line: bool (default=True)
		Whether to draw a line connecting the individual data points
	scatter: bool (default=False)
		Whether to draw a marker at each data point
	errs: bool (default=False)
		Whether to include an error bar at each data point
	current_column: int or str (default=2)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column: int or str (default=1)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	time_column: int or str (default=0)
		Index or label of the column containing time data. Used only if automatic column identification fails
	err_column: tuple or list of int or str (default=(4,5))
		Indices or labels of the columns containing data to draw error bars. Used only if automatic column identification fails. Ignored if errs=False
	xunits: str (default=r'$mA/cm^2$')
		Units of the x-axis
	yunits: tuple or list of str (default=('ma','V'))
		Units of the y-axis
	export_name: str, path object, or file-like (default=None)
		If specified, the figure will be saved as an image. Can either be a complete file path to save the image in a specific directory or a file name to save the image in the current directory
	export_type: str (default='png')
		File type to save the image as. Only used if export_name is specified and export_name does not include the file type
	fig_kw: dict
		Dict with keywords passed to the plt.subplots function to create the figure
	err_kw: dict
		Dict with keywords passed to the plt.errorbars function used to draw errorbars
	**plot_kw:
		all remaining keyword arguments are passed to the plt.plot or plt.scatter function used to draw the graphs

	Returns
	________
	fig: Figure
		Figure object containing all plot elements
	ax: Tuple
		Tuple of axes objects containing the plotted data
	"""
	if data is None:
		return None
	if not utils.check_dict(data):
		data = {'key': data}
	labels = check_labels(data, labels)
	if fig is None and ax is None:
		fig, ax = plt.subplots(**fig_kw)
	ax2 = ax.twinx()
	color1 = 'tab:red'
	color2 = 'tab:blue'
	for l, df in zip (labels, list(data.values())):
		x = datums.find_col(df, 'time', time_column)
		y1 = datums.find_col(df, 'potential', potential_column)
		y2 = datums.find_col(df, 'current', current_column)
		yerr1 = check_errs(errs, df, 'current_err', err_column[0])
		yerr2 = check_errs(errs, df, 'potential_err', err_column[1])
		plotter(ax, x, y1, yerr1, l, line, scatter, errs, err_kw, c=color1, **plot_kw)
		plotter(ax2, x, y2, yerr2, l, line, scatter, errs, err_kw, c=color2, **plot_kw)
	if len(data) > 1:
		ax.legend(loc='best', edgecolor='k')
	# color = 'tab:red'
	ax.set_xlabel(build_axlabel('Time', xunits))
	ax.set_ylabel(build_axlabel('Current Density', yunits[0]))
	ax2.set_ylabel(build_axlabel('Potential', yunits[1]))
	ax.tick_params(axis='y', labelcolor=color1)
	ax2.tick_params(axis='y', labelcolor=color2)
	if export_name:
		fig_saver(export_name, export_type)
	return fig, (ax, ax2)

def build_axlabel(base, units):
	"""
	Generate axis label

	Auxilliary function to generate an axis label from the specified name and units:
	'Base [units]'

	Parameters
	___________
	base: str
		Axis name
	units: str
		Axis units

	Returns
	________
	label:
		Complete axis label
	"""
	label =  base + ' [' + units + ']'
	return label

def check_errs(errs, df, err_name, err_col):
	"""
	Check if data set contains error data and return valid error data

	Auxilliary function to check if the given data set contains data that can be used to draw error bars. Returns the error values if possible, otherwise returns an array of zeros.

	Parameters
	___________
	errs: bool
		Whether data set should be checked for error data. If False, an array of zeros is returned.
	df: DataFrame
		DataFrame that should contain error data
	err_name: str
		String of the form '[datatype]_std' (ex: 'current_std'). Used to parse column labels of df
	err_col: int or str
		Index or label of the column containing data to draw error bars. Used only if automatic column identification fails. Ignored if errs=False

	Returns
	________
	err: numpy array
		Array of values which can be used to draw error bars. If valid error values could not be found, an array of zeros of the same length as df is returned
	"""
	count = df.shape[0]
	if errs:
		try:
			err = datums.find_col(df, err_name, err_col)
		except:
			err = np.zeros(count)
			_log.warning('Unable to use the specified error values')
	else:
		err = np.zeros(count)
	return err

def check_labels(data, labels=None):
	"""
	Check if the specified labels are valid

	Auxilliary functin to checks if the user-specified labels can be used to create the legend. If unspecified or lengths of data and labels are mismatched, dict keys of data are used as default labels.

	Parameters
	___________
	data: dict
		Dict with data to be plotted as values
	labels:list-like
		List of labels to be used in the legend. If unspecified, keys of data are used as labels.

	Returns
	________
	labels:
		Valid list of labels for use in the legend
	"""
	if labels and (len(labels) != len(data)):
		labels = list(data.keys())
		_log.warning('labels and data must have the same length. Using default labels instead of specified labels')
	elif labels is None:
		labels = list(data.keys())
	return labels

def fig_saver(export_name, export_type='png'):
	"""
	Save the current figure

	Auxilliary function to save the current figure as an image.

	export_name: str, path object, or file-like
		File name to save the image as. Can either be a complete file path to save the image in a specific directory or a file name to save the image in the current directory
	export_type: str (default='png')
		File type to save the image as. Only used if export_name does not include the file type
	"""
	if '.' not in export_name:
		export_type = export_type.replace('.','')
		export_name = export_name + '.' + export_type
	plt.savefig(export_name, bbox_inches='tight')

def plotter(ax, x, y, e, l, line, scatter, errs, err_kw, **plot_kw):
	"""
	Plot data

	Auxilliary function to plot the specified data

	Parameters
	___________
	ax: Axes
		Axes object on which to plot the data
	x: array-like
		x values
	y: array-like
		y values
	e: array-like
		Error values used to draw error bars
	l: array-like
		Labels to be used in the legend
	line: bool
		Whether to draw a line connecting the individual data points
	scatter: bool
		Whether to draw a marker at each data point
	errs: bool
		Whether to include an error bar at each data point
	err_kw: dict
		Dict with keywords passed to the plt.errorbars function used to draw errorbars
	**plot_kw:
		all remaining keyword arguments are passed to the plt.plot or plt.scatter function used to draw the graphs
	"""
	if 'marker' not in plot_kw:
			plot_kw['marker'] = '.'
	if errs:
		if 'elinewidth' not in err_kw:
			err_kw['elinewidth'] = 0.5
		if 'capthick' not in err_kw:
			err_kw['capthick'] = 0.5
		if 'capsize' not in err_kw:
			err_kw['capsize'] = 3
		if line and scatter:
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
		elif line:
			plot_kw.pop('marker')
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
		else:
			plot_kw['ls'] = ''
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
	else :
		if line and scatter:
			ax.plot(x, y, label=l, **plot_kw)
		elif line:
			plot_kw.pop('marker')
			ax.plot(x, y, label=l, **plot_kw)
		else:
			ax.scatter(x, y, label=l, **plot_kw)