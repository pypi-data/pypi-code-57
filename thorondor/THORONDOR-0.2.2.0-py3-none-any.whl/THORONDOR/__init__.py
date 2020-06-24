#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import errno
import os
import shutil

import lmfit
from lmfit import minimize, Parameters, Parameter
from lmfit.models import LinearModel, ConstantModel, QuadraticModel, PolynomialModel, StepModel
from lmfit.models import GaussianModel, LorentzianModel, SplitLorentzianModel, VoigtModel, PseudoVoigtModel
from lmfit.models import MoffatModel, Pearson7Model, StudentsTModel, BreitWignerModel, LognormalModel, ExponentialGaussianModel, SkewedGaussianModel, SkewedVoigtModel, DonaichModel
import corner
import numdifftools
from scipy.stats import chisquare

import ipywidgets as widgets
from ipywidgets import interact, Button, Layout, interactive, fixed
from IPython.display import display, Markdown, Latex, clear_output

from scipy import interpolate
from scipy import optimize, signal
from scipy import sparse

from datetime import datetime
from importlib import reload
import pickle
import inspect
import warnings

from matplotlib import rcParams
rcParams['font.serif'] = 'Times'
rcParams['font.size'] = '14'


class Dataset():
    """A new instance of the Dataset class will be initialized for each Dataset saved in the data folder. This object is then modified by the class GUI
        For each Dataset, all the different dataframes that will be created as well as specific information e.g. E0 the edge jump can be find as attributes
        of this class. Certain attributes are instanced directly with the class, such as :
            _ Name of Dataset
            _ Path of original dataset
            _ Timestamp
		
        At the end of the data reduction, each Dataset should have at least three different data sets as attributes, saved as pandas.DataFrame,
            _ df : Original data
            _ ShiftedDf : Is one shifts the energy 
            _ ReducedDf : If one applies some background reduction or normalization method 
            _ ReducedDfSplines : If one applied the specific Splines background reduction and normalization method.

        The attributes of the class can be saved as an hdf5 file as well by using the Dataset.to_hdf5 fucntion.
        The pandas.DataFrame.to_hdf and pandas.Series.to_hdf5 functions have been use to save the data as hdf5, please use the complimentary functions 
        pandas.read_hdf to retrieve the informations.

        A Logbook entry might also be associated, under Dataset.LogbookEntry

        It is possible to add commentaries for each Dataset by using the Dataset.Comment() and to specify some additional inf with the function
        Dataset.AdditionalInfo()

        Each Dataset can be retrieved by using the function Dataset.unpickle() with argument the path of the saved Class.

        THE DATASETS CLASS IS MEANT TO BE READ VIA THE THORONDOR.GUI CLASS !!
        """

    def __init__(self, df, path, name, savedir):
        self.SavingDirectory = savedir
        self.df = df
        self.OriginalData = path
        self.Name = name
        self.Commentary = ""
        self.Author = None
        self.Instrument = None
        self.Experiment = None
        self.Purpose = None
        self.LogbookEntry = None

        self.ShiftedDf = pd.DataFrame()
        self.ReducedDf = pd.DataFrame()
        self.ReducedDfSplines = pd.DataFrame()

        try:
            self.Timestamp = datetime.utcfromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            print("Timestamp of raw file not valid")
            self.Timestamp = datetime.date.today()

        self.pickle()

    def pickle(self):
        """Use the pickle module to save the classes"""
        try:
            with open(f"{self.SavingDirectory}\\"+self.Name.split("~")[0]+".pickle", 'wb') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        except PermissionError:
            print("""Permission denied, You cannot save this file because you are not its creator. The changes are updated for this session and you can still plot figures but once you exit the program, all changes will be erased.""")
            pass

    @staticmethod
    def unpickle(prompt):
        """Use the pickle module to load the classes"""

        with open(f"{prompt}", 'rb') as f:
            return pickle.load(f)

    def AdditionalInfo(self, Author = None, Timestamp = None, Instrument = None, Experiment = None):
        self.Author = Author
        self.Instrument = Instrument
        self.Experiment = Experiment
        self.Timestamp = Timestamp
        self.pickle()

    def Comment(self, prompt, eraseall = False):
        """Precise if you want to erase the previous comments, type your comment as a string"""
        try:
            if eraseall: 
                self.Commentary = ""
            self.Commentary += prompt + "\n"
            print(self.Commentary)
            self.pickle()
        except Exception as e:
            raise e

    def __repr__(self):
        if self.Author == None:
            return "{}, created on the {}.\n".format(self.Name, self.Timestamp)
        else:
            return "{}, created by {} on the {}, recorded on the instrument {}, experiment: {}.\n".format(
            self.Name, self.Author, self.Timestamp, self.Instrument, self.Experiment)
    
    def __str__(self):        
        return repr(self)

    def to_hdf5(self, filename):
        try:

            StringDict = {keys: [value] for keys, value in self.__dict__.items() if isinstance(value, str)}
            DfDict = {keys: value for keys, value in self.__dict__.items() if isinstance(value, pd.core.frame.DataFrame)}
            SeriesDict = {keys: value for keys, value in self.__dict__.items() if isinstance(value, pd.core.series.Series)}
            
            StringDf = pd.DataFrame.from_dict(StringDict)

            for keys, value in DfDict.items():
                value.to_hdf(f"{filename}.h5", keys)
                
            StringDf.to_hdf(f"{filename}.h5", "Strings")

            for keys, value in SeriesDict.items():
                value.to_hdf(f"{filename}.h5", keys)

        except Exception as e:
            raise e



class GUI():
    """This  class is a Graphical User Interface (GUI) that is meant to be used to process important amount of XAS datasets that focus on the same energy range and absoption edge.
        There are two ways of initializing the procedure in a jupyter notebook:
            _ GUI = THORONDOR.GUI(); One will have to write the name of the data folder in which all his datasets are saved.
            _ GUI = THORONDOR.GUI.GetClassList(DataFolder = "<yourdatafolder>") if one has already worked on a dataset and wishes to retrieve his work

        This class makes extensive use of the ipywidgets and is thus meant to be used with a jupyter notebook.
        Additional informations are provided in the "ReadMe" tab of the GUI.

        The necessary Python packages are : numpy, pandas, matplotlib, glob, errno, os, shutil, ipywidgets, IPython, scipy, datetime, importlib, pickle, lmfit
        lmfit, xlrd, corner and inspect.
    """

    def __init__(self, ClassList=False):
        """All the widgets for the GUI are defined here. Two different initialization procedures are possible depending on whether or not a ClassList is given in entry.
        """

        
        self.root_path=os.getcwd()
        self.PathElements = inspect.getfile(np).split("__")[0].split("numpy")[0]+"THORONDOR\\Elements\\"
        self.PathReferences = inspect.getfile(np).split("__")[0].split("numpy")[0]+"THORONDOR\\References\\"

        if ClassList:
            self.ClassList = ClassList
            self.DataFolder = ClassList[0].SavingDirectory.split("\\ClassesSaved")[0].split("\\")[-1]

            PathOriginalData=self.root_path+"\\"+str(self.DataFolder)
            PathClasses=self.root_path+"\\"+str(self.DataFolder)+"\\ClassesSaved"
            PathDataSavedAsCsv=self.root_path+"\\"+str(self.DataFolder)+"\\Data"
            PathFigures=self.root_path+"\\"+str(self.DataFolder)+"\\Figures"

            self.Folders=[PathOriginalData, PathClasses, PathDataSavedAsCsv, PathFigures]
            self.FileLocations = sorted(glob.glob(self.Folders[0]+"\\*.txt"))
            self.Names = ["Dataset_"+f.split("\\")[-1].split(".")[0] for f in self.FileLocations]

            self.NewEnergyColumn = np.round(self.ClassList[0].df["Energy"].values, 2)
            self.InterpolStep = np.round(self.NewEnergyColumn[1] - self.NewEnergyColumn[0], 2)
            #Take shifts into account
            self.NewEnergyColumn = np.linspace(self.NewEnergyColumn[0]-20, self.NewEnergyColumn[-1]+20, int(((self.NewEnergyColumn[-1]+20) - (self.NewEnergyColumn[0]-20))/self.InterpolStep + 1))

        elif not ClassList:
            self.ClassList = []

            self.NewEnergyColumn = np.round(np.linspace(0,1000,2001), 2)
            self.InterpolStep = 0.05

        #Widgets for the initialization
        self.ListWidgetsInit = interactive(self.ClassListInitialisation,
                    DataFolder = widgets.Text(
                        value="DataFolder",
                        placeholder='<YourDataFolder>',
                        description="Datafolder:",
                        disabled=False,
                        style = {'description_width': 'initial'}),
                    FixName = widgets.Checkbox(
                        value=False,
                        description='Fix the name of the folder.',
                        disabled=False,
                        style = {'description_width': 'initial'}),
                    CreateBool = widgets.Checkbox(
                        value=False,
                        description='Create/check subdirectories for the program.',
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    DataType = widgets.Dropdown(
                        options = [".txt", ".dat", ".csv"],
                        value = ".txt",
                        description = 'Data type:',
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    DelimiterType = widgets.Dropdown(
                        options = [("Comma",","), ("Tabulation", "\t"), ("Semicolon", ";")],
                        value = "\t",
                        description = 'Column delimiter type:',
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    DecimalSeparator = widgets.Dropdown(
                        options = [("Dot", "."), ("Comma",",")],
                        value = ".",
                        description = 'Decimal delimiter type:',
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    Marker =widgets.Checkbox(
                        value=False,
                        description="Initial and final markers",
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    InitialMarker = widgets.Text(
                        value="BEGIN",
                        placeholder='<InitialMarker>',
                        description="Initial Marker:",
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    FinalMarker = widgets.Text(
                        value="END",
                        placeholder='<FinalMarker>',
                        description="Final Marker:",
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    DeleteBool = widgets.Checkbox(
                        value=False,
                        description='Delete all data and reset work !',
                        disabled=True,
                        style = {'description_width': 'initial'}),
                    WorkBool = widgets.Checkbox(
                        value=False,
                        description='Start working !',
                        disabled=True,
                        style = {'description_width': 'initial'}))
        
        self.ListWidgetsInit.children[1].observe(self.NameHandler, names='value')
        self.ListWidgetsInit.children[2].observe(self.CreateHandler, names='value')
        self.ListWidgetsInit.children[6].observe(self.MarkerHandler, names='value')
        self.ListWidgetsInit.children[9].observe(self.DeleteHandler, names='value')
        self.ListWidgetsInit.children[10].observe(self.WorkHandler, names='value')

        self.TabInit=widgets.VBox([widgets.HBox(self.ListWidgetsInit.children[:2]), self.ListWidgetsInit.children[2], widgets.HBox(self.ListWidgetsInit.children[3:6]),
            widgets.HBox(self.ListWidgetsInit.children[6:9]), widgets.HBox(self.ListWidgetsInit.children[9:11]), self.ListWidgetsInit.children[-1]])


        #Widgets for the data visualisation
        self.ListData = interactive(self.PrintData, 
            Spec = widgets.Dropdown(
                options = self.ClassList,
                description = 'Select the Dataset:',
                disabled=True,
                style = {'description_width': 'initial'}),
            PrintedDf = widgets.Dropdown(
                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"),("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                value = "df",
                description = 'Select the dataframe:',
                disabled=True,
                style = {'description_width': 'initial'}),
            ShowBool = widgets.Checkbox(
                value=False,
                description='Show dataframe',
                disabled=True,
                style = {'description_width': 'initial'}))
        self.ListData.children[2].observe(self.ShowDataHandler, names = "value")
  
        self.TabData = widgets.VBox([widgets.HBox(self.ListData.children[:3]), self.ListData.children[-1]])


        #Widgets for the treatment
        self.TabTreatment = interactive(self.TreatData,
                            method = widgets.ToggleButtons(
                                options=[("Relative shifts correction", "RelativeShift"), ("Global shift correction", "GlobalShift"), ("Gas correction", "Gas"), ("Membrane correction", "Membrane"), ("Deglitching", "Deglitching"), ("Merge energies", "Merge"),
                                ("Determine errors", "Errors"), ("Linear Combination Fit", "LCF")],
                                value ="RelativeShift",
                                description='Treatment methods:',
                                disabled=True,
                                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                tooltips=['Correct the possible energy shifts between datasets', "Correct a global energy shift", 'Correct for Gas absorption', "Correct for membrane absorption", "Deglitch alien points", "Merge datasets together and export as csv",
                                "Determine errors, see ReadMe"],
                                style = {'description_width': 'initial'}),
                            PlotBool = widgets.Checkbox(
                                value=False,
                                description='Fix method',
                                disabled=True,
                                style = {'description_width': 'initial'}))
        self.TabTreatment.children[1].observe(self.TreatmentBoolHandler, names = "value")

        self.ListRelativeShift = interactive(self.RelativeEnergyShift,
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.WidgetListRelativeShift = widgets.VBox([widgets.HBox(self.ListRelativeShift.children[:3]), self.ListRelativeShift.children[-1]])

        self.ListGlobalShift = interactive(self.GlobalEnergyShift,
                            SpecNumber = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description='Spectra to correct:',
                                disabled=False,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            Shift = widgets.FloatText(
                                step = 0.1,
                                value=1,
                                description='Shift (eV):',
                                disabled=False,
                                style = {'description_width': 'initial'}),)
        self.WidgetListGlobalShift = widgets.VBox([self.ListGlobalShift.children[0], widgets.HBox(self.ListGlobalShift.children[1:4]), self.ListGlobalShift.children[-2], self.ListGlobalShift.children[-1]])

        self.ListCorrectionGas = interactive(self.CorrectionGas,
                            SpecNumber = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description='Spectra to correct:',
                                disabled=False,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            Gas = widgets.Text(
                                value="""{"He":1, "%":100}""",
                                description='Gas.es:',
                                disabled=False,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            d = widgets.FloatText(
                                step = 0.0001,
                                value=0.0005,
                                description='Membrane thickness:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            p = widgets.FloatText(
                                value=101325,
                                description='Pressure:',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.WidgetListCorrectionGas = widgets.VBox([self.ListCorrectionGas.children[0], widgets.HBox(self.ListCorrectionGas.children[1:4]), widgets.HBox(self.ListCorrectionGas.children[4:7]), 
            self.ListCorrectionGas.children[-1]])

        self.ListCorrectionMem = interactive(self.CorrectionMem,
                            SpecNumber = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description='Spectra to correct:',
                                disabled=False,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            ApplyAll = widgets.Checkbox(
                                value=False,
                                description='Combine Gas & Membrane correction.',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.WidgetListCorrectionMem = widgets.VBox([self.ListCorrectionMem.children[0], widgets.HBox(self.ListCorrectionMem.children[1:4]), self.ListCorrectionMem.children[-2], 
            self.ListCorrectionMem.children[-1]])

        self.ListDeglitching = interactive(self.CorrectionDeglitching,
                            Spec = widgets.Dropdown(
                                options = self.ClassList,
                                description = 'Select the Dataset:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            pts = widgets.BoundedIntText(
                                value = 5, 
                                min = 1, 
                                max = 20,
                                step = 1, 
                                description = "Nb of extra points", 
                                disabled=False),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            tipo = widgets.Dropdown(
                                options = [("Linear", "linear"), ("Quadratic", "quadratic"), ("Cubic", "cubic")],
                                value = "linear",
                                description = 'Choose an order:',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.WidgetListDeglitching = widgets.VBox([widgets.HBox(self.ListDeglitching.children[:3]), widgets.HBox(self.ListDeglitching.children[3:6]), 
            self.ListDeglitching.children[-1]])

        self.ListMergeEnergies = interactive(self.MergeEnergies,
                            SpecNumber = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description='Spectra to merge:',
                                disabled=False,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "ReducedDf",
                                description = 'Show the dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("\u03BC Variance (1/\u03BC)", "\u03BC Variance (1/\u03BC)"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights"), ("RMS", "RMS"), ("User error", "UserError")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            Title =widgets.Text(
                                value="<newcsvfile>",
                                placeholder="<newcsvfile>",
                                description='Type the name you wish to save:',
                                disabled=False,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            MergeBool = widgets.Checkbox(
                                value=False,
                                description='Start merging',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.ListMergeEnergies.children[5].observe(self.MergeBoolHandler, names = "value")
        self.WidgetMergeEnergies= widgets.VBox([self.ListMergeEnergies.children[0], widgets.HBox(self.ListMergeEnergies.children[1:4]), self.ListMergeEnergies.children[-3], self.ListMergeEnergies.children[-2], self.ListMergeEnergies.children[-1]])

        self.ListErrors = interactive(self.ErrorsExtraction,
                            Spec = widgets.Dropdown(
                                options = self.ClassList,
                                description = 'Dataset:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Dataframe:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            xcol = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            ycol = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            nbpts = widgets.Dropdown(
                                options = [i for i in range (5, 20)],
                                value = 13,
                                description = 'Nb of points per interval:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            deg =widgets.IntSlider(
                                value=2,
                                min=0,
                                max=3,
                                step=1,
                                description='Degree:',
                                disabled=False,
                                orientation='horizontal',
                                continuous_update=False,
                                readout=True,
                                readout_format='d',
                                style = {'description_width': 'initial'}),
                            direction = widgets.Dropdown(
                                options = [("Left", "left"), ("Right", "right")],
                                value = "left",
                                description = 'Direction if odd:',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            ComputeBool = widgets.Checkbox(
                                value=False,
                                description='Compute errors',
                                disabled=False,
                                style = {'description_width': 'initial'}))
        self.ListErrors.children[7].observe(self.ErrorExtractionHandler, names = "value")
        self.WidgetListErrors = widgets.VBox([widgets.HBox(self.ListErrors.children[:3]), widgets.HBox(self.ListErrors.children[3:7]), self.ListErrors.children[-2], self.ListErrors.children[-1]])        

        self.ListLCF = interactive(self.LCF,
            RefSpectra = widgets.SelectMultiple(
                options = [(f.split("\\")[-1].split(".")[0], f) for f in sorted(glob.glob(f"{self.PathReferences}\\*.csv"))],
                description='Select references for LCF:',
                disabled=False,
                style = {'description_width': 'initial'},
                layout=Layout(display="flex", flex_flow='column')),
            SpecNumber = widgets.SelectMultiple(
                options=self.ClassList,
                value = self.ClassList[0:1],
                rows=5,
                description='Spectra to merge:',
                disabled=False,
                style = {'description_width': 'initial'},
                layout=Layout(display="flex", flex_flow='column')),
            Spec = widgets.Dropdown(
                options = self.ClassList,
                description = 'Select the Dataset:',
                disabled=False,
                style = {'description_width': 'initial'}),
            dftype = widgets.Dropdown(
                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                value = "ReducedDf",
                description = 'Pick the dataframe:',
                disabled=False,
                style = {'description_width': 'initial'}),
            x = widgets.Dropdown(
                options = [("Energy", "Energy")],
                value = "Energy",
                description = 'Pick an x-axis',
                disabled=False,
                style = {'description_width': 'initial'}),
            y = widgets.Dropdown(
                options = [("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                value = "Normalized",
                description = 'Pick an y-axis',
                disabled=False,
                style = {'description_width': 'initial'}),
            LCFBool = widgets.Checkbox(
                value=False,
                description='Perform LCF',
                disabled=False,
                style = {'description_width': 'initial'}),
                )
        self.WidgetListLCF = widgets.VBox([widgets.HBox(self.ListLCF.children[:2]), widgets.HBox(self.ListLCF.children[2:4]), widgets.HBox(self.ListLCF.children[4:6]), self.ListLCF.children[-2], self.ListLCF.children[-1]])

        #Widgets for the Reduction
        self.ListTabReduceMethod = interactive(self.ReduceData,
                            method = widgets.ToggleButtons(
                                options=[("Least square method", "lsf"), ("Chebyshev polynomials", "Chebyshev"), ("Polynoms", "Polynoms"), ("Single Spline", "SingleSpline"), ("Splines", "Splines")],
                                value ="lsf",
                                description='Pick reduction method:',
                                disabled=True,
                                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                tooltips=['Least Square method', 'Chebyshev Polynomials', "Multiple polynoms derived on short intervals", "Subtraction of a spline", "Pre-edge and post-edge splines determination"],
                                style = {'description_width': 'initial'}),
                            UsedClassList = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description = 'Select all the datasets to reduce together:',
                                disabled=True,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            UsedDataset = widgets.Dropdown(
                                options = self.ClassList,
                                description = 'Select the reference dataset:',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            df = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "ShiftedDf",
                                description = 'Select the dataframe:',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            PlotBool = widgets.Checkbox(
                                value=False,
                                description='Start reduction',
                                disabled=True,
                                style = {'description_width': 'initial'}))
        self.ListTabReduceMethod.children[3].observe(self.ReduceBoolHandler, names = "value")
        
        self.TabReduceMethod = widgets.VBox([self.ListTabReduceMethod.children[0], self.ListTabReduceMethod.children[1], widgets.HBox(self.ListTabReduceMethod.children[2:5]), self.ListTabReduceMethod.children[-1]])

        #Widgets for the LSF background reduction and normalization method
        self.ListReduceLSF = interactive(self.ReduceLSF,
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')),
                            interval = widgets.FloatRangeSlider(
                                min = self.NewEnergyColumn[0],
                                value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                                max = self.NewEnergyColumn[-1],
                                step = self.InterpolStep,
                                description='Energy range (eV):',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='.2f',
                                style = {'description_width': 'initial'},
                                layout = Layout(width='50%', height='40px')),
                            lam=widgets.IntSlider(
                                value=10**7,
                                min=10**4,
                                max=10**7,
                                step=1,
                                description='lambda:',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='d',
                                style = {'description_width': 'initial'}),
                            p=widgets.IntSlider(
                                value=2,
                                min=1,
                                max=100,
                                step=1,
                                description='p:',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='d',
                                style = {'description_width': 'initial'}))
        self.WidgetListReduceLSF=widgets.VBox([self.ListReduceLSF.children[0], self.ListReduceLSF.children[1], widgets.HBox(self.ListReduceLSF.children[2:4]), self.ListReduceLSF.children[-1]])

        #Widgets for the Chebyshev background reduction and normalization method
        self.ListReduceChebyshev = interactive(self.ReduceChebyshev,
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            interval = widgets.FloatRangeSlider(
                                min=self.NewEnergyColumn[0],
                                value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                                max = self.NewEnergyColumn[-1],
                                step = self.InterpolStep,
                                description='Energy range (eV):',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='.2f',
                                style = {'description_width': 'initial'},
                                layout = Layout(width='50%', height='40px')),
                            p=widgets.IntSlider(
                                value=10,
                                min=0,
                                max=100,
                                step=1,
                                description='Nb of Polynomials:',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='d',
                                style = {'description_width': 'initial'}),
                            n=widgets.IntSlider(
                                value=2,
                                min=1,
                                max=10,
                                step=1,
                                description='Importance of weights ',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='d',
                                style = {'description_width': 'initial'}))
        self.WidgetListReduceChebyshev=widgets.VBox([self.ListReduceChebyshev.children[0], self.ListReduceChebyshev.children[1], widgets.HBox(self.ListReduceChebyshev.children[2:4]), self.ListReduceChebyshev.children[-1]])

        #Widgets for the Polynoms background reduction and normalization method
        self.ListReducePolynoms = interactive(self.ReducePolynoms,
                                y = widgets.Dropdown(
                                    options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                                    ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                    value = "value",
                                    description = 'Pick an y-axis',
                                    disabled=False,
                                    style = {'description_width': 'initial'}),
                                interval = widgets.FloatRangeSlider(
                                    min=self.NewEnergyColumn[0],
                                    value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                                    max = self.NewEnergyColumn[-1],
                                    step = self.InterpolStep,
                                    description='Energy range (eV):',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='horizontal',
                                    readout=True,
                                    readout_format='.2f',
                                    style = {'description_width': 'initial'},
                                    layout = Layout(width='50%', height='40px')),
                                sL = widgets.BoundedIntText(
                                    value=4,
                                    min=4,
                                    max=11,
                                    step=1,
                                    description='Slider pts::',
                                    disabled=False,
                                    style = {'description_width': 'initial'}))
        self.WidgetListReducePolynoms=widgets.VBox([self.ListReducePolynoms.children[0], self.ListReducePolynoms.children[1], self.ListReducePolynoms.children[2], self.ListReducePolynoms.children[-1]])

        #Widgets for the single spline background reduction and normalization method
        self.ListReduceSingleSpline = interactive(self.ReduceSingleSpline,
                                y = widgets.Dropdown(
                                    options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                                    ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                    value = "value",
                                    description = 'Pick an y-axis',
                                    disabled=False,
                                    style = {'description_width': 'initial'}),
                                order = widgets.Dropdown(
                                    options = [("Select and order", "value"), ("Victoreen", "Victoreen"), ("0", 0), ("1", 1), ("2", 2), ("3", 3)],
                                    value = "value",
                                    description='Order:',
                                    disabled=False,
                                    style = {'description_width': 'initial'}),
                                interval = widgets.FloatRangeSlider(
                                    min=self.NewEnergyColumn[0],
                                    value = [self.NewEnergyColumn[0], np.round(self.NewEnergyColumn[0] + 0.33*(self.NewEnergyColumn[-1] - self.NewEnergyColumn[0]), 0)],
                                    max = self.NewEnergyColumn[-1],
                                    step = self.InterpolStep,
                                    description='Energy range (eV):',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='horizontal',
                                    readout=True,
                                    readout_format='.2f',
                                    style = {'description_width': 'initial'},
                                    layout = Layout(width='50%', height='40px')),
                                Cursor = widgets.FloatSlider(
                                    value = np.round(self.NewEnergyColumn[0] + 0.45*(self.NewEnergyColumn[-1] - self.NewEnergyColumn[0]), 0),
                                    step = self.InterpolStep,
                                    min = self.NewEnergyColumn[0],
                                    max = self.NewEnergyColumn[-1],
                                    description='Cursor:',
                                    orientation='horizontal',
                                    continuous_update=False,
                                    readout=True,
                                    readout_format='.2f',
                                    style = {'description_width': 'initial'},
                                    disabled=False),
                                ParamA = widgets.Text(
                                    value="1000000000",
                                    placeholder='A = ',
                                    description='A:',
                                    disabled=True,
                                    continuous_update=False,
                                    style = {'description_width': 'initial'}),
                                ParamB = widgets.Text(
                                    value="1000000000",
                                    placeholder='B = ',
                                    description='B:',
                                    disabled=True,
                                    continuous_update=False,
                                    style = {'description_width': 'initial'}))
        self.WidgetListReduceSingleSpline = widgets.VBox([widgets.HBox(self.ListReduceSingleSpline.children[:2]), self.ListReduceSingleSpline.children[2], self.ListReduceSingleSpline.children[3], widgets.HBox(self.ListReduceSingleSpline.children[4:6]), self.ListReduceSingleSpline.children[-1]])
        self.ListReduceSingleSpline.children[1].observe(self.ParamVictoreenHandlerSingle, names='value')

        #Widgets for the Splines background reduction and normalization method
        self.ListReduceDerivative = interactive(self.ReduceSplinesDerivative,
                            y = widgets.Dropdown(
                                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                                value = "value",
                                description = 'Pick an y-axis',
                                disabled=False,
                                style = {'description_width': 'initial'}),
                            interval = widgets.FloatRangeSlider(
                                min=self.NewEnergyColumn[0],
                                value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                                max = self.NewEnergyColumn[-1],
                                step = self.InterpolStep,
                                description='Energy range (eV):',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='.2f',
                                style = {'description_width': 'initial'},
                                layout = Layout(width='50%', height='40px')))
        self.WidgetListReduceDerivative=widgets.VBox([self.ListReduceDerivative.children[0], self.ListReduceDerivative.children[1], self.ListReduceDerivative.children[-1]])


        #Widgets for the fit, 
        self.ListFit = interactive(self.Fitting, 
            Spec = widgets.Dropdown(
                options = self.ClassList,
                description = 'Select the Dataset:',
                disabled=True,
                style = {'description_width': 'initial'}),
            PrintedDf = widgets.Dropdown(
                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                value = "df",
                description = 'Select the dataframe:',
                disabled=True,
                style = {'description_width': 'initial'}),
            ShowBool = widgets.Checkbox(
                value=False,
                description='Fix dataframe.',
                disabled=True,
                style = {'description_width': 'initial'}))
        self.ListFit.children[2].observe(self.FitHandler, names = "value")
        self.TabFit = widgets.VBox([widgets.HBox(self.ListFit.children[:3]), self.ListFit.children[-1]])

        self.ListModel = interactive(self.Model,
            xcol = widgets.Dropdown(
                options = [("Energy", "Energy")],
                value = "Energy",
                description = 'Pick an x-axis',
                disabled=False,
                style = {'description_width': 'initial'}),
            ycol = widgets.Dropdown(
                options = [("Select a value","value"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"),
                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                ("Background Corrected", "BackgroundCorrected"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights")],
                value = "\u03BC",
                description = 'Pick an y-axis',
                disabled=False,
                style = {'description_width': 'initial'}),
            interval = widgets.FloatRangeSlider(
                min=self.NewEnergyColumn[0],
                value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                max = self.NewEnergyColumn[-1],
                step = self.InterpolStep,
                description='Energy range (eV):',
                disabled=False,
                continuous_update=False,
                orientation='horizontal',
                readout=True,
                readout_format='.2f',
                style = {'description_width': 'initial'},
                layout = Layout(width='50%', height='40px')),
            PeakNumber = widgets.BoundedIntText(
                value=2,
                min=0,
                max=10,
                step=1,
                description='Amount of Peaks:',
                disabled=False,
                style = {'description_width': 'initial'}),
            PeakType = widgets.Dropdown(
                options = [("Gaussian", GaussianModel), ("Lorentzian", LorentzianModel), ("Split Lorentzian", SplitLorentzianModel), ("Voigt", VoigtModel),
                          ("Pseudo-Voigt", PseudoVoigtModel), ("Moffat", MoffatModel), ("Pearson7", Pearson7Model), ("StudentsT", StudentsTModel),
                          ("Breit-Wigner", BreitWignerModel), ("Log-normal", LognormalModel), ("Exponential-Gaussian", ExponentialGaussianModel),
                          ("Skewed-Gaussian", SkewedGaussianModel), ("Skewed-Voigt", SkewedVoigtModel), ("Donaich", DonaichModel)],
                value = LorentzianModel,
                description = 'Peak distribution:',
                disabled=False,
                style = {'description_width': 'initial'}),
            BackgroundType = widgets.Dropdown(
                options = [("Constant", ConstantModel), ("Linear", LinearModel), ("Victoreen", "Victoreen"), ("Quadratic", QuadraticModel), ("Polynomial", PolynomialModel)],
                value = ConstantModel,
                description = 'Background mode:',
                disabled=False,
                style = {'description_width': 'initial'}),
            PolDegree =widgets.IntSlider(
                value=3,
                min=0,
                max=7,
                step=1,
                description='Degree:',
                disabled=True,
                orientation='horizontal',
                continuous_update=False,
                readout=True,
                readout_format='d',
                style = {'description_width': 'initial'}),
            StepType = widgets.Dropdown(
                options = [("No step", False), ("linear", "linear"), ("arctan", "arctan"), ("erf", "erf"), ("logistic", "logistic")],
                value = False,
                description = 'Step mode:',
                disabled=False,
                style = {'description_width': 'initial'}),
            method = widgets.Dropdown(
                options = [("Levenberg-Marquardt","leastsq"), ("Nelder-Mead", "nelder"), ("L-BFGS-B", "lbfgsb"), ("BFGS", "bfgs"),
                            ("Maximum likelihood via Monte-Carlo Markov Chain", "emcee")],
                value = "leastsq",
                description = 'Pick a minimization method (read doc first):',
                disabled=False,
                style = {'description_width': 'initial'},
                layout=Layout(width='50%')),
            w = widgets.Dropdown(
                options = [("No (=1)", False), ("\u03BC Variance (1/\u03BC)", "\u03BC Variance (1/\u03BC)"), ("RMS", "RMS"), ("User error", "UserError")],
                value=False,
                description='Use weights.',
                disabled=False,
                style = {'description_width': 'initial'}),
            FixModel = widgets.Checkbox(
                value=False,
                description='Fix Model.',
                disabled=False,
                style = {'description_width': 'initial'}))
        self.WidgetListFit=widgets.VBox([widgets.HBox(self.ListModel.children[0:2]), self.ListModel.children[2], widgets.HBox(self.ListModel.children[3:5]),
            widgets.HBox(self.ListModel.children[5:8]), widgets.HBox(self.ListModel.children[8:11]), self.ListModel.children[-1]])
        self.ListModel.children[10].observe(self.ModelHandler, names = "value")
        self.ListModel.children[5].observe(self.ModelDegreeHandler, names = "value")


        #Widgets for the plotting
        self.ListWidgetsPlot = interactive(self.PlotDataset,
                            SpecNumber = widgets.SelectMultiple(
                                options=self.ClassList,
                                value = self.ClassList[0:1],
                                rows=5,
                                description='Spectra to plot:',
                                disabled=True,
                                style = {'description_width': 'initial'},
                                layout=Layout(display="flex", flex_flow='column')),
                            Plotdf = widgets.Dropdown(
                                options = [("Renamed data", "df"), ("Shifted Df", "ShiftedDf"), ("Reduced data", "ReducedDf"), ("Reduced by Splines", "ReducedDfSplines"), ("Fit Df", "FitDf")],
                                value = "df",
                                description = 'Show the dataframe:',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            x = widgets.Dropdown(
                                options = [("Energy", "Energy")],
                                value = "Energy",
                                description = 'Pick an x-axis',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            y = widgets.Dropdown(
                                options = [("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"),
                                ("Gas Corrected", "GasCorrected"), ("Membrane Corrected", "MembraneCorrected"), ("Gas & Membrane corrected", "GasMemCorr"),
                                ("Background Corrected", "BackgroundCorrected"), ("\u03BC Variance (1/\u03BC)", "\u03BC Variance (1/\u03BC)"), ("Normalized", "Normalized"), ("Fit", "Fit"), ("Weights", "Weights"), ("RMS", "RMS"), ("User error", "UserError")],
                                value = "\u03BC",
                                description = 'Pick an y-axis',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            xaxis =widgets.Text(
                                value='Energy',
                                placeholder ="Energy",
                                description='Type the name of the x axis:',
                                disabled=True,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            yaxis =widgets.Text(
                                value='Intensity',
                                placeholder='Intensity',
                                description='Type the name of the y axis:',
                                disabled=True,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            Title =widgets.Text(
                                value='Plot',
                                placeholder='Plot',
                                description='Type the title you wish to use:',
                                disabled=True,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            CheckPlot = widgets.ToggleButtons(
                                options=[('Clear',"Zero"), ('Plot', "Plot"), ("3D", "3D")],
                                value ="Zero",
                                description='Plot:',
                                disabled=True,
                                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                tooltips=['Nothing is plotted', 'We plot one Dataset', 'We plot all the spectra'],
                                style = {'description_width': 'initial'}))
        self.TabPlot=widgets.VBox([self.ListWidgetsPlot.children[0], widgets.HBox(self.ListWidgetsPlot.children[1:4]), 
                                widgets.HBox(self.ListWidgetsPlot.children[4:7]), self.ListWidgetsPlot.children[-2], self.ListWidgetsPlot.children[-1]])


        #Widgets for the logbook
        self.ListLogbook = interactive(self.PrintLogbook,
                            LogName = widgets.Text(
                                value="Logbook.xlsx",
                                placeholder='<logbookname>.xlsx',
                                description='Type the name of the logbook:',
                                disabled=True,
                                continuous_update=False,
                                style = {'description_width': 'initial'}),
                            LogBool = widgets.Checkbox(
                                value=True,
                                description='Reset and hide logbook',
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            column = widgets.Text(
                                value="Quality",
                                placeholder='Quality',
                                description='Column:',
                                continuous_update=False,
                                disabled=True,
                                style = {'description_width': 'initial'}),
                            value = widgets.Text(
                                value="True",
                                placeholder='True',
                                description='Value:',
                                continuous_update=False,
                                disabled=True,
                                style = {'description_width': 'initial'})
                            )
        self.TabLogbook = widgets.VBox([widgets.HBox(self.ListLogbook.children[:2]), widgets.HBox(self.ListLogbook.children[2:4]), self.ListLogbook.children[-1]])


        #Widgets for the ReadMe
        self.TabInfo = interactive(self.ShowInfo, 
                            Contents = widgets.ToggleButtons(
                                options=['Treatment', 'Background', 'Fit'],
                                value ="Treatment",
                                description='Show info about:',
                                disabled=False,
                                tooltips=['Nothing is shown', 'Insight in the functions used for treatment', 'Insight in the functions used for Background', 'Insight in the functions used for fitting'],
                                style = {'description_width': 'initial'}))

        #Create the final window
        self.Window = widgets.Tab(children=[self.TabInit, self.TabData, self.TabTreatment, self.TabReduceMethod, self.TabFit, self.TabPlot, self.TabLogbook, self.TabInfo])
        self.Window.set_title(0, 'Initialize')
        self.Window.set_title(1, 'View Data')
        self.Window.set_title(2, 'Treatment')
        self.Window.set_title(3, 'Reduce Dataset')
        self.Window.set_title(4, 'Fit Data')
        self.Window.set_title(5, 'Plot')
        self.Window.set_title(6, 'Logbook')
        self.Window.set_title(7, 'Readme')


        #Display window
        if ClassList:
            self.ListWidgetsInit.children[0].value = self.DataFolder
            self.ListWidgetsInit.children[1].value = True
            self.ListWidgetsInit.children[2].value = True
            self.ListWidgetsInit.children[10].value = False

            for w in self.ListWidgetsInit.children[:-2]:
                w.disabled = True

            for w in self.ListData.children[:-1] + self.TabTreatment.children[:-1] + self.ListTabReduceMethod.children[:-1] + self.ListFit.children[:-1] + self.ListWidgetsPlot.children[:-1] + self.ListLogbook.children[:-1]:
                w.disabled = False

            #Show the  plotting first
            self.Window.selected_index = 5

            display(self.Window)

        elif not ClassList:
            display(self.Window)

    #Readme interactive function
    def ShowInfo(self, Contents):
        """All the necessary information to be displayed via the ReadMe tab are written here in a Markdown format."""

        if Contents == "Treatment":
            clear_output(True)
            display(Markdown("""## Basic informations"""))
            display(Markdown("""The raw data files from the instrument you must save in the "Datafolder" folder that you specify in entry. 
                Please create the folder and move the files inside. If there is a problem, open one file and verify the delimiter and type of the data.
                The notebook needs to be in the same directory as the datafolder containing your datafiles.
                Each datafile must have an integer name."""))
            display(Markdown("""There is a known issue when importing data files that have a comma instead of a dot as decimal separator, please use a
                dot ! Modify in the initialisation tab if needed."""))
            display(Markdown("""All the datasets that you create are saved in <datafolder>/Data as .csv files.
                The figures in <datafolder>/Figures."""))

            display(Markdown("""### Interpolation"""))
            display(Markdown("""Interpolating the data is recommended if you have a different amount of points and/or a different energy range between the different datasets.
                We use the scipy technique involving splines, details can be found here : https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
                There is no smoothing of the data points."""))

            display(Markdown("""### Logbook"""))
            display(Markdown("""The Logbook needs to be in an excel format, please follow : 
                https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html.
                The logbook also needs to be in the same directory as the datafolder containing your datafiles."""))
            display(Markdown("""The logbook importation routine assumes that the name of each dataset is stored in a \"Name\" column. The names MUST BE the same names
                as the datasets given in entry to the program. The pnly other possibility is to have the names preceded of \"scan_\", followed by the dataset number.
                E.g, for a file \"215215.txt\" given in entry, in the logbook its name is either \"215215\"" or \"scan_215215\"."""))
            
            display(Markdown("""<strong>IMPORTANT NOTICE</strong>"""))
            display(Markdown("""This program only considers a common energy range to all spectra, if you work on another energy range, please create 
                by hand a new folder, put your data there, and create a new notebook dedicated to this energy range that works on this datafolder.
                Basically, one notebook works on one folder where all the data files have a common energy range (and incrementation). Create different 
                datafolders if you work on different absorption edges !"""))
            display(Markdown("""Throughout your work, the docstring of each function is available for you by creating a new cell with the `plus` button 
                at the top of your screen and by typing: `help(function)`. The detail of the GUI can be accessed by `help(THORONDOR.GUI)`."""))
            display(Markdown("""The classes that are continuously saved and that can be reimported through `GUI = THORONDOR.GUI.GetClassList(DataFolder = "<yourdatafolder>")`
                are instances of the Dataset class. For details, please type : `help(THORONDOR.Dataset)`"""))
            
            display(Markdown("""## 1) Extract Data"""))
            display(Markdown("""$I_s$, $I_m$ and $I_t$ are extracted from the experimental data. These notations follow the work environment of APE-He, the 
                ambient pressure soft x-ray absorption spectroscopy beamline at Elettra, where the NEXAFS spectra are recorded in Transmission Electron Yield (TEY).
                Two electrical contacts allow us to polarize the membrane (positively in order to accelerate the electrons away from the sample), and to 
                measure the drain current from the sample through a Keithley 6514 picoammeter (Rev. Sci. Instrum. 89, 054101 (2018)).
                The absorption spectrum is usually acquired by moving the monochromator with a discrete step and recording the TEY intensity at this energy, 
                repeating this operation for the entire range of interest.
                During the continuous or “fast scan” data acquisition mode, the grating monochromator is scanned continuously through the wanted energy range
                and the picoammeter signal is recorded in the streaming mode.
                $I_m$ is the incoming photon intensity, that is used to normalize the intensity collected from the membrane. Indeed, a different photon flux 
                covers the membrane at different energy.
                $I_t$ = $\\frac{I_s}{I_m}$ is the TEY intensity from the sample, normalized by the incoming photon flux."""))
            
            display(Markdown("""## 2) Energy shifts"""))
            display(Markdown("""You must find the shift by selecting a reference feature in the reference column of your dataset. For users of APE-He, the mesh
             or Keithley both provide static features that allow you to align your datasets. First, choose the reference dataset to which all the other datasets
             will be shifted, and use the cursor to pick the reference point on this dataset. 
             The shift is then computed as the difference between the energy that corresponds to the reference cursor and the energy that corresponds to the cursor 
             that you chose on the other datasets. The new data frame is saved as \"ShiftedDf\" and also as a \"<name>_Shifted.csv\" file.
             it is possible to apply a global shifts to the datasets, e.g. if the position of the peaks are known from literature."""))

            display(Markdown("""## 3)  Transmittance Correction"""))
            display(Markdown("""When measuring the drain current in the reactor cell (both from the sample and the membrane), we need to take into account that
             several sources of electrons are present due to the absorption of the primary beam by the reactor cell membrane, the reactant gas, and the sample.
             This effects have been described in Castán-Guerrero, C., Krizmancic, D., Bonanni, V., Edla, R., Deluisa, A., Salvador, F., Rossi, G., Panaccione,
              G., & Torelli, P. (2018). A reaction cell for ambient pressure soft x-ray absorption spectroscopy. Review of Scientific Instruments, 89(5).
              https://doi.org/10.1063/1.5019333 .
              The additional terms to the TEY intensity from the sample can be considered constant as due to constant cross sections, assuming that there are
               no absorption edges of elements present in the membrane or in the gas in the scanned energy range.
              This GUI provides corrections for the X-ray transmittance factors linked to both the gas inside the cell and the membrane."""))

            display(Markdown("""### 3.1) Control Parameters:"""))
            display(Markdown("""The parameters $d$ and $p$ represent, respectively, the gas thickness and the total gas pressure in the cell. Each gas that is
                in the cell must be written as a dictionnary, with each element next to its stochiometry and the total percentage of this gas in the cell. The 
                primary interaction of low-energy x rays within matter, viz. photoabsorption and coherent scattering, have been described for photon energies 
                outside the absorption threshold regions by using atomic scattering factors, $f = f_1 + i f_2$. The atomic photoabsorption cross section,
                $µ_a$ may be readily obtained from the values of $f_2$ using the following relation,
                $μ_a = 2r_0 λf_2$
                where $r_0$ is the classical electron radius, and $λ$ is the wavelength. The transmission of x rays through a slab of thickness $d$ is
                then given by,
                $T = \exp (- n \,µ_a d)$
                where n is the number of atoms per unit volume in the slab. In a first approach:
                $n = \\frac{p}{k_b T}$
                ref : http://henke.lbl.gov/optical_constants/intro.html"""))
            display(Markdown("""<strong>Please respect the following architecture when using this function:</strong>"""))
            display(Markdown("""E.g.: `{"C":1, "O":1, "%":60}, {"He":1, "%":20}, {"O":1, "%":20}`"""))
            display(Markdown("""You may put as many gas as you want, the sum of their percentage must be equal to 1 !The values of $d$, the membrane 
                thickness and $p$, the gas pressure can change but respect the units (meters and Pascals). In the left pannel is reported the imaginary 
                part of the scattering factor $f_{2}$ plotted vs the energy for the different elements involved in the gas feed composition.
                On the right pannel is reported the transmittance trend of the gas feed for each spectra. To change the temperature, you must associate the
                entries in the Logbook tab."""))

            display(Markdown("""### 3.2)  Transmittance correction for the membrane:"""))
            display(Markdown("""The correction due to the membrane is based on the $Si_3 N_4$ membrane used at APE-He in Elettra."""))

            display(Markdown(""" ## 4)  Degliching"""))
            display(Markdown("""Once that the glitch region has been isolated, three kind of functions $(linear, quadratic, cubic)$ can be used 
                to remove it. By pressing the button "Deglich" the modication is directely saved. The "DeGliching" routine returns the degliched data."""))

        if Contents == "Background":
            clear_output(True)
            display(Markdown("""### Case n° 1: Least Squares"""))
            display(Markdown("""This kind of data normalization form is based on the the "Asymmetric Least Squares Smooting" technique. 
                More information about it can be found in : "Baseline Correction with Asymmetric Least SquaresSmoothing" 
                of Paul H. C. Eilers and Hans F.M. Boelens. The background removal procedure is regulated by two parameters: 
                $p$ and $\lambda$. The first parameter: p regulates the asymmetry of the background and it can be moved in the 
                following range: $0.001\leq p \leq 0.1$   while $\lambda$ is a smoothing parameter that can vary between $10^{2}$ 
                and $10^{9}$."""))

            display(Markdown(""" ### Case n°2 : Chebyshev polynomials"""))
            display(Markdown("""First kind Chebyshev polynomialsTn, especially for high temperatures.  The weights as well as the degree N of the equation
            were found empirically. The weights taken during the weighed least squares regression are simply taken as the square of the variance of the 
            counting statistics. The background is then given by:
                $f(x, \\vec{a}) = \sum_{n=0}^N a_n T_n(x) \, + \, \epsilon$
                with $a_n$ the $N+ 1$ coefficients determined by the weighed least square regression."""))

            display(Markdown("""### Case n°3: Polynoms"""))
            display(Markdown(""" The "Polynoms" function allows user to perform the data subtraction using the `splrep` method of the SciPy package (Virtanen).
             Once that the user fixed the energy range of interest and the amount of slider points, each point on the related curve can be moved through sliders.
             Two or more point can not take the same value. In this case the background curve is not plotted."""))

            display(Markdown("""### Case n°4: Data Reduction and Normalization with Splines"""))

            display(Markdown("""#### 1) E0 selection:"""))
            display(Markdown("""We must first fix the edge jump "E0" for each Dataset ! Attention, if there is a pre-edge, it is possible that the 
                finding routine will fit on it instead than on the edje-jump. Please readjust manually in that case."""))

            display(Markdown("""#### 2) Data Normalization:"""))
            display(Markdown("""The data is normalised by the difference between the value of both polynomials at the point E0. 
                Away from edges, the energy dependence fits a power law: $µ \\sim AE^{-3}+BE^{-4}$ (Victoreen)"""))

        if Contents == "Fit":
            clear_output(True)
            display(Markdown("""### Process modelling"""))
            display(Markdown("""Process modelling is defined as the description of a <strong>response variable</strong> $y$ by the summation of a deterministic component 
                given by a <strong>mathematical function</strong> $f(\\vec{x},\\vec{\\beta})$ plus a random error $\\epsilon$ that follows its own probability distribution 
                (see the engineering statistics handbook published by the National Institute of Standards and Technology). """))
            display(Markdown("""We have: $\\quad y = f(\\vec{x};\\vec{\\beta}) + \\epsilon$"""))
            display(Markdown("""Since the model cannot be solely equaled to the data by the deterministic mathematical function $f$, we talk of statistical model that are only relevant for the 
                average of a set of points y. Each response variable $\\vec{y_i}$ defined by the model is binned to a predictor variable $\\vec{x_i}$ which are inputs to the 
                mathematical function. $\\vec{\\beta}$ is the set of parameters that will be used and refined during the modelling process."""))
            display(Markdown("""In general we have:"""))
            display(Markdown("""$\\quad \\vec{x} \\equiv (x_1, x_2,..., x_N),$"""))
            display(Markdown("""$\\quad \\vec{y} \\equiv (y_1, y_2,..., y_N),$"""))
            display(Markdown("""$\\quad \\vec{\\beta} \\equiv (\\beta_1,\\beta_2, ..., \\beta_M)$"""))
            display(Markdown("""It is important to differentiate between errors and residuals, if one works with a sample of a population and evaluates the deviation between one element of the 
                sample and the average value in the sample, we talk of residuals. However, the error is the deviation between the value of this element and the the average on the 
                whole population, the true value that is unobservable. For least squares method, the residuals will be evaluated, difference between the observed value and the 
                mathematical function."""))
            display(Markdown("""The value of the parameters is usually unknown before modelling unless for simulation experiments where one uses a model with a predetermined set of 
                parameters to evaluate its outcome. For refinement, the parameters can be first-guessed and approximated from literature (e.g. the edge jump) but it is the 
                purpose of the refinement to lead to new and accurate parameters. The relation between the parameters and the predictor variables depends on the nature of our problem."""))
            display(Markdown("""### Minimization process"""))
            display(Markdown("""The "method of least squares" that is used to obtain parameter estimates was independently developed in the late 1700's and the early 1800's by the 
                mathematicians Karl Friedrich Gauss, Adrien Marie Legendre and (possibly) Robert Adrain [Stigler (1978)] [Harter (1983)] [Stigler (1986)] working in Germany, France 
                and America, respectively."""))
            display(Markdown("""To find the value of the parameters in a linear or nonlinear least squares method, we use the weighed least squares method. 
                The function $f(\\vec{x}, \\hat{\\vec{\\beta}})$ is fitted to the data $y$ by minimizing the following criterion:"""))
            display(Markdown("""$\chi^2 = \sum_{i=0}^N W_i \\big( y_i-f(x_i; \\hat{\\vec{\\beta}}) \\big)^2 = \\sum_{i=0}^N W_i \, r_i^2$"""))
            display(Markdown("""with N the amount of ($\\theta_i, y_i$) bins in our experiment and $r_i$ the residuals."""))
            display(Markdown("""The sum of the square of the deviations between the data point $y_i$ of the ($\\theta_i, y_i$) bin and the corresponding $f(\\vec{x_i}; \\hat{\\vec{\\beta}})$
            in the model is minimized. For nonlinear models such as ours, the computation must be done via iterative algorithms. The algorithm finds the solution of a system in which each 
            of the partial derivative with respect to each parameter is zero, i.e. when the gradient is zero."""))
            display(Markdown("""Documentation for lmfit can be found here : https://lmfit.github.io/lmfit-py/intro.html"""))

            display(Markdown("""### Fitting guidelines"""))
            display(Markdown("""In general, a NEXAFS spectrum is always characterized by resonances corresponding to different transitions from an occupied core
                state to an unfilled final state (Gann et al., 2016). These resonances can be usually modelled as peak shapes, properly reproduced by Lorentzian
                peak-functions (de Groot, 2005; Henderson et al., 2014; Stöhr, 1992; Watts et al., 2006). The procedure of peak decomposition becomes extremely
                important when one wants to decompose a NEXAFS spectrum into a set of peaks where each of them can be assigned to an existing electronic transition.
                Finally, spectral energy shifts for a set of scans can be recovered from the fitting procedure too, they correspond to the inflexion point in the
                ionization potential energy step function (i.e. the maximum of their first derivatives). The evaluation of these quantities is extremely important
                because they properly indicate the presence of reduction or oxidation phenomena involving the system under study, the fitting procedure allows the
                user to extract rigorous mathematical values from the data."""))

            display(Markdown("""THORONDOR offers a large class of peak functions including Gaussian, Lorentzian, Voight and pseudo-Voigt profiles. The signal ionization potential
                step can be properly modelled using an arc-tangent function (Poe et al., 2004) as well as an error function, also proven suitable for the usage
                (Henderson et al., 2014; Outka & Stohr, 1988). In general, the user should pick a step-function according to his knowledge prior to the fitting,
                since it has been shown that the width of the error function is related to the instrumental resolution (Outka & Stohr, 1988), whereas the width of
                the arc-tangent is related to the life time of the excited state. The step localization depends on the quality of the spectrum, usually several eV
                below the core level ionization energy (Outka & Stohr, 1988). Sometimes, the background in the pre-edge can slightly differ from the step function
                due to features linked to transition to the bound states in the system (de Groot, 2005). In THORONDOR, if one wishes to focus on that energy range,
                it is possible to use splines of different order to fit the baseline for those energy values and then pass to fit and normalize the pre-edge peaks
                (Wilke et al., 2001)"""))

            display(Markdown("""### The basic differences between a Gaussian, a Lorentzian and a Voigt distribution:"""))

            def gaussian(x, amp, cen, wid):
                return amp * np.exp(-(x-cen)**2 / wid)

            x = np.linspace(-10, 10, 101)
            y = gaussian(x, 4.33, 0.21, 1.51) + np.random.normal(0, 0.1, x.size)

            modG = GaussianModel()
            parsG = modG.guess(y, x=x)
            outG = modG.fit(y, parsG, x=x)

            modL = LorentzianModel()
            parsL = modL.guess(y, x=x)
            outL = modL.fit(y, parsL, x=x)

            modV = VoigtModel()
            parsV = modV.guess(y, x=x)
            outV = modV.fit(y, parsV, x=x)

            fig, axs=plt.subplots(figsize = (10, 6))

            # axs.plot(x, y, 'b')
            # axs.plot(x, outG.init_fit, 'k--', label='initial fit')
            axs.plot(x, outG.best_fit, label='Gaussian')

            # axs.plot(x, outL.init_fit, 'k--', label='initial fit')
            axs.plot(x, outL.best_fit, label='Lorentzian')

            # axs.plot(x, outV.init_fit, 'k--', label='initial fit')
            axs.plot(x, outV.best_fit, label='Voigt')
            axs.legend()
            plt.show()


    #Initialization function if previous work had been done
    def GetClassList(DataFolder):
        """Retrieve all the classes, that corespond to the dataset in the folder at <location>"""
        root_path=os.getcwd()
        PathClasses=root_path+"\\"+str(DataFolder)+"\\ClassesSaved"
        ClassesLocations = sorted(glob.glob(PathClasses+"\\*.pickle"))
        Names = ["Dataset_"+f.split("\\")[-1].split(".")[0] for f in ClassesLocations]
        ClassList = []

        for n, f in zip(Names, ClassesLocations):
            try :
                ClassList.append(Dataset.unpickle(f))

            except EOFError: 
                print(f"{n} is empty, restart the procedure from the beginning, this may be due to a crash of Jupyter.")
            except FileNotFoundError:
                print(f"The Class does not exist for {n}")

        return GUI(ClassList)

    #Initialization interactive function, if no previous work had been done
    def ClassListInitialisation(self, DataFolder, FixName, CreateBool, DataType, DelimiterType, DecimalSeparator, Marker, InitialMarker, FinalMarker, DeleteBool, WorkBool):
        """Function that generates or updates three subfolders in the "root_path":
            _ DataFiles where you will save your raw data files.
            _ DataFiles\\Data where the data files will be saved, in .txt after cleaning of strings.
            _ DataFiles\\ClassesSaved where the data will be saved as a class at the end of your work.
        """

        if FixName:
            self.DataFolder = DataFolder

            PathOriginalData=self.root_path+"\\"+str(self.DataFolder)
            PathClasses=self.root_path+"\\"+str(self.DataFolder)+"\\ClassesSaved"
            PathDataSavedAsCsv=self.root_path+"\\"+str(self.DataFolder)+"\\Data"
            PathFigures=self.root_path+"\\"+str(self.DataFolder)+"\\Figures"

            self.Folders=[PathOriginalData, PathClasses, PathDataSavedAsCsv, PathFigures]
            self.FileLocations = sorted(glob.glob(f"{self.Folders[0]}\\*{DataType}"))
            self.Names = ["Dataset_"+f.split("\\")[-1].split(".")[0] for f in self.FileLocations]

        if FixName and CreateBool:
            clear_output=(True)

            for folder in self.Folders:
                if not os.path.exists(folder):
                    try:
                        os.makedirs(folder)
                        print(f"{folder} well created.\n")
                    except FileExistsError:
                        print(f"{folder} already exists.\n")
                    except Exception as e:
                        raise e
        
        if FixName and DeleteBool:
            """Deletes the files that are in the subdirectory "data" of the argument directory, 
            To be used if one wants to start the data reduction again and needs a clean data directory"""
            self.ListData.children[0].options = []
            self.ListCorrectionGas.children[0].options = []
            self.ListCorrectionMem.children[0].options = []
            self.ListMergeEnergies.children[0].options = []
            self.ListTabReduceMethod.children[1].options = []
            self.ListTabReduceMethod.children[2].options = []
            self.ListDeglitching.children[0].options = []
            self.ListFit.children[0].options = []
            self.ListWidgetsPlot.children[0].options = []
            self.ListErrors.children[0].options = []
            self.ListLCF.children[1].options = []
            self.ListLCF.children[2].options = []

            CleanedFolder=[PathClasses, PathDataSavedAsCsv, PathFigures]
            for f in CleanedFolder:
                for the_file in os.listdir(f):
                    file_path = os.path.join(f, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as e:
                            print(e)

            print("Work has been reset")
            clear_output=(True)

        if not WorkBool:
            for w in self.ListData.children[:-1] + self.TabTreatment.children[:-1] + self.ListTabReduceMethod.children[:-1] + self.ListFit.children[:-1] + self.ListWidgetsPlot.children[:-1] + self.ListLogbook.children[:-1] :
                if w.disabled == False:
                    w.disabled = True

        if WorkBool:
            print("""We now start to manipulate the data.\nFirst, rename each column and select the one we want to use.""")
            clear_output=(True)

            def Renaming(NbColumns, NewName):
                ButtonSaveName = Button(
                    description="Save Name",
                    layout=Layout(width='15%', height='35px'))
                ButtonSaveList = Button(
                    description="Show new df",
                    layout=Layout(width='25%', height='35px'))
                display(widgets.HBox((ButtonSaveName, ButtonSaveList)))

                @ButtonSaveName.on_click
                def ActionSaveName(selfbutton):
                    if NewName == "select":
                        print("Please select a value")
                    else:
                        self.newnames[NbColumns] = NewName
                        print(f"Column renamed")
                        print(f"The list of new names is currently {self.newnames}.")

                @ButtonSaveList.on_click
                def ActionSaveList(selfbutton):
                    #Apply the renaming to all the files given in entry only if name given for each column and at least one column names energy
                    if all([i is not None for i in self.newnames]):
                        usecol = [i for i,j in enumerate(self.newnames) if j != "notused"]
                        namae = [j for i,j in enumerate(self.newnames) if j != "notused"]

                        try:
                            datasetrenamed = pd.read_csv(self.FileLocations[0], sep = DelimiterType, header=0, names = namae,  usecols = usecol, decimal=DecimalSeparator).abs()
                            datasetrenamed = datasetrenamed.sort_values("Energy").reset_index(drop=True)

                            print("This is the renamed data.")
                            display(datasetrenamed.head())

                            ButtonSaveNameAllNoInterpol = Button(
                                description="Keep and continue without interpolation.",
                                layout=Layout(width='35%', height='35px'))
                            ButtonSaveNameAllInterpol =  Button(
                                description="Keep and continue with interpolation.",
                                layout=Layout(width='35%', height='35px'))
                            display(ButtonSaveNameAllInterpol)

                            @ButtonSaveNameAllNoInterpol.on_click
                            def ActionSaveNameAllNoInterpol(selfbutton):
                                self.Names = ["Dataset_"+f.split("\\")[-1].split(".")[0] for f in self.FileLocations]

                                for n, f in zip(self.Names, self.FileLocations):
                                    try:
                                        datasetrenamed = pd.read_csv(f, sep = DelimiterType, header=0, names = namae,  usecols = usecol, decimal=DecimalSeparator).abs()
                                        datasetrenamed = datasetrenamed.sort_values("Energy").reset_index(drop=True)
                                        datasetrenamed.to_csv(f"{self.Folders[2]}\\{n}_Renamed.csv", index=False)
                                        datasetrenamed["Energy"] = np.round(datasetrenamed["Energy"], 2)
                                    
                                    except TypeError:
                                        #In case one datasets has a different decimal separator
                                        if DecimalSeparator == ".":
                                            OtherDecimalSeparator = ","
                                        elif DecimalSeparator == ",":
                                            OtherDecimalSeparator = "."

                                        datasetrenamed = pd.read_csv(f, sep = DelimiterType, header=0, names = namae,  usecols = usecol, decimal=OtherDecimalSeparator).abs()
                                        datasetrenamed = datasetrenamed.sort_values("Energy").reset_index(drop=True)
                                        datasetrenamed.to_csv(f"{self.Folders[2]}\\{n}_Renamed.csv", index=False)
                                        datasetrenamed["Energy"] = np.round(datasetrenamed["Energy"], 2)

                                    except pd.errors.ParserError:
                                        print("Are the names of your files not consistent ?")
                                    except Exception as e:
                                        raise e

                                    finally:
                                        try:
                                            C = Dataset(datasetrenamed, f, n, self.Folders[1])
                                            self.ClassList.append(C)
                                            C.pickle()

                                        except Exception as e:
                                            print(f"The class could not been instanced for {n}\n")
                                            raise e

                                print("All data files have also been corrected for the negative values of the energy and for the flipping of values.\n")
                                ButtonSaveNameAllNoInterpol.disabled = True
                                ButtonSaveNameAllInterpol.disabled = True

                                for w in self.ListData.children[:-1] + self.TabTreatment.children[:-1] + self.ListTabReduceMethod.children[:-1] + self.ListFit.children[:-1] + self.ListWidgetsPlot.children[:-1] + self.ListLogbook.children[:-1] :
                                    if w.disabled == True:
                                        w.disabled = False

                                #Does not update automatically sadly
                                self.ListData.children[0].options = self.ClassList
                                self.ListGlobalShift.children[0].options = self.ClassList
                                self.ListCorrectionGas.children[0].options = self.ClassList
                                self.ListCorrectionMem.children[0].options = self.ClassList
                                self.ListMergeEnergies.children[0].options = self.ClassList
                                self.ListTabReduceMethod.children[1].options = self.ClassList
                                self.ListTabReduceMethod.children[2].options = self.ClassList
                                self.ListDeglitching.children[0].options = self.ClassList
                                self.ListFit.children[0].options = self.ClassList
                                self.ListWidgetsPlot.children[0].options = self.ClassList
                                self.ListErrors.children[0].options = self.ClassList
                                self.ListLCF.children[1].options =  self.ClassList
                                self.ListLCF.children[2].options = self.ClassList

                            def Interpolate(StepValue, InterpolBool):
                                """We interpolate the data between the minimum and maximum energy point common to all the datasets with the given step""" 
    
                                if InterpolBool:
                                    self.Names = ["Dataset_"+f.split("\\")[-1].split(".")[0] for f in self.FileLocations]
                                    Emin, Emax = [], []

                                    #Initialize the class Dataset for each file given in entry
                                    for n, f in zip(self.Names, self.FileLocations):
                                        try:
                                            datasetrenamed = pd.read_csv(f, sep = DelimiterType, header=0, names = namae,  usecols = usecol, decimal=DecimalSeparator)
                                            datasetrenamed = datasetrenamed.abs()
                                            datasetrenamed = datasetrenamed.sort_values("Energy").reset_index(drop=True)
                                            datasetrenamed.to_csv(f"{self.Folders[2]}\\{n}_Renamed.csv", index=False)
                                            datasetrenamed["Energy"] = np.round(datasetrenamed["Energy"], 2)
                                        
                                        except TypeError:
                                            #In case one datasets has a different decimal separator
                                            if DecimalSeparator == ".":
                                                OtherDecimalSeparator = ","
                                            elif DecimalSeparator == ",":
                                                OtherDecimalSeparator = "."

                                            datasetrenamed = pd.read_csv(f, sep = DelimiterType, header=0, names = namae,  usecols = usecol, decimal=OtherDecimalSeparator)
                                            datasetrenamed = datasetrenamed.abs()
                                            datasetrenamed = datasetrenamed.sort_values("Energy").reset_index(drop=True)
                                            datasetrenamed.to_csv(f"{self.Folders[2]}\\{n}_Renamed.csv", index=False)
                                            datasetrenamed["Energy"] = np.round(datasetrenamed["Energy"], 2)

                                        except pd.errors.ParserError:
                                            print("Are the names of your files not consistent ?")
                                        except Exception as e:
                                            raise e

                                        finally:
                                            #Store all min and max Energy values
                                            Emin.append(min(datasetrenamed["Energy"].values))
                                            Emax.append(max(datasetrenamed["Energy"].values))

                                            #Append the datasets in ClassList
                                            try:

                                                C = Dataset(datasetrenamed, f, n, self.Folders[1])
                                                self.ClassList.append(C)
                                                C.pickle()

                                            except Exception as e:
                                                print(f"The class could not been instanced for {n}\n")
                                                raise e

                                    #Create a new, common, energy column
                                    self.InterpolStep = StepValue
                                    self.NewEnergyColumn = np.round(np.arange(np.max(Emin), np.min(Emax), StepValue), 2)

                                    """Interpolation happens here"""
                                    try:
                                        # Iterate over all the datasets, we drop the duplicate value that could mess up the splines computation
                                        for C in self.ClassList:
                                            self.UsedDfInit = getattr(C, "df").drop_duplicates('Energy')
                                            x = self.UsedDfInit["Energy"]

                                            InterpolatedDf = pd.DataFrame({
                                                "Energy" : self.NewEnergyColumn
                                                })

                                            # Iterate over all the columns
                                            for col in self.UsedDfInit.columns[self.UsedDfInit.columns != "Energy"]:
                                                y = self.UsedDfInit[col].values
                                                tck = interpolate.splrep(x, y, s = 0)
                                                ynew = interpolate.splev(self.NewEnergyColumn, tck)
                                                InterpolatedDf[col] = ynew

                                            setattr(C, "df", InterpolatedDf)
                                            C.pickle()

                                    except Exception as e:
                                        raise e

                                    print("All data files have also been corrected for the negative values of the energy and for the flipping of values.\n")
                                    ButtonSaveNameAllNoInterpol.disabled = True
                                    ButtonSaveNameAllInterpol.disabled = True

                                    self.ListInterpol.children[0].disabled = True
                                    self.ListInterpol.children[1].disabled = True

                                    for w in self.ListData.children[:-1] + self.TabTreatment.children[:-1] + self.ListTabReduceMethod.children[:-1] + self.ListFit.children[:-1] + self.ListWidgetsPlot.children[:-1] + self.ListLogbook.children[:-1] :
                                        if w.disabled == True:
                                            w.disabled = False

                                    #Does not update automatically sadly
                                    self.ListData.children[0].options = self.ClassList
                                    self.ListGlobalShift.children[0].options = self.ClassList
                                    self.ListCorrectionGas.children[0].options = self.ClassList
                                    self.ListCorrectionMem.children[0].options = self.ClassList
                                    self.ListMergeEnergies.children[0].options = self.ClassList
                                    self.ListTabReduceMethod.children[1].options = self.ClassList
                                    self.ListTabReduceMethod.children[2].options = self.ClassList
                                    self.ListDeglitching.children[0].options = self.ClassList
                                    self.ListFit.children[0].options = self.ClassList
                                    self.ListWidgetsPlot.children[0].options = self.ClassList
                                    self.ListErrors.children[0].options = self.ClassList
                                    self.ListLCF.children[1].options = self.ClassList
                                    self.ListLCF.children[2].options = self.ClassList

                                    # Change displayed energy range selection in case the shifts are important
                                    self.NewEnergyColumn = np.round(np.linspace(self.NewEnergyColumn[0]-20, self.NewEnergyColumn[-1]+20, int(((self.NewEnergyColumn[-1]+20) - (self.NewEnergyColumn[0]-20))/self.InterpolStep + 1)), 2)

                                    for w in [self.ListReduceLSF.children[1], self.ListReduceChebyshev.children[1], self.ListReducePolynoms.children[1], self.ListReduceDerivative.children[1], self.ListModel.children[2]]:
                                        w.min = self.NewEnergyColumn[0]
                                        w.value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]]
                                        w.max = self.NewEnergyColumn[-1]
                                        w.step = self.InterpolStep

                                else:
                                    print("Window cleared")

                            @ButtonSaveNameAllInterpol.on_click
                            def ActionSaveNameAllInterpol(selfbutton):

                                self.ListInterpol = interactive(Interpolate,
                                    StepValue = widgets.FloatSlider(
                                        value=0.05,
                                        min=0.01,
                                        max=0.5,
                                        step=0.01,
                                        description='Step:',
                                        disabled=False,
                                        continuous_update=False,
                                        orientation='horizontal',
                                        readout=True,
                                        readout_format='.2f',
                                        style = {'description_width': 'initial'}),
                                    InterpolBool = widgets.Checkbox(
                                        value=False,
                                        description='Fix step',
                                        disabled=False,
                                        style = {'description_width': 'initial'}))
                                self.LittleTabInterpol=widgets.VBox([widgets.HBox(self.ListInterpol.children[:2]), self.ListInterpol.children[-1]])
                                display(self.LittleTabInterpol)                        
                       
                        except KeyError:
                            print("At least one column must be named \"Energy\"")
                    else:
                        print("Rename all columns before.")

            try:
                if not Marker:
                    df = pd.read_csv(self.FileLocations[0], sep = DelimiterType, decimal=DecimalSeparator).abs()

                if Marker:
                    #The file needs to be rewriten
                    #Open all the files individually and saves its content in a variable
                    for file in self.FileLocations:
                        with open(file,"r") as f:
                            lines = f.readlines()

                        #assign new name to future file
                        CompleteName = file.split(".txt")[0] + "~.dat"
                        with open(CompleteName,"w") as g:
                            #Save the content between the markers
                            for row in lines:
                                if str(InitialMarker)+"\n" in row:
                                    inizio=lines.index(row)

                                if str(FinalMarker)+"\n" in row:
                                    fine=lines.index(row)

                            for j in np.arange(inizio+1, fine):
                                g.write(lines[j])

                    self.FileLocations = sorted(glob.glob(self.Folders[0]+"\\*.dat"))
                    df = pd.read_csv(self.FileLocations[0], sep = DelimiterType, header = None, decimal=DecimalSeparator).abs()
                
                display(df.head())

                nbcolumns = len(df.iloc[0,:])
                if nbcolumns == 4:
                    self.newnames = ['Energy', 'Is', 'I0', '\u03BC']
                elif nbcolumns == 2:
                    self.newnames = ['Energy', '\u03BC']
                elif nbcolumns == 3:
                    self.newnames = ['Energy', "Reference", '\u03BC']
                elif nbcolumns == 5:
                    self.newnames = ['Energy', 'Is', 'I0', '\u03BC', 'Reference']
                elif nbcolumns == 8:
                    self.newnames = ['Energy', 'Is', 'I0', '\u03BC', None, None, None, None]
                else:
                    self.newnames =  [None] * nbcolumns

                ListWorkBool = interactive(Renaming,
                    NbColumns = widgets.Dropdown(
                        options=list(range(nbcolumns)),
                        value=0,
                        description='Column:',
                        disabled=False,
                        style = {'description_width': 'initial'}),
                    NewName = widgets.Dropdown(
                        options=[("Select a value", "select"), ("Energy", "Energy"), ("Is", "Is"), ("I0", "I0"), ("\u03BC", "\u03BC"), ("Reference", "Reference"), ("Not used", "notused"), ("User error", "UserError")],
                        value = "select",
                        description="New name for this column:",
                        disabled=False,
                        style = {'description_width': 'initial'}))
                LittleTabInit=widgets.VBox([widgets.HBox(ListWorkBool.children[:2]), ListWorkBool.children[-1]])
                display(LittleTabInit)
            
            except IndexError:
                print("Empty folder")

            except (TypeError, pd.errors.EmptyDataError, pd.errors.ParserError, UnboundLocalError):
                print("Wrong datatype/delimiter/marker ! This may also be due to the use of colon as the decimal separator in your data, refer to ReadMe.")

            except Exception as e:
                raise e


    #Visualization interactive function
    def PrintData(self, Spec, PrintedDf, ShowBool):
        """Displays the pandas.DataFrame associated to each dataset, there are currently 4 different possibilities:
            _ df : Original data
            _ ShiftedDf : Is one shifts the energy 
            _ ReducedDf : If one applies some background reduction or normalization method 
            _ ReducedDfSplines : If one applied the specific Splines background reduction and normalization method.
        Each data frame is automatically saved as a .csv file after creation."""

        if not ShowBool:
            print("Window cleared")
            clear_output(True)

        elif ShowBool:
            UsedDf = getattr(Spec, PrintedDf)
            if len(UsedDf.columns)==0:
                 print(f"This class does not have the {PrintedDf} dataframe associated yet.")
            else:
                try:
                    display(UsedDf)
                except AttributeError:
                    print(f"Wrong dataset and column combination !")


    #Treatment global interactive function
    def TreatData(self, method, PlotBool):
        if method == "RelativeShift" and PlotBool:
            display(self.WidgetListRelativeShift)
        if method == "GlobalShift" and PlotBool:
            display(self.WidgetListGlobalShift)
        if method == "Gas" and PlotBool:
            display(self.WidgetListCorrectionGas)
        if method == "Membrane" and PlotBool:
            display(self.WidgetListCorrectionMem)
        if method == "Deglitching" and PlotBool:
            display(self.WidgetListDeglitching)
        if method == "Merge" and PlotBool:
            display(self.WidgetMergeEnergies)
        if method == "Errors" and PlotBool:
            display(self.WidgetListErrors)
        if method == "LCF" and PlotBool:
            display(self.WidgetListLCF)
        if not PlotBool:
            print("Window cleared")
            clear_output(True)
            plt.close()

    #Treatment interactive sub-functions
    def RelativeEnergyShift(self, df, x, y):
        """Allows one to shift each Dataset by a certain amount k equal to an integer times the step used for the definition of the x-axis"""

        try :
            UsedDf = getattr(self.ClassList[0], df)
            UsedDf[x]
            UsedDf[y]

            @interact(
                Spec = widgets.Dropdown(
                    options = self.ClassList,
                    description = 'Ref spec :',
                    disabled=False,
                    style = {'description_width': 'initial'}),
                Zoom = widgets.IntRangeSlider(
                    value=[len(UsedDf[x])/3, 2*len(UsedDf[x])/3],
                    min=0,
                    max=len(UsedDf[x]) - 1,
                    step=1,
                    description='Zoom (indices):',
                    disabled=False,
                    continuous_update=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='d',
                    style = {'description_width': 'initial'},
                    layout = Layout(width='50%', height='40px')),
                RefDatasetCursor = widgets.FloatSlider(
                    value = len(UsedDf[x])/2,
                    min = 0,
                    max = len(UsedDf[x]) -1,
                    step = 1,
                    description='Cursor:',
                    orientation='horizontal',
                    continuous_update=False,
                    readout=True,
                    readout_format='d',
                    disabled=False,
                    style = {'description_width': 'initial'},
                    layout = Layout(width='50%', height='40px')),)
            def SetRefDataset(Spec, Zoom, RefDatasetCursor):
                try:
                    self.RefDataset = self.ClassList.index(Spec)

                    plt.close()
                    i, j = Zoom
                    
                    UsedDf = getattr(self.ClassList[self.RefDataset], df)

                    fig,ax = plt.subplots(1, figsize = (16, 8))
                    ax.set_xlabel('Energy')
                    ax.set_ylabel('NEXAFS')
                    ax.set_title(f'Reference Dataset : {self.ClassList[self.RefDataset].Name}')
                    ax.tick_params(direction='in',labelsize=15, width=2)

                    ax.plot(UsedDf[x][i:j+1], UsedDf[y][i:j+1], label='Reference Dataset')

                    ax.axvline(UsedDf[x][i], ls = '--', label = "Left zoom")
                    ax.axvline(UsedDf[x][j], ls = '--', label = "Right zoom")
                    ax.axvline(UsedDf[x][RefDatasetCursor], ls = '--', color='r', label = f"Cursor for Reference Dataset")
                    ax.legend()

                    #Initialize list
                    self.Shifts = [RefDatasetCursor for i in range(len(self.ClassList))]

                    ListMinusRefDataset = self.ClassList.copy()
                    ListMinusRefDataset.remove(Spec)

                    @interact(
                        CurrentDataset = widgets.Dropdown(
                            options = ListMinusRefDataset,
                            description = 'Spec to shift:',
                            disabled=False,
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')),
                        ZoomBis = widgets.IntRangeSlider(
                            value=[len(UsedDf[x])/3, 2*len(UsedDf[x])/3],
                            min=0,
                            max=len(UsedDf[x]) - 1,
                            step=1,
                            description='Zoom (indices):',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='d',
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')),
                        Cursor = widgets.FloatSlider(
                            value = len(UsedDf[x])/2,
                            min = 0,
                            max = len(UsedDf[x]) -1,
                            step=1,
                            description='Cursor:',
                            orientation='horizontal',
                            continuous_update=False,
                            readout=True,
                            readout_format='d',
                            disabled=False,
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')))
                    def ShowArea(CurrentDataset, ZoomBis, Cursor):
                        """Compute area and compare by means of LSM"""
                        try:
                            SpecNb = self.ClassList.index(CurrentDataset)

                            i2, j2 = ZoomBis
                            
                            UsedDf = getattr(self.ClassList[SpecNb], df)

                            fig,ax = plt.subplots(1, figsize = (16, 8))
                            ax.set_xlabel('Energy')
                            ax.set_ylabel('NEXAFS')
                            ax.set_title(f'{self.ClassList[SpecNb].Name}')
                            ax.tick_params(direction='in',labelsize=15,width=2)

                            ax.plot(UsedDf[x][i2:j2+1], UsedDf[y][i2:j2+1], label='Data')

                            ax.axvline(UsedDf[x][Cursor], ls = '--', label = f"Cursor for {self.ClassList[SpecNb].Name}")
                            ax.axvline(UsedDf[x][RefDatasetCursor], ls = '--', color='r', label = f"Cursor for Reference Dataset")
                            ax.legend()

                            ButtonFixShift = widgets.Button(
                                description="Fix shift.",
                                layout=Layout(width='25%', height='35px'))
                            ButtonApplyAllShifts = widgets.Button(
                                description="Apply all the shifts.",
                                layout=Layout(width='25%', height='35px'))
                            display(widgets.HBox((ButtonFixShift, ButtonApplyAllShifts)))

                            @ButtonFixShift.on_click
                            def FixShift(selfbutton):
                                "Fixes the shift"
                                self.Shifts[SpecNb] = Cursor
                                print(f"Shift fixed for Dataset number {CurrentDataset.Name}.\n")
                                print(f"This list contains the currently stored values for the cursor indexes.\n")
                                for x in self.Shifts:
                                    print(x, end=', ')
                                print("\n")

                            @ButtonApplyAllShifts.on_click
                            def ApplyCorrection(selfbutton):
                                "Apply shifts correction"
                                #Keep the same step 
                                Step = self.InterpolStep
                                EShifts = [np.round((self.Shifts[self.RefDataset] - s)* Step, 2)  for s in self.Shifts]
                                print("The shifts are the following, in eV:")
                                print(EShifts)

                                for C, s, name in zip(self.ClassList, EShifts, self.Names):
                                    UsedDf = getattr(C, df)
                                    ShiftDf = UsedDf.copy()
                                    ShiftDf[x] = np.round(UsedDf[x]+s, 2)
                                    setattr(C, "ShiftedDf", ShiftDf)

                                    #Save work
                                    ShiftDf.to_csv(f"{self.Folders[2]}\\{C.Name}_Shifted.csv", index=False)
                                    C.pickle()
                                print("Shifts well applied and saved in a new df ShiftedDf")

                        except (AttributeError, KeyError):
                            plt.close()
                            print(f"Wrong dataset and column combination !")

                except (AttributeError, KeyError):
                    plt.close()
                    print(f"Wrong dataset and column combination !")
        
        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
 
    def GlobalEnergyShift(self, SpecNumber, df, x, y, Shift):

        if SpecNumber:
            try:
                fig, axs = plt.subplots(2, figsize = (16, 11))

                axs[0].set_title('Selected datasets before the shift')
                axs[0].set_xlabel('Energy')
                axs[0].set_ylabel('NEXAFS intensity')
                
                axs[1].set_title('Selected datasets after the shift')
                axs[1].set_xlabel('Energy')
                axs[1].set_ylabel('NEXAFS intensity')

                for j, C in enumerate(SpecNumber):
                    UsedDf = getattr(C, df)

                    #Plot before correction
                    axs[0].plot(UsedDf[x], UsedDf[y])

                    #Plot after correction
                    axs[1].plot(UsedDf[x]+Shift, UsedDf[y], label = C.Name)

                lines, labels = [], []
                for ax in axs:
                    axLine, axLabel = ax.get_legend_handles_labels()
                    lines.extend(axLine)
                    labels.extend(axLabel)

                fig.tight_layout()

                fig.legend(lines,
                           labels,
                            loc='lower center',
                            borderaxespad=0.1,
                            fancybox=True,
                            shadow=True,
                            ncol=5)
                plt.subplots_adjust(bottom=0.15)
                plt.show()

                ButtonGlobalShift = Button(
                    description="Apply global shift",
                    layout=Layout(width='25%', height='35px'))
                display(ButtonGlobalShift)

                @ButtonGlobalShift.on_click
                def ActionButtonGlobalShift(selfbutton):
                    "Apply shifts correction"
                    for j, C in enumerate(SpecNumber):
                        UsedDf = getattr(C, df)
                        ShiftDf = UsedDf.copy()
                        ShiftDf[x] += Shift
                        setattr(C, "ShiftedDf", ShiftDf)
                        #Save work
                        ShiftDf.to_csv(f"{self.Folders[2]}\\{C.Name}_Shifted.csv", index=False)
                        C.pickle()
                    print("Shifts well applied and saved in a new df ShiftedDf")

            except (AttributeError, KeyError):
                clear_output(True)
                plt.close()
                if y =="value":
                    print("Please select a column.")
                else:
                    print(f"Wrong dataset and column combination !")

        else:
            clear_output(True)
            plt.close()
            print("You need to select at least one dataset !")

    def CorrectionGas(self, SpecNumber, df, x, y, Gas, d, p):
        """This function computes the absorbance correction that need to be applied due to the presence of gas in the cell.
        d is the width of the membrane and p the pressure of the gas.
        Each gas may be imput as a dictionnary and the sum of the percentage of each gas must be equal to 100."""
        elements, per = [], []

        try:
            T = [int(C.LogbookEntry["Temp (K)"]) for C in SpecNumber]
            print("The color is function of the temperature for each Dataset.")
        except:
            print("No valid Logbook entry for the temperature found as [Temp (K)], the T for each Dataset will be set to RT.\nPlease refer to ReadMe.\n")
            T =  273.15*np.ones(len(SpecNumber))

        try:
            for j, C in enumerate(SpecNumber):
                UsedDf = getattr(C, df)
                UsedDf[x]
                UsedDf[y]
            #Make tuple of dict
            GasList = [i.replace("{","").replace("}","") for i in Gas.split("},")]
            GasDict = [dict((k.split(":")[0].strip(" ").strip("\""), int(k.split(":")[1])) for k in e.split(",")) for e in GasList]

            #Make sure that the gazes are well defined
            for g in GasDict:
                print(g)
                try:
                    if g["%"] <100 and g["%"]>0:
                        "Good percentage"
                except (KeyError, TypeError):
                    return "You need to include a valid percentage for"+str(g)+". Please refer to ReadMe."
                
                if len(g)>1:
                    per.append(g["%"]/100)
                    del g["%"]
                    if bool(g):
                        elements.append(g)
                else:   
                    return "You need to include at least one gas and its stoiechiometry. Please refer to ReadMe."

            if np.sum(per) != 1.0:
                raise ValueError("The sum of the percentage of the different gazes is not equal to 1! Please refer to ReadMe.")

            #Retrieve the stochiometric number for each atom per gas
            atom = [v  for e in elements for k,v in e.items()]
            NbAtoms = [len(e) for e in elements]

            #Variables used
            kb=(1.38064852)*10**(-23)
            #radius of atom classical approach
            r0=(2.8179)*10**(-15)
            T=np.array(T)
            #Number of atoms per unit volume in the slab
            n=np.array(p/(kb*T))

            #Name of the files needed in order of the gazes
            nomi = [str(k)+".nff" for e in elements for k, v in e.items()]
            labels = [str(k) for e in elements for k, v in e.items()]

            #Store lambdas, energies and f2, for all the gazes, does not depend on their stochio or %
            energies, lambdas, f2_original = [], [], []
            for file in nomi:
                Reference=np.loadtxt(str(self.PathElements)+file, skiprows =1)
                energies.append(Reference[:,0])
                lambdas.append((10**(-9))*(1236)/Reference[:,0])
                f2_original.append(np.transpose(Reference[:,2]))

            #Compute interpolated values for each Spectra
            for j, C in enumerate(SpecNumber):
                UsedDf = getattr(C, df)
                energy = UsedDf[x]

                #Real lambda values
                RealL = ((10**(-9))*(1236)/energy)

                f2 =[]
                #Interpolate for new f2 values, for all the gases, does not depend on their stochio or %
                for f, e in zip(f2_original, energies):
                    tck=interpolate.splrep(e, f, s=0)
                    f2int=interpolate.splev(energy, tck, der=0)
                    f2.append(np.transpose(f2int))

            #Plotting
            fig,axs=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))

            #Plot each scattering factor on the instrument's energy range
            axs[0].set_title('Gas Scattering Factor')
            for f in f2:
                axs[0].plot(energy, f)
            axs[0].set_xlabel('Energy')
            axs[0].set_ylabel('f2')
            axs[0].legend(labels)
            cmap = matplotlib.cm.get_cmap('Spectral')

            TotalTransmittance = []
            for unitvolume, t in zip(n, T):
                Tr = []
                count = 0 
                for pour, nb in zip(per, NbAtoms):
                    tg = np.ones(len(RealL))
                    for i in range(nb):
                        sto = atom[count +i]
                        tg = tg * np.array([np.exp(-2*sto *unitvolume*r0*RealL[j]*f2[count+i][j]*d) for j in range(len(RealL))])
                    Tr.append(pour * tg)
                    count += nb
                TotalTransmittance.append(sum(Tr))
                axs[1].plot(energy, sum(Tr), label = f"Total transmittance at T =  {t} K".format(t), color=( t/max(T), 0, (max(T)-t)/max(T)))

            # Put a legend below current axis
            axs[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=4);

            axs[1].set_title('Gas Transmittance')    
            axs[1].set_xlabel('Energy')
            axs[1].set_ylabel('Transmittance')
            axs[1].yaxis.set_label_position("right")
            axs[1].yaxis.tick_right()
            axs[1].axvline(x=np.min(energy),color='black',linestyle='--')
            axs[1].axvline(x=np.max(energy),color='black',linestyle='--')

            for j, C in enumerate(SpecNumber):
                UsedDf = getattr(C, df)
                UsedDf["GasTransmittance"] = TotalTransmittance[j]
                UsedDf["GasCorrected"] = UsedDf[y].values / UsedDf["GasTransmittance"].values
                UsedDf.to_csv(f"{self.Folders[2]}\\{C.Name}_{df}_GasCorrected.csv", index=False)
                C.pickle()

            plt.show()

        except (AttributeError, KeyError):
            clear_output(True)
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except ValueError:
            clear_output(True)
            plt.close()
            print("Gases not well defined. Please refer to ReadMe. Please mind as well that all the datasets must be of same length !")
        except UnboundLocalError:
            clear_output(True)
            plt.close()
            print("You need to select at least one class !")

    def CorrectionMem(self, SpecNumber, df, x, y, ApplyAll):
        """Apply the method of correction to the membrane, does not depend on the temperature, membrane composition fixed.""" 

        try:
            plt.close()
            fig,ax=plt.subplots(figsize=(16, 6))
            ax.tick_params(direction='in',labelsize=15,width=2)
            ax.set_xlabel('Energy')
            ax.set_ylabel('Transmittance')
            ax.set_xlim(0,1000)
            ax.set_title('Membrane Scattering Factor')

            TM=np.loadtxt(self.PathElements+"membrane.txt")

            #New interpolation
            energyMem=TM[:,0]
            mem=TM[:,1]
            tck=interpolate.splrep(energyMem, mem, s=0)

            if SpecNumber:
                ax.plot(energyMem, mem)
            
                for j, C in enumerate(SpecNumber):
                    UsedDf = getattr(C, df)
                    energy = UsedDf[x]

                    f2int=interpolate.splev(energy, tck, der=0)

                    UsedDf["MembraneTransmittance"] = f2int
                    UsedDf["MembraneCorrected"] = UsedDf["MembraneTransmittance"] * UsedDf[y]
                    print(f"Membrane correction applied to {C.Name}")

                    ax.plot(energy, f2int)
                    ax.axvline(x=np.min(energy), color='black',linestyle='--')
                    ax.axvline(x=np.max(energy), color='black',linestyle='--')
                plt.show()

            else:
                plt.close()
                print("Please select at least one dataset.")
            
            if ApplyAll:
                for j, C in enumerate(SpecNumber):
                    try:
                        UsedDf = getattr(C, df)
                        UsedDf["MembraneCorrected"] = UsedDf["MembraneTransmittance"] * UsedDf[y]
                        UsedDf["TotalReducingFactor"] = UsedDf["MembraneTransmittance"] * UsedDf["GasTransmittance"]
                        UsedDf["GasMemCorr"] = UsedDf[y] / UsedDf["TotalReducingFactor"]
                        UsedDf.to_csv(f"{self.Folders[2]}\\{C.Name}_{df}_MembraneGasCorrected.csv", index=False)
                        C.pickle()
                        print(f"Gas & membrane corrections combined for {C.Name}!")

                    except:
                        print("You did not define the gas correction yet.")

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except Exception as e:
            raise e

    def CorrectionDeglitching(self, Spec, df, pts, x, y, tipo):
        """Allows one to delete some to replace glitches in the data by using linear, square or cubic interpolation."""
        try :
            self.UsedDataset = Spec
            self.UsedDfType = df
            UsedDf = getattr(self.UsedDataset, self.UsedDfType)
            UsedDf[y]

            @interact(
                 interval=widgets.IntRangeSlider(
                    value=[len(UsedDf[x])//4,len(UsedDf[x])//2],
                    min=pts,
                    max=len(UsedDf[x]) - 1 - pts,
                    step=1,
                    description='Range (indices):',
                    disabled=False,
                    continuous_update=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='d',
                    style = {'description_width': 'initial'},
                    layout = Layout(width='50%', height='40px')))
            def Deglitch(interval):
                try:
                    plt.close()

                    #Assign values
                    energy = UsedDf[x]
                    Mu = UsedDf[y]
                    v1, v2 = interval

                    #Plot
                    fig,axs=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                    axs[0].set_xlabel('Energy')
                    axs[0].set_ylabel('NEXAFS')
                    axs[0].set_title('Raw Data')
                    axs[0].tick_params(direction='in',labelsize=15,width=2)

                    axs[0].plot(energy, Mu,label='Data')
                    axs[0].plot(energy[v1:v2], Mu[v1:v2],'-o',linewidth = 0.2,label='Selected Region')

                    axs[0].axvline(x=energy[v1],color='black',linestyle='--')
                    axs[0].axvline(x=energy[v2],color='black',linestyle='--')
                    axs[0].legend()

                    axs[1].set_title('Region Zoom')
                    axs[1].set_xlabel('Energy')
                    axs[1].set_ylabel('NEXAFS')
                    axs[1].tick_params(direction='in',labelsize=15,width=2)

                    axs[1].plot(energy[v1:v2],Mu[v1:v2],'o',color='orange')
                    axs[1].plot(energy[v1-pts:v1],Mu[v1-pts:v1],'-o',color='C0')
                    axs[1].plot(energy[v2:v2+pts],Mu[v2:v2+pts],'-o',color='C0')

                    axs[1].yaxis.set_label_position("right")
                    axs[1].yaxis.tick_right()

                    #Interpolate
                    Erange1=energy[v1-pts:v1]
                    Erange2=energy[v2:v2+pts]
                    ITrange1=Mu[v1-pts:v1]
                    ITrange2=Mu[v2:v2+pts]
                    Erange=np.concatenate((Erange1,Erange2),axis=0)
                    ITrange=np.concatenate((ITrange1,ITrange2),axis=0)

                    Enew=energy[v1:v2]
                    f1 = interpolate.interp1d(Erange, ITrange, kind=tipo)
                    ITN=f1(Enew)

                    axs[1].plot(Enew,ITN,'--',color='green',label='New line')
                    axs[1].legend()

                    ButtonDeglitch = widgets.Button(
                        description="Deglich",
                        layout=Layout(width='25%', height='35px'))
                    display(ButtonDeglitch)

                    @ButtonDeglitch.on_click
                    def ActionButtonDeglitch(selfbutton):
                        C = self.UsedDataset
                        UsedDf = getattr(C, df)
                        UsedDf[y][v1:v2] = ITN
                        clear_output(True)
                        C.pickle()
                        print(f"Degliched {C.Name}, Energy Range: [{energy[v1]}, {energy[v2]}] (eV)")
                        Deglitch(interval)
                except ValueError:
                    plt.close()
                    clear_output(True)
                    print("For quadratic and cubic methods, you need to select more than one extra point.")

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")

    def MergeEnergies(self, SpecNumber, df, x, y, Title, MergeBool):
        """The output of this function is an excel like file (.csv) that is saved in the subdirectory data. 
        In this single file, the same column in saved for each dataset on the same energy range to ease the plotting outside this GUI."""
        if MergeBool and len(SpecNumber) >1:
            try:
                #Create a df that spans the entire energy range and check if filename if valid
                self.MergedValues = pd.DataFrame({
                    x : self.NewEnergyColumn
                    })

                self.MergedValues.to_csv(f"{self.Folders[2]}\\{Title}.csv", sep= ";", index=False, header=True)

            except OSError:
                print("Please specify a new name.")

            try:
                #Do the merging
                for j, C in enumerate(SpecNumber):
                    UsedDf = getattr(C, df)
                    yvalues = pd.DataFrame({x : UsedDf[x].values, y: UsedDf[y].values})

                    for v in self.MergedValues[x].values:
                        if v not in yvalues[x].values:
                            yvalues = yvalues.append({x: v}, ignore_index=True).sort_values(by = [x]).reset_index(drop=True)

                    self.MergedValues[str(C.Name) +"_"+str(y)] = yvalues[y]

                    print(f"{j+1} out of {len(SpecNumber)} datasets processed.\n")

                self.MergedValues.to_csv(f"{self.Folders[2]}\\{Title}.csv", sep= ";", index=False, header=True)

                print(f"Datasets merged for {df} and {y}. Available as {Title}.csv in the subfolders.")

            except (AttributeError, KeyError):
                plt.close()
                if y =="value":
                    print("Please select a column.")
                else:
                    print(f"Wrong dataset and column combination !")

            except Exception as e:
                raise e

        elif MergeBool and len(SpecNumber) <2:
            plt.close()
            print("Please select at least two datasets.")

        else:
            plt.close()
            print("Window cleared.")
            clear_output(True)

    def ErrorsExtraction(self, Spec, df, xcol, ycol, nbpts, deg, direction, ComputeBool):
        
        def poly(x, y, deg):
            coef = np.polyfit(x, y, deg)
            #Create the polynomial function from the coefficients
            return np.poly1d(coef)(x)
        
        if ComputeBool:
            try:
                clear_output(True)
                self.UsedDataset, self.UsedDfType = Spec, df
                UsedDf = getattr(self.UsedDataset, self.UsedDfType)
                x = UsedDf[xcol]
                y = UsedDf[ycol]

                if nbpts%2 is 0:
                    n = int(nbpts/2)
                    self.intl = [k-n if k-n > 0 else 0 for k in range(len(x))]
                    self.intr = [k+n if k+n < len(x) else len(x) for k in range(len(x))]

                    #Cut the intervals
                    self.xcut = {f"Int {n}" : x.values[i : j] for i,j,n in zip(self.intl,self.intr, range(len(x)))}
                    self.ycut = {f"Int {n}" : y.values[i : j] for i,j,n in zip(self.intl,self.intr, range(len(x)))}
                    
                elif nbpts%2 is 1 and direction == "left":
                    n = int(nbpts/2)
                    self.intl = [k-n-1 if k-n-1 > 0 else 0 for k in range(len(x))]
                    self.intr = [k+n if k+n < len(x) else len(x) for k in range(len(x))]

                    #Cut the intervals
                    self.xcut = {f"Int {n}" : x.values[i : j] for i,j,n in zip(self.intl,self.intr, range(len(x)))}
                    self.ycut = {f"Int {n}" : y.values[i : j] for i,j,n in zip(self.intl,self.intr, range(len(x)))}
                    
                elif nbpts%2 is 1 and direction == "right":
                    n = int(nbpts/2)
                    self.intl = [k-n if k-n > 0 else 0 for k in range(len(x))]
                    self.intr = [k+n+1 if k+n < len(x) else len(x) for k in range(len(x))]

                    #Cut the intervals
                    self.xcut = {f"Int {n}" : x.values[i : j] for i,j,n in zip(self.ntl,self.intr, range(len(x)))}
                    self.ycut = {f"Int {n}" : y.values[i : j] for i,j,n in zip(self.intl,self.intr, range(len(x)))}

                #Create a dictionnary with all the polynoms
                self.polynoms = {f"Poly {i}" : poly(self.xcut[f"Int {i}"], self.ycut[f"Int {i}"], deg) for i in range(len(x))}
                
                self.errors = pd.DataFrame({
                    "Deviations" : [self.polynoms[f"Poly {i}"] - self.ycut[f"Int {i}"] for i in range(len(x))],
                    "RMS" : [(np.sum((self.polynoms[f"Poly {i}"] - self.ycut[f"Int {i}"])**2)/len(self.ycut[f"Int {i}"]))**(1/2) for i in range(len(x))]
                })

                print("RMS and deviation well determined.")

                plt.close()

                fig, axs=plt.subplots(nrows=1, ncols=2, figsize = (16, 6))
                axs[0].set_xlabel('Energy')
                axs[0].set_ylabel('NEXAFS')
                axs[0].set_title('Data')
                axs[0].plot(x, y, label = "Data")
                axs[0].legend()

                axs[1].set_xlabel('Energy')
                axs[1].set_ylabel('NEXAFS')
                axs[1].set_title('Root Mean Square')
                axs[1].plot(x, self.errors["RMS"], label = "RMS")
                axs[1].legend()

                try:    
                    UsedDf["Deviations"] = self.errors["Deviations"]
                    UsedDf["RMS"] = self.errors["RMS"]
                except:
                    setattr(self.UsedDataset, self.UsedDfType, pd.concat([UsedDf, self.errors], axis=1, sort=False))

                self.UsedDataset.pickle()
                display(getattr(self.UsedDataset, self.UsedDfType))

            except (AttributeError, KeyError):
                plt.close()
                if ycol =="value":
                    print("Please select a column.")
                else:
                    print(f"Wrong dataset and column combination !")
                
            except Exception as e:
                raise e

        else:
            plt.close()
            print("Window cleared.")
            clear_output(True)

    def LCF(self, RefSpectra, SpecNumber, Spec, dftype, x, y, LCFBool):
        if LCFBool and len(RefSpectra)>1:

            #Check if good df and y
            try:
                self.UsedDfLCF = getattr(Spec, dftype).copy()
                self.RefNames = [f.split("\\")[-1].split(".")[0] for f in RefSpectra]

                def AlignRefAndSpec(**kwargs):
                    try:
                        try :
                            v1 = int(np.where(self.UsedDfLCF[x] == self.EnergyWidget[0].value[0])[0])
                        except TypeError:
                            v1 = 0

                        try:
                            v2 = int(np.where(self.UsedDfLCF[x] == self.EnergyWidget[0].value[1])[0])
                        except TypeError:
                            v2 = len(self.UsedDfLCF)-1

                        Shifts = [c.value for c in self.ShiftWidgets]
                        Factors = [c.value for c in self.IntFactorWidgets]
                        
                        self.UsedDfLCF = getattr(Spec, dftype)[v1 : v2].copy()
                        EminSpec = self.UsedDfLCF[x].values[0]
                        EmaxSpec = self.UsedDfLCF[x].values[-1]
                        
                        #Import the references
                        self.RefDf = [pd.read_csv(f) for f in RefSpectra]
                        
                        # Add Shifts and factors
                        for df, s, a in zip(self.RefDf, Shifts, Factors):
                            df[x] += s
                            df["mu"] = df["mu"]*a
                        
                        EminRef = min([min(df[x]) for df in self.RefDf])
                        EmaxRef = max([max(df[x]) for df in self.RefDf])
                                        
                        #Check if energy range is consistent with those in the literature,
                        GoodRangeRef = [any((df[x] >= EminSpec) & (df[x] <= EmaxSpec)) for df in self.RefDf]
                        
                        GoodRangeSpec = all((self.UsedDfLCF[x] >= EminRef) & (self.UsedDfLCF[x] <= EmaxRef))
                                            
                        #New reference df on different energy range
                        self.RedDfSpectrumRange = [df.loc[(df[x] >= EminSpec) & (df[x] <= EmaxSpec)] for df in self.RefDf]
                        
                        #Plotting
                        fig, ax = plt.subplots(figsize = (16, 6))
                        for data, n in zip(self.RedDfSpectrumRange, self.RefNames):
                            ax.plot(data[x], data["mu"], "--", label = f"Reference {n}")
                        
                        #Change energy range of data
                        ax.plot(self.UsedDfLCF[x], self.UsedDfLCF[y], label = Spec.Name)
                        ax.legend()
                        plt.title("First visualization of the data")
                        plt.show()
                        
                        if all(GoodRangeRef) and GoodRangeSpec:
                            print("The energy ranges between the references and the data match.")
                            @interact(
                                StepValue = widgets.FloatSlider(
                                    value=0.05,
                                    min=0.01,
                                    max=0.5,
                                    step=0.01,
                                    description='Step:',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='horizontal',
                                    readout=True,
                                    readout_format='.2f',
                                    style = {'description_width': 'initial'}),
                                InterpolBool = widgets.Checkbox(
                                    value=False,
                                    description='Fix step',
                                    disabled=False,
                                    style = {'description_width': 'initial'}))
                            def Interpolate(StepValue, InterpolBool):
                                """We interpolate the data between the minimum and maximum energy point common to all the datasets with the given step""" 

                                if InterpolBool:
                                    clear_output(True)
                                    plt.close()
                                    
                                    #Create a new, common, energy column
                                    self.NewEnergyColumn = np.round(np.arange(np.max(EminSpec), np.min(EmaxSpec), StepValue), 2)

                                    # Iterate over all selected spectra
                                    for j, C in enumerate(SpecNumber):
                                        self.UsedDfLCF = getattr(C, dftype)

                                        try :
                                            v1 = int(np.where(self.UsedDfLCF[x] == self.EnergyWidget[0].value[0])[0])
                                        except TypeError:
                                            v1 = 0

                                        try:
                                            v2 = int(np.where(self.UsedDfLCF[x] == self.EnergyWidget[0].value[1])[0])
                                        except TypeError:
                                            v2 = len(self.UsedDfLCF)-1

                                        self.UsedDfLCF = getattr(C, dftype)[v1 : v2].copy()

                                        #Interpolation happens here
                                        try:
                                            # First for the dataset, we drop the duplicate value that could mess up the splines computation
                                            # self.UsedDfLCF = self.UsedDfLCF.drop_duplicates(x)
                                            # Oldx = self.UsedDfLCF[x]                      
                                            # self.InterpolatedUsedDf = pd.DataFrame({
                                            #     x : self.NewEnergyColumn
                                            #     })
                                            
                                            # Iterate over all the columns
                                            # for col in self.UsedDfLCF.columns[self.UsedDfLCF.columns != x]:
                                            #     Oldy = self.UsedDfLCF[col]
                                            #     tck = interpolate.splrep(Oldx, Oldy, s = 0)
                                            #     ynew = interpolate.splev(self.NewEnergyColumn, tck)
                                            #     self.InterpolatedUsedDf[col] = ynew
                                                                            
                                            # Now for the references
                                            self.RefSpectraInterpolated = []
                                            for df in self.RedDfSpectrumRange:
                                                df = df.drop_duplicates(x)
                                                Oldx = df[x]
                                                Oldy = df["mu"]
                                                tck = interpolate.splrep(Oldx, Oldy, s = 0)
                                                ynew = interpolate.splev(self.NewEnergyColumn, tck)
                                                
                                                InterpolatedRefDf = pd.DataFrame({
                                                    x : self.NewEnergyColumn
                                                    })
                                                InterpolatedRefDf["InterpolatedIt"] = ynew
                                                self.RefSpectraInterpolated.append(InterpolatedRefDf)
                                                
                                            #Plotting
                                            # plt.close()
                                            # fig, ax = plt.subplots(figsize = (16, 6))
                                            # for data, n in zip(self.RefSpectraInterpolated, self.RefNames):
                                            #     ax.plot(data[x], data["InterpolatedIt"], label = n)

                                            # #Change energy range of data
                                            # ax.plot(self.InterpolatedUsedDf[x], self.InterpolatedUsedDf[y], label = C.Name)
                                            # ax.legend()
                                            # plt.title("Interpolated data")
                                            # plt.show()
                                            
                                            #Create model
                                            def RefModel(pars):
                                                #Sum weighted ref
                                                y = np.zeros(len(self.RefSpectraInterpolated[0].values))
                                                
                                                #fig, ax = plt.subplots(figsize = (16, 6))
                                                
                                                #All ref but last one
                                                for df, p, n in zip(self.RefSpectraInterpolated[:-1], pars, self.RefNames[-1]):
                                                    y += df["InterpolatedIt"].values * p
                                                    
                                                    #print(p)
                                                    #ax.plot(df["InterpolatedIt"].values * p, label = n)
                                                
                                                #Last ref
                                                y += self.RefSpectraInterpolated[-1]["InterpolatedIt"].values * (1-np.sum(pars))
                                                
                                                #print(1-np.sum(pars))
                                                #ax.plot(self.RefSpectraInterpolated[-1]["InterpolatedIt"].values * (1-np.sum(pars)), label = self.RefNames[-1])
                                                
                                                #Data
                                                #ax.plot(self.InterpolatedUsedDf["Normalized"].values, label ="Data")
                                                #ax.legend()
                                                        
                                                return np.sum((self.UsedDfLCF["Normalized"].values - y)**2)

                                            #Now we lauch fit
                                            InitialGuess = np.ones(len(self.RefDf)-1)/len(self.RefDf)
                                            Bnds = [(0,1) for i in range(len(self.RefNames)-1)]

                                            LCFResult = optimize.minimize(RefModel, InitialGuess, bounds=Bnds, method='TNC')
                                            setattr(C, "LCFResult", LCFResult)

                                            RefWeights = np.append(LCFResult.x.copy(), 1 - np.sum(LCFResult.x))
                                            setattr(C, "RefWeigths", RefWeights)

                                            #Create DataFrame with all the data resulting from the LCF
                                            LCFDf = pd.DataFrame({
                                                x : self.NewEnergyColumn,
                                                "InterpolatedDatasetAbscisse" : self.UsedDfLCF[y],
                                                })

                                            #Plotting result
                                            fig, ax = plt.subplots(figsize = (16, 6))
                                            for data, n, w in zip(self.RefSpectraInterpolated, self.RefNames, RefWeights):
                                                ax.plot(data[x], data["InterpolatedIt"]*w, "--", label = f"{n} component * {w}")
                                                LCFDf[f"WeighedInterpolatedIt_{n}"] = data["InterpolatedIt"]*w

                                            SumWeightedRef = np.sum([w * df["InterpolatedIt"] for df, w in zip(self.RefSpectraInterpolated, RefWeights)], axis = 0)

                                            LCFDf["SumWeightedRef"] = SumWeightedRef
                                            setattr(C, "LCFDf", LCFDf)

                                            ax.plot(self.NewEnergyColumn, SumWeightedRef, label = "Sum of weighted references.")
                                            ax.plot(self.NewEnergyColumn, self.UsedDfLCF[y], label = C.Name)
                                            ax.legend()
                                            plt.title("LCF Result")
                                            plt.show()

                                            #Print detailed result
                                            print(f"The detail of the fitting for {C.Name} is the following:")
                                            print(LCFResult)
                                            print(f"The weights for the references are {RefWeights}")

                                            RFact = np.sum((self.UsedDfLCF[y]-SumWeightedRef)**2) / np.sum((self.UsedDfLCF[y])**2)
                                            print(f"R-factor :{RFact}")
                                            setattr(C, "RefRFact", RFact)

                                            C.pickle()
                                        
                                        # except ValueError:
                                        #     print("Select at least two references.")
                                        except Exception as e:
                                            raise e

                                    #Final plot of the reference weights
                                    fig, ax = plt.subplots(figsize = (10, 6))

                                    xplot = np.arange(0, len(self.ClassList[:10]), 1)
                                    for j, n in enumerate(self.RefNames):
                                        ax.plot(xplot, [C.RefWeigths[j] for C in self.ClassList[:10]], marker='x', label = f"{n} component")
                                    ax.legend()
                                    ax.set_ylabel('Weight')
                                    ax.set_title('Comparison of weight importance thoughout data series')
                                    ax.set_xticks(xplot)
                                    ax.set_xticklabels([C.Name for C in self.ClassList[:10]], rotation=90, fontsize=14);
                       
                                else:
                                    print("Please select a step for the interpolation.")

                        else:
                            print("The energy ranges between the references and the data do not match.")
                            
                    
                    except Exception as e:
                        raise e 
                    # except (AttributeError, KeyError):
                    #     print(f"Wrong dataset and column combination !")

                    # except(ValueError):
                    #     print("Select at least two refs and one spectrum.")

                # Shift the references
                self.ShiftWidgets = [widgets.FloatText(
                            value = 0,
                            step = 0.01,
                            continuous_update=False,
                            description = f"Shift for {n}",
                            style = {'description_width': 'initial'}) for n in self.RefNames]
                ListShiftWidgets = widgets.HBox(tuple(self.ShiftWidgets))

                #Multiply the reference intensity
                self.IntFactorWidgets = [widgets.FloatText(
                            value = 1,
                            step = 0.01,
                            continuous_update=False,
                            description = f"Intensity Factor for {n}",
                            style = {'description_width': 'initial'}) for n in self.RefNames]
                ListIntFactorWidgets = widgets.HBox(tuple(self.IntFactorWidgets))

                #Select the energy range of interest for the data
                self.EnergyWidget = [widgets.FloatRangeSlider(
                            min=self.NewEnergyColumn[0],
                            value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                            max = self.NewEnergyColumn[-1],
                            step = self.InterpolStep,
                            description='Energy range (eV):',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.2f',
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px'))]
                ListEnergyWidget = widgets.HBox(tuple(self.EnergyWidget))

                AlignRefAndSpecDict = {c.description : c for c in self.EnergyWidget + self.ShiftWidgets + self.IntFactorWidgets}

                ListIn = widgets.VBox([ListEnergyWidget, ListShiftWidgets, ListIntFactorWidgets])
                ListOut = widgets.interactive_output(AlignRefAndSpec, AlignRefAndSpecDict)
                display(ListIn, ListOut)

            except (AttributeError, KeyError):
                print(f"Wrong dataset and column combination !") 
                
            except Exception as e:
                raise e
        else:
            clear_output(True)
            print("Select at least two references, one dataset that will serve to visualise the interpolation, and the list of datasets you would like to process.")


    #Reduction interactive function
    def ReduceData(self, method, UsedClassList, UsedDataset, df, PlotBool):
        """Define the reduction routine to follow depending on the Reduction widget state."""
        try:
            self.UsedClassList = UsedClassList
            self.UsedDataset = UsedDataset
            self.UsedDatasetPosition = UsedClassList.index(UsedDataset)
            clear_output(True)
        
            #Update
            self.ListReduceLSF.children[0].value = "value"
            self.ListReduceChebyshev.children[0].value = "value"
            self.ListReducePolynoms.children[0].value = "value"
            self.ListReduceDerivative.children[0].value = "value"

            try :
                self.UsedDfType = df
                UsedDf = getattr(self.UsedDataset, self.UsedDfType)

            except (AttributeError, KeyError):
                print(f"Wrong dataset and column combination !")

            if method == "lsf" and PlotBool:
                display(self.WidgetListReduceLSF)
            if method == "Chebyshev" and PlotBool:
                display(self.WidgetListReduceChebyshev)
            if method == "Polynoms" and PlotBool:
                display(self.WidgetListReducePolynoms)
            if method == "SingleSpline" and PlotBool:
                display(self.WidgetListReduceSingleSpline)
            if method == "Splines" and PlotBool:
                self.ListReduceDerivative.children[0].disabled = False
                self.ListReduceDerivative.children[1].disabled = False
                display(self.WidgetListReduceDerivative)
            if not PlotBool:
                print("Window cleared")
                plt.close()

        except ValueError:
            clear_output(True)
            print(f"{UsedDataset.Name} is not in the list of datatsets to reduce.")

    #Reduction interactive sub-functions
    def ReduceLSF(self, y, interval, lam, p):
        """Reduce the background following a Least Square Fit method"""

        def baseline_als(y, lam, p, niter=10):
            """Polynomial function defined by sparse"""
            L = len(y)
            D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
            w = np.ones(L)
            for i in range(niter):
                W = sparse.spdiags(w, 0, L, L)
                Z = W + lam * D.dot(D.transpose())
                z = sparse.linalg.spsolve(Z, w*y)
                w = p * (y > z) + (1-p) * (y < z)
            return z

        try:
            number = self.UsedDatasetPosition
            df = self.UsedDfType

            #Retrieve original data
            Mu, Energy, v1, v2 = [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y].values)
                Energy.append(UsedDf["Energy"].values)

                try :
                    v1.append(int(np.where(Energy[j] == interval[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    v2.append(int(np.where(Energy[j] == interval[1])[0]))
                except TypeError:
                    v2.append(len(Energy[j])-1)

            ButtonRemoveBackground = Button(
                description="Remove background for all",
                layout=Layout(width='30%', height='35px'))
            ButtonSaveDataset = Button(
                description="Save background reduced data",
                layout=Layout(width='30%', height='35px'))
            display(widgets.HBox((ButtonRemoveBackground, ButtonSaveDataset)))

            plt.close()

            fig, axs=plt.subplots(nrows=1, ncols=2, figsize = (16, 6))
            axs[0].set_xlabel('Energy')
            axs[0].set_ylabel('NEXAFS')
            axs[0].set_title('Raw Data')
            axs[0].tick_params(direction='in',labelsize=15,width=2)

            #Compute from sliders
            baseline = baseline_als(Mu[number][v1[number]:v2[number]], lam, p*10**(-3), niter=10)
            
            axs[0].plot(Energy[number],Mu[number],label='Data')
            axs[0].plot(Energy[number][v1[number]:v2[number]],Mu[number][v1[number]:v2[number]],'-o',label='Selected Region')
            axs[0].plot(Energy[number][v1[number]:v2[number]],baseline,'--',color='green',label='Bkg')
            axs[0].axvline(x=Energy[number][v1[number]],color='black',linestyle='--')
            axs[0].axvline(x=Energy[number][v2[number]],color='black',linestyle='--')
            axs[0].legend()

            difference = Mu[number][v1[number]:v2[number]] - baseline

            axs[1].set_title('Background Subtrackted')
            axs[1].set_xlabel('Energy')
            axs[1].set_ylabel('NEXAFS')
            axs[1].yaxis.set_label_position("right")
            axs[1].yaxis.tick_right()
            axs[1].tick_params(direction='in',labelsize=15,width=2)
            axs[1].set_xlim(Energy[number][v1[number]], Energy[number][v2[number]])

            axs[1].plot(Energy[number][v1[number]:v2[number]],difference,'-',color='C0')

            print("Channel 1:", v1[number], ";","Energy:", Energy[number][v1[number]])
            print("Channel 2:", v2[number], ";","Energy:", Energy[number][v2[number]])


            @ButtonSaveDataset.on_click
            def ActionSaveDataset(selfbutton):
                #Save single Dataset without background in Class
                C = self.UsedDataset
                IN = Mu[number][v1[number]:v2[number]] / np.trapz(difference, x=Energy[number][v1[number]:v2[number]])
                TempDF = pd.DataFrame()
                TempDF["Energy" ] = Energy[number][v1[number]:v2[number]]
                TempDF["\u03BC"] =  Mu[number][v1[number]:v2[number]]
                TempDF["BackgroundCorrected"] = difference
                TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in difference]
                TempDF["Normalized"] = IN
                print(f"Saved Dataset {C.Name}")
                setattr(C, "ReducedDf", TempDF)
                display(TempDF)
                TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                C.pickle()

            @ButtonRemoveBackground.on_click
            def ActionRemoveBackground(selfbutton):
                #Substract background to the intensity
                clear_output(True)

                fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                ax[0].set_title('Background Subtrackted')
                ax[0].set_xlabel('Energy')
                ax[0].set_ylabel('NEXAFS')
                ax[0].tick_params(direction='in',labelsize=15,width=2)

                ax[1].set_title('Background Subtrackted Shifted')
                ax[1].set_xlabel('Energy')
                ax[1].set_ylabel('NEXAFS')
                ax[1].yaxis.tick_right()
                ax[1].tick_params(direction='in',labelsize=15,width=2)
                ax[1].yaxis.set_label_position("right")

                ITB=[]
                try : 
                    for i in range(len(Mu)):
                        baseline = baseline_als(Mu[i][v1[i]:v2[i]], lam, p*10**(-3), niter=10)
                        ITnew=Mu[i][v1[i]:v2[i]]-baseline
                        ITB.append(ITnew)

                    for i in range(len(ITB)):
                        ax[0].plot(Energy[i][v1[i]:v2[i]],ITB[i])
                        ax[1].plot(Energy[i][v1[i]:v2[i]],ITB[i]+0.1*(i), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);


                except Exception as e:
                    print(e)

                ButtonSave = widgets.Button(
                    description="Save background reduced data",
                    layout=Layout(width='30%', height='35px'))
                ButtonNormalize = widgets.Button(
                    description = 'Normalize for all',
                    layout=Layout(width='30%', height='35px'))
                display(widgets.HBox((ButtonNormalize, ButtonSave))) 

                @ButtonSave.on_click
                def ActionButtonSave(selfbutton):
                    #Save intensity without background 
                    for j, C in enumerate(self.UsedClassList):
                        TempDF = pd.DataFrame()  
                        TempDF = getattr(C, "ReducedDf")
                        TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                        TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                        TempDF["BackgroundCorrected"] = ITB[j]
                        TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in IB[j]]
                        setattr(C, "ReducedDf", TempDF)
                        print(f"Saved Dataset {C.Name}")
                        TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                        C.pickle()

                @ButtonNormalize.on_click
                def ActionButtonNormalize(selfbutton):
                    #Normalize data

                    clear_output(True)
                    area=[]
                    ITN= []
                    for i in range(len(ITB)):
                        areaV=np.trapz(ITB[i], x=Energy[i][v1[i]:v2[i]])
                        area.append(areaV)
                        ITN.append(ITB[i]/area[i])
                                
                    fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                    ax[0].set_title('Background Subtrackted Normalized')
                    ax[0].set_xlabel('Energy')
                    ax[0].set_ylabel('NEXAFS')
                    ax[0].tick_params(direction='in',labelsize=15,width=2)
                    ax[1].set_title('Background Subtrackted Normalized & Shifted')
                    ax[1].set_xlabel('Energy')
                    ax[1].set_ylabel('NEXAFS')
                    ax[1].yaxis.set_label_position("right")
                    ax[1].yaxis.tick_right()
                    ax[1].tick_params(direction='in',labelsize=15,width=2)

                    for i in range(len(ITN)):
                        ax[0].plot(Energy[i][v1[i]:v2[i]],ITN[i])
                        ax[1].plot(Energy[i][v1[i]:v2[i]],ITN[i]+0.1*(i+1), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);


                    ButtonSaveNormalizedData = widgets.Button(
                        description="Save normalized data",
                        layout=Layout(width='30%', height='35px'))
                    display(ButtonSaveNormalizedData)

                    @ButtonSaveNormalizedData.on_click
                    def ActionSaveNormalizedData(selfbutton):
                        #Save normalized data
                        for j, C in enumerate(self.UsedClassList):
                            TempDF = pd.DataFrame()
                            TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                            TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                            TempDF["BackgroundCorrected"] = ITB[j]
                            TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB[j]]
                            TempDF["Normalized"] = ITN[j]
                            setattr(C, "ReducedDf", TempDF)
                            print(f"Saved Dataset {C.Name}")
                            TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                            C.pickle()

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")

        except (ValueError, NameError):
            plt.close()
            print("The selected energy range is wrong.")

    def ReduceChebyshev(self, y, interval, p, n):
        """Reduce the background with ChebYshev polynomails"""

        def Chebyshev( x, y, d, n):
            """Define a chebyshev polynomial using np.polynomial.Chebyshev.fit method"""
            w = (1/y)**n
            p = np.polynomial.Chebyshev.fit(x, y, d, w=w)

            return p(x)
        
        try:
            number = self.UsedDatasetPosition
            df = self.UsedDfType

            #Retrieve original data
            Mu, Energy, v1, v2 = [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y].values)
                Energy.append(UsedDf["Energy"].values)

                try :
                    v1.append(int(np.where(Energy[j] == interval[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    v2.append(int(np.where(Energy[j] == interval[1])[0]))
                except TypeError:
                    v2.append(len(Energy[j])-1)

            plt.close()

            fig,axs=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
            axs[0].set_xlabel('Energy')
            axs[0].set_ylabel('NEXAFS')
            axs[0].set_title('Raw Data')
            axs[0].tick_params(direction='in',labelsize=15,width=2)

            #Compute from sliders
            baseline=Chebyshev(Energy[number][v1[number]:v2[number]],Mu[number][v1[number]:v2[number]], p, n)

            axs[0].plot(Energy[number],Mu[number],label='Data')
            axs[0].plot(Energy[number][v1[number]:v2[number]],Mu[number][v1[number]:v2[number]],'-o',label='Selected Region')
            axs[0].plot(Energy[number][v1[number]:v2[number]],baseline,'--',color='green',label='Bkg')
            axs[0].axvline(x=Energy[number][v1[number]],color='black',linestyle='--')
            axs[0].axvline(x=Energy[number][v2[number]],color='black',linestyle='--')
            axs[0].legend()

            difference = Mu[number][v1[number]:v2[number]] - baseline

            axs[1].set_title('Background Subtrackted')
            axs[1].set_xlabel('Energy')
            axs[1].set_ylabel('NEXAFS')
            axs[1].yaxis.set_label_position("right")
            axs[1].yaxis.tick_right()
            axs[1].tick_params(direction='in',labelsize=15,width=2)
            axs[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])

            axs[1].plot(Energy[number][v1[number]:v2[number]],difference,'-',color='C0')

            print("Channel 1:", v1[number], ";","Energy:",Energy[number][v1[number]])
            print("Channel 2:", v2[number], ";","Energy:",Energy[number][v2[number]])
        
            ButtonRemoveBackground = Button(
                description="Remove background for all",
                layout=Layout(width='30%', height='35px'))
            ButtonSaveDataset = Button(
                description="Save background reduced data",
                layout=Layout(width='30%', height='35px'))
            display(widgets.HBox((ButtonRemoveBackground, ButtonSaveDataset)))

            @ButtonSaveDataset.on_click
            def ActionSaveDataset(selfbutton):
                #Save single Dataset without background in Class
                C = self.UsedDataset
                IN = Mu[number][v1[number]:v2[number]] / np.trapz(difference, x=Energy[number][v1[number]:v2[number]])
                TempDF = pd.DataFrame()
                TempDF["Energy" ] = Energy[number][v1[number]:v2[number]]
                TempDF["\u03BC"] =  Mu[number][v1[number]:v2[number]]
                TempDF["BackgroundCorrected"] = difference
                TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in difference]
                TempDF["Normalized"] = IN
                setattr(C, "ReducedDf", TempDF)
                print(f"Saved Dataset {C.Name}")
                TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                C.pickle()

            @ButtonRemoveBackground.on_click
            def ActionRemoveBackground(selfbutton):
                #Substract background to the intensity
                clear_output(True)

                fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                ax[0].set_title('Background Subtrackted')
                ax[0].set_xlabel('Energy')
                ax[0].set_ylabel('NEXAFS')
                ax[0].tick_params(direction='in',labelsize=15,width=2)
                ax[0].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])

                ax[1].set_title('Background Subtrackted Shifted')
                ax[1].set_xlabel('Energy')
                ax[1].set_ylabel('NEXAFS')
                ax[1].yaxis.tick_right()
                ax[1].tick_params(direction='in',labelsize=15,width=2)
                ax[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                ax[1].yaxis.set_label_position("right")
                #ax.plot(energy[v1:v2],ITN)

                ITB=[]
                try:
                    for i in range(len(Mu)):
                        baseline=Chebyshev(Energy[i][v1[i]:v2[i]],Mu[i][v1[i]:v2[i]], p, n)
                        ITnew=Mu[i][v1[i]:v2[i]]-baseline
                        ITB.append(ITnew)

                    for i in range(len(ITB)):
                        ax[0].plot(Energy[i][v1[i]:v2[i]], ITB[i])
                        ax[1].plot(Energy[i][v1[i]:v2[i]], ITB[i]+0.1*(i), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);
                
                except ValueError:
                    print("The energy range is wrong.")

                ButtonSave = widgets.Button(
                    description="Save background reduced data",
                    layout=Layout(width='30%', height='35px'))
                ButtonNormalize = widgets.Button(
                    description = 'Normalize for all',
                    layout=Layout(width='30%', height='35px'))
                display(widgets.HBox((ButtonNormalize, ButtonSave))) 

                @ButtonSave.on_click
                def ActionButtonSave(selfbutton):
                    #Save intensity without background 
                    for j, C in enumerate(self.UsedClassList):
                        TempDF = pd.DataFrame()
                        TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                        TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                        TempDF["BackgroundCorrected"] = ITB[j]
                        TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB[j]]
                        setattr(C, "ReducedDf", TempDF)
                        print(f"Saved Dataset {C.Name}")
                        TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                        C.pickle()

                @ButtonNormalize.on_click
                def ActionButtonNormalize(selfbutton):
                    #Normalize data

                    clear_output(True)
                    area=[]
                    ITN= []
                    for i in range(len(ITB)):
                        areaV=np.trapz(ITB[i], x=Energy[i][v1[i]:v2[i]])
                        area.append(areaV)
                        ITN.append(ITB[i]/area[i])
                                
                    fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                    ax[0].set_title('Background Subtrackted Normalized')
                    ax[0].set_xlabel('Energy')
                    ax[0].set_ylabel('NEXAFS')
                    ax[0].tick_params(direction='in',labelsize=15,width=2)
                    ax[0].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                    ax[1].set_title('Background Subtrackted Normalized & Shifted')
                    ax[1].set_xlabel('Energy')
                    ax[1].set_ylabel('NEXAFS')
                    ax[1].yaxis.set_label_position("right")
                    ax[1].yaxis.tick_right()
                    ax[1].tick_params(direction='in',labelsize=15,width=2)
                    ax[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])

                    for i in range(len(ITN)):
                        ax[0].plot(Energy[i][v1[i]:v2[i]],ITN[i])
                        ax[1].plot(Energy[i][v1[i]:v2[i]],ITN[i]+0.1*(i+1), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);


                    ButtonSaveNormalizedData = widgets.Button(
                        description="Save normalized data",
                        layout=Layout(width='30%', height='35px'))
                    display(ButtonSaveNormalizedData)
                    
                    @ButtonSaveNormalizedData.on_click
                    def ActionSaveNormalizedData(selfbutton):
                        #Save normalized data
                        for j, C in enumerate(self.UsedClassList):
                            TempDF = pd.DataFrame()
                            TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                            TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                            TempDF["BackgroundCorrected"] = ITB[j]
                            TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB[j]]
                            TempDF["Normalized"] = ITN[j]
                            setattr(C, "ReducedDf", TempDF)
                            print(f"Saved Dataset {C.Name}")
                            TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                            C.pickle()
        
        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except (ValueError, NameError):
            plt.close()
            print("The selected energy range is wrong.")

    def ReducePolynoms(self, y, interval, sL):
        """Reduce the background using a fixed number of points and Polynoms between them"""
        try:
            number = self.UsedDatasetPosition
            df = self.UsedDfType

            #Retrieve original data
            Mu, Energy, v1, v2 = [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y].values)
                Energy.append(UsedDf["Energy"].values)

                try :
                    v1.append(int(np.where(Energy[j] == interval[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    v2.append(int(np.where(Energy[j] == interval[1])[0]))
                except TypeError:
                    v2.append(len(Energy[j])-1)

            plt.close()

            def plotSliders(**selfsliders):
                #Take values from sliders
                positions=[]
                for i in range(sL):
                    positions.append(controls[i].value)
                positions.sort()

                fig, axs=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                axs[0].set_xlabel('Energy')
                axs[0].set_ylabel('NEXAFS')
                axs[0].set_title('Raw Data')
                axs[0].tick_params(direction='in',labelsize=15,width=2)

                axs[0].plot(Energy[number],Mu[number],label='Data')
                axs[0].plot(Energy[number][v1[number]:v2[number]],Mu[number][v1[number]:v2[number]],'-o',label='Selected Region')
                axs[0].axvline(x=Energy[number][v1[number]],color='black',linestyle='--')
                axs[0].axvline(x=Energy[number][v2[number]],color='black',linestyle='--')
                axs[0].set_ylim(np.min(Mu[number])-0.01*np.min(Mu[number]),np.max(Mu[number])+0.01*np.max(Mu[number]))

                energy_int=Energy[number][positions]
                data_int=Mu[number][positions]

                baseline=interpolate.splrep(energy_int, data_int, s=0)
                ITint = interpolate.splev(Energy[number][v1[number]:v2[number]],baseline, der=0)
                axs[0].plot(Energy[number][v1[number]:v2[number]],ITint,'--',color='green',label='Bkg')

                for i in range(sL):
                    axs[0].plot(Energy[number][positions[i]],Mu[number][positions[i]],'o',color='black',markersize=10)
                    axs[0].axvline(x=Energy[number][positions[i]])
                axs[0].legend()
                difference=Mu[number][v1[number]:v2[number]]-ITint

                axs[1].plot(Energy[number][v1[number]:v2[number]],difference)
                axs[1].set_title('Bgk Subtrackted')
                axs[1].set_xlabel('Energy')
                axs[1].set_ylabel('NEXAFS')
                axs[1].yaxis.set_label_position("right")
                axs[1].tick_params(direction='in',labelsize=15,width=2)
                axs[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])

                #################################### BUTTONS ###############################################################################
                ButtonRemoveBackground = Button(
                    description="Remove background for all",
                    layout=Layout(width='30%', height='35px'))
                ButtonSaveDataset = Button(
                    description="Save background reduced data",
                    layout=Layout(width='30%', height='35px'))
                display(widgets.HBox((ButtonRemoveBackground, ButtonSaveDataset)))

                @ButtonSaveDataset.on_click
                def ActionSaveDataset(selfbutton):
                    #Save single Dataset without background in Class
                    C = self.UsedDataset
                    IN = Mu[number][v1[number]:v2[number]] / np.trapz(difference, x=Energy[number][v1[number]:v2[number]])
                    TempDF = pd.DataFrame()
                    TempDF["Energy" ] = Energy[number][v1[number]:v2[number]]
                    TempDF["\u03BC"] =  Mu[number][v1[number]:v2[number]]
                    TempDF["BackgroundCorrected"] = difference
                    TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in difference]
                    TempDF["Normalized"] = IN
                    setattr(C, "ReducedDf", TempDF)
                    print(f"Saved Dataset {C.Name}")
                    C.pickle()
                    TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)

                @ButtonRemoveBackground.on_click
                def ActionRemoveBackground(selfbutton):
                    #Substract background to the intensity
                    ITB=[]
                    for i in range(len(Mu)):
                        baseline=interpolate.splrep(energy_int, data_int, s=0)
                        ITint = interpolate.splev(Energy[i][v1[i]:v2[i]], baseline, der=0)
                        ITnew=Mu[i][v1[i]:v2[i]]-ITint
                        ITB.append(ITnew)

                    clear_output(True)

                    fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                    ax[0].set_title('Background Subtrackted')
                    ax[0].set_xlabel('Energy')
                    ax[0].set_ylabel('NEXAFS')
                    ax[0].tick_params(direction='in',labelsize=15,width=2)
                    ax[0].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])

                    ax[1].set_title('Background Subtrackted Shifted')
                    ax[1].set_xlabel('Energy')
                    ax[1].set_ylabel('NEXAFS')
                    ax[1].yaxis.tick_right()
                    ax[1].tick_params(direction='in',labelsize=15,width=2)
                    ax[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                    ax[1].yaxis.set_label_position("right")

                    for i in range(len(ITB)):
                        ax[0].plot(Energy[i][v1[i]:v2[i]],ITB[i])
                        ax[1].plot(Energy[i][v1[i]:v2[i]],ITB[i]+0.1*(i), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);


                    ButtonSave = widgets.Button(
                        description="Save background reduced data",
                        layout=Layout(width='30%', height='35px'))
                    ButtonNormalize = widgets.Button(
                        description = 'Normalize for all',
                        layout=Layout(width='30%', height='35px'))
                    display(widgets.HBox((ButtonNormalize, ButtonSave))) 

                    @ButtonSave.on_click
                    def ActionButtonSave(selfbutton):
                        #Save intensity without background 
                        for j, C in enumerate(self.UsedClassList):
                            TempDF = pd.DataFrame()
                            TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                            TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                            TempDF["BackgroundCorrected"] = ITB[j]
                            TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB[j]]
                            setattr(C, "ReducedDf", TempDF)
                            print(f"Saved Dataset {C.Name}")
                            C.pickle()
                            TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)

                    @ButtonNormalize.on_click
                    def ActionButtonNormalize(selfbutton):
                        #Normalize data
                        clear_output(True)
                        area=[]
                        ITN= []
                        for i in range(len(ITB)):
                            areaV=np.trapz(ITB[i], x=Energy[i][v1[i]:v2[i]])
                            area.append(areaV)
                            ITN.append(ITB[i]/area[i])
                                    
                        fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                        ax[0].set_title('Background Subtrackted Normalized')
                        ax[0].set_xlabel('Energy')
                        ax[0].set_ylabel('NEXAFS')
                        ax[0].tick_params(direction='in',labelsize=15,width=2)
                        ax[0].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                        ax[1].set_title('Background Subtrackted Normalized & Shifted')
                        ax[1].set_xlabel('Energy')
                        ax[1].set_ylabel('NEXAFS')
                        ax[1].yaxis.set_label_position("right")
                        ax[1].yaxis.tick_right()
                        ax[1].tick_params(direction='in',labelsize=15,width=2)
                        ax[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                        for i in range(len(ITN)):
                            ax[0].plot(Energy[i][v1[i]:v2[i]],ITN[i])
                            ax[1].plot(Energy[i][v1[i]:v2[i]],ITN[i]+0.1*(i+1), label = self.UsedClassList[i].Name)

                        ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);

                        ButtonSaveNormalizedData = widgets.Button(
                            description="Save normalized data",
                            layout=Layout(width='30%', height='35px'))
                        display(ButtonSaveNormalizedData)

                        @ButtonSaveNormalizedData.on_click
                        def ActionSaveNormalizedData(selfbutton):
                            #Save normalized data
                            for j, C in enumerate(self.UsedClassList):
                                TempDF = pd.DataFrame()
                                TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                                TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                                TempDF["BackgroundCorrected"] = ITB[j]
                                TempDF["\u03BC Variance (1/\u03BC)"] =[1/d if d >0 else 0 for d in ITB[j]]
                                TempDF["Normalized"] = ITN[j]
                                setattr(C, "ReducedDf", TempDF)
                                print(f"Saved Dataset {C.Name}")
                                C.pickle()
                                TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)

            #Polynoms 
            controls=[widgets.IntSlider(
                    description=f"P_{i+1}",
                    min=v1[number], 
                    max=v2[number],
                    step=1,
                    orientation= "vertical",
                    continuous_update=False) for i in range (sL)]

            controlsDict = {c.description : c for c in controls}

            uif = widgets.HBox(tuple(controls))
            outf = widgets.interactive_output(plotSliders,controlsDict)
            display(uif, outf)

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except (ValueError, NameError):
            plt.close()
            print("The selected energy range is wrong.")

    def ReduceSingleSpline(self, y, order, interval, Cursor, ParamA, ParamB):

        try:
            number = self.UsedDatasetPosition
            df = self.UsedDfType

            #Retrieve original data
            Mu, Energy, v1, v2, c = [], [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y].values)
                Energy.append(UsedDf["Energy"].values)

                try :
                    v1.append(int(np.where(Energy[j] == interval[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    v2.append(int(np.where(Energy[j] == interval[1])[0]))
                except TypeError:
                    v2.append(len(Energy[j])-1)

                try:
                    c.append(int(np.where(Energy[j] == Cursor)[0]))
                except TypeError:
                    c.append(len(Energy[j])-1)

            if order is "value":
                raise AttributeError("Please select an order.")

            elif order is "Victoreen":
                #make a lsq fit
                self.Vmodel = lmfit.Model(self.Victoreen, prefix='Background_')

                self.x = Energy[number]
                self.y = Mu[number]
                self.resultV = self.Vmodel.fit(Mu[number][v1[number]:v2[number]], x=Energy[number][v1[number]:v2[number]], Background_A=int(ParamA), Background_B=int(ParamB))
                display(self.resultV.params)

                p = self.Victoreen(Energy[number], self.resultV.params["Background_A"].value, self.resultV.params["Background_B"].value)

            elif isinstance(order, int):
                #Find the polynomials coefficients
                coef=np.polyfit(Energy[number][v1[number]:v2[number]], Mu[number][v1[number]:v2[number]], order)

                #Create the polynomial function from the coefficients
                pcall=np.poly1d(coef)
                p = pcall(Energy[number])

            # Substract background
            difference = Mu[number]-p

            # Normalize
            NormalizedData = difference / difference[c[number]]

            ButtonRemoveBackground = Button(
                description="Remove background for all",
                layout=Layout(width='30%', height='35px'))
            ButtonSaveDataset = Button(
                description="Save background reduced data",
                layout=Layout(width='30%', height='35px'))
            display(widgets.HBox((ButtonRemoveBackground, ButtonSaveDataset)))

            plt.close()

            fig, axs=plt.subplots(nrows=1, ncols=2, figsize = (16, 6))
            axs[0].set_xlabel('Energy')
            axs[0].set_ylabel('NEXAFS')
            axs[0].set_title('Raw Data')

            axs[0].plot(Energy[number], Mu[number],label='Data')
            axs[0].plot(Energy[number][v1[number]:v2[number]], Mu[number][v1[number]:v2[number]],'-o',label='Selected Region')
            axs[0].plot(Energy[number], p,'--', color='green',label='Background curve')
            axs[0].axvline(x=Energy[number][v1[number]], color='black',linestyle='--')
            axs[0].axvline(x=Energy[number][v2[number]], color='black',linestyle='--')
            axs[0].axvline(x=Energy[number][c[number]], color='orange',linestyle='--', label = "Cursor for Normalisation")

            axs[0].legend()

            axs[1].set_title('Background subtrackted & normalized curve')
            axs[1].set_xlabel('Energy')
            axs[1].set_ylabel('NEXAFS')
            axs[1].yaxis.set_label_position("right")
            axs[1].yaxis.tick_right()
            axs[1].set_xlim(Energy[number][0], Energy[number][-1])

            axs[1].plot(Energy[number], NormalizedData,'-',color='C0')


            @ButtonSaveDataset.on_click
            def ActionSaveDataset(selfbutton):
                #Save single Dataset without background in Class
                C = self.UsedDataset
                TempDF = pd.DataFrame()
                TempDF["Energy" ] = Energy[number]
                TempDF["\u03BC"] =  Mu[number]
                TempDF["BackgroundCorrected"] = difference
                TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in difference]
                TempDF["Normalized"] = NormalizedData
                print(f"Saved Dataset {C.Name}")
                setattr(C, "ReducedDf", TempDF)
                display(TempDF)
                TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                C.pickle()

            @ButtonRemoveBackground.on_click
            def ActionRemoveBackground(selfbutton):
                #Substract background to the intensity
                clear_output(True)

                fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                ax[0].set_title('Background Subtrackted')
                ax[0].set_xlabel('Energy')
                ax[0].set_ylabel('NEXAFS')

                ax[1].set_title('Background Subtrackted Shifted')
                ax[1].set_xlabel('Energy')
                ax[1].set_ylabel('NEXAFS')
                ax[1].yaxis.tick_right()
                ax[1].yaxis.set_label_position("right")

                ITB=[]
                try :
                    for i in range(len(Mu)):
                        if order is "value":
                            raise AttributeError("Please select an order.")

                        elif order is "Victoreen":
                            #make a lsq fit
                            self.Vmodel = lmfit.Model(self.Victoreen, prefix='Background_')

                            self.x = Energy[i]
                            self.y = Mu[i]
                            self.resultV = self.Vmodel.fit(Mu[i][v1[i]:v2[i]], x=Energy[i][v1[i]:v2[i]], Background_A=int(ParamA), Background_B=int(ParamB))
                            print(f"Parameters for {self.UsedClassList[i].Name}")
                            display(self.resultV.params)
                            print("\n")

                            p = self.Victoreen(Energy[i], self.resultV.params["Background_A"].value, self.resultV.params["Background_B"].value)

                        elif isinstance(order, int):
                            #Find the polynomials coefficients
                            coef=np.polyfit(Energy[i][v1[i]:v2[i]], Mu[i][v1[i]:v2[i]], order)

                            #Create the polynomial function from the coefficients
                            pcall=np.poly1d(coef)
                            p = pcall(Energy[i])

                        ITB.append(Mu[i] - p)

                    for i in range(len(ITB)):
                        ax[0].plot(Energy[i], ITB[i])
                        ax[1].plot(Energy[i], ITB[i]+0.1*(i), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);

                except Exception as e:
                    print(e)

                ButtonSave = widgets.Button(
                    description="Save background reduced data",
                    layout=Layout(width='30%', height='35px'))
                ButtonNormalize = widgets.Button(
                    description = 'Normalize for all',
                    layout=Layout(width='30%', height='35px'))
                display(widgets.HBox((ButtonNormalize, ButtonSave))) 

                @ButtonSave.on_click
                def ActionButtonSave(selfbutton):
                    #Save intensity without background 
                    for j, C in enumerate(self.UsedClassList):
                        TempDF = pd.DataFrame()  
                        TempDF = getattr(C, "ReducedDf")
                        TempDF["Energy" ] = Energy[j][v1[j]:v2[j]]
                        TempDF["\u03BC"] =  Mu[j][v1[j]:v2[j]]
                        TempDF["BackgroundCorrected"] = ITB[j]
                        TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in IB[j]]
                        setattr(C, "ReducedDf", TempDF)
                        print(f"Saved Dataset {C.Name}")
                        TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                        C.pickle()

                @ButtonNormalize.on_click
                def ActionButtonNormalize(selfbutton):
                    #Normalize data
                    clear_output(True)
                    area=[]
                    ITN= []
                    for i in range(len(ITB)):
                        ITN.append(ITB[i] / ITB[i][c[i]])
                                
                    fig,ax=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                    ax[0].set_title('Background Subtrackted Normalized')
                    ax[0].set_xlabel('Energy')
                    ax[0].set_ylabel('NEXAFS')
                    ax[0].tick_params(direction='in',labelsize=15,width=2)
                    ax[1].set_title('Background Subtrackted Normalized & Shifted')
                    ax[1].set_xlabel('Energy')
                    ax[1].set_ylabel('NEXAFS')
                    ax[1].yaxis.set_label_position("right")
                    ax[1].yaxis.tick_right()
                    ax[1].tick_params(direction='in',labelsize=15,width=2)

                    for i in range(len(ITN)):
                        ax[0].plot(Energy[i], ITN[i])
                        ax[1].plot(Energy[i], ITN[i]+0.1*(i+1), label = self.UsedClassList[i].Name)

                    ax[1].legend(loc='upper center', bbox_to_anchor=(0, -0.2), fancybox=True, shadow=True, ncol=5);


                    ButtonSaveNormalizedData = widgets.Button(
                        description="Save normalized data",
                        layout=Layout(width='30%', height='35px'))
                    display(ButtonSaveNormalizedData)

                    @ButtonSaveNormalizedData.on_click
                    def ActionSaveNormalizedData(selfbutton):
                        #Save normalized data
                        for j, C in enumerate(self.UsedClassList):
                            TempDF = pd.DataFrame()
                            TempDF["Energy" ] = Energy[j]
                            TempDF["\u03BC"] =  Mu[j]
                            TempDF["BackgroundCorrected"] = ITB[j]
                            TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB[j]]
                            TempDF["Normalized"] = ITN[j]
                            setattr(C, "ReducedDf", TempDF)
                            print(f"Saved Dataset {C.Name}")
                            TempDF.to_csv(f"{self.Folders[2]}\\{C.Name}_Reduced.csv", index=False)
                            C.pickle()

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")

        except (ValueError, NameError):
            plt.close()
            print("The selected energy range is wrong.")


    def ReduceSplinesDerivative(self, y, interval):
        """Finds the maximum of the derivative foe each Dataset"""

        def derivativeList(Energy, Mu):
            """Return the right derivative for each point x_i as (y[1:]-y[:-1])/(x[1:]-x[:-1]), with a new x_i = np.round(0.5*(x[:-1]+x[1:]), 2)
            Also returns the abscisse taken between each of these point, array of same length."""
            dEnergy =  []
            dIT = []

            for i in range(len(Mu)):
                x=Energy[i].values
                y=Mu[i].values
                dy = (y[1:]-y[:-1])/(x[1:]-x[:-1])
                dx = np.round(0.5*(x[:-1]+x[1:]), 2)

                dEnergy.append(dx)
                dIT.append(dy)

            return dIT, dEnergy
            
        try:
            number = self.UsedDatasetPosition
            df = self.UsedDfType

            Mu, Energy, v1, v2 = [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y])
                Energy.append(UsedDf["Energy"])
                try :
                    v1.append(int(np.where(Energy[j] == interval[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    #Take one less point due to the right derivative in derivativeList
                    v2.append(int(np.where(Energy[j] == interval[1])[0]) -1)
                except TypeError:
                    v2.append(len(Energy[j])-1 -1)


            dy, dE = derivativeList(Energy,Mu)

            Emin = [np.min(e) for e in dE]
            Emax = [np.max(e) for e in dE]
            maxima=[k.argmax() for k in dy]

            def sliderCursor(s):
                plt.close()
                energymaximasl=dE[number][maxima[number]]

                fig,axs=plt.subplots(nrows=1, ncols=2,figsize = (16, 6))
                axs[0].set_xlabel('Energy')
                axs[0].set_ylabel('NEXAFS')
                axs[0].set_title('1st Derivative')
                axs[0].tick_params(direction='in',labelsize=15,width=2)
                axs[0].plot(dE[number],dy[number],"--", linewidth = 1,label='Derivative')
                axs[0].set_xlim(Emin[number],Emax[number])

                maxD=np.max(dy[number])
                positionMaxD=list(dy[number]).index(maxD)

                axs[0].plot(dE[number][v1[number]:v2[number]],dy[number][v1[number]:v2[number]], linewidth = 1,label='Selected Region')
                axs[0].plot(dE[number][positionMaxD],maxD,'o',markersize=2,label='E0 derivative')
                axs[0].axvline(x=dE[number][s],color='green',linestyle='--',label='E0 slider')
                axs[0].axvline(x=dE[number][v1[number]],color='black',linestyle='--')
                axs[0].axvline(x=dE[number][v2[number]],color='black',linestyle='--')
                axs[0].legend()

                axs[1].plot(Energy[number][v1[number]:v2[number]],Mu[number][v1[number]:v2[number]])
                axs[1].set_xlim(Energy[number][v1[number]],Energy[number][v2[number]])
                axs[1].tick_params(direction='in',labelsize=15,width=2)
                axs[1].axvline(x=Energy[number][s],color='green',linestyle='--')
                axs[1].set_title("F")

                axs[1].set_xlabel('Energy')
                axs[1].set_ylabel('NEXAFS')
                axs[1].yaxis.set_label_position("right")

                print('Cursor Position:',dE[number][s], 'eV')
                print("Calculated Maximum Position:",dE[number][positionMaxD], 'eV', ' ; channel:',positionMaxD)

                ButtonSaveE0 = widgets.Button(
                    description="Save E0",
                    layout=Layout(width='25%', height='35px'))
                ButtonSaveAll = widgets.Button(
                    description="Save all default values",
                    layout=Layout(width='25%', height='35px'))
                ButtonSplinesReduction = widgets.Button(
                    description="Proceed to reduction",
                    layout=Layout(width='25%', height='35px'))
                display(widgets.HBox((ButtonSaveE0, ButtonSaveAll, ButtonSplinesReduction)))

                def ActionSaveE0(selfbutton):
                    setattr(self.UsedDataset, "E0", dE[number][s])
                    self.UsedDataset.pickle()
                    print(f"Saved E0 for {self.UsedDataset.Name};  ")

                def ActionSaveAll(selfbutton):
                    for j, C in enumerate(self.UsedClassList):
                        setattr(self.UsedClassList[j], "E0", dE[j][maxima[j]])
                        C.pickle()
                        print(f"Saved E0 for {self.UsedClassList[j].Name};  ")

                def ActionSplinesReduction(selfbutton):
                    try:
                        E0Values = [getattr(self.UsedClassList[j], "E0") for j, C in enumerate(self.UsedClassList)]

                        self.ListReduceSplines = interactive(self.ReduceSplines,
                                            Spec = widgets.Dropdown(
                                                options = self.UsedClassList,
                                                description = 'Select the Dataset:',
                                                disabled=False,
                                                style = {'description_width': 'initial'}),
                                            order_pre = widgets.Dropdown(
                                                options = [("Select and order", "value"), ("Victoreen", "Victoreen"), ("0", 0), ("1", 1), ("2", 2), ("3", 3)],
                                                value = "value",
                                                description='Order of pre-edge:',
                                                disabled=False,
                                                style = {'description_width': 'initial'}),
                                            order_pst = widgets.Dropdown(
                                                options = [("Select and order", "value"), ("Victoreen", "Victoreen"), ("0", 0), ("1", 1), ("2", 2), ("3", 3)],
                                                value = "value",
                                                description='Order of post-edge:',
                                                disabled=False,
                                                style = {'description_width': 'initial'}),
                                            s1= widgets.FloatRangeSlider(
                                                min=self.NewEnergyColumn[0],
                                                value = [self.NewEnergyColumn[0], np.round(self.NewEnergyColumn[0] + 0.33*(self.NewEnergyColumn[-1] - self.NewEnergyColumn[0]), 0)],
                                                max = self.NewEnergyColumn[-1],
                                                step = self.InterpolStep,
                                                description='Energy range (eV):',
                                                disabled=False,
                                                continuous_update=False,
                                                orientation='horizontal',
                                                readout=True,
                                                readout_format='.2f',
                                                style = {'description_width': 'initial'},
                                                layout = Layout(width='50%', height='40px')),
                                            s2= widgets.FloatRangeSlider(
                                                min=self.NewEnergyColumn[0],
                                                value = [np.round(self.NewEnergyColumn[0] + 0.66*(self.NewEnergyColumn[-1] - self.NewEnergyColumn[0]), 0), self.NewEnergyColumn[-1]],
                                                max = self.NewEnergyColumn[-1],
                                                step = self.InterpolStep,
                                                description='Energy range (eV):',
                                                disabled=False,
                                                continuous_update=False,
                                                orientation='horizontal',
                                                readout=True,
                                                readout_format='.2f',
                                                style = {'description_width': 'initial'},
                                                layout = Layout(width='50%', height='40px')),
                                            ParamA1 = widgets.Text(
                                                value="1000000000",
                                                placeholder='A1 = ',
                                                description='A1:',
                                                disabled=True,
                                                continuous_update=False,
                                                style = {'description_width': 'initial'}),
                                            ParamB1 = widgets.Text(
                                                value="1000000000",
                                                placeholder='B1 = ',
                                                description='B1:',
                                                disabled=True,
                                                continuous_update=False,
                                                style = {'description_width': 'initial'}),
                                            ParamA2 = widgets.Text(
                                                value="1000000000",
                                                placeholder='A2 = ',
                                                description='A2:',
                                                disabled=True,
                                                continuous_update=False,
                                                style = {'description_width': 'initial'}),
                                            ParamB2 = widgets.Text(
                                                value="1000000000",
                                                placeholder='B2 = ',
                                                description='B2:',
                                                disabled=True,
                                                continuous_update=False,
                                                style = {'description_width': 'initial'}),
                                            y = fixed(y))
                        self.WidgetListReduceSplines=widgets.VBox([widgets.HBox(self.ListReduceSplines.children[:3]), widgets.HBox(self.ListReduceSplines.children[3:5]), widgets.HBox(self.ListReduceSplines.children[5:9]),
                            self.ListReduceSplines.children[-1]])
                        
                        self.ListTabReduceMethod.children[1].disabled = True
                        self.ListReduceDerivative.children[0].disabled = True
                        self.ListReduceDerivative.children[1].disabled = True
                        self.SlidersSplines.children[0].disabled = True

                        self.ListReduceSplines.children[1].observe(self.ParamVictoreenHandler1, names='value')
                        self.ListReduceSplines.children[2].observe(self.ParamVictoreenHandler2, names='value')

                        clear_output(True)
                        print(f"We now use the values previously fixed for E0 in our reduction routine, to normalize the intensity by the absorption edge jump.\n")
                        display(self.WidgetListReduceSplines)
                    except Exception as e:
                        raise e
                    # except AttributeError:
                    #     print("You have not yet fixed all the values !")

                ButtonSplinesReduction.on_click(ActionSplinesReduction)
                ButtonSaveE0.on_click(ActionSaveE0)
                ButtonSaveAll.on_click(ActionSaveAll)

            self.SlidersSplines = interactive(sliderCursor, 
                s = widgets.BoundedIntText(
                    value=maxima[number],
                    step=1,
                    min = 0,
                    max = len(Energy[0]) -1,
                    description='Cursor:',
                    disabled=False))
            display(self.SlidersSplines)

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except (ValueError, NameError):
            plt.close()
            print("The selected energy range is wrong.")

    def ReduceSplines(self, Spec, order_pre, order_pst, s1, s2, ParamA1, ParamB1, ParamA2, ParamB2, y):
        """Reduce the background using two curves and then normalize by edge-jump."""

        try:
            number = self.UsedClassList.index(Spec)
            df = self.UsedDfType
            print(s1, s2)

            Mu, Energy, E0, v1, v2, v3, v4 = [], [], [], [], [], [], []
            for j, C in enumerate(self.UsedClassList):
                UsedDf = getattr(C, df)
                Mu.append(UsedDf[y].values)
                Energy.append(UsedDf["Energy"].values)
                E0.append(getattr(C, "E0"))
                
                #First and second zoom
                try :
                    v1.append(int(np.where(Energy[j] == s1[0])[0]))
                except TypeError:
                    v1.append(0)

                try:
                    #Take one less point due to the right derivative in derivativeList
                    v2.append(int(np.where(Energy[j] == s1[1])[0]) -1)
                except TypeError:
                    v2.append(len(Energy[j])-1 -1)

                try :
                    v3.append(int(np.where(Energy[j] == s2[0])[0]))
                except TypeError:
                    v3.append(0)

                try:
                    #Take one less point due to the right derivative in derivativeList
                    v4.append(int(np.where(Energy[j] == s2[1])[0]) -1)
                except TypeError:
                    v4.append(len(Energy[j])-1 -1)

            plt.close()

            #Compute the background that will be subtracted
            e0=min(Energy[number], key=lambda x:abs(x-E0[number]))
            e0c=list(Energy[number]).index(e0)

            if order_pre is "value":
                raise AttributeError("Please select an order.")

            elif order_pre is "Victoreen":
                #make a lsq fit
                self.Vmodel = lmfit.Model(self.Victoreen, prefix='Pre_edge_')

                self.x = Energy[number]
                self.y = Mu[number]
                self.resultVpre = self.Vmodel.fit(Mu[number][v1[number]:v2[number]], x=Energy[number][v1[number]:v2[number]], Pre_edge_A=int(ParamA1), Pre_edge_B=int(ParamB1))
                display(self.resultVpre.params)

                p1 = self.Victoreen(Energy[number], self.resultVpre.params["Pre_edge_A"].value, self.resultVpre.params["Pre_edge_B"].value)
                p1E0 = self.Victoreen(E0[number], self.resultVpre.params["Pre_edge_A"].value, self.resultVpre.params["Pre_edge_B"].value)

            elif isinstance(order_pre, int):
                #Find the polynomials coefficients
                coef1=np.polyfit(Energy[number][v1[number]:v2[number]], Mu[number][v1[number]:v2[number]], order_pre)

                #Create the polynomial function from the coefficients
                p1call=np.poly1d(coef1)
                p1 = p1call(Energy[number])
                p1E0 = p1call(E0[number])


            if order_pst is "value":
                raise AttributeError("Please select an order.")

            elif order_pst is "Victoreen":
                #make a lsq fit
                self.Vmodel = lmfit.Model(self.Victoreen, prefix='Post_edge_')

                self.resultVpst = self.Vmodel.fit(Mu[number][v3[number]:v4[number]], x=Energy[number][v3[number]:v4[number]], Post_edge_A=int(ParamA2), Post_edge_B=int(ParamB2))
                display(self.resultVpst.params)

                p2 = self.Victoreen(Energy[number], self.resultVpst.params["Post_edge_A"].value, self.resultVpst.params["Post_edge_B"].value)
                p2E0 = self.Victoreen(E0[number], self.resultVpst.params["Post_edge_A"].value, self.resultVpst.params["Post_edge_B"].value)


            elif isinstance(order_pst, int):
                #Find the polynomials coefficients
                coef2=np.polyfit(Energy[number][v3[number]:v4[number]], Mu[number][v3[number]:v4[number]], order_pst)

                #Create the polynomial function from the coefficients
                p2call=np.poly1d(coef2)
                p2 = p2call(Energy[number])
                p2E0 = p2call(E0[number])


            #Substract pre-edge
            ITs=Mu[number]-p1
            #Compute edge-jump
            delta=abs(p2E0-p1E0)
            #Normalise
            ITB = ITs/delta
            ITN = ITB / np.trapz(ITB)

            #Plot current work
            fig,axs=plt.subplots(nrows=1, ncols=2,figsize=(16, 6))
            axs[0].set_xlabel('Energy')
            axs[0].set_ylabel('NEXAFS')
            axs[0].set_title('Raw Data')
            axs[0].tick_params(direction='in',labelsize=15,width=2)

            axs[0].plot(Energy[number], Mu[number], linewidth = 1, label='Data')
            axs[0].plot(Energy[number][v1[number]:v2[number]], Mu[number][v1[number]:v2[number]], 'o',color='orange',label='pre-edge')
            axs[0].plot(Energy[number][v3[number]:v4[number]], Mu[number][v3[number]:v4[number]], 'o',color='red',label='post-edge')
            axs[0].axvline(Energy[number][e0c],  color='green', linestyle='--',label='E0')

            axs[0].axvline(Energy[number][v1[number]], color='orange', linestyle='--')
            axs[0].axvline(Energy[number][v2[number]], color='orange', linestyle='--')
            axs[0].axvline(Energy[number][v3[number]], color='tomato', linestyle='--')
            axs[0].axvline(Energy[number][v4[number]], color='tomato', linestyle='--')

            axs[0].plot(Energy[number], p1,'--', linewidth = 1, color='dodgerblue',label='Polynoms')
            axs[0].plot(Energy[number], p2,'--', linewidth = 1, color='dodgerblue')

            axs[0].legend()
            axs[0].set_ylim(np.min(Mu[number])-0.01*np.min(Mu[number]), np.max(Mu[number])+0.01*np.max(Mu[number]))

            #Plot without background
            axs[1].set_title('Bkg Subtrackted & Normalized')

            axs[1].plot(Energy[number], ITB,label='Data')

            axs[1].axvline(E0[number], color='green', linestyle='--', label = "E0")
            axs[1].axhline(1, color='red', linestyle='--', label = "Normalisation to 1.")
            axs[1].set_xlim(np.min(Energy[number]),np.max(Energy[number]))
            axs[1].set_xlabel('Energy')
            axs[1].set_ylabel('NEXAFS')
            axs[1].yaxis.set_label_position("right")
            axs[1].tick_params(direction='in',labelsize=15,width=2)
            axs[1].legend()

            ButtonSaveDataset = Button(
                description="Save Data",
                layout=Layout(width='15%', height='35px'))
            display(ButtonSaveDataset)

            @ButtonSaveDataset.on_click
            def ActionSaveDataset(selfbutton):
                #Save single Dataset without background in Class
                TempDF = pd.DataFrame()
                TempDF["Energy" ] = Energy[number]
                TempDF["\u03BC"] =  Mu[number]
                TempDF["BackgroundCorrected"] = ITB
                TempDF["\u03BC Variance (1/\u03BC)"] = [1/d if d >0 else 0 for d in ITB]
                TempDF["Normalized"] = ITN
                setattr(Spec, "ReducedDfSplines", TempDF)
                print(f"Saved Dataset {Spec.Name}")
                TempDF.to_csv(f"{self.Folders[2]}\\{Spec.Name}_SplinesReduced.csv", index=False)

                #Need to plot again
                fig,axs=plt.subplots(nrows=1, ncols=2,figsize=(16, 6))
                axs[0].set_xlabel('Energy')
                axs[0].set_ylabel('NEXAFS')
                axs[0].set_title('Raw Data')
                axs[0].tick_params(direction='in',labelsize=15,width=2)

                axs[0].plot(Energy[number], Mu[number], linewidth = 1, label='Data')
                axs[0].plot(Energy[number][v1[number]:v2[number]], Mu[number][v1[number]:v2[number]], 'o',color='orange',label='pre-edge')
                axs[0].plot(Energy[number][v3[number]:v4[number]], Mu[number][v3[number]:v4[number]], 'o',color='red',label='post-edge')
                axs[0].axvline(Energy[number][e0c],  color='green', linestyle='--',label='E0')

                axs[0].axvline(Energy[number][v1[number]], color='orange', linestyle='--')
                axs[0].axvline(Energy[number][v2[number]], color='orange', linestyle='--')
                axs[0].axvline(Energy[number][v3[number]], color='tomato', linestyle='--')
                axs[0].axvline(Energy[number][v4[number]], color='tomato', linestyle='--')

                axs[0].plot(Energy[number], p1,'--', linewidth = 1, color='dodgerblue',label='Polynoms')
                axs[0].plot(Energy[number], p2,'--', linewidth = 1, color='dodgerblue')

                axs[0].legend()
                axs[0].set_ylim(np.min(Mu[number])-0.01*np.min(Mu[number]), np.max(Mu[number])+0.01*np.max(Mu[number]))

                #Plot without background
                axs[1].set_title('Bkg Subtrackted & Normalized')

                axs[1].plot(Energy[number], ITB,label='Data')

                axs[1].axvline(E0[number], color='green', linestyle='--', label = "E0")
                axs[1].axhline(1, color='red', linestyle='--', label = "Normalisation to 1.")
                axs[1].set_xlim(np.min(Energy[number]),np.max(Energy[number]))
                axs[1].set_xlabel('Energy')
                axs[1].set_ylabel('NEXAFS')
                axs[1].yaxis.set_label_position("right")
                axs[1].tick_params(direction='in',labelsize=15,width=2)
                axs[1].legend()
                plt.tight_layout()

                plt.savefig(f"{self.Folders[3]}\\SplinesReduced_{Spec.Name}.pdf");
                plt.savefig(f"{self.Folders[3]}\\SplinesReduced_{Spec.Name}.png");
                plt.close()
                Spec.pickle()

        except (AttributeError, KeyError):
            plt.close()
            if y =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except (ValueError, NameError):
            plt.close()
            print("The selected energy range, order, or parameter value is wrong.")

    #Fitting
    def Fitting(self, Spec, PrintedDf, ShowBool):
        """Displays the pandas.DataFrame associated to each dataset, there are currently 4 different possibilities:
            _ df : Original data
            _ ShiftedDf : Is one shifts the energy 
            _ ReducedDf : If one applies some background reduction or normalization method 
            _ ReducedDfSplines : If one applied the specific Splines background reduction and normalization method.
        Each data frame is automatically saved as a .csv file after creation."""

        if not ShowBool:
            print("Window cleared")
            clear_output(True)

        elif ShowBool:
            try :
                self.UsedDataset = Spec
                self.UsedDfType = PrintedDf
                UsedDf = getattr(self.UsedDataset, self.UsedDfType)

                display(self.WidgetListFit)

            except (AttributeError, KeyError):
                print(f"Wrong dataset and column combination !")
    
    def Model(self, xcol, ycol, interval, PeakNumber, PeakType, BackgroundType, PolDegree, StepType, method, w, FixModel):
        #We built a model using the lmfit package, composed of a background, a step and a certain number of polynomials
        
        # Retrieve the data      
        self.UsedDfFit = getattr(self.UsedDataset, self.UsedDfType)
        clear_output(True)

        try:

            # We create the model
            try :
                i = int(np.where(self.UsedDfFit[xcol] == interval[0])[0])
            except TypeError:
                i = 0

            try:
                j = int(np.where(self.UsedDfFit[xcol] == interval[1])[0])
            except TypeError:
                j = -1

            y = self.UsedDfFit[ycol].values[i:j]
            x = self.UsedDfFit[xcol].values[i:j]

            self.FitDf = pd.DataFrame({
                xcol : x,
                ycol : y
                })

            # Background
            if BackgroundType == PolynomialModel:
                self.mod = BackgroundType(degree = PolDegree, prefix='Bcgd_')
                self.pars = self.mod.guess(y, x=x)

            elif BackgroundType is "Victoreen":
                self.mod = lmfit.Model(self.Victoreen, prefix='Bcgd_')
                self.pars = self.mod.make_params(Bcgd_A=1, Bcgd_B=1)

            else:
                self.mod = BackgroundType(prefix='Bcgd_')
                self.pars = self.mod.guess(y, x=x)
            
            # Add a step if needed
            if StepType:
                Step = StepModel(form = StepType, prefix="Step_")
                self.pars.update(Step.make_params())
                self.mod += Step
            
            # Create a dictionnary for the peak to be able to iterate on their names
            peaks=dict()
            
            for i in range(PeakNumber):
                peaks[f"Peak_{i}"] = PeakType(prefix=f"P{i}_")
                self.pars.update(peaks[f"Peak_{i}"].make_params())
                self.mod += peaks[f"Peak_{i}"]

            self.paranames = [str(p) for p in self.pars]
            self.paracolnames = ["value", "min", "max"]
            
            if FixModel:
                print("Please start by selecting a parameter to start working on the initial guess.")

                def InitPara(para, column, value):
                    ButtonRetrievePara = Button(
                        description="Retrieve parameters",
                        layout=Layout(width='25%', height='35px'))
                    ButtonSavePara = Button(
                        description="Save parameter value",
                        layout=Layout(width='25%', height='35px'))
                    ButtonFit = Button(
                        description="Launch Fit",
                        layout=Layout(width='15%', height='35px'))
                    ButtonGuess = Button(
                        description="See current guess",
                        layout=Layout(width='15%', height='35px'))
                    ButtonSaveModel = Button(
                        description="Save current work",
                        layout=Layout(width='15%', height='35px'))
                    display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))
                    display(self.pars)

                    @ButtonRetrievePara.on_click
                    def ActionRetrievePara(selfbutton):
                        clear_output(True)
                        plt.close()
                        display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))

                        try:
                            self.result = getattr(self.UsedDataset, "result")
                            self.pars = getattr(self.result, "params")
                            print("Previously saved parameters loaded, press see current guess to see current guess.")

                        except:
                            print("Could not load any parameters.")

                    @ButtonSavePara.on_click
                    def ActionSavePara(selfbutton):
                        clear_output(True)
                        plt.close()
                        display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))                        
                        try:
                            if column == "value":
                                self.pars[f"{para}"].set(value = value)
                            if column == "min":
                                self.pars[f"{para}"].set(min = value)
                            if column == "max":
                                self.pars[f"{para}"].set(max = value)

                            display(self.pars)
                        except Exception as e:
                            raise e

                    @ButtonGuess.on_click
                    def ActionGuess(selfbutton):
                        clear_output(True)
                        plt.close()
                        display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))                        
                        try:
                            display(self.pars)

                            # Current guess
                            self.init = self.mod.eval(self.pars, x=x)

                            fig, ax = plt.subplots(figsize=(16, 6))
                            ax.plot(x, y, label = "Data")
                            ax.plot(x, self.init, label='Current guess')
                            ax.legend()
                            plt.show()  
                        except Exception as e:
                            raise e

                    @ButtonFit.on_click
                    def ActionFit(selfbutton):
                        clear_output(True)
                        display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))                        

                        # Current guess
                        self.init = self.mod.eval(self.pars, x=x)

                        #Retrieve the interval
                        try :
                            i = int(np.where(self.UsedDfFit[xcol] == interval[0])[0])
                        except TypeError:
                            i = 0

                        try:
                            j = int(np.where(self.UsedDfFit[xcol] == interval[1])[0])
                        except TypeError:
                            j = -1

                        #Retrieve weights
                        if w is "Obs":
                            weights = 1/y.values[i:j]

                        elif w is "RMS":
                            try:
                                weights = 1/self.UsedDfFit["RMS"].values[i:j]
                            except AttributeError:
                                print("You need to define the RMS error first, the weights are put to 1 for now.")
                                weights = None

                        elif w is "UserError":
                            try:
                                weights = self.UsedDfFit["UserError"].values[i:j]
                            except (KeyError, AttributeError):
                                print("You need to define the User error in the initialisation, the weights are put to 1 for now.")
                                weights = None                 
                        else:
                            weights = None

                        self.FitDf["Weights"] = weights

                        # Launch fit
                        self.out = self.mod.fit(y, self.pars, x=x, method = method, weights = weights)
                        self.comps = self.out.eval_components(x=x)

                        display(self.out)

                        ### Check the stats of the fit
                        chisq, p = chisquare(self.out.data, self.out.best_fit, ddof=(self.out.nfree))
                        setattr(self.UsedDataset, "chisq", chisq)
                        setattr(self.UsedDataset, "p", p)

                        print(f"Sum of squared residuals : {np.sum(self.out.residual**2)}, lmfit chisqr : {self.out.chisqr}")
                        print(f"Sum of squared residuals/nfree : {np.sum(self.out.residual**2)/(self.out.nfree)}, lmfit redchisqr : {self.out.redchi}")

                        # https://docs.scipy.org/doc/scipy/Reference/generated/scipy.stats.chisquare.html
                        print(f"Scipy Chi square for Poisson distri = {chisq}, 1 - p = {1 - p}")
                        print(f"lmfit chisqr divided iter by expected : {np.sum((self.out.residual**2)/self.out.best_fit)}")

                        RFact = 100 * (np.sum(self.out.residual**2)/np.sum(self.out.data**2))
                        setattr(self.UsedDataset, "RFact", RFact)
                        print(f"R factor : {RFact} %.\n")

                        # Plot
                        fig, axes = plt.subplots(2, 2, figsize=(16, 7), gridspec_kw={'height_ratios': [5, 1]})

                        axes[0, 0].plot(x, y, label = "Data")
                        axes[0, 0].plot(x, self.out.best_fit, label='Best fit')
                        axes[0, 0].set_xlabel(xcol, fontweight='bold')
                        axes[0, 0].set_ylabel(ycol, fontweight='bold')
                        axes[0, 0].set_title(f"Best fit - {self.UsedDataset.Name}")
                        axes[0, 0].legend()

                        # Residuals
                        axes[1, 0].set_title("Residuals")
                        axes[1, 0].scatter(x, self.out.residual, s = 0.5)
                        axes[1, 0].set_xlabel(xcol, fontweight='bold')
                        axes[1, 0].set_ylabel(ycol, fontweight='bold')

                        axes[1, 1].set_title("Residuals")
                        axes[1, 1].scatter(x, self.out.residual, s = 0.5)   
                        axes[1, 1].set_xlabel(xcol, fontweight='bold')
                        axes[1, 1].set_ylabel(ycol, fontweight='bold')

                        # Detailed plot
                        axes[0, 1].set_title("Best fit - Detailed")
                        axes[0, 1].plot(x, y, label = "Data")

                        if BackgroundType == ConstantModel:
                            axes[0, 1].plot(x, np.ones(len(x)) * self.comps['Bcgd_'], 'k--', label='Background')
                        else:
                            axes[0, 1].plot(x, self.comps['Bcgd_'], 'k--', label='Background')

                        if StepType:
                            axes[0, 1].plot(x, self.comps['Step_'], label='Step')

                        for i in range(PeakNumber):
                              axes[0, 1].plot(x, self.comps[f"P{i}_"], label=f"Peak nb {i}")

                        axes[0, 1].set_xlabel(xcol, fontweight='bold')
                        axes[0, 1].set_ylabel(ycol, fontweight='bold')
                        axes[0, 1].legend()
                        plt.tight_layout()

                        plt.savefig(f"{self.Folders[3]}\\Fit{self.UsedDataset.Name}.pdf");
                        plt.savefig(f"{self.Folders[3]}\\Fit{self.UsedDataset.Name}.png");

                        ButtonCI = Button(
                            description="Determine confidence intervals",
                            layout=Layout(width='25%', height='35px'))
                        ButtonParaSpace = Button(
                            description="Determine the parameter distribution",
                            layout=Layout(width='35%', height='35px'))
                        display(widgets.HBox((ButtonCI,  ButtonParaSpace)))

                        @ButtonCI.on_click
                        def ActionCI(selfbutton):
                            try :
                                C = self.out.covar
                                self.out.stderr = [self.out.params[f"{p}"].stderr for p in self.out.params]
                                self.out.correl = [self.out.params[f"{p}"].correl for p in self.out.params]
                                print(f"The shape of the estimated covariance matrix is : {np.shape(self.out.covar)}.")
                                # determine conf int direct du coup

                                def ResidualsCompModel(p):
                                    return self.out.userfcn(p, y, x = x, weights = weights)

                                self.Minimizer = lmfit.Minimizer(ResidualsCompModel, self.pars)
                                result = self.Minimizer.minimize()
                                self.ci = lmfit.conf_interval(self.Minimizer, result)
                                lmfit.printfuncs.report_ci(self.ci)

                                try:
                                    # setattr(self.UsedDataset, "ResidualsCompModel", self.ResidualsCompModel)
                                    # setattr(self.UsedDataset, "Minimizer", self.Minimizer)
                                    setattr(self.UsedDataset, "ci", self.ci)
                                    self.UsedDataset.pickle()
                                except:
                                    print("CI could not be saved.\n")

                            except Exception as e:
                                raise e

                            #except:
                            #    print("No covariance matrix could be estimated from the fitting routine.")

                        @ButtonParaSpace.on_click
                        def ActionParaSpace(selfbutton):
                            print(i, j)
                            return self.ExploreParams(self.UsedDataset, self.UsedDfType, i, j, xcol, ycol)

                    @ButtonSaveModel.on_click
                    def ActionSave(selfbutton):
                        clear_output(True)
                        display(widgets.HBox((ButtonRetrievePara, ButtonSavePara, ButtonGuess, ButtonFit, ButtonSaveModel)))                        

                        print("Saved the initial parameters as GUI.pars")
                        self.pars = self.out.params

                        try:
                            setattr(self.UsedDataset, "init", self.init)
                            print("Saved the initial guess as Dataset.init")

                            setattr(self.UsedDataset, "result", self.out.result)
                            print("Saved the output of the fitting routine as Dataset.result ")
                        except:
                            print("Launch the fit first. \n")

                        try:
                            self.FitDf["Fit"] = self.out.best_fit
                            self.FitDf["Residuals"] = self.out.residual
                            setattr(self.UsedDataset, "FitDf", self.FitDf)
                        except Exception as e:
                            raise e

                        try:
                            self.UsedDataset.pickle()

                        except Exception as e:
                            raise e
                            print("Could not save the class instance with pickle().")

                self.ListPara = interactive(InitPara,
                    para = widgets.Dropdown(
                        options = self.paranames,
                        value = None,
                        description = 'Select the parameter:',
                        style = {'description_width': 'initial'}),
                    column = widgets.Dropdown(
                        options = self.paracolnames,
                        description = 'Select the column:',
                        style = {'description_width': 'initial'}),
                    value = widgets.FloatText(
                        value = 0,
                        step = 0.01,
                        description='Value :'))
                self.WidgetListPara=widgets.VBox([widgets.HBox(self.ListPara.children[0:3]), self.ListPara.children[-1]])
                display(self.WidgetListPara)

            else :
                plt.close()
                print("Cleared")
                clear_output(True)

        except (AttributeError, KeyError):
            plt.close()
            if ycol =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except TypeError:
            print("This peak distribution is not yet working, sorry.")

    def ExploreParams(self, i, j, xcol, ycol):
        """To execute after a fit, allows one to explore the parameter space with the emcee Markov Monte carlo chain."""
        try:

            y = self.UsedDfFit[ycol].values[i:j]
            x = self.UsedDfFit[xcol].values[i:j]
            
            self.mi = self.out
            self.mi.params.add('__lnsigma', value=np.log(0.1), min=np.log(0.001), max=np.log(2))
            self.resi = self.mod.fit(y, params = self.mi.params, x=x, method = "emcee", nan_policy='omit')
            
            plt.plot(self.resi.acceptance_fraction)
            plt.xlabel('walker')
            plt.ylabel('acceptance fraction')
            plt.title("Rule of thumb, should be between 0.2 and 0.5.")
            plt.show()
            plt.close()
            
            self.emcee_plot = corner.corner(self.resi.flatchain, labels=self.resi.var_names, truths=list(self.resi.params.valuesdict().values()))
            plt.savefig(f"{self.Folders[3]}\\{self.UsedDataset.Name}CornerPlot.pdf")
            plt.savefig(f"{self.Folders[3]}\\{self.UsedDataset.Name}CornerPlot.png")
            
            print('median of posterior probability distribution')
            print('--------------------------------------------')
            lmfit.report_fit(self.resi.params)
            
            
            self.p = self.pars.copy()
            used_param = self.resi.var_names
            del used_param[-1]

            highest_prob = np.argmax(self.resi.lnprob)
            hp_loc = np.unravel_index(highest_prob, self.resi.lnprob.shape)
            mle_soln = self.resi.chain[hp_loc]
            for i, par in enumerate(used_param):
                self.p[par].value = mle_soln[i]


            print('\nMaximum Likelihood Estimation from emcee       ')
            print('-------------------------------------------------')
            print('Parameter  MLE Value   Median Value   Uncertainty')
            fmt = '  {:5s}  {:11.5f} {:11.5f}   {:11.5f}'.format
            for name, param in self.p.items():
                if self.resi.params[name].stderr:
                    print(fmt(name, param.value, self.resi.params[name].value, self.resi.params[name].stderr))
                    
                    
            print('\nError Estimates from emcee    ')
            print('------------------------------------------------------')
            print('Parameter  -2sigma  -1sigma   median  +1sigma  +2sigma ')

            for name, param in self.p.items():
                if self.resi.params[name].stderr:
                    quantiles = np.percentile(self.resi.flatchain[name],
                                          [2.275, 15.865, 50, 84.135, 97.275])
                    median = quantiles[2]
                    err_m2 = quantiles[0] - median
                    err_m1 = quantiles[1] - median
                    err_p1 = quantiles[3] - median
                    err_p2 = quantiles[4] - median
                    fmt = '  {:5s}   {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}'.format
                    print(fmt(name, err_m2, err_m1, median, err_p1, err_p2))
        
        except (AttributeError, KeyError):
            plt.close()
            if ycol =="value":
                print("Please select a column.")
            else:
                print(f"Wrong dataset and column combination !")
        except Exception as e:
            raise e


    #Plotting interactive function
    def PlotDataset(self, SpecNumber, Plotdf, x, y, xaxis, yaxis, Title, CheckPlot):
        """Allows one to plot one Dataset or all spectra together and to then save the figure"""
        if CheckPlot == "Zero":
            print("No plotting atm.")

        elif CheckPlot == "Plot" and len(SpecNumber) == 1:
            @interact(
                interval = widgets.FloatRangeSlider(
                            min=self.NewEnergyColumn[0],
                            value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                            max = self.NewEnergyColumn[-1],
                            step = self.InterpolStep,
                            description='Energy range (eV):',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.2f',
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')),
                colorplot = widgets.ColorPicker(
                            concise=False,
                            description='Pick a color',
                            value='Blue',
                            disabled=False,
                            style = {'description_width': 'initial'}))
            def PlotOne(interval, colorplot):
                try:
                    UsedDf = getattr(SpecNumber[0], Plotdf)
                    try :
                        v1 = int(np.where(UsedDf[x] == interval[0])[0])
                    except TypeError:
                        v1 = 0

                    try:
                        v2 = int(np.where(UsedDf[x] == interval[1])[0])
                    except TypeError:
                        v2 = -1

                    ButtonSavePlot = Button(
                        description="Save Plot",
                        layout=Layout(width='15%', height='35px'))
                    display(ButtonSavePlot)

                    plt.close()

                    fig, ax = plt.subplots(figsize = (16, 6))
                    ax.set_xlabel(xaxis)
                    ax.set_ylabel(yaxis)
                    ax.set_title(Title)

                    ax.plot(UsedDf[x][v1:v2], UsedDf[y][v1:v2], linewidth = 1, color = colorplot, label=f"{SpecNumber[0].Name}")
                    ax.legend()

                    @ButtonSavePlot.on_click
                    def ActionSavePlot(selfbutton):
                        fig, ax = plt.subplots(figsize = (16, 6))
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        ax.set_title(Title)

                        ax.plot(UsedDf[x][v1:v2], UsedDf[y][v1:v2], linewidth = 1, color = colorplot, label=f"{SpecNumber[0].Name}")
                        ax.legend()
                        plt.tight_layout()
                        plt.savefig(f"{self.Folders[3]}\\{Title}.pdf");
                        plt.savefig(f"{self.Folders[3]}\\{Title}.png");
                        print(f"Figure {Title} saved !")
                        plt.close()

                except AttributeError:
                    plt.close()
                    print(f"This class does not have the {Plotdf} dataframe associated yet.")
                except IndexError:
                    plt.close()
                    print(f"Please select at least one spectra.")
                except KeyError:
                    plt.close()
                    print(f"The {Plotdf} dataframe does not have such attributes.")


        elif CheckPlot == "Plot" and len(SpecNumber) > 1:
            try:
                T = [int(C.LogbookEntry["Temp (K)"]) for C in SpecNumber]
                print("The color is function of the temperature for each Dataset.")
            except:
                print("No valid Logbook entry for the temperature found as [Temp (K)], the color of the plots will be random.")
                T = False

            @interact(interval = widgets.FloatRangeSlider(
                            min=self.NewEnergyColumn[0],
                            value = [self.NewEnergyColumn[0], self.NewEnergyColumn[-1]],
                            max = self.NewEnergyColumn[-1],
                            step = self.InterpolStep,
                            description='Energy range (eV):',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.2f',
                            style = {'description_width': 'initial'},
                            layout = Layout(width='50%', height='40px')))
            def Plotall(interval):
                try:
                    plt.close()
                    fig, ax = plt.subplots(figsize = (16, 6))
                    ax.set_xlabel(xaxis)
                    ax.set_ylabel(yaxis)
                    ax.set_title(Title)

                    for j, C in enumerate(SpecNumber):
                        UsedDf = getattr(C, Plotdf)
                        try :
                            v1 = int(np.where(UsedDf[x] == interval[0])[0])
                        except TypeError:
                            v1 = 0

                        try:
                            v2 = int(np.where(UsedDf[x] == interval[1])[0])
                        except TypeError:
                            v2 = -1

                        if T:
                            ax.plot(UsedDf[x][v1 : v2], UsedDf[y][v1 : v2], linewidth = 1, label=f"{SpecNumber[j].Name}", color=( (T[j]-273.15)/(max(T)-273.15), 0, ((max(T)-273.15)-(T[j]-273.15))/(max(T)-273.15)))
     
                        if not T:
                            ax.plot(UsedDf[x][v1 : v2], UsedDf[y][v1 : v2], linewidth = 1, label=f"{SpecNumber[j].Name}")
                    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5);

                    ButtonSavePlot = Button(
                        description="Save Plot",
                        layout=Layout(width='15%', height='35px'))
                    display(ButtonSavePlot)

                    @ButtonSavePlot.on_click
                    def ActionSavePlot(selfbutton):
                        plt.close()
                        fig, ax = plt.subplots(figsize = (16, 6))
                        ax.set_xlabel(xaxis)
                        ax.set_ylabel(yaxis)
                        ax.set_title(Title)

                        for j, C in enumerate(SpecNumber):
                            UsedDf = getattr(C, Plotdf)
                            try :
                                v1 = int(np.where(UsedDf[x] == interval[0])[0])
                            except TypeError:
                                v1 = 0

                            try:
                                v2 = int(np.where(UsedDf[x] == interval[1])[0])
                            except TypeError:
                                v2 = -1
                            if T:
                                ax.plot(UsedDf[x][v1 : v2], UsedDf[y][v1 : v2], linewidth = 1, label=f"{SpecNumber[j].Name}", color=( (T[j]-273.15)/(max(T)-273.15), 0, ((max(T)-273.15)-(T[j]-273.15))/(max(T)-273.15)))
         
                            if not T:
                                ax.plot(UsedDf[x][v1 : v2], UsedDf[y][v1 : v2], linewidth = 1, label=f"{SpecNumber[j].Name}")

                        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5);
                        plt.tight_layout()
                        plt.savefig(f"{self.Folders[3]}\\{Title}.pdf");
                        plt.savefig(f"{self.Folders[3]}\\{Title}.png");
                        print(f"Figure {Title} saved !")
                        plt.close()

                except AttributeError:
                    plt.close()
                    print(f"This class does not have the {Plotdf} dataframe associated yet.")
                except KeyError:
                    plt.close()
                    print(f"The {Plotdf} dataframe does not have such attributes.")


        elif CheckPlot == "3D" and len(SpecNumber) > 1:
            print("Please pick a valid range for the x axis.")
            # try:
            #     T = [int(C.LogbookEntry["Temp (K)"]) for C in SpecNumber]
            #     print("The color is function of the temperature for each Dataset.")
            # except:
            #     print("No valid Logbook entry for the temperature found as [Temp (K)], the color of the plots will be random.")
            #     T = False

            try :
                #Create a df that spans the entire energy range
                self.MergedValues = pd.DataFrame({
                    x : self.NewEnergyColumn
                    })

                for C in SpecNumber:
                    UsedDf = getattr(C, Plotdf)
                    yvalues = pd.DataFrame({x : UsedDf[x].values, y: UsedDf[y].values})

                    for v in self.MergedValues[x].values:
                        if v not in yvalues[x].values:
                            yvalues = yvalues.append({x: v}, ignore_index=True).sort_values(by = [x]).reset_index(drop=True)

                    self.MergedValues[str(C.Name) +"_"+str(y)] = yvalues[y]

                def ThreeDimPlot(xname, yname, zname, dist, elev, azim, cmapstyle, title, interval):
                    try:
                        # Get the data
                        clear_output(True)
                        v1 = int(np.where(self.NewEnergyColumn == interval[0])[0])
                        v2 = int(np.where(self.NewEnergyColumn == interval[1])[0])

                        data = self.MergedValues.copy()[v1:v2]                        
                        data.index = data['Energy']
                        del data['Energy']

                        display(data)

                        df=data.unstack().reset_index()
                        df.columns=["X","Y","Z"]

                        df['X']=pd.Categorical(df['X'])
                        df['X']=df['X'].cat.codes

                        NonNanValues = [j for j in df["Z"] if not np.isnan(j)]

                        # Make the plot
                        fig = plt.figure(figsize =(15, 10))
                        ax = fig.add_subplot(111, projection='3d')
                        ax.dist = dist
                        ax.elev = elev
                        ax.azim = azim
                        
                        # Add a color bar which maps values to colors. viridis or jet
                        surf=ax.plot_trisurf(df['Y'], df['X'], df['Z'], cmap=cmapstyle, linewidth=0.2, vmin = min(NonNanValues), vmax = max(NonNanValues))
                        colorbarplot = fig.colorbar(surf, shrink=0.6, label = "Colorbar")

                        ax.set_xlabel(xname)
                        ax.set_ylabel(yname)
                        ax.set_zlabel(zname)
                        ax.set_title(title)

                        fig.tight_layout()
                        plt.savefig(f"{self.Folders[3]}\\{Title}.pdf");
                        plt.savefig(f"{self.Folders[3]}\\{Title}.png");
                        plt.show()

                    except IndexError:
                        print("Please pick a valid range for the x axis.")

                List3D = interactive(ThreeDimPlot,
                        xname =widgets.Text(
                            value="Energy",
                            placeholder ="xaxis",
                            description='Name of x axis:',
                            disabled=False,
                            continuous_update=False,
                            style = {'description_width': 'initial'}),
                        yname =widgets.Text(
                            value="Temperature",
                            placeholder ="yaxis",
                            description='Name of y axis:',
                            disabled=False,
                            continuous_update=False,
                            style = {'description_width': 'initial'}),
                        zname =widgets.Text(
                            value="Normalized EXAFS intensity",
                            placeholder ="zaxis",
                            description='Name of z axis:',
                            disabled=False,
                            continuous_update=False,
                            style = {'description_width': 'initial'}),
                        title =widgets.Text(
                            value="Evolution of edge with temperature",
                            placeholder ="3D plot",
                            description='Title:',
                            disabled=False,
                            continuous_update=False,
                            style = {'description_width': 'initial'}),
                        dist=widgets.IntSlider(
                            value=10,
                            min=0,
                            max=50,
                            step=1,
                            description='Distance:',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='d',
                            style = {'description_width': 'initial'}),
                        elev=widgets.IntSlider(
                            value=45,
                            min=0,
                            max=90,
                            step=1,
                            description='Elevation:',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='d',
                            style = {'description_width': 'initial'}),
                        azim=widgets.IntSlider(
                            value=285,
                            min=0,
                            max=360,
                            step=1,
                            description='Azimuthal:',
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='d',
                            style = {'description_width': 'initial'}),
                        cmapstyle = widgets.Dropdown(
                            options = [("Viridis", plt.cm.viridis), ("Jet", plt.cm.jet), ("Plasma", plt.cm.plasma), ("Cividis", plt.cm.cividis), ("Magma", plt.cm.magma), ("Inferno", plt.cm.inferno)],
                            description = 'Select the style:',
                            continuous_update=False,
                            disabled=False,
                            style = {'description_width': 'initial'}),
                        interval = widgets.FloatRangeSlider(
                                min=self.NewEnergyColumn[0],
                                value = [self.NewEnergyColumn[-2], self.NewEnergyColumn[-1]],
                                max = self.NewEnergyColumn[-1],
                                step = self.InterpolStep,
                                description='Energy range (eV):',
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='.2f',
                                style = {'description_width': 'initial'},
                                layout = Layout(width='50%', height='40px')))
                WidgetList3D = widgets.VBox([widgets.HBox(List3D.children[:3]), widgets.HBox(List3D.children[3:6]), widgets.HBox(List3D.children[6:9]), List3D.children[-1]])
                display(WidgetList3D)

            except (AttributeError, KeyError):
                plt.close()
                print(f"Wrong dataset and column combination !")
            except PermissionError:
                plt.close()
                print(f"Figure with same name opened in another program.")

        elif len(SpecNumber) == 0:
            print("Select more datatsets.")

        elif CheckPlot == "3D" and len(SpecNumber) < 2:
            print("Select more datatsets.")

    #Logbook interactive function
    def PrintLogbook(self, LogName, LogBool, column, value):
        """Allows one to filter multiple logbook columns by specific values"""
        
        #work on filtering values
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        try:
            value = int(value)
        except ValueError:
            value = value

        #Show logbook
        if not LogBool:
            global ThisLogbook
            try:
                Logbook = pd.read_excel(LogName)
                ButtonFilterLogbook = Button(
                    description="Add a filter",
                    layout=Layout(width='15%', height='35px'))
                ButtonAssociateLogbook = Button(
                    description="Associate Logbook entry to classes",
                    layout=Layout(width='25%', height='35px'))
                display(widgets.HBox((ButtonFilterLogbook, ButtonAssociateLogbook)))

                @ButtonFilterLogbook.on_click
                def ActionFilterLogbook(selfbutton):
                    clear_output(True)
                    global ThisLogbook
                    try:
                        global ThisLogbook
                        filt = ThisLogbook[column] == value
                        ThisLogbook = ThisLogbook[filt]
                        display(ThisLogbook)
                    except NameError:
                        try:
                            ThisLogbook = Logbook
                            filt = ThisLogbook[column] == value
                            ThisLogbook = ThisLogbook[filt]
                            display(ThisLogbook)
                        except:
                            print("Wrong Logbook Name")
                    except KeyError:
                        print("Wrong column value")

                @ButtonAssociateLogbook.on_click
                def ActionAssociateLogbook(selfbutton):
                    Logbook = pd.read_excel(LogName)

                    for items in Logbook.iterrows():
                        if "scan_" in items[1].Name:
                            namelog = items[1].Name.split("scan_")[1]

                            for C in self.ClassList:
                                nameclass = C.Name.split("Dataset_")[1]
                                if namelog == nameclass:
                                    try :
                                        setattr(C, "LogbookEntry", items[1])
                                        print(f"The logbook has been correctly associated for {C.Name}.")
                                        C.pickle()
                                    except:
                                        print(f"The logbook has been correctly associated for {C.Name}, but could not be pickled, i.e. it will not be saved after this working session.\n")

                        else:
                            namelog = items[1].Name

                            for C in self.ClassList:
                                nameclass = C.Name.split("Dataset_")[1]
                                if namelog == nameclass:
                                    try :
                                        setattr(C, "LogbookEntry", items[1])
                                        print(f"The logbook has been correctly associated for {C.Name}.")
                                        C.pickle()
                                    except:
                                        print(f"The logbook has been correctly associated for {C.Name}, but could not be pickled, i.e. it will not be saved after this working session.\n")

                                else:
                                    print("The logbook entries and datasets could not be associated. Please refer to readme for guidelines on how to name your data.")

                            # except ValueError:
                            #     print("""This routine assumes that the name of each dataset is stored in a \"Name\" column.\n
                            #         The names can be the same name as the datasets given in entry to the program,\n
                            #         In this case, the names must be possible to convert to intergers.\n
                            #         Otherwise, the names can be preceded of \"scan_\", followed by the dataset number.\n
                            #         E.g, we have a file \"215215.txt\" in entry, and in the logbook, its name is either 215215 or scan_215215.""")

            except:
                print("Logbook not available.")

            try:
                display(ThisLogbook)
            except NameError:
                try:
                    display(Logbook)
                except:
                    print("Wrong name")


        else:
            try: 
                del ThisLogbook
            except:
                pass
            print("The logbook has been reset.")
            clear_output(True)


    #All handler functions
    def NameHandler(self, change):
        """Handles changes on the widget used for the definition of the datafolder's name"""
        if (change.new == True):
            self.ListWidgetsInit.children[0].disabled = True
            self.ListWidgetsInit.children[2].disabled = False

        elif (change.new == False):
            self.ListWidgetsInit.children[0].disabled = False
            self.ListWidgetsInit.children[2].disabled = True

    def CreateHandler(self, change):
        """Handles changes on the widget used for the creation of subfolders"""

        if (change.new == True):
            for w in self.ListWidgetsInit.children[3:7]:
                w.disabled = False
            self.ListWidgetsInit.children[1].disabled = True
            self.ListWidgetsInit.children[9].disabled = False
            self.ListWidgetsInit.children[10].disabled = False

        elif (change.new == False):
            for w in self.ListWidgetsInit.children[3:7]:
                w.disabled = True
            self.ListWidgetsInit.children[1].disabled = False
            self.ListWidgetsInit.children[9].disabled = True
            self.ListWidgetsInit.children[10].disabled = True

    def MarkerHandler(self, change):
        if (change.new == True):
            for w in self.ListWidgetsInit.children[7:9]:
                w.disabled = False  
        if (change.new == False):
            for w in self.ListWidgetsInit.children[7:9]:
                w.disabled = True

    def DeleteHandler(self, change):
        """Handles changes on the widget used for the deletrion of previous work"""

        if (change.new == False):
            self.ListWidgetsInit.children[10].disabled = False
        elif (change.new == True):
            self.ListWidgetsInit.children[10].disabled = True       

    def WorkHandler(self, change):
        """Handles changes on the widget used for marking the beginning of data treatment"""
        if (change.new == True):
            for w in self.ListWidgetsInit.children[:10]:
                w.disabled = True
        elif (change.new == False):
            for w in self.ListWidgetsInit.children[1:7]:
                w.disabled = False
            self.ListWidgetsInit.children[9].disabled = False

    def ShowDataHandler(self, change):
        """Handles changes on the widget used to decide whether or not we show the data in the visualization tab."""

        if (change.new == True):
            self.ListData.children[0].disabled = True
            self.ListData.children[1].disabled = True
        elif (change.new == False):
            self.ListData.children[0].disabled = False
            self.ListData.children[1].disabled = False   

    def ReduceBoolHandler(self, change):
        """Handles changes on the widget used to decide whether or not we start the reduction in the reduction tab."""
        if self.ListTabReduceMethod.children[0].value != "Splines":
            if (change.new == True):
                for w in self.ListTabReduceMethod.children[:3]:
                    w.disabled = True
            elif (change.new == False):
                for w in self.ListTabReduceMethod.children[:3]:
                    w.disabled = False

        elif self.ListTabReduceMethod.children[0].value == "Splines":
            if (change.new == True):
                for w in [self.ListTabReduceMethod.children[0], self.ListTabReduceMethod.children[2]]:
                    w.disabled = True
            elif (change.new == False):
                for w in self.ListTabReduceMethod.children[:3]:
                    w.disabled = False

    def MergeBoolHandler(self, change):
        """Handles changes on the widget used to decide whether or not we merge the energies in the treatment tab."""

        if (change.new == True):
            for w in self.ListMergeEnergies.children[0:5]:
                w.disabled = True
        elif (change.new == False):
            for w in self.ListMergeEnergies.children[0:5]:
                w.disabled = False

    def ErrorExtractionHandler(self, change):
        """Handles changes on the widget used to decide whether or not we merge the energies in the treatment tab."""

        if (change.new == True):
            for w in self.ListErrors.children[0:7]:
                w.disabled = True
        elif (change.new == False):
            for w in self.ListErrors.children[0:7]:
                w.disabled = False

    def TreatmentBoolHandler(self, change):
        """Handles changes on the widget used to decide whether or not we start the data treatment in the treatment tab."""

        if (change.new == True):
            self.TabTreatment.children[0].disabled = True
        elif (change.new == False):
            self.TabTreatment.children[0].disabled = False

    def FitHandler(self, change):
        """Handles changes on the widget used to pick the dataframe and spectra during the fitting routine."""

        if (change.new == True):
            self.ListFit.children[0].disabled = True
            self.ListFit.children[1].disabled = True
        elif (change.new == False):
            self.ListFit.children[0].disabled = False
            self.ListFit.children[1].disabled = False 

    def ModelHandler(self, change):
        """Handles changes on the widget list after fixing the fitting routine."""

        if (change.new == True):
            for w in self.ListModel.children[:6]:
                w.disabled = True
            for w in self.ListModel.children[7:10]:
                w.disabled = True
        elif (change.new == False):
            for w in self.ListModel.children[:6]:
                w.disabled = False
            for w in self.ListModel.children[7:10]:
                w.disabled = False

    def ModelDegreeHandler(self, change):
        """Handles changes on the widget used to pick the degree of the polynomail background in the fitting routine."""
        if (change.new == PolynomialModel):
            self.ListModel.children[6].disabled = False
        elif (change.new != PolynomialModel):
            self.ListModel.children[6].disabled = True


    def ParamVictoreenHandlerSingle(self, change):
        """Handles changes on the widgets used to pick hte value of the initial parameter of the 1 Victoreen function"""
        if (change.new == "Victoreen"):
            self.ListReduceSingleSpline.children[4].disabled = False
            self.ListReduceSingleSpline.children[5].disabled = False

        elif (change.new != "Victoreen"):
            self.ListReduceSingleSpline.children[4].disabled = True
            self.ListReduceSingleSpline.children[5].disabled = True

    def ParamVictoreenHandler1(self, change):
        """Handles changes on the widgets used to pick hte value of the initial parameter of the 1 Victoreen function"""
        if (change.new == "Victoreen"):
            self.ListReduceSplines.children[5].disabled = False
            self.ListReduceSplines.children[6].disabled = False

        elif (change.new != "Victoreen"):
            self.ListReduceSplines.children[5].disabled = True
            self.ListReduceSplines.children[6].disabled = True

    def ParamVictoreenHandler2(self, change):
        """Handles changes on the widgets used to pick hte value of the initial parameter of the 1 Victoreen function"""
        if (change.new == "Victoreen"):
            self.ListReduceSplines.children[7].disabled = False
            self.ListReduceSplines.children[8].disabled = False

        elif (change.new != "Victoreen"):
            self.ListReduceSplines.children[7].disabled = True
            self.ListReduceSplines.children[8].disabled = True

    """Additional functions"""
    def Victoreen(self, x, A, B):
        """Victoreen function"""        
        return A*x**(-3) + B*x**(-4)