import warnings
warnings.filterwarnings("ignore")

import os
import pickle
import csv 
from .dataCleaning import *
from .taxonomyAPI import *
from .higherLevelAPI import *
from .commonNameAPI import *
import itertools

class EcoNameTranslator:
    def __init__(self):
        self.index = {}
        self.result = {}
        self.failed = {}
    
    def translate(self,uncheckedNames,includeCommon=True):
        print("Beginnging name reformatting")
        for item in uncheckedNames:
            self.index[item] = [cleanSingleSpeciesString(item),'']
        print("Name reformatting complete")
        print("Indexing records on taxonomy")
        self.tagInputWithTaxaLevel()
        print("Expanding higher level taxonomic names")
        self.mapKnownTaxaLevelToSpecies()
        print("Trying common name translation...(this may take a while)")
        if includeCommon: self.tryCommonNameOnErrorCases()
        self.ensureUniqueInIndex()
        return self.index
    
    def tagInputWithTaxaLevel(self):
        try:
            names = list(map(lambda x: self.index[x][0], self.index.keys()))
            taxonomyAPIResuls, excepted = taxonomyAPI(names)
            self.writeApiResultsToIndex(taxonomyAPIResuls)
        except Exception as e:
            print("Caught fatal exception in taxonomic indexer")
            print(str(e))
    
    def mapKnownTaxaLevelToSpecies(self):
        try:
            names = list(map(lambda x: self.index[x][0], self.index.keys()))
            taxaTuples = list(map(lambda x: self.index[x][1], self.index.keys()))
            originalNamesWthTaxa = list(zip(names,taxaTuples))
            speciesNamesOnly = higherLevelAPI(originalNamesWthTaxa)
            self.writeApiResultsToIndex(speciesNamesOnly)
        except Exception as e:
            print("Caught fatal exception in taxonomic level resolver")
            print(str(e))
    
    def tryCommonNameOnErrorCases(self):
        try:
            names = list(map(lambda x: self.index[x][0], self.index.keys()))
            currentSpeciesResults = list(map(lambda x: self.index[x][1], self.index.keys()))
            bestEffortOfSpecies = list(zip(names,currentSpeciesResults))
            speciesNamesOnly = commonNameAPI(bestEffortOfSpecies)
            self.writeApiResultsToIndex(speciesNamesOnly)
        except Exception as e:
            print("Caught fatal exception in common name resolver")
            print(str(e))
    
    def writeApiResultsToIndex(self,taxonomyAPIResuls):
        taxaAPIDict = {}
        for cleanedName,success,result in taxonomyAPIResuls:
            taxaAPIDict[cleanedName] = result
        
        for name in self.index:
            try: self.index[name][1] = taxaAPIDict[self.index[name][0]]
            except: pass
        
    def ensureUniqueInIndex(self):
        for name in self.index:
            species = self.index[name][1]
            species = list(set(species))
            self.index[name][1] = species
    
    def toPickleFile(self,path):
        with open(path,'wb') as fh:
            pickle.dump(index,fh) 
    
    def toCSV(self,path,name="translatedNames.csv"):
        headers = [["Input Name","Name After Cleaning","Result"]]
        csvData = map(lambda indivEcoName: \
                    list(map(lambda result: [indivEcoName,self.index[indivEcoName][0],result], \
                    self.index[indivEcoName][1])), \
                  self.index.keys())
                      
        csvData = list(itertools.chain(headers,*csvData))
        
        with open(path+"/"+name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csvData)
