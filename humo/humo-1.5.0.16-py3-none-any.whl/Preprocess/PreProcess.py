from .processing import processor
import pandas as pd
import numpy as np
import json
import pathlib
import os
import datetime
import inspect
import pathlib
import tkinter, tkinter.filedialog, tkinter.messagebox
import sys


class Convert2pkl(object):
    def __init__(self, *filepath):
        """Summary line.
        Convert2pkl converts csv file output from NEXUS to pkl file.

        Parameters
        ----------
        *path : str
            filepath to pkl file.
        
        Returns
        -------
        None

        note
        ------
        - If you do not specify the path, specify the file in the GUI.
        """
        if not filepath:
            root = tkinter.Tk()
            root.withdraw()
            root.call("wm","attributes",".","-topmost",True)
            fileType = [("","*csv")]
            startdir = pathlib.Path.home()
            self.p = tkinter.filedialog.askopenfilenames(filetypes=fileType, initialdir=startdir)[0]
            print(self.p)
        else:
            self.p = pathlib.Path(filepath[0]).resolve()
        self.data = pd.read_csv(self.p, usecols=[0],header=None,dtype=object)
        self.dataflags = processor.getdataflags(self.data)
        self.Nanflags = processor.getNanflags(self.data)
        self.device = None
        self.model = None
        self.marker = None
        self.deviceheader = None
        self.modelheader = None
        self.markerheader = None
        self.spep = None
        self.NumberOfMuscle = None # the number of muscles
        self.EMGset = None
        self.id = None
        self.MMT = None
        self.rawMMT = None
        
        
    def methodofPreProcess(self):
        """Summary line.
        Search for a method.

        Parameters
        ----------
        None

        Returns
        -------
        list
        All methods of the class.
        """
        method = []
        for i in inspect.getmembers(self,inspect.ismethod):
            method.append(i[0])
        method.remove("__init__")
        return method

    def datacleansing(self, **kwargs):
        """Summary line.
        It does data preprocessing to convert csv file to pkl file for humo.

        Parameters
        ----------
        NumberOfMuscle : int
            Number of muscles to be tested.
        triggercount : int
            Number of triggers pressed between trials.
        trialcount : int
            Number of trials.
        triggername : str
            The device name used to enter the trigger.
        NumberOfMuscle : int
            The number of muscles which was measured.
        EMGdevicename : str
            EMG device name which was used for measuring EMG data.
        ID : dic
            Subject parameters.
            It is recommended to edit and use the default ID.json

        Returns
        -------
        Data cleansing results
		"""
        keys = set(kwargs.keys())
        expected_key = {"NumberOfMuscle","triggercount","trialcount","triggername","NumberOfMuscle","EMGdevicename","ID"}
        unexpected_key = keys - expected_key
        if not unexpected_key:
            pass
        else:
            print("Checking your args. - Unexpected keyword args.")
            print("="*50)
            for i in unexpected_key:
                print(i)
            print("="*50)
            sys.exit()

        self.setData()
        self.rename_forceplate()
        if not kwargs:
            self.setEMGinfo()
        else:
            self.setEMGinfo(kwargs)
        if "triggercount" in kwargs.keys():
            try:
                a,b,c = kwargs["triggercount"], kwargs["trialcount"], kwargs["triggername"]
                self.setTrigger(a,b,c)
            except:
                a, b = kwargs["triggercount"], kwargs["trialcount"]
                self.setTrigger(a,b)
        else:
            print("[Attension] - setTrigger")
            print("="*50)
            print("The trigger is not used.")
            print("="*50)
            print("")
        print("[Attension] - checkmissingvalues")
        print("="*50)
        self.checkmissingvalues()
        print("="*50)
        print("")
        try:
            id_ = kwargs["ID"]
            self.setID(id_)
            print("-> Do not overlook !")
            print("-"*50)
            print("    - Remember to check that the various data are processed correctly.")
            
        except:
            pass
            print("-> Do not overlook !")
            print("-"*50)
            print("    - Remember to check that the various data are processed correctly.")
            print("    - Remember to set the subject's unique information [setID method].")



    def setData(self):
        """Summary line.
        Device data, modeloutputs data, and marker data
        are extracted from the csv data.
        If the name of the kistler force plate is the default name of NEXUS,
        it will be changed appropriately.

        Exsample
        --------
        'Imported Kistler Force Plate (External Amplifier) #2 - Force'
        -> 'FP2 - Force'

        Parameters
        ----------
        Notiong

        Returns
        -------
        Notiong

        [Note1]
        Instance variables such as device, model, and marker are stored.
        These contain actual data.
        Also, instance variables such as deviceheader, modelheader, and markerheader
        are stored at the same time.
        These include the header of each data.
        
        [Note2]
        Generate Convert2pkl instance and execute.
		"""
        ToF = []
        try:
            self.device = processor.getData(
                self.data,
                "Device",
                self.dataflags,
                self.Nanflags,
                self.p
            )
            self.deviceheader = self.device.columns
            ToF.append(True)
            #dheader = [i for i in self.device.columns if "Unnamed" not in i]
            #kistlerheader = [i for i in dheader if "Imported Kistler" in i]
            #if not kistlerheader:
            #    pass
            #else:
            #    dic = {}
            #    for i in kistlerheader:
            #        dic[i] = "FP" + i.split("#")[1]
            #    self.device = self.device.rename(columns=dic)
            #    self.deviceheader = self.device.columns
            #    print("[Attention]")
            #    print("="*50)
            #    print("The name of the reaction force plate (kistler)\nhas been changed.")


        except:
            print("Error in Device")
            ToF.append(False)
        try:
            self.model = processor.getData(
                self.data,
                "Model",
                self.dataflags,
                self.Nanflags,
                self.p
            )
            self.model = self.model.rename(columns=lambda s:s if "Unnamed" in s else s.split(":")[1])
            self.modelheader = self.model.columns
            ToF.append(True)
        except:
            print("Error in Model")
            ToF.append(False)
        try:
            self.marker = processor.getData(
                self.data,
                "Marker",
                self.dataflags,
                self.Nanflags,
                self.p
            )
            #self.marker = self.marker.rename(columns=lambda s:s if "Unnamed" in s else s.split(":")[1])
            marker_header = []
            for i in self.marker.columns:
                if "Unnamed" in i:
                    marker_header.append(i)
                elif ":" not in i:
                    marker_header.append(i)
                else:
                    marker_header.append(i.split(":")[1])
            marker_header_dic = dict(zip(self.marker.columns, marker_header))
            self.marker = self.marker.rename(columns=marker_header_dic)
            self.markerheader = self.marker.columns
            ToF.append(True)
        except:
            print("Error in Marker")
            ToF.append(False)
        if False not in ToF:
            print("[Attension] - setData")
            print("="*50)
            print("Each data was successfully extracted.")
            print("="*50)
            print("")
        else:
            print("[Attension] - setData")
            print("="*50)
            print("Some error has occurred during data output.")
            print("="*50)
            print("")
    
    def rename_deviceheader(self, dic):
        """Summary line.
        Change the device data header name.

        Parameters
        ----------
        dic : dictionary
            Dictionary type created from old and new header names.

        Returns
        -------
        Nothing
        
        [Example]
        Create a dicsionary with the old header name as key and
        the new header name as value.
        dic = {
            "hoge1":"hoo1",
            "hoge2":"hoo2"
        }
        When such a dictionary is created, 'hoge1' and 'hoge2' in the header
        are changed to 'hoo1' and 'hoo2', respectively.
        """
        self.device = self.device.rename(columns = dic)
        self.deviceheader = self.device.columns
    
    def rename_modelheader(self, dic):
        """Summary line.
        Change the model data header name.

        Parameters
        ----------
        dic : dictionary
            Dictionary type created from old and new header names.

        Returns
        -------
        Nothing
        
        [Example]
        Create a dicsionary with the old header name as key and
        the new header name as value.
        dic = {
            "hoge1":"hoo1",
            "hoge2":"hoo2"
        }
        When such a dictionary is created, 'hoge1' and 'hoge2' in the header
        are changed to 'hoo1' and 'hoo2', respectively.
        """
        self.model = self.model.rename(columns = dic)
        self.modelheader = self.model.columns

    def rename_markerheader(self, dic):
        """Summary line.
        Change the marker data header name.

        Parameters
        ----------
        dic : dictionary
            Dictionary type created from old and new header names.

        Returns
        -------
        Nothing
        
        [Example]
        Create a dicsionary with the old header name as key and
        the new header name as value.
        dic = {
            "hoge1":"hoo1",
            "hoge2":"hoo2"
        }
        When such a dictionary is created, 'hoge1' and 'hoge2' in the header
        are changed to 'hoo1' and 'hoo2', respectively.
        """
        self.marker = self.marker.rename(columns = dic)
        self.markerheader = self.marker.columns

    def rename_forceplate(self):
        """Summary line.
        Convert the default name of force plate to FP + number.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        kistlerheader = [i for i in self.deviceheader if "Imported Kistler" in i]
        if not kistlerheader:
            print("[Attention] - rename_forceplate")
            print("="*50)
            print("There was no problem with the force plate information.")
            print("="*50)
            print("")
        else:
            dic = {}
            for i in kistlerheader:
                dic[i] = "FP" + i.split("#")[1]
                self.device = self.device.rename(columns=dic)
                self.deviceheader = self.device.columns
            print("[Attention] - rename_forceplate")
            print("="*50)
            print("The name of the reaction force plate (kistler)\nhas been changed.")
            print("="*50)
            print("")
            header = [i for i in self.device.columns if "Unnamed" not in i]
            kistler_name = []
            for i in header:
                if "Imported Kistler" in i:
                    kistler_name.append(i)
                else:
                    pass
            dic = {}
            for i in kistler_name:
                dic[i] = "FP" + i.split("#")[1]
            self.device = self.device.rename(columns=dic)
            self.deviceheader = self.device.columns

    def checkDeviceheader(self):
        """Summary line.
        Display the device data header.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            header = [i for i in self.device.columns if "Unnamed" not in i]
            print("--------------------------------------")
            print("<< Check the data about Device >>")
            print("The number of device header : {}".format(len(header)))
            print("--------------------------------------")
            for name in ["Force", "Moment", "CoP"]:
                print("Force plate - '{}'".format(name))
                print("=======================")
                for i in header:
                    if name in i:
                        print("    > {}".format(i))
                print("")
            print("'Others'")
            print("=======================")
            for i in header:
                if ("Force" not in i) & ("Moment" not in i) & ("CoP" not in i):
                    print("    > {}".format(i))
        except AttributeError:
            print("Please set Data.")

    def checkModelheader(self):
        """Summary line.
        Display the model data header.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            header = [i for i in self.model.columns if "Unnamed" not in i]
            print("--------------------------------------")
            print("<< Check the data about ModelOutputs >>")
            print("The number of model header : {}".format(len(header)))
            print("--------------------------------------")
            for name in ["Angle", "Force", "Moment", "Power", "COM"]:
                print("{} data".format(name))
                print("==============")
                for i in header:
                    if name in i:
                        print(i.split(name)[0])
                print("")
            print("Others data")
            print("==============")
            for i in header:
                if ("Angle" not in i) & ("Force" not in i) & ("Moment" not in i) & ("Power" not in i) & ("COM" not in i):
                    print(i)
        except AttributeError:
            print("Please set Data.")

    def checkMarkerheader(self):
        """Summary line.
        Display the marker data header.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            header = [i for i in self.marker.columns if "Unnamed" not in i]
            print("--------------------------------------")
            print("<< Check the data about Markers >>")
            print("The number of model header : {}".format(len(header)))
            for name in ["R", "L"]:
                if name == "R":
                    print("{} side marker".format("Right"))
                    print("=========================")
                elif name == "L":
                    print("{} side marker".format("Left"))
                    print("=========================")
                for i in header:
                    if name in i[0]:
                        print(i)
                print("")
            print("Others data")
            print("=========================")
            for i in header:
                if ("R" != i[0]) & ("L" != i[0]):
                    print(i)
        except AttributeError:
            print("Please set Data.")

    def setdataheader(self):
        """Summary line.
        Register the headers of device, model, and marker data to the instance members.

        Parameters
        ----------
        Nothing.

        Returns
        -------
        Nothing.

        note
        -------
        When the header name is changed manually, register the header in the instance member.
		"""
        self.deviceheader = self.device.columns
        self.modelheader = self.model.columns
        self.markerheader = self.marker.columns

#*NumberOfMuscle, EMGdevicename
    def getEMGdevicePostion(self, **kwargs):
        """
        EMGdevicename : str
        """
        if not kwargs:
            DelsysDevice = {
                "Delsys - voltage".lower(),
                "Delsys[1000Hz] - voltage".lower()
            }
        else:
            DelsysDevice = set([kwargs["EMGdevicename"].lower()])
        deviceheader = [i.lower() for i in self.deviceheader]
        commonname = list(DelsysDevice & set(deviceheader))
        if not commonname:
            print("[Attension - getEMGdevicePosition]")
            print("="*50)
            print("The specified EMG device was not found.")
            print("="*50)
            sys.exit()
        else:
            return deviceheader.index(commonname[0])

    def getNumberOfEMG(self, position):
        head = list(self.deviceheader[position:])
        for_last_index = [head.index(i) for i in head if "Unnamed" in i]
        return for_last_index[-1] + 1

    def setEMGinfo(self, *args):
        """Summary line.
        Build a relationship between the muscle under test and the index.

        Parameters
        ----------
        dictionary
        NumberOfMusckle : int
        EMGdevicename : str

        Returns
        -------
        Nothing.

        note
        -------
        -Specify the number of muscles to be inspected and the EMG device name if the acquisition is not successful.
        """
        if not args:
            EMGdeviceposition = self.getEMGdevicePostion()
            NumOfEMG = self.getNumberOfEMG(EMGdeviceposition)
        else:
            if "NumberOfMuscle" in args[0].keys():
                NumOfEMG = args[0]["NumberOfMuscle"]
                if "EMGdevicename" in args[0].keys():
                    EMGdeviceposition = self.getEMGdevicePostion(EMGdevicename = args[0]["EMGdevicename"])
                else:
                    EMGdeviceposition = self.getEMGdevicePostion()
            else:
                if "EMGdevicename" in args[0].keys():
                    EMGdeviceposition = self.getEMGdevicePostion(EMGdevicename = args[0]["EMGdevicename"])
                else:
                    EMGdeviceposition = self.getEMGdevicePostion()
                NumOfEMG = self.getNumberOfEMG(EMGdeviceposition)
            # Below, the process of making an EMG set
        data = pd.read_csv(self.p, index_col=0,header=3,dtype=object,nrows=10)
        EMG_list = list(data.columns[EMGdeviceposition:EMGdeviceposition+NumOfEMG])
        self.EMGset = dict(zip(EMG_list, np.arange(len(EMG_list))))
        print("[Attention] - setEMGinfo")
        print("="*50)
        print("Please check the muscle name and its number later.")
        print("="*50)
        print("")
            
            

        
    def setEMGinfo_(self, *args):
        self.EMGset = dict(zip(args, np.arange(len(args))))


    def checkmissingvalues(self):
        """Summary line.
        Check for missing values.

        Parameters
        ----------
        None.

        Returns
        -------
        None

        note
        -------
        -If the missing values match, check again for missing markers on NEXUS and re-output.
        """
        missingvalues = [getattr(self, i).isnull().any(axis=0) for i in ["device","model","marker"]]
        missingvalues = {name:i[i==True] for i, name in zip(missingvalues, ["device","model","marker"])}
        for key, value in missingvalues.items():
            if not list(value):
                print("- There were no missing values in the {} data.".format(key))
            else:
                print("- There were missing values in the {} data".format(key))
                NanIndex = [getattr(self, key).columns.get_loc(i) for i in value.index]
                for i, j in zip(value.index, NanIndex):
                    print("    - {} : {}".format(j, i))

    def getmissingvalues(self):
        missingvalues = [getattr(self, i).isnull().any(axis=0) for i in ["device","model","marker"]]
        missingvalues = {name:i[i==True] for i, name in zip(missingvalues, ["device","model","marker"])}
        return missingvalues

    def checkheaderintegrity(self, expectedset, dataset):
        """
        expectedset : set
        dataset : set
        """
        if expectedset == dataset:
            print("- The expected set and the data set are equal.")
        else:
            if expectedset.issubset(dataset):
                print("- Expected set is a subset of the dataset")
                print("-"*50)
                print("Included only in dataset")
                print(dataset - expectedset)
            elif dataset.issubset(expectedset):
                print("- Dataset is a subset of the expected set")
                print("-"*50)
                print("Included only in expected set")
                print(expectedset - dataset)
            else:
                print("- The common set")
                print(expectedset & dataset)
                print("Included only in expected set")
                print(expectedset - dataset)
                print("Included only in dataset")
                print(dataset - expectedset)


    def checkheaderset(self, expectedsetlist):
        """Summary line.
        Check for missing data.

        Parameters
        ----------
        expectedsetlist : set
            json file output from generate_headerset method.
        Returns
        -------
        None

        note
        -------
        - If there is a marker label error, model calculation may fail and data may not be output.
        """
        for name in ["device","model","marker"]:
            dataset = {i for i in getattr(self, name).columns if "Unnamed" not in i}
            expectedset = set(expectedsetlist[name])
            print("Results of {} data".format(name))
            print("="*50)
            self.checkheaderintegrity(expectedset, dataset)
            print("")

    def generate_headerset(self, filename):
        """Summary line.
        Save the header set.

        Parameters
        ----------
        filename : str
            Not path but filename.
        Returns
        -------
        None

        note
        -------
        - It is saved in the calendar directory.
        """
        headerdata = {
            "device":[i for i in getattr(self, "device").columns if "Unnamed" not in i],
            "model":[i for i in getattr(self, "model").columns if "Unnamed" not in i],
            "marker":[i for i in getattr(self, "marker").columns if "Unnamed" not in i]
        }
        f = open("{}.json".format(filename), "w")
        json.dump(headerdata, f, indent=4)

    def load_headerset(self,path):
        """Summary line.
        Read the header set.

        Parameters
        ----------
        path : str
            path to file.
        Returns
        -------
        None

        note
        -------
        - If you want to load hoge.json on the desktop, do the following.
            "C: /Users/username/Desktop/hoge.json"
        - For Windows OS user.
            Backslash (/) is treated as an escape character, so prefix r.
        """
        p = pathlib.Path(path)
        with open(p) as f:
            header_set = json.load(f)
        return header_set

    def setTrigger(self, triggercount, trialcount, *triggername):
        """Summary line.
        Set the start time and end time of each trial from the trigger information that separates the trials.

        Parameters
        ----------
        triggercount : int
            The number of triggers entered during the trial.
        trialcount : int
            The number of trials.
        *triggername : str
            The device name you used for input trigger.
        
        Returns
        -------
        None
        """
        if len(triggername) == 0:
            triggerName = {
                "Generic Analog - Electric Potential",
                "Imported Generic Analog - Electric Potential",
                "oisaka - Electric Potential",
                "trigger - Electric Potential",
                "Generic Analog #2 - Electric Potential",
                "Imported Generic Analog #2 - Electric Potential",
                "Imported Generic Analog #3 - Electric Potential"
            }
            common_name = triggerName & set(self.device.columns)
            if len(common_name) == 0:
                print("[Attention] - setTriggger")
                print("="*50)
                print("Trigger information could not be obtained."\
                        "\nIf trigger information is included, please set the correct device name.")
                print("="*50)
                print("")
            else:
                pass
            common_name = list(common_name)[0]
        else:
            common_name = triggername[0]
            dic = {common_name:triggerName[0]}
            self.device = self.device.rename(columns = dic)
            self.deviceheader = self.device.columns
        triggerIndex = list(self.device.columns).index(common_name)
        triggerData = self.device.iloc[:,triggerIndex].values.astype("float32")
        import numpy as np
        triggerData_ = np.where(triggerData > 0.2, 1, 0)
        spep = np.where(np.diff(triggerData_) == 1)[0]
        if triggercount == 1:
            sp, ep = spep[:-1], spep[1:]
        elif triggercount == 2:
            sp, ep = spep[::2], spep[1::2]
        if len(sp) == trialcount & len(ep) == trialcount:
            self.spep = [[(sp/10).astype("int"), (ep/10).astype("int")], [sp, ep]]
            print("[Attention] - setTriggger")
            print("="*50)
            print("There is no problem about trigger infomation.")
            print("Use convert2pickle method for saving data.")
            print("="*50)
            print("")
        else:
            print("[Attention] - setTrigger")
            print("="*50)
            print("Trigger information was obtained,\nbut the values ​​for trigger count\nand trial count are inconsistent. \nCheck the trigger count and trial count.")
            print("="*50)
            print("")

    def setID(self, *id_list):
        """Summary line.
        Register subject information.

        Parameters
        ----------
        *id_list : dict
            json file loaded by the load_id_list method.
        
        Returns
        -------
        None

        note
        -------
        - If id_list is not given as an argument, enter it according to the guidance.
        """
        if len(id_list) == 0:
            name = str(input("subject name? : "))
            sex = str(input("Sex? : "))
            height = np.array(input("Height? : "))
            weight = np.array(input("weight? : "))
            model_type = str(input("Model type? : "))
            motion = str(input("motion? : "))
            degree = str(input("What is your degree? : "))
            id_input = {
                "name":name,
                "sex":sex,
                "height":height.astype("float32"),
                "weight":weight.astype("float32"),
                "model_type":model_type,
                "motion":motion,
                "degree":degree
            }
            self.id = id_input
        else:
            self.id = id_list[0]

    def load_id_list(self, path):
        """Summary line.
        Read the header set.

        Parameters
        ----------
        path : str
            path to file.
        Returns
        -------
        None

        note
        -------
        - If you want to load hoge.json on the desktop, do the following.
            "C: /Users/username/Desktop/hoge.json"
        - For Windows OS user.
            Backslash (/) is treated as an escape character, so prefix r.
        """
        p = pathlib.Path(path)
        with open(p) as f:
            id_list = json.load(f)
        return id_list

    def setMMTvalues(self, MVCvalues, rawMMT=None):
        """Summary line.
        Register the value to calculate MVC.

        Parameters
        ----------
        MVCvalues : list
            output from MVCmain or MVCmain2 instance.
        rawMMT : list
            output from MVCmain or MVCmain2 instance.
        
        Returns
        -------
        None

        note
        -------
        - If you want to normalize by MMT, MVC values are required.
        - If there is a possibility of MVC process, it is recommended to register rawMMT at the same time.
        """
        self.MMT = MVCvalues
        self.rawMMT = rawMMT


    def convert2pickle(self, **kwargs):
        """Summary line.
        Register the value to calculate MVC.

        Parameters
        ----------
        filename : str
        path : str
        
        Returns
        -------
        None

        note
        -------
        - If you do not specify the path, specify the directory and file name in the GUI.
        - When the file name is specified, specify the directory on the GUI.
        - If you want to load hoge.json on the desktop, do the following.
            "C: /Users/username/Desktop/hoge.json"
        - For Windows OS user.
            Backslash (/) is treated as an escape character, so prefix r.
        """
        convert_date = str(datetime.datetime.today())
        if self.id != None:
            self.id["convert_date"] = convert_date
        else:
            self.id = {"convert_data":convert_date}
        data = {
            "device":[self.device.astype("float64"), list(self.deviceheader)],
            "model":[self.model.astype("float64"), list(self.modelheader)],
            "marker":[self.marker.astype("float64"), list(self.markerheader)],
            "spep":self.spep,
            "MMT":self.MMT,
            "rawMMT":self.rawMMT,
            "ID":self.id,
            "EMG_name":self.EMGset
        }
        # 指定したデータパスのディレクトリを取得
        # ディレクトリに存在するファイルを全て列挙
        # 保存したいファイル名と同一のファイルが存在するか確認
        # 上書き or キャンセル
        if not kwargs:
            root = tkinter.Tk()
            root.withdraw()
            root.call("wm", "attributes", ".", "-topmost", True)
            fileType = [("", "*.pkl")]
            startdir = pathlib.Path.home()
            ret = tkinter.filedialog.asksaveasfilename(defaultextension="pkl", filetypes=fileType, initialdir=startdir, title="Save as...")
            p = pathlib.Path(ret)
            files = []
            for i in p.parent.glob("*"):
                if i.is_file():
                    files.append(i.stem)
            if p.stem in files:
                print("The file you input already exists")
                print("Do you want to overwrite ?")
                answer = str(input("y or n : " ))
                if answer.lower() == "y":
                    print("Continue the saving process.")
                    import pickle
                    with open('{}'.format(p), mode='wb') as f:
                        pickle.dump(data, f, protocol=4)
                    print("File conversion and save succeeded.")
            else:
                import pickle
                with open("{}".format(p), mode="wb") as f:
                    pickle.dump(data, f, protocol=4)
                print("File conversion and save succeeded.")
        elif "filename" in kwargs.keys():
            root = tkinter.Tk()
            root.withdraw()
            root.call("wm", "attributes", ".", "-topmost", True)
            startdir = pathlib.Path.home()
            savedir = tkinter.filedialog.askdirectory(initialdir=startdir)
            p = pathlib.Path(savedir)
            files = []
            for i in p.glob("*"):
                if i.is_file():
                    files.append(i.stem)
            if "." not in kwargs["filename"]:
                if kwargs["filename"] in files:
                    print("The file you input already exists.")
                    print("Do you want to overwrite ?")
                    answer = str(input("y or n : " ))
                    if answer.lower() == "y":
                        print("Continue the saving process.")
                        import pickle
                        with open("{}.pkl".format(p /kwargs["filename"]), mode='wb') as f:
                            pickle.dump(data, f, protocol=4)
                        print("File conversion and save succeeded.")
                    else:
                        print("Saving process was interrupted.")
                        
                else:
                    import pickle
                    with open("{}.pkl".format(p /kwargs["filename"]), mode='wb') as f:
                        pickle.dump(data, f, protocol=4)
                    print("File conversion and save succeeded.")
            else:
                if kwargs["filename"].split(".")[0] in files:
                    print("The file you input already exists.")
                    print("Do you continue the saving process ?")
                    answer = str(input("y or n : "))
                    if answer.lower() == "y":
                        print("Continue the saving process.")
                        import pickle
                        with open("{}".format(p /kwargs["filename"]), mode='wb') as f:
                            pickle.dump(data, f, protocol=4)
                        print("File conversion and save succeeded.")
                    else:
                        print("Saving process was interrupted.")
                else:
                    import pickle
                    with open("{}".format(p /kwargs["filename"]), mode='wb') as f:
                        pickle.dump(data, f, protocol=4)
                    print("File conversion and save succeeded.")
        elif "path" in kwargs.keys():
            p = pathlib.Path(kwargs["path"])
            datadir = p.parent
            files = []
            for i in datadir.glob("*"):
                if i.is_file():
                    files.append(i.name.split(".")[0])
            #files = [os.path.basename(i.split(".")[0]) for i in glob.glob(cwd)]
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



