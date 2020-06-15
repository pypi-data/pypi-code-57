from .processing import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import pathlib
import os


class PreProcess:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv("{}.csv".format(file_name),usecols=[0],sep=",",header=None,dtype=object)
        self.SwitchCount = None
        self.NumberOfTrials = None
        self.Device = None
        self.DeviceHeader = None
        self.Model = None
        self.ModelHeader = None
        self.Marker = None
        self.MarkerHeader = None
        self.MMT = None
        self.spep = None
        self.id = None
        self.EMGs = None
        self.EMG_name = None


# setter methods
    def AuteCheckData(self):
        self.setAllData()
        EMGs = int(input("How many muscles did you measure? : "))
        self.EMGs = EMGs
        self.setAllHeader()
        self.setEMG_name_Aute()
        self.setTriggerInfo()
        self.SetSwitch()


    def setAllData(self):
        for i in tqdm(range(3),desc="now loading..."):
            if i == 0:
                self.Device = self.getDevice()
            elif i == 1:
                self.Model = self.getModel()
            elif i == 2:
                self.Marker = self.getMarker()
        print("Data has been loaded.")

    def setAllHeader(self):
        self.DeviceHeader = self.getDeviceHeader()
        self.ModelHeader = self.getModelHeader()
        self.MarkerHeader = self.getMarkerHeader()

    def setDeviceData(self):
        self.Device = self.getDevice()

    def setDeviceHeader(self):
        self.DeviceHeader = self.getDeviceHeader()

    def setModelData(self):
        self.Model = self.getModel()

    def setModelHeader(self):
        self.ModelHeader = self.getModelHeader()

    def setMarkerData(self):
        self.Marker = self.getMarker()

    def setMarkerHeader(self):
        self.MarkerHeader = self.getMarkerHeader()

    def setEMG_name_Aute(self):
        self.EMG_name = self.getEMG_set()

    def setEMG_name(self,*args):
        self.EMG_name = dict(zip(args, np.arange(len(args))))

    def setMVC(self, params):
        self.MMT = params

    def setTriggerInfo(self):
        self.SwitchCount = int(input("How many times did you press the switch between the trials? : "))
        self.NumberOfTrials = int(input("How many trials do you have? : "))

    def setID(self,ID=None):
        if ID == None:
            name = str(input("subject name? : "))
            sex = str(input("Sex? : "))
            height = np.array(input("Height? : "))
            weight = np.array(input("weight? : "))
            model_type = str(input("Model type? : "))
            motion = str(input("motion? : "))
            degree = str(input("What is your degree? : "))
            id = {
                "name":name,
                "sex":sex,
                "height":height.astype("float32"),
                "weight":weight.astype("float32"),
                "model_type":model_type,
                "motion":motion,
                "degree":degree
            }
            self.id = id
        else:
            self.id = ID




# fileconverting process
    @sp_process
    def getStartPoint(self):
        return

    @length_process
    def getDataLength(self):
        return

    @readingData("device")
    def getDevice(self):
        return

    @readingData("model")
    def getModel(self):
        return

    @readingData("marker")
    def getMarker(self):
        return

    @header("device")
    def getDeviceHeader(self):
        return

    @header("model")
    def getModelHeader(self):
        return

    @header("marker")
    def getMarkerHeader(self):
        return

    @findSwitch
    def SetSwitch(self):
        return

    @findEMG
    def getEMG_set(self):
        return self.EMGs





    def convert2pickle(self,*path):
        convert_date = str(datetime.datetime.today())
        if self.id != None:
            self.id["convert_date"] = convert_date
        else:
            self.id = {"convert_data":convert_date}
        data = {
            "device":[self.Device, self.DeviceHeader],
            "model":[self.Model, self.ModelHeader],
            "marker":[self.Marker, self.MarkerHeader],
            "spep":self.spep,
            "MMT":self.MMT,
            "ID":self.id,
            "EMG_name":self.EMG_name
        }
        # ここから分岐させる
        # 引数は*path；任意のディレクトリ名を受け取る
        # 1. 実行されているディレクトリのパスを取得する
        # 2. Anaconda3，/rootが含まれているか確認する
        #   2.1 Anaconda3が含まれている場合；ローカルにインストール済み
        #       SSPファイルに保存されているデータパスに保存する
        #   2.2 /rootが含まれている場合；colaboratory上で実行されている
        #       import時に指定したデータディレクトリにアクセスする
        #   2.3 いずれにも当てはまらない場合；sys.pathに実行パスを渡している
        #       従来通りの方法でデータディレクトリにアクセスする
        cwd = os.getcwd()
        if ("Anaconda3" in os.path.dirname(__file__)) or ("anaconda3" in os.path.dirname(__file__)) or  ("miniconda" in os.path.dirname(__file__)):
            from ..dataIO.IO import SSP
            ssp = SSP()
            filepath = pathlib.Path.home() /ssp.getSSP()["data_path"]
            datapath = filepath.joinpath(*path)
            os.chdir(datapath)
            datahome = datapath
        elif "/root" in str(pathlib.Path.home()):
            from ..dataIO.IO import SSP
            ssp = SSP()
            filepath = pathlib.Path(ssp.getSSP()["data_path"])
            datapath = filepath.joinpath(*path)
            os.chdir(datapath)
            datahome = datapath
        else:
            filepath = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath("..","_MeasurementData")
            datapath = filepath.joinpath(*path)
            os.chdir(datapath)
            datahome = datapath
        #p = os.path.dirname(__file__)
        #datahome = pathlib.Path(p).joinpath("..","_MeasurementData").joinpath(*path)
        file_name = str(input("Input file name : "))
        ##dir_name = str(input("Which directory do you want to save ? : "))
        #cwd_home = os.getcwd()
        ##filepath = os.path.dirname(os.path.abspath(__file__))
        ##os.chdir(filepath)
        #os.chdir(datahome)
        #cwd = os.getcwd() + "/*"
        files = []
        for i in datahome.glob("*"):
            if i.is_file():
                files.append(i.name.split(".")[0])
        #files = [os.path.basename(i.split(".")[0]) for i in glob.glob(cwd)]
        if file_name in files:
            print("The file you input already exists")
            print("Do you want to overwrite ?")
            answer = str(input("y or n : " ))
            if answer.lower() == "y":
                print("Continue the saving process.")
                import pickle
                with open('{}.pkl'.format(file_name), mode='wb') as f:
                    pickle.dump(data, f, protocol=4)
                print("File conversion and save succeeded.")
            elif answer.lower() == "n":
                print("Saving process was interrupted.")
        else:
            import pickle
            with open('{}.pkl'.format(file_name), mode='wb') as f:
                pickle.dump(data, f, protocol=4)
            print("File conversion and save succeeded.")
        os.chdir(cwd)


# The method to use when you forget to press the switch
    def getSwitch_motion(self):
        from ..dataIO.IO import SSP
        ssp = SSP()
        try:
            TriggerName = list(set(ssp.getSSP()["Trigger"]) & set(self.DeviceHeader))[0]
            switch = self.Device[TriggerName].values.astype("float32")
            return switch
        except TypeError:
            print("Please execute the AuteCheckData method first.")
            print("Processing was interrupted.")


    def getEMG_motion(self,number):
        from ..dataIO.IO import SSP
        ssp = SSP()
        try:
            emg_device_name = set([i.lower() for i in ssp.getSSP()["EMGdevice"]])
            device_name = [i.lower() for i in self.DeviceHeader]
            emg_device = list(emg_device_name & set(device_name))[0]
            emg_num = list(device_name).index(emg_device) - 1
            emg = self.Device.iloc[:,emg_num + number].values.astype("float32")
            return emg
        except TypeError:
            print("Please execute the AuteCheckData method first.")
            print("Processing was interrupted.")



