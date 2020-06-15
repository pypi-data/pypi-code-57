import pathlib
import pandas as pd
from .mmt_processor import filtEMG,takeAbsValues,smoothingEMG,calcMVCvalue
from .mmt_processor import calcMVCvalue2

class MVCprocess(object):
    def __init__(self, **kwargs):
        self.data_directory = pathlib.Path(kwargs["dirpath"])
        self.filename = self.data_directory.name
        if "subID" in kwargs.keys():
            self.emgname = self.data_directory.stem.split("_")[1]
            print(self.emgname)
        else:
            if len(self.data_directory.stem.split("_")) == 3:
                self.emgname = self.data_directory.stem.split("_")[1]
            elif len(self.data_directory.stem.split("_")) == 2:
                self.emgname = self.data_directory.stem.split("_")[0]
        self.col = pd.read_csv(self.data_directory,usecols=[0],header=None,dtype=object)
        if len(self.col[self.col[0].isnull()]) > 2:
            self.data_length = self.col[self.col[0].isnull()].index[2] - self.col[self.col[0].isnull()].index[1] - 2
            self.data = pd.read_csv(self.data_directory,
                                    sep=",",
                                    header = 3,
                                    nrows = self.data_length,
                                    index_col = 0,
                                    dtype=object,
                                    skiprows=0)[1:]
        else:
            self.data = pd.read_csv(self.data_directory,
                                    sep=",",
                                    header=3,
                                    dtype=object)[1:]
        self.emg = self.data[self.emgname].dropna().values.astype("float32")


    @filtEMG
    def rawEMG(self):
        return

    @takeAbsValues
    def absEMG(self):
        return self.rawEMG()

    @smoothingEMG
    def arvEMG(self):
        return self.absEMG()

    #@calcMVCvalue(0.8, 0.9)
    @calcMVCvalue2
    def MVCvalue_of_rawEMG(self):
        return self.absEMG()

    #@calcMVCvalue(0.8, 0.9)
    @calcMVCvalue2
    def MVCvalue_of_arvEMG(self):
        return self.arvEMG()


class MVCprocess2(object):
    def __init__(self, filepath, EMGlist, triggercount, *args):
        self.EMGlist = EMGlist
        self.triggercount = triggercount
        self.data_directory = pathlib.Path(filepath)
        self.col = pd.read_csv(self.data_directory, usecols=[0], header=None, dtype=object)
        if len(self.col[self.col[0].isnull()]) > 2:
            self.data_length = self.col[self.col[0].isnull()].index[2] - self.col[self.col[0].isnull()].index[1] - 2
            self.data = pd.read_csv(self.data_directory,
                                    sep=",",
                                    header = 3,
                                    nrows = self.data_length,
                                    index_col = 0,
                                    dtype=object,
                                    skiprows=0)[2:]
        else:
            self.data = pd.read_csv(self.data_directory,
                                    sep=",",
                                    header=3,
                                    dtype=object)[2:]
        columns = pd.read_csv(
                                self.data_directory,
                                header = 2,
                                nrows = 3,
                                index_col = 0,
                                dtype=object
                                ).columns
        if not args:
            triggerName = {
                "Generic Analog - Electric Potential",
                "Imported Generic Analog - Electric Potential",
                "oisaka - Electric Potential",
                "trigger - Electric Potential",
                "Generic Analog #2 - Electric Potential",
                "Imported Generic Analog #2 - Electric Potential",
                "Imported Generic Analog #3 - Electric Potential"
            }
        else:
            triggerName = set(args)
        common_name = triggerName & set(columns)
        if len(common_name) == 0:
            print("[Attention] - setTriggger")
            print("="*50)
            print("Trigger information could not be obtained."\
                    "\nIf trigger information is included, please set the correct device name.")
            print("="*50)
            print("")
        else:
            pass
        self.triggerIndex = list(columns).index(list(common_name)[0])
        del columns

    def calcStartEndPoint(self):
        import numpy as np
        triggerdata = self.data.iloc[:,self.triggerIndex].values.astype("float32")
        triggerdata = np.where(triggerdata > 0.2, 1,0)
        spep = np.where(np.diff(triggerdata) == 1)[0]
        if self.triggercount == 1:
            sp, ep = spep[:-1], spep[1:]
        elif self.triggercount == 2:
            sp, ep = spep[::2], spep[1::2]
        else:
            print("[Attention] - calcStartEndPont")
            print("="*50)
            print("triggercount is an integer and can only take 1 or 2.")
            print("="*50)
        if len(sp) == len(self.EMGlist) & len(ep) == len(self.EMGlist):
            return sp, ep
        else:
            print("[Attension] - calcStartEndPoint")
            print("="*50)
            print("The trigger information has been acquired.\nHowever, the number of test muscles and the number of sections are different.\nPlease check the muscle to be inspected, forgetting to press the trigger, etc.")
            print("="*50)
        
