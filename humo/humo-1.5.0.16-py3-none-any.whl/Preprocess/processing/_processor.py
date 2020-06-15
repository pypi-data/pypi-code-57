import functools
import pandas as pd
import numpy as np
import os
import glob
from . import MMT_Error_msg
import sys

msg = MMT_Error_msg.MMT_Error_msg()

def sp_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            num = []
            for target in ["Device", "Model Outputs", "Trajectories"]:
                num.append(args[0].data[args[0].data[0].str.contains(target) == True].index.values[0])
            return num
        except IndexError:
            msg.sp_process()
            sys.exit("flag error")
    return wrapper

def sp_process4MVC(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        num = []
        try:
            for target in ["Device","Trajectories","Joints","Segments"]:
                num.append(args[0].data[args[0].data[0].str.contains(target) == True].index.values[0])
        except IndexError:
            pass
        num.sort()
        if len(num) == 1:
            last_number = len(args[0].data[0].values[5:])
            return [0, last_number]
            #msg.sp_process4MVC()
            #sys.exit("flag error")
        else:
            return num[:2]
    return wrapper

def length_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sp = args[0].getStartPoint()
        DeviceLength = sp[1] - sp[0] - 5
        PointLength = sp[2] - sp[1] - 5
        return [DeviceLength, PointLength]
    return wrapper

def length_process4MVC(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sp = args[0].getStartPoint()
        DeviceLength = sp[1] - sp[0]
        return DeviceLength
    return wrapper



def readingData(types):
    def readingData_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if types == "device":
                sp = args[0].getStartPoint()[0]
                DeviceLength = args[0].getDataLength()[0]
                data = pd.read_csv("{}.csv".format(args[0].file_name),
                                    sep=",",
                                    header = sp + 2,
                                    nrows = DeviceLength + 2,
                                    index_col = 0,
                                    dtype=object)[62:-60]
                return data.astype("float32")
            elif types == "model":
                sp = args[0].getStartPoint()[1]
                PointLength = args[0].getDataLength()[1]
                data = pd.read_csv("{}.csv".format(args[0].file_name),
                                    sep=",",
                                    header = sp + 2,
                                    nrows = PointLength + 2,
                                    index_col = 0,
                                    dtype=object)[6:-6]
                return data.astype("float32")
            elif types == "marker":
                sp = args[0].getStartPoint()[2]
                PointLength = args[0].getDataLength()[1]
                data = pd.read_csv("{}.csv".format(args[0].file_name),
                                    sep=",",
                                    header = sp + 2,
                                    nrows = PointLength + 2,
                                    index_col = 0,
                                    dtype=object)[6:-6]
                return data.astype("float32")
        return wrapper
    return readingData_

def readingData4MVC(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sp = args[0].getStartPoint()[0]
        DeviceLength = args[0].getDeviceLength()
        skip_rows = list(np.arange(DeviceLength+1,len(args[0].data)))
        data = pd.read_csv("{}.csv".format(args[0].file_name),
                            sep=",",
                            header = sp + 2,
                            nrows = DeviceLength + 2,
                            index_col = 0,
                            dtype=object,
                            skiprows=skip_rows)[20:-70]
        return data
    return wrapper


def header(types):
    def header_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if types.lower() == "device":
                try:
                    return list(args[0].Device.columns)
                except AttributeError:
                    print("Set a Device data.")
            elif types.lower() == "model":
                try:
                    return [col.split(":")[1] for col in args[0].Model.columns]
                except AttributeError:
                    print("Set a Model data.")
            elif types.lower() == "marker":
                try:
                    return [col.split(":")[1] for col in  args[0].Marker.columns]
                except AttributeError:
                    print("Set a Model data.")
        return wrapper
    return header_


def findSwitch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from ...dataIO.IO import SSP
        ssp = SSP()
        triggerName = set(ssp.getSSP()["Trigger"])
        try:
            common_name = triggerName & set(args[0].getDeviceHeader())
            num =  list(args[0].getDeviceHeader()).index(list(common_name)[0])
            switchData = args[0].Device.iloc[:,num].values.astype("float32")
            switch_ = np.where(switchData > 0.2, 1, 0)
            spep = np.where(np.diff(switch_) == 1)[0]
            if args[0].SwitchCount == 1:
                sp, ep = spep[:-1], spep[1:]
            elif args[0].SwitchCount == 2:
                sp, ep = spep[::2], spep[1::2]
            if len(sp) == args[0].NumberOfTrials & len(ep) == args[0].NumberOfTrials:
                spep = [[(sp/10).astype("int"),(ep/10).astype("int")],[sp,ep]]
                args[0].spep = spep
                print(" ")
                print("============================================")
                print("There is no problem about switch.")
                print("Use convert2pickle method for saving data.")
                print("============================================")
            else:
                print("Set spep at manually.")
        except:
            print("Did you use trigger at the time of measurement?")
            print("Do you want to continue converting?")
            answer = input("y or n :")
            if answer == "y":
                pass
            else:
                sys.exit()
    return wrapper

def findEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        EMG_name = {
            "Delsys - voltage".lower(),
            "Delsys[1000Hz] - voltage".lower()
        }
        header = [i.lower() for i in args[0].getDeviceHeader()]
        EMG_common = list(EMG_name & set(header))[0]
        EMG_header_number = header.index(EMG_common)
        data = pd.read_csv("{}.csv".format(args[0].file_name),index_col = 0,sep=",",header=3,dtype=object,nrows=10)
        EMGs = func(*args, **kwargs)
        EMG_list = list(data.columns[EMG_header_number:EMG_header_number + EMGs])
        EMG_set = dict(zip(EMG_list, np.arange(len(EMG_list))))
        return EMG_set
    return wrapper

def calc_MVC_values_with_proportion(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        sp, ep = args[0].spep[1][0], args[0].spep[1][1]
        EMGs = list(args[0].EMG_name.keys())
        MVCValues = []
        for EMG in EMGs:
            emg = args[0].getEMGraw(EMG)[sp[args[0].MMT_order[EMG]]:ep[args[0].MMT_order[EMG]]]
            t = int(len(emg)*args[1])
            sorted_emg = np.sort(np.abs(emg))[::-1]
            MVCValues.append(sorted_emg[:t].mean())
        MVC = {}
        for i in EMGs:
            MVC[i] = MVCValues[args[0].MMT_order[i]]
        args[0].MVC = MVC
    return wrapper



def fileconverter_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        file_name = str(input("Input file name : "))
        dir_name = str(input("Input your directory : "))
        cwd_home = os.getcwd()
        filepath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(filepath)
        os.chdir("../../_MeasurementData/{}".format(dir_name))
        cwd = os.getcwd()
        files = [os.path.basename(i) for i in glob.glob(cwd)]
        if file_name in files:
            print("That file already exists.")
            print("Do you want to overwrite ?")
            answer = str(input("y or n : "))
            if answer.lower() == "y":
                print("Continue the save process.")
                return file_name
                #func(*args, **kwargs)
            else:
                print("Saving process was interrupted.")
        else:
            return file_name
            #func(*args, **kwargs)
        os.chdir(cwd_home)
    return wrapper



