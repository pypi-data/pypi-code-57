from pyOpenRPA.Robot import UIDesktop
import os
import time # Time wait operations
from . import ConnectorExceptions # Exceptions classes
from . import Connector
from . import Processor # Module for process some functions on thr RDP
# Main function
def RobotRDPActive(inGSettings):
    # inGSettings = {
    # ... "RobotRDPActive": {} ...
    # }
    lL = inGSettings["Logger"] #Logger alias
    Processor.gSettings = inGSettings  # Set gSettings in processor module
    mGSettingsRDPActiveDict = inGSettings["RobotRDPActive"] # Get configuration from global dict settings
    # Global error handler
    try:
        ######## Init the RDP List
        for lRDPSessionKeyStrItem in mGSettingsRDPActiveDict["RDPList"]:
            lConfigurationItem = mGSettingsRDPActiveDict["RDPList"][lRDPSessionKeyStrItem]
            lConfigurationItem["SessionIsWindowExistBool"] = False  # Flag that session is not started
            lConfigurationItem["SessionIsWindowResponsibleBool"] = False  # Flag that session is not started
            lConfigurationItem["SessionHex"] = " 77777sdfsdf77777dsfdfsf77777777"  # Flag that session is not started
        ##########
        # Run monitor - main loop
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        inGlobalDict = mGSettingsRDPActiveDict # Compatibility
        inListUpdateTimeout = 1 # Compatibility
        lFlagWhile = True
        lResponsibilityCheckLastSec = time.time()  # Get current time for check interval
        while lFlagWhile:
            try:
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Check RDP window is OK - reconnect if connection was lost
                lUIOSelectorList = []
                lRDPConfigurationDictList = []
                # Prepare selectors list for check
                for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                    lItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                    lRDPConfigurationDictList.append(lItem) # Add RDP Configuration in list
                    lUIOSelectorList.append([{"title_re": f"{lItem['SessionHex']}.*", "backend": "win32"}])
                # Run wait command
                lRDPDissappearList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List(lUIOSelectorList, inListUpdateTimeout)
                for lItem in lRDPDissappearList: # Reconnect if connection was lost
                    lRDPConfigurationDict = lRDPConfigurationDictList[lItem] # Get RDP Configuration list
                    lRDPConfigurationDict["SessionIsWindowExistBool"] = False  # Set flag that session is disconnected
                    # Check if RDP window is not ignored
                    if not lRDPConfigurationDict["SessionIsIgnoredBool"]:
                        try:
                            Connector.Session(lRDPConfigurationDict, inScreenSize550x350Bool = True)
                            lRDPConfigurationDict["SessionIsWindowExistBool"] = True  # Flag that session is started
                            if lL: lL.info(f"SessionHex: {str(lRDPConfigurationDict['SessionHex'])}:: Session has been initialized!")  #Logging
                        # catch ConnectorExceptions.SessionWindowNotExistError
                        except ConnectorExceptions.SessionWindowNotExistError as e:
                            lRDPConfigurationDict["SessionIsWindowExistBool"] = False  # Set flag that session is disconnected
                            if lL: lL.warning(f"SessionHex: {str(lRDPConfigurationDict['SessionHex'])}:: Session is not exist!")  #Logging
                        # general exceptions
                        except Exception as e:
                            if lL: lL.exception(f"!!! ATTENTION !!! Unrecognized error")  #Logging
                            pass
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Safe turn off the - no need because of Orchestrator control
                #if inGlobalDict.get("OrchestratorToRobotResetStorage", {}).get("SafeTurnOff", False):
                #    lFlagWhile = False
                #    # Set status disconnected for all RDP List
                #    for lItem in inGlobalDict["RDPList"]:
                #        lItem["SessionIsWindowExistBool"] = False
                #        lItem["SessionIsWindowResponsibleBool"] = False
                #    # Kill all RDP sessions
                #    os.system('taskkill /F /im mstsc.exe')
                #    # Return from function
                #    return
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                Connector.SystemRDPWarningClickOk() # Click all warning messages
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Check if RDP session is full screen (if is not ignored)
                if inGlobalDict["FullScreenRDPSessionKeyStr"] is not None:
                    lRDPSessionKeyStr = inGlobalDict["FullScreenRDPSessionKeyStr"] # Get the RDPSessionKeyStr
                    if lRDPSessionKeyStr in inGlobalDict["RDPList"]: # Session Key is in dict
                        lRDPConfigurationDict = inGlobalDict["RDPList"][lRDPSessionKeyStr]
                        #if not lRDPConfigurationDict["SessionIsIgnoredBool"]: # Session is not ignored
                        # Check if full screen
                        lIsFullScreenBool = Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDict["SessionHex"])
                        if not lIsFullScreenBool: # If not the full screen
                            # Check all RDP window and minimize it
                            for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                                lRDPConfigurationDictItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                                if Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]):
                                    Connector.SessionScreenSize_X_Y_W_H(inSessionHex=lRDPConfigurationDictItem["SessionHex"], inXInt=10, inYInt=10,
                                                              inWInt=550,
                                                              inHInt=350)  # Prepare little window
                            # Set full screen for new window
                            Connector.SessionScreenFull(inSessionHex=lRDPConfigurationDict["SessionHex"], inLogger= inGSettings["Logger"], inRDPConfigurationItem=inGlobalDict["RDPList"][lRDPSessionKeyStrItem])
                else:
                    # Check all RDP window and minimize it
                    for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                        lRDPConfigurationDictItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                        if Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]) or Connector.SessionIsMinimizedScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]): # If window is minimized - restore # if window in full screen - resize
                            Connector.SessionScreenSize_X_Y_W_H(inSessionHex=lRDPConfigurationDictItem["SessionHex"],
                                                                inXInt=10, inYInt=10,
                                                                inWInt=550,
                                                                inHInt=350)  # Prepare little window
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Iterate the activity list in robot RDP active
                lActivityListNew = []
                lActivityListOld = inGlobalDict["ActivityList"]
                inGlobalDict["ActivityList"] = []
                for lActivityItem in lActivityListOld:
                    lSubmoduleFunctionName = lActivityItem["DefNameStr"]
                    if lSubmoduleFunctionName in dir(Processor):
                        lActivityItemResult = None # init the variable
                        try: # try to run function from Processor.py
                            lActivityItemResult = getattr(Processor, lSubmoduleFunctionName)(
                                *lActivityItem["ArgList"], **lActivityItem["ArgDict"])
                        except Exception as e:
                            if lL: lL.exception(f"RDP::main: Exception when run def in processor.py - activity will be ignored. Activity item: {lActivityItem}")  #Logging
                            lActivityItemResult = True # True - clear from repeat list
                        lActivityItemResultType = type(lActivityItemResult)
                        # Check if Result is bool
                        if lActivityItemResultType is bool:
                            if not lActivityItemResult:
                                # Activity is not done - add to list (retry in future)
                                lActivityListNew.append(lActivityItem)
                inGlobalDict["ActivityList"] = lActivityListNew  # Override the value
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            except RuntimeError as e:
                # case noGUI error passed - do nothing
                if lL: lL.warning(f"Host session has lost the GUI")  #Logging
            finally:
                # Wait for the next iteration
                time.sleep(0.7)
        # Scheduler.Scheduler(mGSettingsRDPActiveDict["Scheduler"])  # Init & Run Scheduler TODO remake in processor list
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #Monitor.Monitor(mGSettingsRDPActiveDict, 1)
    except Exception as e:
        if lL: lL.exception(f"!!! ATTENTION !!! Global error handler - look at code")  #Logging