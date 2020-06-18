import itertools
import numpy as np
import scipy.linalg

import materia


def generate_axes(structure, symprec=5, seed=None):
    symmetries = tuple(
        R.matrix
        for R in materia.symmetry.GraphSymmetryFinder().symmetry_operations(
            structure=structure, symprec=symprec
        )
        if not (np.allclose(R.matrix, np.eye(3)) or np.allclose(R.matrix, np.eye(3)))
    )

    num_symmetries = len(symmetries)

    # FIXME: is there an easy way to check if R1 == -R2 when R1 and R2 are SymmetryOperation objects?
    excluded_generator = (
        (R1, R2, _excluded_circles(A=R1, B=R2))
        for R1, R2 in itertools.product(symmetries, symmetries)
        if (not np.allclose(R1, R2) and not np.allclose(R1, -R2))
    )  # R1 != R2)#
    try:
        R1, R2, excluded_circles = next(excluded_generator)
        intersections = np.hstack(
            [
                materia.utils.perpendicular_vector(a=n1, b=n2)
                for n1, n2 in itertools.combinations(
                    excluded_circles.T[:, :, None], r=2
                )
            ]
        )
        A, B, C = materia.utils.closest_trio(points=intersections).T[:, :, None]
        sin_alpha = scipy.linalg.norm(A)
        sin_beta = scipy.linalg.norm(B)
        sin_gamma = scipy.linalg.norm(C)
        # triangle vertices
        A /= sin_alpha
        B /= sin_beta
        C /= sin_gamma

        q = materia.utils.sample_spherical_triangle(
            A=A,
            B=B,
            C=C,
            sin_alpha=sin_alpha,
            sin_beta=sin_beta,
            sin_gamma=sin_gamma,
            seed=seed,
        )
        r = R1 @ q
        s = R2 @ q

        axes = np.hstack([q, r, s])
    except StopIteration:
        if num_symmetries > 0:
            R1 = symmetries[0]
            R2 = None

            q = materia.utils.make_nontrivial_vector(R=R1, seed=seed)
            r = R1 @ q
            s = materia.utils.perpendicular_vector(a=q, b=r)

            axes = np.hstack([q, r, s])
        else:
            R1 = R2 = None
            axes = np.eye(3)

    if _validate_axes(axes=axes):
        # FIXME: this wprime line is wrong - replace the conditional with something which can tell whether or not the three axes are all symmetry related
        # wprime = (A.T@axes[:,-1])[:,None] if wprime is not None else wprime
        return axes, R1, R2
    else:
        print("Error validating vectors!")
        return np.eye(3), None, None


def _excluded_circles(A, B):
    """
    Construct list of excluded circles on unit sphere.

    Parameters
    ----------
    A,B : numpy.ndarray
        3x3 Numpy arrays representating the two symmetry operations whose excluded circles are being calculated.

    Returns
    -------
    numpy.ndarray:
        3xNc Numpy array representing the normal vectors of excluded circles, where Nc is the number of excluded circles.
    """
    identity = np.eye(3)
    null_bases = [
        scipy.linalg.null_space(M)
        for M in (
            (A + identity, A - identity, B + identity, B - identity, A + B, A - B)
            if B is not None
            else (A + identity, A - identity)
        )
    ]

    # each null basis with geometric multiplicity two results in a circle of excluded points whose normal vector is the cross product of the null basis
    fixed_excluded_circles = [
        materia.utils.perpendicular_vector(*nb.T[:, :, None])
        for nb in null_bases
        if nb.shape[1] == 2
    ]
    # create additional circles which encompass all excluded points and which go through the selected intersection
    additional_excluded_circles = _extend_points_to_circles(
        _intersection(*fixed_excluded_circles),
        *(nb for nb in null_bases if nb.shape[1] == 1)
    )
    excluded_circles = materia.utils.linearly_independent(
        vectors=np.hstack(fixed_excluded_circles + additional_excluded_circles)
    )

    # if there are still fewer than three excluded circles, generate additional circles perpendicular to the previous circle(s)
    while excluded_circles.shape[1] < 3:
        excluded_circles = np.hstack(
            [
                excluded_circles,
                materia.utils.perpendicular_vector(*excluded_circles.T[:, :, None]),
            ]
        )

    assert excluded_circles.shape[1] < 4

    return excluded_circles


def _intersection(*normals):
    if (
        len(normals) > 1
    ):  # pick two fixed circles and choose their intersection axis as the intersection axis for subsequent circles (excepting the third fixed circle);  if there are two fixed circles, choose their intersection axis
        a, b, *_ = normals
        return materia.utils.perpendicular_vector(a=a, b=b)
    elif (
        len(normals) == 1
    ):  # if there is one fixed circle, choose a vector in the circle as the intersection axis for subsequent circles
        [a] = normals
        return materia.utils.perpendicular_vector(a=a)
    else:  # if there are no fixed circles, then choose the north pole
        return np.array([[0, 0, 1]]).T


def _extend_points_to_circles(intersection, *excluded_points):
    return [
        materia.utils.perpendicular_vector(a=p, b=intersection)
        for p in excluded_points
        if not np.allclose(p, intersection) and not np.allclose(p, -intersection)
    ]


def _validate_axes(axes):
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
