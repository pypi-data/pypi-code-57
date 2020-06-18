import numpy as np
import scipy.linalg
import scipy.spatial

import itertools
import collections

import spglib


class SymmetryFinder:
    def __init__(self):
        pass

    def molecular_pointgroup(self, coordinates, atomic_numbers):
        min_x, min_y, min_z = [min(p) for p in coordinates.T]
        # the 0.1 ensures that the fractional positions are sufficiently smaller than 1,
        # which appears to be necessary for accurate symmetry determination, and it
        # also ensures that max_x,max_y,max_z are all > 0 so that scipy.linalg.inv(lattice)
        # is well-defined
        max_x, max_y, max_z = [
            max(abs(p) - min) + 0.1
            for p, min in zip(coordinates.T, (min_x, min_y, min_z))
        ]

        lattice = np.diag([max_x, max_y, max_z])
        fractional_positions = coordinates @ scipy.linalg.inv(lattice)

        cell = (lattice, fractional_positions, atomic_numbers)

        return spglib.get_spacegroup_type(
            spglib.get_symmetry_dataset(cell=cell)["hall_number"]
        )["pointgroup_international"]

    def get_rotations(self, pointgroup_symbol):
        """
        Generates two lists of rotations, one proper and one improper, which are symmetries corresponding to the given point group symbol.

        Parameters
        ----------
        pointgroup_symbol: str
            String denoting a Schoenflies point group symbol.

        Returns
        -------
        list of numpy.ndarrays:
            List of unique proper rotation matrices corresponding to pointgroup_symbol, excluding the identity matrix.
        list of numpy.ndarrays:
            List of unique improper rotation matrices corresponding to pointgroup_symbol, excluding the negative identity matrix.
        """
        representative_numbers = {
            spglib.get_spacegroup_type(i)["pointgroup_international"]: i
            for i in range(1, 531)
        }
        hall_number = representative_numbers[
            pointgroup_symbol
        ]  # lowest Hall number of a space group which contains the given point group.
        # hall_number = self.get_representative_hall_number(pointgroup_symbol=pointgroup_symbol) # lowest Hall number of a space group which contains the given point group.

        # symmetry_dict = spglib.get_symmetry_from_database(hall_number)
        # rotations = symmetry_dict['rotations'][(symmetry_dict['translations'] == 0).sum(axis=1) == 3]
        rotations = spglib.get_symmetry_from_database(hall_number)["rotations"]
        _, unique_indices = np.unique(ar=rotations, axis=0, return_index=True)
        unique_rotations = rotations[sorted(unique_indices)]

        # exact (as opposed to np.isclose) conditions on determinant and identity-ness are fine since spglib gives rotation matrices with integer elements
        determinants = np.linalg.det(unique_rotations)
        proper_rotations = tuple(
            R
            for R, det in zip(unique_rotations, determinants)
            if det == 1 and (R @ R.T == np.eye(3)).all() and not (R == np.eye(3)).all()
        )
        improper_rotations = tuple(
            R
            for R, det in zip(unique_rotations, determinants)
            if det == -1
            and (R @ R.T == np.eye(3)).all()
            and not (R == -np.eye(3)).all()
        )

        return proper_rotations, improper_rotations


class AxesGenerator:
    def __init__(self, seed=None):
        self.sf = SymmetryFinder()
        self.geometry = Geometry(seed=seed)

    def generate_axes(self, pointgroup_symbol, inertia_tensor):
        axes, A, B = self._generate_unaligned_axes(pointgroup_symbol=pointgroup_symbol)

        alignment_matrix = self._align_axes_with_molecule(inertia_tensor=inertia_tensor)
        axes = alignment_matrix.T @ axes if not (axes == np.eye(3)).all() else axes
        A = alignment_matrix.T @ A if A is not None else A
        B = alignment_matrix.T @ B if B is not None else B
        wprime = (A.T @ axes[:, -1])[:, None] if wprime is not None else wprime

        return axes, A, B, wprime
        # if A is not None and B is not None:

    #            wprime = (A.T@axes[:,-1])[:,None]
    #        aligned_wprime = alignment_matrix.T@wprime #FIXME: is this correct??
    # else:
    #    aligned_prime = None

    # if self._validate_axes(axes=axes):
    #     return aligned_axes,aligned_A,aligned_B,aligned_wprime
    # else:
    #     print('Error validating vectors!')
    #     return np.eye(3),None,None,None

    def _generate_unaligned_axes(self, pointgroup_symbol):
        proper, improper = self.sf.get_rotations(pointgroup_symbol=pointgroup_symbol)

        num_proper = len(proper)
        num_improper = len(improper)

        if num_proper == 0 and num_improper == 0:
            # print('No usable symmetries found. Returning Cartesian axes.')
            axes, A, B = self._generate_unaligned_axes_no_symmetries()
        elif num_proper == 0 and num_improper == 1:
            # print('One rotoflection found. Generating two axes...')
            axes, A, B = self._generate_unaligned_axes_one_symmetry(R=improper[0])
        elif num_proper == 1 and num_improper == 0:
            # print('One rotation found. Generating two axes...')
            axes, A, B = self._generate_unaligned_axes_one_symmetry(R=proper[0])
        elif num_proper == 0 and num_improper > 1:
            # print('Multiple symmetries found. Generating three axes...')
            # print('Multiple symmetries found, but all symmetries have degnerate span. Generating two axes...')
            axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
                symmetries=improper
            )
        elif num_proper > 1 and num_improper == 0:
            # print('Multiple symmetries found. Generating three axes...')
            # print('Multiple symmetries found, but all symmetries have degnerate span. Generating two axes...')
            axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
                symmetries=proper
            )
        else:
            # print('Multiple symmetries found. Generating three axes...')
            # print('Multiple symmetries found, but all symmetries have degnerate span. Generating two axes...')
            axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
                symmetries=proper + improper
            )

        if self._validate_axes(axes=axes):
            return axes, A, B
        else:
            print("Error validating vectors!")
            return np.eye(3), None, None

    def _generate_unaligned_axes_no_symmetries(self):
        return np.eye(3), None, None

    def _generate_unaligned_axes_one_symmetry(self, R):
        q = self.geometry.make_nontrivial_vector(R=R)
        r = R @ q
        s = self.geometry.perpendicular_vector(a=q, b=r)

        return np.hstack([q, r, s]), R, None

    def _generate_unaligned_axes_multiple_symmetries(self, symmetries):
        excluded_generator = (
            (a, b, *self._excluded_points_and_circles(A=a, B=b))
            for a, b in itertools.product(symmetries, symmetries)
            if (not (a == b).all() and not (a == -b).all())
        )
        try:
            A, B, excluded_points, excluded_circles = next(
                (
                    (a, b, xp, xc)
                    for (a, b, xp, xc) in excluded_generator
                    if (
                        xc.shape[1] == 0
                        or (xc.shape[1] > 0 and np.linalg.matrix_rank(xc) < 3)
                    )
                )
            )
            self.geometry.add_excluded_points(excluded_points=excluded_points)
            self.geometry.add_excluded_circles(excluded_circles=excluded_circles)
            q = self.geometry.sample_axis()
            r = A @ q
            s = B @ q

            return np.hstack([q, r, s]), A, B
        except StopIteration:
            return self._generate_unaligned_axes_one_symmetry(R=symmetries[0])

    def _align_axes_with_molecule(self, inertia_tensor):
        """
        Computes the unique rotation matrix which maps the two highest-inertia
        principal vectors to the z- and y-axes, respectively.

        Parameters
        ----------
        numpy.ndarray: inertia_tensor
            3x3 numpy array specifying the inertia tensor in arbitrary units.

        Returns
        -------
        numpy.ndarray:
            3x3 numpy array representing the rotation matrix which maps the
            first two principal vectors to the z- and y-axes.
        """
        principal_moments, principal_directions = scipy.linalg.eigh(inertia_tensor)

        # FIXME: this is currently broken for monomers
        sorted_moments, sorted_directions = zip(
            *sorted(zip(principal_moments, principal_directions.T), reverse=True)
        )
        u, v, _ = sorted_directions

        Ru = self.geometry.rotation_matrix_m_to_n(m=u, n=np.array([[0, 0, 1]]).T)
        Rv = self.geometry.rotation_matrix_m_to_n(m=Ru @ v, n=np.array([[0, 1, 0]]).T)
        R = Rv @ Ru

        return R

    def _excluded_points_and_circles(self, A, B):
        """
        Construct list of excluded points and circles on unit sphere.

        Parameters
        ----------
        A,B : numpy.ndarray
            3x3 numpy arrays representating the two symmetry operations whose excluded points are being calculated.

        Returns
        -------
        numpy.ndarray:
            3xNp Numpy array representing excluded points on a unit sphere, where Np is the number of excluded points.
        numpy.ndarray:
            3xNc Numpy array representing the normal vectors of excluded circles, where Nc is the number of excluded circles.
        """
        identity = np.eye(3)
        null_bases = [
            scipy.linalg.null_space(M)
            for M in (
                A + identity,
                A - identity,
                B + identity,
                B - identity,
                A + B,
                A - B,
            )
        ]
        geometric_multiplicities = [null_basis.shape[1] for null_basis in null_bases]

        # each null basis with geometric multiplicity two results in a circle of excluded points whose normal vector is the cross product of the null basis
        excluded_circles = [
            self.geometry.perpendicular_vector(*nb.T[:, :, None])
            for nb in null_bases
            if nb.shape[1] == 2
        ]
        excluded_circles = (
            np.unique(np.hstack(excluded_circles).round(decimals=10), axis=1)
            if len(excluded_circles) > 0
            else np.array([[], [], []])
        )

        # only get excluded points which do not lie on an excluded circle
        excluded_points = [
            nb
            for nb in null_bases
            if nb.shape[1] == 1 and not np.isclose(nb.T @ excluded_circles, 0).any()
        ]
        excluded_points = (
            np.unique(np.hstack(excluded_points).round(decimals=10), axis=1)
            if len(excluded_points) > 0
            else np.array([[], [], []])
        )

        return excluded_points, excluded_circles

    def _validate_axes(self, axes):
        """
        Checks whether or not three vectors span R^3.

        Parameters
        ----------
        axes: numpy.ndarray
            3x3 Numpy array whose columns are the vectors whose span is to be checked.

        Returns
        -------
        bool
            True if the columns of vector_array span R^3, else False.
        """
        return scipy.linalg.null_space(axes).shape[1] == 0


class Geometry:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)

    def add_excluded_points(self, excluded_points):
        self.excluded_points = excluded_points

    def add_excluded_circles(self, excluded_circles):
        self.excluded_circles = excluded_circles

    def points_to_circles(self):
        new_circles = np.hstack(
            [self.perpendicular_vector(m=p) for p in self.excluded_points[:, :, None]]
        )
        self.excluded_circles = np.hstack([self.excluded_circles, new_circles])

    def rotation_matrix(self, axis, cos_theta):
        """
        Generates a matrix which rotates a vector a given angle about a given axis.

        Parameters
        ----------
        axis: numpy.ndarray
            3x1 Numpy array representing the vector whose direction is the axis of rotation.
        cos_theta: float
            Cosine of angle of rotation about the axis of rotation.

        Returns
        -------
        numpy.ndarray:
            3x3 Numpy array representing the rotation matrix which rotates a vector by the given angle about the given axis.
        """
        if scipy.linalg.norm(axis) > 0:
            axis /= scipy.linalg.norm(axis)

        u1, u2, u3 = np.ravel(axis)

        K = np.array([[0, -u3, u2], [u3, 0, -u1], [-u2, u1, 0]])

        sin_theta = np.sqrt(1 - cos_theta ** 2)

        return np.eye(3) + sin_theta * K + (1 - cos_theta) * (K @ K)

    def rotation_matrix_m_to_n(self, m, n):
        """
        Generates a matrix which rotates one given vector to another.

        Parameters
        ----------
        m: numpy.ndarray
            3x1 Numpy array representing the vector to be rotated.
        n: numpy.ndarray
            3x1 Numpy array representing the vector after rotation, i.e. the target vector.

        Returns
        -------
        numpy.ndarray:
            3x3 Numpy array representing the rotation matrix which maps m to n.
        """
        # make rotation axis, which is perpendicular to both m and n
        # no need to normalize, since rotation_matrix will do that for us
        u = np.cross(m.T, n.T).T

        # cosine of the angle between m and n
        c = np.dot(m.T, n) / (scipy.linalg.norm(m) * scipy.linalg.norm(n))

        return self.rotation_matrix(axis=u, cos_theta=c)

    def perpendicular_vector(self, a, b=None):
        """
        Generates a unit vector which is perpendicular to one or two given nonzero vector(s).

        Parameters
        ----------
        a: numpy.ndarray
            3x1 Numpy array representing a nonzero vector.
        b: numpy.ndarray
            3x1 Numpy array representing a nonzero vector.

        Returns
        -------
        numpy.ndarray:
            3x1 Numpy array representing a unit vector which is perpendicular to a (and b, if applicable).
        """
        if b is None:
            m = np.zeros(a.shape)

            ravel_a = np.ravel(a)  # storing in variable for reuse

            i = (ravel_a != 0).argmax()  # index of the first nonzero element of a
            j = next(
                ind for ind in range(len(ravel_a)) if ind != i
            )  # first index of a which is not i
            i, j = (
                np.unravel_index(i, a.shape),
                np.unravel_index(j, a.shape),
            )  # unravel indices for 3x1 arrays m and a

            # make m = np.array([[-ay,ax,0]]).T so np.dot(m.T,a) = -ax*ay + ax*ay = 0
            m[j] = a[i]
            m[i] = -a[j]
        else:
            m = np.cross(a.T, b.T).T

        m /= scipy.linalg.norm(m)

        return m

    def make_nontrivial_vector(self, R):
        """
        Generates a vector which is acted upon nontrivially (i.e. is sent to a linearly independent vector) by the given rotation matrix.

        Parameters
        ----------
        R: numpy.ndarray
            3x3 numpy array representing a rotation matrix.

        Returns
        -------
        numpy.ndarray:
            3x1 numpy array representing a vector which is acted upon nontrivially by R.
        """
        # get the eigenvectors with real (i.e. 1 or -1) eigenvalues, since these are mapped to colinear vectors by R
        evals, evecs = scipy.linalg.eig(
            R
        )  # each column of evecs is an eigenvector of R

        real_eigenbasis = np.real(
            evecs.T[np.imag(evals) == 0].T
        )  # ???: why np.real(evec) instead of simply evec?

        # form the linear combination of the "trivial" eigenvectors
        # get random coefficients between 1 and 2 so that 0 is never chosen
        # the result is guaranteed to be mapped to a linearly independent vector
        # by R because the "trivial" eigenvectors do not all have the same eigenvalues #all have different eigenvalues
        # this is true because R is not proportional to the identity matrix
        coeffs = np.random.uniform(low=1, high=2, size=(real_eigenbasis.shape[1], 1))
        t = real_eigenbasis @ coeffs
        t /= scipy.linalg.norm(t)

        return t

    def sample_axis(self):
        self.points_to_circles()
        n1, n2 = self.closest_pair(points=self.excluded_circles)

        return self.sample_from_lune(n1=n1, n2=n2)

    def sample_from_lune(self, n1, n2):
        q = self.sample_from_standard_lune(dphi=np.arccos(np.dot(n1.T, n2)).item())

        l = self.perpendicular_vector(a=n1, b=n2)
        a = self.perpendicular_vector(a=n1, b=l)
        b = self.perpendicular_vector(a=n2, b=l)
        c = a if np.sign(np.dot(n1.T, b)) > 0 else b
        x = np.array([[1, 0, 0]]).T
        z = np.array([[0, 0, 1]]).T

        Ru = self.rotation_matrix_m_to_n(m=z, n=l)
        Rv = self.rotation_matrix_m_to_n(m=Ru @ x, n=c)

        return (Rv @ Ru) @ q

    def sample_from_standard_lune(self, dphi):
        eps = np.finfo(float).eps

        phi = np.random.uniform(low=eps, high=dphi)
        cos_theta = np.random.uniform(low=-1, high=1)
        sin_theta = np.sqrt(1 - cos_theta ** 2)

        q = np.array([[sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta]]).T

        return q

    def closest_pair(self, points):
        """
        Finds the two closest points from a given list of points.

        Parameters
        ----------
        points : numpy.ndarray
            3xNp Numpy array whose columns represent points on the unit sphere, where Np is the number of points.

        Returns
        -------
        numpy.ndarray:
            3x2 Numpy array whose columns are the two closest points from the given list of points.
        """

        return points.T[
            min(
                zip(*scipy.spatial.KDTree(points).query(points, k=2)),
                key=lambda t: t[0][1],
            )[1]
        ].T
