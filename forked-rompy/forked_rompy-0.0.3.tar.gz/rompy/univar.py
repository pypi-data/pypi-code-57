import numpy as np
from . import fits


# ------------------------------- #
# Class for univariate regression #
# ------------------------------- #

class UnivariateFits(object):
  
  def __init__(self, x, y, fit=None, params=None, **options):
    self._dict = {
      'chebfit': self._chebfit,
      'curve_fit': self._curve_fit,
      'fourier': self._fourier,
      'greedy': self._greedy,  # TODO: Maybe make this an option for each fit type?
      'legfit': self._legfit,
      'localreg': self._local_regression,
      'odr': self._odr,
      'polyfit': self._polyfit,
      # 'romSpline': self._romSpline,
      'spline': self._spline,
      }
    self.fits = list(self._dict.keys())
    self._params = params
    
    if fit is None:
      raise Exception("No fit specified. Available fits listed in `fits` attribute.")
    else:
      self._fit = fit
      self.options = options
      
      # Perform the requested fit
      self._dict[fit](x, y, **options)
    
    self._x_dim = np.shape(x)
    self._y_dim = np.shape(y)
    self.dim = self._x_dim[0]
    
    self.CrossValidation = fits.CrossValidation(fit=fit, **options)
  
  
  def __getitem__(self, fit):
    return self._dict[fit]
  
  
  def __call__(self, x):
    return self.eval(x)
  
  
  def update(self, **options):
    self.options.update(options)
    self.CrossValidation = fits.CrossValidation(fit=self._fit, **self.options)
  
  
  def _chebfit(self, x, y, deg=3, rcond=None, full=False, w=None):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.options['full'] = full
    self.options['w'] = w
    self.eval, self._eval = fits.chebfit(x, y, deg=deg, rcond=rcond, full=full, w=w)
    
  
  def _fourier(self, x, y, deg=3, rcond=-1):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.eval, self._eval = fits.fourier(x, y, deg=deg, rcond=rcond)
  
  
  def _curve_fit(self, x, y, f=None, p0=None, maxfev=1000):
    self.options['p0'] = p0
    self.options['maxfev'] = maxfev
    
    if f is None:
      raise Exception("Must input a function.")
    else:
      self.options['f'] = f
      self.eval, self._eval = fits.curve_fit(x, y, f=f, p0=p0, maxfev=maxfev)
  
  
  def _greedy(self):
    raise Exception("Feature not implemented yet.")
  
  
  def _legfit(self, x, y, deg=3, rcond=None, full=False, w=None):
    self.options['deg'] = deg
    self.options['rcond'] = rcond
    self.options['full'] = full
    self.options['w'] = w
    self.eval, self._eval = fits.legfit(x, y, deg=deg, rcond=rcond, full=full, w=w)
  
  
  def _local_regression(self, x, y, deg=3, window=None, weights=None):
    """Local regression for a single value of x"""
    self.options['deg'] = deg
    self.options['weights'] = weights
    
    if window is None:
      win = deg
    else:
      win = window
    self.options['window'] = win
    
    self.eval = fits.local_regression(x, y, deg=deg, window=win, weights=weights)
  
  
  def _odr(self, x, y, f=None, p0=None):
    """Orthogonal Distance Regression"""
    if p0 is None:
      p0 = np.ones()
    self.options['p0'] = p0
    
    if f is None:
      raise Exception("Must input a function.")
    else:
      self.options['f'] = f
      self.eval, self._eval = fits.odr(x, y, f=f, p0=p0)
  
  
  def _polyfit(self, x, y, **options):
    self._options = options
    if self._params is None:
      self.eval, self._eval = fits.polyfit(x, y, **options)
    else:
      self._eval = self._params
      self.eval = fits.polyEval(self._params)
  
  
  # def _romSpline(self, x, y, deg=5, tol=1e-6, rel=False, verbose=False, seeds=None):
  #   """Builds a reduced-order spline interpolant of degree deg from (x,y data)
  #   and accurate to a tolerance of tol.
  #
  #   Input:
  #   ------
  #   x       -- samples
  #   y       -- values to interpolate
  #   deg     -- spline degree or order
  #              (default is 5)
  #   tol     -- tolerance threshold for spline to reproduce y values
  #              (default is 1e-6)
  #   rel     -- Use relative errors for termination of greedy algorithm
  #              (default False)
  #   verbose -- Verbose output from greedy algorithm
  #              (default False)
  #   seeds   -- (deg+1) array indices to seed the greedy algorithm.
  #              (default is None, which uses equally spaced samples)
  #   """
  #   self.options['deg'] = deg
  #   self.options['tol'] = tol
  #   self.options['rel'] = rel
  #   self.options['seeds'] = seeds
  #   self.eval, self._eval = fits.rom_spline(x, y, deg=deg, tol=tol, rel=rel, verbose=verbose, seeds=seeds)
    
  
  def _spline(self, x, y, deg=5, s=0):
    """Builds a univariate spline interpolant of degree deg from (x,y) data.
    
    Input
    -----
    x   -- samples
    y   -- values to interpolate
    deg -- spline degree or order
           (default is 5)
    s   -- degree of smoothing
           (default is 0)
    """
    self.options['deg'] = deg
    self.options['s'] = s
    self.eval, self._eval = fits.spline(x, y, deg=deg, s=s)

