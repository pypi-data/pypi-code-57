import unittest
import os, sys
from astropy import units as u
from numpy import genfromtxt

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from src.simulator import seeing_to_IQ, Atmospheric_diffraction, Aperture_loss

class test_aperture_correction(unittest.TestCase):
  
  def test_shift(self):
      
      #http://www.eso.org/gen-fac/pubs/astclim/lasilla/diffrefr.html
      #Differential atmospheric refraction at Paranal (T=11.5 C, RH=14.5%, P=743.0 mbar) as a function of wavelength (horizontal, in microns) and airmass (vertical). The values are in arcseconds with respect to a wavelength of 5000 Angstrom
      dumpText = genfromtxt('Shift_paranal.csv', delimiter=' ')
      shift_ref = dumpText[1:,1:] 
      wave_ref = dumpText[0,1:]
      airmass_ref = dumpText[1:,0]
      
      # Paranal conditions
      conditions = {}
      conditions['temperature']=11.5 * u.deg_C
      conditions['humidity']=14.5 * u.percent
      conditions['pressure']=743.0 * u.mBa
      
      i=0
      for airmass in airmass_ref:
          j=0
          for wave in wave_ref:
              #print(airmass,wave,Atmospheric_diffraction(wave * u.micron ,airmass,0.5 * u.micron,conditions).value,shift_ref[i,j])
              self.assertAlmostEqual(Atmospheric_diffraction(wave * u.micron ,airmass,0.5 * u.micron,conditions).value,-1 * shift_ref[i,j],1)
              j=j+1
          i=i+1   


  def test_IQ(self):
    # Paranal conditions
    seeing = 0.8 * u.arcsec
   # print( seeing_to_IQ(seeing, 0.50 * u.micron, 1, 9 * u.m, L_0 = 39*u.m))
    self.assertAlmostEqual(seeing_to_IQ(seeing, 0.50 * u.micron, 1, 9* u.m, L_0 = 39 * u.m).value, seeing.value,2)
    
  def test_Aperture_loss(self):
      seeing = 0.9
      self.assertAlmostEqual(Aperture_loss(3.*seeing/2.355, seeing, 0),0.99,2)
      self.assertAlmostEqual(Aperture_loss(seeing/2., seeing, 0),0.5,2)
if __name__ == '__main__':
    unittest.main()