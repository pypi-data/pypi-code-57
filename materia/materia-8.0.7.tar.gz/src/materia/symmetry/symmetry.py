import itertools
import numpy as np
import scipy.linalg
import math

import materia

# SEE https://iopscience.iop.org/book/978-1-6817-4637-1/chapter/bk978-1-6817-4637-1ch1, https://math.stackexchange.com/questions/693414/reflection-across-the-plane, https://github.com/psi4/psi4/blob/master/psi4/src/psi4/libmints/molecule.cc, http://www.pci.tu-bs.de/aggericke/PC4e/Kap_IV/Matrix_Symm_Op.htm


class SymmetryAnalyzer:
    def symmetry_operations(self, molecule, symprec=5, graph=False):
        if graph:
            permutations = {
                hash(P.data.tobytes()): P
                for P in self._automorphism_iterator(molecule=molecule, symprec=symprec)
            }

            for P in permutations.values():
                permutations[hash(P.T.data.tobytes())] = P.T
            for P1, P2 in itertools.combinations(permutations.values(), r=2):
                P3 = P1 @ P2
                permutations[hash(P3.data.tobytes())] = P3
                permutations[hash(P3.T.data.tobytes())] = P3.T

            X = molecule.structure.centered_atomic_positions.value
            pinv_X = np.linalg.pinv(X)

            # FIXME: need to check that these rotations are actually symmetries before returning them!
            return tuple(
                SymmetryOp(matrix=scipy.linalg.polar(X @ P @ pinv_X)[0])
                for P in permutations.values()
            )
        else:
            I = molecule.structure.inertia_tensor / np.trace(
                molecule.structure.inertia_tensor
            )
            principal_moments, principal_axes = scipy.linalg.eig(I)
            (m1, m2, m3) = principal_moments.round(symprec)

            symmetry_operations = []

            for p1, p2 in itertools.combinations(
                molecule.structure.centered_atomic_positions.value.T, r=2
            ):
                axis = p1 - p2
                axis /= scipy.linalg.norm(axis)

                R = Reflection(axis=axis)

                if R.is_symmetry_of(molecule, symprec=symprec):
                    symmetry_operations.append(R)
                print(len(symmetry_operations))
                axis = p1 + p2
                axis_norm = scipy.linalg.norm(axis)
                if not np.isclose(axis_norm, 0):
                    axis /= axis_norm
                    R2 = ProperRotation(order=2, axis=axis)
                    R3 = ProperRotation(order=2, axis=axis)
                    R4 = ProperRotation(order=2, axis=axis)
                    R5 = ProperRotation(order=2, axis=axis)

                    if R2.is_symmetry_of(molecule, symprec=symprec):
                        symmetry_operations.append(R2)
                    if R3.is_symmetry_of(molecule, symprec=symprec):
                        symmetry_operations.append(R3)
                    if R4.is_symmetry_of(molecule, symprec=symprec):
                        symmetry_operations.append(R4)
                    if R5.is_symmetry_of(molecule, symprec=symprec):
                        symmetry_operations.append(R5)

                print(len(symmetry_operations))
            print(len({hash(R.matrix.data.tobytes()): R for R in symmetry_operations}))
            if np.isclose(np.prod((m1, m2, m3)), 0):  # one of the eigenvalues is zero
                return self._analyze_linear_molecule(molecule=molecule)
            elif np.allclose((m1 - m2, m2 - m3), 0):  # all eigenvalues are the same
                return self._analyze_spherical_top(molecule=molecule)
            elif (
                np.sum(np.isclose((m1 - m2, m2 - m3, m1 - m3), 0)) == 0
            ):  # all eigenvalues are different
                # possible groups: C1, Ci, Cs, C2, C2v, C2h, D2, D2h
                for axis in principal_axes.T:
                    R = ProperRotation(order=2, axis=axis)
                    if R.is_symmetry_of(molecule=molecule, symprec=symprec):
                        symmetry_operations.append(R)
                if len(symmetry_operations) == 0:
                    # possible groups: C1, Ci, Cs
                    inv = Inversion()
                    if inv.is_symmetry_of(molecule=molecule, symprec=symprec):
                        # Ci
                        symmetry_operations.append(inv)
                    # elif Reflection(axis=)# check for mirror plane
                elif len(symmetry_operations) == 1:
                    # possible groups: C2, C2v, C2h
                    pass
                else:
                    # possible groups: D2, D2h
                    pass
                print(symmetry_operations)
                return self._analyze_asymmetrical_top(molecule=molecule)
            else:  # two eigenvalues are the same, one is different
                return self._analyze_symmetrical_top(molecule=molecule)

    def _analyze_linear_molecule(self, molecule):
        inv = Inversion()
        if inv.is_symmetry_of(molecule):
            pass  # FIXME: what to return for infinite point group Dinfh?
        else:
            pass  # FIXME: what to return for infinite point group Cinfv?

    # def asymmetrical_top(self, molecule):
    #     for

    def _automorphism_iterator(self, molecule, symprec):
        import networkx as nx

        num_atoms = len(molecule.structure.atoms)

        g = nx.Graph()

        nodes = tuple(
            range(num_atoms + 1)
        )  # node with label num_atoms represents COM node
        edges = tuple(
            (num_atoms, i) for i in nodes[:-1]
        )  # make edge between COM node and every non-COM node

        atomic_symbols = (
            *molecule.structure.atomic_symbols,
            "COM",
        )  # 'COM' is the "atomic symbol" for the COM node
        com_distances = (
            np.linalg.norm(p).round(symprec)
            for p in molecule.structure.centered_atomic_positions.value.T
        )

        g.add_edges_from(edges)
        nx.set_node_attributes(
            G=g, values={n: {"Z": v} for n, v in zip(nodes, atomic_symbols)}
        )
        nx.set_edge_attributes(
            G=g, values={e: {"dist": v} for e, v in zip(edges, com_distances)}
        )

        permutation_iterator = nx.algorithms.isomorphism.GraphMatcher(
            G1=g,
            G2=g,
            node_match=lambda n1, n2: n1["Z"] == n2["Z"],
            edge_match=lambda e1, e2: e1["dist"] == e2["dist"],
        ).isomorphisms_iter()

        yield from (
            self._permutation_matrix(permutation_dict=perm)
            for perm in permutation_iterator
        )

    def _permutation_matrix(self, permutation_dict):
        n = len(permutation_dict) - 1  # number of atoms
        permutation_dict.pop(n)  # remove the COM

        I = np.eye(n, dtype=int)
        return np.hstack(
            [
                I[:, col_ind].reshape(n, -1)
                for _, col_ind in sorted(permutation_dict.items())
            ]
        )


class PointGroup:
    def __init__(self, reps):
        self.reps = tuple(np.atleast_1d(r) for r in reps)

    def cayley_table(self, reps):
        labels = {k: i for i, k in enumerate(reps)}
        num_reps = len(labels)
        ctable = np.zeros(shape=(num_reps, num_reps), dtype=int)

        for P, Q in itertools.combinations(reps.values(), r=2):
            c = np.atleast_1d(P @ Q)
            i = labels[hash(P.data.tobytes())]
            j = labels[hash(Q.data.tobytes())]
            ctable[i, j] = ctable[j, i] = labels[hash(c.data.tobytes())]

        rowset = set(tuple(r) for r in ctable)
        colset = set(tuple(c) for c in ctable.T)

        return ctable


class SymmetryOp:
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
        u = self._perpendicular_vector(p=axis)
        axis *= np.sign(np.dot(axis, np.cross(u, self.matrix @ u)))

        return axis

    def _perpendicular_vector(self, p):
        m = np.zeros(p.shape)

        i = (np.ravel(p) != 0).argmax()  # index of the first nonzero element of p
        j = next(
            ind for ind in range(len(np.ravel(p))) if ind != i
        )  # first index of p which is not i
        i, j = (
            np.unravel_index(i, p.shape),
            np.unravel_index(j, p.shape),
        )  # unravel indices for 1x3 arrays m and p

        # make m = np.array([[-py,px,0]]) so np.dot(m,p) = -px*py + px*py = 0
        m[j] = p[i]
        m[i] = -p[j]
        m /= scipy.linalg.norm(m)

        return np.array(m)

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


class Inversion(SymmetryOp):
    def __init__(self):
        determinant = -1
        trace = -3
        axis = None
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class Reflection(SymmetryOp):
    def __init__(self, axis):
        determinant = -1
        trace = 1
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class ProperRotation(SymmetryOp):
    def __init__(self, order, axis):
        determinant = 1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class ImproperRotation(SymmetryOp):
    def __init__(self, order, axis):
        determinant = -1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)


# class SigmaX(SymmetryOp):
#     def __init__(self):
#         super().__init__(matrix=np.array([[-1,0,0],[0,1,0],[0,0,1]]))
#
# class SigmaY(SymmetryOp):
#     def __init__(self):
#         super().__init__(matrix=np.array([[1,0,0],[0,-1,0],[0,0,1]]))
#
# class SigmaZ(SymmetryOp):
#     def __init__(self):
#         super().__init__(matrix=np.array([[1,0,0],[0,1,0],[0,0,-1]]))
#
# class Inversion(SymmetryOp):
#     def __init__(self):
#         super().__init__(matrix=np.array([[-1,0,0],[0,-1,0],[0,0,-1]]))
#         self.periodicity = 2
#
# class Sigma(SymmetryOp):
#     def __init__(self, axis):
#         matrix = np.eye(3) - 2*np.outer(axis,axis)
#         super().__init__(matrix=matrix)
#         self.periodicity = 2
#
# class CnU(SymmetryOp):
#     def __init__(self, n, axis):
#         u1,u2,u3 = np.asarray(axis).reshape(3,)
#
#         K = np.array([[0,-u3,u2],[u3,0,-u1],[-u2,u1,0]])
#
#         angle = 2*np.pi/n
#
#         matrix = (np.eye(3) + np.sin(angle)*K + (1-np.cos(angle))*(K @ K)).astype('float64')
#
#         super().__init__(matrix=matrix)
#         self.periodicity = n
#
# class C2X(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[1,0,0],[0,np.cos(np.pi),np.sin(np.pi)],[0,-np.sin(np.pi),np.cos(np.pi)]])
#
# class C2Y(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi),0,np.sin(np.pi)],[0,1,0],[-np.sin(np.pi),0,np.cos(np.pi)]])
#
# class C2Z(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi),np.sin(np.pi),0],[-np.sin(np.pi),np.cos(np.pi),0],[0,0,1]])
#
# class C3X(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[1,0,0],[0,np.cos(2*np.pi/3),np.sin(2*np.pi/3)],[0,-np.sin(2*np.pi/3),np.cos(2*np.pi/3)]])
#
# class C3Y(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(2*np.pi/3),0,np.sin(2*np.pi/3)],[0,1,0],[-np.sin(2*np.pi/3),0,np.cos(2*2*np.pi/3/3)]])
#
# class C3Z(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(2*np.pi/3),np.sin(2*np.pi/3),0],[-np.sin(2*np.pi/3),np.cos(2*np.pi/3),0],[0,0,1]])
#
# class C4X(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[1,0,0],[0,np.cos(np.pi/2),np.sin(np.pi/2)],[0,-np.sin(np.pi/2),np.cos(np.pi/2)]])
#
# class C4Y(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],[0,1,0],[-np.sin(np.pi/2),0,np.cos(np.pi/2)]])
#
# class C4Z(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi/2),np.sin(np.pi/2),0],[-np.sin(np.pi/2),np.cos(np.pi/2),0],[0,0,1]])
#
# class C5X(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[1,0,0],[0,np.cos(2*np.pi/5),np.sin(2*np.pi/5)],[0,-np.sin(2*np.pi/5),np.cos(2*np.pi/5)]])
#
# class C5Y(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(2*np.pi/5),0,np.sin(2*np.pi/5)],[0,1,0],[-np.sin(2*np.pi/5),0,np.cos(2*np.pi/5)]])
#
# class C5Z(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(2*np.pi/5),np.sin(2*np.pi/5),0],[-np.sin(2*np.pi/5),np.cos(2*np.pi/5),0],[0,0,1]])
#
# class C6X(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[1,0,0],[0,np.cos(np.pi/3),np.sin(np.pi/3)],[0,-np.sin(np.pi/3),np.cos(np.pi/3)]])
#
# class C6Y(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi/3),0,np.sin(np.pi/3)],[0,1,0],[-np.sin(np.pi/3),0,np.cos(np.pi/3)]])
#
# class C6Z(SymmetryOp):
#     def __init__(self):
#         self.matrix = np.array([[np.cos(np.pi/3),np.sin(np.pi/3),0],[-np.sin(np.pi/3),np.cos(np.pi/3),0],[0,0,1]])


def _equivalent_atoms(molecule):
    mol_dict = {
        tuple(p.squeeze()): symb
        for symb, p in zip(
            molecule.structure.atomic_symbols,
            molecule.structure.centered_atomic_positions.value.T,
        )
    }
    elements = tuple(set(mol_dict.values()))

    yield from (
        [position for position, element in mol_dict.items() if element == el]
        for el in elements
    )


def _candidate_symmetry_axes(molecule):
    centroid_lines = (
        np.asarray(position1) + np.asarray(position2)
        for position1, position2 in itertools.chain(
            *(
                itertools.combinations(isoelemental_group, r=2)
                for isoelemental_group in _equivalent_atoms(molecule=molecule)
            )
        )
    )

    return tuple(
        tuple(l / np.linalg.norm(l))
        for l in itertools.chain(
            molecule.structure.centered_atomic_positions.value.T, centroid_lines
        )
    )


def find_symmetry(mol):
    # FIXME: first align principal axes, center on COM
    possible_lines_of_symmetry = _candidate_symmetry_axes(molecule=mol)
    if mol.structure.is_linear:
        if Inversion().is_symmetry_of(mol=mol):
            print("D-infh")
        else:
            print("C-infv")
    # print([CnU(n=6,axis=line).is_symmetry_of(mol=mol) for line in mol.structure.atomic_lines])
    # print([CnU(n=5,axis=line).is_symmetry_of(mol=mol) for line in mol.structure.atomic_lines])
    # print([CnU(n=4,axis=line).is_symmetry_of(mol=mol) for line in mol.structure.atomic_lines])
    # print([CnU(n=3,axis=line).is_symmetry_of(mol=mol) for line in mol.structure.atomic_lines])
    # print([CnU(n=2,axis=line).is_symmetry_of(mol=mol) for line in mol.structure.atomic_lines])
    if (
        sum(
            CnU(n=5, axis=line).is_symmetry_of(molecule=mol)
            for line in possible_lines_of_symmetry
        )
        >= 2
    ):
        if mol.has_symmetry(symmetry_op=Inversion()):
            print("Ih")
        else:
            print("I")
    if (
        sum(
            CnU(n=4, axis=line).is_symmetry_of(molecule=mol)
            for line in possible_lines_of_symmetry
        )
        >= 2
    ):
        if mol.has_symmetry(symmetry_op=Inversion()):
            print("Oh")
        else:
            print("O")
    if (
        sum(
            CnU(n=3, axis=line).is_symmetry_of(molecule=mol)
            for line in possible_lines_of_symmetry
        )
        == 4
    ):
        if (
            sum(
                mol.has_symmetry(symmetry_op=Sigma(axis=plane_normal))
                for plane_normal in mol.atom_planes
            )
            >= 1
        ):
            if mol.has_symmetry(symmetry_op=Inversion()):
                print("Th")
            else:
                print("Td")
        else:
            print("T")
    print(
        [
            CnU(n=2, axis=line).is_symmetry_of(molecule=mol)
            for line in possible_lines_of_symmetry
        ]
    )
    print(possible_lines_of_symmetry)
    has_cs = [
        sum(
            CnU(n=n, axis=line).is_symmetry_of(molecule=mol)
            for line in possible_lines_of_symmetry
        )
        for n in (2, 3, 4, 5, 6)
    ]
    if sum(has_cs) == 0:
        if (
            sum(
                mol.has_symmetry(symmetry_op=Sigma(axis=plane_normal))
                for plane_normal in mol.atom_planes
            )
            >= 1
        ):
            print("Cs")
        else:
            if mol.has_symmetry(symmetry_op=Inversion()):
                print("Ci")
            else:
                print("C1")
    else:
        max_n = 6 - np.argmax(has_cs[::-1])
        if max_n <= 1:
            pass
