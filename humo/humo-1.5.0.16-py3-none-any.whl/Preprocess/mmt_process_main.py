import matplotlib.pyplot as plt
from collections import namedtuple
from .processing.MVCprocess import MVCprocess, MVCprocess2
import pathlib
import tkinter, tkinter.filedialog, tkinter.messagebox

class MVCmain(object):
    def __init__(self, **kwargs):
        if "dirpath" in kwargs.keys():
            self.p = pathlib.Path(kwargs["dirpath"]).resolve()
            if self.p.exists():
                pass
            else:
                print("The directory path you specified does not exist.")
        else:
            root = tkinter.Tk()
            root.withdraw()
            root.call("wm","attributes",".","-topmost",True)
            startdir = pathlib.Path.home()
            self.p = pathlib.Path(tkinter.filedialog.askdirectory(initialdir=startdir))
        if "subID" in kwargs.keys():
            file_name = list(self.p.glob("*mmt.csv"))
            self.file_name = [i for i in file_name if kwargs["subID"] in i.stem]
            if not self.file_name:
                print("The MMT measurement file was not found.")
            else:
                pass
            #self.mmtdata = [MVCprocess(dirpath=i, subID = kwargs["subID"]) for i in self.file_name]
            self.mmtdata = [MVCprocess(**{"dirpath":i, "subID":kwargs["subID"]}) for i in self.file_name]
        else:
            self.file_name = list(self.p.glob("*mmt.csv"))
            if not self.file_name:
                print("The MMT measurement file was not found.")
            else:
                pass
            #self.mmtdata = [MVCprocess(dirpath=i) for i in self.file_name]
            self.mmtdata = [MVCprocess(**{"dirpath":i}) for i in self.file_name]
        self.name_ = " ".join([i.emgname for i in self.mmtdata])
        Ntuple = namedtuple("MMTdata", self.name_)
        self.EMGdata = Ntuple(*self.mmtdata)
        self.name = [i.emgname for i in self.mmtdata]

    def calcMVC(self):
        mvcvalues = self.calc_all_MVCvalues()
        rawMMT = self.getMMTvaluesRaw()
        return mvcvalues, rawMMT

    def calc_all_MVCvalues(self):
        mvcvalues = {"normal":{}, "arv":{}}
        for i in self.name:
            mvcvalues["normal"][i] = getattr(self.EMGdata, i).MVCvalue_of_rawEMG()
            mvcvalues["arv"][i] = getattr(self.EMGdata, i).MVCvalue_of_arvEMG()
        return mvcvalues

    def getMMTvaluesRaw(self):
        rawMMT = []
        for i in self.name:
            rawMMT.append(getattr(self.EMGdata,i).emg)
        return dict(zip(self.name, rawMMT))

    def check_all_MVCvalues_rawEMG(self,size=(20,15),screen=(3,3)):
        plt.figure(figsize=size)
        for num, name in enumerate(self.name):
            plt.subplot(screen[0], screen[1], num+1)
            plt.plot(getattr(self.EMGdata, name).rawEMG()*1000000)
            v = getattr(self.EMGdata, name).MVCvalue_of_rawEMG()*1000000
            plt.axhline(v, color="r",label="MVCvalues:{}μV".format(round(v,2)))
            plt.axhline(-v, color="r",ls="--")
            plt.legend(fontsize=15,loc="lower left")
            plt.grid()
            plt.title(name, fontsize=20)
        plt.tight_layout()

    def check_all_MVCvalues_absEMG(self,size=(20,15),screen=(3,3)):
        plt.figure(figsize=size)
        for num, name in enumerate(self.name):
            plt.subplot(screen[0], screen[1], num+1)
            plt.plot(getattr(self.EMGdata, name).absEMG()*1000000)
            v = getattr(self.EMGdata, name).MVCvalue_of_rawEMG()*1000000
            plt.axhline(v, color="r",label="MVCvalues:{}μV".format(round(v,2)))
            plt.legend(fontsize=15,loc="lower left")
            plt.grid()
            plt.title(name, fontsize=20)
        plt.tight_layout()

    def check_all_MVCvalues_arvEMG(self,size=(20,15),screen=(3,3)):
        plt.figure(figsize=size)
        for num, name in enumerate(self.name):
            plt.subplot(screen[0], screen[1], num+1)
            plt.plot(getattr(self.EMGdata, name).arvEMG()*1000000)
            v = getattr(self.EMGdata, name).MVCvalue_of_arvEMG()*1000000
            plt.axhline(v, color="r",label="MVCvalues:{}μV".format(round(v,2)))
            plt.legend(fontsize=15,loc="lower left")
            plt.grid()
            plt.title(name, fontsize=20)
        plt.tight_layout()


class MVCmain2(object):
    def __init__(self,**kwargs):
        """
        Performs MVC processing when measuring the test muscle in the same file.

        input
        =====
        filepath [opt] : str
            Path to MMT file
        EMGlist [req] : list
        triggername [opt]: str
        triggercount [req] : int

        note
        =====
        If no path is entered, the GUI will launch.
        Please select the appropriate file.
        """
        if "filepath" in kwargs.keys():
            self.p = pathlib.Path(kwargs["filepath"]).resolve()
        else:

            root = tkinter.Tk()
            root.withdraw()
            root.call("wm","attributes",".","-topmost",True)
            fileType = [("", "*csv")]
            startdir = pathlib.Path.home()
            self.p = tkinter.filedialog.askopenfilenames(filetypes=fileType, initialdir=startdir)[0]
            print(self.p)
        if "triggername" not in kwargs.keys():
            self.data = MVCprocess2(self.p, kwargs["EMGlist"], kwargs["triggercount"])
            self.sp, self.ep = self.data.calcStartEndPoint()
        else:
            self.data = MVCprocess2(self.p, kwargs["EMGlist"], kwargs["triggername"], kwargs["triggercount"])
            self.sp, self.ep = self.data.calcStartEndPoint()
        self.MMT = [self.data.data[name].dropna().values[s:e].astype("float32") for name, s, e in zip(kwargs["EMGlist"], self.sp, self.ep)]
        self.MMT_ = {name:self.data.data[name].dropna().values[s:e].astype("float32") for name, s, e in zip(kwargs["EMGlist"], self.sp, self.ep)}
        Ntuple = namedtuple("MMTdata", kwargs["EMGlist"])
        self.MMTdata = Ntuple(*self.MMT)
        self.EMGlist = kwargs["EMGlist"]

    def setStartEndPoint(self,sp,ep):
        self.sp, self.ep = sp, ep
        self.MMT = [self.data.data[name].dropna().values[s:e].astype("float32") for name, s, e in zip(self.EMGlist, self.sp, self.ep)]
        self.MMT_ = {name:self.data.data[name].dropna().values[s:e].astype("float32") for name, s, e in zip(self.EMGlist, self.sp, self.ep)}
        Ntuple = namedtuple("MMTdata", self.EMGlist)
        self.MMTdata = Ntuple(*self.MMT)

    
    def calc_all_MVCvalues(self):
        from scipy import signal
        mvcvalues = {"normal":{}, "arv":{}}
        for muscle, val in self.MMT_.items():
            mvcvalues["normal"][muscle] = val.max()
            order, fq1, fq2, fq3 = 4, 20.0, 480.0, 10.0
            b,a = signal.butter(order,[fq1*2.0/1000,fq2*2.0/1000],"band",analog=False)
            val_ = signal.filtfilt(b, a, val)
            b, a = signal.butter(order,fq3*2.0/1000,"low",analog=False)
            mvcvalues["arv"][muscle] = signal.filtfilt(b, a, val_).max()
        return mvcvalues

    def calcMVC(self):
        return self.calc_all_MVCvalues(), self.MMT_



