import os
import sys
import json
import pickle
#import pandas as pd
#from .processor import *
#from .path import file_out

import datetime
import pathlib
import tkinter, tkinter.filedialog, tkinter.messagebox

"""
SSPファイル名の決め方
SSP_のあとに固有識別名を入れる。
SSP_default.jsonは使用禁止。
"""


#============================================================================================#
#============================================================================================#
#============================================================================================#
def load_data(*path):
    """Summary line.
    Read a pkl file.

    Parameters
    ----------
    *path : str
        path to pkl file.
    Returns
    -------
    pkl data

    note
    ------
    - If you do not specify the path, specify the file in the GUI.
    """
    if not path:
        root = tkinter.Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)
        fileType = [("", "*.pkl")]
        startdir = pathlib.Path.home()
        p = tkinter.filedialog.askopenfilenames(filetypes = fileType,initialdir = startdir)
        if len(p) == 1:
            with open(p[0], "rb") as f:
                data = pickle.load(f)
            print(p[0])
        else:
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(pickle.load(f))
                print(i)
            
    else:
        if len(path) == 1:
            p = pathlib.Path(path[0])
            with open(p.resolve(), "rb") as f:
                data = pickle.load(f)
        else:
            p = [pathlib.Path(i).resolve() for i in path]
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(pickle.load(f))
    return data

def load_cfg(*path):
    """Summary line.
    Read a cfg file.

    Parameters
    ----------
    *path : str
        path to pkl file.
    Returns
    -------
    pkl data

    note
    ------
    - If you do not specify the path, specify the file in the GUI.
    - The cfg file is a json file that describes parameters such as filtering processing.
    """
    if not path:
        root = tkinter.Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)
        fileType = [("", "*.json")]
        startdir = pathlib.Path.home()
        p = tkinter.filedialog.askopenfilenames(filetypes = fileType,initialdir = startdir)
        if len(p) == 1:
            with open(p[0], "rb") as f:
                data = json.load(f)
            print(p[0])
        else:
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(json.load(f))
                print(i)
    else:
        if len(path) == 1:
            p = pathlib.Path(path[0])
            with open(p.resolve(), "rb") as f:
                data = json.load(f)
        else:
            p = [pathlib.Path(i).resolve() for i in path]
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(json.load(f))
    return data

def load_id(*path):
    """Summary line.
    Read a id file.

    Parameters
    ----------
    *path : str
        path to id file.
    Returns
    -------
    pkl data

    note
    ------
    - If you do not specify the path, specify the file in the GUI.
    - The id file is a json file that describes subject data.
    """
    if not path:
        root = tkinter.Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)
        fileType = [("", "*.json")]
        startdir = pathlib.Path.home()
        p = tkinter.filedialog.askopenfilenames(filetypes = fileType,initialdir = startdir)
        if len(p) == 1:
            with open(p[0], "rb") as f:
                data = json.load(f)
            print(p[0])
        else:
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(json.load(f))
                print(i)
    else:
        if len(path) == 1:
            p = pathlib.Path(path[0])
            with open(p.resolve(), "rb") as f:
                data = json.load(f)
        else:
            p = [pathlib.Path(i).resolve() for i in path]
            data = []
            for i in p:
                with open(i, "rb") as f:
                    data.append(json.load(f))
    return data


def save_pkl(data, path):
    """Summary line.
    Save the pkl file.
    This function is used when the measurement data is added or modified.

    Parameters
    ----------
    path : str

    Returns
    -------
    None

    note
    ------
    - If you want to save the file hoge.pkl on your desktop, set the path as follows.
        "C: /Users/username/Desktop/hoge.pkl"
    - For Windows OS user.
        Backslash (/) is treated as an escape character, so prefix r.
    """
    if "modified_count" not in  data.keys():
        data["ID"]["modified_1"] = str(datetime.datetime.today())
        data["modified_count"] = 1
    else:
        data["modified_count"] += 1
        count = data["modified_count"]
        data["ID"]["modified_{}".format(count)] = str(datetime.datetime.today())
    p = pathlib.Path(path)
    datadir = p.parent
    files = []
    for i in datadir.glob("*"):
        if i.is_file():
            files.append(i.name.split(".")[0])
    if str(p.stem) in files:
        print("The file you input already exists")
        print("Do you want to overwrite ?")
        answer = str(input("y or n : " ))
        if answer.lower() == "y":
            print("Continue the saving process.")
            import pickle
            with open('{}'.format(p), mode='wb') as f:
                pickle.dump(data, f, protocol=4)
            print("File conversion and save succeeded.")
        elif answer.lower() == "n":
            print("Saving process was interrupted.")
    else:
        import pickle
        with open('{}'.format(p), mode='wb') as f:
            pickle.dump(data, f, protocol=4)
        print("File conversion and save succeeded.")

def extract_data(data):
    """Summary line.
    Output data from humo instance.
    The output data has the same data structure as the pkl file.
    (The data required for humo instance generation is included.)

    Parameters
    ----------
    data : dic
        dic from humo instance.

    Returns
    -------
    pkl data

    note
    ------
    - If you add or modify data while analyzing with humo instance,
    save the dictionary data output from this function using the save_pkl function.
    - If you want to add other information, set key and value and save.
    """
    pkl = {}
    pkl["device"] = [data._device, data.deviceheader]
    pkl["model"] = [data._model, data.modelheader]
    pkl["marker"] = [data._marker, data.mkheader]
    pkl["spep"] = data._spep
    pkl["MMT"] = data._mvc
    pkl["rawMMT"] = data._MMTraw
    pkl["ID"] = data._ID
    pkl["EMG_name"] = data._emg_name
    return pkl

# 廃止機能
#"""
#Initial setting.
#Set the data directory.
#"""
#
#def set_data_directory(dir_,name = "SSP"):
#	if name == "SSP":
#		ssp = SSP(name)
#		defaultSSP = ssp.getSSP()
#		defaultSSP["data_path"] = dir_
#		ssp.overwriteSSP(defaultSSP)
#	else:
#		ssp = SSP(name)
#		defaultSSP = ssp.getSSP()
#		defaultSSP["data_path"] = dir_
#		ssp.mySSP = defaultSSP
#		ssp.save_mySSP(name)
#	return

#def save_data(data, *file_path):
#	if "modified_count" not in  data.keys():
#		data["ID"]["modified_1"] = str(datetime.datetime.today())
#		data["modified_count"] = 1
#	else:
#		data["modified_count"] += 1
#		count = data["modified_count"]
#		data["ID"]["modified_{}".format(count)] = str(datetime.datetime.today())
#	filename = str(input("Input file name : ")) + ".pkl"
#	existingfile = file_out(*file_path)
#	abspath = homedir.joinpath(*file_path)
#	os.chdir(abspath)
#	if filename in existingfile:
#		print("The file you input already exists")
#		print("Do you want to overwrite ?")
#		answer = str(input("y or n :"))
#		if answer.lower() == "y":
#			print("Continue the saving process.")
#			import pickle
#			with open(filename, mode="wb") as f:
#				pickle.dump(data, f, protocol=4)
#			print("Saving process is succceeded.")
#	else:
#		print("Save as a new file.")
#		import pickle
#		with open(filename, mode="wb") as f:
#			pickle.dump(data, f, protocol=4)
#		print("Saving process is succceeded.")

#def reading_pkl(name):
#	"""Summary line.
#	The reading_pkl function reads a pkl file in the current working directory.
#	You can also read the absolute path of a pkl file.
#	Parameters
#	----------
#	name : str
#		File name or absolute file path
#
#	Returns
#	-------
#	pkl data : dictionary
#		pkl data converted by fileconverter
#	"""
#	with open(name,"rb") as f:
#		data = pickle.load(f)
#	return data

#def loading_partial_data(file_name,target=[True,True,True],*file_path):
#	"""Summary line.
#	Load measurement data that exists in the specified directory.
#
#	Parameters
#	----------
#	file_name : str or list
#
#	Returns
#	-------
#	measurement data : pkl or list
#		When multiple files are specified in list type,
#		it is output in list type.
#		When specified as a single file, pkl data is output.
#	"""
#	cwd = os.getcwd()
#	filepath = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("..","_MeasurementData")
#	datapath = filepath.joinpath(*file_path)
#	os.chdir(datapath)
#
#	if type(file_name) == list:
#		data = []
#		for i in file_name:
#			with open("{}.pkl".format(i.split(".")[0]), 'rb') as f:
#				data.append(pickle.load(f))
#	else:
#		with open("{}.pkl".format(file_name), 'rb') as f:
#			data = pickle.load(f)
#	os.chdir(cwd)
#	if target[0] == True:
#		pass
#	else:
#		data["device"][0] = None
#	if target[1] == True:
#		pass
#	else:
#		data["model"][0] = None
#	if target[2] == True:
#		pass
#	else:
#		data["marker"][0] = None
#	return data

#def loading_abs(file_name, SSPname = "SSP", ASPname = "ASP"):
#	"""Summary line.
#	Load measurement data that exists in the specified directory and SSP and ASP file.
#
#	Parameters
#	----------
#	file_name : str or list.
#		File name of the data to be read. The file name does not require an extension.
#	SSP : str
#		name of SSP file.
#	ASP : str
#		name of ASP file.
#	file_path : str
#		variable-length argument.
#
#	Returns
#	-------
#	measurement data : pkl or list
#		When multiple files are specified in list type,
#		it is output in list type.
#		When specified as a single file, pkl data is output.
#	ASP file.
#	SSP file.
#	"""
#	data = loading_absdata(file_name)
#	a, b = settings(SSPname, ASPname)
#	return data, a, b

#def loading_absdata(file_name):# doc stringsを修正する
#	"""Summary line.
#	Load measurement data that exists in the specified directory.
#
#	Parameters
#	----------
#	file_name : str or list
#
#	Returns
#	-------
#	measurement data : pkl or list
#		When multiple files are specified in list type,
#		it is output in list type.
#		When specified as a single file, pkl data is output.
#	"""
#
#	if type(file_name) == list:
#		data = []
#		for i in file_name:
#			with open("{}.pkl".format(i), 'rb') as f:
#				data.append(pickle.load(f))
#	else:
#		with open("{}.pkl".format(file_name), 'rb') as f:
#			data = pickle.load(f)
#	return data
#
#def loadings(file_name, file_path, SSPname="SSP", ASPname="ASP" ):
#	"""Summary line.
#	Load measurement data that exists in the specified directory and SSP and ASP file.
#
#	Parameters
#	----------
#	file_name : str or list.
#		File name of the data to be read. The file name does not require an extension.
#	SSP : str
#		name of SSP file.
#	ASP : str
#		name of ASP file.
#	file_path : str
#		variable-length argument.
#
#	Returns
#	-------
#	measurement data : pkl or list
#		When multiple files are specified in list type,
#		it is output in list type.
#		When specified as a single file, pkl data is output.
#	ASP file.
#	SSP file.
#	"""
#	if type(file_name) == list:
#		data = []
#		for i in file_name:
#			data.append(loading_data(i.split(".")[0],file_path,SSPname))
#	else:
#		data = loading_data(file_name, file_path, SSPname)
#	a, b = settings(SSPname, ASPname)
#	return data, a, b

#def loading_data(file_name,file_path,sspfile="SSP"):
#    """Summary line.
#	Load measurement data that exists in the specified directory.
#
#	Parameters
#	----------
#	file_name : str or list
#
#	Returns
#	-------
#	measurement data : pkl or list
#		When multiple files are specified in list type,
#		it is output in list type.
#		When specified as a single file, pkl data is output.
#	"""
#	cwd = os.getcwd()
#	if ("Anaconda3" in os.path.dirname(__file__)) or ("anaconda3" in os.path.dirname(__file__) or ("miniconda" in os.path.dirname(__file__))):
#		ssp = SSP(sspfile)
#		filepath = Path.home() /ssp.getSSP()["data_path"]
#		datapath = filepath.joinpath(file_path)
#		os.chdir(datapath)
#	elif "site-packages" in os.path.dirname(__file__):
#		ssp = SSP(sspfile)
#		filepath = Path.home() /ssp.getSSP()["data_path"]
#		datapath = filepath.joinpath(file_path)
#		os.chdir(datapath)
#	elif "/root" in str(Path.home()):
#		ssp = SSP(sspfile)
#		filepath = Path(ssp.getSSP()["data_path"])
#		datapath = filepath.joinpath(file_path)
#		os.chdir(datapath)
#	else:
#		ssp = SSP("SSP_")
#		filepath = Path.home() /ssp.getSSP()["data_path"]
#		datapath = filepath.joinpath(file_path)
#		os.chdir(datapath)
#		#filepath = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("..","_MeasurementData")
#		#datapath = filepath.joinpath(*file_path)
#		#os.chdir(datapath)
#
#	if type(file_name) == list:
#		data = []
#		for i in file_name:
#			with open("{}.pkl".format(i.split(".")[0]), 'rb') as f:
#				data.append(pickle.load(f))
#	else:
#		with open("{}.pkl".format(file_name), 'rb') as f:
#			data = pickle.load(f)
#	os.chdir(cwd)
#	return data

# SSP, ASPファイルを読み込む
#def load_cfg():
#	root = tkinter.Tk()
#	root.withdraw()
#	root.call('wm', 'attributes', '.', '-topmost', True)
#	fileType = [("", "json")]
#	#cdir = os.path.abspath(os.path.dirname(__file__))
#	startdir = pathlib.Path.home()
#	tkinter.messagebox.showinfo("humo","Please select cfg file.")
#	cfg_path = tkinter.filedialog.askopenfilename(
#										filetypes = fileType,
#										initialdir = startdir
#	)
#	#ssp = pathlib.Path(ssp)
#	#if ssp == "":
#	#	sys.exit(1)
#	#else:
#	#	pass
#	with open(cfg_path) as f:
#		cfg = json.load(f)
#	#root = tkinter.Tk()
#	#root.withdraw()
#	#root.call('wm', 'attributes', '.', '-topmost', True)
#	#fileType = [("", "json")]
#	##cdir = os.path.abspath(os.path.dirname(__file__))
#	#tkinter.messagebox.showinfo("humo","Please select a ASP file.")
#	#asp = tkinter.filedialog.askopenfilename(
#	#									filetypes = fileType,
#	#									initialdir = startdir
#	#)
#	#if asp == "":
#	#	sys.exit(1)
#	#else:
#	#	pass
#	##asp = pathlib.Path(asp)
#	#with open(asp) as f:
#	#	asp = f.read()
#	return cfg