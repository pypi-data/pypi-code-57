import datetime
import http.client
import json
import pdb
import os
import sys
import subprocess
import importlib
import psutil
#Input arg
#       [
#           {
#               "Type": <RemoteMachineProcessingRun>,
#               host: <localhost>,
#               port: <port>,
#               bodyObject: <object dict, int, str, list>
#           },
#           {
#               "Type": "CMDStart",
#				"Command": ""
#           },
#           {
#               "Type": "OrchestratorRestart"
#           },
#           {
#               "Type": "GlobalDictKeyListValueSet",
#               "KeyList": ["key1","key2",...],
#               "Value": <List, Dict, String, int>
#           },
#           {
#               "Type": "GlobalDictKeyListValueAppend",
#               "KeyList": ["key1","key2",...],
#               "Value": <List, Dict, String, int>
#           },
#           {
#               "Type": "GlobalDictKeyListValueOperator+",
#               "KeyList": ["key1","key2",...],
#               "Value": <List, Dict, String, int>
#           },
#           {
#               "Type": "GlobalDictKeyListValueGet",
#               "KeyList": ["key1","key2",...]
#           },
#           {
#               "Type":"ProcessStart",
#               "Path":"",
#               "ArgList":[]
#           },
#           {
#               "Type":"ProcessStartIfTurnedOff",
#               "CheckTaskName":"", #Check if current task name is not active (then start process),
#               "Path":"",
#               "ArgList":[]
#           },
#           {
#               "Type":"ProcessStop",
#               "Name":"",
#               "FlagForce":True,
#               "User":"" #Empty - all users, user or %username%
#           },
#           {
#               "Type":"PythonStart",
#               "ModuleName":"",
#               "FunctionName":"",
#               "ArgList":[],
#               "ArgDict":{}
#           },
#           {
#               "Type":"WindowsLogon",
#               "Domain":"",
#               "User":"",
#               "Password":""
#               # Return "Result": True - user is logged on, False - user is not logged on
#           }
#       ]
##################################
#Output result
# <input arg> with attributes:
# "DateTimeUTCStringStart"
# "DateTimeUTCStringStop"
# "Result"
gSettingsDict = None
def Activity(inActivity):
    #Глобальная переменная - глобальный словарь унаследованный от Settings.py
    global gSettingsDict
    #Alias (compatibility)
    lItem = inActivity
    lCurrentDateTime = datetime.datetime.now()
    ###########################################################
    #Обработка запроса на отправку команды на удаленную машину
    ###########################################################
    if lItem["Type"]=="RemoteMachineProcessingRun":
        lHTTPConnection = http.client.HTTPConnection(lItem["host"], lItem["port"], timeout=5)
        try:
            lHTTPConnection.request("POST","/ProcessingRun",json.dumps(lItem["bodyObject"]))
        except Exception as e:
            #Объединение словарей
            lItem["Result"] = {"State":"disconnected","ExceptionString":str(e)}
        else:
            lHTTPResponse=lHTTPConnection.getresponse()
            lHTTPResponseByteArray=lHTTPResponse.read()
            lItem["Result"] = json.loads(lHTTPResponseByteArray.decode('utf8'))
    ###########################################################
    #Обработка команды CMDStart
    ###########################################################
    if lItem["Type"]=="CMDStart":
        lCMDCode="cmd /c "+lItem["Command"]
        subprocess.Popen(lCMDCode)
        lResultCMDRun=1#os.system(lCMDCode)
        lItem["Result"] = str(lResultCMDRun)
    ###########################################################
    #Обработка команды OrchestratorRestart
    ###########################################################
    if lItem["Type"]=="OrchestratorRestart":
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        lItem["Result"] = True
        sys.exit(0)
    ###########################################################
    #Обработка команды GlobalDictKeyListValueSet
    ###########################################################
    if lItem["Type"]=="GlobalDictKeyListValueSet":
        lDict = gSettingsDict
        for lItem2 in lItem["KeyList"][:-1]:
            #Check if key - value exists
            if lItem2 in lDict:
                pass
            else:
                lDict[lItem2]={}
            lDict=lDict[lItem2]
        #Set value
        lDict[lItem["KeyList"][-1]]=lItem["Value"]
        lItem["Result"] = True
    ###########################################################
    # Обработка команды GlobalDictKeyListValueAppend
    ###########################################################
    if lItem["Type"] == "GlobalDictKeyListValueAppend":
        lDict = gSettingsDict
        for lItem2 in lItem["KeyList"][:-1]:
            # Check if key - value exists
            if lItem2 in lDict:
                pass
            else:
                lDict[lItem2] = {}
            lDict = lDict[lItem2]
        # Set value
        lDict[lItem["KeyList"][-1]].append(lItem["Value"])
        lItem["Result"] = True
    ###########################################################
    # Обработка команды GlobalDictKeyListValueOperator+
    ###########################################################
    if lItem["Type"] == "GlobalDictKeyListValueOperator+":
        lDict = gSettingsDict
        for lItem2 in lItem["KeyList"][:-1]:
            # Check if key - value exists
            if lItem2 in lDict:
                pass
            else:
                lDict[lItem2] = {}
            lDict = lDict[lItem2]
        # Set value
        lDict[lItem["KeyList"][-1]]+=lItem["Value"]
        lItem["Result"] = True
    ###########################################################
    #Обработка команды GlobalDictKeyListValueGet
    ###########################################################
    if lItem["Type"]=="GlobalDictKeyListValueGet":
        lDict = gSettingsDict
        for lItem2 in lItem["KeyList"][:-1]:
            #Check if key - value exists
            if lItem2 in lDict:
                pass
            else:
                lDict[lItem2]={}
            lDict=lDict[lItem2]
        #Return value
        lItem["Result"]=lDict.get(lItem["KeyList"][-1],None)
    #####################################
    #ProcessStart
    #####################################
    if lItem["Type"]=="ProcessStart":
        #Вид активности - запуск процесса
        #Запись в массив отработанных активностей
        #Запустить процесс
        lItemArgs=[lItem["Path"]]
        lItemArgs.extend(lItem["ArgList"])
        subprocess.Popen(lItemArgs,shell=True)
    #####################################
    #ProcessStartIfTurnedOff
    #####################################
    if lItem["Type"]=="ProcessStartIfTurnedOff":
        #Check if process running
        #remove .exe from Taskname if exists
        lCheckTaskName = lItem["CheckTaskName"]
        if len(lCheckTaskName)>4:
            if lCheckTaskName[-4:].upper() != ".EXE":
                lCheckTaskName = lCheckTaskName+".exe"
        else:
            lCheckTaskName = lCheckTaskName+".exe"
        #Check if process exist
        if not CheckIfProcessRunning(lCheckTaskName):
            #Вид активности - запуск процесса
            #Запись в массив отработанных активностей
            #Запустить процесс
            lItemArgs=[lItem["Path"]]
            lItemArgs.extend(lItem["ArgList"])
            subprocess.Popen(lItemArgs,shell=True)
    #################################
    #ProcessStop
    #################################
    if lItem["Type"]=="ProcessStop":
        #Вид активности - остановка процесса
        #часовой пояс пока не учитываем
        #Сформировать команду на завершение
        lActivityCloseCommand='taskkill /im '+lItem["Name"]
        #TODO Сделать безопасную обработку,если параметра нет в конфигурации
        if lItem.get('FlagForce',False):
            lActivityCloseCommand+=" /F"
        #Завершить процессы только текущего пользоваиеля
        if lItem.get('User',"")!="":
            lActivityCloseCommand+=f' /fi "username eq {lItem["User"]}"'
        #Завершить процесс
        os.system(lActivityCloseCommand)
    #################################
    #PythonStart
    #################################
    if lItem["Type"]=="PythonStart":
        try:
            #Подключить модуль для вызова
            lModule=importlib.import_module(lItem["ModuleName"])
            #Найти функцию
            lFunction=getattr(lModule,lItem["FunctionName"])
            lItem["Result"]=lFunction(*lItem.get("ArgList",[]),**lItem.get("ArgDict",{}))
        except Exception as e:
            logging.exception("Loop activity error: module/function not founded")
    #################################
    # Windows logon
    #################################
    if lItem["Type"] == "WindowsLogon":
        import win32security
        try:
            hUser = win32security.LogonUser(
                lItem["User"],
                lItem["Domain"],
                lItem["Password"],
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT
            )
        except win32security.error:
            lItem["Result"] = False
        else:
            lItem["Result"] = True
    ###################################
    #Вернуть результат
    return lItem

def ActivityListOrDict(inActivityListOrDict):
    #Check arg type (list or dict)
    if type(inActivityListOrDict)==list:
        #List activity
        lResult=[]
        for lItem in inActivityListOrDict:
            lResult.append(Activity(lItem))
        return lResult
    if type(inActivityListOrDict)==dict:
        #Dict activity
        return Activity(inActivityListOrDict)
        
def CheckIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;