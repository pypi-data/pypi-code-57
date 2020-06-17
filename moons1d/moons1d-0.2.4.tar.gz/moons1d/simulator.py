"""
Copyright (c) 2010-2018 Myriam Rodrigues

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# Class Simulator
import numpy as np
import math
import copy
from astropy.io import fits
from astropy import units as u
from astropy.constants import c
from astropy.units import Quantity
from astropy.modeling.models import Gaussian2D, Disk2D

import scipy.io as sc
from scipy.stats import multivariate_normal, poisson, norm, sigmaclip

from moons1d.spectra import SimSpectrum, Template, Spectra , Sky, Atm_abs, flux2mag


def airmass_to_zenith_dist(airmass):
    """
    returns zenith distance in degrees
    Z = arccos(1/X)
    """
    return np.rad2deg(np.arccos(1. / airmass))


def zenith_dist_to_airmass(zenith_dist):
    """
    ``zenith_dist`` is in degrees
    X = sec(Z)
    """
    return 1. / np.cos(np.deg2rad(zenith_dist))
    
def seeing_to_IQ(seeing, wave, airmass, telescope_diam, L_0 = 25*u.m):

    """Convert seeing into Image quality
    
    This fonction computes the image quality (FWHM of the PSF) at a given wavelength for 
    a seeing and airmass value. The fonction uses the equations defined in https://www.eso.org/observing/etc/doc/helpfors.html 
        
    Parameters
    ----------
    seeing : float
        Seeing value (in arcsec)

    wave : float
        Reference wavelength to compute image quality (in astropy.units)
            
    airmass : float
        Airmass of the observation 
        
    telescope_diam : float
        Diameter of the telescope (in meters)
    
    L_0 : float
        outer scale.  use 25m for ELT and 49m for VLT (in meter)
    

    Returns
    -------
    IQ : float 
        Image quality (astropy.units.arcsec)
        
    Notes
    -------
    Adapted from the MOONS ETC (Oscar Gonzalez, ATC UK)   
    """
    
    wave = wave.to(u.nm)
    telescope_diam = telescope_diam.to(u.m)

    r_0 = 0.100/seeing.value *(wave.value/500.0)**(1.2)*airmass**(-0.6)
    F_kolb = (1/(1+300*telescope_diam/L_0))#-0.981644
    fwhm_atm = seeing.value * airmass**(0.6)*(wave.value/500.0)**(-0.2) *np.sqrt(1.0+F_kolb.value*2.183*(r_0/L_0.value)**(0.356))
  
    #fwhm_atm = seeing.value * airmass.value**(3/5.)*(wave.value/500.0)**(-1/5.)
    fwhm_tel = 0.000212*(wave.value/telescope_diam.value)
    IQ = np.sqrt(fwhm_tel**2 + fwhm_atm**2)
     
     

    return IQ * u.arcsec

def Atmospheric_diffraction(wave, airmass, atm_ref_wav, conditions):
    """Compute the effect of atmospheric difraction at a given airmass and reference wavelength
    
    This fonction computes the difraction shift at a given wavelength relatively to a 
    reference wavelength, using the equations from Fillipenko et al (1992). The fonction accepts an array 
    of wavelengths for which the difraction shift will be computed.
    
    Parameters
    ----------
    wave : array
        Input wavelength (in astropy.units)

    atm_ref_wav : float
        Reference wavelength for atmospheric diffraction

    airmass : float
        Airmass of the observation

    conditions: dic 
        dictionary of environmmental conditions {Temperature [C], Humidity[%], Pressure[mbar]} in astropy.units

    Returns
    -------
    DR : float
        Difraction shift (astropy.units.arcsec)
    
    Notes
    ----------
    Modified from the MOONS ETC (Oscar Gonzalez, ATC UK)
    """                      

    Lambda0 = atm_ref_wav.to(u.micron).value 
    wave = wave.to(u.micron).value
    
    T = conditions['temperature'].to(u.K, equivalencies= u.temperature()).value
    HR = conditions['humidity'].to(u.dimensionless_unscaled).value
    P = (conditions['pressure'].to(u.mBa)).value
    
    ZD_deg = airmass_to_zenith_dist(airmass)
    ZD = np.deg2rad(ZD_deg)
    
    #saturation pressure Ps (millibars)
    PS = -10474.0 + 116.43*T - 0.43284*T**2 + 0.00053840*T**3
     #water vapour pressure 
    Pw = HR * PS
    #dry air pressure
    Pa = P - Pw
    
    Da = (1 - Pa * (57.90*1.0e-8 - 0.0009325/T + 0.25844/T**2)) * Pa/T
    Dw = (1 -Pw * (1 + 3.7 * 1E-4* Pw) *  ( -2.37321 * 1E-3 + 2.23366/T - 710.792/T**2 + 77514.1/T**3)) * Pw/T

    S0 = 1.0/Lambda0
    S = 1.0/wave
    
    N0_1 = 1.0E-8*((2371.34+683939.7/(130.0-S0**2)+4547.3/(38.9-S0**2))*Da+(6487.31+58.058*S0**2-0.71150*S0**4+0.08851*S0**6)*Dw)
    N_1 = 1.0E-8*((2371.34+683939.7/(130.0-S**2)+4547.3/(38.9-S**2))*Da+(6487.31+58.058*S**2-0.71150*S**4+0.08851*S**6)*Dw)
    
    DR=np.tan(ZD)*(N0_1-N_1)* u.rad
    
    return DR.to(u.arcsec)                        

def Aperture_loss(apert_radius, psf_FWHM, shift_psf):
    
    #Generate 2D grid for computingh aperture loss
    x = np.arange(-6, 6, 0.01)
    y = np.arange(-6, 6, 0.01)
    xx, yy = np.meshgrid(x, y)
    
    m = Disk2D(1,0,0,apert_radius)
    mask = m(xx,yy)        

    sigma = psf_FWHM/2.355
    g = Gaussian2D(1, 0., shift_psf, sigma, sigma)
    g1 = g(xx,yy)
    g1 /= g1.sum()
    
    aper_loss =  g1 * mask
    loss = np.sum(aper_loss)

    return loss
    

def Create_Frame(Shape, Distribution, Value, dtype = float):
    """Create a frame with a given distributon
    
    This fonction create 1D or 2D arrays with a given randomn distribution. Three distribution
    can be generate: Poisson, Normal or Constant. 
    
    Parameters
    ----------
    Shape : array
        Dimension of the frame. 1D array or 2D array.  

    Distribution : str
        "Poisson" : Compute a Poisson random variates from the value in `Value`
        "Normal" : Compute a Normal random variates from the value in `Value`
        "Constant" : Fill the Frame with a constant given in parameter 'Value`
            
    Value : float or array
        If Value dimension if 1, the generate
        If Value dim > 2, it should have same dimension as the Shape
    
    dtype: dtype, optional   
        Data type of the output frame (eg. 'int' or 'float' )
        
    Returns
    -------
    Frame : array
        Difraction shift (astropy.units.arcsec)
        
    Notes
    -------
    Use scipy stat generator
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html#scipy.stats.norm
    """
    Frame = np.zeros(Shape)
    if len(Value.shape) <= 1 :
        Frame[:]=Value
    if len(Value.shape) >= 2 :
        Frame = Value
        
    if Distribution == "Poisson":
        Poisson_array = (poisson.rvs(Frame.flatten(), size=Frame.size))
        Frame = Poisson_array.reshape(Shape)
        
    if Distribution == "Normal":
        Normal_array = (norm.rvs(scale = Frame.flatten(), size=Frame.size))
        Frame = Normal_array.reshape(Shape)
        
    if Distribution == "Constant":
        Frame = Frame
    Frame = Frame.astype(dtype)
    
    return Frame

def Merge_fitsband(listfile,outfile):
    """Merge fits files from the three MOONS bands into a single fits
    
    Parameters
    ----------
    listfile : string list
        List of the filename of the three bands fits files
    outfile: string
        Name of the merge file
        
    Returns
    -------
    outfile : .fits file 
        Store the merger of the three bands into a fits file
        
    """
    hdu_RI = fits.open(listfile[0])
    hdu_YJ = fits.open(listfile[1])
    hdu_H = fits.open(listfile[2])
    
    del hdu_RI[0].header['BAND']
    
    hdu = fits.PrimaryHDU()
    hdu_list = [hdu_RI[0],hdu_RI[1],hdu_RI[2],hdu_RI[3],hdu_RI[4],hdu_YJ[1],hdu_YJ[2],hdu_YJ[3],hdu_YJ[4],hdu_H[1],hdu_H[2],hdu_H[3],hdu_H[4]]
    new_hdul = fits.HDUList(hdu_list)
    new_hdul.writeto(outfile, overwrite=True)

class Simulation:
    
    """Simulation object contains all the parameter and methods to run a MOONS simulation. 
    
    A simulation object is defined by a set of properties, including observing condition and 
    instrument configuration files, and a set of 'Spectra' objects, including the input template, 
    skymodel, atmospheric absorption and the output model.
    
    At initialisation, the properties of the Simulation object are filled with the value 
    parameters stored in 'Insconfig' and 'Obsconfig' data structure, that respectively 
    store the information from the instrument configuration file (Virtual_MOONS.ini) and 
    OB configuration file (e.g. OB_config.ini). A empty 'Spectra' object called .model is also 
    initialize to store the simulated model. 
    
    """


    def __init__(self, Insconfig_all, Obsconfig):
        """Initialise simulation object
        Initialise the Simulation object using the content of the two configuration files Insconfig_all and Obsconfig 
        
        Attributes
        ----------
        mode : str
           The attribute `mode` is the resolution mode of MOONS. Could be etiher "LR" for the low resolution mode or "HR" for the high resolution mode
        band : str
           The attribute `band` stores the band of the simulated observartion. Valid options are "RI", "YJ", "H", "all"  
        OB_name : str
           Name of the Observing Block  
        Atm_correction : float
            Wavelength reference for the atmospheric diffraction correction (in micron)
        NDIT : int
            Number of exposure in the simulated OB
        DIT : float
            Exposure time of each NDIT (s)
        seeing : float
            Seeing during observations(arcsec)
        airmass : float
            Airmass during observation    
        condition : dic
            Dictionary containing the environemental conditions during observation. 
            temperature (C), humidity (%), pressure (mBar)
    
        config : dic
            Dictionary containing the configuration of the instrument during the observations. 
            detector properties - ron, dark current, gain, saturation_level, pix_size, qe
            spectral config - wave_min (microns), wave_max(microns), resolution, spec_sampling (pixels)
            throughput - transmission_file, telescope_file
            apertures - t_aperture (diameter in m), sky_aperture (fibre aperture in sky, in arcsec)
        
    model : :obj:`SimSpectrum`
        SimSpectrum class object containing the simulated MOONS spectra, and the throughput curves.
            
        """
        Insconfig = Insconfig_all[Obsconfig['mode']][Obsconfig['band']]
        Insconfig.update({'sky_aperture': Insconfig_all['sky_aperture'], 'mode': Obsconfig['mode'], 'band': Obsconfig['band'], 'path_Inst_config':Insconfig_all['path_Inst_config'] })
        Insconfig.update(Insconfig_all['Telescope'][Obsconfig['telescope']])                   
        del Insconfig_all

        self.mode = Insconfig['mode']
        self.band = Insconfig['band']
        
        self.OB_name = Obsconfig['Obs_ID']
        self.Atm_correction = float(Obsconfig['at_corr']) * u.micron
        self.NDIT = int(Obsconfig['ndit']) * u.dimensionless_unscaled
        self.DIT = float(Obsconfig['dit']) * u.s
        self.seeing = float(Obsconfig['seeing']) * u.arcsec
        self.airmass = float(Obsconfig['airmass']) * u.dimensionless_unscaled
        
        self.conditions = {}
        self.conditions['temperature'] = float(Obsconfig['temperature']) * u.deg_C
        self.conditions['humidity'] = float(Obsconfig['humidity']) * u.percent
        self.conditions['pressure'] = float(Obsconfig['pressure']) * u.mBa
        
        self.config = {}
        self.config['wave_min'] = float(Insconfig['wave_min']) * u.micron
        self.config['wave_max'] = float(Insconfig['wave_max']) * u.micron
        self.config['wave_min'] = self.config['wave_min'].to(u.angstrom)
        self.config['wave_max'] = self.config['wave_max'].to(u.angstrom)
        self.config['ron'] = float(Insconfig['ron'])
        self.config['dark'] = float(Insconfig['dark']) /3600. 
        self.config['gain'] = float(Insconfig['gain']) * u.count / u.photon
        self.config['saturation_level'] = float(Insconfig['saturation_level'])
        self.config['pix_size'] = float(Insconfig['pix_size']) * u.micron
        self.config['resolution'] = float(Insconfig['resolution'])
        self.config['spec_sampling'] = float(Insconfig['spec_sampling']) * u.pix       
        self.config['qe_file'] = Insconfig['path_Inst_config'] + Insconfig['qe_file']
        self.config['transmission_file'] = Insconfig['path_Inst_config'] + Insconfig['transmission_file']
        self.config['sky_aperture'] = float(Insconfig['sky_aperture']) * u.arcsec
        self.config['t_aperture'] = float(Insconfig['t_aperture']) * u.m
        self.config['telescope_file'] = Insconfig['path_Inst_config'] + Insconfig['telescope_file']
        
        self.model = SimSpectrum(1)
  
        self.FileOutput = ""
        
    def setFileOut(self, FileOutput):
        """Define as a property the path and name of the output .fits file, where the results of the simulation are stored.

        Parameters
        ----------
        FileOutput : str
            Path and filename of the output .fits file 
        
        Attributes
        ----------
        FileOutput : str
            Path and filename of the output .fits file
        """
        self.FileOutput =  FileOutput      
    
    def setTemplate(self, template ):
        """Define as a property of the object, a Spectra object with the input template, called .template

        Parameters
        ----------
        template : Spectra object
            Spectra object with the template spectrum
        
        Attributes
        ----------
        template ::obj:`Template`
            Template object from Spectra class containg the input science template
        """
        self.template = Template(2)
        self.template =  template 

    def setSky(self, sky ):
        """Define as a property of the object, a Spectra object with the input sky, called .sky

        Parameters
        ----------
        sky : Spectra object
            Spectra object with the sky spectrum
        
        Attributes
        ----------
        sky ::obj:`Sky`
            `Sky`object from Spectra class containg the input sky spectrum
        """
        self.sky = Sky(1)
        self.sky =  sky 
        
    def setAtms_abs(self, atm ):
        """Define as a property of the object, a Spectra object with the input atmospheric absorption, called .sky

        Parameters
        ----------
        atm : Spectra object
            Spectra object with the atmospheric absorption spectrum
        
        Attributes
        ----------
        atm_abs ::obj:`atm_abs`
            `atm_abs`object from Spectra class containg the input atmospheric absorption spectrum
        """
        self.atm_abs = Atm_abs(1)
        self.atm_abs =  atm    
        
    def GenerateDispersionAxis(self, verbose = True):
        """ Generate the dispersion axis for a MOONS bands according to the parameters stored in the object properties.
        
        Parameters
        ----------
        verbose : bol
            if True print out information on the output dispersion axis
            
        wave_min : float
            Minimun of the wavelength range. Stored in self.wave_min.  
        wave_max : float
            Maximun of the wavelength range. Stored in self.wave_max. 
        resolution : str
            Spectral resolution. Stored in self.resolution. 
        spec_sampling: str
            Pixels per elements of spectral resolution. Stored in self.spec_sampling
            
        Attributes
        ----------
        model.wave : array
            Store the array in the property .wave of the Spectra object .model.
        
        central_wave: float
            Central wavelength of the band. Store as properties .central_wave
        SRE: float
            Spectral resolution element. Store as properties .SRE
        npix: int
            Number of pixels in the spectra array. Store as properties .npix
        
        Returns
        -------
        None
        """
        
        #Description of return value
        #Set dispersion axis
        central_wave = (self.config['wave_min'] + self.config['wave_max'] )/2.
        self.central_wave = central_wave
        range_wave = np.round(self.config['wave_max'] - self.config['wave_min'])
        
        #xanpix=0.072*(self.config['pix_size']/15.0)*(1.1/1.0)*(39.0/self.config['t_aperture']) 
        #yanpix=0.072*(self.config['pix_size']/15.0)*(1.1/1.0)*(39.0/self.config['t_aperture'])
        #ypix_fwhm = self.config['sky_aperture'] / yanpix 
        
        self.config['SRE'] = central_wave /self.config['resolution']
        self.config['dispersion']= central_wave /self.config['resolution'] / self.config['spec_sampling']
        self.config['npix']= range_wave / self.config['dispersion'] 
                                
        pix_arr = np.arange(0,int(self.config['npix'].value),1) * u.pix
        self.model.wave = self.config['wave_min'] + pix_arr * self.config['dispersion']
        
        if verbose:
            print('[INFO] | GENERATE DISPERSION AXIS:')
            print('[INFO] |--- [Wave range]= %f - %f %s' % (self.config['wave_min'].value,self.config['wave_max'].value,self.config['wave_max'].unit))
            print('[INFO] |--- [Spectral Resolution Element]= %f' % (self.config['SRE'].value))
            print('[INFO] |--- [dispersion]= %f %s' % (self.config['dispersion'].value,self.config['dispersion'].unit))
            print('[INFO] |--- [npix]= %f %s' % (self.config['npix'].value,self.config['npix'].unit))
            
    def Generate_Instrument_Transmission(self, verbose = True):
        """ Generate the Instrument transmission functions, detector and optical tray, for a given MOONS configuration.
        
        The transmission functions of the detector an the optical tray are stored it in '.model.detector' and '.model.instrument' respectively.
        
        Parameters
        ----------
        verbose : bol
            if True print out information on the breakdown of the instrument transmission     
        mode : str
            Spectral resolution mode, "HR" or "LR". Stored in self.mode
            
        Attributes
        ----------
        model.instrument : array in a :Spectra: object
            Transmission from the optical tray. Store as an array of the property .model
        model.detector : array in a :Spectra: object
            Detector efficiency. Store as an array of the property .model
        
        Returns
        -------
        None
            
        """
        
        #Load the transmission from the optical tray and store it in a Spectra object
        efficiency = sc.readsav(self.config['transmission_file'],verbose=False)
        Instrument_response = Spectra(101) 
        Instrument_response.wave = efficiency.weff * u.nm
        if (self.mode == "HR"):
            Instrument_response.flux = efficiency.hreff * 100 * u.percent
        if (self.mode == "LR"):
            Instrument_response.flux = efficiency.lreff * 100 * u.percent
            #Re-sample to the dispersion solution as stored in .model.wave
        Instrument_response.ReSampleArr(self.model.wave)   
        self.model.instrument = Instrument_response.flux      
        if verbose:
            print('[INFO] | LOAD INSTRUMENT TRANSMISSION:')     
            print('[INFO] |--- [File]= %s' % (self.config['transmission_file']))
            
        #Load the transmission from the optical tray    
        Detector_response = Spectra(102)
        Detector_response.LoadFromTxt(self.config['qe_file'],unitwave = u.micron, unitflux = u.percent )
        Detector_response.ReSampleArr(self.model.wave)
        self.model.detector = Detector_response.flux
        if verbose:
            print('[INFO] | LOAD DETECTOR TRANSMISSION:')     
            print('[INFO] |--- [File]= %s' % (self.config['qe_file']))
            
    def Generate_Telescope_Transmission(self, verbose = True):
        """ Generate the telescope transmission and store it in `.model.telescope` 
        
        Parameters
        ----------
        verbose : bol
            if True print out information on the input file 
            
        telescope_file : string
            Filename of the txt file with the VLT transmission. Stored in self.config['telescope_file']
      
        Attributes
        ----------
        model.telescope : array
            Transmission from the atmosphere. Store as an array of the property .model
        
        Returns
        -------
        None
        """
        
        Telescope_response = Spectra(100)

        Telescope_response.LoadFromTxt(self.config['telescope_file'],unitwave = u.micron, unitflux = u.dimensionless_unscaled)
        Telescope_response.flux = Telescope_response.flux.to(u.percent)
        Telescope_response.ReSampleArr(self.model.wave)
        self.model.telescope = Telescope_response.flux
        if verbose:
            print('[INFO] | LOAD TELESCOPE TRANSMISSION:')     
            print('[INFO] |--- [File]= %s' % (self.config['telescope_file']))
            
    def Generate_Total_Transmission(self, verbose=True):  
        """ Generate the total transmission function from the atmosphere, telescope and instrument transmission array. 
        The total transmission is stored as an float array in .model.transmission
        
        Parameters
        ----------
        verbose : bol
            if True print out information on the breakdown of the transmission contribution 
        model.instrument : float 
            array with the instrument transmission  
        model.detector : float 
            array with detector efficiency
        model.telescope : float 
            array with telescope transmission  
        model.atmosphere : float 
            array with atmosphere transmission  
            
        Attributes
        -------
        model.transmission : array in a Spectra object
            Total transmission. Store as an array of the property .model
        
        Returns
        -------
        None
        """
            
        Transmission = Spectra(103)
        print('[INFO] | GENERATE TOTAL TRANSMISSION:')     
        if hasattr(self.model,'instrument'):
            Transmission.flux = self.model.instrument.to(u.dimensionless_unscaled) 
            if verbose:
                mean = np.mean(self.model.instrument.to(u.dimensionless_unscaled))
                print('[INFO] |--- Add Instrument [Mean]= %f' % (mean))
        else: 
            Transmission.flux = np.ones_like(self.model.wave.value) * u.dimensionless_unscaled
            print('[WARNING] |--- Instrument response is missing - Transmission set to 100%')
        
        if hasattr(self.model,'detector'):
            Transmission.flux *=  self.model.detector.to(u.dimensionless_unscaled) 
            if verbose:
                mean = np.mean(self.model.detector.to(u.dimensionless_unscaled))
                print('[INFO] |--- Add Detector [Mean]= %f' % (mean))
        else :
            print('[WARNING] |--- Detector response is missing - Set to 100%')
            
        if hasattr(self.model,'telescope'):
            Transmission.flux *= self.model.telescope.to(u.dimensionless_unscaled) 
            if verbose:
                mean = np.mean(self.model.telescope.to(u.dimensionless_unscaled))
                print('[INFO] |--- Add Telescope [Mean]= %f' % (mean))
        else :
            print('[WARNING] |--- Telescope response is missing - Set to 100%')
        
        if hasattr(self.model,'fibreLoss'):
            Transmission.flux *= self.model.fibreLoss.to(u.dimensionless_unscaled) 
            if verbose:
                mean = np.mean(self.model.fibreLoss.to(u.dimensionless_unscaled))
                print('[INFO] |--- Add Fibre losses [Mean]= %f' % (mean))
        else :
            print('[WARNING] |--- Aperture loss is missing - Set to 100%')
        
        self.model.transmission = Transmission.flux.to(u.percent)
        if verbose:
            mean = np.mean(self.model.transmission.to(u.dimensionless_unscaled))
            print('[INFO] |--- Total transmission [Mean]= %f' % (mean))
        
    def Generate_FibreLoss(self, atm_disp = True): 
        
        """ Compute flux loss at the entrance of the fibre. Includes the aperture loss as function of the seeing
        and optionaly the loss due to the atmospheric dispersion
        
        Parameters
        ----------
        atm_disp : bol
            if True computes the fibre loss due to the atmospheric dispersion using 'atm_ref_wav' and 'conditions'
            
        sky_aperture : float 
            size of the aperture on sky (arcsec) 
        model.wave : array
            Input wavelength (in astropy.units)
            
        airmass : float 
            Airmass of the observation 
        
        seeing : float
            Seeing of the observation (in arcsec)
            
        t_aperture : float
            Telescope diameter (m) 
        
        atm_ref_wav : float (optional)
            Reference wavelength for atmospheric_diffraction
        
        conditions: dictionary (optional)
            dictionary of environmmental conditions     
            {Temperature [C], Humidity[%], Pressure[mbar]} in astropy.units  
        
        Attributes
        ----------
        model.fibreLoss : array
            Update model with FibreLoss troughtput curve
        
        Returns
        -------
        None
        """
        lambda_unit = self.config['wave_min'].unit
        lambda_arr = np.linspace(self.config['wave_min'].value,self.config['wave_max'].value ,10) * lambda_unit
        F_atm = np.empty([10])
        
        for i in range(0, len(lambda_arr), 1): 
            #Compute PSF FWHM at the given wavelength
            PSF_FWHM = seeing_to_IQ(self.seeing, lambda_arr[i] , self.airmass , self.config['t_aperture'] )   
            
            if atm_disp == True: 
                ADisp = Atmospheric_diffraction(lambda_arr[i], self.airmass, self.Atm_correction, self.conditions)
            else:
                ADisp = 0 * u.arcsec
                
            F_atm[i] = Aperture_loss(self.config['sky_aperture'].value /2., PSF_FWHM.value, ADisp.value) * 100
            
            
        FibreLoss = Spectra(104) 
        FibreLoss.wave  = lambda_arr 
        FibreLoss.flux = F_atm * u.percent
        FibreLoss.ReSampleArr(self.model.wave)      
        self.model.fibreLoss = FibreLoss.flux
         
    def Match_resolution(self):
        
        """ Degrade all Spectra object attached to the Simulation object to the requiered resolution and sampling
        
        This function search for 'template' , 'sky', 'atm_abs' type object in the Simulation instance, and degrade the spectral
        resolution and resample the arrays to the resolution and sampling defined in Simulation.config['resolution'] 
        and Simulation.config['dispersion'].  
        
        Parameters
        ----------
        resolution : float
            Resolution of the output spectrum
            
        dispersion : float 
            Pixel per elements of spectral resolution of the output spectrum
        
        Attributes
        ----------
        Simulation.template : Spectra Object
            The wave and flux arrays are updated, as well as the object properties template.Resolution, template.dispersion
        
        Simulation.sky : Spectra Object
            Same as above
        
        Simulation.atm_abs : Spectra Object
            Same as above      
        
        Returns
        -------
        None
        """
        wave_range = [self.config['wave_min'].value * 0.9 , self.config['wave_max'].value * 1.1 ] * self.config['wave_max'].unit
  
        if hasattr(self, 'template'):
            self.template.Trim(wave_range)
            central_wave_in = np.mean(self.template.wave)
            FWHM_in =  central_wave_in / self.template.Resolution 
            dispersion_in = self.template.Dispersion 
            FWHM_out = self.central_wave /self.config['resolution']
            if FWHM_in < FWHM_out:
                self.template.Degrade_Resolution(FWHM_in, dispersion_in, FWHM_out)
            self.template.Resolution = self.config['resolution']
            self.template.ReSampleArr(self.model.wave)
            self.template.Dispersion = self.config['dispersion']
        else : 
            print('[ERROR] ---- No template is attached to the simulation')
            
        if hasattr(self, 'sky'): 
            self.sky.Trim(wave_range)
            central_wave_in = np.mean(self.sky.wave)
            dispersion_in = self.sky.Dispersion 
            FWHM_in = self.sky.Dispersion * 2. * u.pix
            FWHM_out = self.central_wave /self.config['resolution'] 
            self.sky.Degrade_Resolution(FWHM_in, dispersion_in, FWHM_out)
            self.sky.Resolution = self.config['resolution']
            self.sky.ReSampleArr(self.model.wave)
            self.sky.Dispersion = self.config['dispersion']
        else : 
            print('[ERROR] ---- No Sky is attached to the simulation')
            
        if hasattr(self, 'atm_abs'):  
            self.atm_abs.Trim(wave_range)
            central_wave_in = np.mean(self.atm_abs.wave)
            dispersion_in = self.atm_abs.Dispersion 
            FWHM_in = self.atm_abs.Dispersion * 2. * u.pix
            FWHM_out = self.central_wave /self.config['resolution'] 
            self.atm_abs.Degrade_Resolution(FWHM_in, dispersion_in, FWHM_out)
            self.atm_abs.Resolution = self.config['resolution']
            self.atm_abs.ReSampleArr(self.model.wave)
            self.atm_abs.Dispersion = self.config['dispersion']
        else : 
            print('[WARNING] ---- No Atmospheric absorption is attached to the simulation')
            
            
    def ConvertFlux2Counts(self, type_source='point-source'): 
        """ Convert fluxes into photons counts according to the type of the source 'point source' or 'extended' source. 
        
        This function search for 'template' , 'sky', -type object in the Simulation instance, and convert the flux arrays 
        from flux to counts. 
        For 'Template' objects, fluxes are first convolved with the atmospheric absorption function stored in Simulation.atm_abs
        and then converted into counts. The flux array of 'Extended' source is in surface brigthness and therefore is first integrated 
        over the sky aperture before the convertion.
        'Sky' objects, the surface brightness is integrated over the sky aperture.
        
        Parameters
        ----------
        type_source : str
            'point-source' : point sources have fluxes interpreted as being erg/s/A/cm2
            'extended' : extended sources have fluxes  interpreted as being erg/s/A/cm2/arcsec2. The flux is integrated in the fibre aperture
            
        dit : foat    
            Dit for a single exposure
        central_wave : float 
            Central wavelength  (angstrom) 
        
        t_aperture : float 
            Telescope diameter  (m) 
            
        sky_aperture : float 
            Fibre aperture on sky (arcsec)   
        
        gain : float 
            Detector gain (arcsec)     
        
        dispersion : float 
            number of pixels per elements of spectral resolution     
        
        Attributes
        ----------
        Simulation.template : Spectra Object
            The wave and flux arrays are updated, as well as the object properties template.Resolution, template.dispersion
        
        Simulation.sky : Spectra Object
            Same as above
        
        Simulation.atm_abs : Spectra Object
            Same as above     
        Returns
        -------
        None        
        """
        self.config['central_wave'] = np.mean(self.template.wave)
        self.config['S_coll'] = math.pi * ((self.config['t_aperture']).to(u.cm)/2.0)**2
        self.config['S_aper'] = math.pi * (self.config['sky_aperture']/2)**2
        Conversion_factor = self.model.transmission.to(u.dimensionless_unscaled) * (self.config['dispersion'] * 1 * u.pix) * self.config['S_coll']  *self.config["gain"] 
        
        if hasattr(self, 'template'):
            F_erg = self.template.flux * self.atm_abs.flux.value
                 
            if self.template.type_source == 'extended': 
                F_erg *= self.config['S_aper'] 
            
            F_pho = F_erg.to( u.photon / u.s / u.cm**2/ u.angstrom, equivalencies=u.spectral_density(self.config['central_wave']))
            F_pho *= self.DIT * Conversion_factor
            self.model.Obj_pho = F_pho 
            
        if hasattr(self, 'sky'):
            FS_erg = self.sky.flux  * self.atm_abs.flux.value
            FS_erg *=self.config['S_aper'] 
            FS_pho = FS_erg.to( u.photon / u.s / u.cm**2/ u.angstrom, equivalencies=u.spectral_density(self.config['central_wave']))
            FS_pho *= self.DIT * Conversion_factor
            self.model.Sky_pho = FS_pho
            
    def Generate_Nod_Seq(self, stack = 'sum'):
        """ Generate a Nodding Sequence observation
        
        This function simulates a reduced nodding sequence (or Xshitch) prior to the flux calibration. 
        NDIT exposures are generated for both target+sky and sky spectra. Each spectra include the Poisson 
        noise from the Target and sky, dark level and its Noise (Poisson), and RoN (Normal noise). 
        For each NDIT, the funtion subtracts the sky to the target+sky spectrum. The NDIT x residuals spectra are 
        then stack either by 'sum' or 'mean'. The output spectra are in ADU units. 
        
        In addition to the reduced spectrum, an associated noise spectrum is computed as:
        Noise = sqrt(Target_pho + Sky_phot + NDIT * ron**2 + dark * DIT))
        
        Parameters
        ----------
        stack : str, optional
            'sum' (default) or 'mean'
        
        Attributes
        ----------
        model.Reduced_frame : :obj:`model` array
            array of a `model`object from Spectra class containg the reduced spectrum 
        
        model.Noise_frame : :obj:`model` array
            array of a `model`object from Spectra class containg the noise spectrum associated to the reduced spectrum 
                    
        Returns
        -------
        None
        """  
        
        #Poisson Noise from Sky
        # Signal and sky frame
        Shape_o = np.squeeze(self.model.Obj_pho.shape)
        Size_obs= [int(Shape_o), int(self.NDIT.value)]
        Reduced_frames = np.zeros(Size_obs)
        
        for i in range(0,int(self.NDIT)):
            Sky_model = self.model.Sky_pho 
            Sky_frame = Create_Frame(Shape_o,"Poisson", Sky_model.value , dtype = int) * u.count #in pho
            Dark_current = np.array([self.config["dark"] * self.DIT.value])
            Dark_frame = Create_Frame(Shape_o,"Poisson", Dark_current, dtype = int ) * u.count
            Ron_signal = np.array([ self.config["ron"]])
            RoN_frame = Create_Frame(Shape_o,"Normal", Ron_signal, dtype = int)  * u.count
            
            Sky_frame += Dark_frame + RoN_frame
                      
            Object_frame = (self.model.Obj_pho + self.model.Sky_pho) 
            Observed_frame = Create_Frame(Shape_o,"Poisson", Object_frame.value, dtype = int) * u.count
            Dark_current = np.array([self.config["dark"] * self.DIT.value])
            Dark_frame = Create_Frame(Shape_o,"Poisson", Dark_current, dtype = int )  * u.count
            Ron_signal = np.array([ self.config["ron"]])
            RoN_frame = Create_Frame(Shape_o,"Normal", Ron_signal, dtype = int)  * u.count
            Observed_frame += Dark_frame + RoN_frame

            Residual_frame = Observed_frame - Sky_frame
            Reduced_frames[:,i] = Residual_frame

        if stack == 'sum':
            Reduced_frame = np.sum(Reduced_frames, axis = 1) 
        if stack == 'mean': 
            Reduced_frame = np.mean(Reduced_frames, axis = 1) 
        self.model.Reduced_frame = Reduced_frame * u.count 
        
        #Generate noise array
        tmp = (self.model.Sky_pho + self.model.Obj_pho) 
        noise = np.sqrt(( tmp.value + self.NDIT * self.config["ron"]**2 + self.config["dark"] * self.DIT.value))
        self.model.Noise_frame = noise.value * u.count
                          
        
    def Calibrate_data(self, units = u.erg / u.s / u.cm**2/ u.angstrom):       
        """ Calibrate the reduced spectra generated by Generate_Nod_Seq()
        This function update the 'model' object with a flux-calibrated spectrum. The calibration include the
        instrument and telescope response, and the atmospheric absorption. 
        
        Parameters
        ----------
        units : str, optional
            Flux units of the output spectrum. The default is u.erg / u.s / u.cm**2/ u.angstrom).
        
        Attributes
        ----------
        model.Obs_calibrated : obj:`model` array
            array of a `model`object from Spectra class containg the flux-calibrated spectrum 
        
        model.Error_calibrated :  obj:`model` array
            array of a `model`object from Spectra class containg the flux-calibrated noise spectrum
        
        Returns
        -------
        None
        
        """
        
        factor = (self.config['dispersion'] * 1 * u.pix) * self.NDIT * self.DIT * self.config["S_coll"] * self.atm_abs.flux * self.model.transmission.to(u.dimensionless_unscaled) * self.config["gain"] 
        
        if self.template.type_source == 'point-source':  
            FS_pho =  self.model.Reduced_frame / factor
            self.model.Obs_calibrated = FS_pho.to( units, equivalencies=u.spectral_density(self.config['central_wave'])) 
            
            FE_pho = self.model.Noise_frame/ factor
            self.model.Error_calibrated = FE_pho.to( units, equivalencies=u.spectral_density(self.config['central_wave'])) 
            
        if self.template.type_source == 'extended': 
            
            FS_pho =  self.model.Reduced_frame / factor
            FS_erg = FS_pho.to( units, equivalencies=u.spectral_density(self.config['central_wave']))     
            self.model.Obs_calibrated = FS_erg / ( math.pi * (self.config['sky_aperture']/2)**2)
            
            FE_pho = self.model.Noise_frame/ factor
            FE_erg = FE_pho.to( units, equivalencies=u.spectral_density(self.config['central_wave']))        
            self.model.Error_calibrated = FE_erg / ( math.pi * (self.config['sky_aperture']/2)**2)
        
    def SavetoFits_Debug(self):
        """ BEBUG - Save simulation outputs in a fits file
        This function saves all parameters and spectra associated to a simulation instance into a fits file.
        The primary header stores the parameters of the simulations, namely the observation and instrument configuration,
        and the properties of the input template (source type, template name, redshift, magnitude).
        
        - HDU1 Flux-calibrated spectrum  
        - HDU2 Flux-calibrated noise spectrum 
        - HDU3 Object in cnts without noise   
        - HDU4 Template in flux  
        - HDU5 Sky in flux 
        - HDU6 Transmission 
        - HDU7 Sky mask
        
        Parameters
        ----------
        FileOutput : str
            Path and name of the output file  
                        
        Returns
        -------
        None
        
        """
        
        #Create Primary header with the simulation config
        hdu = fits.PrimaryHDU()
        hdu.header['INST'] = 'MOONS_SIM'
        hdu.header['MODE'] = self.mode
        hdu.header['BAND'] = self.band
        hdu.header['OBNAME'] = self.OB_name
        hdu.header['ATCORR'] = self.Atm_correction.value
        hdu.header['NDIT'] = self.NDIT.value
        hdu.header['DIT'] = self.DIT.value
        hdu.header['SEEING'] = self.seeing.value
        hdu.header['TEMP'] = self.conditions['temperature'].value
        hdu.header['HUMIDITY'] = self.conditions['humidity'].value
        hdu.header['PRESSUR'] = self.conditions['pressure'].value
        hdu.header['WMIN'] = self.config['wave_min'].value
        hdu.header['WMAX'] = self.config['wave_max'].value
        hdu.header['RON'] = self.config['ron']
        hdu.header['DARK'] = self.config['dark']
        hdu.header['GAIN'] = self.config['gain'].value
        hdu.header['SATLEVEL'] = self.config['saturation_level']
        hdu.header['PIXSIZE'] = self.config['pix_size'].value
        hdu.header['R'] = self.config['resolution']
        hdu.header['SAMPLING'] = self.config['spec_sampling'].value
        hdu.header['SKY_AP'] = self.config['sky_aperture'].value
        hdu.header['TEL_AP'] = self.config['t_aperture'].value
        hdu.header['TEMPLATE'] = self.template.name
        hdu.header['TYPE'] = self.template.type_source
        hdu.header['Z'] = self.template.z
        hdu.header['MAGAB'] = self.template.magAB
        hdu.header['WAVEAB'] = self.template.waveAB
        
        #Create extension 1     
        hdu1 = fits.ImageHDU(data = self.model.Obs_calibrated.value)
        hdu1.header['NAME'] = 'Flux-calib frame'
        hdu1.header['NAXIS1'] = self.config['npix'].value
        hdu1.header['CRVAL1'] = self.config['wave_min'].value
        hdu1.header['CDELT1'] = self.config['dispersion'].value  
        hdu1.header['CRPIX1'] =	1.0  
        hdu1.header['TUNIT1'] = 'AA'
        hdu1.header['TUNIT2'] = self.model.Obs_calibrated.unit.to_string('fits')
        hdu1.header['R'] = self.config['resolution']
        hdu1.header['SAMPLING'] = self.config['spec_sampling'].value 

        if hasattr(self.model, 'Error_calibrated'):  
            #Create extension - Flux calibrated Noise spectrum    
            hdu2 = fits.ImageHDU(data = self.model.Error_calibrated.value)
            hdu2.header = copy.deepcopy(hdu1.header)
            hdu2.header['NAME'] = 'Flux error'
        
        #Create extension - Object in cnts without noise     
        hdu3 = fits.ImageHDU(data = self.model.Obj_pho.value)
        hdu3.header = copy.deepcopy(hdu1.header)
        hdu3.header['NAME'] = 'Obs noNoise'
        
        #Create extension - Template in flux  
        hdu4 = fits.ImageHDU(data = self.template.flux.value)
        hdu4.header = copy.deepcopy(hdu1.header)
        hdu4.header['TUNIT2'] = 'erg/AA/cm2/s'
        hdu4.header['NAME'] = 'Template'
        
        #Create extension - Sky in flux  
        hdu5 = fits.ImageHDU(data = self.sky.flux.value)
        hdu5.header = copy.deepcopy(hdu1.header)
        hdu5.header['TUNIT2'] = 'ph/s/cm2/AA/arcsec2'
        hdu.header['NAXIS'] = 5
        hdu5.header['NAME'] = 'Sky'
        hdu_list = [hdu,hdu1, hdu2, hdu3, hdu4, hdu5]
        
        #Create extension - Transmission   
        hdu6 = fits.ImageHDU(data = self.model.transmission.value)
        hdu6.header = copy.deepcopy(hdu1.header)
        hdu6.header['TUNIT2'] = 'ph/s/cm2/AA/arcsec2'
        hdu6.header['NAME'] = 'Transmission'
        hdu.header['NAXIS'] = 6
        hdu_list = [hdu,hdu1, hdu2, hdu3, hdu4, hdu5, hdu6]
        
        #Create extension - Sky mask  
        if len(self.sky.Mask) > 2 :
            hdu7 = fits.ImageHDU(data = self.sky.Mask.astype(int))
            hdu7.header = copy.deepcopy(hdu1.header)
            hdu7.header['TUNIT2'] = ''
            hdu7.header['NAME'] = 'Sky mask'
            hdu.header['NAXIS'] = 7
            hdu_list = [hdu,hdu1, hdu2, hdu3, hdu4, hdu5,hdu6, hdu7]

        new_hdul = fits.HDUList(hdu_list)
        new_hdul.writeto(self.FileOutput, overwrite=True)
   
        return


    def SavetoFits(self):
        """ Save simulation outputs in a fits file
        This function saves all parameters and spectra associated to a simulation instance into a fits file.
        The primary header stores the parameters of the simulations, namely the observation and instrument configuration,
        and the properties of the input template (source type, template name, redshift, magnitude).
        
        - HDU1 Flux-calibrated spectrum 
        - HDU2 Flux-calibrated noise spectrum
        - HDU3 Sky mask   
        - HDU4 Sky in flux 
        
        Parameters
        ----------
        FileOutput : str
            Path and name of the output file  
        
        Returns
        -------
        None
        
        """
        #Create Primary header with the simulation config
        hdu = fits.PrimaryHDU()
        hdu.header['INST'] = 'MOONS_SIM'
        hdu.header['MODE'] = self.mode
        hdu.header['BAND'] = self.band
        hdu.header['OBNAME'] = self.OB_name
        hdu.header['ATCORR'] = self.Atm_correction.value
        hdu.header['NDIT'] = self.NDIT.value
        hdu.header['DIT'] = self.DIT.value
        hdu.header['SEEING'] = self.seeing.value
        hdu.header['TEMP'] = self.conditions['temperature'].value
        hdu.header['HUMIDITY'] = self.conditions['humidity'].value
        hdu.header['PRESSUR'] = self.conditions['pressure'].value
        hdu.header['RON'] = self.config['ron']
        hdu.header['DARK'] = self.config['dark']
        hdu.header['GAIN'] = self.config['gain'].value
        hdu.header['SATLEVEL'] = self.config['saturation_level']
        hdu.header['PIXSIZE'] = self.config['pix_size'].value
        hdu.header['R'] = self.config['resolution']
        hdu.header['SAMPLING'] = self.config['spec_sampling'].value
        hdu.header['SKY_AP'] = self.config['sky_aperture'].value
        hdu.header['TEL_AP'] = self.config['t_aperture'].value
        hdu.header['TEMPLATE'] = self.template.name
        hdu.header['TYPE'] = self.template.type_source
        hdu.header['Z'] = self.template.z
        hdu.header['MAGAB'] = self.template.magAB
        hdu.header['WAVEAB'] = self.template.waveAB
        
        #Create extension 1     
        hdu1 = fits.ImageHDU(data = self.model.Obs_calibrated.value)
        hdu1.header['NAME'] = 'DATA_' + self.band
        hdu1.header['NAXIS1'] = self.config['npix'].value
        hdu1.header['CRVAL1'] = self.config['wave_min'].value
        hdu1.header['CDELT1'] = self.config['dispersion'].value 
        hdu1.header['CRPIX1'] =	1.0   
        hdu1.header['TUNIT1'] = 'AA'
        hdu1.header['TUNIT2'] = self.model.Obs_calibrated.unit.to_string('fits')
        #'erg/AA/cm2/s' 
        hdu1.header['R'] = self.config['resolution']
        hdu1.header['SAMPLING'] = self.config['spec_sampling'].value 

        #Create extension 2 - Error array     
        hdu2 = fits.ImageHDU(data = self.model.Error_calibrated.value)
        hdu2.header = copy.deepcopy(hdu1.header)
        hdu2.header['NAME'] = 'ERR_' + self.band
        
        #Create extension 3 - Sky mask    
        hdu3 = fits.ImageHDU(data = self.sky.Mask.astype(int))
        hdu3.header = copy.deepcopy(hdu1.header)
        hdu3.header['NAME'] = 'QUAL_' + self.band
        hdu3.header['TUNIT2'] = ''
        
        #Create extension 3 - Sky spectrum
        hdu4 = fits.ImageHDU(data = self.sky.flux.value)
        hdu4.header = copy.deepcopy(hdu1.header)
        hdu4.header['NAME'] = 'SKY_'
        hdu4.header['TUNIT2'] = 'ph/s/cm2/AA/arcsec2'
        hdu4.header['NAME'] = 'Sky'
        
        hdu_list = [hdu,hdu1, hdu2, hdu3, hdu4]
        new_hdul = fits.HDUList(hdu_list)
        new_hdul.writeto(self.FileOutput, overwrite=True)
        

 
        

