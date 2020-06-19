"""
implements the greedy reduced basis
algorithm with
iterative modified gram-schmidt orthogonalisation

    - http://iacs-courses.seas.harvard.edu/courses/am205/slides/am205_lec08.pdf
    - https://www.math.uci.edu/~ttrogdon/105A/html/Lecture23.html
    - Algorithm from Hoffman, `Iterative Algorithms for Gram-Schmidt Orthogonalization`
    - Chad Galley rompy package
    - Blackman+ 2017
    - Field+ 2014
"""

import numpy as np
import rompy as rp


class Integration(object):
    """
    class for function integration
    based on Chad Galley's rompy
    https://github.com/Cyberface/rompy/blob/master/rompy/integrals.py
    """

    def __init__(self):
        pass

    def integral(self, f):
        return np.dot(self.weights, f)

    def dot(self, f, g):
        return np.dot(self.weights, f.conj()*g)

    def norm(self, f):
        return np.sqrt(np.dot(self.weights, f.conj()*f).real)


class Riemann(Integration):
    def __init__(self, interval, num):
        super().__init__()

        self.interval = interval
        self.num = num

        self.nodes, self.weights = \
            self.make_quadrature_rules(self.interval, self.num)

    def make_quadrature_rules(self, interval, num):
        a = interval[0]
        b = interval[1]
        nodes = np.linspace(a, b, num=num)
        weights = np.ones(num, dtype='double')
        weights = (b-a)/(num-1) * weights

        return nodes, weights


class Trapezoidal(Integration):
    def __init__(self, interval, num):
        super().__init__()

        self.interval = interval
        self.num = num

        self.nodes, self.weights = \
            self.make_quadrature_rules(self.interval, self.num)

    def make_quadrature_rules(self, interval, num):
        a = interval[0]
        b = interval[1]
        nodes = np.linspace(a, b, num=num)
        weights = np.ones(num, dtype='double')
        weights[0] = 0.5
        weights[-1] = 0.5
        weights = (b-a)/(num-1) * weights

        return nodes, weights


class GreedyReducedBasis(object):
    """
    based upon Chad Galley's rompy package
    """
#     def __init__(self, seed_training_space, seed_index, integration):

    def __init__(self, integration):
        """
        """
        self.integration = integration

        # 1. set initial basis to be the `seed_index`
        # vector from the `seed_training_space`
        # i.e. `seed_training_space[seed_index]`

        # 2. find new greedy point (GP)

        # 3. add new GP to basis

        # 4. validate basis

        pass

    def update_greedy_points(self, new_point):

        npoints = self.greedy_points.shape[0]
        try:
            ndim = self.greedy_points.shape[1]
            new = np.zeros(shape=(npoints+1, ndim))
        except:
            #             ndim = 1
            new = np.zeros(npoints+1)

        new[:-1] = self.greedy_points

        new[-1] = new_point
        self.greedy_points = new

        return

    def compute_projection_coefficients(self, basis, ts):
        """
        for a single new vector compute it's projection onto the basis
        """
        return np.array([self.integration.dot(ts, b) for b in basis])

    def compute_projection_coefficients_array(self, basis, ts):
        """
        loop over all vectors in the training set (ts)
        and compute their projection coefficients by
        computes their projection onto the basis

        returns:
            alphas: numpy.ndarray
                alphas.shape = (ts.shape[0], basis.shape[0])
        """

        n_vectors = ts.shape[0]
        n_basis = basis.shape[0]

        alpha = np.zeros(shape=(n_vectors, n_basis))

        for i in range(n_vectors):
            alpha[i] = self.compute_projection_coefficients(basis, ts[i])
        return alpha

    def compute_representation(self, alpha, basis):
        """
        if you have the basis coefficients then
        compute the representation with current basis
        """
        return np.dot(alpha, basis)

    def compute_representation_ts(self, ts):
        """
        giving a single training point compute the
        representation by the current basis
        """
        alpha = self.compute_projection_coefficients(self.basis, ts)
        return self.compute_representation(alpha, self.basis)

    def compute_greedy_error(self, ts):
        """
        computes greedy error for current basis and an input training set
        returns:
            greedy_errors: numpy.ndarray
                array of projection (greedy) errors
        """
        alphas = self.compute_projection_coefficients_array(self.basis, ts)

        n_vectors, n_dim = ts.shape
        greedy_errors = np.zeros(n_vectors)

        for i in range(n_vectors):
            rep = self.compute_representation(alphas[i], self.basis)

            greedy_errors[i] = self.integration.norm(ts[i] - rep)**2

        return greedy_errors

    def find_new_greedy_point(self, basis, ts):
        """
        using the current basis find the point
        in the training set that has the
        largest projection error

        returns:
            max_err_idx: int, index of maximum projection (greedy)
            error
        """

        greedy_errors = self.compute_greedy_error(ts)

        max_err_idx = np.argmax(greedy_errors)
        max_err = greedy_errors[max_err_idx]

        return max_err, max_err_idx

    def _add_basis(self, v, basis, tol, max_iter):
        """
        once we have found the
        vector in the training space
        with the largest greedy-error
        we want to add it to our basis.

        We do this by othogonalising it against
        the current basis using an
        iterative modified gram-schmidt algorithm (IMGS)
        """
        norm = self.integration.norm(v)
        e = v / norm

        flag, ctr = 0, 1
        while flag == 0:
            for b in basis:
                e -= b*self.integration.dot(b, e)
            new_norm = self.integration.norm(e)
            if new_norm / norm <= tol:
                norm = new_norm
                ctr += 1
                if ctr > max_iter:
                    msg = "WARNING max number of iter reached " \
                        + "basis may not be orthonormal."
                    print(msg, flush=True)
                    flag = 1
            else:
                flag = 1

        return e/new_norm

    def build_seed_basis(self, ts, ts_coords, tol=0.5, max_iter=3):
        """

        This builds an orthonormal basis out of the input
        training set `ts`.

        This is used as the `seed basis` so that things
        like deterministic or boundary points can be included.

        input:
            ts: numpy.ndarray
                The "training set" (ts).
                the rows are the individual vectors
                the columns are the components of each vector
                ts.shape[0] = number of vectors
                ts.shape[1] = number of components === dimensionality of each vector
            ts_coords: numpy.ndarray
                ts_coords.shape[0] = number of vectors
                ts_coords.shape[1] = number of parameters === dimensionality of parameter space
        returns:
            nothing

        sets the `basis` attribute
        """

        n_vectors, n_dim = ts.shape

        # save seed training set points to the greedy points
        self.greedy_points = ts_coords.copy()

        # allocated memory for basis
        basis = np.zeros(shape=(n_vectors, n_dim))

        # select first element of training set as the
        # initial basis vector
        # FIXME: should shuffle to pick a random
        # vector to be the first one.
        norm = self.integration.norm(ts[0])
        basis[0] = ts[0] / norm

        for i in range(1, n_vectors):
            basis[i] = self._add_basis(
                ts[i], basis[:i], tol=tol, max_iter=max_iter)

        self.basis = basis

    def greedy_sweep(self, ts, ts_coords, greedy_tol=1e-12, imgs_tol=0.5, imgs_max_iter=3, verbose=True):
        """
        for a given training set performs
        a number of `greedy_iter` stopping if
            1. tol is met - #TODO currently only this is implemented
            2. number of steps is met or
            3. if the training set has been exhausted
        """

        # list to store the indicies of the parameters in the current greedy
        # sweep to avoid adding the same vector twice
        self.indicies = []
        self.greedy_errors = []

        steps = len(ts)

        for step in range(steps):
            status = self.greedy_step(
                step, ts, ts_coords, greedy_tol, imgs_tol, imgs_max_iter, verbose)
            if status in ['tol', 'idx']:
                break
            else:
                continue

        self.nbasis = len(self.greedy_points)
        return

    def greedy_step(self, step, ts, ts_coords, greedy_tol, imgs_tol=0.5, imgs_max_iter=3, verbose=True):
        """
        perform an iteration of the greedy algorithm
        possibly adding a new vector to the basis
        """
        # index with worst representation error
        max_error, idx = self.find_new_greedy_point(self.basis, ts)
        if max_error <= greedy_tol:
            if verbose:
                print("tolerance reached. exiting", flush=True)
            return 'tol'

        self.greedy_errors.append(max_error)

        # check that potential new point is not already in the basis already
        # if it is then exit without adding it again
        # if it is not then add it.

        if step != 0:
            if idx in self.indicies:
                if verbose:
                    print(
                        "proposed new greedy point is already in basis. exiting", flush=True)
                return 'idx'

        if verbose:
            print(f"step = {step}, error = {max_error}", flush=True)

        self.indicies.append(idx)
        self.update_greedy_points(np.array(ts_coords[idx]))

        new_element = self._add_basis(
            ts[idx], self.basis, tol=imgs_tol, max_iter=imgs_max_iter)

        # extend basis array by one
        new_basis = np.zeros(
            shape=(self.basis.shape[0]+1, self.basis.shape[1]))
        new_basis[:-1] = self.basis
        new_basis[-1] = new_element

        self.basis = new_basis
        return

    def setup_eim(self):
        """
        instantiate instance of rp.EmpiricalInterpolant.
        Computes EIM basis
        """
        self.eim = rp.EmpiricalInterpolant(self.basis)

    def build_eim(self, eim_ts):
        """
        builds an empirical interpolant for the current basis
        input:
            eim_ts: numpy.ndarray
                training set generated at the self.greedy_points
        """
        if hasattr(self, 'eim') is False:
            self.setup_eim()

        self.eim.make_data(eim_ts)
