"""
High-level classes and functions for building a reduced-order surrogate model.
"""

__author__ = "Chad Galley <crgalley@tapir.caltech.edu, crgalley@gmail.com>"

import numpy as np, time, os, h5py
from scipy.interpolate import UnivariateSpline
from .integrals import Integration
from .greedy import ReducedBasis
from .eim import EmpiricalInterpolant
from .univar import UnivariateFits
from .multivar import MultivariateFits
from .lib import string_to_chars, chars_to_string, get_arg, h5open, h5close
from .data import Data



class Surrogate(Data):
  
  def __init__(self, inner=None, rb=None, ei=None, fits=True, components=None, compose=None, pmap=None, label=None, load=None, exclude=None, open=None, **load_options):
    
    Data.__init__(self, components=components, compose=compose, label=label, load=load, open=open, **load_options)
    
    self._inner = inner
    
    if rb is None and ei is None:
      self._rb_made = False
      self._ei_made = False
    else:
      if rb is not None:
        if load is None:
          assert isinstance(rb, ReducedBasis), "Expecting rompy.ReducedBasis class instance."
          self.rb = rb
          self._rb_made = True
          if ei is not None:
            assert isinstance(ei, EmpiricalInterpolant), "Expecting rompy.EmpiricalInterpolant class instance."
            self.ei = ei
            if hasattr(ei, 'data'):
              self._ei_made = True
            else:
              print (">>> Warning(No empirical interpolant data): Run `EmpiricalInterpolant.make_data` method.")
              self._ei_made = False
      else:
        if ei is not None:
          if load is None:
            raise Exception("Must also input a rompy.ReducedBasis class instance.")
    
    self._fits_made = False
    
    if self.components == []:
      self.map = (lambda x: x)
    
    # Load component surrogate data from filename given in `load`
    if load is not None:
      assert type(load) is str, "Expecting string input for `load`."
      
      if exclude is None:
        exclude = []
      else:
        if type(exclude) is str:
          exclude = [exclude]
        assert type(exclude) is list, "Expecint list or string input for `exclude` option."
      
      if rb is False:
        exclude.extend(['rb'])
        self._rb_made = False
      else:
        self._rb_made = True
      if ei is False:
        exclude.extend(['ei'])
        self._ei_made = False
      else:
        self._ei_made = True
      if fits is False:
        exclude.extend(['fits'])
        self._fits_made = False
      else:
        self._fits_made = True
      
      self.Load(load, exclude=exclude, structure=Surrogate(), **load_options)
    
    if self._rb_made and self._ei_made:
      self._rom_made = True
    else:
      self._rom_made = False
  
  
  def MakeRB(self, training, seed, tol, num=None, loss='L2', rel=False, verbose=False, timer=False):
    # Throw a warning to the user that reduced basis data is present
    if self._rb_made:
      print (">>> Warning(Reduced basis data exists) Data will be overwritten.")
      self._rb_made = False

    # Build reduced basis
    if self._inner is not None:
      self.rb = ReducedBasis(self._inner, loss=loss)
    else:
      raise Exception("Integration rule, nodes, and weights not given.\nPopulate the `_inner` attribute with a rompy.Integration instance.")
    self.rb.make(training, seed, tol, num=num, rel=rel, verbose=verbose, timer=timer)
    # TODO: Keep rb.points attribute?
    #self.rb.points = np.asarray(training)[self.rb.indices]
    self._rb_made = True
    
    if not self._rb_made:
      self._rb_made = True
  
  
  def MakeEI(self, verbose=False, timer=False):
    # Throw a warning to the user that empirical interpolant data is present
    if self._ei_made:
      print (">>> Warning(Empirical interpolant data exists) Data will be overwritten.")
      self._ei_made = False
    
    if self._rb_made:
      self.ei = EmpiricalInterpolant(self.rb.basis, make=True, verbose=verbose, timer=timer)
      
    if not self._ei_made:
      self._ei_made = True
    if self._rb_made and self._ei_made:
      self._rom_made = True
    else:
      self._rom_made = False
  
  
  def MakeROM(self, training, seed, tol, num=None, loss='L2', rel=False, verbose=False, timer=False):
    # Build reduced basis
    self.MakeRB(training=training, seed=seed, tol=tol, num=num, loss=loss, rel=rel, verbose=verbose, timer=timer)
    
    # Build empirical interpolant
    #self.MakeEI(self.rb.basis, verbose=verbose, timer=timer)
    self.MakeEI(verbose=verbose, timer=timer)
    self.ei.make_data(training)
    #self.ei.make_data(training[self.rb.indices])
    
    if self._rb_made and self._ei_made:
      self._rom_made = True
    else:
      self._rom_made = False
  
  
  # TODO: Add a method for viewing the empirical data
  # for the purposes of assessing data quality and to
  # identify outlier data that would otherwise contaminate
  # a fit.
  # OR: Associate a large uncertainty with outlier data points.
  # But the problem then is that not every fitting function can
  # accomodate uncertainties...
  # Better yet: Use Huber's penalty function to weigh outliers less
  
  
  def Assess1dData(self, x, xlabel=None, ylabel=None, loc='lower left'):
    try:
      import matplotlib.pyplot as plt
    except ImportError:
      print ("Cannot import matplotlib.pyplot module.")
    assert hasattr(self, 'ei'), "No empirical interpolant data. \n>>> Run `make_ei` or `make_rom` methods <<<"
    assert hasattr(self.ei, 'data'), "Empirical interpolant data not assembled for fitting. \n>>> Run `ei.make_data` method <<<"
    assert hasattr(self.ei, 'indices'), "Indices of empirical interpolant nodes not found."
    
    # Plot 1d data at each empirical node
    for ii, dd in enumerate(self.ei.data):
      plt.plot(x, dd, 'ko', label='Node index = '+str(self.ei.indices[ii]))
      if xlabel is not None:
        plt.xlabel(xlabel)
      if ylabel is not None:
        plt.ylabel(ylabel)
      plt.legend(loc=loc)
      plt.show()
  
  
  def MakeFits(self, x, cut=None, **options):
    assert hasattr(self, 'ei'), "No empirical interpolant data. \n>>> Run `make_ei` or `make_rom` methods <<<"
    assert hasattr(self.ei, 'data'), "Empirical interpolant data not assembled for fitting. \n>>> Run `ei.make_data` method <<<"
    if hasattr(self.ei, 'data') and not self._ei_made:
      self._ei_made = True
      if self._rb_made:
        self._rom_made = True
    
    # TODO: Test this
    # NOTE: The cut on the data does not propagate to the fitting yet
    mask = np.ones(len(x), dtype='bool')
    if cut is not None:
      if type(cut) is not list:
        cut = [cut]
      for cc in cut:
        mask[cc] = False
    
    dim = len(np.shape(x))
    if dim == 1:
      self.fits = UnivariateFits(x, self.ei.data, **options)
    elif dim > 1:
      # TODO: Need to finish accommodating multi-dim y-data
      self.fits = MultivariateFits(x, self.ei.data, **options)
    else:
      raise Exception("Shape of input data %s not understood." % x)
    self._fits_made = True
  
  
  def Assess1dFits(self, x, X, pmap=None, xlabel=None, ylabel=None, loc='lower left'):
    try:
      import matplotlib.pyplot as plt
    except ImportError:
      print ("Cannot import matplotlib.pyplot module.")
    assert hasattr(self, 'ei'), "No empirical interpolant data. \n>>> Run `make_ei` or `make_rom` methods <<<"
    assert hasattr(self.ei, 'data'), "Empirical interpolant data not assembled for fitting. \n>>> Run `ei.make_data` method <<<"
    assert hasattr(self.ei, 'indices'), "Indices of empirical interpolant nodes not found."
    assert hasattr(self, 'fits'), "No fit information found. \n>>> Run `make_fits` method <<<"
    
    # Plot 1d data at each empirical node
    if pmap is None:
      pmap = (lambda y: y)
    fits = self.fits(pmap(X))
    for ii, dd in enumerate(self.ei.data):
      plt.plot(x, dd, 'ko', label='Node index = '+str(ii)+', '+str(self.ei.indices[ii]))
      plt.plot(X, fits[ii], 'k-')
      if xlabel is not None:
        plt.xlabel(xlabel)
      if ylabel is not None:
        plt.ylabel(ylabel)
      if loc is not False:
        if loc is not None:
          plt.legend(loc=loc)
      plt.show()
  
  
  def UpdateFits(self, x, cut, **options):
    assert type(cut) is list, "Expecting list for `cut`"
    
    mask = np.ones(len(x), dtype='bool')
    for cc in cut:
      mask[cc] = False
    
    dim = len(np.shape(x))
    if dim == 1:
      for ii, dd in enumerate(self.ei.data):
        fit = UnivariateFits(x[mask], dd[mask], **options)
        self.fits._eval[ii] = fit._eval
    elif dim > 1:
      for ii, dd in enumerate(self.ei.data):
        fit = MultivariateFits(x[mask], dd[mask], **options)
        self.fits._eval[ii] = fit._eval
  
  
  def Append(self, components, compose=None, pmap=None):
    
    # Use the identity for the parameter map if not specified
    # TODO: Fix this to carry over a previously defined map (?)
    self.map = pmap
    if pmap is None:
      self.map = (lambda x: x)
    
    self._Append(components, compose=compose)
  
  
  def Remove(self, labels, compose=None, pmap=None):
    """Remove surrogates from the composite surrogate."""
    
    if len(self.components) == 0:
      self.map = None
    else:
      self.map = pmap
      if pmap is None:
        self.map = (lambda x: x)
    
    self._Remove(labels, compose=compose)
  
  
  def __call__(self, x, t=None, deg=5, compose=True, **options):
    return self.Eval(x, t=t, deg=deg, compose=True, **options)
  
  
  def Eval(self, x, t=None, deg=5, compose=True, **options):
    """Evaluate the composite surrogate at samples x."""
    # TODO: Allow for Y to be multi-dimensional for the spline fitting
    #if self.components != []:
    # Evaluate the component surrogates and then compose the result
    X = self.map(x)
    if len(self.components) == 0:
      y = np.dot(self.fits(X), self.ei.B)
    elif len(self.components) == 1:
      y = self.__getattribute__(self.components[0]).Eval(X)
    else:
      y = [self.__getattribute__(ll).Eval(X) for ll in self.components]

    if compose:
      Y = np.asarray(self.compose(y, **options))
    else:
      Y = np.asarray(y)
    
    # Resample output at new samples, if requested
    if t is None:
      return Y
    else:
      if Y.dtype in ['complex128', 'complex64', 'complex32']:
        re = UnivariateSpline(self._inner.nodes, Y.real, s=0, k=deg)(t)
        im = UnivariateSpline(self._inner.nodes, Y.imag, s=0, k=deg)(t)
        return re+1j*im
      else:
        return UnivariateSpline(self._inner.nodes, Y, s=0, k=deg)(t)
  
  
  def Write(self, file, rb=True, ei=True, fits=True, alpha=False, mode='w', exclude=None, close=True, **options):
    """Write composite surrogate data to HDF5 file format."""
    # TODO: Allow option to write a specific component surrogate(s)
    
    _exclude = ['compose', 'label', 'components', 'map']
    #_exclude = ['compose', 'components', 'map']
    if exclude is None:
      exclude = _exclude
    else:
      if type(exclude) is str:
        exclude = [exclude]
      if type(exclude) is list:
        exclude.extend(_exclude)
      else:
        raise Exception("Expecting list or string input for `exclude` option.")
    
    assert mode in ['w', 'a'], "Expecting either write ('w') or append ('a') modes."
    fp, isopen = h5open(file, mode)
    
    if isopen:
      # H5 compression options if not specified in `options`
      h5options = {}
      if not hasattr(options, 'compression'):
        h5options['compression'] = 'gzip'
      if not hasattr(options, 'shuffle'):
        h5options['shuffle'] = True
      
      # Make each component a group and call the component's write method
      if self.components == []:
        for kk, vv in self.__dict__.items():
          if not kk.startswith('_'):
            if kk not in exclude:
              if kk not in ['rb', 'ei', 'fits']:
                try:
                  fp.create_dataset(kk, data=vv, **h5options)
                except:
                  fp.create_dataset(kk, data=vv)
              else:
                if kk == 'rb' and rb:
                  self._WriteRB(fp, alpha=alpha, **h5options)
                if kk == 'ei' and ei:
                  self._WriteEI(fp, exclude=exclude, **h5options)
                if kk == 'fits' and fits:
                  self._WriteFits(fp, **h5options)
      else:
        for cc in self.components:
          group = fp.create_group(cc)
          self.__getattribute__(cc).Write(group, rb=rb, ei=ei, fits=fits, exclude=exclude, alpha=alpha, **options)
          
      # Close the file if fp is a File descriptor
      if close:
        h5close(fp)
  
  
  def _WriteRB(self, descriptor, alpha=False, **options):
    
    assert hasattr(self, '_rb_made')
    if self._rb_made and hasattr(self, 'rb'):
      rb_group = descriptor.create_group('rb')
      if hasattr(self.rb, 'indices'):
        rb_group.create_dataset('indices', 
                                data=self.rb.indices, 
                                dtype='int', 
                                **options)
      if hasattr(self.rb, 'points'):
        rb_group.create_dataset('points', 
                                data=self.rb.points,
                                dtype=self.rb.points.dtype, 
                                **options)
      if hasattr(self.rb, 'basis'):
        rb_group.create_dataset('basis', 
                                data=self.rb.basis, 
                                dtype=self.rb.basis.dtype, 
                                **options)
      if hasattr(self.rb, 'errors'):
        rb_group.create_dataset('errors', 
                                data=self.rb.errors, 
                                dtype=self.rb.errors.dtype, 
                                **options)
      if alpha:
        if hasattr(self.rb, 'alpha'):
          rb_group.create_dataset('alpha',
                                  data=self.rb.alpha,
                                  dtype=self.rb.alpha.dtype,
                                  **options)
    else:
      print ("No reduced basis data to export to file.")
  
  
  def _WriteEI(self, descriptor, exclude=None, **options):
    
    assert hasattr(self, '_ei_made')
    
    # Compile list of excluded data labels
    _exclude = []
    if type(exclude) is str:
      exclude = [exclude]
    if type(exclude) is list:
      exclude.extend(_exclude)
    else:
      raise Exception("Expecting list or string input for `exclude` option.")
    
    if self._ei_made and hasattr(self, 'ei'):
      ei_group = descriptor.create_group('ei')
      if 'indices' not in exclude:
        if hasattr(self.ei, 'indices'):
          ei_group.create_dataset('indices', 
                                  data=self.ei.indices, 
                                  dtype='int', 
                                  **options)
      if 'B' not in exclude:
        if hasattr(self.ei, 'B'):
          ei_group.create_dataset('B', 
                                  data=self.ei.B, 
                                  dtype=self.ei.B.dtype, 
                                  **options)
      if 'data' not in exclude:
        if hasattr(self.ei, 'data'):
          ei_group.create_dataset('data', 
                                  data=self.ei.data, 
                                  dtype=self.ei.data.dtype, 
                                  **options)
    else:
      print ("No empirical interpolation data to export to file.")
  
  
  def _WriteFits(self, descriptor, **options):
    
    assert hasattr(self, '_fits_made')
    if self._fits_made and hasattr(self, 'fits'):
      fits_group = descriptor.create_group('fits')
      if hasattr(self.fits, '_fit'):
        fits_group.create_dataset('fit_type', 
                                data=string_to_chars(self.fits._fit),
                                dtype='int')
      if self.fits._fit.startswith('spline'):
        # FIXME: Check for dimension of _eval array
        fit_params = fits_group.create_group('fit_params')
        dim = len(np.shape(self.fits._eval))
        if dim == 1:
          fit_params.create_dataset('x_knots',
                                    data=np.array(self.fits._eval[0]),
                                    **options)
          fit_params.create_dataset('y_knots',
                                    data=np.array(self.fits._eval[1]),
                                    **options)
          fit_params.create_dataset('coefficients',
                                    data=np.array(self.fits._eval[2]),
                                    **options)
        elif dim > 1:
          fit_params.create_dataset('x_knots',
                                    data=np.array(self.fits._eval[0][0]),
                                    **options)
          fit_params.create_dataset('y_knots',
                                    data=np.array(self.fits._eval[0][1]),
                                    **options)
          fit_params.create_dataset('coefficients',
                                    data=np.array([ee[2] for ee in self.fits._eval]),
                                    **options)
        else:
          print ("Dimension of fitting parameters in fits._eval are unexpected. Proceeding without writing these to file.")
      else:
        if hasattr(self.fits, '_eval'):
          fits_group.create_dataset('fit_params', 
                                  data=np.array(self.fits._eval), 
                                  **options)
      if hasattr(self.fits, 'options'):
        if self.fits.options is not None or self.fits.options != {}:
          options = fits_group.create_group('options')
          for kk, oo in self.fits.options.items():
            try:
              if oo is not None:
                options.create_dataset(kk, data=oo)
            except:
              print(("Cannot write fits option {} to file.".format(kk)))
        
    else:
      print ("No fits data to export to file.")
  
  
  def Load(self, file, exclude=None, **options):
    """Load composite surrogate data from HDF5 file format"""
    
    # Compile list of excluded data labels
    _exclude = []
    if exclude is None:
      exclude = _exclude
    else:
      if type(exclude) is str:
        exclude = [exclude]
      exclude.extend(_exclude)
    
    self._fp, self._isopen = h5open(file, 'r')
    
    # If file is a file or group descriptor then file should already be open
    if self._isopen:
      self.components = []
      # items = []
      # self._fp.visit(items.append)
      for kk in list(self._fp.keys()):
        if kk not in exclude:
          # for ii in items:
          #   split = kk.split('/')
          #   if len(split) > 1:
          #     if split[1] in ['rb', 'ei', 'fits']:
          #       structure = Surrogate()
          #   else:
          #     structure = Data()
          item = self._fp[kk]
          if type(item) is h5py._hl.group.Group:
            self.components.append(kk)
            #self.__setattr__(kk, structure)
            self.__setattr__(kk, Surrogate())
            self.__getattribute__(kk)._Load(item, exclude=exclude, **options)
          elif type(item) is h5py._hl.dataset.Dataset:
            try:
              self.__setattr__(kk, item[:])
            except:
              self.__setattr__(kk, item[()])
          
      # Close the file if fp is a File descriptor
      self._isopen = h5close(self._fp)
