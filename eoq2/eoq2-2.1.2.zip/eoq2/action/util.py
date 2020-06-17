'''
 2019 Bjoern Annighoefer
'''

from .call import CallStatus
from ..command.command import Cmp,Ubs
from ..query.query import His
from ..event.event import EvtTypes

import time

def ShowProgress(progress):
    print('Total progress: %d%%'%(int(progress)))
    return


class CallObserver:
    def __init__(self,domain,forwardOutput=False):
        self.domain = domain
        self.callId = 0  
        self.forwardOutput = forwardOutput
        self.callFinished = False
        self.gotReturnValue = False
        self.callReturnValue = None
        self.callStatus = None
        
        #observe the domain
        self.domain.Observe(self.OnCallEvent,context=self)
        
    def __del__(self):
        self.domain.Unobserve(self.OnCallEvent,context=self)
        
    def WaitOnCall(self,action,args,opts):
        cmd = Cmp().Asc(action,args,opts).Obs('*',His(0))
        res = self.domain.Do(cmd)
        self.callId = res[0]
        
    def CleanUp(self):
        self.domain.Do(Ubs('*',str(self.callId)))
        
    def IsCallFinished(self):
        return self.callFinished
    
    def CallIsRunning(self):
        return not self.callFinished
    
    def GetCallResult(self):
        return (self.callStatus,self.callReturnValue)
        
    def OnCallEvent(self,evts,source):
        for evt in evts: #the event handler always gets a list of events.
            if(evt.evt == EvtTypes.CST and evt.a[0]==self.callId):
                if(CallStatus.FIN == evt.a[1]):
                    self.callStatus = evt.a[1]
                    if(self.gotReturnValue):
                        self.callFinished = True #set only finished if return value was also received
                elif(CallStatus.ABO == evt.a[1] or CallStatus.ERR == evt.a[1]):
                    self.callStatus = evt.a[1]
                    self.callFinished = True
            elif(evt.evt == EvtTypes.CVA and evt.a[0]==self.callId):
                self.callReturnValue = evt.a[1]
                self.gotReturnValue = True
                if(CallStatus.FIN == self.callStatus):
                    self.callFinished = True
            elif(self.forwardOutput and evt.evt == EvtTypes.OUP and evt.a[0]==self.callId):
                self.domain.callManager.AddCallOutput(evt.a[1],evt.a[2])
                  

def AscAndWait(domain,action,args=[],opts=[],forwardOutput=False):
    observer = CallObserver(domain,forwardOutput=forwardOutput)
    observer.WaitOnCall(action,args,opts)
    #main wait loop
    while(observer.CallIsRunning()):
        time.sleep(0.1) #waste time until call is ready
    
    observer.CleanUp()
    
    return observer.GetCallResult()
    