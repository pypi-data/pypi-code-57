
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Problem:
    
    def __init__(self, pType):
        """ Problem class used to establish an instance of a modelling problem
        
        Attributes :
            
            type = string that declares whether the problem is
            Cat = Categorical OR 
            Quant = Quantitative
            
            data = a file of records that represent the problem
            
            nRecords = the number of records
            
            nAttributes = the number of problem variables
            
            outcome = the outcome field for the problem
            
            outcomeMetric = a metric that illustrates the problem outcome
            
        """
        
        self.data = []
        if pType == 'Cat' : 
            self.type = pType
        elif pType == 'Quant':
            self.type = pType
        else:
            self.Type = 'Uknown'
            print("The problem type is Uknown")
            
        self.nRecords = 0
        self.nAttributes = 0
        self.outcome = 0
        self.outcomeMetric = 0
        
        

    def read_csv_file(self, file_name, pOutcome):
    
        """Function to read in data from a txt file. The txt file should have
        one record per line. 
        
        The records should each have an outcome.
                
        Args:
            file_name (string): name of a file to read from
            outcome (int) : the position of the outcome field
        
        Returns:
            None
        
        """
            
        data_list = pd.read_csv(file_name)
    
        self.data = data_list
        self.ootcome = self.setOutcome(pOutcome)
        self.nRecords = self.calculateRecords()
        self.nAttributes = self.calculateAttributes()
        self.outcomeMetric = self.calculateOutcomeMetric()
        


    
    def setOutcome(self, n):
        self.outcome = n
        
        return self.outcome
    
        
    def calculateRecords(self):
        
        """ Function that calaculates the number of records
        
        Args:
            None
            
        Returns:
            self.nRecords
        """
        
        nR = len(self.data)
        self.nRecords = nR
        
        return nR
        
    def calculateAttributes(self):
        """ Function that calaculates the number of attributes
        
        Args:
            None
            
        Returns:
            self.nAttributes
        """
        nA = len(self.data.columns) - 1
        self.nAttributes = nA
        
        return nA
        
    def calculateOutcomeMetric(self):
        """ Function that calaculates the number of attributes
        
        Args:
            None
            
        Returns:
            self.outcomeMetric
        """
        df = pd.DataFrame(self.data)
        pos = self.outcome
        avg = df.iloc[:,pos].sum()/self.nRecords
        
        self.outcomeMetric = avg
        
        return self.outcomeMetric