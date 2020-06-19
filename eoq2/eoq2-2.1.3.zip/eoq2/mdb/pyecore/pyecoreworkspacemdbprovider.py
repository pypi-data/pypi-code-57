'''
 Workspace MDB Provider
 Bjoern Annighoefer 2019
'''

from ...util import NoLogging
from ...event import MsgEvt,ChgTypes,EvtTypes
from .pyecoremdb import PyEcoreMdb

from .workspacemdbmodel import Workspace,ModelResource,Directory,FileResourceTypesE,PathElementA,FileResourceA,XmlResource
from .xmlresourcemodel import Document,Element,Attribute

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EObject,EPackage

import os
import shutil
import glob
import xml.etree.ElementTree
import xml.dom.minidom
from timeit import default_timer
from threading import Timer
import traceback


import pyecore.behavior as behavior # We need to import the 'behavior' package

# Ugly global necessary for the path methods 
PROVIDER_INSTANCE = None


#Implement methods
@PathElementA.behavior
def actualPath(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetElementPath(self)
    return path

@PathElementA.behavior
def actualPathAbs(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetAbsElementPath(self)
    return path

@PathElementA.behavior
def actualPathCwd(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetElementPath(self)
    return path

# intended for saving changes for later, but file system changes must be checked imidiatly in order to prevent unwanted situations
# class WorkspaceChgTypes:
#     RESOURCE_ADD = "RESOURCE_ADD"
#     RESOURCE_MOV = "RESOURCE_MOV"
#     RESOURCE_DEL = "RESOURCE_DEL"
#     DIRECTORY_ADD = "DIRECTORY_ADD"
#     DIRECTORY_MOV = "DIRECTORY_MOV"
#     DIRECTORY_DEL = "DIRECTORY_DEL"
    
        
        
class PyEcoreWorkspaceMdbProvider():
    def __init__(self,baseDir,metaDir=['./.meta'],saveTimeout=10.0,logger=NoLogging(),autoload=True):
        super().__init__()
        
        self.baseDir = os.path.normpath(baseDir)
        self.baseDirAbs = os.path.join(os.getcwd(),self.baseDir)
        self.baseDirUri = URI(self.baseDir) 
        self.rset = ResourceSet()
        self.modelResourceLut = {} #a look-up table between eResources and ModelResource objects
        self.eResourceLut = {} #a look-up table between ModelResource and eResources objects
        self.metaDir = metaDir #the directory that contains model definitions
        
        self.logger = logger
        
        self.modelroot = Workspace(name='.') #clone behavior of the old localdomain
        self.lastPersistentPaths = {} # dir or resources -> path
        self.dirtyResources = [] #stores all modified resources, such that they can be saved 
        self.deletedResources = {} #stores all resources marked for deletion
        self.dirtyObjects = [] #stores all objects that have been modified in order to do not mark them twice
        self.saveTimeout = saveTimeout #This time is waited for any model modifications and than autosafe is called 
        self.saveTimer = None
        
        self.knownModelExtensions = ['ecore'] #this is used to identify the model files to be loaded. ecore files are known as model files by default.
        self.knownXmlExtensions = ['xml']
        
        self.valueCodec = None #is set during coupling
        self.domain = None #is set during coupling
        self.mdb = None #is created later
        
        if(autoload):
            self.Load()
            
        #register this as an singelton
        global PROVIDER_INSTANCE
        PROVIDER_INSTANCE = self
        
        
    def __del__(self):
        #make sure any changes are saved
        #self.logger.Info("Closing workspace MDB ...") #makes problems when main thread has ended already
        
        self.__StopDelayedSaving()
        self.__SaveAllDirtyResources()
        
        
        #self.logger.Info("ok")
        
    def GetMdb(self):
        return self.mdb
    
    def Load(self):
        self.logger.Info("Loading workspace MDB for %s (meta=%s)..."%(self.baseDir,self.metaDir))
        start = default_timer()
        self.__LoadMetaModels()
        self.__LoadResourceTree()
        end = default_timer()
        self.mdb = PyEcoreMdb(self.modelroot,self.rset.metamodel_registry)
        self.logger.Info("Workspace MDB ready after %f s"%(end-start))
    
    def CoupleWithDomain(self,domain,valueCodec):
        self.domain = domain
        self.valueCodec = valueCodec
        self.domain.Observe(self.OnChange,[EvtTypes.CHG])
        
    ''' sync model changes with workspace '''
        
    def OnChange(self,evts,src):
        for evt in evts:
            chg = evt
            ctype = chg.a[1]
            target = self.valueCodec.Dec(chg.a[2]) #reverse what the domain did to the element
            feature = chg.a[3]
            oldOwner = self.valueCodec.Dec(chg.a[6])
            
            if(isinstance(target,FileResourceA)):
                if(ctype==ChgTypes.SET and "name"==feature):
                    #rename action
                    newName = chg.a[4]
                    self.__RenameResource(target,newName)
                else: #handle any other resource change like an object change
                    self.__SetObjectDirty(target)
                    self.__SetObjectDirty(oldOwner)
            elif(isinstance(target,Directory)):
                #directories might be renamed or deleted or new resources/subdirs added or deleted
                if(ctype==ChgTypes.SET and "name"==feature ):
                    #resource renamed
                    newName = chg.a[4]
                    self.__RenameDirectory(target,newName)
                elif(ctype==ChgTypes.ADD and "resources"==feature):
                    #new resource
                    resource = self.valueCodec.Dec(chg.a[4])
                    if(oldOwner):
                        self.__MoveResource(resource)
                    else:
                        self.__AddResource(target,resource)
                elif(ctype==ChgTypes.REM and "resources"==feature):
                    #resource deleted
                    resource = self.valueCodec.Dec(chg.a[4])
                    self.__DeleteResource(resource)
                elif(ctype==ChgTypes.ADD and "subdirectories"==feature):
                    #new directory
                    directory = self.valueCodec.Dec(chg.a[4])
                    if(oldOwner):
                        self.__MoveDirectory(directory)
                    else:
                        self.__AddDirectory(target,directory)
                elif(ctype==ChgTypes.REM and "subdirectories"==feature):
                    #directory deleted
                    directory = self.valueCodec.Dec(chg.a[4])
                    self.__DeleteDirectory(directory)
            elif(isinstance(target,EObject)):
                self.__SetObjectDirty(target)
                self.__SetObjectDirty(oldOwner)
                
    ''' resource sync functions '''
       
    def __AddResource(self,dir,resource):
        if(dir): #otherwise there is no need to move the resource
            try:
                #move the file 
                newPath = self.GetAbsElementPath(resource)
                if(newPath): #if this is false, then the resource was added to a directory not attached to the workspace
                    #create placeholder file
                    open(newPath, 'w').close()
                    self.__SetLastPersistentPath(resource, newPath)
                    self.__SetResourceDirty(resource)
                    #update the pyecore URI
                    if(resource.type == FileResourceTypesE.MODEL):
                        eResource = self.rset.create_resource(newPath)
                        self.__LinkModelResourceAndEResource(resource,eResource)
                    #inform about action
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Added resource %s."%(newRelPath))
            except Exception as e:
                self.logger.Error("Failed to add resource: %s"%(str(e)))
                traceback.print_exc()            
                   
    def __RenameResource(self,resource,newName):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                try:
                #move the file 
                    newPath = os.path.join(filePath,newName)
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(resource)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Renamed resource %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to rename resource: %s"%(str(e)))
                    traceback.print_exc()
                
    def __MoveResource(self,resource):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath): #otherwise there is no need to move the resource
            oldPath = lastPersistentPath
            newPath = self.GetAbsElementPath(resource)
            if(newPath!=oldPath):
                try:
                    #move the file 
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(resource)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Moved resource %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to moved resource: %s"%(str(e)))
                    traceback.print_exc()
                
    def __DeleteResource(self,resource):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath):
            try: 
                oldPath = lastPersistentPath
                #delete resource
                os.remove(oldPath)
                self.__DeleteResourceOrDirectoryPath(resource)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                self.logger.Info("Deleted resource %s."%(oldRelPath))
            except Exception as e:
                self.logger.Info("Failed to delete resource %s."%(str(e)))
                traceback.print_exc()
                
    ''' directory sync functions '''
                
    def __AddDirectory(self,parent,directory):
        if(parent): #otherwise there is no need to move the resource
            try:
                newPath = self.GetAbsElementPath(directory)
                if(newPath): #if this is false, then the dir was added to a directory not attached to the workspace
                    #create new dir file
                    os.mkdir(newPath)
                    self.__SetLastPersistentPath(directory, newPath)
                    #recursively consider all contained resources and subdirs 
                    for res in directory.resources:
                        self.__AddResource(directory, res)
                    for subdir in directory.subdirectories:
                        self.__AddDirectory(directory, subdir)
                    #inform about action
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Added directory %s."%(newRelPath))
            except Exception as e:
                self.logger.Error("Failed to add directory: %s"%(str(e)))
                traceback.print_exc() 
                
    
    def __RenameDirectory(self,directory,newName):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                try:
                    newPath = os.path.join(filePath,newName)
                    #create the new dir
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(directory)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Renamed directory %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to rename directory: %s"%(str(e)))
                    traceback.print_exc() 
                    
    def __MoveDirectory(self,directory):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath): #otherwise there is no need to move the directory
            oldPath = lastPersistentPath
            newPath = self.GetAbsElementPath(directory)
            if(newPath!=oldPath):
                try:
                    #move the directory 
                    shutil.move(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(directory)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Moved directory %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to move directory: %s"%(str(e)))
                    traceback.print_exc()
                
    def __DeleteDirectory(self,directory):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath):
            try: 
                oldPath = lastPersistentPath
                #delete resource
                shutil.rmtree(oldPath)
                self.__DeleteResourceOrDirectoryPath(directory)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                self.logger.Info("Deleted directory %s."%(oldRelPath))
            except Exception as e:
                self.logger.Info("Failed to delete directory %s."%(str(e)))
                traceback.print_exc()
                
    ''' Generic path functions '''
                
    def __RefreshResourceOrDirectoryPath(self,element):
        newPath = self.GetAbsElementPath(element)
        if(newPath):
            self.__SetLastPersistentPath(element, newPath)
            if(isinstance(element, ModelResource)):  
                #update the pyecore URI
                newUri = URI(newPath)
                eResource = self.__GetEResourceForModelResource(element)
                eResource.uri = newUri
            elif(isinstance(element, Directory)):
                #update contained elements
                for subres in element.resources:
                    self.__RefreshResourceOrDirectoryPath(subres)
                for subdir in element.subdirectories:
                    self.__RefreshResourceOrDirectoryPath(subdir)
                    
    def __DeleteResourceOrDirectoryPath(self,element):
        self.__DeleteLastPeristentPath(element)
        if(isinstance(element, FileResourceA)):  
            self.__SetResourceClean(element)
            if(element.type == FileResourceTypesE.MODEL):
                self.__UnlinkModelResourceAndEResource(element)
        elif(isinstance(element, Directory)):
            #update contained elements
            for subres in element.resources:
                self.__DeleteResourceOrDirectoryPath(subres)
            for subdir in element.subdirectories:
                self.__DeleteResourceOrDirectoryPath(subdir)
                
    def GetElementPath(self,directory):
        workspaceFound = False #indicates if the element is attached correctly somewhere below the root
        path = directory.name
        if(isinstance(directory,Workspace)):
            return path
        parent = directory.eContainer()
        while(isinstance(parent,Directory)):
            path = os.path.join(parent.name,path)
            if(isinstance(parent,Workspace)):
                workspaceFound = True
                break #exit because there should not be an element further down.
            parent = parent.eContainer()
        if(workspaceFound):
            return path
        else:
            return None
    
    def GetAbsElementPath(self,directory):
        path = self.GetElementPath(directory)
        if(path):
            return os.path.join(self.baseDirAbs,path)
        else:
            return None
     
    def __SetObjectDirty(self,obj):
        if(obj): 
            #find the resource object and mark it dirty
            if(obj in self.dirtyObjects):
                return #quit here if object is already marked as dirty.
            self.dirtyObjects.append(obj)
            resource = self.__GetResourceForObject(obj)
            self.__SetResourceDirty(resource)
       
    ''' Last persistent path functions '''     
    def __GetLastPersitentPath(self,dirOrResource):
        lastPersistentPath = None
        try:
            lastPersistentPath = self.lastPersistentPaths[dirOrResource]
        except KeyError:
            lastPersistentPath = None
        return lastPersistentPath
    
    def __SetLastPersistentPath(self,dirOrResource,lastPersistentPath):
        self.lastPersistentPaths[dirOrResource] = lastPersistentPath
        
    def __DeleteLastPeristentPath(self,dirOrResource):
        try:
            self.lastPersistentPaths.pop(dirOrResource)
        except:
            pass #fail silent if element does not has no path so far
    
    ''' Saving functions '''
    def __InitSave(self):
        #stop the current save action 
        self.__StopDelayedSaving()
        if(0<len(self.dirtyResources)):
            if(self.saveTimeout > 0):
                self.__StartDelayedSaving()
            else:
                self.__SaveAllDirtyResources() #skip threading for a 0 timeout
        
    
    def __StartDelayedSaving(self):
        self.saveTimer = Timer(self.saveTimeout,self.__DelayedSaving)
        self.saveTimer.start()
        
    def __StopDelayedSaving(self):
        if(self.saveTimer):
            self.saveTimer.cancel()
            self.saveTimer = None
            
    def __DelayedSaving(self):
        self.__SaveAllDirtyResources()
        self.saveTimer = None
        
    def __SaveAllDirtyResources(self):
        evts = []
        self.__ConnectAllEResources() #necessary for model resources
        for resource in self.dirtyResources:
            try:
                self.__SaveResource(resource)
                evts.append(MsgEvt("WorkspaceMdb","Saved %s."%(resource.name)))
            except Exception as e:
                evts.append(MsgEvt("WorkspaceMdb","Failed to save %s: %s"%(resource.name,str(e))))
                traceback.print_exc()
        self.__DisconnectAllEResources() #necessary for model resources

        self.dirtyResources.clear()
        self.dirtyObjects.clear()
        
        #notify observers
        self.domain.NotifyObservers(evts, self)
    
    
    ''' resource handling functions '''   
    def __SetResourceDirty(self,resource):
        if(resource and resource not in self.dirtyResources):
            self.dirtyResources.append(resource)
            self.__InitSave()
            
    def __SetResourceClean(self,resource):
        try:
            self.dirtyResources.remove(resource)
        except:
            pass #do nothing if the resource was never marked as dirty
 
    def __GetResourceForObject(self,obj):
        container = obj
        while container and not isinstance(container, FileResourceA):
            container = container.eContainer()
        return container
         
    def __LoadMetaModels(self):
        #look for existing meta models and load them on them
        for mp in self.metaDir:
            metadir = mp
            if(not os.path.isabs(mp)):
                metadir = os.path.join(self.baseDir,mp)
            searchString = os.path.join(metadir+'/*.ecore')
            modeldefinitions = glob.glob(searchString)
            for md in modeldefinitions:
                self.__LoadMetaModelResource(md)
        return
    
    def __LoadModelContents(self,resourceFile):
        resource = self.rset.get_resource(resourceFile)
        return list(resource.contents) #make a copy of the list contents
    
    def __LoadMetaModelResource(self,resourceFile):
        modelContents = self.__LoadModelContents(resourceFile)
        gcmRoot = modelContents[0]
        self.rset.metamodel_registry[gcmRoot.nsURI] = gcmRoot
        # register all possible subpackages
        for child in gcmRoot.eAllContents():
            if(isinstance(child,EPackage)):
                self.rset.metamodel_registry[child.nsURI] = child
        #remember the file extension, which is the file name (without extension) of the model file
        metaModelFileName = os.path.basename(resourceFile)
        modelExtension = os.path.splitext(metaModelFileName)[0]
        self.knownModelExtensions += [modelExtension]
        #return the root
        return modelContents
                        
            
    def __LoadResourceTree(self):
        (directories,modelfiles) = self.__ScanForFilesAndDirectories()
        
        #create directories (this includes empty ones)
        for dirpath in directories:
            directory = self.__GetOrCreateDir(dirpath)
        
        #create model files
        for modelfile in modelfiles:
            head,tail = os.path.split(modelfile)
            directory = self.__GetOrCreateDir(head)
            resource = self.__LoadResource(modelfile)
            if(resource): #check if loading succeeded
                resource.name = tail
                directory.resources.add(resource)
    
    
    def __GetOrCreateDir(self,path):
        relPath = os.path.relpath(path, self.baseDirAbs)
        directory = self.modelroot
        if(relPath and relPath != '.'): #only proceed for non empty strings
            segments = relPath.split(os.path.sep)
            for segment in segments: 
                subdirexists = False
                for subdir in directory.subdirectories:
                    if(subdir.name == segment):
                        directory = subdir
                        subdirexists = True
                        break
                if(not subdirexists):
                    newsubdir = Directory(name=segment)
                    self.__SetLastPersistentPath(newsubdir, path)
                    directory.subdirectories.add(newsubdir)
                    directory = newsubdir
        return directory
    
    def __ScanForFilesAndDirectories(self):
        directories = []
        modelFiles = []
        for root, dirs, files in os.walk(self.baseDirAbs, topdown=True):
            for d in dirs:
#                 relativeRoot = os.path.relpath(root, self.baseDir)
                path = os.path.join(root,d)
                directories.append(path)
            for f in files:
#                 for extension in self.knownModelExtensions:
#                     if(f.endswith('.%s'%(extension))):
#                         relativeRoot = os.path.relpath(root, self.baseDir)
                        path = os.path.join(root,f)
                        modelFiles.append(path)
        return (directories,modelFiles)
    
    def __LoadResource(self,path):
        resource = None
        try:
            extension = os.path.splitext(path)[1].replace('.','') #remove the point in the extension
            self.logger.Info("Loading %s ..."%(path))
            start = default_timer() 
            if(extension in self.knownModelExtensions):
                resource = self.__LoadModelResource(path)
            elif(extension in self.knownXmlExtensions):
                resource = self.__LoadXmlResource(path)
            #check if a handler was found
            if(resource):
                self.__SetLastPersistentPath(resource, path)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            else:
                self.logger.Info("skipped: Unknown format.")
        except Exception as e:
            self.logger.Info("failed: %s"%(str(e)))
        return resource
      
    def __LoadModelResource(self,path):
        resource = ModelResource()
        eResource = self.rset.get_resource(path) 
        for content in eResource.contents:
            resource.contents.add(content)
        #register the resource in the lookup table
        self.__LinkModelResourceAndEResource(resource,eResource)
        #read the contents to the resource object because the containment removes it
        for content in resource.contents:
            eResource.append(content)
        return resource
    
    def __LoadXmlResource(self,path):
        resource = XmlResource()
        #parse input-xml
        xmlparse = xml.etree.ElementTree
        tree = xmlparse.parse(path)
        root = tree.getroot()
        ldfile = Document(name=resource.name, version = "1.0")
        rootelement = Element(name = root.tag, content = root.text.strip())
        resource.document = ldfile
        resource.document.rootelement = rootelement
        for attr in root.attrib:
            newAttr = Attribute(name = attr, value = root.attrib[attr])
            rootelement.attributes.add(newAttr)
        # find first layer
        for element in root:
            if(element.text == None):
                element.text = ""
            #find all subclasses within first layer
            self.__FindChildElements(element, rootelement)
        return resource           
    
    def __FindChildElements(self, element, parent):
        if(element.text == None):
            element.text = ""
        newChild = Element(name = element.tag, content = element.text.strip())
        parent.subelements.add(newChild)
        #create attribute class for each attribute
        for attr in element.attrib:
            newAttr = Attribute(name = attr, value = element.attrib[attr])
            newChild.attributes.add(newAttr)
        #find all child elements
        for child in element:
            self.__FindChildElements(child, newChild)
        return parent
              
    def __SaveResource(self,resource):
        actualPath = self.__GetLastPersitentPath(resource)
        if(actualPath):
            actualRelPath = os.path.relpath(actualPath, self.baseDirAbs)
            self.logger.Info("Saving %s ..."%(actualRelPath))
            start = default_timer()
            if(resource.type == FileResourceTypesE.MODEL): 
                eResource = self.__GetEResourceForModelResource(resource)
                eResource.save()
            elif(resource.type == FileResourceTypesE.XML):
                tree = self.__SaveXmlResource(resource)
                with open(actualPath, "w") as f:
                    #comment: replace is not necessary
                    f.write(tree.replace('<?xml version="1.0" ?>',
                                         '<?xml version="1.0" encoding="utf-8"?>'))  
            elif(resource.type == FileResourceTypesE.TEXT):
                pass
            elif(resource.type == FileResourceTypesE.RAW):
                pass
            #self.__SetLastPersistentPath(resource, actualPath)
            end = default_timer()
            self.logger.Info("ok (%f s)"%(end-start))
        else:
            self.logger.Info("Saving %s skipped,because it is not attached to the workspace."%(resource.name))
        
    def __SaveXmlResource(self, resource):
        ET = xml.etree.ElementTree
        parser = xml.dom.minidom
        #get root element
        rootElement = resource.document.rootelement
        rootTag = ET.Element(rootElement.name)
        rootTag.text = rootElement.content
        #get attributes
        for attrib in rootElement.attributes:
                rootTag.set(attrib.name, attrib.value)
        #find all elements in root
        self.__FindSubElements(ET, rootTag, rootElement)
        #create output string
        xmlstr = parser.parseString(ET.tostring(rootTag)).toprettyxml(indent = "   ")
        return xmlstr   

    def __FindSubElements(self,ET, parentTag, Element):
        for subelement in Element.subelements:
            #add to parent
            subTag = ET.SubElement(parentTag, subelement.name)
            subTag.text = subelement.content
            #get attributes
            for attrib in subelement.attributes:
                subTag.set(attrib.name, attrib.value)
            # find (sub)subelement
            self.__FindSubElements(ET, subTag, subelement)

        
    ''' Special methods for model resources '''
    
    
    def __LinkModelResourceAndEResource(self,modelResource,eResource):
        self.modelResourceLut[eResource] = modelResource
        self.eResourceLut[modelResource] = eResource
        
    def __UnlinkModelResourceAndEResource(self,modelResource):
        try:
            eResource = self.eResourceLut.pop(modelResource)
            self.modelResourceLut.pop(eResource)
        except Exception as e:
            self.logger.Warn("Unlink model resource and eResource failed: %s"%(str(e)))
            
    def __GetModelResourceForEResource(self,eResource):
        try:
            return self.modelResourceLut[eResource]
        except:
            return None
        
    def __GetEResourceForModelResource(self,modelResource):
        try:
            return self.eResourceLut[modelResource]
        except:
            return None
        
    def __ConnectAllEResources(self):
        for resourceUri in self.rset.resources:
            resource = self.rset.resources[resourceUri]
            modelResource = self.__GetModelResourceForEResource(resource)
            if(modelResource):
                for content in resource.contents:
                    resource.remove(content)
                for content in modelResource.contents:
                    resource.append(content)
                    #modelResource.contents.discard(content)
                #HACK1: elements must be removed from the Resource in order to make save work
                modelResource.contents.clear()
        
    def __DisconnectAllEResources(self):
        for resourceUri in self.rset.resources:
            resource = self.rset.resources[resourceUri]
            modelResource = self.__GetModelResourceForEResource(resource)
            if(modelResource):
                #HACK2: now read the content
                for content in resource.contents:
                    modelResource.contents.add(content)
                #HACK3: content must be re-added to the resource because eResource() wont work otherwise
                for content in modelResource.contents:
                    resource.append(content)
        
        