import numpy as np
import scipy.linalg

import materia


class SymmetryOperation:
    def __init__(self, matrix=None, determinant=None, trace=None, axis=None):
        if matrix is not None:
            self.matrix, _ = scipy.linalg.polar(matrix)
        else:
            if axis is None:
                self.matrix, _ = scipy.linalg.polar(
                    determinant * np.eye(3).astype("float64")
                )
            else:
                cos_theta = max(min((trace - determinant) / 2, 1), -1)
                sin_theta = max(min(np.sqrt(1 - cos_theta ** 2), 1), -1)

                u1, u2, u3 = axis
                K = np.array([[0, -u3, u2], [u3, 0, -u1], [-u2, u1, 0]])

                rotation = (
                    np.eye(3) + sin_theta * K + (1 - cos_theta) * (K @ K)
                ).astype("float64")
                reflection = np.eye(3) - (determinant == -1) * 2 * np.outer(axis, axis)

                self.matrix, _ = scipy.linalg.polar(rotation @ reflection)

    def __eq__(self, other):
        return hasattr(other, "matrix") and np.allclose(self.matrix, other.matrix)

    @property
    def det(self):
        return int(round(np.linalg.det(self.matrix)))

    @property
    def tr(self):
        return np.trace(self.matrix)

    @property
    def cos_theta(self):
        return max(min((self.tr - np.sign(self.det)) / 2, 1), -1)

    @property
    def axis(self):
        if np.isclose(abs(self.tr), 3):
            return None

        S = self.matrix + self.matrix.T - (self.tr - np.sign(self.det)) * np.eye(3)
        S[np.isclose(S, 0)] = 0

        axis = np.sqrt(
            np.abs(np.diag(S) / (3 - np.sign(self.det) * self.tr))
        )  # scipy.linalg.null_space(R-det*np.eye(3)).squeeze()
        u = materia.Geometry()._perpendicular_vector(p=axis)
        axis *= np.sign(np.dot(axis, np.cross(u, self.matrix @ u)))

        return axis

    def is_symmetry_of(self, structure, symprec):
        transformed_atomic_positions = (
            self.matrix @ structure.centered_atomic_positions.value
        )
        return set(
            tuple(row) for row in transformed_atomic_positions.T.round(symprec)
        ) == set(
            tuple(row)
            for row in structure.centered_atomic_positions.value.T.round(symprec)
        )


class Inversion(SymmetryOperation):
    def __init__(self):
        determinant = -1
        trace = -3
        axis = None
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class Reflection(SymmetryOperation):
    def __init__(self, axis):
        determinant = -1
        trace = 1
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class ProperRotation(SymmetryOperation):
    def __init__(self, order, axis):
        determinant = 1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class ImproperRotation(SymmetryOperation):
    def __init__(self, order, axis):
        determinant = -1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)
