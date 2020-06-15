import pandas as pd
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt

def mkdf(data,axis):
    condition = ["near","mid","far"]
    hoge = pd.DataFrame([data[0][:,axis],data[1][:,axis],data[2][:,axis]]).T
    hoge.columns = condition
    return hoge

def simps(data, sp, ep):
    emg_activity = integrate.simps(data[sp:ep], np.arange(len(data[sp:ep])))
    activity_length = ep - sp + 1
    return emg_activity / activity_length

def APDF(data,seq):
    result = []
    for i in seq:
        result.append(np.where(data < i)[0].size / data.size)
    return np.array(result)

class interEMG_fig:
    def __init__(self, data):
        self.data = data
        self.c = ["k","k","b","k","r","g"]
        self.ls = ["dotted","dotted","--","dotted","-","-"]

    def EMG_fig(self,name,num):
        emg = self.data.interSICarv(name)[num]
        p = [i[num] for i in self.data.get_all_point(1000)]
        plt.plot(emg,color="k")
        for number,i in enumerate(p): plt.plot([i,i],[0,3],color=self.c[number],ls=self.ls[number])
        plt.fill_between(np.arange(p[0],p[2]), 0, emg[p[0]:p[2]],label="moving phase",alpha=0.5)
        plt.fill_between(np.arange(p[2],p[4]), 0, emg[p[2]:p[4]],label="stroking phase",alpha=0.5)
        plt.fill_between(np.arange(p[4],p[5]), 0, emg[p[4]:p[5]],label="releasing phase",alpha=0.5)
        plt.axhline(0,color="k",alpha=0.5)
        plt.xlabel("Time [1000Hz]",fontsize=15),plt.ylabel("Amplitude [%]", fontsize=15)
        plt.title("EMG of {} [trial : {}]".format(name[1:].upper(),num+1),fontsize=15)
        plt.legend()


    def EMGs_fig(self,name1,name2,num):
        emg1 = self.data.interSICarv(name1)[num]
        emg2 = -self.data.interSICarv(name2)[num]
        p = [i[num] for i in self.data.get_all_point(1000)]
        plt.plot(emg1,color="k"),plt.plot(emg2,color="k",ls="--")
        for number,i in enumerate(p): plt.plot([i,i],[-3,3],color=self.c[number],ls=self.ls[number])
        plt.fill_between(np.arange(p[0],p[2]), emg1[p[0]:p[2]], emg2[p[0]:p[2]],label="moving phase",alpha=0.5)
        plt.fill_between(np.arange(p[2],p[4]), emg1[p[2]:p[4]], emg2[p[2]:p[4]],label="stroking phase",alpha=0.5)
        plt.fill_between(np.arange(p[4],p[5]), emg1[p[4]:p[5]], emg2[p[4]:p[5]],label="releasing phase",alpha=0.5)
        plt.axhline(0,color="k",alpha=0.5)
        plt.xlabel("Time [1000Hz]",fontsize=15),plt.ylabel("Amplitude [%]", fontsize=15)
        plt.title("EMG of {}(upper line) & {}(lower line) [trial : {}]".format(name1[1:].upper(),name2[1:].upper(),num+1),fontsize=15)
        plt.legend()

    def EMGs_fig2(self,name1,name2,num):
        emg1 = self.data.interSICarv(name1)[num]
        emg2 = self.data.interSICarv(name2)[num]
        p = [i[num] for i in self.data.get_all_point(1000)]
        plt.plot(emg1,color="k",label=name1[1:].upper()),plt.plot(emg2,color="k",ls="--",label=name2[1:].upper())
        for number,i in enumerate(p): plt.plot([i,i],[0,3],color=self.c[number],ls=self.ls[number])
        plt.axhline(0,color="k",alpha=0.5)
        plt.xlabel("Time [1000Hz]",fontsize=15),plt.ylabel("Amplitude [%]", fontsize=15)
        plt.title("EMG of {}(upper line) & {}(lower line) [trial : {}]".format(name1[1:].upper(),name2[1:].upper(),num+1),fontsize=15)
        plt.legend()




class PianoAnalysis1:
    """
    The PianoAnalysis1 class is a class that handles data structures
    including an instance for each condition.
    The structure of output data is as follows;
        - EMG (4 dimensions)
            -axis0: muscle
            -axis1: subject
            -axis2: trial
            -axis3: Time
        - Other (4 dimensions)
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
    """
    def __init__(self,data,EndPoint,length):
        self.data = data
        self.length = length
        self.NOS = len(data)
        self.AxisOfEMG = {
                        "axis0":"muscle",
                        "axis1":"subject",
                        "axis2":"trial",
                        "axis3":"time"
                        }
        self.Axis = {
                    "axis0":"axis",
                    "axis1":"subject",
                    "axis2":"trial",
                    "axis3":"time"
                    }
        # about device
        self.emg_name = list(data[0]._emg_name.keys())
        self.mus = data[0]._emg_name
        self.EndPoint = EndPoint
        self.sig = np.array([[self.data[sub].normSICarv2(emgs,
                                                        self.EndPoint)
                            for sub in range(self.NOS)]
                        for emgs in self.emg_name])
        self.sigabs = np.array([[self.data[sub].normSICabs2(emgs,
                                                        self.EndPoint)
                            for sub in range(self.NOS)]
                        for emgs in self.emg_name])

    def point(self):
        p = np.array([self.data[sub].get_all_point(1000) for sub in range(self.NOS)])
        p = np.array([p[sub][:self.EndPoint] for sub in range(self.NOS)])
        p = np.array([(p[sub]*1000 / p[sub][-1]).astype("int") for sub in range(self.NOS)])
        for i in range(self.NOS):
            p[i][-1] = p[i][-1] - 1
        return p

    def Angle(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointAngle2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def angleVel(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointAngleVel2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def angleAcc(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointAngleAcc2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def Moment(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointMoment2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def Force(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointForce2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def Power(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointPower2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def SegCOM(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normSegmentCOM2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def SegCOMVel(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normSegmentCOMVel2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def SegCOMAcc(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normSegmentCOMAcc2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def JointCenter(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointCenter2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def JointCenterVel(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointCenterVel2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def JointCenterAcc(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normJointCenterAcc2(name,
                                                            axis,
                                                            self.EndPoint,
                                                            self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def Marker(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normMarker2(name,
                                                    axis,
                                                    self.EndPoint,
                                                    self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def MarkerVel(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normMarkerVel2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                        for sub in range(self.NOS)]
                    for axis in range(3)])

    def MarkerAcc(self,name):
        """
        4 dimensions
            -axis0: Axis
            -axis1: subject
            -axis2: trial
            -axis3: Time
        """
        return np.array([[self.data[sub].normMarkerAcc2(name,
                                                        axis,
                                                        self.EndPoint,
                                                        self.length)
                            for sub in range(self.NOS)]
                        for axis in range(3)])

    def posture_joint_center(self):
        """
        Acquires joint center coordinates necessary for drawing the tapping posture.
            return:
                Rsho, Lsho, elb, wrist
        """
        Rsho = self.JointCenter("Rsjc")
        Lsho = self.JointCenter("Lsjc")
        elb = self.JointCenter("Rejc")
        wrist = self.JointCenter("Rwjc")
        hoge = {
            "Rsho":Rsho,
            "Lsho":Lsho,
            "elb":elb,
            "wrist":wrist
        }
        #return Rsho,Lsho,elb,wrist
        return hoge

    def joint_center_name_set(self):
        names = {
            "Rsho":0,
            "Lsho":1,
            "elb":2,
            "wrist":3
        }

    def posture_Segment_COM(self):
        """
        Acquires segment COM coordinates necessary for drawing the tapping posture.
            return:
                thorax, humerus, radius, hand, pelvis
        """
        thorax = self.SegCOM("thorax")
        rhumerus = self.SegCOM("Rhumerus")
        rradius = self.SegCOM("Rradius")
        rhand = self.SegCOM("Rhand")
        pelvis = self.SegCOM("pelvis")
        hoge = {
            "thorax":thorax,
            "Rhumerus":rhumerus,
            "Rradius":rradius,
            "Rhand":rhand,
            "pelvis":pelvis}
        #return thorax, rhumerus,rradius,rhand,pelvis
        return hoge

    def segment_name_set(self):
        names =  {
            "thorax":0,
            "humerus":1,
            "radius":2,
            "hand":3,
            "pelvis":4
        }
        return names


    def posture_Marker(self):
        Rasi = self.Marker("RASI")
        Lasi = self.Marker("LASI")
        Rpsi = self.Marker("RPSI")
        Lpsi = self.Marker("LPSI")
        hoge = {
            "RASI":Rasi,
            "LASI":Lasi,
            "RPSI":Rpsi,
            "LPSI":Lpsi
        }
        #return Rasi, Lasi, Rpsi, Lpsi
        return hoge
    
    def marker_name_set(self):
        names = {
            "PASI":0,
            "LASI":1,
            "RPSI":2,
            "LPSI":3
        }
        return names



def dstructure(data):
    print("Data structure")
    print("================================")
    print("Dimension : {}".format(data.ndim))
    print("Size      : {}".format(data.size))
    print("Shape     : {}".format(data.shape))
    print("================================")

class Axis:
    def __init__(self):
        self.x = 0
        self.y = 1
        self.z = 2

class Condition:
    def __init__(self):
        self.near = 0
        self.mid = 1
        self.far = 2

class Muscle_name:
    def __init__(self):
        self.Rtraps = 0
        self.Ltraps = 1
        self.Radelt = 2
        self.Rmdelt = 3
        self.Rpdelt = 4
        self.Rbiceps = 5
        self.Rtriceps = 7
        self.Rfcr = 9
        self.Recu = 12
        self.muscles = {
                        "Rtraps":0,
                        "Ltraps":1,
                        "Radelt":2,
                        "Rmdelt":3,
                        "Rpdelt":4,
                        "Rbiceps":5,
                        "Rtriceps":7,
                        "Rfcr":9,
                        "Recu":12
                        }


class Model2:
    """
    Model 2 class is a class that handles data including all experimental conditions. 
    In order to create Model 2 instances, it is necessary to store all the experimental condition instances 
    in a list and pass them as arguments.
    Each experimental condition instance consists of instances of all subjects.
    Model 2 instances consist of five dimensions: condition, axis, subject, trial, and time.
        -axis0: Condition
        -axis1: Axis
        -axis2: subject
        -axis3: Trial
        -axis4: time
    """
    def __init__(self,data,EndPoint):
        # The data contains instance about each conditions.
        # The instance contains each subject data.
        self.data = data
        self.EndPoint = EndPoint
        self.showAxis = {"axis0":"Condition",
                         "axis1":"Axis",
                         "axis2":"Subject",
                         "axis3":"Trial",
                         "axis4":"Time"}
        
    def Angle(self,name):
        return np.array([[[self.data[cond][sub].normJointAngle2(name,
                                                                axis,
                                                                self.EndPoint,
                                                                1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])
        
    def Moment(self,name):
        return np.array([[[self.data[cond][sub].normJointMoment2(name,
                                                                 axis,
                                                                 self.EngPoint,
                                                                 1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])
    
    def Force(self,name):
        return np.array([[[self.data[cond][sub].normJointForce2(name,
                                                                axis,
                                                                self.EngPoint,
                                                                1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])
    
    def Power(self,name):
        return np.array([[[self.data[cond][sub].normJointPower2(name,
                                                                axis,
                                                                self.EngPoint,
                                                                1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])
    
    def SegCOM(self,name):
        return np.array([[[self.data[cond][sub].normSegmentCOM2(name,
                                                                axis,
                                                                self.EngPoint,
                                                                1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])
    
    def JointCenter(self,name):
        return np.array([[[self.data[cond][sub].normJointCenter2(name,
                                                                 axis,
                                                                 self.EngPoint,
                                                                 1000) 
                           for sub in range(3)] 
                          for axis in range(3)] 
                         for cond in range(3)])


def average_fig_posture_frontal(sub,JointCenter,SegmentCOM,Marker,point,timing,offtorn=False):
    rsho, lsho,elb,wrist = JointCenter
    thorax, humerus, radius,hand, pelvis = SegmentCOM
    Rasi, Lasi, Rpsi, Lpsi = Marker
    point = point.mean(axis=2).astype("int")
    point = np.insert(point,0,0,axis=1)
    point = point[sub][timing]
    x0,z0 = -pelvis.mean(axis=2)[0,sub,0],pelvis.mean(axis=2)[2,sub,0]
    rsho1, rsho2 = -rsho.mean(axis=2)[0,sub]-x0, rsho.mean(axis=2)[2,sub]-z0
    lsho1, lsho2 = -lsho.mean(axis=2)[0,sub]-x0, lsho.mean(axis=2)[2,sub]-z0
    elb1, elb2 = -elb.mean(axis=2)[0,sub]-x0, elb.mean(axis=2)[2,sub]-z0
    wrist1, wrist2 = -wrist.mean(axis=2)[0,sub]-x0, wrist.mean(axis=2)[2,sub]-z0
    thorax1, thorax2 = -thorax.mean(axis=2)[0,sub]-x0, thorax.mean(axis=2)[2,sub]-z0
    pelvis1, pelvis2 = -pelvis.mean(axis=2)[0,sub]-x0, pelvis.mean(axis=2)[2,sub]-z0
    hand1, hand2 = -hand.mean(axis=2)[0,sub]-x0, hand.mean(axis=2)[2,sub]-z0
    #Rasi1, Rasi2 = -Rasi.mean(axis=2)[0,sub]-x0, Rasi.mean(axis=2)[2,sub]-z0
    #Lasi1, Lasi2 = -Lasi.mean(axis=2)[0,sub]-x0, Lasi.mean(axis=2)[2,sub]-z0
    #Rpsi1, Rpsi2 = -Rpsi.mean(axis=2)[0,sub]-x0, Rpsi.mean(axis=2)[2,sub]-z0
    #Lpsi1, Lpsi2 = -Lpsi.mean(axis=2)[0,sub]-x0, Lpsi.mean(axis=2)[2,sub]-z0
    
    if offtorn == False:
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,lw=3)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,lw=3)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,lw=3)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,lw=3)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,lw=3)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,lw=3)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,lw=3)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color="k")
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color="k")
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color="k")
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color="k")
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color="k")
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color="k",alpha=0.6)
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color="k",alpha=0.3)
    elif offtorn == True:
        color,alpha,ls = "k", 0.5, "--"
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,color=color,ls=ls,alpha=alpha)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color=color,ls=ls,alpha=alpha)

def average_fig_posture_sagital(sub,JointCenter,SegmentCOM,Marker,point,timing,offtorn=False):
    rsho, lsho,elb,wrist = JointCenter
    thorax, humerus, radius,hand, pelvis = SegmentCOM
    Rasi, Lasi, Rpsi, Lpsi = Marker
    point = point.mean(axis=2).astype("int")
    point = np.insert(point,0,0,axis=1)
    point = point[sub][timing]
    x0,z0 = -pelvis.mean(axis=2)[1,sub,0],pelvis.mean(axis=2)[2,sub,0]
    rsho1, rsho2 = -rsho.mean(axis=2)[1,sub]-x0, rsho.mean(axis=2)[2,sub]-z0
    lsho1, lsho2 = -lsho.mean(axis=2)[1,sub]-x0, lsho.mean(axis=2)[2,sub]-z0
    elb1, elb2 = -elb.mean(axis=2)[1,sub]-x0, elb.mean(axis=2)[2,sub]-z0
    wrist1, wrist2 = -wrist.mean(axis=2)[1,sub]-x0, wrist.mean(axis=2)[2,sub]-z0
    thorax1, thorax2 = -thorax.mean(axis=2)[1,sub]-x0, thorax.mean(axis=2)[2,sub]-z0
    pelvis1, pelvis2 = -pelvis.mean(axis=2)[1,sub]-x0, pelvis.mean(axis=2)[2,sub]-z0
    hand1, hand2 = -hand.mean(axis=2)[1,sub]-x0, hand.mean(axis=2)[2,sub]-z0
    #Rasi1, Rasi2 = -Rasi.mean(axis=2)[0,sub]-x0, Rasi.mean(axis=2)[2,sub]-z0
    #Lasi1, Lasi2 = -Lasi.mean(axis=2)[0,sub]-x0, Lasi.mean(axis=2)[2,sub]-z0
    #Rpsi1, Rpsi2 = -Rpsi.mean(axis=2)[0,sub]-x0, Rpsi.mean(axis=2)[2,sub]-z0
    #Lpsi1, Lpsi2 = -Lpsi.mean(axis=2)[0,sub]-x0, Lpsi.mean(axis=2)[2,sub]-z0
    
    if offtorn == False:
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,lw=3)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,lw=3)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,lw=3)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,lw=3)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,lw=3)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,lw=3)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,lw=3)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color="k",alpha=0.8)
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color="k")
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color="k",alpha=0.5)
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color="k")
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color="k")
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color="k")
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color="k")
    elif offtorn == True:
        color,alpha,ls = "k", 0.5, "--"
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,color=color,ls=ls,alpha=alpha)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color=color,ls=ls,alpha=alpha)

def average_fig_posture_horizontal(sub,JointCenter,SegmentCOM,Marker,point,timing,offtorn=False):
    rsho, lsho,elb,wrist = JointCenter
    thorax, humerus, radius,hand, pelvis = SegmentCOM
    Rasi, Lasi, Rpsi, Lpsi = Marker
    point = point.mean(axis=2).astype("int")
    point = np.insert(point,0,0,axis=1)
    point = point[sub][timing]
    x0,z0 = -pelvis.mean(axis=2)[0,sub,0],-pelvis.mean(axis=2)[1,sub,0]
    rsho1, rsho2 = -rsho.mean(axis=2)[0,sub]-x0, -rsho.mean(axis=2)[1,sub]-z0
    lsho1, lsho2 = -lsho.mean(axis=2)[0,sub]-x0, -lsho.mean(axis=2)[1,sub]-z0
    elb1, elb2 = -elb.mean(axis=2)[0,sub]-x0, -elb.mean(axis=2)[1,sub]-z0
    wrist1, wrist2 = -wrist.mean(axis=2)[0,sub]-x0, -wrist.mean(axis=2)[1,sub]-z0
    thorax1, thorax2 = -thorax.mean(axis=2)[0,sub]-x0, -thorax.mean(axis=2)[1,sub]-z0
    pelvis1, pelvis2 = -pelvis.mean(axis=2)[0,sub]-x0, -pelvis.mean(axis=2)[1,sub]-z0
    hand1, hand2 = -hand.mean(axis=2)[0,sub]-x0, -hand.mean(axis=2)[1,sub]-z0
    #Rasi1, Rasi2 = -Rasi.mean(axis=2)[0,sub]-x0, Rasi.mean(axis=2)[2,sub]-z0
    #Lasi1, Lasi2 = -Lasi.mean(axis=2)[0,sub]-x0, Lasi.mean(axis=2)[2,sub]-z0
    #Rpsi1, Rpsi2 = -Rpsi.mean(axis=2)[0,sub]-x0, Rpsi.mean(axis=2)[2,sub]-z0
    #Lpsi1, Lpsi2 = -Lpsi.mean(axis=2)[0,sub]-x0, Lpsi.mean(axis=2)[2,sub]-z0
    
    if offtorn == False:
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,lw=3)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,lw=3)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,lw=3)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,lw=3)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,lw=3)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,lw=3)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,lw=3)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color="k")
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color="k",alpha=0.7)
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color="k",alpha=0.7)
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color="k",alpha=0.3)
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color="k")
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color="k")
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color="k")
    elif offtorn == True:
        color,alpha,ls = "k", 0.5, "--"
        plt.plot(rsho1,rsho2,label="Rsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(lsho1,lsho2 ,label="Lsjc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(elb1,elb2 ,label="ejc",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(wrist1,wrist2 ,label="wjc",zorder=3,color=color,ls=ls,alpha=alpha)
        plt.plot(thorax1,thorax2 ,label="thorax COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(pelvis1,pelvis2 ,label="pelvis COM",zorder=5,color=color,ls=ls,alpha=alpha)
        plt.plot(hand1,hand2 ,label="hand COM",zorder=2,color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],lsho1[point]],[rsho2[point],lsho2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],thorax1[point]],[rsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([lsho1[point],thorax1[point]],[lsho2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([pelvis1[point],thorax1[point]],[pelvis2[point],thorax2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([rsho1[point],elb1[point]],[rsho2[point],elb2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([elb1[point],wrist1[point]],[elb2[point],wrist2[point]],color=color,ls=ls,alpha=alpha)
        plt.plot([wrist1[point],hand1[point]],[wrist2[point],hand2[point]],color=color,ls=ls,alpha=alpha)
