from ..mdb import Mdb

import types

class PyEcoreMdb(Mdb):
    def __init__(self,root,metamodelRegistry):#must be the original meta model registry and allow for modifications
        super().__init__()
        self.root = root
        self.metamodelRegistry = metamodelRegistry
    
    def Root(self):
        return self.root
    
    def Metamodels(self):
        return [(p.eClass if(isinstance(p,types.ModuleType)) else p) for p in self.metamodelRegistry.values()]
            
    def AddMetamodel(self,name,metamodel): #name is neglegted since the namespace URI is the identifier in pyecore
        self.metamodelRegistry[metamodel.nsURI] = metamodel #metamodel is expected to be a EPackage
        
    def RemoveMetamodel(self,name,metamodel): #name is neglegted since the namespace URI is the identifier in pyecore
        self.metamodelRegistry.pop(metamodel.nsURI)
        
    def GetMetamodel(self,name):
        package = self.metamodelRegistry[name]
        if(isinstance(package,types.ModuleType)):
            #this happens for metamodels loaded by generated python code
            #in this case we must create a copy as a psydo EPackge
            package = package.eClass
        return package