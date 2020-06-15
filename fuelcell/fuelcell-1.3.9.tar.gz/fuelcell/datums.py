import numpy as np
import pandas as pd
import os
import re

from . import utils

dlm_default = utils.dlm_default
col_default_labels = {'current':'i', 'potential':'v', 'time':'t', 'current_err':'i_sd', 'potential_err':'v_sd'}
col_default_ids = {'current':2, 'potential':1, 'time':0, 'current_err':2, 'potential_err':3}
ref_electrodes = {'she':0, 'sce':0.241}


def testfun():
	print('thomson (no p)')

def ca_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads chronoamperometry data

	Efficient way to load multiple CA files at once;equivalent to calling load_data and specifying expt_type='ca'. If called with no arguments, loads all ca files in the present folder.

	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).

	Returns
	________
	data: DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame. If multiple files are read, a dictionary is returned with the file names as keys and DataFrames as values.
	"""
	data = load_data(filename, folder, pattern, 'ca', filetype, delimiter)
	return data

def ca_process(data=None, current_column=2, potential_column=1, area=5, reference='she', export_data=False, save_dir='processed', threshold=5, min_step_length=50, pts_to_average=300, pyramid=False, **kwargs):
	"""
	Processes chronoamperometry data

	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'ca' files in the present folder. See process_steps for details on the operations performed.

	Parameters
	___________
	data: DataFrame or dict
		Either a DataFrame containing CA data or a dict with DataFrames of CA data as values. If unspecified, data will be loaded using ca_raw before processing. Designed to be used seamlessly with the output of ca_raw
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=2)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	**kwargs:
		Remaining arguments are passed to ca_raw to load data
	"""
	if data is None:
		data = ca_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		ca_processed = process_steps(df, potential_column, current_column, threshold, min_step_length, pts_to_average, pyramid, 'ca', area, reference)
		newdata[k] = ca_processed
		if export_data:
			utils.save_data(ca_processed, k+'.csv', save_dir)
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cp_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads chronopotentiometry data

	Efficient way to load multiple CP files at once;equivalent to calling load_data and specifying expt_type='cp'. If called with no arguments, loads all cp files in the present folder.

	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\\t')
		Delimiting character if the file is a text file. Defaults to '\\t' (tab-delimiting).

	Returns
	________
	data: DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame. If multiple files are read, a dictionary is returned with the file names as keys and DataFrames as values.
	"""
	data = load_data(filename, folder, pattern, 'cp', filetype, delimiter)
	return data

def cp_process(data=None, current_column=2, potential_column=1, area=5, reference='she', export_data=False, save_dir='processed', threshold=5, min_step_length=25, pts_to_average=300, pyramid=True, **kwargs):
	"""
	Processes chronopotentiometry data

	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'cp' files in the present folder. See process_steps for details on the operations performed.

	Parameters
	___________
	data: DataFrame or dict
		Either a DataFrame containing CP data or a dict with DataFrames of CP data as values. If unspecified, data will be loaded using cp_raw before processing. Designed to be used seamlessly with the output of cv_raw
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=2)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	**kwargs:
		Remaining arguments are passed to cp_raw to load data
	"""
	if data is None:
		data = cp_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		cp_processed = process_steps(df, current_column, potential_column, threshold, min_step_length, pts_to_average, pyramid, 'cp', area, reference)
		newdata[k] = cp_processed
		if export_data:
			utils.save_data(cp_processed, k+'.csv', save_dir)
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cv_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	"""
	Loads cyclic voltammetry data

	Efficient way to load multiple CV files at once;equivalent to calling load_data and specifying expt_type='cv'. If called with no arguments, loads all cv files in the present folder.

	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).

	Returns
	________
	data: DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame. If multiple files are read, a dictionary is returned with the file names as keys and DataFrames as values.
	"""
	data = load_data(filename, folder, pattern, 'cv', filetype, delimiter)
	return data

def cv_process(data=None, current_column=1, potential_column=0, area=5, reference='she', export_data=False, save_dir='processed', **kwargs):
	"""
	Processes cyclic voltammetry data

	Can either process pre-loaded data or load and process data files. If called with no arguments, loads and processes all 'cv' files in the present folder. Peforms the following operations in order:
	1. Parse column labels to find columns containing current and potential data. If parsing fails, specified labels/indices are used
	2. Convert current to current density using the specified area

	Parameters
	__________
	data : DataFrame or dict
		Either a DataFrame containing CV data or a dict with DataFrames of CV data as values. If unspecified, data will be loaded using cv_raw before processing. Designed to be used seamlessly with the output of cv_raw
	area : int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to durrent density
	current_column : int or str (default=1)
		Index or label of the column containing current data. Used only if automatic column identification fails
	potential_column : int or str (default=0)
		Index or label of the column containing potential data. Used only if automatic column identification fails
	**kwargs:
		Remaining arguments are passed to cv_raw to load data
	
	Returns
	_______
	newdata: DataFrame or dict
		If a single file is processed, it is returned directly as a pandas DataFrame. If multiple files are orocessed, a dictionary is returned with the file names as keys and DataFrames as values.
	"""
	if data is None:
		data = cv_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		current = find_col(df, 'current', current_column)
		current = current / area
		potential = find_col(df, 'potential', potential_column)
		potenial = electrode_correct(potential, reference)
		cv_processed = pd.DataFrame({'i':current,'v':potential})
		newdata[k] = cv_processed
		if export_data:
			utils.save_data(cv_processed, k+'.csv', save_dir)
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def array_apply(arr, func, **kwargs):
	"""
	Applies a function to each value in an array

	Parameters
	___________
	arr: array-like
		Array to which function will be applied
	func: function
		function to apply to each value
	**kwargs:
		Any other arguments required by the specified function

	Returns
	________
	result: numpy array
		Array of the transformed values
	"""
	result =  np.array([func(a, **kwargs) for a in arr])
	return result

def avg_last_pts(arr, numpts=300):
	"""
	Average of the last several values of an array

	Auxilliary function to compute the average of an array accross the last several data points. Useful for obtaining a steady-state average.

	Parameters
	___________
	arr: list or numpy array
		Array of values used to compute the average.
	numpts: int (default=300)
		Average is calculated using the last numpts values of the array.

	Returns
	________
	avg: float
		Average of the last several values
	"""
	if type(arr) == list:
		arr = np.array(arr)
	avg = np.mean(arr[-numpts:])
	return avg

def find_col(data, col_type, label=None):
	"""
	Finds column containing the desired measurement

	Parameters
	___________
	data: DataFrame
		DataFrame containing the full data set
	col_type: {'current', 'potential', 'time', 'current_err', 'potential_err'}
		Type of data being searched for
	label: str or int (default=None)
		Label or index of the desired column if the column label cannot be automatically parsed

	Returns
	________
	col: numpy array
		Array of the desired measurement values
	"""
	default_label = col_default_labels[col_type]
	default_id = col_default_ids[col_type]
	newdf = data.copy()
	newdf.columns = utils.check_labels(newdf)
	if default_label in newdf.columns:
		col = newdf[default_label]
	elif label:
		if utils.check_str(label):
			col = newdf[label]
		else:
			col = newdf.iloc[:,label]
	else:
		col = newdf.iloc[:, default_id]
	col = np.array(col)
	return col

def find_steps(arr, threshold=5):
	"""
	Find indices at which an array of roughly stepwise data changes values

	Auxilliary function to find the points at which curren/voltage is stepped up or down during and experiment. Identifies 'steps' by determining the points at which the consecutive absolute difference between array values is greater than a specified threshold.

	Parameters
	___________
	arr: list or numpy array
		Array of roughly stepwise data
	threshold: int or float  (default=5)
		Minimum consecutive absolute difference which constitutes a step

	Returns
	________
	splits: numpy array
		Indices at which the array steps up or down
	"""
	if type(arr) == list:
		arr = np.array(arr)
	diffs = np.abs(np.diff(arr))
	splits = np.where(diffs > threshold)[0] + 1
	return splits

def load_data(filename=None, folder=None, pattern='', expt_type='', filetype='', delimiter=dlm_default):
	"""
	Loads data file(s) as a pandas DataFrame

	Function to load data files as a pandas DataFrame. If called with no
	arguments, loads all supported data files in the present folder.

	Parameters
	___________
	filename: str, path object, or file-like (default=None)
		Full filename of a file in the present directory or a complete path to an individual file. If filename is specified, all other arguments except delimiter are ignored.
	folder: str, path object, or path-like (default=None)
		Directory in which data files are stored. If none, defaults to the present directory.
	pattern: str or regex
		If specified, only files matching this pattern in the specified folder are loaded. Ignored if filename is specified.
	expt_type: str (default='')
		Alternative to specifying pattern; ignored if pattern is specified. All files containing expt_type anywhere in the file name will be loaded. Ex: to load all chronopotentiometry files, specify expt_type='cp'.
	filetype : str
		Any supported filetype. Only files of the specified file type will be loaded. Can be used in conjunction with pattern or expt_type.
	delimiter : char (default = '\t')
		Delimiting character if the file is a text file. Defaults to '\t' (tab-delimiting).

	Returns
	________
	data: DataFrame or dict
		If a single file is read, it is returned directly as a pandas DataFrame. If multiple files are read, a dictionary is returned with the file names as keys and DataFrames as values.
	"""
	data = None
	if filename:
		name, data = utils.read_file(filename, delimiter)
	else:
		if folder:
			dirpath = os.path.realpath(folder)
		else:
			dirpath = os.getcwd()
		if expt_type and not pattern:
			pattern = r'.*' + expt_type + r'.*'
		files = utils.get_files(dirpath, pattern, filetype)
		data = dict()
		for f in files:
			path = os.path.join(dirpath, f)
			name, df = utils.read_file(path, delimiter)
			if df is not None:
				data[name] = df
		if len(data) == 1:
			data = list(data.values())[0]
	return data

def process_steps(data, control_column=0, response_column=1, threshold=5, min_step_length=25, pts_to_average=300, pyramid=True, expt_type='cp', area=None, reference='she'):
	"""
	Processes stepwise data (ex chronopotentiometry and chronoamperometry data)

	Performs the following operations in order:
	1. Parse column labels to find the columns containing the desired data. If automatic parsing fails, the specified column labels/indices are used.
	2. Find the points at which the independent variable steps up or down using the specified threshold value.
	3. Split the data  at these split points. Holds with fewer than the minimum number of points are filtered out to account for outliers. Note: splitting is based upon values of the independent variable, so this will not result in the loss of meaningful data.
	4. Average and standard deviation are calculated using the last several points of each step to obtain steady-state values.
	5. If the indpendent variable is ramped up and down, the steady-state average and standard deviation are calculated across both the ramp-up and ramp-down holds. 
	6. Any necessary scaling or transformations are performed (ex. reference electrode correction, coversion to current density, etc.)

	Parameters
	___________
	data: DataFrame
		Dataframe containing the data to be processed
	control_column: int or str (default=0)
		Label or index of the column containing the control/independent variable values
	response_column: int or str (default=1)
		Label or index of the column cotaining the response/dependent variabble values
	threshold: int (default=5)
		Minimum consecutive absolute difference which constitutes a step
	min_step_length: int (default=25)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	pts_to_average: int (default=300)
		Steady-state average and sd are calculated using the last pts_to_average values of the array. Default is 300 points, which is the last 30 seconds of each hold at the instrument's default collection rate of 10 Hz.
	pyramid: bool (default=True)
		Specifies whether the current is ramped in both directions. Set pyramid=False if only ramping up or only ramping down.
	expt_type: {'cp', 'ca'} (default='cp')
		Specifies the type of experiment being analyzed. This is used to determine which variables are the control and response variables.
	area: int or float (default=5)
		Geometric active area of the MEA. Scaling factor to convert current to current density.
	reference: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	"""
	if expt_type == 'ca':
		control_var = 'potential'
		response_var = 'current'
	elif expt_type == 'cp': 
		control_var = 'current'
		response_var = 'potential'
	control = np.array(find_col(data, control_var, control_column))
	response = np.array(find_col(data, response_var, response_column))
	split_pts = find_steps(control, threshold=threshold)
	control_steps = split_and_filter(control, split_pts, min_length=min_step_length)
	response_steps = split_and_filter(response, split_pts, min_length=min_step_length)
	control_avg = array_apply(control_steps, avg_last_pts, numpts=pts_to_average)
	response_avg = array_apply(response_steps, avg_last_pts, numpts=pts_to_average)
	control_std = array_apply(control_steps, std_last_pts, numpts=pts_to_average)
	response_std = array_apply(response_steps, std_last_pts, numpts=pts_to_average)	
	# if expt_type == 'ca':
	# 	split_pts = find_steps(potential, threshold=threshold)
	# elif expt_type == 'cp':
	# 	split_pts = find_steps(current, threshold=threshold)
	# current_steps = split_and_filter(current, split_pts, min_length=min_step_length)
	# potential_steps = split_and_filter(potential, split_pts, min_length=min_step_length)
	# current_avg = array_apply(current_steps, avg_last_pts, numpts=pts_to_average)
	# potential_avg = array_apply(potential_steps, avg_last_pts, numpts=pts_to_average)
	# current_std = array_apply(current_steps, std_last_pts, numpts=pts_to_average)
	# potential_std = array_apply(potential_steps, std_last_pts, numpts=pts_to_average)
	if pyramid:
		sort_idx = np.argsort(control_avg)
		control_avg = control_avg[sort_idx]
		response_avg = response_avg[sort_idx]
		control_std = control_std[sort_idx]
		response_std = response_std[sort_idx]
		split_pts = find_steps(control_avg, threshold=2)
		# if expt_type == 'ca':
		# 	split_pts = find_steps(potential_avg, threshold=2)
		# elif expt_type == 'cp':
		# 	split_pts = find_steps(current_avg, threshold=2)
		control_steps = split_and_filter(control_avg, split_pts)
		response_steps = split_and_filter(response_avg, split_pts)
		control_std_steps = split_and_filter(control_std, split_pts)
		response_std_steps = split_and_filter(response_std, split_pts)
		control_avg = array_apply(control_steps, np.mean)
		response_avg = array_apply(response_steps, np.mean)
		control_std = array_apply(control_std_steps, std_agg)
		response_std = array_apply(response_std_steps, std_agg)
	# current_avg = current_avg / area
	# current_std = current_std / area
	if expt_type == 'ca':
		if reference:
			control_avg = electrode_correct(control_avg, reference)
		response_avg = response_avg / area
		response_std = response_std / np.sqrt(area)
		processed = pd.DataFrame({'i':response_avg, 'v':control_avg, 'i_sd':response_std, 'v_sd':control_std})
	elif expt_type == 'cp':
		if reference:
			response_avg = electrode_correct(response_avg, reference)
		control_avg = control_avg / area
		control_std = control_std / np.sqrt(area)
		processed = pd.DataFrame({'i':control_avg, 'v':response_avg, 'i_sd':control_std, 'v_sd':response_std})
	return processed

def electrode_correct(arr, ref='she'):
	"""
	Corrects for the reference electrode

	Parameters
	___________
	arr: list or numpy array
		Array of potential values to which the correction will be applied
	ref: {'she', 'sce'}, int, or float (default='she')
		Either a string identifying the reference electrode (ie 'she' or 'sce'), or the potential of the reference electrode used. sce=0.241
	"""
	if type(arr) == list:
		arr = np.array(arr)
	corrected = arr
	if utils.check_str(ref):
		ref = ref.lower()
		try:
			corrected += ref_electrodes[ref]
		except KeyError:
			pass
	elif utils.check_float(ref) or utils.check_int(ref):
		corrected += ref
	return corrected

def split_and_filter(arr, split_pts, min_length=0):
	"""
	Split continuous array at the specified points.

	Auxilliary function to split continuous current or voltage data into individual holds. Splits the array at the specified indices and discards resulting arrays which are shorter than the required minimum length.

	Parameters
	___________
	arr: list or numpy array
		Array to split
	split_pts: int or array-like
		Indices at which to split the array
	min_length: int (default=0)
		Minimum length of the arrays which result from spliting the intial array. Arrays shorter than this value will be discarded
	
	Returns
	________
	steps: numpy array
		Array containing one array for each hold/step
	"""
	if type(arr) == list:
		arr = np.array(arr)
	steps = np.split(arr, split_pts)
	steps = np.array([s for s in steps if len(s) > min_length])
	return steps

def std_agg(arr):
	"""
	Aggregate standard deviations of multiple measurements.

	Auxilliary function to calculate the aggregate standard deviation of multiple measuremtns. Assumes that the measurements are independent of each other

	Parameters
	___________
	arr: list or numpy array
		Array of standard deviations to be aggregated

	Returns
	________
	sd: float
		Aggregated standard deviation
	"""
	if type(arr) == list:
		arr = np.array(arr)
	sd = np.sqrt(np.sum(arr**2))
	return sd

def std_last_pts(arr, numpts=300):
	"""
	Standard deviation of the last several values of an array

	Auxilliary function to compute the standard deviation of an array accross the last several data points. Useful for obtaining a steady-state standard deviation.

	Parameters
	___________
	arr: list or numpy array
		Array of values used to compute the standard deviation.
	numpts: int (default=300)
		Standard deviation is calculated using the last numpts values of the array.

	Returns
	________
	sd: float
		Standard deviation of the last several values
	"""
	if type(arr) == list:
		arr = np.array(arr)
	sd = np.std(arr[-numpts:], ddof=1)
	return sd