import subprocess
import json
import datetime
import time
import codecs
import os
import signal
import sys #Get input argument
import pdb
from . import Server
from . import Timer
from . import Processor

#from .Settings import Settings
import importlib
from importlib import util
import threading # Multi-threading for RobotRDPActive
from .RobotRDPActive import RobotRDPActive #Start robot rdp active
import uuid # Generate uuid

#Единый глобальный словарь (За основу взять из Settings.py)
global gSettingsDict
#Call Settings function from argv[1] file
################################################
lSubmoduleFunctionName = "Settings"
lFileFullPath = sys.argv[1]
lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
gSettingsDict = None
if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
    # Run SettingUpdate function in submodule
    gSettingsDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
#################################################
#mGlobalDict = Settings.Settings(sys.argv[1])
#Logger alias
lL = gSettingsDict["Logger"]

if lL: lL.info("Link the gSettings in submodules")  #Logging
Processor.gSettingsDict = gSettingsDict
Timer.gSettingsDict = gSettingsDict
Timer.Processor.gSettingsDict = gSettingsDict
Server.gSettingsDict = gSettingsDict
Server.Processor.gSettingsDict = gSettingsDict

#Инициализация настроечных параметров
lDaemonLoopSeconds=gSettingsDict["Scheduler"]["ActivityTimeCheckLoopSeconds"]
lDaemonActivityLogDict={} #Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
lDaemonLastDateTime=datetime.datetime.now()

#Инициализация сервера
lThreadServer = Server.RobotDaemonServer("ServerThread", gSettingsDict)
lThreadServer.start()
if lL: lL.info("Web server has been started")  #Logging

# Init the RobotRDPActive in another thread
lRobotRDPActiveThread = threading.Thread(target= RobotRDPActive.RobotRDPActive, kwargs={"inGSettings":gSettingsDict})
lRobotRDPActiveThread.daemon = True # Run the thread in daemon mode.
lRobotRDPActiveThread.start() # Start the thread execution.
if lL: lL.info("Robot RDP active has been started")  #Logging

# Orchestrator start activity
if lL: lL.info("Orchestrator start activity run")  #Logging
for lActivityItem in gSettingsDict["OrchestratorStart"]["ActivityList"]:
    Processor.ActivityListOrDict(lActivityItem)

if lL: lL.info("Scheduler loop start")  #Logging
gDaemonActivityLogDictRefreshSecInt = 10 # The second period for clear lDaemonActivityLogDict from old items
gDaemonActivityLogDictLastTime = time.time() # The second perioad for clean lDaemonActivityLogDict from old items
while True:
    lCurrentDateTime = datetime.datetime.now()
    #Циклический обход правил
    lFlagSearchActivityType=True
    # Periodically clear the lDaemonActivityLogDict
    if time.time()-gDaemonActivityLogDictLastTime>=gDaemonActivityLogDictRefreshSecInt:
        gDaemonActivityLogDictLastTime = time.time() # Update the time
        for lIndex, lItem in enumerate(lDaemonActivityLogDict):
            if lItem["ActivityEndDateTime"] and lCurrentDateTime<=lItem["ActivityEndDateTime"]:
                pass
                # Activity is actual - do not delete now
            else: 
                # remove the activity - not actual
                lDaemonActivityLogDict.pop(lIndex,None)
    lIterationLastDateTime = lDaemonLastDateTime # Get current datetime before iterator (need for iterate all activities in loop)
    # Iterate throught the activity list
    for lIndex, lItem in enumerate(gSettingsDict["Scheduler"]["ActivityTimeList"]):
        # Prepare GUID of the activity
        lGUID = None
        if "GUID" in lItem and lItem["GUID"]:
            lGUID = lItem["GUID"]
        else:
            lGUID = str(uuid.uuid4())
            lItem["GUID"]=lGUID
        
        #Проверка дней недели, в рамках которых можно запускать активность
        lItemWeekdayList=lItem.get("WeekdayList", [0, 1, 2, 3, 4, 5, 6])
        if lCurrentDateTime.weekday() in lItemWeekdayList:
            if lFlagSearchActivityType:
                #######################################################################
                #Branch 1 - if has TimeHH:MM
                #######################################################################
                if "TimeHH:MM" in lItem:
                    #Вид активности - запуск процесса
                    #Сформировать временной штамп, относительно которого надо будет проверять время
                    #часовой пояс пока не учитываем
                    lActivityDateTime=datetime.datetime.strptime(lItem["TimeHH:MM"],"%H:%M")
                    lActivityDateTime=lActivityDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                    #Убедиться в том, что время наступило
                    if (
                            lActivityDateTime>=lDaemonLastDateTime and
                            lCurrentDateTime>=lActivityDateTime):
                        # Log info about activity
                        if lL: lL.info(f"Scheduler:: Activity is started. Scheduler item: {lItem}")  #Logging
                        # Do the activity
                        Processor.ActivityListOrDict(lItem["Activity"])
                        lIterationLastDateTime = datetime.datetime.now() # Set the new datetime for the new processor activity
                #######################################################################
                #Branch 2 - if TimeHH:MMStart, TimeHH:MMStop, ActivityIntervalSeconds
                #######################################################################
                if "TimeHH:MMStart" in lItem and "TimeHH:MMStop" in lItem and "ActivityIntervalSeconds" in lItem:
                    #Сформировать временной штамп, относительно которого надо будет проверять время
                    #часовой пояс пока не учитываем
                    lActivityDateTime=datetime.datetime.strptime(lItem["TimeHH:MMStart"],"%H:%M")
                    lActivityDateTime=lActivityDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                    lActivityTimeEndDateTime=datetime.datetime.strptime(lItem["TimeHH:MMStop"],"%H:%M")
                    lActivityTimeEndDateTime=lActivityTimeEndDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                    #Убедиться в том, что время наступило
                    if (
                            lCurrentDateTime<lActivityTimeEndDateTime and
                            lCurrentDateTime>=lActivityDateTime and
                            (lGUID,lActivityDateTime) not in lDaemonActivityLogDict):
                        #Запись в массив отработанных активностей
                        lDaemonActivityLogDict[(lGUID,lActivityDateTime)]={"ActivityStartDateTime":lCurrentDateTime, "ActivityEndDateTime":lActivityTimeEndDateTime}
                        #Запуск циклической процедуры
                        Timer.activityLoopStart(lItem["ActivityIntervalSeconds"], lActivityTimeEndDateTime, lItem["Activity"])
    lDaemonLastDateTime = lIterationLastDateTime # Set the new datetime for the new processor activity
    #Уснуть до следующего прогона
    time.sleep(lDaemonLoopSeconds)