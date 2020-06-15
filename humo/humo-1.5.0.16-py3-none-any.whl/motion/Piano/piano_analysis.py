import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools
import json
from functools import lru_cache

from ..main import CoreMain
from .processor import *

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


class PIANO_octaval(CoreMain):
    def __init__(self,data, SSP, ASP):
        super().__init__(data, SSP, ASP)


    #================================================================
    #   Time point calculation to output analysis interval
    #================================================================
    @lru_cache(maxsize=None)
    def select_marker(self, sampling):
        """Summary line.
        Output z coordinate of key1 marker.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """

        if sampling == 100:
            return self.getMarker("key1")[:,2]
        elif sampling == 1000:
            return self.getMarker_device("key1")[:,2]

    @lru_cache(maxsize=None)
    def select_marker2(self, sampling):
        """Summary line.
        Output z coordinate of far marker.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        if self._ID["motion"] == "front2near": marker2 = "key3"
        elif self._ID["motion"] == "front2mid": marker2 = "key3"
        elif self._ID["motion"] == "front2far": marker2 = "key4"
        if sampling == 100: return self.getMarker(marker2)[:,2]
        elif sampling == 1000: return self.getMarker_device(marker2)[:,2]

    @lru_cache(maxsize=None)
    def select_markers(self,sampling):
        marker1 = "key1"
        if self._ID["motion"] == "front2near":
            marker2 = "key3"
        elif self._ID["motion"] == "front2mid":
            marker2 = "key3"
        elif self._ID["motion"] == "front2far":
            marker2 = "key4"
        if sampling == 100:
            keyA, keyB = self.getMarker(marker1)[:,2], self.getMarker(marker2)[:,2]
        elif sampling == 1000:
            keyA, keyB = self.getMarker_device(marker1)[:,2], self.getMarker_device(marker2)[:,2]
        return keyA, keyB

    @lru_cache(maxsize=None)
    def get_threshold(self):
        return self._ID["threshold"]["key1"], self._ID["threshold"]["key2"]

    @lru_cache(maxsize=None)
    @getInterval_by_keymarker
    def getInterval_point(self, sampling):
        """Summary line.
        Output the entire analysis interval.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array
            Start point(sp) and end point(sp)
        """
        keyA = self.select_marker(sampling)
        threshold1, threshold2 = self.get_threshold()
        return keyA, threshold1


    @lru_cache(maxsize=None)
    @get_p1_point
    def p1(self, sampling):
        """Summary line.
        Outputs the keybottom point of the front keyboard.
        This point is defined as p1.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        key1 = self.select_marker(sampling)
        sp, ep = self.getInterval_point(sampling)
        return key1, sp, ep


    #@lru_cache(maxsize=None)
    #@get_p2_point
    #def p2(self, sampling):
    #    """Summary line.
    #    Outputs the release point of the front keyboard.
    #    This point is defined as p2.
#
    #    Parameters
    #    ----------
    #    sampling : int
    #        100 or 1000
#
    #    Returns
    #    -------
    #    array(1 dimension)
    #    """
    #    key1 = self.select_marker(sampling)
    #    threshold1,threshold2 = self.get_threshold()
    #    sp, ep = self.getInterval_point(sampling)
    #    return key1, threshold1, sp, ep

    @lru_cache(maxsize=None)
    @get_p2_point
    def p2(self, sampling):
        """Summary line.
        Outputs the release point of the front keyboard.
        This point is defined as p2.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        if sampling == 100:
            com = self.getSegmentCOM("Rhand")
            p4 = self.p4(sampling)
        elif sampling == 1000:
            com = self.getSegmentCOM_device("Rhand")
            p4 = self.p4(sampling)
        sp, ep = self.getInterval_point(sampling)
        return com, sp, ep, p4



    @lru_cache(maxsize=None)
    @get_p3_point
    def p3(self, sampling,name = "Rfin"):
        """Summary line.
        Outputs the point when the height of the marker during keying reaches the highest point.
        This point is defined as p3.

        Parameters
        ----------
        sampling : int
            100 or 1000
        name : str
            default is "Rfin"

        Returns
        -------
        array(1 dimension)
        """
        if sampling == 1000:
            marker = self.getMarker_device(name)[:,2]
        elif sampling == 100:
            marker = self.getMarker(name)[:,2]
        sp, ep = self.getInterval_point(sampling)
        p4 = self.p4(sampling)
        return marker, sp, ep, p4


    @lru_cache(maxsize=None)
    @get_p4_point
    def p4(self, sampling):
        """Summary line.
        Outputs the stroke point of the far keyboard.
        This point is defined as p4.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        key2 = self.select_marker2(sampling)
        threshold1,threshold2 = self.get_threshold()
        sp, ep = self.getInterval_point(sampling)
        return key2, threshold2, sp, ep


    @lru_cache(maxsize=None)
    @get_p5_point
    def p5(self, sampling):
        """Summary line.
        Outputs the keybottom point of the far keyboard.
        This point is defined as p5.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        key2 = self.select_marker2(sampling)
        threshold1,threshold2 = self.get_threshold()
        sp, ep = self.getInterval_point(sampling)
        return key2, threshold2, sp, ep


    @lru_cache(maxsize=None)
    @get_p6_point
    def p6(self, sampling):
        """Summary line.
        Outputs the release point of the far keyboard.
        This point is defined as p6.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        array(1 dimension)
        """
        key2 = self.select_marker2(sampling)
        threshold1,threshold2 = self.get_threshold()
        sp, ep = self.getInterval_point(sampling)
        return key2, threshold2, sp, ep


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p1(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p1(sampling)
        return p, sp, ep, num_type


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p2(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p2(sampling)
        return p, sp, ep, num_type


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p3(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p3(sampling)
        return p, sp, ep, num_type


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p4(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p4(sampling)
        return p, sp, ep, num_type


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p5(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p5(sampling)
        return p, sp, ep, num_type


    @lru_cache(maxsize=None)
    @normalizing_point
    def norm_p6(self,sampling,num_type):
        sp, ep = self.getInterval_point(sampling)
        p = self.p6(sampling)
        return p, sp, ep, num_type

    @lru_cache(maxsize=None)
    def get_all_point(self, sampling):
        """Summary line.
        Output all event points.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        6 arrays(1 dimension)
        """
        p1 = self.p1(sampling)
        p2 = self.p2(sampling)
        p3 = self.p3(sampling)
        p4 = self.p4(sampling)
        p5 = self.p5(sampling)
        p6 = self.p6(sampling)
        return p1, p2, p3, p4, p5, p6

    @lru_cache(maxsize=None)
    def get_norm_all_point(self, sampling, num_type):
        """Summary line.
        Output all event points.

        Parameters
        ----------
        sampling : int
            100 or 1000

        Returns
        -------
        6 arrays(1 dimension)
        """
        p1 = self.norm_p1(sampling, num_type)
        p2 = self.norm_p2(sampling, num_type)
        p3 = self.norm_p3(sampling, num_type)
        p4 = self.norm_p4(sampling, num_type)
        p5 = self.norm_p5(sampling, num_type)
        p6 = self.norm_p6(sampling, num_type)
        return p1, p2, p3, p4, p5, p6


    @lru_cache(maxsize=None)
    @getAnalysis_Interval_by_keymarker
    def getStroke_point(self,sampling):
        key_A, key_B = self.select_marker()
        threshold1, threshold2 = self.get_threshold()
        return key_A, key_B, threshold1, threshold2

    @lru_cache(maxsize=None)
    @normalized_stroke_section
    def normed_Stroke_point(self, sampling):
        sp, ep = self.getInterval_point(sampling)
        asp, asp = self.getStroke_point(sampling)
        return sp, ep, asp, asp
    @lru_cache(maxsize=None)
    
    @key_onset_figure
    def key_onset(self):
        key_A, key_B = self.select_marker()
        threshold1, threshold2 = self.get_threshold()
        return key_A, key_B, threshold1, threshold2

    #================================================================
    # [Device]
    #              Inter method
    #================================================================
    @dividingData(dimension=3)
    def interFPforce(self,name):
        sp, ep = self.getInterval_point(1000)
        data = self.getFPforce(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interFPmoment(self,name):
        sp, ep = self.getInterval_point(1000)
        data = self.getFPmoment(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interFPcop(self, name):
        sp, ep = self.getInterval_point(1000)
        data = self.getFPcop(name)
        return data, sp, ep

    #================================================================
    # [Device]
    #              Normed method
    #================================================================
    @normalizingData(dimension=3)
    def normFPforce(self,name,axis,length=1000):
        return self.interFPforce(name)

    @normalizingData(dimension=3)
    def normFPmoment(self,name,axis,length=1000):
        return self.interFPmoment(name)

    @normalizingData(dimension=3)
    def normFPcop(self,name,axis,length=1000):
        return self.interFPcop(name)

    #================================================================
    # [EMG]
    #              Inter method
    #================================================================
    @dividingData(dimension=1)
    def interEMGraw(self,emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getEMGraw(emg)
        return data, sp, ep

    @dividingData(dimension=1)
    def interEMGabs(self,emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getEMGabs(emg)
        return data, sp, ep

    @dividingData(dimension=1)
    def interEMGarv(self, emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getEMGarv(emg)
        return data, sp, ep

    @dividingData(dimension=1)
    def interSICraw(self,emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getSICraw(emg)
        return data, sp, ep

    @dividingData(dimension=1)
    def interSICabs(self,emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getSICabs(emg)
        return data, sp, ep

    @dividingData(dimension=1)
    def interSICarv(self, emg):
        sp, ep = self.getInterval_point(1000)
        data = self.getSICarv(emg)
        return data, sp, ep
    #================================================================
    # [EMG]
    #              Normalizing method
    #================================================================
    @normalizingData(dimension=1)
    def normEMGraw(self,emg,length=1000):
        return self.interEMGraw(emg), length

    @normalizingData(dimension=1)
    def normEMGabs(self,emg,length=1000):
        return self.interEMGabs(emg), length

    @normalizingData(dimension=1)
    def normEMGarv(self,emg,length=1000):
        return self.interEMGarv(emg), length

    @normalizingData(dimension=1)
    def normSICraw(self,emg,length=1000):
        return self.interSICraw(emg), length

    @normalizingData(dimension=1)
    def normSICabs(self,emg,length=1000):
        return self.interSICabs(emg), length

    @normalizingData(dimension=1)
    def normSICarv(self,emg,length=1000):
        return self.interSICarv(emg), length


    @normalizingData2(dimension=1)
    def normEMGraw2(self,emg,ep,length=1000):
        return self.interEMGraw(emg), length,ep

    @normalizingData2(dimension=1)
    def normEMGabs2(self,emg,ep,length=1000):
        return self.interEMGabs(emg), length,ep

    @normalizingData2(dimension=1)
    def normEMGarv2(self,emg,ep,length=1000):
        return self.interEMGarv(emg), length,ep

    @normalizingData2(dimension=1)
    def normSICraw2(self,emg,ep,length=1000):
        return self.interSICraw(emg), length,ep

    @normalizingData2(dimension=1)
    def normSICabs2(self,emg,ep,length=1000):
        return self.interSICabs(emg), length,ep

    @normalizingData2(dimension=1)
    def normSICarv2(self,emg,ep,length=1000):
        return self.interSICarv(emg), length,ep
    #================================================================
    # [Model]
    #              Inter method
    #================================================================
    @dividingData(dimension=3)
    def interCOM(self):
        sp, ep = self.getInterval_point(100)
        data = self.getCOM()
        return data, sp, ep

    @dividingData(dimension=3)
    def interCOM_floor(self):
        sp, ep = self.getInterval_point(100)
        data = self.getCOM_floor()
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointAngle(self,name):
        sp, ep = self.getInterval_point(100)
        if (self._ID["name"] == "niimi") and (name.lower() == "rwrist"):
            data = self.getJointAngle(name)
            data = (data + np.array([180,-180,180]))*np.array([1,-1,1])
        else:
            data = self.getJointAngle(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointMoment(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointMoment(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointForce(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointForce(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointPower(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointPower(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interAbsJointAngle(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getAbsJointAngle(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointAngleVel(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointAngleVel(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointAngleAcc(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointAngleAcc(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interAbsJointAngleVel(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getAbsJointAngleVel(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interAbsJointAngleAcc(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getAbsJointAngleAcc(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentCOM(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentCOM(name)*np.array([-1,-1,1])
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentCOMVel(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentCOMVel(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentCOMAcc(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentCOMAcc(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointCenter(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointCenter(name)*np.array([-1,-1,1])
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointCenterVel(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointCenterVel(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interJointCenterAcc(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getJointCenterAcc(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentAngle(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentAngle(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentabs(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentabs(name)
        return data, sp, ep

    @dividingData(dimension=3)
    def interSegmentrel(self,name):
        sp, ep = self.getInterval_point(100)
        data = self.getSegmentrel(name)
        return data, sp, ep


    #================================================================
    # [Model]
    #              Normalizing method
    #================================================================
    @normalizingData(dimension=3)
    def normCOM(self,axis,length=100):
        return self.interCOM()

    @normalizingData(dimension=3)
    def normCOM_floor(self,axis,length=100):
        return self.interCOM_floor(), length

    @normalizingData(dimension=3)
    def normJointAngle(self,name,axis,length=100):
        return self.interJointAngle(name),length

    @normalizingData(dimension=3)
    def normJointMoment(self,name,axis,length=100):
        return self.interJointMoment(name), length

    @normalizingData(dimension=3)
    def normJointForce(self,name,axis,length=100):
        return self.interJointForce(name), length

    @normalizingData(dimension=3)
    def normJointPower(self,name,axis,length=100):
        return self.interJointPower(name), length

    @normalizingData(dimension=3)
    def normAbsJointAngle(self,name,axis,length=100):
        return self.interAbsJointAngle(name), length

    @normalizingData(dimension=3)
    def normJointAngleVel(self,name,axis,length=100):
        return self.interJointAngleVel(name), length

    @normalizingData(dimension=3)
    def normJointAngleAcc(self,name,axis,length=100):
        return self.interJointAngleAcc(name), length

    @normalizingData(dimension=3)
    def normJointCenter(self,name,axis,length=100):
        return self.interJointCenter(name), length

    @normalizingData(dimension=3)
    def normAbsJointAngleVel(self,name,axis,length=100):
        return self.interAbsJointAngleVel(name), length

    @normalizingData(dimension=3)
    def normAbsJointAngleAcc(self,name,axis,length=100):
        return self.interAbsJointAngleAcc(name), length

    @normalizingData(dimension=3)
    def normSegmentCOM(self,name,axis,length=100):
        return self.interSegmentCOM(name), length

    @normalizingData(dimension=3)
    def normSegmentCOMVel(self,name,axis,length=100):
        return self.interSegmentCOMVel(name), length

    @normalizingData(dimension=3)
    def normSegmentCOMAcc(self,name,axis,length=100):
        return self.interSegmentCOMAcc(name), length


    @normalizingData2(dimension=3)
    def normJointAngle2(self,name,axis, ep, length=100):
        return self.interJointAngle(name),length,ep

    @normalizingData2(dimension=3)
    def normJointMoment2(self,name,axis,ep,length=100):
        return self.interJointMoment(name), length,ep

    @normalizingData2(dimension=3)
    def normJointForce2(self,name,axis,ep,length=100):
        return self.interJointForce(name), length,ep

    @normalizingData2(dimension=3)
    def normJointPower2(self,name,axis,ep,length=100):
        return self.interJointPower(name), length,ep

    @normalizingData2(dimension=3)
    def normAbsJointAngle2(self,name,axis,ep,length=100):
        return self.interAbsJointAngle(name), length,ep

    @normalizingData2(dimension=3)
    def normJointAngleVel2(self,name,axis,ep,length=100):
        return self.interJointAngleVel(name), length,ep

    @normalizingData2(dimension=3)
    def normJointAngleAcc2(self,name,axis,ep,length=100):
        return self.interJointAngleAcc(name), length,ep

    @normalizingData2(dimension=3)
    def normAbsJointAngleVel2(self,name,axis,ep,length=100):
        return self.interAbsJointAngleVel(name), length,ep

    @normalizingData2(dimension=3)
    def normAbsJointAngleAcc2(self,name,axis,ep,length=100):
        return self.interAbsJointAngleAcc(name), length,ep

    @normalizingData2(dimension=3)
    def normSegmentCOM2(self,name,axis,ep,length=100):
        return self.interSegmentCOM(name), length,ep

    @normalizingData2(dimension=3)
    def normJointCenter2(self,name,axis,ep,length=100):
        return self.interJointCenter(name), length, ep
    
    @normalizingData2(dimension=3)
    def normSegmentCOMVel2(self,name,axis,ep,length=100):
        return self.interSegmentCOMVel(name), length, ep

    @normalizingData2(dimension=3)
    def normSegmentCOMVel2_(self,name,axis,ep,length=100):
        return self.interSegmentCOMVel(name), length, ep

    @normalizingData2(dimension=3)
    def normSegmentCOMAcc2(self,name,axis,ep,length=100):
        return self.interSegmentCOMAcc(name), length, ep
    #================================================================
    # [Trajectory]
    #              Inter method
    #================================================================
    @dividingData(dimension=3)
    def interMarker(self,name):
        sp, ep = self.getInterval_point(100)
        marker = self.getMarker(name)*np.array([-1,-1,1])
        return marker, sp, ep



    @dividingData(dimension=3)
    def interMarkerVel(self,name):
        sp, ep = self.getInterval_point(100)
        marker = self.getMarkerVel(name)
        return marker, sp, ep


    @dividingData(dimension=3)
    def interMarkerAcc(self,name):
        sp, ep = self.getInterval_point(100)
        marker = self.getMarkerAcc(name)
        return marker, sp, ep


    @upsampling
    def getMarker_device(self, name):
        marker = self.getMarker(name)*np.array([-1,-1,1])
        emg_length = self.getEMGraw(1).size
        return marker, emg_length

    def getLowest_point(self,name):
        marker = self.interMarker_device(name)
        lp = [i.argmin() for i in marker]
        return np.array(lp)


    def getMarker_stroke(self, name, dist, axis=2):
        marker = self.getMarker_device(name)
        threshold1, threshold2 = self.get_threshold()
        if dist == "near":
            threshold = threshold1
        elif dist == "far":
            threshold = threshold2
        return np.diff(np.where(marker[:,axis] < threshold, 1, 0))


    @dividingData(dimension=1)
    def interMarker_device(self, name):
        sp, ep = self.getInterval_point(1000)
        marker = self.getMarker_device(name)
        return marker[:,2], sp, ep

    @dividingData(dimension=1)
    def interMarker_device2(self, name, axis):
        sp, ep = self.getInterval_point(1000)
        marker = self.getMarker_device(name)
        return marker[:,axis], sp, ep
    #================================================================
    #                normed method
    #================================================================
    @normalizingData(dimension=3)
    def normMarker(self,name,axis,length=100):
        return self.interMarker(name), length

    @normalizingData(dimension=3)
    def normMarkerVel(self,name,axis,length=100):
        return self.interMarkerVel(name), length

    @normalizingData(dimension=3)
    def normMarkerAcc(self,name,axis,length=100):
        return self.interMarkerAcc(name), length

    @normalizingData(dimension=1)
    def normMarker_device(self, name,length=1000):
        return self.interMarker_device(name), length


    @normalizingData2(dimension=3)
    def normMarker2(self,name,axis,ep,length=100):
        return self.interMarker(name), length,ep

    @normalizingData2(dimension=3)
    def normMarkerVel2(self,name,axis,ep,length=100):
        return self.interMarkerVel(name), length,ep

    @normalizingData2(dimension=3)
    def normMarkerAcc2(self,name,axis,ep,length=100):
        return self.interMarkerAcc(name), length,ep

    @normalizingData2(dimension=1)
    def normMarker_device2(self, name,ep,length=1000):
        return self.interMarker_device(name), length,ep

    @upsampling
    def getJointAngle_device(self, name):
        # 切り出しに必要
        angle = self.getJointAngle(name)
        emg_length = self.getEMGraw(1).size
        return angle, emg_length

    @upsampling
    def getSegmentCOM_device(self,name):
        # 切り出しに必要
        com = self.getSegmentCOM(name)
        emg_length = self.getEMGraw(1).size
        return com, emg_length


