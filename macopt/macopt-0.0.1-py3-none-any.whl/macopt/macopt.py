import numpy as np
import logging

class Macopt:
    """
    Conjugate gradient optimizer that uses only gradient information.
    
    Parameters
    ----------

    gradient : function
        The callable gradient must have the following signature:

        gradient(x) → (gradient, convergence)

        where x is an array_like that represents the variable vector, gradient is an array_like that represents the gradient at point x.
        The minimization terminates when convergence < tol.
    x_init : array_like
        Initial guess.
    options : dict, optional
        Dictionary of solver options.

        tol : float
            Tolerance criterion for the user-supplied convergence, see above. Default: 1e-10.
        max_iterations : int
            Maximum number of iterations. Default: 500000.
        callback : function
            Function that is called after each iteration, with signature callback(current_x) -> void. Default: None.
        normalize_function : function
            If supplied, the minimizer will keep the variable vector normalized at all times. This is a requirement for certain problems.
            Signature must be normalize_function(current_x) -> void, i.e. it must normalize in place. Default: None.
        logging_level : int
            Level of verbosity of output. logging.WARNING shows a warning when the minimizer failed to converge. 
            logging.INFO shows the convergence every log_every steps (see directly below). logging.DEBUG shows updates about various stages in the line search.
            For more information about logging levels, see `here <https://docs.python.org/3/howto/logging.html>`_. Default: logging.WARNING.
        log_every : int
            Frequency of logging, i.e. if log_every = n, log current convergence every n iterations. Default: 25.

        In addition, there are several minimizer-specific options. For more information, see `David MacKay's page <http://www.inference.org.uk/mackay/c/macopt.html>`_.

        linmin_max_iterations : int
            Default: 40.
        linmin_g1 : float
            Default: 2.0.
        linmin_g2 : float
            Default: 1.25.
        linmin_g3 : float
            Default: 0.5.
        last_x_default : float
            Default: 0.0001.
        gam_bound : float
            Default: 4.0.

    Returns
    -------
    result : dict
        Dictionary with the result.

        x : array_like
            Solution vector.
        converged : bool
            Whether the minimizer converged or not.
        tol : float
            Final convergence.
        iterations : int
            Number of iterations.

    Example
    -------
    .. code-block:: python

        import numpy as np 
        from scipy.optimize import rosen_der, rosen

        # Minimize the Rosenbrock function in 2D (https://mathworld.wolfram.com/RosenbrockFunction.html).
        def gradient(x):
            grad = rosen_der(x)
            convergence = np.linalg.norm(grad)
            return grad, convergence

        x_init = np.random.rand(2)

        minimizer = Macopt(gradient, x_init)
        result =  minimizer.minimize()
        # => {'x': array([1., 1.]), 'converged': True, 'tol': 8.109748258843716e-12, 'iterations': 15}
    """

    def __init__(self, gradient, x_init, options={}):
        self.gradient = gradient
        
        self.callback = options.get('callback') or None
        self.logging_level = options.get('logging_level') or logging.WARNING
        self.log_every = options.get('log_every') or 25
        self.max_iterations = options.get('max_iterations') or 500000
        self.tol = options.get('tol') or 1e-10
        self.normalize_function = options.get('normalize_function') or None

        self.linmin_max_iterations = options.get('linmin_max_iterations') or 40
        self.linmin_g1 = options.get('linmin_g1') or 2.0     # factors for growing and shrinking the interval- don't change
        self.linmin_g2 = options.get('linmin_g2') or 1.25
        self.linmin_g3 = options.get('linmin_g3') or 0.5
        self.last_x_default = options.get('last_x_default') or 0.0001
        self.gam_bound = options.get('gam_bound') or 4.0

        self.p = np.copy(x_init)
        self.q, self.current_convergence = self.gradient(self.p)
        self.g = np.zeros_like(x_init)
        self.h = np.zeros_like(x_init)
        self.scratch = np.zeros_like(x_init)
        self.lastx = self.last_x_default
        self.problem_dimension = x_init.shape[0]

        self.restart = 0;
        self.initialize_minimizer(1)

    def minimize(self):
        for self.current_it in range(self.max_iterations):
            gg = np.dot(self.g, self.g)
            maxGradSqr = np.amax(gg)
            self.gtyp = np.sqrt(gg / self.problem_dimension)


            if self.current_convergence < self.tol:
                self.finish_up(converged=True)
                return self.result

            if self.current_it % self.log_every == 0 and self.current_it != 0:
                self.display_progress()

            if self.callback:
                self.callback(self.p)

            step = self.linmin()

            if self.restart != 0:
                self.q, self.current_convergence = self.gradient(self.p)
                logging.debug("Restarting optimizer.")
                self.initialize_minimizer(0)
            else:
                # This is our own addition, and doesn't appear in the original by David MacKay.
                dgg = np.dot(self.q + self.g, self.q)
                gam = dgg / gg
                if gam > self.gam_bound:
                    logging.debug("Gamma was too big, restarting optimizer.")
                    self.restart = 1
                    self.initialize_minimizer(0)
                else:
                    self.g = -np.copy(self.q)       # g stores minus the most recent gradient
                    self.h = self.g + gam*self.h    # h stores q, the current line direction
                    self.q = self.h
                    tmpd = - np.dot(self.q, self.g) # Check that inner product of gradient and line search is < 0.
                    
                    if tmpd > 0.0:
                        self.restart = 2
                        logging.debug("Restarting optimizer (2).")
                        self.initialize_minimizer(0)

        self.finish_up(converged=False)
        return self.result

    def linmin(self):
        gx = np.zeros(self.problem_dimension)
        gy = np.zeros(self.problem_dimension)
        x = self.lastx / self.gtyp
        s, gx = self.prod(x)

        overran = True
        if s < 0:
            for it in range(self.linmin_max_iterations):
                y = x*self.linmin_g1
                t, gy = self.prod(y)

                if t >= 0.0:
                    overran = False
                    break

                x = y
                s = t
                # swap gx and gy
                gUnused = np.copy(gx)
                gx = np.copy(gy)
                gy = np.copy(gUnused)
        # Do the same loop as above, but with a different break condition and multiplier
        elif s > 0:
            for it in range(self.linmin_max_iterations):
                y = x*self.linmin_g3
                t, gy = self.prod(y)    # result goes into gy

                if t <= 0.0:
                    overran = False
                    break

                x = y
                s = t
                # swap gx and gy
                gUnused = np.copy(gx)
                gx = np.copy(gy)
                gy = np.copy(gUnused)
        # "Hole in one", s == 0.0
        else:
            overran = False
            t = 1.0
            y = x
    
        if overran:
            logging.debug("linmin overran.")
            tmpd, gy = self.prod(0.0)
            if tmpd > 0: self.restart = 1 

        if s < 0: s = -s 
        if t < 0: t = -t 
        m = s + t
        s /= m
        t /= m

        m = s*y + t*x
        # Evaluate step length
        self.p += m*self.q      # this is the point where the parameter vector steps
        step = np.sum( np.abs(m*self.q) )
        self.q = s*gy + t*gx    # estimated gradient is stored in q

        if self.normalize_function:
            self.normalize_function(self.p)

        self.lastx = m*self.linmin_g2*self.gtyp
        
        return step / self.problem_dimension

    def initialize_minimizer(self, start):
        if start == 0: self.lastx = self.last_x_default 
        if self.restart != 2: self.g = -np.copy(self.q) 
        self.h = np.copy(self.g)
        self.q = np.copy(self.g)

        self.restart = 0

    def prod(self, x):
        self.scratch = self.p + x*self.q
        gradScratch, self.current_convergence = self.gradient(self.scratch)
        s = np.dot(gradScratch, self.q)
        return s, gradScratch

    def finish_up(self, converged=True):
        solution_vector = self.p
        final_tol = self.current_convergence
        final_iterations = self.current_it

        if not converged:
            logging.warning("After %d iterations, minimizer did not convergence. Final convergence: %g." % (final_iterations, final_tol))

        self.result = {
            'x': solution_vector,
            'converged': converged,
            'tol': final_tol,
            'iterations': final_iterations
        }

    def display_progress(self):
        logging.info("[iter %d] convergence: %g" % (self.current_it, self.current_convergence))
