import numpy as np, itertools
from scipy.special import factorial
from scipy.interpolate import UnivariateSpline
from scipy.optimize import leastsq
from scipy import odr
from numpy.polynomial import legendre
from numpy.polynomial import chebyshev

# For building reduced-order splines
# try:
#   import romspline
#   _romspline = True
# except:
#   print "Cannot load romSpline module."
#   _romspline = False

from . import lib

# For parallelization
try:
  from concurrent.futures import ProcessPoolExecutor, wait, as_completed
  from multiprocessing import cpu_count
  _futures = True
except:
  print ("Cannot load `concurrent.futures` or `multiprocessing` modules for parallel computing.")
  _futures = False


def Fitting(object):
  
  def __init__(self):
    pass
  
  def fit(self):
    pass
  
  def eval(self):
    pass



####################
# Helper functions #
####################

def _map_poly_coeffs(coeffs, x, a, b):
  """Map polynomial coefficients of p(x) to the polynomial on the interval [a,b]"""
  
  # Linear transformation from x to [a,b]
  M = (np.max(x)-np.min(x))/(b-a)
  B = np.min(x)-M*a
  
  # Map the polynomial coefficients
  deg, mapped_coeffs = len(coeffs), []
  c = coeffs[::-1]	# Reverse order of polynomial coefficients
  for n in range(deg):
    mapped_coeffs.append( M**n*np.sum(lib.choose(kk,n)*c[kk]*B**(kk-n) for kk in range(n,deg)) )
  
  # Reverse order of polynomial coefficients for use with np.polyval
  return mapped_coeffs[::-1]


def get_arg(a, x):
  """Get index of array a that has the closest value to x"""
  return abs(a-x).argmin()


def make_patch(x, x_grid, dim):
  """Make patch with dim elements centered around x"""
  
  # Find grid points closest to x
  ix = get_arg(x_grid, x)
  
  # Find how many elements to take on either side of x
  if dim % 2:    # Check if dim is odd...
    a = int((dim+1)/2.)
    b = a
  else:          #...or even
    a = int(dim/2.)
    b = a+1
  
  # Ensure patch doesn't cross the training grid boundary
  ix = check_patch(ix, a, b, x_grid.size)
  
  # Indices of the patch 
  ipatch = np.arange(ix-a, ix+b)
  return ipatch, ix, get_arg(ipatch, ix)


def check_patch(i, dileft, diright, dim):
  """Check if i is too close to interval endpoints and adjust if so."""
  if i <= dileft: 
    ans = dileft
  elif dim-i <= diright: 
    ans = dim-diright
  else:
    ans = i
  return ans


# TODO: Extend this to different degrees/orders in different dims
def number_of_terms(deg, dim):
  """Calculate the number of terms in a polynomial of degree deg of dim number of variables"""
  ans = np.sum(factorial(ii+dim-1.)/factorial(ii) for ii in range(deg+1))
  return int(ans / factorial(dim-1))

# TODO: Extend this to different degrees/orders in different dims
def make_orders(deg, dim):
  num = number_of_terms(deg, dim)
  ans = np.zeros((num, dim), dtype='int')
  ranges = [list(range(deg+1))]*dim
  ijs = itertools.product(*ranges)
  ctr = 0
  for kk, inds in enumerate(ijs):
    if sum(inds) <= deg:
      ans[ctr] = inds
      ctr += 1
  return ans


def delta(x, x0):
  """Kronecker delta-like function"""
  return 1. * (x == x0)


#########################
# Univariate regression #
#########################

def chebfit(x, y, deg=3, rcond=None, full=False, w=None):
  # TODO: Add support for 2d y array
  args = np.argsort(x)
  dim_y = len(np.shape(y))
  if dim_y == 1:
    _eval = chebyshev.chebfit(x[args], y[args], deg, rcond=rcond, full=full, w=w)
    def ans(x):
      return chebyshev.chebval(x, _eval)
  else:
    raise Exception ("Feature not available yet.")
  return ans, _eval


def curve_fit(x, y, f=None, p0=None, maxfev=1000):
  args = np.argsort(x)
  dim_y = len(np.shape(y))
  if dim_y == 1:
    _eval = _curve_fit(f, x[args], y[args], p0=p0, maxfev=maxfev)[0]
    def ans(x):
      return f(x, *_eval)
  elif dim_y > 1:
    _eval = [_curve_fit(f, x[args], yy[args], p0=p0, maxfev=maxfev)[0] for yy in y]
    def ans(x):
      return np.array([f(x, *ee) for ee in _eval])
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  return ans, _eval


def curveEval(params, f=None):
  dim = len(np.shape(params))
  if dim == 1:
    def ans(X):
      return f(X, *params)
  elif dim == 2:
    def ans(X):
      return np.array([f(X, *ee) for ee in params])
  return ans


def fourier(x, y, deg=3, rcond=None):
  T = (x.max()-x.min()) / np.pi
  powers = np.arange(deg, dtype='double')
  powers /= T
  ncols = deg+1
  dim_y = len(np.shape(y))
  
  if dim_y == 1:
    G = np.zeros((len(x), 2*ncols))
    for ii, pp in enumerate(powers):
      G[:,ii] = np.sin(pp*x)
      G[:,ncols+ii] = np.cos(pp*x)
    _eval = np.linalg.lstsq(G, y, rcond=rcond)[0]
    
    def ans(X):
      Y = np.zeros_like(X)
      for ii, pp in enumerate(powers):
        Y += _eval[ii] * np.sin(pp*X) + _eval[ncols+ii] * np.cos(pp*X)
      return Y
  
  elif dim_y == 2:
    _eval = []
    for jj, yy in enumerate(y):
      G = np.zeros((len(x), 2*ncols))
      for ii, pp in enumerate(powers):
        G[:,ii] = np.sin(pp*x)
        G[:,ncols+ii] = np.cos(pp*x)
      _eval.append( np.linalg.lstsq(G, yy, rcond=rcond)[0] )
      
    def ans(X):
      Y = []
      for ee in _eval:
        result = 0.
        for ii, pp in enumerate(powers):
          result += ee[ii] * np.sin(pp*X) + ee[ncols+ii] * np.cos(pp*X)
        Y.append(result)
      return np.array(Y)
  
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  
  return ans, _eval


def legfit(x, y, deg=3, rcond=None, full=False, w=None):
  # TODO: Add support for 2d y array
  args = np.argsort(x)
  dim_y = len(np.shape(y))
  if dim_y == 1:
    _eval = legendre.legfit(x[args], y[args], deg, rcond=rcond, full=full, w=w)
    def ans(x):
      return legendre.legval(x, _eval)
  else:
    raise Exception("Feature not available yet.")
  return ans, _eval


def local_regression(x, y, deg=3, window=None, weights=None):
  # TODO: Check me!
  # TODO: Generalize to 2d y arrays
  # TODO: Make weights (select from 'linear', 'exponential', etc.?)
  args = np.argsort(x)
  X = x[args]
  Y = y[args]
  def ans(x0):
    dim = np.shape(x0)
    if len(dim) == 0:
      patch = make_patch(x0, X, window)[0]
      _eval = np.polyfit(X[patch], Y[patch], deg=deg, w=weights)
      return np.polyval(_eval, x0)
    else:
      _eval, out = [], []
      for xx in x0:
        patch = make_patch(xx, X, window)[0]
        coeffs = np.polyfit(X[patch], Y[patch], deg=deg, w=weights)
        _eval.append(coeffs)
        out.append( np.polyval(coeffs, xx) )
      return out
  return ans


def odr(x, y, f=None, p0=None):
  model = odr.Model(f)
  data = odr.RealData(x, y)
  setup = odr.ODR(data, model, beta0=p0)
  _eval = setup.run()
  def ans(x):
    return f(_eval.beta, x)
  return ans, _eval


def polyfit(x, y, **options):
  args = np.argsort(x)
  x_ref = lib.map_intervals(x, -1., 1.)
  dim_y = len(np.shape(y))
  if dim_y == 1:
    coeffs = np.polyfit(x_ref[args], y[args], **options)
    _eval = _map_poly_coeffs(coeffs, x_ref, np.min(x), np.max(x))
    def ans(x):
      return np.polyval(_eval, x)
  elif dim_y == 2:
    _eval = [np.polyfit(x[args], yy[args], **options) for yy in y]
    def ans(x):
      return np.array([np.polyval(ee, x) for ee in _eval])
  else:
    raise Exception ("Unexpected dimension for y data array(s).")
  return ans, _eval


def polyEval(_eval):
  dim = len(np.shape(_eval))
  if dim == 1:
    def ans(X):
      return np.polyval(_eval, X)
  elif dim == 2:
    def ans(X):
      return np.array([np.polyval(ee, X) for ee in _eval])
  return ans


# def rom_spline(x, y, deg=5, tol=1e-6, rel=False, verbose=False, seeds=None):
#   if _romspline:
#     args = np.argsort(x)
#     dim_y = len(np.shape(y))
#     if dim_y == 1:
#       _eval = romSpline.ReducedOrderSpline(x[args], y[args], deg=deg, tol=tol, rel=rel, verbose=verbose, seeds=seeds)
#       ans = _eval._spline
#     elif dim_y == 2:
#       _eval = [romSpline.ReducedOrderSpline(x[args], yy[args], deg=deg, tol=tol, rel=rel, verbose=verbose, seeds=seeds) for yy in y]
#       def ans(x):
#         return np.array([ee._spline(x) for ee in _eval])
#     else:
#       raise Exception, "Unexpected dimension for y data array(s)."
#     return ans, _eval
#   else:
#     raise Exception, "romSpline module not imported."


def spline(x, y, deg=5, s=0):
  args = np.argsort(x)
  dim_y = len(np.shape(y))
  if dim_y == 1:
    _eval = UnivariateSpline(x[args], y[args], k=deg, s=s)
    ans = _eval
  elif dim_y == 2:
    _eval = [UnivariateSpline(x[args], yy[args], k=deg, s=s) for yy in y]
    def ans(x):
      return np.array([ee(x) for ee in _eval])
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  return ans, _eval


###########################
# Multivariate regression #
###########################

def chebfit2d(x, y, deg=3, rcond=-1):
  # NOTE: This might be redundant with polyfit2d
  
  # Make tuples of orders up to the specified degree
  dim = 2
  orders = make_orders(deg, dim)
  ncols = number_of_terms(deg, dim)
  
  dim_y = len(np.shape(y))
  if dim_y == 1:
    # Fit to the data using least squares
    G = np.zeros((len(x[0]), ncols))
    for ii, oo in enumerate(orders):
      G[:,ii] = chebyshev.chebval(x[0], delta(list(range(deg+1)), oo[0])) * chebyshev.chebval(x[1], delta(list(range(deg+1)), oo[1]))
    _eval, _, _, _ = np.linalg.lstsq(G, y, rcond=rcond)
    
    # Generate the function to evaluate the fit
    def ans(X):
      Y = np.zeros_like(X[0])
      for ii, oo in enumerate(orders):
        Y += _eval[ii] * chebyshev.chebval(X[0], delta(list(range(deg+1)), oo[0])) * chebyshev.chebval(X[1], delta(list(range(deg+1)), oo[1]))
      return Y
  
  else:
    raise Exception ("Unexpected dimension for y data array(s).")
  
  return ans, _eval


def curve_fitnd(x, y, f=None, p0=None, maxfev=1000, sigma=None):
  """Use non-linear least squares to fit a function, f, to data."""
  # TODO: Include sigma option
  
  dim_y = np.shape(y)[0]
  if dim_y == 1:
    _eval = _curve_fit(f, x, y, p0=p0, maxfev=maxfev, sigma=sigma)[0]
    def ans(X):
      return f(X, *_eval)
  
  elif dim_y > 1:
    _eval = [_curve_fit(f, x, yy, p0=p0, maxfev=maxfev, sigma=sigma)[0] for yy in y]
    def ans(X):
      return np.array([f(X, *ee) for ee in _eval])
  
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  
  return ans, _eval


# TODO: Extend this to different degrees/orders in different dims
def polyfit2d(x, y, deg=3, rcond=-1):
  # Make powers for a binomial of degree deg
  dim = 2
  powers = make_orders(deg, dim)
  ncols = number_of_terms(deg, dim)
  
  dim_y = len(np.shape(y))
  if dim_y == 1:
    # Fit to the data using least squares
    G = np.zeros((len(x[0]), ncols))
    for ii, pp in enumerate(powers):
      G[:,ii] = x[0]**pp[0] * x[1]**pp[1]
    _eval = np.linalg.lstsq(G, y, rcond=rcond)[0]
    
    # Generate the function to evaluate the fit
    def ans(X):
      Y = np.zeros_like(X[0])
      for ii, pp in enumerate(powers):
        Y += _eval[ii] * X[0]**pp[0] * X[1]**pp[1]
      return Y
  
  elif dim_y > 1:
    _eval = np.zeros((len(y), ncols))
    for jj, yy in enumerate(y):
      # Fit to the data using least squares
      G = np.zeros((len(x[0]), ncols))
      for ii, pp in enumerate(powers):
        G[:,ii] = x[0]*pp[0] * x[1]**pp[1]
      _eval[jj] = np.linalg.lstsq(G, yy, rcond=rcond)[0]
    
    # Generate the function to evaluate the fit
    # TODO: Test if this is "fast enough""
    def ans(X):
      #Y = np.zeros((len(_eval), np.shape(X[0]))
      Y = []
      for jj, ee in enumerate(_eval):
        ans = 0.
        for ii, pp in enumerate(powers):
          ans += ee[ii] * X[0]**pp[0] * X[1]**pp[1]
        Y.append(ans)
      return Y
  
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  
  return ans, _eval


def polyfit3d(x, y, deg=3, rcond=-1):
  # Make powers for a binomial of degree deg
  dim = 3
  powers = make_orders(deg, dim)
  ncols = number_of_terms(deg, dim)
  
  # Fit to the data using least squares
  G = np.zeros((len(x[0]), ncols))
  for ii, pp in enumerate(powers):
    G[:,ii] = x[0]**pp[0] * x[1]**pp[1] * x[2]**pp[2]
  _eval = np.linalg.lstsq(G, y, rcond=rcond)[0]
  
  # Generate the function to evaluate the fit
  def ans(X):
    Y = np.zeros_like(X[0])
    for ii, pp in enumerate(powers):
      Y += _eval[ii] * X[0]**pp[0] * X[1]**pp[1] * X[2]**pp[2]
    return Y
  
  return ans, _eval


def polyfit4d(x, y, deg=3, rcond=-1):
  # Make powers for a binomial of degree deg
  dim = 4
  powers = make_orders(deg, dim)
  ncols = number_of_terms(deg, dim)
  
  # Fit to the data using least squares
  G = np.zeros((len(x[0]), ncols))
  for ii, pp in enumerate(powers):
    G[:,ii] = x[0]**pp[0] * x[1]**pp[1] * x[2]**pp[2] * x[3]**pp[3]
  _eval, _, _, _ = np.linalg.lstsq(G, y, rcond=rcond)
  
  # Generate the function to evaluate the fit
  def ans(X):
    Y = np.zeros_like(X[0])
    for ii, pp in enumerate(powers):
      Y += _eval[ii] * X[0]**pp[0] * X[1]**pp[1] * X[2]**pp[2] * X[3]**pp[3]
    return Y
  
  return ans, _eval


def polyfitnd(x, y, deg=3, rcond=-1):
  # Make powers for a binomial of degree deg
  dim = np.shape(x)
  powers = make_orders(deg, dim[0])
  ncols = number_of_terms(deg, dim[0])
  
  # Fit to the data using least squares
  G = np.zeros((dim[1], ncols))
  for ii, pp in enumerate(powers):
    G[:,ii] = np.prod([x[jj]**pp[jj] for jj in range(len(pp))], axis=0)
  _eval, _, _, _ = np.linalg.lstsq(G, y, rcond=rcond)
  
  # Generate the function to evaluate the fit
  def ans(X):
    Y = np.zeros_like(X[0])
    for ii, pp in enumerate(powers):
      Y += _eval[ii] * np.prod([X[jj]**pp[jj] for jj in range(len(pp))], axis=0)
    return Y
  
  return ans, _eval


from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import bisplrep, bisplev
def spline2d(x, y, xdeg=5, ydeg=5, s=0):
  #args = np.argsort(x)
  assert len(x) == 2, "Sample data not 2-dimensional."
  
  dim_y = len(np.shape(y))
  if dim_y == 2:
    #tck = bisplrep(x[0], x[1], y, kx=xdeg, ky=ydeg, s=s)
    #_eval = RectBivariateSpline(x[0], x[1], y, kx=xdeg, ky=ydeg, s=s)
    spline = RectBivariateSpline(x[0], x[1], y, kx=xdeg, ky=ydeg, s=s)
    #coeffs = spline.get_coeffs()
    #knots = spline.get_knots()
    _eval = list(spline.tck)
    def ans(X, dx=0, dy=0):
      #return _eval(X[0], X[1], dx=dx, dy=dy)[0][0]
      return bisplev(X[0], X[1], [_eval[0], _eval[1], _eval[2], xdeg, ydeg], dx=dx, dy=dy)
      
  #elif dim_y == 2:  
  elif dim_y > 2:
    _eval = []
    for yy in y:
      spline = RectBivariateSpline(x[0], x[1], yy, kx=xdeg, ky=ydeg, s=s)
      _eval.append( list(spline.tck) )
      #_eval.append([tck[0], tck[1], tck[2], xdeg, ydeg])
    #_eval = [bisplrep(x[0], x[1], yy, kx=xdeg, ky=ydeg, s=s) for yy in y]
    #_eval = [RectBivariateSpline(x[0], x[1], yy, kx=xdeg, ky=ydeg, s=s) for yy in y]
    def ans(X, dx=0, dy=0):
      #return np.array([ee(X[0], X[1], dx=dx, dy=dy)[0][0] for ee in _eval])
      return np.array([bisplev(X[0], X[1], [ee[0], ee[1], ee[2], xdeg, ydeg], dx=dx, dy=dy) for ee in _eval])
  
  else:
    raise Exception("Unexpected dimension for y data array(s).")
  
  return ans, _eval



######################
# Dictionary of fits #
######################

_dict = {
  # Univariate
  'chebfit': chebfit,
  'curve_fit': curve_fit,
  'fourier': fourier,
  'legfit': legfit,
  'localreg': local_regression,
  'odr': odr,
  'polyfit': polyfit,
  # 'romSpline': rom_spline,
  'spline': spline,
  
  # Multivariate
  'chebfit2d': chebfit2d,
  'curve_fitnd': curve_fitnd,
  'polyfit2d': polyfit2d,
  'polyfit3d': polyfit3d,
  'polyfit4d': polyfit4d,
  'polyfitnd': polyfitnd,
  'spline2d':  spline2d,
}


class EvaluateFits(object):
  
  def __init__(self, fit, fit_params, **options):
    if fit is None:
      raise Exception("No fit specified. Available fits listed in `fits` attribute.")
    else:
      assert type(fit) is str, "Expecting string input for `fit`."
      self.__setattr__(fit, _dict[fit])
      self._fit = fit
      self._eval = fit_params
      self.options = options
  
  # def spline(self):
  #   dim = np.shape(self._eval)[0]
  #   if dim == 1:
  #     #_eval = UnivariateSpline(x[args], y[args], k=deg, s=s)
  #     ans = self._eval
  #   elif dim == 2:
  #     #_eval = [UnivariateSpline(x[args], yy[args], k=deg, s=s) for yy in y]
  #     def ans(x):
  #       return np.array([ee(x) for ee in self._eval])
  #   else:
  #     raise Exception, "Unexpected dimension."
  #   return ans


####################
# Cross-Validation #
####################

def _Linfty(x, y, arg=False):
  """L-infinity norm of x - y"""
  diff = np.abs(x-y)
  max_diff = np.max(diff)
  if arg:
    return max_diff, np.argmax(diff)
  else:  
    return max_diff


def partitions(n, K):
  """Split array with n samples into K (nearly) equal partitions"""
  assert n >= K, "Number of partitions must not exceed number of samples."
  return np.asarray( np.array_split(np.arange(n), K) )


def random_partitions(n, K):
  """Split array with n samples into K (nearly) equal partitions of non-overlapping random subsets"""
  assert n >= K, "Number of folds must not exceed number of samples."
  
  # Make array with unique random integers
  rand = np.random.choice(list(range(n)), n, replace=False)
  
  # Split into K (nearly) equal partitions
  return [np.sort(rand[pp]) for pp in partitions(n, K)]


def get_dims(dim_x, dim_y):
  dims = len(dim_x)
  if dims == 1:
    assert dim_x[0] == dim_y[0]
    size = dim_x[0]
  elif dims == 2:
    assert dim_x[1] == dim_y[0]
    size = dim_x[1]
  else:
    raise Exception("Expecting an array or array of arrays for samples.")
  return dims, size


def _Kfold(x, y, K, i_fold, folds, fit, **options):
  """K-fold cross validation on a given partition (or fold)"""
  
  # Assemble training data excluding the i_fold'th partition for validation
  # TODO: There's got to be a better way to do this
  folds = np.asarray(folds)
  complement = np.ones(len(folds), dtype='bool')
  complement[i_fold] = False
  f_trial = np.sort( np.concatenate([ff for ff in folds[complement]]) )
  fold = folds[i_fold]

  # Form trial data
  dims, size = get_dims(np.shape(x), np.shape(y))
  if dims == 1:
    x_trial = x[f_trial]
    x_test = x[fold]
  elif dims == 2:
    x_trial = x[:,f_trial]
    x_test = x[:, fold]
  else:
    raise Exception("Expecting 1d or 2d arrays.")
  y_trial = y[f_trial]
  y_test = y[fold]
  
  # Build trial interpolant
  # if fit == 'romSpline':
  #   if _romspline:
  #     interp = romSpline._greedy(x_trial, y_trial, **options)[0]
  #   else:
  #     raise Exception, "romSpline module not imported."
  # else:
  #   interp = _dict[fit](x_trial, y_trial, **options)[0]
  interp = _dict[fit](x_trial, y_trial, **options)[0]
  
  # Compute L-infinity errors between trial and data in validation partition
  error, arg_error = _Linfty(interp(x_test), y_test, arg=True)
  
  return error, fold[arg_error]


class CrossValidation(object):
  # TODO: Extend also to higher dim y input?
  
  def __init__(self, fit, **options):
    assert type(fit) is str, "Expecting a string."
    self._fit = fit
    self._dict = _dict
    self._options = options
    
    self.errors = {}
    self.arg_errors = {}
    self.ensemble_errors = {}
    self.ensemble_arg_errors = {}
  
  
  def __call__(self, x, y, K=10, parallel=True, random=True):
    return self.Kfold(x, y, K=K, parallel=parallel, random=random)
  
  
  def LOOCV(self, x, y, parallel=True, random=True):
    """Leave-one-out cross-validation"""
    self.Kfold(x, y, K=np.shape(x)[-1], parallel=parallel, random=random)
  
  
  def Kfold(self, x, y, K=10, parallel=True, random=True):
    """K-fold cross-validation"""
    
    # Validate input
    x = np.asarray(x)
    y = np.asarray(y)
    dim_x = np.shape(x)
    dim_y = np.shape(y)
    assert len(dim_y) == 1, "Expecting an array of input response values."
    dims, size = get_dims(dim_x, dim_y)
    
    # Allocate some memory
    errors = np.zeros(K, dtype='double')
    arg_errors = np.zeros(K, dtype='int')
    
    # Divide into K random or nearly equal partitions
    if random:
      self._partitions = random_partitions(size, K)
    else:
      self._partitions = partitions(size, K)
    
    if parallel is False:
      for ii in range(K):
        errors[ii], arg_errors[ii] = _Kfold(x, y, K, ii, self._partitions, self._fit, **self._options)
    else:
      # Determine the number of processes to run on
      if parallel is True:
        try:
          numprocs = cpu_count()
        except NotImplementedError:
          numprocs = 1
      else:
        numprocs = parallel
      
      # Create a parallel process executor
      executor = ProcessPoolExecutor(max_workers=numprocs)
      
      # Compute the interpolation errors on each testing partition
      output = []
      for ii in range(K):
        output.append( executor.submit(_Kfold, x, y, K, ii, self._partitions, self._fit, **self._options) )
      
      # Gather the results as they complete
      for ii, ee in enumerate(as_completed(output)):
        errors[ii], arg_errors[ii] = ee.result()
      
    self.errors[K] = errors
    self.arg_errors[K] = arg_errors
  
  
  def Kfold_ensemble(self, x, y, n, K=10, parallel=True, random=True, verbose=False):
    """Perform a number n of K-fold cross-validations"""
    ens_arg_errors, ens_errors = [], []
    for nn in range(n):
      if verbose and not (nn+1)%10:
        print(("Trial number", nn+1))
      self.Kfold(x, y, K=K, parallel=parallel, random=random)
      ens_errors.append( self.errors[K] )
      ens_arg_errors.append( self.arg_errors[K] )
    
    self.ensemble_errors[K] = ens_errors
    self.ensemble_arg_errors[K] = ens_arg_errors


##############################################
# The following three functions (_general_function, _weighted_general_function, 
# curve_fit) are from scipy.optimize. I have changed the error handling here
# so that curve_fit returns the parameters found, even if they are not optimal. 
# The original code raises an exception and aborts the program. Using a `try` and `except`
# pair does not seem to retain the (suboptimal) fit parameters.
##############################################

def _general_function(params, xdata, ydata, function):
  return function(xdata, *params) - ydata


def _weighted_general_function(params, xdata, ydata, function, weights):
  return weights * (function(xdata, *params) - ydata)


def _curve_fit(f, xdata, ydata, p0=None, sigma=None, **kw):
  """
  Use non-linear least squares to fit a function, f, to data.
  
  Assumes ``ydata = f(xdata, *params) + eps``
  
  Parameters
  ----------
  f : callable
      The model function, f(x, ...).  It must take the independent
      variable as the first argument and the parameters to fit as
      separate remaining arguments.
  xdata : An N-length sequence or an (k,N)-shaped array
      for functions with k predictors.
      The independent variable where the data is measured.
  ydata : N-length sequence
      The dependent data --- nominally f(xdata, ...)
  p0 : None, scalar, or M-length sequence
      Initial guess for the parameters.  If None, then the initial
      values will all be 1 (if the number of parameters for the function
      can be determined using introspection, otherwise a ValueError
      is raised).
  sigma : None or N-length sequence
      If not None, this vector will be used as relative weights in the
      least-squares problem.
  
  Returns
  -------
  popt : array
      Optimal values for the parameters so that the sum of the squared error
      of ``f(xdata, *popt) - ydata`` is minimized
  pcov : 2d array
      The estimated covariance of popt.  The diagonals provide the variance
      of the parameter estimate.
  
  See Also
  --------
  leastsq
  
  Notes
  -----
  The algorithm uses the Levenberg-Marquardt algorithm through `leastsq`.
  Additional keyword arguments are passed directly to that algorithm.
  
  Examples
  --------
  >>> import numpy as np
  >>> from scipy.optimize import curve_fit
  >>> def func(x, a, b, c):
  ...     return a*np.exp(-b*x) + c
  
  >>> x = np.linspace(0,4,50)
  >>> y = func(x, 2.5, 1.3, 0.5)
  >>> yn = y + 0.2*np.random.normal(size=len(x))
  
  >>> popt, pcov = curve_fit(func, x, yn)
  
  """
  if p0 is None:
    # determine number of parameters by inspecting the function
    import inspect
    args, varargs, varkw, defaults = inspect.getargspec(f)
    if len(args) < 2:
      msg = "Unable to determine number of fit parameters."
      raise ValueError(msg)
    if 'self' in args:
      p0 = [1.0] * (len(args)-2)
    else:
      p0 = [1.0] * (len(args)-1)

  if np.isscalar(p0):
    p0 = array([p0])

  args = (xdata, ydata, f)
  if sigma is None:
    func = _general_function
  else:
    func = _weighted_general_function
    args += (1.0/np.asarray(sigma),)

  # Remove full_output from kw, otherwise we're passing it in twice.
  return_full = kw.pop('full_output', False)
  res = leastsq(func, p0, args=args, full_output=1, **kw)
  (popt, pcov, infodict, errmsg, ier) = res

  if ier not in [1, 2, 3, 4]:
    msg = "Optimal parameters not found: " + errmsg
    #raise RuntimeError(msg)
    print (msg)
    return popt, pcov
    #if return_full:
    #    return popt, pcov, infodict, errmsg, ier
    #else:
    #    return popt, pcov 

  if (len(ydata) > len(p0)) and pcov is not None:
    s_sq = (func(popt, *args)**2).sum()/(len(ydata)-len(p0))
    pcov = pcov * s_sq
  else:
    pcov = np.inf

  if return_full:
    return popt, pcov, infodict, errmsg, ier
  else:
    return popt, pcov


