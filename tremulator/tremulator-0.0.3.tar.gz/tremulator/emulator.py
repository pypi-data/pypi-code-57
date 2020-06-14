import numpy as np
import scipy.optimize as op
import warnings

import asdf
import emcee
import george
from george import kernels
from george import metrics
import pyDOE as pd
from tqdm import tqdm

# all possible kernel types that we can serialize easily
kernel_types = [
    kernels.ConstantKernel,
    kernels.CosineKernel,
    kernels.DotProductKernel,
    kernels.EmptyKernel,
    kernels.ExpKernel,
    kernels.ExpSine2Kernel,
    kernels.ExpSquaredKernel,
    kernels.LinearKernel,
    kernels.LocalGaussianKernel,
    kernels.Matern32Kernel,
    kernels.Matern52Kernel,
    kernels.MyLocalGaussianKernel,
    kernels.PolynomialKernel,
    # # This kernel also needs an alpha parameter besides the metric...
    # kernels.RationalQuadraticKernel,
]

# we will need to extract the correct operators for composed kernels
kernel_operators = [kernels.Sum, kernels.Product]

# since metric parameters are the log of the given parameter, we need to
# pass the metric instead of the parameters to instantiate the kernel.
# Only works for kernels that take only a metric.
metric_type = np.zeros_like(kernel_types, dtype=bool)
metric_type[[4, 6, 9, 10]] = True


def metric_to_dict(metric):
    """
    Convert george.metrics.Metric object to dict for asdf serialization.
    """
    m_dict = {}
    m_dict["metric_type"] = metric.metric_type
    m_dict["ndim"] = metric.ndim
    m_dict["parameter_names"] = metric.parameter_names
    m_dict["parameter_bounds"] = metric.parameter_bounds
    m_dict["unfrozen_mask"] = metric.unfrozen_mask
    m_dict["parameter_vector"] = metric.parameter_vector
    m_dict["axes"] = metric.axes
    return m_dict


def dict_to_metric(m_dict):
    """
    Convert dict with metric keywords to george.metrics.Metric object
    for asdf serialization.
    """
    # instantiate dummy metric type
    m = metrics.Metric(1, ndim=m_dict["ndim"])

    # now set the metric parameters
    m.metric_type = m_dict["metric_type"]
    # need to create a view of the arrays so that they will be loaded from asdf
    m.parameter_names = m_dict["parameter_names"][:]
    m.unfrozen_mask = m_dict["unfrozen_mask"][:]
    m.parameter_vector = m_dict["parameter_vector"][:]
    m.parameter_bounds = m_dict["parameter_bounds"][:]
    m.axes = m_dict["axes"][:]

    return m


def kernel_to_dict(kernel):
    """
    Convert george.kernels.Kernel object to dict for asdf serialization.
    """
    if isinstance(kernel, kernels.Kernel):
        if kernel.kernel_type == -1:
            raise ValueError("need a basic Kernel object")
        else:
            k_dict = {"type": kernel.kernel_type,
                      "parameters": (kernel.get_parameter_vector()
                                     if not metric_type[kernel.kernel_type]
                                     else metric_to_dict(kernel.metric)),
                      "ndim": kernel.ndim}
        return k_dict
    elif isinstance(kernel, dict):
        if ("type" in kernel.keys() and
            "parameters" in kernel.keys() and
            "ndim" in kernel.keys()):
            return kernel
        else:
            raise ValueError("kernel_dict needs 'type', 'parameters' and 'ndim' keys")
    else:
        raise TypeError("kernel should be kernels.Kernel or dict")


def dict_to_kernel(k_dict):
    """
    Convert dict with kernel parameters to george.kernels.Kernel object,
    hands back the same object if it already is a Kernel, necessary for
    map_to_kernel recursion. Used in asdf serialization.
    """
    if isinstance(k_dict, dict):
        if ("type" in k_dict.keys() and
            "parameters" in k_dict.keys() and
            "ndim" in k_dict.keys()):
            k = kernel_types[k_dict["type"]](k_dict["parameters"]
                                             if not metric_type[k_dict["type"]]
                                             else dict_to_metric(k_dict["parameters"]),
                                             ndim=k_dict["ndim"])
            return k
        else:
            raise ValueError("kernel_dict needs 'type', 'parameters' and 'ndim' keys")
            
    elif isinstance(k_dict, kernels.Kernel):
        return k_dict
    else:
        raise TypeError("kernel should be kernels.Kernel or dict")


def kernel_to_map(kernel):
    """
    Extract map of all constituent kernels as dictionaries with their
    operations.

    Parameters
    ----------
    kernel : george.kernels.Kernel object
        possible sum and product of kernels

    Returns
    -------
    kernel_map : list
        list of building blocks [operation, kernel1, kernel2]
        where kernel1 or kernel2 is either a dict or another
        building block.
    """
    # kernel is still composed of multiple kernels
    if kernel.kernel_type == -1:
        operator = kernel.operator_type
        kernel_1 = kernel.models["k1"]
        kernel_2 = kernel.models["k2"]
        return [operator, kernel_to_map(kernel_1), kernel_to_map(kernel_2)]

    # kernel is a single building block -> convert to dict
    else:
        return kernel_to_dict(kernel)


def map_to_kernel(kernel_map):
    """
    Convert a kernel_map to the george.kernels.Kernel object
    with correct operations order.

    Parameters
    ----------
    kernel_map : list
        list of building blocks [operation, kernel1, kernel2]
        where kernel1 or kernel2 is either a dict or another
        building block.

    Returns
    -------
    kernel : george.kernels.Kernel object
        kernel resulting from all the correct operations on kernel_map
    """
    # whichever of the two kernels is not reduced, needs to be reduced
    if isinstance(kernel_map[1], list):
        kernel_map[1] = map_to_kernel(kernel_map[1])
    elif isinstance(kernel_map[2], list):
        kernel_map[2] = map_to_kernel(kernel_map[2])
    # if both kernels are reduced, we can add them and send them up the stack
    else:
        k1 = dict_to_kernel(kernel_map[1])
        k2 = dict_to_kernel(kernel_map[2])
        return kernel_operators[kernel_map[0]](k1, k2)

    # now we need to add up the final objects
    k1 = dict_to_kernel(kernel_map[1])
    k2 = dict_to_kernel(kernel_map[2])
    return kernel_operators[kernel_map[0]](k1, k2)


def arrays_to_theta(*xi):
    '''
    Convert a set of N 1-D coordinate arrays to a regular coordinate grid of
    dimension (npoints, N) for the interpolator
    '''
    # the meshgrid matches each of the *xi to all the other *xj
    Xi = np.meshgrid(*xi, indexing='ij')

    # now we create a column vector of all the coordinates
    theta = np.concatenate([X.reshape(X.shape + (1,)) for X in Xi], axis=-1)

    return theta.reshape(-1, len(xi))


class Interpolator(object):
    """
    Gaussian process interpolator

    Parameters
    ----------
    bounds : array
        lower and upper bounds for each dimension of the input theta
    theta : array (n_samples, n_dim)
        input coordinates
    y : array (n_samples, )
        function values
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    hyper_parameters : array or None
        vector of hyper parameters
    hyper_bounds : array or None
        only required if hyper_vector is None, bounds for hyper_vector
        optimization
    alpha : array or None, optional
        gp alpha for exact reproduction (default: None)
    n_restarts : int
        number of random initialization positions for hyperparameters
        optimization (default: 5)
    """
    def __init__(
            self,
            bounds=None,
            theta=None,
            y=None,
            kernel=None,
            hyper_parameters=None,
            hyper_bounds=None,
            alpha=None,
            n_restarts=5
    ):
        self.theta = theta
        self.bounds = bounds
        self.y = y
        self.kernel = kernel
        self.hyper_parameters = hyper_parameters
        self.hyper_bounds = hyper_bounds
        self.alpha = alpha
        self.n_restarts = n_restarts

    def _check_theta(self, theta):
        """Check whether theta has right dimensions"""
        theta = np.atleast_2d(theta)
        if len(theta.shape) > 2 or theta.shape[1] != self._n_dim:
            raise TypeError("theta should have shape (n_samples, n_dim)")
        return theta

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        if value is None:
            warnings.warn("theta will need to be loaded", RuntimeWarning)
            self._theta = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2:
                raise TypeError("theta should have shape (n_samples, n_dim)")
            self._n_dim = value.shape[1]
            self._n_samples = value.shape[0]
            self._theta = value

    def _within_bounds(self, theta):
        """Return indices of given theta within the given bounds"""
        # difference between coord and the bounds of its dimension
        diff = (theta.reshape(-1, self._n_dim, 1)
                - self.bounds.reshape(1, self._n_dim, 2))

        # out_of bounds := coord - lower_bound < 0 or coord - upper_bound > 0
        out_of_bounds = ((diff[..., 0] < 0) | (diff[..., 1] > 0)).any(axis=-1)

        return ~out_of_bounds

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        if value is None:
            try:
                value = np.ones((self._n_dim, 2))
                value[:, 0] = -np.inf
                value[:, 1] = np.inf
                self._bounds = value
                warnings.warn("no bounds provided, we might end up extrapolating...",
                              RuntimeWarning)
            except AttributeError:
                warnings.warn("bounds will need to be loaded",
                              RuntimeWarning)
                self._bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2 or value.shape[1] != 2:
                raise TypeError("bounds should have shape (n_dim, 2)")
            if (value[:, 0] >= value[:, 1]).any():
                raise ValueError("cannot have lower bound >= upper bound")
            self._n_dim = value.shape[0]
            self._bounds = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value is None:
            warnings.warn("y will need to be loaded", RuntimeWarning)
            self._y = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("y should have shape (n_samples, )")
            elif value.shape[0] != self._n_samples:
                raise ValueError("y should have same n_samples as theta")
            else:
                self._y = value

    @property
    def kernel(self):
        return self._kernel

    @kernel.setter
    def kernel(self, kernel):
        if kernel is None:
            warnings.warn("kernel will need to be loaded", RuntimeWarning)
            self._kernel = None
        elif isinstance(kernel, kernels.Kernel):
            self._kernel_dim = kernel.ndim
            self._kernel = kernel
        else:
            raise TypeError("kernel needs to be Kernel instance")

    @property
    def n_restarts(self):
        return self._n_restarts

    @n_restarts.setter
    def n_restarts(self, value):
        if type(value) is int:
            self._n_restarts = value
        else:
            raise TypeError("n_restarts has to be int")

    @property
    def hyper_parameters(self):
        return self._hyper_parameters

    @hyper_parameters.setter
    def hyper_parameters(self, value):
        # if hyper_parameters is None, we need to optimize it later
        if value is None:
            self._optimize = True
            self._hyper_parameters = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("hyper_parameters should be 1d")
            elif value.shape[0] != self._kernel_dim + 1:
                raise ValueError("hyper_parameters should have size {}".format(self._kernel_dim + 1))
            else:
                self._optimize = False
                self._hyper_parameters = value

    @property
    def hyper_bounds(self):
        return self._hyper_bounds

    @hyper_bounds.setter
    def hyper_bounds(self, value):
        # if no optimization required, all is well
        # self._optimize is True if no hyper_parameters are given
        if not self._optimize:
            self._hyper_bounds = None

        # need hyper_bounds if optimization required
        elif self._optimize and value is None:
            warnings.warn("hyper_parameters will need to be loaded",
                          RuntimeWarning)
            self._hyper_bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2:
                raise TypeError("hyper_bounds should be 2d")
            elif (value.shape[0] == self._kernel_dim + 1 and
                  value.shape[1] == 2):
                self._hyper_bounds = value
            else:
                raise TypeError("hyper_bounds should have size (n_dim_kernel + 1, 2)")

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if value is None:
            self._alpha = None
        else:
            value = np.atleast_1d(value)
            if len(value.shape) > 1:
                raise TypeError("alpha should be 1d")
            elif value.shape[0] != self.theta.shape[0]:
                raise ValueError("alpha should have same n_samples as theta")
            else:
                self._alpha = value

    def _gp_init(self):
        self._gp = george.GP(self.kernel)
        self._gp.compute(self.theta)
        if self.alpha is not None:
            self._gp._alpha = self.alpha

        if self._optimize:
            self._optimize_hyper_parameters()
        else:
            self._gp.set_parameter_vector(self.hyper_parameters)

    @property
    def gp(self):
        try:
            # if hyper_parameters or alpha were updated, reload them in the gp
            if not (self._gp.get_parameter_vector()
                    == self.hyper_parameters).all():
                self._gp.set_parameter_vector(self.hyper_parameters)
            if not (self._gp._alpha == self.alpha).all():
                self._gp._alpha = self.alpha
            return self._gp
        except AttributeError:
            self._gp_init()
            return self._gp

    def _optimize_hyper_parameters(self):
        """Optimize the Gaussian process hyperparameters by minimizing the log
        likelihood.

        The optimizations is performed for num_restarts random
        starting points within hyper_bounds and the hyperparameters
        resulting in the highest log_likelihood are chosen.
        """
        # define the negative log likelihood
        def nll(p):
            self._gp.set_parameter_vector(p)
            ll = self._gp.log_likelihood(self.y, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        # And the gradient of the objective function.
        def grad_nll(p):
            self._gp.set_parameter_vector(p)
            return -self._gp.grad_log_likelihood(self.y, quiet=True)

        parameters = []
        results = []
        for _ in range(self.n_restarts):
            # Run the optimization routine.
            p0 = np.random.uniform(low=self.hyper_bounds[:, 0],
                                   high=self.hyper_bounds[:, 1])

            # find optimal parameters
            result = op.minimize(nll, p0, jac=grad_nll, method="L-BFGS-B")
            parameters.append(result.x)

            # now compute the loglikelihood for these parameters
            self._gp.set_parameter_vector(result.x)
            results.append(self._gp.log_likelihood(self.y, quiet=True))

        # the highest value of the loglikelihood corresponds to the
        # wanted hyperparameters
        best_idx = np.argmax(results)

        # Update the kernel
        self._gp.set_parameter_vector(parameters[best_idx])
        self.hyper_parameters = parameters[best_idx]

    def predict(self, theta, var=False, cov=False, **kwargs):
        theta = self._check_theta(theta)

        # check if all values are within the bounds
        out_of_bounds = ~self._within_bounds(theta)
        if out_of_bounds.any():
            warnings.warn("extrapolating for {}".format(theta[out_of_bounds]),
                          RuntimeWarning)
        return self.gp.predict(self.y, theta, return_var=var, return_cov=cov,
                               **kwargs)

    def load(self, fname):
        with asdf.open(fname, copy_arrays=True) as af:
            self.theta = af.tree["theta"][:]
            self.y = af.tree["y"][:]
            self.kernel = map_to_kernel(af.tree["kernel"][:])
            self.hyper_parameters = af.tree["hyper_parameters"][:]
            self.bounds = af.tree["bounds"][:]
            self.hyper_bounds = af.tree["hyper_bounds"][:]
            self.alpha = af.tree["alpha"][:]


class EmulatorBase(object):
    """
    Base Gaussian process emulator of y(theta)

    Parameters
    ----------
    n_init : int
        number of points in the initial Latin hypercube (default: 10)
    f : callable f(theta)
        function to be emulated f(theta, *args, **kwargs) -> float
    bounds : (n_dim, 2) array
        lower and upper bounds for each dimension of the input theta to f
    f_args : tuple, optional
        positional arguments for f
    f_kwargs : dict, optional
        keyword arguments for f
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    hyper_bounds: array
        lower and upper bounds for each hyperparameter in the given kernel
    n_restarts : int
        number of random initialization positions for hyperparameters 
        optimization (default: 5)
    """
    def __init__(
            self,
            n_init=10,
            f=None,
            kernel=None,
            bounds=None,
            args=(),
            kwargs={},
            hyper_bounds=None,
            n_restarts=25,
    ):
        self.n_init = n_init
        self.bounds = bounds
        if self.bounds is not None:
            self._reset()
        self.f = f
        self.kernel = kernel
        self.args = args
        self.kwargs = kwargs
        self.hyper_bounds = hyper_bounds
        self.n_restarts = n_restarts

    @property
    def n_init(self):
        return self._n_init

    @n_init.setter
    def n_init(self, value):
        if type(value) is int:
            self._n_init = value
        else:
            raise TypeError("n_init has to be int")

    def _within_bounds(self, theta):
        """Return indices of given theta within the given bounds"""
        # difference between coord and the bounds of its dimension
        diff = (theta.reshape(-1, self._n_dim, 1)
                - self.bounds.reshape(1, self._n_dim, 2))

        # out_of bounds := coord - lower_bound < 0 or coord - upper_bound > 0
        out_of_bounds = ((diff[..., 0] < 0) | (diff[..., 1] > 0)).any(axis=-1)

        return ~out_of_bounds

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        if value is None:
            warnings.warn("bounds will need to be loaded",
                          RuntimeWarning)
            self._bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2 or value.shape[1] != 2:
                raise TypeError("bounds should have shape (n_dim, 2)")
            if (value[:, 0] >= value[:, 1]).any():
                raise ValueError("cannot have lower bound >= upper bound")
            self._n_dim = value.shape[0]
            self._bounds = value

            # set initial guess for theta
            self.theta_center = 0.5 * (self.bounds[:, 1] + self.bounds[:, 0])
            self.theta_range = self.bounds[:, 1] - self.bounds[:, 0]
            self.theta_init = ((pd.lhs(self._n_dim,
                                       self.n_init,
                                       criterion="maximin") - 0.5)
                               * self.theta_range + self.theta_center)
            # and load test values
            self.theta_test = None

    def _check_theta(self, theta):
        """Check whether theta has right dimensions"""
        theta = np.atleast_2d(theta)
        if len(theta.shape) > 2 or theta.shape[1] != self._n_dim:
            raise TypeError("theta should have shape (n_samples, n_dim)")
        return theta

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        value = self._check_theta(value)
        self._n_samples = value.shape[0]
        self._theta = value

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        if value is None:
            warnings.warn("f will need to be loaded", RuntimeWarning)
            self._f = None
        elif not callable(value):
            raise TypeError("f should be callable")
        else:
            self._f = value

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if value is None:
            self._args = ()
        else:
            self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if value is None:
            self._kwargs = {}
        elif not isinstance(value, dict):
            raise TypeError("kwargs should be dict")
        else:
            self._kwargs = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        value = np.atleast_1d(value)
        if len(value.shape) > 1:
            raise TypeError("y should have shape (n_samples, )")
        elif value.shape[0] != self._n_samples:
            raise TypeError("y should have same n_samples as theta")
        self._y = value

    @property
    def kernel(self):
        return self._kernel

    @kernel.setter
    def kernel(self, kernel):
        if kernel is None:
            warnings.warn("kernel will need to be loaded", RuntimeWarning)
            self._kernel = None
        elif isinstance(kernel, kernels.Kernel):
            self._kernel_dim = kernel.ndim
            self._kernel = kernel
        else:
            raise TypeError("kernel needs to be Kernel instance")

    @property
    def hyper_bounds(self):
        return self._hyper_bounds

    @hyper_bounds.setter
    def hyper_bounds(self, value):
        if value is None:
            warnings.warn("hyper_parameters will need to be loaded",
                          RuntimeWarning)
            self._hyper_bounds = None
        else:
            value = np.atleast_2d(value)
            if len(value.shape) > 2:
                raise TypeError("hyper_bounds should be 2d")
            elif (value.shape[0] == self._kernel_dim + 1 and
                  value.shape[1] == 2):
                self._hyper_bounds = value
            else:
                raise TypeError("hyper_bounds should have size (n_dim_kernel + 1, 2)")

    @property
    def n_restarts(self):
        return self._n_restarts

    @n_restarts.setter
    def n_restarts(self, value):
        if type(value) is int:
            self._n_restarts = value
        else:
            raise TypeError("n_restarts has to be int")

    def _reset(self):
        """Reset theta to a Latin hypercube with n_init points"""
        # theta_init is set when loading bounds
        self.theta = self.theta_init
        # set theta_test to None to automatically load the test points
        # can be updated later
        self.theta_test = None

    @property
    def theta_test(self):
        return self._theta_test

    @theta_test.setter
    def theta_test(self, value):
        """Create theta grid spanning parameter space for testing"""
        if value is None:
            # for low-dimensional data, sample regular grid
            if self._n_dim <= 4:
                self._theta_test = arrays_to_theta(*np.linspace(self.bounds[:, 0],
                                                                self.bounds[:, 1],
                                                                5).T)
            # otherwise, hypercube with fixed number of points
            else:
                self._theta_test = ((pd.lhs(self._n_dim, 512, criterion="maximin") - 0.5)
                                    * self.theta_range + self.theta_center)

        else:
            self._theta_test = self._check_theta(value)

    def _optimize_hyper_parameters(self, verbose=False):
        """Optimize the Gaussian process hyperparameters by minimizing the log
        likelihood.

        The optimizations is performed for n_restarts random
        starting points within hyper_bounds and the hyperparameters
        resulting in the highest log_likelihood are chosen.
        """
        # define the negative log likelihood
        def nll(p):
            self.gp.set_parameter_vector(p)
            ll = self.gp.log_likelihood(self.y, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        # And the gradient of the objective function.
        def grad_nll(p):
            self.gp.set_parameter_vector(p)
            return -self.gp.grad_log_likelihood(self.y, quiet=True)

        if verbose:
            # Print the initial ln-likelihood.
            print("Initial log likelihood: "
                  "{}".format(self.gp.log_likelihood(self.y)))

        parameters = []
        results = []
        for _ in range(self.n_restarts):
            # Run the optimization routine.
            p0 = np.random.uniform(low=self.hyper_bounds[:, 0],
                                   high=self.hyper_bounds[:, 1])

            # find optimal parameters
            result = op.minimize(nll, p0, jac=grad_nll, method="L-BFGS-B")
            parameters.append(result.x)

            # now compute the loglikelihood for these parameters
            self.gp.set_parameter_vector(result.x)
            results.append(self.gp.log_likelihood(self.y, quiet=True))

        # the highest value of the loglikelihood corresponds to the
        # wanted hyperparameters
        best_idx = np.argmax(results)

        # Update the kernel
        self.gp.set_parameter_vector(parameters[best_idx])

        if verbose:
            # print the final log-likelihood.
            print("Final log likelihood: "
                  "{}".format(self.gp.log_likelihood(self.y)))

    def _gp_init(self):
        self._gp = george.GP(self.kernel)
        self._gp.compute(self.theta)
        try:
            # if y has already been loaded, we don't need to recompute it
            # but it should have the same shape is y
            if self.y.shape[0] != self.theta.shape[0]:
                raise TypeError("y should have same n_samples as theta")
        except AttributeError:
            self.y = np.array([self.f(t, *self.args, **self.kwargs)
                               for t in tqdm(self.theta,
                                             desc="Setting up y(theta_init)",
                                             position=1)])

    @property
    def gp(self):
        try:
            return self._gp
        except AttributeError:
            self._gp_init()
            return self._gp

    def predict(self, theta, var=False, cov=False, **kwargs):
        """
        Predict f(theta) using the GP emulator
        """
        theta = self._check_theta(theta)

        # # check if all values are within the bounds
        # out_of_bounds = ~self._within_bounds(theta)
        # if out_of_bounds.any():
        #     warnings.warn("extrapolating for {}".format(theta[out_of_bounds]),
        #                   RuntimeWarning)
        return self.gp.predict(self.y, theta, return_var=var, return_cov=cov,
                               **kwargs)

    def add(self, theta):
        """Add observations theta to the emulator"""
        theta = self._check_theta(theta)
        y = np.array([self.f(c, *self.args, **self.kwargs) for c in theta])

        is_nan = np.isnan(y)
        if is_nan.any():
            warnings.warn("NaNs in function, dropping theta = {}".format(theta[is_nan]),
                          RuntimeWarning)
            theta = theta[~is_nan]
            y = y[~is_nan]
        # update the coordinates and function values
        self.theta = np.vstack([self.theta, theta])
        self.y = np.concatenate([self.y, y])

        # now get the new Gaussian process
        self.gp.compute(self.theta)

    def _check_converged(self, *args, **kwargs):
        """Convergence check for the emulator"""
        raise NotImplementedError("overloaded by subclasses")

    def acquisition(self, *args, **kwargs):
        """Acquisition function for new emulator training points"""
        raise NotImplementedError("overloaded by subclasses")

    def train(self, *args, **kwargs):
        """Train the emulator"""
        raise NotImplementedError("overloaded by subclasses")


class Emulator(EmulatorBase):
    """
    Gaussian process emulator of y(theta) trained by sampling acquisition.

    Parameters
    ----------
    n_init : int
        number of points in the initial Latin hypercube (default: 10)
    f : callable f(theta)
        function to be emulated f(theta, *args, **kwargs) -> float
    kernel : george.kernels.Kernel object
        kernel to use for the Gaussian process
    bounds : array
        lower and upper bounds for each dimension of the input theta to f
    args : tuple, optional
        positional arguments for f
    kwargs : dict, optional
        keyword arguments for f
    hyper_bounds: array
        lower and upper bounds for each hyperparameter in the given kernel
    n_restarts : int
        number of random initialization positions for hyperparameters 
        optimization (default: 25)
    """
    def __init__(
            self,
            n_init=10,
            f=None,
            kernel=None,
            bounds=None,
            args=(),
            kwargs={},
            hyper_bounds=None,
            n_restarts=25,
    ):
        super(Emulator, self).__init__(
            n_init=n_init,
            f=f,
            kernel=kernel,
            bounds=bounds,
            args=args,
            kwargs=kwargs,
            hyper_bounds=hyper_bounds,
            n_restarts=n_restarts)
        # cannot be converged at initialization
        self.converged = False

    def _check_converged(self, var_tol=1e-3):
        """Check convergence of the process by requiring var_max < var_tol for
        the minimum variance of the GP when sampled multiple times"""
        def neg_var(theta):
            y, var = self.predict(theta, var=True)
            return -var

        parameters = []
        results = []

        # sample Latin hypercube to ensure coverage of parameter space
        p0s = ((pd.lhs(self._n_dim,
                       self.n_restarts,
                       criterion="maximin") - 0.5)
               * self.theta_range + self.theta_center)
        for p0 in p0s:
            # find optimal parameters
            result = op.minimize(neg_var, p0, method="L-BFGS-B",
                                 bounds=self.bounds)
            parameters.append(result.x)
            results.append(-neg_var(result.x))

        parameters = np.array(parameters)
        results = np.array(results)

        # set convergence status
        self.converged = np.max(results) < var_tol
        self.theta_max_var = parameters[np.argmax(results)]

    def acquisition(self, theta, a, b):
        """Acquisition function returns linear combination of function value
        and GP variance"""
        within_bounds = self._within_bounds(theta)
        if within_bounds.all():
            pred, pred_var = self.predict(theta, var=True)
            return np.squeeze(a * pred + b * pred_var)
        else:
            return -np.inf

    def train(
            self,
            n_steps=50,
            a=1,
            b=1,
            n_add=5,
            n_walkers=32,
            var_tol=1e-3,
            epsilon=0.05
    ):
        """Train the emulator by drawing points from the function sampled from
        the acquisition function. Training is stopped after n_steps or
        when converged.

        Parameters
        ----------
        n_steps : int
            number of steps to iterate
        a : float
            relative weight of func in acquisition
        b : float
            relative weight of variance in acquisition
        n_add : int
            number of points to add
        n_walkers : int
            number of walkers to use to sample acquisition function
        var_tol : float
            maximum allowed variance of GP
        epsilon : float
            minimum fractional distance between new and previous theta
        """
        def acquire_theta(a, b, n_add, n_walkers):
            """Draw samples from acquisition"""
            p0 = (np.ones((n_walkers, self._n_dim))
                  * self.theta_center.reshape(1, -1))
            p0 += ((np.random.rand(n_walkers, self._n_dim) - 0.5)
                   * self.theta_range)

            # set up the sampler for the acquisition function
            sampler = emcee.EnsembleSampler(n_walkers, self._n_dim,
                                            self.acquisition,
                                            args=(a, b))

            # run the chain
            sampler.run_mcmc(p0, 600)

            # get the samples with burn-in removed
            samples = sampler.chain[:, 100:, :].reshape(-1, self._n_dim)

            # get random theta from the drawn samples
            indices = np.random.randint(0, samples.shape[0], n_add)

            close = np.zeros(len(samples[indices]), dtype=bool)
            theta_temp = self.theta * 1.
            for idx, theta in enumerate(samples[indices]):
                # for each coordinate compare the distance to the data points
                # to the minimum length scale of the domain
                # do not include points which are less than epsilon of that scale
                norms = np.linalg.norm(theta_temp - theta, axis=-1)
                scale = np.min(self.theta_range)
                too_close = (norms / scale < epsilon)
                close[idx] = too_close.any()

                # add new coordinate to comparison
                theta_temp = np.vstack([theta_temp, theta])

            return samples[indices][~close]

        self.a = a
        self.b = b
        # run the training
        for i in tqdm(range(n_steps), desc="Training", position=0):
            theta_new = acquire_theta(a=self.a, b=self.b, n_add=n_add,
                                      n_walkers=n_walkers)
            self.add(theta_new)

            # rescale a and b by the median of y and var to preserve relative
            # importance of both
            y_test, var_test = self.predict(self.theta_test, var=True)
            self.a = a / np.median(y_test)
            self.b = b / np.median(var_test)

            # only check convergence every 10 steps
            if (i + 1) % 10:
                continue

            # first optimize hyper parameters
            self._optimize_hyper_parameters()
            self._check_converged(var_tol=var_tol)
            if self.converged:
                print("Convergence reached")
                break

        # if stopped before convergence, warn the user
        # but also optimize hyper parameters to be sure
        if not self.converged:
            warnings.warn("Convergence criterion not reached, run some more steps...",
                          RuntimeWarning)
            self._optimize_hyper_parameters()

    def save(self, fname, extra={}):
        """Save the trained GP parameters to fname

        Parameters
        ----------
        fname : str
            path for savefile, asdf format
        extra : dict
            extra information to be saved
        """
        # if alpha has not been computed, calculate it
        if self.gp._alpha is None:
            self.gp._compute_alpha(self.y, cache=True)
        parameters = {
            "n_init": self.n_init,
            # # cannot save functions to asdf...
            # "f": self.f,
            "args": self.args,
            "kwargs": self.kwargs,
            "kernel": kernel_to_map(self.kernel),
            "bounds": self.bounds,
            "hyper_bounds": self.hyper_bounds,
            "n_restarts": self.n_restarts,
            "theta": self.theta,
            "y": self.y,
            "hyper_parameters": self.gp.get_parameter_vector(),
            "alpha": self.gp._alpha,
        }

        # python 2 compatible
        parameters = parameters.copy()
        parameters.update(extra)
        with asdf.AsdfFile(parameters) as ff:
            ff.write_to(fname)

    def load(self, fname):
        with asdf.open(fname, copy_arrays=True) as af:
            self.n_init = af.tree["n_init"]
            # # will need to load these separately...
            # self.f = af.tree["f"]
            self.args = af.tree["args"]
            self.kwargs = af.tree["kwargs"]
            self.kernel = map_to_kernel(af.tree["kernel"][:])
            self.bounds = af.tree["bounds"][:]
            self.hyper_bounds = af.tree["hyper_bounds"][:]
            self.n_restarts = af.tree["n_restarts"]
            self.theta = af.tree["theta"][:]
            self.y = af.tree["y"][:]
            self.hyper_parameters = af.tree["hyper_parameters"][:]
            self.alpha = af.tree["alpha"][:]

        warnings.warn("f, args and kwargs will need to be loaded",
                      RuntimeWarning)        
