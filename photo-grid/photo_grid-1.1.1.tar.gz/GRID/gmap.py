# basic imports
import numpy as np
import pandas as pd
import sys

# self imports
from .io import *
from .lib import *


class GMap():
    """
    """
    def __init__(self):
        """
        ----------
        Parameters
        ----------
        """

        # constant var
        self._degRot = range(-75, 90+1, 15)

        # map file
        self.pdMap = None
        self.isMap = False
        self.countNames = 0

        # dimension
        self.nAxs = [0, 0]
        self.nAxsCur = [0, 0]
        self.nRow = 0
        self.nCol = 0
        self.img = None
        self.imgBin = None
        self.imgRGB = None
        self.imgH = 0
        self.imgW = 0

        # axes
        self.angles = [0, 0]
        self.anglesCur = [0, 0]
        self.slps = [0, 0]  # 0 and 90 degrees for common images
        self.sigs = [0, 0]
        self.itcs = [0, 0]
        self.slpsReset = [0, 0]
        self.itcsReset = [0, 0]

        # output
        self.dt = None

        # progress bar
        self.flag = True
        self.subflag = True
        self.window = 1000

    def load(self, pathMap):
        """
        ----------
        Parameters
        ----------
        """

        self.pdMap = loadMap(pathMap)

        # if self.pdMap is not None:
        #     self.nRow, self.nCol = self.pdMap.shape
        #     self.isMap = True

    def findPlots(self, imgRGB, imgBin, nRow=0, nCol=0, nSmooth=100):
        """
        ----------
        Parameters
        ----------
        """

        # get image info
        self.imgBin = imgBin
        self.imgRGB = imgRGB
        self.imgH, self.imgW = imgBin.shape[:2]
        isDimAssigned = (nRow != 0 and nCol != 0)

        # if dim is assigned regardless have map or not, force changning nR and nC 
        if isDimAssigned:
            self.nAxs = [nCol, nRow]
        elif self.pdMap is not None:
            self.nAxs = [self.pdMap.shape[1], self.pdMap.shape[0]]

        # find angles and slopes
        self.angles = self.detectAngles(img=imgBin, rangeAngle=self._degRot)

        # find intercepts and make centers as pandas DT
        self.locateCenters(nSmooth)

    def detectAngles(self, img, rangeAngle):
        # evaluate each angle
        sc = []
        for angle in rangeAngle:
            imgR = rotateBinNdArray(img, angle)
            sig = imgR.mean(axis=0)
            sigFour = getFourierTransform(sig)
            sc.append(max(sigFour))

        # angle with maximum score win
        scSort = sc.copy()
        scSort.sort()
        idxMax = [i for i in range(len(sc)) if (sc[i] in scSort[-2:])]
        angles = np.array([rangeAngle[idx] for idx in idxMax])

        # sort angles (one closer to 0/90 is major angle)
        idx_major = np.argmin(angles % 90)
        angles = angles[[idx_major, abs(idx_major-1)]]

        # return
        return angles

    def locateCenters(self, nSmooth=100):
        self.slps = [1/np.tan(np.pi/180*angle) for angle in self.angles]

        # progress bar
        prog = None
        if self.flag:
            self.flag = False
            prog = initProgress(2, "Calculate slopes and intercepts")

        # find intercepts given 2 angles
        self.updateIntercepts(self.angles, self.nAxs, nSmooth)

        # get pandas data table
        updateProgress(prog, flag=self.subflag)
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)

        # end progress bar
        if self.subflag and "__main__.py" in sys.argv[0]:
            self.subflag = False
            QTimer.singleShot(
                self.window, lambda: setattr(self, "flag", True))
            QTimer.singleShot(
                self.window, lambda: setattr(self, "subflag", True))

    def updateIntercepts(self, angles, nSigs, nSmooth):
        for i in range(2):
            if (nSigs[i] == 0 or
                    self.nAxsCur[i] != nSigs[i] or
                    self.angles[i] != self.anglesCur[i]):
                sig, intercept = self.cpuIntercept(angles[i], nSigs[i], nSmooth)

                self.sigs[i] = sig
                self.itcs[i] = intercept
                # update number of peaks
                self.nAxs[i] = len(intercept)
                self.nAxsCur[i] = len(intercept)
                # update angles
                self.anglesCur[i] = self.angles[i]

        # self.imgsR_Bin[i] = imgR_bin
        # self.imgsR_RGB[i] = imgR_rgb
        # self.imgHr[i] = imgR_bin.shape[0]
        # self.imgWr[i] = imgR_bin.shape[1]

    def cpuIntercept(self, angle, nSig, nSmooth):
        imgR_bin = rotateBinNdArray(self.imgBin, angle)
        sig = findPeaks(img=imgR_bin, nPeaks=nSig, nSmooth=nSmooth)[0]
        intercept = getCardIntercept(sig, angle, self.imgH)
        if isinstance(intercept, int):
            intercept = list([intercept])
        return sig, intercept

    def getDfCoordinate(self, angles, slopes, intercepts):
        """
        ----------
        Parameters
        ----------
        """
        imgH, imgW = self.imgBin.shape
        tol = 0.025
        bdN, bdS = -imgH*tol, imgH*(1+tol)
        bdW, bdE = -imgW*tol, imgW*(1+tol)

        idxCol = 0 if abs(slopes[0]) > abs(slopes[1]) else 1
        idxRow = 1 - idxCol
        idxMaj = 0 if getClosedTo0or90(angles[0]) <= getClosedTo0or90(angles[1]) else 1
        idxMin = 1 - idxMaj

        itc_maj = np.sort(intercepts[0])
        itc_min = np.sort(intercepts[1])

        plotsMaj = []
        plotsMin = []
        pts = []

        pMaj = 0
        for itcMaj in itc_maj:  # major
            pMin = 0
            for itcMin in itc_min:  # minor
                ptX, ptY = solveLines(
                    slopes[idxMaj], itcMaj, slopes[idxMin], itcMin)
                if ptX >= bdW and ptX <= bdE and ptY >= bdN and ptY <= bdS:
                    # outside the frame but within tolerant range
                    if ptX < 0:
                        ptX = 0
                    elif ptX >= imgW:
                        ptX = imgW-1
                    if ptY < 0:
                        ptY = 0
                    elif ptY >= imgH:
                        ptY = imgH-1
                    plotsMaj.append(pMaj)
                    plotsMin.append(pMin)
                    pts.append((ptX, ptY))
                    pMin += 1
            pMaj += 1

        if idxCol == idxMaj:
            dataframe = pd.DataFrame(
                {"row": plotsMin, "col": plotsMaj, "pt": pts})
        elif idxCol == idxMin:
            dataframe = pd.DataFrame(
                {"row": plotsMaj, "col": plotsMin, "pt": pts})

        self.nRow, self.nCol = dataframe['row'].max()+1, dataframe['col'].max()+1

        # update map names
        ctNA = 0
        names = []
        for _, entry in dataframe.iterrows():
            row = entry.row
            col = entry.col
            try:
                names.append(self.pdMap.iloc[row, col])
            except Exception:
                names.append("unnamed_%d" % (ctNA))
                ctNA += 1
        dataframe['var'] = names

        # return
        return dataframe

    def getCoordinate(self, row, col):
        """
        ----------
        Parameters
        ----------
        """
        dt = self.dt
        return dt[(dt.row == row) & (dt.col == col)]['pt'].values[0]

    def getName(self, row, col):
        """
        ----------
        Parameters
        ----------
        """
        dt = self.dt
        return dt[(dt.row == row) & (dt.col == col)]['var'].values[0]

    def delAnchor(self, axis, index):
        # since numpy array required elements in same length if they were
        # temp = self.sigs.tolist()
        temp = self.sigs
        try:
            temp[axis].remove(temp[axis][index])
        except Exception:
            temp[axis] = np.delete(temp[axis], index)
        self.sigs = np.array(temp)
        # temp = self.itcs.tolist()
        temp = self.itcs
        temp[axis] = getCardIntercept(
            self.sigs[axis], self.angles[axis], self.imgH)
        self.itcs = np.array(temp)
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)

    def addMajAnchor(self, value):
        # signals
        temp = self.sigs
        try:
            temp[0].append(value)
        except Exception:
            temp[0] = np.append(temp[0], value)
        self.sigs = np.array(temp)

        # intercepts (derived from signals)
        temp = self.itcs
        temp[0] = getCardIntercept(
            self.sigs[0], self.angles[0], self.imgH)
        self.itcs = np.array(temp)

        # update dataframe
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)

    def addMinAnchor(self, itc):
        angle = self.angles[1]

        # signal
        new_signal = getSigFromItc(itc, angle, self.imgH)
        
        temp = self.sigs
        try:
            temp[1].append(new_signal)
        except Exception:
            temp[1] = np.append(temp[1], new_signal)
        self.sigs = np.array(temp)

        # intercepts
        temp = self.itcs
        try:
            temp[1].append(itc)
        except Exception:
            temp[1] = np.append(temp[1], itc)
        self.itcs = np.array(temp)

        # update dataframe
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)

    def modMajAnchor(self, index, value):
        self.sigs[0][index] = value
        self.itcs[0] = getCardIntercept(
            self.sigs[0], self.angles[0], self.imgH)
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)

    def modMinAnchor(self, index, itc):
        angle = self.angles[1]

        self.sigs[1][index] = getSigFromItc(itc, angle, self.imgH)

        # print("")
        # print("before")
        # print(self.itcs[1][index])
        # print("after")
        # print(itc)

        # self.itcs[1][index] = itc
        self.itcs[1] = getCardIntercept(
            self.sigs[1], self.angles[1], self.imgH)

        # print("=== itcs")
        # print(self.itcs[1])
        # print("=== sigs")
        # print(self.sigs[1])
        self.dt = self.getDfCoordinate(self.angles, self.slps, self.itcs)


def getClosedTo0or90(x):
    s1 = abs(abs(x)-90)
    s2 = abs(abs(x))
    return min(s1, s2)


def scaleTo0and1(array, length):
    array = np.array(array)
    return array/length


def scaleToOrg(array, length):
    array = np.array(array)
    return array*length
