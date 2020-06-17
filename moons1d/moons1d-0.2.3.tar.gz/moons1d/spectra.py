# Class Target
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.convolution import Gaussian1DKernel, convolve
from astropy.constants import c
from astropy.units import Quantity
from astropy.stats import sigma_clip

class Spectra:
    """Spectra objects contain 1D arrays of numbers along a regularly spaced grid of wavelengths.

    The spectral pixel values and the wavelength, if any, are available as arrays that can be accessed via properties of the
    Spectrum object called .flux and .wave, respectively. In addition to these 1D arrays, severals attributes are associated 
    that provide general information on the type of spectra.
    
    Attributes
    ----------
    nid : int
        Number identifier of an object instance
    header : str
        String container for comments
    
    flux : 1D array
        Fluxes for each spectral pixels
    wave : 1D array
        Wavelength for each spectral pixels
    
    """    
    def __init__(self, nid ):
        self.nid = nid
        self.header = ""
        self.flux = 0.0 # in ergs/s/cm2/A
        self.wave = 0.0 # in Ang
     
    def Trim(self,wave_range):   
        """Trim spectrum into a wavelength range
        """ 
        wave_range = wave_range.to(self.wave.unit)
        pixel_range = np.where((self.wave >= wave_range[0]) & (self.wave <= wave_range[1]))[0]
        self.wave =  self.wave[pixel_range]
        self.flux =  self.flux[pixel_range]     
    
    def Mean(self,wave_range):
        """Return the mean value of the fluxes array inside a wavelength range
        """
        wave_range = wave_range.to(self.wave.unit)
        pixel_range = np.where((self.wave > wave_range[0]) & (self.wave < wave_range[1]))[0]
        mean = np.mean(self.flux[pixel_range])
        return mean
        
    def ABmag_band(self, lbda, dlbda, unit_wave = u.angstrom) :
        """Compute the AB magnitude corresponding to a wavelength band

        Parameters
        ----------
        lbda : float
            Mean wavelength in Angstrom.
        dlbda : float
            Width of the wavelength band in Angstrom.

        Returns
        -------
        out : float, float
              Magnitude value and its error
        """
        lmin = (lbda - dlbda / 2.0) * unit_wave
        lmax = (lbda + dlbda / 2.0 ) * unit_wave
        lmin = lmin.to(self.wave.unit)
        lmax = lmax.to(self.wave.unit)
        pixel_range = np.where((self.wave > lmin) & (self.wave < lmax))[0]
        vflux = np.mean(self.flux[pixel_range])
        if vflux == 0:
            return (99, 0)
        else:
            return flux2mag(vflux.value, lbda)

    def trapezoidIntegration(self, x, y):
        """Compute the tabulated integral using a trapezoid approximation

        Parameters
        ----------
        x : array_like
            Wavelength set.

        y : array_like
            Integrand. For example, throughput or throughput
            multiplied by wavelength.

        Returns
        -------
        sum : float
            Integrated sum.

        """
        npoints = x.size
        if npoints > 0:
            indices = N.arange(npoints)[:-1]
            deltas = x[indices+1] - x[indices]
            integrand = 0.5*(y[indices+1] + y[indices])*deltas
            sum = integrand.sum()
            if x[-1] < x[0]:
                sum *= -1.0
            return sum
        else:
            return 0.0
        
    def LoadFromTxt(self, file, unitwave = u.angstrom, unitflux = (u.erg/u.s/u.cm**2/u.angstrom)):  
        """ Load fluxes from file 
        """
            
        self.wave, self.flux = np.loadtxt(file, unpack = True)
        self.wave = self.wave * unitwave
        self.flux = self.flux * unitflux
    
    def ReSampleArr(self, wave_new):   
        """Resample the flux and wave array to a new wavelength sampling
        """ 
        self.wave = self.wave.to(wave_new.unit)
        self.flux = np.interp(wave_new,self.wave,self.flux) * self.flux.unit
        self.wave = wave_new
    
    def Degrade_Resolution(self,FWHM_in, dispersion, FWHM_out):
        """Degrades the spectral resolution of the spectra using a Gaussian 1D Kernel
        """
        FWHM_dif = np.sqrt(FWHM_out**2 - FWHM_in**2)
        sigma = FWHM_dif/2.355/dispersion # Sigma difference in pixels
        gauss_1D_kernel = Gaussian1DKernel(sigma.value)
        self.flux = convolve(self.flux, gauss_1D_kernel) * self.flux.unit
        
class Template(Spectra):
    """Template objects are a sub-class of Spectra to 
    
    Template objects are a sub-class of Spectra. In addition to the attributes of 'Spectra', severals attributes store 
    general information on the type of template.
    
    Attributes
    ----------
    type_source : str
        'point-source' : point sources have fluxes in erg/s/A/cm2
        'extended' : extended sources have fluxes in erg/s/A/cm2/arcsec2
           
    z : float
        Redshift of the object
    
    magAB : float
       magAB of the normalized spectrum
    
    waveAB : float
        Wavelength of the normalisation
    
    Sampling : float
        Number of pixels per element of spectral resolution
    
    Resolution :float
         Spectral resolution
    
    """
    def __init__(self, nid, type_source='point-source'):
        Spectra.__init__(self, "Template")
        self.type_source = type_source #(point-source or surface brigthness)
        self.z = 0.0 
        self.magAB = 0.0 # flux normalised to the given magnitude (AB mags)
        self.waveAB = 0.0 # Wavelength of normalisation
        self.flux = []
        self.wave = []
        
        self.Sampling = 0.
        self.Dispersion = 0.
        self.Resolution = 0.
        self.header = ""
        
    def Load_Templates_File(self,File):
        """Load spectra from a template fits file
    
        Load spectra from a template fits file
        
        """
        try:
            fits.getdata(str(File))
        except FileNotFoundError:
            print("FITS file not found or not valid input file")
            
        HDU = fits.open(str(File))
        self.flux = HDU[0].data
        self.header = HDU[0].header
        self.wave = self.header['CRVAL1'] + self.header['CDELT1'] * np.arange(0, self.header['NAXIS1'], 1) 
        self.Resolution = self.header['R']
        self.Sampling = self.header['Sampling'] * u.pix
        self.Dispersion = self.header['CDELT1']  * u.angstrom / u.pix
        self.name = self.header['MNAME']
        
        #Convert wavelenght unit
        if self.header['TUNIT1'] in ['AA','A', 'ang','Angstroms']:
            self.wave = self.wave * u.angstrom
        if self.header['TUNIT1'] in ['nm','nanometer']:
            self.wave = self.wave * 10. * u.angstrom
            self.header['TUNIT1'] = 'Angstroms'
        if self.header['TUNIT1'] in ['micron']:    
            self.wave = self.wave * u.micron 
            self.wave = self.wave.to(u.angstrom)
        
        #Set units dependending of the source type
        if self.type_source == 'point-source':
            ergscm2A = u.erg / u.s / u.cm**2 / u.angstrom
            self.flux = self.flux * ergscm2A
        else:
            ergscm2Aarcsec2 = u.erg / u.s / u.cm**2 / u.angstrom / u.arcsec **2
            self.flux = self.flux * ergscm2Aarcsec2
                   
        
    def Redshift(self,redshift):
        """Redshift template spectrum
        """ 
        unit_wave = self.wave.unit
        lnlambdagal = np.log10(self.wave.value)
        ln_shift = np.log10(1. + redshift)
        der_lnlambdagal = lnlambdagal  + ln_shift
        self.wave = 10**(der_lnlambdagal) * unit_wave
        self.flux = self.flux.value/(1+redshift)  * self.flux.unit 
        self.z = redshift
        
    def VelocityDisp(self,FWHM_in,FWHM_out):
        """Increase the velocity dispersion of a stellar template
        """
        FWHM_dif = np.sqrt(FWHM_out**2 - FWHM_in**2)
        sigma = FWHM_dif/2.355/self.Dispersion # Sigma difference in pixels
        gauss_1D_kernel = Gaussian1DKernel(sigma.value)
        self.flux = convolve(self.flux, gauss_1D_kernel) * self.flux.unit

    def SetMagnitude(self, band, value, unit_wave = u.angstrom ):
        """Normalise the template to a given magnitude (value, band wavelength)
        """
        lbda = band[0] 
        dlbda = band[1] 
        
        ABmag = self.ABmag_band(lbda, dlbda, unit_wave = unit_wave)
        
        magDiff = value - ABmag 
        factor = 10**(-0.4*(magDiff))
        self.flux = self.flux * factor 
        self.magAB = value 
        self.waveAB = band[0]
        return     
    
class Sky(Spectra):
    """ Sky spectrum class 
    
    Sky objects are a sub-class of Spectra. 
    
    Attributes
    ----------
    type: str
        Type of sky model. e.g 'SKYCAL_local' for sky models from SkyCal ESO simulator
    
    """
    
    def __init__(self, nid):
        Spectra.__init__(self, "Sky")
        self.type = "" 
        
    def Load_ESOSkyCal_Template(self,airmass):
        """ Load ESO sky spectra from librairy
        """
        # in Vacuum
        self.type = "SKYCAL_local"
        self.model = ""
        
        #Search for closest templates in terms of airmass
        available_airmass = np.array([1.0,1.2,1.4,1.6,1.8,2.0])
        closest_airmass = available_airmass[np.argmin(np.abs(available_airmass-airmass))]
        self.model = '../models/Skymodel/SkyTemplate_ESO_a'+np.str(closest_airmass)+'.fits'
        
        try:
            fits.getdata(str(self.model))
        except FileNotFoundError:
            print("FITS file not found or not valid input file")
            
        
        HDU = fits.open(str(self.model))
        self.flux = HDU[0].data
        self.header = HDU[0].header
        
        self.wave = self.header['CRVAL1'] + self.header['CDELT1'] * np.arange(0, self.header['NAXIS1'], 1) 
        
        #Convert wavelenght unit
        if self.header['TUNIT1'] in ['AA','A', 'ang','Angstroms']:
            self.wave = self.wave * u.angstrom
        if self.header['TUNIT1'] in ['nm','nanometer']:
            self.wave = self.wave * u.nm
            self.wave = self.wave.to(u.angstrom)
            self.header['TUNIT1'] = 'Angstroms'
        if self.header['TUNIT1'] in ['micron']:    
            self.wave = self.wave * u.micron 
            self.wave = self.wave.to(u.angstrom)
            self.header['TUNIT1'] = 'Angstroms'
        
        self.Dispersion = self.header['CDELT1'] * u.angstrom / u.pix
        
        #Convert flux
        if self.header['TUNIT2'] == 'ph/s/cm2/A/arcsec2':   
            #assumes a surface brightness - flux in 1 arcsec2
            phscm2A = u.photon / u.s / u.cm**2 / u.angstrom / u.arcsec**2
            self.flux = self.flux * phscm2A 
            
    def CreateSkyMask(self,sigma=6.2):
        """ Create a mask for strong sky lines using sigma-clipping
        """
        Mask_sky = sigma_clip(self.flux.value, sigma= sigma).mask
        self.Mask = Mask_sky

class Atm_abs(Spectra):
    """ Atmospheric absorption spectra class 
    
    Atm_abs objects are a sub-class of Spectra. 
    
    Attributes
    ----------
    type: str
        Type of sky model. e.g 'SKYCAL_local' for sky models from SkyCal ESO simulator
    
    """
    
    def __init__(self, nid):
        Spectra.__init__(self, "Atm_abs")
        self.type = "" 
        
    def Load_ESOSkyCal_Template(self,airmass):
        """Load ESO atmospheric absorption spectra from library
        """
    
        self.type = "SKYCAL_local"
        self.model = ""

        #Search for closest templates in terms of airmass
        available_airmass = np.array([1.0,1.2,1.4,1.6,1.8,2.0])
        closest_airmass = available_airmass[np.argmin(np.abs(available_airmass-airmass))]
        self.model = '../models/Skymodel/SkyTemplate_ESO_a'+np.str(closest_airmass)+'.fits'
        
        try:
            fits.getdata(str(self.model))
        except FileNotFoundError:
            print("FITS file not found or not valid input file")
            
        
        HDU = fits.open(str(self.model))
        self.flux = HDU[1].data
        self.header = HDU[1].header
        
        self.wave = self.header['CRVAL1'] + self.header['CDELT1'] * np.arange(0, self.header['NAXIS1'], 1) 
        
        #Convert wavelenght unit
        if self.header['TUNIT1'] in ['AA','A', 'ang','Angstroms']:
            self.wave = self.wave * u.angstrom
        if self.header['TUNIT1'] in ['nm','nanometer']:
            self.wave = self.wave * u.nm
            self.wave = self.wave.to(u.angstrom)
            self.header['TUNIT1'] = 'Angstroms'
        if self.header['TUNIT1'] in ['micron']:    
            self.wave = self.wave * u.micron 
            self.wave = self.wave.to(u.angstrom)
            self.header['TUNIT1'] = 'Angstroms'
        
        self.Dispersion = self.header['CDELT1'] * u.angstrom / u.pix
        
        if self.header['TUNIT2'] == 'sky transmission fraction':
            self.flux = self.flux * u.dimensionless_unscaled        
        
class SimSpectrum(Spectra):
    def __init__(self, nid):
        Spectra.__init__(self, "SimSpectrum")
        
class LSF(Spectra):
    def __init__(self, nid):
        Spectra.__init__(self, "PSF")
    
    #def Load_fromFile():
        
        
def flux2mag(flux, wave):
    """Convert flux from erg.s-1.cm-2.A-1 to AB mag.

    wave is the wavelength in A

    """
    if flux > 0:
        cs = c.to('Angstrom/s').value  # speed of light in A/s
        mag = -48.60 - 2.5 * np.log10(wave ** 2 * flux / cs)
        return (mag)
    else:
        return (99)



def mag2flux(mag, wave):
    """Convert flux from AB mag to erg.s-1.cm-2.A-1

    wave is the wavelength in A

    """
    cs = c.to('Angstrom/s').value  # speed of light in A/s
    return 10 ** (-0.4 * (mag + 48.60)) * cs / wave ** 2

    