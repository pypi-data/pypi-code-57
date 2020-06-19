import numpy as np
import scipy.optimize as op
from george import kernels
import george
george.__version__


class GPRFit(object):
    def __init__(self, X, Y, yerr=None):
        """
        X : np.ndarray, shape = (N, D), N=samples, D=dimension
        Y : np.ndarray, shape = (N,)
        yerr : np.ndarray, shape = (N,)
        """
        self.X = X
        self.Y = Y
        self.yerr = yerr
        if self.yerr is None:
            print("no yerr given - setting to zero")
            self.yerr = np.zeros(shape=self.Y.shape)

    def setup_kernel(self, kernel):
        self.kernel = kernel

    def fit(self, solver=george.BasicSolver):
        self.gp = george.GP(self.kernel, solver=solver)
        self.gp.compute(self.X, self.yerr)

    def opt(self, method="L-BFGS-B"):
        # Define the objective function (negative log-likelihood in this case).
        def nll(p):
            self.gp.set_parameter_vector(p)
            ll = self.gp.log_likelihood(self.Y, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        # And the gradient of the objective function.
        def grad_nll(p):
            self.gp.set_parameter_vector(p)
            return -self.gp.grad_log_likelihood(self.Y, quiet=True)

        # You need to compute the GP once before starting the optimization.
        self.gp.compute(self.X, self.yerr)

        # Print the initial ln-likelihood.
#         print(self.gp.log_likelihood(self.Y))

        # Run the optimization routine.
        p0 = self.gp.get_parameter_vector()
        results = op.minimize(nll, p0, jac=grad_nll, method=method)

        # Update the kernel and print the final log-likelihood.
        self.gp.set_parameter_vector(results.x)
#         print(self.gp.log_likelihood(self.Y))

    def predict(self, X):
        mean, var = self.gp.predict(self.Y, X, return_var=True)
        return mean, var
