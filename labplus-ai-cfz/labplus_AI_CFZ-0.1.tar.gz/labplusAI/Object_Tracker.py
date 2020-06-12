# coding=UTF-8

import cv2
#labplusAI.cv2_lib.cv2 as cv2

class Object_Tracker():

    def __init__(self, method="CSRT"):
        self.initBB = None
        self.success = False
        self.box = None

        if method == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()
        elif method == "KCF":
            self.tracker = cv2.TrackerKCF_create()
        elif method == "MOSSE":
            self.tracker = cv2.TrackerMOSSE_create()
        else:
            self.tracker = None
            return

    def init(self, frame, initBB):
        self.frame = frame
        self.initBB = initBB
        if self.tracker is not None:
            self.tracker.init(frame, initBB)

    def get_box(self,frame):
        if self.tracker is not None:
            (self.success, self.box) = self.tracker.update(frame)
        if self.success == False or self.initBB == None:
            return None
        (x,y,w,h) = [int(v) for v in self.box]
        return (x,y,w,h)

    def set_box(self, frame, initBB):
        if self.tracker is None: return
        self.initBB=initBB
        self.tracker.init(frame, self.initBB)

    def select_box(self, frame):
        if self.tracker is None: return
        self.initBB = cv2.selectROI("select_object", frame, fromCenter=False, showCrosshair=True)
        self.tracker.init(frame, self.initBB)
        cv2.destroyWindow("select_object")

