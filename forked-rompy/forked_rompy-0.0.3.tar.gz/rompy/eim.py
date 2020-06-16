import numpy as np
from scipy.linalg.lapack import get_lapack_funcs
from .lib import malloc


class _EmpiricalInterpolation(object):
  """
  Class for building an empirical interpolant given a reduced basis
  """
  
  def __init__(self):
    pass
  
  def malloc(self, Nbasis, Nquads, Nmodes=1, dtype='complex'):
    self.indices = malloc('int', Nbasis) 
    self.invV = malloc(dtype, Nbasis, Nbasis) 
    self.R = malloc(dtype, Nbasis, Nquads)
    self.B = malloc(dtype, Nbasis, Nquads)
  
  def coefficient(self, invV, e, indices):
    return np.dot(invV.T, e[indices])
  
  def residual(self, e, c, R):
    """Difference between a basis function 'e' and its empirical interpolation"""
    return e - np.dot(c, R)
  
  def next_invV_col(self, R, indices, check_finite=False):
    b = np.zeros(len(indices), dtype=R.dtype)
    b[-1] = 1.
    return _solve_triangular(R[:,indices], b, lower=False, check_finite=check_finite)
  
  def interpolant(self, invV, R):
    """The empirical interpolation matrix `B`"""
    return np.dot(invV, R)
  
  def interp(self, h, indices, B):
    """Empirically interpolate a function"""
    dim = np.shape(h)
    if len(dim) == 1:
      return np.dot(h[indices], B)
    elif len(dim) > 1:
      return np.array([np.dot(h[ii][indices], B) for ii in range(dim[0])])


class EmpiricalInterpolant(_EmpiricalInterpolation):
  
  def __init__(self, basis=None, seed=None, make=True, verbose=False, timer=False):
    _EmpiricalInterpolation.__init__(self)
    
    if basis is not None:
      if type(basis) is np.ndarray:
        self._Nbasis = len(basis)
        if make:
          self.make(basis, seed=seed, verbose=verbose, timer=timer)
          self.make_interpolant()
      else:
        raise Exception("Expecting numpy array of basis vectors.")
    elif basis is None and make:
      raise Exception("Must input an array of basis vectors to make the empirical interpolant.")
    else:
      print ("No basis vectors given.")
  
  
  def seed(self, e, seed=None):
    """Seed the algorithm"""
    
    # Extract dimensions of basis
    dim = np.shape(np.asarray(e))
    if len(dim) == 1:
      Nsamples = dim[0]
      Nmodes = 1
    elif len(dim) == 2:
      Nsamples, Nmodes = dim
    else:
      raise Exception("Unexpected dimensions for basis vector.")
    
    # Allocate memory for greedy algorithm arrays
    dtype = type(np.asarray(e).flatten()[0])
    self.malloc(self._Nbasis, Nsamples, Nmodes=Nmodes, dtype=dtype)
    
    # Seed
    if seed is None:
      self.indices[0] = np.argmax(np.abs(e))
    else:
      self.indices[0] = seed
    self.R[0] = e
    self.invV[:1,:1] = self.next_invV_col(self.R[:1], self.indices[:1])

  def iter(self, step, e):
    """One iteration in the empirical interpolation greedy algorithm"""
    ctr = step+1
    
    # Compute interpolant residual
    c = self.coefficient(self.invV[:ctr,:ctr], e, self.indices[:ctr])
    r = self.residual(e, c, self.R[:ctr])
    
    # Update
    self.indices[ctr] = np.argmax(np.abs(r))
    self.R[ctr] = r
    self.invV[:,ctr][:ctr+1] = self.next_invV_col(self.R[:ctr+1], self.indices[:ctr+1])

  def make(self, basis, seed=None, verbose=False, timer=False):
    """Make an empirical interpolant using the standard greedy algorithm"""
    
    # Seed the greedy algorithm
    self.seed(basis[0], seed=seed)
    
    # EIM algorithm with reduced complexity for inverting the van der Monde matrix
    if verbose:
      print(("\nStep", "\t", "Nodes"))
    if timer:
      t0 = time.time()

    for nn in range(self._Nbasis):
      if verbose:
        print((nn+1, "\t", self.indices[nn]))
        
      # Single iteration
      if nn == self._Nbasis-1:
        break
      else:
        self.iter(nn, basis[nn+1])
      
    if timer:
      print(("\nElapsed time =", time.time()-t0))
    
    # Compute interpolant matrix 'B'
    assert self._Nbasis == len(self.indices), "Number of nodes not equal to size of basis."
    self.trim(self._Nbasis)
    self.make_interpolant()
    self.size = self._Nbasis
    
  def make_interpolant(self):
    self.B = self.interpolant(self.invV, self.R)
    
  def interpolate(self, h):
    return self.interp(h, self.indices, self.B)
    
  def trim(self, num):
    """Trim arrays to have size num"""
    if num > 0:
      self.indices = self.indices[:num]
      self.R = self.R[:num]
      self.invV = self.invV[:num,:num]
      self.B = self.B[:num,:]
  
  def make_data(self, training_space):
    """
    Assemble training space data at empirical interpolant 
    nodes for the purposes of fitting
    """
    self.data = np.transpose(training_space)[self.indices]


##########################################
# Linear algebra helper functions needed #
#    for EmpiricalInterpolation class    #
##########################################

# This is scipy.linalg's source code. For some reason my scipy doesn't recognize
# the check_finite option, which may help with speeding up. Because this may be an 
# issue related to the latest scipy.linalg version, I'm reproducing the code here
# to guarantee future compatibility.

def _solve_triangular(a, b, trans=0, lower=False, unit_diagonal=False, \
                      overwrite_b=False, debug=False, check_finite=True):
  """
  Solve the equation `a x = b` for `x`, assuming a is a triangular matrix.
  
  Parameters
  ----------
  a : (M, M) array_like
      A triangular matrix
  b : (M,) or (M, N) array_like
      Right-hand side matrix in `a x = b`
  lower : boolean
      Use only data contained in the lower triangle of `a`.
      Default is to use upper triangle.
  trans : {0, 1, 2, 'N', 'T', 'C'}, optional
      Type of system to solve:
  
      ========  =========
      trans     system
      ========  =========
      0 or 'N'  a x  = b
      1 or 'T'  a^T x = b
      2 or 'C'  a^H x = b
      ========  =========
  unit_diagonal : bool, optional
      If True, diagonal elements of `a` are assumed to be 1 and
      will not be referenced.
  overwrite_b : bool, optional
      Allow overwriting data in `b` (may enhance performance)
  check_finite : bool, optional
      Whether to check that the input matrices contain only finite numbers.
      Disabling may give a performance gain, but may result in problems
      (crashes, non-termination) if the inputs do contain infinities or NaNs.
  
  Returns
  -------
  x : (M,) or (M, N) ndarray
      Solution to the system `a x = b`.  Shape of return matches `b`.
  
  Raises
  ------
  Exception
      If `a` is singular
  
  Notes
  -----
  .. versionadded:: 0.9.0
  
  """
  
  if check_finite:
      a1, b1 = list(map(np.asarray_chkfinite,(a,b)))
  else:
      a1, b1 = list(map(np.asarray, (a,b)))
  if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
      raise ValueError('expected square matrix')
  if a1.shape[0] != b1.shape[0]:
      raise ValueError('incompatible dimensions')
  overwrite_b = False #overwrite_b or _datacopied(b1, b)
  if debug:
      print(('solve:overwrite_b=',overwrite_b))
  trans = {'N': 0, 'T': 1, 'C': 2}.get(trans, trans)
  trtrs, = get_lapack_funcs(('trtrs',), (a1,b1))
  x, info = trtrs(a1, b1, overwrite_b=overwrite_b, lower=lower, trans=trans, unitdiag=unit_diagonal)
  
  if info == 0:
      return x
  if info > 0:
      raise Exception("singular matrix: resolution failed at diagonal %s" % (info-1))
  raise ValueError('illegal value in %d-th argument of internal trtrs' % -info)

# def _transpose(a):
#   dim = a.shape
#   if len(dim) != 2:
#     raise ValueError('Expected a matrix')
#   aT = np.zeros(dim[::-1], dtype=a.dtype)
#   for ii, aa in enumerate(a):
#     aT[:,ii] = a[ii]
#   return aT
