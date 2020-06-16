import numpy as np, itertools
from . import fits


# --------------------------------- #
# Class for multivariate regression #
# --------------------------------- #

class MultivariateFits(object):
  # TODO: Figure out how to use the ODR method for higher dimensions
  # TODO: Add bivariate spline interface
  # TODO: Find some way to resample the initial guesses and test the approximations

  def __init__(self, x, y, fit=None, **options):
    self._dict = {
      'chebfit2d': self._chebfit2d,
      'curve_fitnd': self._curve_fitnd,
      'odr': self._odr,
      'polyfit2d': self._polyfit2d,
      'polyfit3d': self._polyfit3d,
      'polyfit4d': self._polyfit4d,
      'polyfitnd': self._polyfitnd,
      'spline2d': self._spline2d
      }
    self.fits = list(self._dict.keys())
    
    if fit is None:
      raise Exception("No fit specified. Available fits listed in `fits` attribute.")
    else:
      self._fit = fit
      self.options = options
      
      # Perform the requested fit
      self._dict[fit](x, y, **options)
      
    self.CrossValidation = fits.CrossValidation(fit=fit, **options)
  
  
  def __getitem__(self, fit):
    return self._dict[fit]
  
  
  def __call__(self, x):
    return self.eval(x)
  
  
  def update(self, **options):
    self.options.update(options)
    self.CrossValidation = fits.CrossValidation(fit=self._fit, **self.options)
  
  
  def _chebfit2d(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.eval, self._eval = fits.chebfit2d(x, y, deg=deg, rcond=rcond)
  
  
  def _curve_fitnd(self, x, y, f=None, p0=None, maxfev=1000):
    self.options['p0'] = p0
    self.options['maxfev'] = maxfev
    
    if f is None:
      raise Exception("Must input a function.")
    else:
      self.options['f'] = f
      self.eval, self._eval = fits.curve_fitnd(x, y, f=f, p0=p0, maxfev=maxfev)
  
  
  def _odr(self):
    raise Exception("Feature not implemented yet.")
  
  
  def _polyfit2d(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.eval, self._eval = fits.polyfit2d(x, y, deg=deg, rcond=rcond)
  
  
  def _polyfit3d(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.eval, self._eval = fits.polyfit3d(x, y, deg=deg, rcond=rcond)
  
  
  def _polyfit4d(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.eval, self._eval = fits.polyfit4d(x, y, deg=deg, rcond=rcond)
  
  
  def _polyfitnd(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] =rcond
    self.eval, self._eval = fits.polyfitnd(x, y, deg=deg, rcond=rcond)
  
  
  def _spline2d(self, x, y, xdeg=5, ydeg=5, s=0):
    self.options['xdeg'] = xdeg
    self.options['ydeg'] = ydeg
    self.options['s'] = s
    self.eval, self._eval = fits.spline2d(x, y, xdeg=xdeg, ydeg=ydeg, s=s)
