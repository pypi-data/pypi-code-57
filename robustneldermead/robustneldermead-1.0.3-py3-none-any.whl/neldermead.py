# Contains the custom Nelder-Mead algorithm
import numpy as np
import sys
eps = sys.float_info.epsilon # For Amoeba xtol and tfol
import time
import pdb
import copy
from numba import njit, jit, prange
from pdb import set_trace as stop
import optimparameters.parameters as optimparameters
import numba


class NelderMead:
    """A class to interact with the Nelder Mead optimizer.
    
    """
    
    def __init__(self, target_function, init_pars, names=None, minvs=None, maxvs=None, varies=None, max_f_evals=None, xtol=1E-4, ftol=1E-4, n_iterations=None, no_improve_break=3, penalty=1E6, alpha=1, gamma=2, sigma=0.5, delta=0.5, args_to_pass=(), kwargs_to_pass={}):
        """Initiate a Nelder Mead solver.
        
        Args:
            target_function (function): The function to optimize. Must be called as ``target_function(pars, *args_to_pass, **kwargs_to_pass)``, with return values: ``(F, CONS)``, where F is the value to minimize and CONS = g(x) is the constraint. If g(x) < 0, the target function is penalized, along with parameters being out of bounds.
            init_pars (Parameters or np.ndarray): The initial parameters.
            names (list or np.ndarray, optional): The names of the parameters. Internally defaults to par1, par2, ...
            minvs (list or np.ndarray, optional): The lower bounds. Defaults to -inf.
            maxvs (list or np.ndarray, optional): The upper bounds. Defaults to inf.
            varies (list or np.ndarray, optional): Whether or not to vary (and effectively solve for) this parameter. Defaults to True.
            max_f_evals (int, optional): The maximum total number of function calls, including all full simplex + subspace calls. Defaults to 5000 x number of varied parameters.
            xtol (float, optional): If the relative range of all parameters are below this threshold (i.e, span a range smaller than this), then the solver breaks. Defaults to 1E-4.
            ftol (float, optional): If the relative range of function values is below this threshold, then the solver breaks and is considered converged.. Defaults to 1E-4.
            n_iterations (int, optional): The number of iterations to run. One iteration = 1 full simplex call + Subspace calls for consecutive pairs of parameters, including last parameter, first parameter. Defaults to = number of varied parameters.
            no_improve_break (int, optional): The consective number of times the solver needs to converge (reach ftol) before breaking. Defaults to 3.
            penalty (float, optional): The penalty term added to the target function return value if either parameters are out of bounds or if the constraint is < 0.. Defaults to 1E6.
            alpha (float, optional): NM hyper-parameter (see src code). Defaults to 1.
            gamma (float, optional): NM hyper-parameter (see src code). Defaults to 2.
            sigma (float, optional): NM hyper-parameter (see src code). Defaults to 0.5.
            delta (float, optional): NM hyper-parameter (see src code). Defaults to 0.5.
            args_to_pass (tuple, optional): The additional arguments to pass to the target function. Defaults to (), empty tuple.
            kwargs_to_pass (dict, optional): The additional keyword arguments to pass to the target function. Defaults to {}, empty dict.
        """

        # The target function
        self.target_function = target_function
        
        # The tolerance on x and f
        self.xtol, self.ftol = xtol, ftol
            
        
        # The number of consecutive convergences to actually converge
        self.no_improve_break = no_improve_break
            
        # The arguments to pass to the target function
        self.args_to_pass = args_to_pass
        self.kwargs_to_pass = kwargs_to_pass
        
        # The panalty term
        self.penalty = penalty
        
        # Nelder-Mead scale factors
        self.alpha, self.gamma, self.sigma, self.delta = alpha, gamma, sigma, delta
        
        # Init simplex
        self.init_params(init_pars, names=names, minvs=minvs, maxvs=maxvs, varies=varies)
        self.init_base_simplex(init_pars)
        
        if n_iterations is not None:
            self.n_iterations = n_iterations
        else:
            self.n_iterations = self.n_pars_vary
            
        if max_f_evals is not None:
            self.max_f_evals = max_f_evals
        else:
            self.max_f_evals = self.n_pars_vary * 5000
        
        # test_pars is constantly updated and passed to the target function
        # If only using numpy, test_pars will be unpacked before calling the target function.
        self.test_pars = copy.deepcopy(self.init_pars)
        
        # Copy the original parameters to the current min
        self.xmin = copy.deepcopy(self.init_pars)
        self.xmin_numpy = self.xmin.unpack()
        
        # f calls
        self.fcalls = 0
        
        # The current fmin = inf
        self.fmin = np.inf
        
        # Init the subspaces
        self.init_subspaces()
        
        # Reason for returning, may be anything
        self.converged = False
        
    def init_subspaces(self):
        init_pars_varies_inds = np.where(self.init_pars_numpy['varies'])[0]
        self.subspaces = [np.array([init_pars_varies_inds[i], init_pars_varies_inds[i+1]], dtype=int) for i in range(self.n_pars_vary - 1)]
        self.subspaces.append(np.array([init_pars_varies_inds[0], init_pars_varies_inds[-1]], dtype=int))
        
    def reset(self):
        #if hasattr(self, 'init_pars') and self.init_pars is not None:
        self.init_pars = copy.deepcopy(self.original_pars)
            
        self.fcalls = 0
        self.dx = np.inf
        self.fmin = np.inf # breaks when less than ftol N times.
        self.xmin = copy.deepcopy(self.init_pars)
            
    def init_params(self, init_pars, names=None, minvs=None, maxvs=None, varies=None):
        
        # The number of parameters
        self.n_pars = len(init_pars)
        
        # The initial parameters
        if type(init_pars) is optimparameters.Parameters:
            self.uses_parameters = True
            self.init_pars = init_pars
        else:
            self.uses_parameters = False
            names = ['par' + str(i+1) for i in range(self.n_pars)]
            self.init_pars = optimparameters.Parameters.from_numpy(names=names, values=init_pars, minvs=minvs, maxvs=maxvs)
            
        
        self.init_pars_numpy = self.init_pars.unpack()
        self.locked_pars_original, self.varied_pars_original = self.init_pars.get_locked(), self.init_pars.get_varied()
        self.locked_pars_numpy_original, self.varied_pars_numpy_original = self.locked_pars_original.unpack(), self.varied_pars_original.unpack()
        
        self.init_pars_vary_indices = np.where(self.init_pars_numpy['varies'])[0]
        
        
        # Number of varied parameters
        self.n_pars_vary = len(self.varied_pars_original)
        
            
    def init_base_simplex(self, init_pars):

        # Initialize the simplex
        right = np.zeros(shape=(self.n_pars_vary, self.n_pars_vary + 1), dtype=float)
        left = np.transpose(np.tile(self.varied_pars_numpy_original['values'], ( self.n_pars_vary + 1, 1)))
        diag = np.diag(0.5 * self.varied_pars_numpy_original['values'])
        right[:, :-1] = diag
        
        # Define a base simplex
        self.base_simplex = left + right
        
        # Copy the base simplex
        self.current_simplex = np.copy(self.base_simplex)
        
        # Sanity check init params
        bad_pars = self.init_pars.sanity_check()
        if len(bad_pars) > 0:
            raise ValueError("Parameter(s) " + str(bad_pars) + " out of bounds.")


    def init_sub_simplex(self, indices=None, par_names=None):
            
        if indices is not None:
            self.current_subspace_indices = np.array(indices, dtype=int)
            par_names_all = list(self.init_pars.keys())
            self.current_subspace_names = [par_names_all[i] for i in indices]
        else:
            self.current_subspace_names = par_names
            par_names_all = list(self.init_pars.keys())
            self.current_subspace_indices = np.array([par_names_all.index(p) for p in self.current_subspace_names], dtype=int)
            
        # Create an array for the default parameters
        self.xpass_values = self.xmin.unpack(keys='values')['values']
        
        if len(self.current_subspace_indices) < self.n_pars_vary:
            
            # Original
            v1 = [self.init_pars_numpy['values'][self.current_subspace_indices[0]],
                self.init_pars_numpy['values'][self.current_subspace_indices[1]]]
            
            # Best
            v2 = [self.xmin_numpy['values'][self.current_subspace_indices[0]],
                self.xmin_numpy['values'][self.current_subspace_indices[1]]]
            
            # Mix
            v3 = [self.xmin_numpy['values'][self.current_subspace_indices[0]],
                self.init_pars_numpy['values'][self.current_subspace_indices[1]]]
            simplex_sub = np.array([v1, v2, v3]).T
        else:
            simplex_sub = np.copy(self.current_simplex)

        return simplex_sub

    def solve_subspace(self, indices=None, par_names=None):
        
        # Generate a simplex for this subspace
        simplex = self.init_sub_simplex(indices=indices, par_names=par_names)
        
        # Define these as they are used often
        nx, nxp1 = simplex.shape

        # Initiate storage arrays
        fvals = np.empty(nxp1, dtype=float)
        
        x = np.empty(nx, dtype=float)
        xr = np.empty(nx, dtype=float)
        xbar = np.empty(nx, dtype=float)
        xc = np.empty(nx, dtype=float)
        xe = np.empty(nx, dtype=float)
        xcc = np.empty(nx, dtype=float)
        
        # Generate the fvals for the initial simplex
        for i in range(nxp1):
            fvals[i] = self.foo_wrapper(simplex[:, i])

        # Sort the fvals and then simplex
        ind = np.argsort(fvals)
        simplex = simplex[:, ind]
        fvals = fvals[ind]
        fmin = fvals[0]
        
        # Best fit parameter is the first column
        xmin = simplex[:, 0]
        
        # Keeps track of the number of times the solver thinks it has converged in a row.
        n_converged = 0
        
        # Force convergence
        while True:

            # Sort the vertices according from best to worst
            # Define the worst and best vertex, and f(best vertex)
            xnp1 = simplex[:, -1]
            fnp1 = fvals[-1]
            x1 = simplex[:, 0]
            f1 = fvals[0]
            xn = simplex[:, -2]
            fn = fvals[-2]
                
            # Possibly updated
            shrink = False

            # break after max number function calls is reached.
            if self.fcalls >= self.max_f_evals:
                self.converged = False
                break
                
            # Break if f tolerance has been met
            if self.compute_ftol(fmin, fnp1) > self.ftol:
                n_converged = 0
            else:
                n_converged += 1
            if n_converged >= self.no_improve_break:
                self.converged = True
                break

            # Idea of NM: Given a sorted simplex; N + 1 Vectors of N parameters,
            # We want to iteratively replace the worst point with a better point.
            
            # The "average" vector, V_i=par_i_avg
            # We first anchor points off this average Vector
            xbar[:] = np.average(simplex[:, :-1], axis=1)
            
            # The reflection point
            xr[:] = xbar + self.alpha * (xbar - xnp1)
            
            # Update the current testing parameter with xr
            x[:] = xr
            
            fr = self.foo_wrapper(x)

            if fr < f1:
                xe[:] = xbar + self.gamma * (xbar - xnp1)
                x[:] = xe
                fe = self.foo_wrapper(x)
                if fe < fr:
                    simplex[:, -1] = xe
                    fvals[-1] = fe
                else:
                    simplex[:, -1] = xr
                    fvals[-1] = fr
            elif fr < fn:
                simplex[:, -1] = xr
                fvals[-1] = fr
            else:
                if fr < fnp1:
                    xc[:] = xbar + self.sigma * (xbar - xnp1)
                    x[:] = xc
                    fc = self.foo_wrapper(x)
                    if fc <= fr:
                        simplex[:, -1] = xc
                        fvals[-1] = fc
                    else:
                        shrink = True
                else:
                    xcc[:] = xbar + self.sigma * (xnp1 - xbar)
                    x[:] = xcc
                    fcc = self.foo_wrapper(x)
                    if fcc < fvals[-1]:
                        simplex[:, -1] = xcc
                        fvals[-1] = fcc
                    else:
                        shrink = True
            if shrink:
                for j in range(1, nxp1):
                    simplex[:, j] = x1 + self.delta * (simplex[:, j] - x1)
                    fvals[j] = self.foo_wrapper(x)

            ind = np.argsort(fvals)
            fvals = fvals[ind]
            simplex = simplex[:, ind]
            fmin = fvals[0]
            xmin = simplex[:, 0]
            
        # Update the best fit parameters
        for i, p in enumerate(self.current_subspace_names):
            self.xmin[p].value = xmin[i]
            ii = np.where(self.init_pars_vary_indices == self.current_subspace_indices[i])[0]
            self.current_simplex[ii, -nxp1:] = simplex[i, :]
            
        # Redefine the numpy variable
        self.xmin_numpy = self.xmin.unpack()
        
        # Store the function minimum
        self.fmin = fmin
        
        
    def solve(self):
        
        iteration = 1
        
        dx = np.inf
        
        while iteration <= self.n_iterations and dx >= self.xtol:

            # Perform Ameoba call for all parameters
            self.solve_subspace(indices=self.init_pars_vary_indices)
            
            # If there's <= 2 params, a three-simplex is the smallest simplex used and only used once.
            if self.n_pars_vary <= 2:
                break
            
            # Perform Ameoba call for dim=2 ( and thus three simplex) subspaces
            for subspace in self.subspaces:
                
                # Call the solver
                self.solve_subspace(indices=subspace)

            # Update the iteration
            iteration += 1
            
            # Compute the max absolute range of the simplex
            dx = np.max(self.compute_xtol(np.nanmin(self.current_simplex, axis=1), np.nanmax(self.current_simplex, axis=1)))
        
        # Compute uncertainties
        #self.compute_uncertainties(self.current_simplex)
            
        # Recreate new parameter obejcts
        if self.uses_parameters:
            xmin = self.xmin
        else:
            xmin = self.xmin.unpack(keys=['values'])['values']
            
        return xmin, self.fmin, self.fcalls
    
    @staticmethod
    #@njit(numba.types.float64[:, :](numba.types.float64[:, :]))
    def compute_uncertainties(simplex):
        nx, nxp1 = simplex.shape
        p = np.empty(shape=(nxp1, nxp1), dtype=np.ndarray)
        for i in range(nxp1):
            for j in range(nxp1):
                if i != j:
                    p[i, j] = (simplex[:, i] + simplex[:, j]) / 2
        
        
        
        
    @staticmethod
    @njit(numba.types.float64[:](numba.types.float64[:], numba.types.float64[:]))
    def compute_xtol(a, b):
        c = (np.abs(b) + np.abs(a)) / 2
        c = np.atleast_1d(c)
        ind = np.where(c < eps)[0]
        if ind.size > 0:
            c[ind] = 1
        r = np.abs(b - a) / c
        return r

    @staticmethod
    @njit(numba.types.float64(numba.types.float64, numba.types.float64))
    def compute_ftol(a, b):
        return np.abs(a - b)
            
            
    def foo_wrapper(self, x):

        # Update the current varied subspace from the current simplex
        self.xpass_values[self.current_subspace_indices] = x

        # Correct the vary attributes
        v = np.zeros(self.n_pars, dtype=bool)
        v[self.current_subspace_indices] = True
        
        self.test_pars.setv(values=self.xpass_values, varies=v)
        
        # Call the target function
        if self.uses_parameters:
            f, c = self.target_function(self.test_pars, *self.args_to_pass, **self.kwargs_to_pass)
        else:
            f, c = self.target_function(self.test_pars.unpack(keys=['values'])['values'], *self.args_to_pass, **self.kwargs_to_pass)
        
        # Penalize the target function if pars are out of bounds or constraint is less than zero
        f += self.penalty * np.where((self.xpass_values < self.init_pars_numpy['minvs']) | (self.xpass_values > self.init_pars_numpy['maxvs']))[0].size
        f += self.penalty * (c < 0)
        
        # Update fcalls
        self.fcalls += 1
        
        # Only return a single value for the function.
        return f