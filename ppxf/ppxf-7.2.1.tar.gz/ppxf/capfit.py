"""
################################################################################

Copyright (C) 2017-2020, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your research,
I would appreciate an acknowledgement to the use of the
"CapFit constrained least-squares optimization program, which combines
the Sequential Quadratic Programming and the Levenberg-Marquardt methods
and is included in the pPXF Python package of Cappellari (2017)".

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

###############################################################################

Changelog
---------

V2.0.2: MC, Oxford, 20 June 2020
--------------------------------

- ``capfit``: new keyword ``cond`` (passed to ``lsqlin``).
- ``capfit``: Use ``bvls`` to solve quadratic subproblem with only ``bounds``.

V2.0.1: MC, Oxford, 24 January 2020
-----------------------------------

- New keyword ``cond`` for ``lsqlin``.
- Relaxed assertion for inconsistent inequalities in ``lsqlin`` to avoid false
  positives. Thanks to Kyle Westfall (UCO Lick) for a detailed bug report.

V2.0.0: MC, Oxford, 10 January 2020
-----------------------------------

- Use the new general linear least-squares optimization
  function``lsqlin`` to solve the quadratic subproblem.
- Allow for linear inequality/equality constraints
  ``A_ineq``, ``b_ineq`` and  ``A_eq``, ``b_eq``

V1.0.7: MC, Oxford, 10 October 2019
-----------------------------------

- Included complete documentation.
- Improved print formatting.
- Return ``.message`` attribute.
- Improved ``xtol`` convergence test.
- Only accept final move if ``chi2`` decreased.
- Strictly satisfy bounds during Jacobian computation.

V1.0.6: MC, Oxford, 11 June 2019
++++++++++++++++++++++++++++++++

- Use only free parameters for small-step convergence test.
- Explain in words convergence status when verbose != 0
- Fixed program stop when abs_step is undefined.
- Fixed capfit ignoring optional max_nfev.

V1.0.5: MC, Oxford, 28 March 2019
+++++++++++++++++++++++++++++++++

- Raise an error if the user function returns non-finite values.

V1.0.4: MC, Oxford, 30 November 2018
++++++++++++++++++++++++++++++++++++

- Allow for a scalar ``abs_step``.

V1.0.3: MC, Oxford, 20 September 2018
+++++++++++++++++++++++++++++++++++++

- Raise an error if one tries to tie parameters to themselves.
  Thanks to Kyle Westfall (Univ. Santa Cruz) for the feedback.
- Use Python 3.6 f-strings.

V1.0.2: MC, Oxford, 10 May 2018
+++++++++++++++++++++++++++++++

- Dropped legacy Python 2.7 support.

V1.0.1: MC, Oxford, 13 February 2018
++++++++++++++++++++++++++++++++++++

- Make output errors of non-free variable exactly zero.

V1.0.0: MC, Oxford, 15 June 2017
++++++++++++++++++++++++++++++++

- Written by Michele Cappellari

"""
import numpy as np
from scipy import optimize, linalg

################################################################################

def fprint(x):
    return (" {:.4g}"*len(x)).format(*x)

################################################################################

def chi2(x):
    return x @ x

################################################################################

def cov_err(jac):
    """
    Covariance and 1sigma formal errors calculation (i.e. ignoring covariance).
    See e.g. Press et al. 2007, Numerical Recipes, 3rd ed., Section 15.4.2

    """
    U, s, Vh = linalg.svd(jac, full_matrices=False)
    w = s > np.spacing(s[0])*max(jac.shape)
    cov = (Vh[w].T/s[w]**2) @ Vh[w]
    perr = np.sqrt(np.diag(cov))

    return cov, perr

###############################################################################

def lsqlin(A_lsq, b_lsq, A_ineq=None, b_ineq=None, A_eq=None, b_eq=None,
           bounds=None, cond=None):
    """
    Linear least-squares problem with both linear
    equalities and inequalities constraints

          Minimize      || A_lsq @ x - b_lsq ||
          Subject to    A_ineq @ x <= b_ineq
          and           A_eq @ x == b_eq
          and           bounds[0] <= x <= bounds[1]

    Implements the approach described in Chapter 23 of
    Lawson & Hanson, 1995, Solving Least Squares Problems, SIAM
    https://doi.org/10.1137/1.9781611971217

    cond: is the cutoff for small singular values used to determine
    the effective rank of A_lsq. Singular values smaller than
    cond*largest_singular_value are considered zero.

    """
    A_lsq, b_lsq = map(np.asarray, (A_lsq, b_lsq))
    assert A_lsq.shape[0] == b_lsq.size, "A_lsq/b_lsq size mismatch"

    if A_ineq is not None:
        A_ineq, b_ineq = map(np.asarray, (A_ineq, b_ineq))
        assert A_ineq.shape[0] == b_ineq.size, "A_ineq/b_ineq size mismatch"
        assert A_ineq.shape[1] == A_lsq.shape[1], "A_ineq/A_lsq size mismatch"
        A_ineq, b_ineq = -A_ineq, -b_ineq  # Adopt common sign convention

    # Convert bounds into linear inequality constraints
    if (bounds is not None) and np.any(np.abs(bounds) != np.inf):
        m, n = A_lsq.shape
        bounds = np.asarray([np.resize(b, n) for b in bounds])
        wl = np.flatnonzero(bounds[0] != -np.inf)
        wu = np.flatnonzero(bounds[1] != np.inf)
        A_bnd = np.zeros((wl.size + wu.size, n))
        A_bnd[np.arange(wl.size), wl] = 1
        A_bnd[wl.size + np.arange(wu.size), wu] = -1
        b_bnd = np.append(bounds[0, wl], -bounds[1, wu])

        if A_ineq is None:
            A_ineq, b_ineq = A_bnd, b_bnd
        else:
            A_ineq = np.vstack([A_ineq, A_bnd])
            b_ineq = np.append(b_ineq, b_bnd)

    # Eliminate equality constraints with change of variables
    if A_eq is not None:
        A_eq, b_eq = map(np.asarray, (A_eq, b_eq))
        assert A_eq.shape[0] == b_eq.size, "A_eq/b_eq size mismatch"
        assert A_eq.shape[1] == A_lsq.shape[1], "A_eq/A_lsq size mismatch"
        m1, n = A_eq.shape
        Q, R, p = linalg.qr(A_eq, pivoting=True)
        R1, R2 = np.hsplit(R, [m1])
        k1 = linalg.solve_triangular(R1, R2)
        Qb = Q.T @ b_eq
        k2 = linalg.solve_triangular(R1, Qb)
        A_lsq1, A_lsq2 = np.hsplit(A_lsq[:, p], [m1])
        A_lsq = A_lsq2 - A_lsq1 @ k1
        b_lsq = b_lsq - A_lsq1 @ k2

        # Apply transformation to inequality constraints
        if A_ineq is not None:
            A_ineq1, A_ineq2 = np.hsplit(A_ineq[:, p], [m1])
            A_ineq = A_ineq2 - A_ineq1 @ k1
            b_ineq = b_ineq - A_ineq1 @ k2

    if A_ineq is None:
        # Solve unconstrained problem
        x = linalg.lstsq(A_lsq, b_lsq, cond=cond)[0]
    else:
        # Solve inequality-constrained problem
        U, s, V = linalg.svd(A_lsq, full_matrices=False)
        tol = np.spacing(s[0])*max(A_lsq.shape) if cond is None else cond*s[0]
        w = s > tol
        sinv = np.zeros_like(s)
        sinv[w] = 1/s[w]
        Vs = sinv*V.T
        fu = b_lsq @ U
        A = A_ineq @ Vs
        E = np.vstack([A.T, b_ineq - A @ fu])
        f = np.append(np.zeros_like(s), 1)
        u = optimize.nnls(E, f, maxiter=15*E.shape[1])[0]
        r = E @ u - f
        assert linalg.norm(r) != 0, "Incompatible constraints or degenerate Jacobian"
        x = Vs @ (fu - r[:-1]/r[-1])

    # Back to original variables
    if A_eq is not None:
        x1 = linalg.solve_triangular(R1, Qb - R2 @ x)
        x = np.hstack([x1, x])
        x[p] = x.copy()

    return x

################################################################################

class capfit:

    """
    CapFit
    ------

    ``CapFit`` solves linearly-constrained least-squares optimization problems.
    Linear inequality/equality constraints and bound constraints are supported.
    Moreover one can easily tie or fix some parameters without having to
    modify the fitting function.

    ``CapFit`` combines two successful ideas:

        (i) The Sequential Quadratic Programming (SQP) approach,
            specialized for the case of linear constraints;
        (ii) The Levenberg-Marquardt (LM) method.

    It was designed for the common situations where the user function is not
    a simple analytic function but is the result of some complex calculations
    and is more expensive to compute than the small quadratic subproblem.

    I found ``CapFit`` performance generally better, in terms of robustness
    and number of functions evaluations, than the best uncostrained or
    bound-constrained least-squares algorithms currently available, but
    in addition ``CapFit`` allows for more general constraints.

    Given a function of ``n`` model parameters ``x_k`` returning the ``m``
    model residuals ``f_j(x)``, ``CapFit`` finds a local minimum of the cost
    function::

        G(x) = sum[f_j(x)^2]

    subject to::

        A_ineq @ x <= b_ineq            # Linear Inequality Constraints
        A_eq @ x == b_eq                # Linear Equality Constraints
        bounds[0] <= x <= bounds[1]     # Bounds
        x_k = f(x)                      # Tied Parameters
        x_k = a_k                       # Fixed Parameters

    Attribution
    -----------

    If you use this software for your research, please cite the Python package
    ``ppxf`` by `Cappellari (2017)
    <http://adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_, where this
    software was introduced. The BibTeX entry for the paper is::

        @ARTICLE{Cappellari2017,
            author = {{Cappellari}, M.},
            title = "{Improving the full spectrum fitting method:
                accurate convolution with Gauss-Hermite functions}",
            journal = {MNRAS},
            eprint = {1607.08538},
            year = 2017,
            volume = 466,
            pages = {798-811},
            doi = {10.1093/mnras/stw3020}
        }

    Usage Examples
    --------------

    .. code-block:: python

        import numpy as np
        import matplotlib.pyplot as plt

        from ppxf.capfit import capfit

        def model(p, x, a):
            return p[0]*np.exp(-0.5*(x - p[1]/a)**2/p[2]**2)

        def resid(p, x=None, y=None, yerr=None, a=None):
            ymod = model(p, x, a)
            return (y - ymod)/yerr

        a = 1.0
        x = np.linspace(-3, 3, 100)
        ptrue = np.array([2., -1., 0.5])
        y = model(ptrue, x, a)
        yerr = np.full_like(y, 0.1)
        y += np.random.normal(0, yerr, x.size)
        p0 = np.array([1., 1., 1.])
        kwargs = {'x': x, 'y': y, 'yerr': yerr, 'a': a}

        print("#### Unconstrained case ####")
        res = capfit(resid, p0, kwargs=kwargs, verbose=1)

        print("#### Bounds on parameters ####")
        res = capfit(resid, p0, kwargs=kwargs, verbose=1,
                     bounds=[(-np.inf, -0.95, 0.55), np.inf])

        print("#### Tied parameters ####")
        res = capfit(resid, p0, kwargs=kwargs, tied=['', '-p[0]/2', ''], verbose=1)

        print("#### Fixed parameters ####")
        res = capfit(resid, [1, 1, 0.5], kwargs=kwargs, fixed=[0, 0, 1], verbose=1)

        plt.plot(x, y, 'o')
        plt.plot(x, model(res.x, x, a))

    Input Parameters
    ----------------

    fun : callable
        Function which computes the vector of residuals, with the signature
        ``fun(x, *args, **kwargs)``, i.e., the minimization proceeds with
        respect to its first argument. The argument ``x`` passed to this
        function is an 1-d darray of shape (n,).
        The function must return a 1-d array of shape (m,).
    x0 : array_like with shape (n,) or float
        Initial guess on independent variables. For guaranteed convergence, the
        initial guess must be feasible (satsfies the constraints) and for this
        reason an error is returned if it is not the case.


    Optional Keywords
    -----------------

    bounds : 2-tuple of array_like, optional
        Lower and upper bounds (lb, ub) on independent variables.
        Defaults to no bounds. Each array must match the size of `x0` or be a
        scalar, in the latter case a bound will be the same for all variables.
        Use ``np.inf`` with an appropriate sign to disable bounds on all or
        some variables.
    cond : float, optional
        Cutoff for small singular values used to determine the effective rank of
        the Jacobian. Singular values smaller than cond*largest_singular_value
        are considered zero.
    ftol : float or None, optional
        Tolerance for termination by the change of the cost function (default
        is 1e-4). The optimization process is stopped when both
        ``prered < ftol`` and ``abs(actred) < ftol`` and additionally
        ``actred <= 2*prered``, where ``actred`` and ``prered`` are the actual
        and predicted relative changes respectively
        (as described in More' et al. 1980).
    xtol : float or None, optional
        Tolerance for termination by the change ``dx`` of the independent
        variables (default is 1e-4). The condition is
        ``norm(dx) < xtol*(xtol + norm(xs))`` where ``xs`` is the value of ``x``
        scaled according to `x_scale` parameter (see below).
        If None, the termination by this condition is disabled.
    x_scale : array_like or 'jac', optional
        Characteristic scale of each variable. Setting `x_scale` is equivalent
        to reformulating the problem in scaled variables ``xs = x/x_scale``.
        An alternative view is that the initial size/2 of the box trust region
        along j-th dimension is given by ``x_scale[j]`` and the box ratains its
        shape during the optimization. Improved convergence is achieved by
        setting `x_scale` such that a step of a given size along any of the
        scaled variables has a similar effect on the cost function.  If set to
        'jac', the scale is iteratively updated using the inverse norms of the
        columns of the Jacobian matrix (as described in More' 1978).
    max_nfev : None or int, optional
        Maximum number of function evaluations before the termination
        (default is 100*n).
    diff_step : None, scalar or array_like, optional
        Determines the relative step size for the finite difference
        approximation of the Jacobian. The actual step is computed as
        ``diff_step*maximum(1, abs(x))`` (default=1e-4)
    abs_step : None, scalar or array_like, optional
        Determines the absolute step size for the finite difference
        approximation of the Jacobian. Default is None and ``diff_step``
        is used instead.
    tied : array_like with shape (n,), optional
        A list of string expressions. Each expression "ties" the parameter to
        other free or fixed parameters.  Any expression involving constants and
        the parameter array ``p[j]`` are permitted. Since they are totally
        constrained, tied parameters are considered to be fixed; no errors are
        computed for them.

        This is a vector with the same dimensions as ``x0``. In practice,
        for every element of ``x0`` one needs to specify either an empty string
        ``''`` implying that the parameter is free, or a string expression
        involving some of the variables ``p[j]``, where ``j`` represents the
        index of the vector of parameters. See usage example.
    A_ineq: array_like with shape (p, n), optional
        Defines the linear inequality constraints on the fitted parameters::

            A_ineq @ x <= b_ineq

    b_ineq: array_like with shape (p), optional
        See description of ``A_ineq``.
    A_eq: array_like with shape (q, n), optional
        Defines the linear equality constraints on the fitted parameters::

            A_eq @ x == b_eq

        The same result can be achieved using the ``tied``
        keyword, which also allows for non-linear equality constraints.
    b_eq: array_like with shape (q), optional
        See description of ``A_eq``.
    verbose : {0, 1, 2}, optional
        Level of algorithm's verbosity:
            * 0 (default) : work silently.
            * 1 : display a termination report.
            * 2 : display progress during iterations.
    args, kwargs : tuple and dict, optional
        Additional arguments passed to `fun`, empty by default.
        The calling signature is ``fun(x, *args, **kwargs)``.

    Returns
    -------

    `OptimizeResult` with the following fields defined:

    x : ndarray, shape (n,)
        Solution found.
    cost : float
        Value of the cost function at the solution.
    fun : ndarray, shape (m,)
        Vector of residuals at the solution.
    jac : ndarray, shape (m, n)
        Modified Jacobian matrix at the solution, in the sense that J.T @ J
        is a Gauss-Newton approximation of the Hessian of the cost function.
    grad : ndarray, shape (m,)
        Gradient of the cost function at the solution.
    nfev : int
        Number of function evaluations done.
    njev : int
        Number of Jacobian evaluations done.
    status : int
        The reason for algorithm termination:
            * -1 : improper input parameters status
            *  0 : the maximum number of function evaluations is exceeded.
            *  2 : `ftol` termination condition is satisfied.
            *  3 : `xtol` termination condition is satisfied.
            *  4 : Both `ftol` and `xtol` termination conditions are satisfied.
    message : str
        Verbal description of the termination reason.
    success : bool
        True if one of the convergence criteria is satisfied (`status` > 0).

    Notes
    -----

    An early SQP method specialized for linear constraints was described in
    `Fletcher (1972) <https://doi.org/10.1007/BF01584540>`_

    A general textbook description of the *uncostrained* LM algorithm is in:

    - Chapter 5.2 of `Fletcher R., 1987, Practical Methods of Optimization, 2nd ed., Wiley
      <http://doi.org/10.1002/9781118723203>`_
    - Chapter 10.3 of `Nocedal J. & Wright S.J., 2006, Numerical Optimization, 2nd ed., Springer
      <http://doi.org./10.1007/978-0-387-40065-5>`_

    The original papers introducing the LM method *without* bounds are:

    - `Levenberg K., 1944, Quart. Appl. Math., 164, 2
      <https://doi.org/10.1090/qam/10666>`_
    - `Marquardt D.W., 1963, J. Soc. Indust. Appl. Math, 11, 431
      <https://doi.org/10.1137/0111030>`_

    The Jacobian scaling and convergence tests follow
    `More', J.J., Garbow, B.S. & Hillstrom, K.E. 1980, User Guide for MINPACK-1,
    Argonne National Laboratory Report ANL-80-74 <http://cds.cern.ch/record/126569>`_

    """
    def __init__(self, func, p1, abs_step=None, bounds=(-np.inf, np.inf),
                 cond=None, diff_step=1e-4, fixed=None, ftol=1e-4, max_nfev=None,
                 tied=None, A_ineq=None, b_ineq=None, A_eq=None, b_eq=None,
                 verbose=0, x_scale='jac', xtol=1e-4, args=(), kwargs={}):

        p1 = np.array(p1, dtype=float)  # Make copy to leave input unchanged
        bounds = np.asarray([np.resize(b, p1.size) for b in bounds])
        assert np.all(bounds[0] < bounds[1]), "Must be lower bound < upper bound"
        p1 = p1.clip(*bounds)   # Force initial guess within bounds

        bounds_only = all(v is None for v in [A_ineq, b_ineq, A_eq, b_eq])
        if not bounds_only:
            if A_ineq is not None:
                assert np.all(A_ineq @ p1 <= b_ineq), "Initial guess is unfeasible for inequality"
            if A_eq is not None:
                assert np.allclose(A_eq @ p1, b_eq), "Initial guess is unfeasible for equality"

        fixed = np.full(p1.size, False) if fixed is None else np.asarray(fixed)
        if tied is None:
            tied = np.full(p1.size, '')
        else:
            assert np.all([f'p[{j}]' not in td for j, td in enumerate(tied)]), \
                "Parameters cannot be tied to themselves"
        assert len(p1) == len(fixed) == len(tied), \
            "`x0`, `fixed` and `tied` must have the same size"

        self.nfev = self.njev = 0
        self.diff_step = diff_step
        self.abs_step = abs_step
        self.tied = np.asarray([a.strip() for a in tied])
        self.free = (np.asarray(fixed) == 0) & (self.tied == '')
        self.args = args
        self.kwargs = kwargs
        self.max_nfev = 100*self.free.sum() if max_nfev is None else max_nfev
        self.ftol = ftol
        self.xtol = xtol
        self.verbose = verbose

        f1 = self.call(func, p1)
        assert f1.ndim == 1, "The fitting function must return a vector of residuals"
        J1 = self.fdjac(func, p1, f1, bounds)
        dd = linalg.norm(J1, axis=0)
        mx = np.max(dd)
        eps = np.finfo(float).eps
        dd[dd < eps*(eps + mx)] = 1  # As More'+80
        lam = 0.01*mx**2  # 0.01*max(diag(J1.T @ J1))

        if verbose == 2:
            print(f"\nStart lambda: {lam:.4g}  chi2: {chi2(f1):.4g}\nStart p:" + fprint(p1))

        while(True):

            if x_scale == 'jac':
                dd = np.maximum(dd, linalg.norm(J1, axis=0))
            else:
                dd = np.ones_like(p1)/x_scale

            # Solve the constrained quadratic sub-problem
            dn = dd/np.max(dd)
            A = np.vstack([J1, np.diag(np.sqrt(lam)*dn)])
            b = np.append(-f1, np.zeros_like(p1))
            if bounds_only:
                h = optimize.lsq_linear(A, b, bounds=bounds-p1, method='bvls').x
            else:
                b_ineq_p = None if A_ineq is None else b_ineq - A_ineq @ p1
                b_eq_p = None if A_eq is None else b_eq - A_eq @ p1
                h = lsqlin(A, b, A_ineq, b_ineq_p, A_eq, b_eq_p, bounds=bounds-p1, cond=cond)

            p2 = p1 + h
            f2 = self.call(func, p2)

            # Actual versus predicted chi2 reduction
            actred = 1 - chi2(f2)/chi2(f1)
            prered = 1 - chi2(f1 + J1 @ h)/chi2(f1)
            ratio = actred/prered

            status = self.check_conv(lam, f2, p2, h, dd, actred, prered)

            if status != -1:
                if actred > 0:
                    p1, f1 = p2, f2
                if self.verbose:
                    print(f"\n{self.message}\nFinal iter: {self.njev}  "
                          f"Func calls: {self.nfev}  chi2: {chi2(f1):.4g}  "
                          f"Status: {status}\nFinal p:" + fprint(p1) + "\n")
                break

            # Algorithm (5.2.7) of Fletcher (1987)
            # Algorithm 4.1 in Nocedal & Wright (2006)
            if ratio < 0.25:
                lam *= 4
            elif ratio > 0.75:
                lam /= 2

            if ratio > 0.01:  # Successful step: move on
                J2 = self.fdjac(func, p2, f2, bounds)
                p1, f1, J1 = p2, f2, J2

        self.x = p1
        self.cost = 0.5*chi2(f1)  # as in least_squares()
        self.fun = f1
        self.jac = J1
        self.grad = J1.T @ f1
        self.status = status
        self.success = status > 0
        self.cov, self.x_err = cov_err(J1)
        self.x_err[~self.free] = 0

################################################################################

    def fdjac(self, func, pars, f, bounds):

        self.njev += 1

        if self.abs_step is None:
            h = self.diff_step*np.maximum(1.0, np.abs(pars))  # as in least_squares()
        else:
            h = self.abs_step*np.ones_like(pars)

        x = pars + h
        hits = (x < bounds[0]) | (x > bounds[1])

        # Respect bounds in finite differences
        if np.any(hits):
            dist = np.abs(bounds - pars)
            fits = np.abs(h) <= np.maximum(*dist)
            h[hits & fits] *= -1
            forward = (dist[1] >= dist[0]) & ~fits
            backward = (dist[1] < dist[0]) & ~fits
            h[forward] = dist[1, forward]
            h[backward] = -dist[0, backward]

        # Compute derivative for free parameters
        w = np.flatnonzero(self.free)
        jac = np.zeros([f.size, pars.size])
        for j in w:
            pars1 = pars.copy()
            pars1[j] += h[j]
            f1 = self.call(func, pars1)
            jac[:, j] = (f1 - f)/h[j]

        return jac

################################################################################

    def call(self, func, p):

        self.nfev += 1
        w = np.flatnonzero(self.tied != '')
        for j in w:   # loop can be empty
            exec(f'p[{j}] = {self.tied[j]}')
        resid = func(p, *self.args, **self.kwargs)
        assert np.all(np.isfinite(resid)), \
            "The fitting function returned infinite residuals"

        return resid

################################################################################

    def check_conv(self, lam, f, p, h, dn, actred, prered):

        status = -1
        if self.nfev > self.max_nfev:
            self.message = "Terminating on function evaluations count"
            status = 0

        if prered < self.ftol and abs(actred) < self.ftol and actred <= 2*prered:  # (More'+80)
            self.message = "Terminating on small function variation (ftol)"
            status = 2

        if linalg.norm((dn*h)[self.free]) < self.xtol*(self.xtol + linalg.norm((dn*p)[self.free])):
            if status == 2:
                self.message = "Both ftol and xtol convergence test are satisfied"
                status = 4
            else:
                self.message = "Terminating on small step (xtol)"
                status = 3

        if self.verbose == 2:
            print(f"\niter: {self.njev}  lambda: {lam:.4g}  chi2: {chi2(f):.4g}"
                  f"  ratio: {actred/prered:.4g}\np:" + fprint(p) + "\nh:" + fprint(h))

        return status

################################################################################
