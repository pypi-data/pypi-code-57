#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

from enum import Enum

from six import string_types
import wagascianpy.plotting.detector

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class Colors(Enum):
    Red = ROOT.kRed
    AlternateRed = ROOT.kRed + 2
    Green = ROOT.kGreen
    AlternateGreen = ROOT.kGreen + 2
    Blue = ROOT.kBlue
    AlternateBlue = ROOT.kBlue - 2
    Orange = ROOT.kOrange
    AlternateOrange = ROOT.kOrange + 2
    Cyan = ROOT.kCyan
    AlternateCyan = ROOT.kCyan + 2
    Azure = ROOT.kAzure
    AlternateAzuer = ROOT.kAzure + 2
    Black = ROOT.kBlack

    @classmethod
    def get_by_dif(cls, dif_id):
        dif_id = int(dif_id)
        if dif_id == 0:
            return cls.get_by_detector("WallMRD north top")
        elif dif_id == 1:
            return cls.get_by_detector("WallMRD north bottom")
        elif dif_id == 2:
            return cls.get_by_detector("WallMRD south top")
        elif dif_id == 3:
            return cls.get_by_detector("WallMRD south bottom")
        elif dif_id == 4:
            return cls.get_by_detector("WAGASCI upstream top")
        elif dif_id == 5:
            return cls.get_by_detector("WAGASCI upstream side")
        elif dif_id == 6:
            return cls.get_by_detector("WAGASCI downstream top")
        elif dif_id == 7:
            return cls.get_by_detector("WAGASCI downstream side")
        return cls.Black

    @classmethod
    def get_by_detector(cls, detector):
        name = ""
        if isinstance(detector, wagascianpy.plotting.detector.Detector):
            name = detector.name
        elif isinstance(detector, string_types):
            name = detector
        else:
            TypeError("Wrong type : {}".format(type(detector).__name__))
        if name == "WallMRD north" or name == "WallMRD north top":
            return cls.Green
        elif name == "WallMRD north bottom":
            return cls.AlternateGreen
        elif name == "WallMRD south" or name == "WallMRD south top":
            return cls.Cyan
        elif name == "WallMRD south bottom":
            return cls.AlternateCyan
        elif name == "WAGASCI upstream" or name == "WAGASCI upstream top":
            return cls.Orange
        elif name == "WAGASCI upstream side":
            return cls.AlternateOrange
        elif name == "WAGASCI downstream" or name == "WAGASCI downstream top":
            return cls.Blue
        elif name == "WAGASCI downstream side":
            return cls.AlternateBlue
        return cls.Black
