"""
High-level classes for organizing, exporting, 
and importing composite data structures.
"""

__author__ = "Chad Galley <crgalley@tapir.caltech.edu, crgalley@gmail.com>"

import numpy as np, h5py
from .lib import h5open, h5close



class Data(object):
  """
  Basic data class that holds data, composes data components together,
  and includes methods to import/export data from/to HDF5 file format.
  """
  
  # TODO: Include a __call__ method for data??
  # Maybe just for composing component data 
  # but then I could just create/apply a compose attribute/method...
  
  def __init__(self, components=None, compose=None, label=None, load=None, open=None, **load_options):
    self.label = label
    self.components = []
    
    if compose is None:
      self.compose = (lambda x: x)
    else:
      self.compose = compose
    
    if components is not None:
      self.Append(components, compose=compose)
    
    # Load data if load is a filename
    if load is not None:
      assert type(load) is str, "Expecting string input for `load` option."
      self.Load(load, **load_options)
    
    # Open (not load) data file if data is a filename
    if open is not None:
      assert type(open) is str, "Expecting string input for `open` option."
      self.Open(open)
  
  
  def __getitem__(self, item):
    return self.__getattribute__(item)
  
  
  def Add(self, name, value):
    """Add attribute to Data structure"""
    self.__setattr__(name, value)
  
  
  def Delete(self, name):
    """Delete attribute from Data structure"""
    delattr(self, name)
  
  
  def Append(self, components, compose=None):
    self._Append(components, compose=compose)
  
  
  def _Append(self, components, compose=None):
    """Append component Data structure(s) to Data"""
    
    # Make components a list if not already so
    if type(components) is not list:
      components = [components]
    
    # Use the identity for composition if not specified
    if compose is None:
      self.compose = (lambda x: x)
    else:
      self.compose = compose
    
    if not hasattr(self, 'components'):
      self.__setattr__('components', [])
    
    # Get the largest counting index of unlabeled data components
    ctr = 0
    for cc in self.components:
      if cc.startswith('component'):
        cc_component = int(cc[len('component'):])
        if cc_component > ctr:
          ctr = cc_component
    
    # Loop over all the data components
    for ii, cc in enumerate(components):
      
      # Label component data with integer if no label is given
      if hasattr(cc, 'label'):
        if cc.label is None:
          ctr += 1
          self.components.append('component'+str(ctr))
        else:
          self.components.append(cc.label)
      else:
        ctr += 1
        self.components.append('component'+str(ctr))
      
      # Add each component data object as an attribute
      self.__setattr__(self.components[-1], cc)
  
  
  def Remove(self, labels, compose=None):
    self._Remove(labels, compose=compose)
  
  
  def _Remove(self, labels, compose=None):
    """Remove components from the composite data"""
    if type(labels) is not list:
      labels = [labels]
    for ii, ll in enumerate(labels):
      del self.components[self.components.index(ll)]
      self.__delattr__(ll)
    
    # Use the identity for composition if not specified
    if len(self.components) == 0:
      self.compose = None
    else:
      if compose is None:
        self.compose = (lambda x: x)
      else:
        self.compose = compose
  
  
  def Write(self, file, mode='w', exclude=None, **options):
    self._Write(file, mode=mode, exclude=exclude, **options)
  
  
  def _Write(self, file, mode='w', writedata=True, exclude=None, close=True, **options):
    """Write composite data to HDF5 file format"""
    
    _exclude = ['compose', 'label', 'components']
    if exclude is None:
      exclude = _exclude
    else:
      if type(exclude) is str:
        exclude = [exclude]
      exclude.extend(_exclude)
    
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
              if writedata:
                try:
                  fp.create_dataset(kk, data=vv, **h5options)
                except:
                  fp.create_dataset(kk, data=vv)
      else:
        for cc in self.components:
          group = fp.create_group(cc)
          self.__getattribute__(cc).Write(group, **options)
          
      # Close the file if fp is a File descriptor
      if close:
        h5close(fp)
    
    return fp
  
  
  def Load(self, file, exclude=None, structure=None, **options):
    self._Load(file, exclude=exclude, structure=structure, **options)
  
  
  def _Load(self, file, exclude=None, structure=None, **options):
    """Load composite data from HDF5 file format"""
    
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
      # if structure is None:
      #   structure = Data()
      for kk in list(self._fp.keys()):
        if kk not in exclude:
          item = self._fp[kk]
          if type(item) is h5py._hl.group.Group:
            self.components.append(kk)
            self.__setattr__(kk, Data())
            self.__getattribute__(kk)._Load(item, exclude=exclude, **options)
          elif type(item) is h5py._hl.dataset.Dataset:
            try:
              self.__setattr__(kk, item[:])
            except:
              self.__setattr__(kk, item[()])
        
      # Close the file if fp is a File descriptor
      self._isopen = h5close(self._fp)
  
  
  def Open(self, file):
    self._Open(file)
  
  
  def _Open(self, file):
    """Open composite data from HDF5 file format without loading data"""
    # FIXME: The components inherit this method...
    self._fp, self._isopen = h5open(file, 'r')
    
    if self._isopen:
      self.components = []
      for kk in list(self._fp.keys()):
        if type(self._fp[kk]) is h5py._hl.group.Group:
          self.components.append(kk)
          self.__setattr__(kk, Data())
          #self.__getattribute__(kk).load(self._fp[kk], **options)
  
  
  def Close(self):
    """Close composite data HDF5 file"""
    # FIXME: The components inherit this method...
    if self._isopen:
      self._isopen = h5close(self._fp)
    else:
      print("File not open.")



