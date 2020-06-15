import numpy as np
import pandas as pd
from functools import lru_cache
import inspect
from .CoreProcessor import *
import pathlib

'''
Make docstrings consistent with google style.
The following is an example.
Use copy and paste

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        """Summary line.

        Parameters
        ----------
        arg1 : str
            Name of markers.

        Returns
        -------
        array(3 dimension)
            It is output in the order of x axis, y axis, z axis.
        """

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''

class CoreModel:
    def __init__(self,data, **kwargs):
        self._ID = data["ID"]
        # each data
        self._model = data["model"][0]
        # header data
        self._modelheader = [i.lower() for i in data["model"][1]]
        self.modelheader = data["model"][1]
        # spep
        self._spep = data["spep"]
        if "cfg" in kwargs.keys():
            self.cfg = kwargs["cfg"]
        else:
            self.cfg = None
        # EMG name
        self._emg_name = data["EMG_name"]
        self.mvc = data["MMT"]







    @showheader("model")
    def modelCols(self):
        return

    @find_name
    def is_model(self, name):
        return self.modelCols(), name

    def getModelList(self):
        try:
            header = [i for i in self._model.columns if "Unnamed" not in i]
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



    def model_names(self, subdivision):
        """Summary line.
        This method is to output modeloutputs data item by item.

        Parameters
        ----------
        subdivision : str
            "Segment", "SegmentCOM" or "Nmodel"

        Returns
        -------
        model names : list

        Notes:
            - "Segment includes"
                - segment posture angles
                - absolute coordinates of segment
                - relative coordinates of segment"
            - "SegmentCOM includes"
                - absolute coordinates of COM for each segment.
            - "Nmodel includes"
                - regular kinematics data(3 dimensions).
            - "jointcenter"
                - 3d coordination of center of joint
        """
        delete_item = ["angles","angle","moment","force","power","mass","grf"]
        Segment, SegmentCOM, Nmodel,coj = [], [], [], []
        for i in self._modelheader:
            try:
                int(i)
            except:
                boolian = []
                for j in delete_item:
                    boolian.append(j in i)
                if True in boolian:
                    Nmodel.append(i)
                else:
                    if "com" in i:
                        SegmentCOM.append(i)
                    else:
                        if i[-2:] == "jc":
                            coj.append(i)
                        else:
                            Segment.append(i)
        if subdivision == "Segment": return Segment
        elif subdivision == "SegmentCOM":return SegmentCOM
        elif subdivision == "Nmodel":return Nmodel
        elif subdivision == "JC":return coj
        else: print('inpot "Segment" or "SegmentCOM" or "Nmodel" or "JC"')



# method for getting raw model data.
    @cvt_HumoArray(argsType=None)
    @retrivingModelData(True)
    @isCOMname(floor=False) # docstrings修正
    def getCOM(self):
        """Summary line.
        Get 3D coordinates of mass center.

        Parameters
        ----------
        None

        Returns
        -------
        humoArray
            3D coordinates of COM.
        """
        return

    @cvt_HumoArray(argsType=None)
    @retrivingModelData(True)
    @isCOMname(floor=True) # docstrings修正
    def getCOM_floor(self):
        """Summary line.
		Get the coordinates of the center of mass projected on the floor.

        Parameters
        ----------
        None

        Returns
        -------
        humoArray
            COM projected on the flooe.
            It is output in order of x axis, y axis and z axis.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isModelName("angles")
    def getJointAngle(self,name):
        """Summary line.
        Output the joint angle.
        Accept only one joint name.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The relative angle between each segment is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isModelName("moment")
    def getJointMoment(self,name):
        """Summary line.
        Output the joint moment.
        Accept only one joint name.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The joint moment is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return

    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isModelName("force")
    def getJointForce(self,name):
        """Summary line.
        Output the joint force.
        Accept only one joint name.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The joint force is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isModelName("power")
    def getJointPower(self,name):
        """Summary line.
        Output the joint power.
        Accept only one joint name.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The joint power is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isModelName("abs")
    def getAbsJointAngle(self, name):
        """Summary line.
        Output absolute joint angle.
        Accept only one joint name.

        Parameters
        ----------
        name : str
            Name of segment.

        Returns
        -------
        humoArray
            The absolute joint angle is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @differentation(difforder="1st")
    @retrivingModelData(False)
    @isModelName("angles")
    def getJointAngleVel(self,name):
        """Summary line.
        Output the angular velocity of the joint angle.
		The angular velocity is calculated by central difference method.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The angular velocity is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @differentation(difforder="2nd")
    @retrivingModelData(False)
    @isModelName("angles")
    def getJointAngleAcc(self,name):
        """Summary line.
        Output the angular acceleration of the joint angle.
		The angular acceleration is calculated by central difference method.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The angilar acceleration is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @differentation(difforder="1st")
    @retrivingModelData(False)
    @isModelName("abs") # 何故かanglesになっていた。absに修正。
    def getAbsJointAngleVel(self, name):
        """Summary line.
        Output the angular velocity of the absolute joint angle.
		The angular velocity is calculated by central difference method.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The angular velocity is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @differentation(difforder="2nd")
    @retrivingModelData(False)
    @isModelName("abs") # 何故かanglesになっていた。absに修正。
    def getAbsJointAngleAcc(self, name):
        """Summary line.
        Output the angular acceleration of the absolute joint angle.
		The angular acceleration is calculated by central difference method.

        Parameters
        ----------
        name : str
            Name of joint.

        Returns
        -------
        humoArray
            The angular acceleration is output.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @retrivingModelDataany(True)
    @isModelany
    def getModelPoint(self,name,*args):
        """Summary line.
        Output data included in modeloutputs.

        Parameters
        ----------
        name : str
            The exact name contained in the header.
        *args : int
            dimension.

        Returns
        -------
        array
            The number of dimensions you specified

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingModelData(True)
    @isSegmentCOMname
    def getSegmentCOM(self, name): # multi outputには現在未対応
        """Summary line.
		Get 3D coordinates of segment COM.
        The first letter of a segment that has a distinction between left and right
        must be specified in upper case ("L" or "R").

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return

    @cvt_HumoArray(argsType="general")
    @differentation(difforder="1st")
    @retrivingModelData(False)
    @isSegmentCOMname
    def getSegmentCOMVel(self, name):# multi outputには現在未対応
        """Summary line.
		Get 3D coordinates of segment COM velocity.
        The first letter of a segment that has a distinction between left and right
        must be specified in upper case ("L" or "R").

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @differentation(difforder="2nd")
    @retrivingModelData(False)
    @isSegmentCOMname
    def getSegmentCOMAcc(self, name):# multi outputには現在未対応
        """Summary line.
		Get 3D coordinates of segment COM acceleration.
        The first letter of a segment that has a distinction between left and right
        must be specified in upper case ("L" or "R").

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return


    @cvt_HumoArray(argsType="general")
    @retrivingJointCenterData(adjustframes=True)
    @isSegmentName
    def getJointCenter(self, name):
        """Summary line.
		Get joint center coordination.

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return

    @cvt_HumoArray(argsType="general")
    @differentation(difforder="1st")
    @retrivingJointCenterData(adjustframes=False)
    @isSegmentName
    def getJointCenterVel(self, name):
        """Summary line.
		Get velocity of joint center coordination.

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return

    @cvt_HumoArray(argsType="general")
    @differentation(difforder="2nd")
    @retrivingJointCenterData(adjustframes=False)
    @isSegmentName
    def getJointCenterAcc(self, name):
        """Summary line.
		Get acceleration of joint center coordination.

        Parameters
        ----------
        name : str
            segment name.

        Returns
        -------
        humoArray
            COM coordinates of the segment.
            It is output in order of x axis, y axis and z axis.
        
		note
		------
		- If you want to get multiple data at the same time, enter a list.
        """
        return

    @cvt_HumoArray(argsType="general")
    @retrivingSegmentData(True,"angle")
    @isSegmentName
    def getSegmentAngle(self, name):
        return

    @cvt_HumoArray(argsType="general")
    @retrivingSegmentData(True,"abs")
    @isSegmentName
    def getSegmentabs(self, name):
        return

    @cvt_HumoArray(argsType="general")
    @retrivingSegmentData(True,"rel")
    @isSegmentName
    def getSegmentrel(self, name):
        return



# method for getting  data divided by trigger.
    @cvt_divHumoArray(argsType=None)
    @dividingData(dimension=3)
    def divCOM(self, step=None):
        """Summary line.
        Get COM data separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getCOM()

    @cvt_divHumoArray(argsType=None)
    @dividingData(dimension=3)
    def divCOM_floor(self, step=None):
        """Summary line.
        Get COM data projected to floor, separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getCOM_floor()

    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointAngle(self,name, step=None):
        """Summary line.
        Get joint angle separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointAngle(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointMoment(self,name ,step=None):
        """Summary line.
        Get joint moment separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointMoment(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointForce(self, name, step=None):
        """Summary line.
        Get joint force separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointForce(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointPower(self, name, step=None):
        """Summary line.
        Get joint power separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointPower(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointCenter(self, name, step=None):
        """Summary line.
        Get joint center coordinate separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointCenter(name)



    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divAbsJointAngle(self, name, step=None):
        """Summary line.
        Get joint abs angle separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getAbsJointAngle(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointAngleVel(self, name, step=None):
        """Summary line.
        Get joint angle velocity separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointAngleVel(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointAngleAcc(self, name, step=None):
        """Summary line.
        Get joint angle acceleration separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointAngleAcc(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divAbsJointAngleVel(self, name, step=None):
        """Summary line.
        Get joint abs angle velocity separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getAbsJointAngleVel(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divAbsJointAngleAcc(self, name, step=None):
        """Summary line.
        Get joint angle acceleration separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getAbsJointAngleAcc(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointCenterVel(self, name, step=None):
        """Summary line.
        Get velocity of joint center coordination separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointCenterVel(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divJointCenterAcc(self, name, step=None):
        """Summary line.
        Get acceleration of joint center coordination separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getJointCenterAcc(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentCOM(self, name, step=None):
        """Summary line.
        Get COM of segment separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getSegmentCOM(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentCOMVel(self, name, step=None):
        """Summary line.
        Get COM velocity of segment separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getSegmentCOMVel(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentCOMAcc(self, name, step=None):
        """Summary line.
        Get COM acceleration of segment separated by trigger.

        Parameters
        ----------
        name : str
            Name of joint.
        setp : list

        Returns
        -------
        humoArray

        note
        -------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
        """
        return self.getSegmentCOMAcc(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentAngle(self, name, step=None):
        return self.getSegmentAngle(name)


    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentabs(self, name, step=None):
        return self.getSegmentabs(name)

    @cvt_divHumoArray(argsType="general")
    @dividingData(dimension=3)
    def divSegmentrel(self, name, step=None):
        return self.getSegmentrel(name)
