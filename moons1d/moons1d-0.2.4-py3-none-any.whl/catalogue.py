# Class Target
import numpy as np
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii

class Target:
    
    def __init__(self, nid ):
        self.id = nid
        self.name = ""
        self.RA = 0.0
        self.DEC = 0.0
        self.mag = 0
        self.mag_filter = ""
        self.template = ""
        self.type = "" # Point-Source or Extended
        self.redshift = ""
        self.survey_name = ""
        self.FileOutput = ""  
        
    def getinfo(self):
         return '%s: %s | %s (%s) | %s ' % (self.id, self.name, self.redshift, self.mag, self.mag_filter, self.template)

    def setMag(self, mag,mag_filter ):
        self.mag = mag
        self.mag_filter = mag_filter
        
    def setRedshift(self, redshift ):
        self.redshift = redshift        
        
    def setTemplate(self, template ):
        self.template = template
        
    def setname(self, name ):
        self.name =  name   
        
    def setOutFile(self, FileOutput):
        self.FileOutput =  FileOutput       
    
    def getFileOutput(self):
        return self.FileOutput
    
    def getRedshift(self):
        return self.redshift
    
    def getMag(self):
        return self.mag
    
#Catalogue 
def Catalogue_Unidistribution(Survey, nTarget, mag_range, mag_band, redshift_range):
    Catalogue = []
    mags = np.random.uniform(mag_range[0],mag_range[1],nTarget)
    redshifts = np.random.uniform(redshift_range[0],redshift_range[1],nTarget)
    
    for i in range(nTarget):
        new_target = Target(i)
        new_target.setRedshift(redshifts[i])
        new_target.setname('%s_%s' % (Survey,i))
        new_target.setMag(mags[i],mag_band)  
        new_target.setOutFile('%s_%s.fits' % (Survey,i))
        Catalogue.append(new_target)
        
    return Catalogue

def Save_Catalogue(catalogue, filename):
    data = []
    for target in catalogue : 
        row = {'id': target.id, 'name': target.name, 'RA': target.RA, 'DEC' : target.DEC, 'mag': target.mag,'mag_filter':target.mag_filter,'template':target.template,'type':target.type,'redshift':target.redshift,'survey_name':target.survey_name,'FileOutput':target.FileOutput }
        data.append(row)
    ascii.write(Table(data), filename, overwrite=True)
    return 
    
