import collections
import itertools
import numpy as np
import scipy.linalg

import materia.symmetry
import materia.utils


def fragment_seas(structure):
    return {
        Z: materia.Structure(atoms=atoms)
        for Z, atoms in itertools.groupby(
            sorted(structure.atoms, key=lambda a: a.Z), lambda a: a.Z
        )
    }


import functools


def factors(n):
    return set(
        functools.reduce(
            list.__add__,
            ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0),
        )
    )


def symmetry_operations(structure, symprec):
    seas = fragment_seas(structure=structure).values()
    candidate_operations = find_operations(structure=seas, symprec=symprec) + [
        materia.symmetry.Inversion()
    ]


def find_operations(structure, symprec):
    if structure.is_linear:
        return _find_rotations_linear(structure=structure, symprec=symprec)
    elif structure.is_planar:
        normal = structure.principal_axes[np.argmax(structure.principal_moments)]
        overall_reflection = materia.symmetry.Reflection(axis=normal)

        rotations = [
            _find_rotations_planar(structure=sea, symprec=symprec) for sea in seas
        ]
        reflections = [
            _find_reflections_planar(structure=structure, symprec=symprec)
            for sea in seas
        ]
        # FIXME: improper? no need for inversion
        return rotations + reflections + [overall_reflection]
    else:
        # FIXME: write this
        return None


def _find_rotations_planar(structure, symprec):
    divisors = factors(n=structure.num_atoms)
    rs = []
    m1, m2, m3 = structure.principal_moments
    if m1 == m2:
        normal = structure.principal_axes[2]
    elif m1 == m3:
        normal = structure.principal_axes[1]
    else:  # m2 == m3
        normal = structure.principal_axes[0]
    for p1, p2 in itertools.combinations(
        structure.centered_atomic_positions.value.T, r=2
    ):
        Rs = (
            materia.symmetry.ProperRotation(
                order=d, axis=materia.utils.normalize(p1 + p2)
            )
            for d in divisors
        )
        rs.extend(
            [R for R in Rs if R.is_symmetry_of(structure=structure, symprec=symprec)]
        )
        Rs = (materia.symmetry.ProperRotation(order=d, axis=normal) for d in divisors)
        rs.extend(
            [R for R in Rs if R.is_symmetry_of(structure=structure, symprec=symprec)]
        )

    return rs


# FIXME: resume editing here
# def _find_reflections_planar(structure, symprec):
#     return materia.symmetry.Reflection(axis=materia.utils.normalize(p1 - p2)) for p1,p2 in itertools.combinations(structure.centered_atomic_positions.value.T,r=2)

# (m1,m2,m3) = self.principal_moments.value/sum(self.principal_moments.value)
# if (m1 == m2 != m3) or (m1 == m3 != m2) or (m2 == m3 != m1): # oblate symmetric top, regular polygon


# class SEA:
#     def __init__(self, structure):
#         self.structure = structure
#
# def principal_axes_R2(structure, symprec):
#     I = structure.inertia_tensor/np.trace(structure.inertia_tensor)
#     principal_moments,principal_axes = scipy.linalg.eigh(I)
#     operators = (materia.symmetry.ProperRotation(order=2,axis=axis) for axis in principal_axes)
#
#     return tuple(R for R in operators if R.is_symmetry_of(structure=structure,symprec=symprec))

# SEARCHING FOR PLANES
# a mirror plane must map every atom to an atom of the same element
# if a mirror plane goes through no atoms, then it must map every atom to a different atom, so its normal is the difference of two isoelemental atoms
# if a mirror plane goes through at least one atom but not all atoms of any element, then it must map every other atom to a different atom, so its normal is the difference of two isoelemental atoms
# if a mirror plane goes through all atoms of an element, then it must map all atoms of that element to themselves, and the plane is simply the plane of those atoms
# so all mirror planes can be found by listing all mirror planes separating isoelemental atoms and all mirror planes containing all atoms of an element
# SEARCHING FOR PROPER ROTATION AXES
# a rotation axis must map every atom to an atom of the same element
# if a rotation axis goes through no atoms, then it must be at the center of n atoms where n is the order of the axis
# if these n atoms are coplanar, then the rotation axis is the normal to the plane
# otherwise, the rotation axis is the centroid of the n atoms
# if a rotation axis goes through at least one atom, then the axis is the vector from the COM to that atom
# so all rotation axes can be found by checking all atomic position vectors and the centroid/plane normal of all sets of n isoelemental atoms
# SEARCHING FOR IMPROPER ROTATION AXES
# SEARCHING FOR INVERSION
# if inversion symmetry exists, then the center of mass is the center of inversion
# for _,equivalent_atoms in itertools.groupby(sorted(structure.atoms,key=lambda a: a.Z),lambda a: a.Z):
#     for a1,a2 in itertools.combinations(equivalent_atoms,r=2):
#         materia.symmetry.Reflection(axis=materia.utils.normalize(a1 - p2)))
# def run(structure,symprec):
#     rs = []
#     for (z1,p1),(z2,p2) in itertools.combinations(zip(structure.atomic_numbers,structure.centered_atomic_positions.value.T),r=2):
#         if z1 == z2:
#             R = materia.symmetry.Reflection(axis=materia.utils.normalize(p1 - p2))
#             if R.is_symmetry_of(structure,symprec):
#                 rs.append(R)
#             R = materia.symmetry.ProperRotation(order=2,axis=materia.utils.normalize(p1 + p2))
#             if R.is_symmetry_of(structure,symprec):
#                 rs.append(R)
#             R = materia.symmetry.ProperRotation(order=2,axis=materia.utils.normalize(p1 - p2))
#             if R.is_symmetry_of(structure,symprec):
#                 rs.append(R)
#             R = materia.symmetry.ProperRotation(order=2,axis=materia.utils.normalize(np.cross(p1.T,p2.T)))
#             if R.is_symmetry_of(structure,symprec):
#                 rs.append(R)
#             R = materia.symmetry.Reflection(axis=materia.utils.normalize(np.cross(p1.T,p2.T)))
#             if R.is_symmetry_of(structure,symprec):
#                 rs.append(R)
#     return rs
#
# class ExplicitSymmetryFinder:
#     def symmetry_operations(self, structure, symprec=5):
#         I = structure.inertia_tensor/np.trace(structure.inertia_tensor)
#         principal_moments,principal_axes = scipy.linalg.eigh(I)
#         (m1,m2,m3) = principal_moments.round(symprec)
#
#         symmetry_operations = []
#
#         for p1,p2 in itertools.combinations(structure.centered_atomic_positions.value.T,r=2):
#             R = materia.symmetry.Reflection(axis=materia.utils.normalize(p1 - p2))
#
#             if R.is_symmetry_of(structure=structure,symprec=symprec):
#                 symmetry_operations.append(R)
#
#             axis = materia.utils.normalize(p1 + p2)
#             # axis_norm = scipy.linalg.norm(axis)
#             # if not np.isclose(axis_norm,0):
#             #     axis /= axis_norm
#             R2 = ProperRotation(order=2,axis=axis)
#             R3 = ProperRotation(order=2,axis=axis)
#             R4 = ProperRotation(order=2,axis=axis)
#             R5 = ProperRotation(order=2,axis=axis)
#
#             if R2.is_symmetry_of(molecule,symprec=symprec):
#                 symmetry_operations.append(R2)
#             if R3.is_symmetry_of(molecule,symprec=symprec):
#                 symmetry_operations.append(R3)
#             if R4.is_symmetry_of(molecule,symprec=symprec):
#                 symmetry_operations.append(R4)
#             if R5.is_symmetry_of(molecule,symprec=symprec):
#                 symmetry_operations.append(R5)
#
#             print(len(symmetry_operations))
#         print(len({hash(R.matrix.data.tobytes()):R for R in symmetry_operations}))
#         if np.isclose(np.prod((m1,m2,m3)),0): # one of the eigenvalues is zero
#             return self._analyze_linear_molecule(molecule=molecule)
#         elif np.allclose((m1-m2,m2-m3),0): # all eigenvalues are the same
#             return self._analyze_spherical_top(molecule=molecule)
#         elif np.sum(np.isclose((m1-m2,m2-m3,m1-m3),0)) == 0: # all eigenvalues are different
#             # possible groups: C1, Ci, Cs, C2, C2v, C2h, D2, D2h
#             for axis in principal_axes.T:
#                 R = materia.symmetry.ProperRotation(order=2,axis=axis)
#                 if R.is_symmetry_of(structure=structure,symprec=symprec):
#                     symmetry_operations.append(R)
#             if len(symmetry_operations) == 0:
#                 # possible groups: C1, Ci, Cs
#                 inv = materia.symmetry.Inversion()
#                 if inv.is_symmetry_of(structure=structure,symprec=symprec):
#                     # Ci
#                     symmetry_operations.append(inv)
#                     print('Ci')
#                 elif any(Reflection(axis=axis).is_symmetry_of(structure=structure,symprec=symprec) for axis in principal_axes):# check for mirror plane
#                     print('Cs')
#                 else:
#                     print('C1')
#             elif len(symmetry_operations) == 1:
#                 # possible groups: C2, C2v, C2h
#                 pass
#             else:
#                 # possible groups: D2, D2h
#                 pass
#             print(symmetry_operations)
#             return self._analyze_asymmetrical_top(molecule=molecule)
#         else: # two eigenvalues are the same, one is different
#             return self._analyze_symmetrical_top(molecule=molecule)
#
#     # def asymmetrical_top(self, molecule):
#     #     for
#
#     def _analyze_linear_molecule(self, molecule):
#         inv = Inversion()
#         if inv.is_symmetry_of(molecule):
#             pass #FIXME: what to return for infinite point group Dinfh?
#         else:
#             pass #FIXME: what to return for infinite point group Cinfv?


class GraphSymmetryFinder:
    def symmetry_operations(self, structure, symprec=5):
        permutations = {
            hash(P.data.tobytes()): P
            for P in self._automorphism_iterator(structure=structure, symprec=symprec)
        }

        for P in permutations.values():
            permutations[hash(P.T.data.tobytes())] = P.T
        for P1, P2 in itertools.combinations(permutations.values(), r=2):
            P3 = P1 @ P2
            permutations[hash(P3.data.tobytes())] = P3
            permutations[hash(P3.T.data.tobytes())] = P3.T

        X = structure.centered_atomic_positions.value
        pinv_X = np.linalg.pinv(X)

        # FIXME: need to check that these rotations are actually symmetries before returning them!
        return tuple(
            materia.symmetry.SymmetryOperation(
                matrix=scipy.linalg.polar(X @ P @ pinv_X)[0]
            )
            for P in permutations.values()
        )

    def _automorphism_iterator(self, structure, symprec):
        import networkx as nx

        num_atoms = len(structure.atoms)

        g = nx.Graph()

        nodes = tuple(
            range(structure.num_atoms + 1)
        )  # node with label num_atoms represents COM node
        edges = tuple(
            (structure.num_atoms, i) for i in nodes[:-1]
        )  # make edge between COM node and every non-COM node

        atomic_symbols = (
            *structure.atomic_symbols,
            "COM",
        )  # 'COM' is the "atomic symbol" for the COM node
        com_distances = (
            np.linalg.norm(p).round(symprec)
            for p in structure.centered_atomic_positions.value.T
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


class SpglibSymmetryFinder:
    def symmetry_operations(self, molecule, symprec=1e-5):
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
        import spglib

        pointgroup_symbol = self.molecular_pointgroup(
            molecule=molecule, symprec=symprec
        )
        alignment_matrix = self._align_rotations_with_molecule(
            inertia_tensor=molecule.structure.inertia_tensor
        )
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
        # evidently spglib sometimes gives rotations which are not orthogonal matrices, so we need to exclude those
        proper_rotations = tuple(
            R @ alignment_matrix
            for R, det in zip(unique_rotations, determinants)
            if det == 1 and (R @ R.T == np.eye(3)).all() and not (R == np.eye(3)).all()
        )
        improper_rotations = tuple(
            R @ alignment_matrix
            for R, det in zip(unique_rotations, determinants)
            if det == -1
            and (R @ R.T == np.eye(3)).all()
            and not (R == -np.eye(3)).all()
        )

        # return proper_rotations,improper_rotations
        return tuple(
            R @ alignment_matrix
            for R in unique_rotations
            if (R @ R.T == np.eye(3)).all()
        )

    def molecular_pointgroup(self, molecule, symprec=1e-5):
        import spglib

        coordinates = molecule.structure.atomic_positions.value
        atomic_numbers = molecule.structure.atomic_numbers
        min_x, min_y, min_z = (min(p) for p in coordinates)
        # the 0.1 ensures that the fractional positions are sufficiently smaller than 1,
        # which appears to be necessary for accurate symmetry determination, and it
        # also ensures that max_x,max_y,max_z are all > 0 so that scipy.linalg.inv(lattice)
        # is well-defined
        max_x, max_y, max_z = [
            max(abs(p) - min) + 0.1
            for p, min in zip(coordinates, (min_x, min_y, min_z))
        ]

        lattice = np.diag([max_x, max_y, max_z])
        fractional_positions = coordinates.T @ scipy.linalg.inv(lattice)

        cell = (lattice, fractional_positions, atomic_numbers)

        return spglib.get_spacegroup_type(
            spglib.get_symmetry_dataset(cell=cell, symprec=symprec)["hall_number"]
        )["pointgroup_schoenflies"]

    # def get_rotations(self, pointgroup_symbol):
    #     """
    #     Generates two lists of rotations, one proper and one improper, which are symmetries corresponding to the given point group symbol.
    #
    #     Parameters
    #     ----------
    #     pointgroup_symbol: str
    #         String denoting a Schoenflies point group symbol.
    #
    #     Returns
    #     -------
    #     list of numpy.ndarrays:
    #         List of unique proper rotation matrices corresponding to pointgroup_symbol, excluding the identity matrix.
    #     list of numpy.ndarrays:
    #         List of unique improper rotation matrices corresponding to pointgroup_symbol, excluding the negative identity matrix.
    #     """
    #     representative_numbers = {spglib.get_spacegroup_type(i)['pointgroup_international']: i for i in range(1,531)}
    #     hall_number = representative_numbers[pointgroup_symbol] # lowest Hall number of a space group which contains the given point group.
    #     #hall_number = self.get_representative_hall_number(pointgroup_symbol=pointgroup_symbol) # lowest Hall number of a space group which contains the given point group.
    #
    #     #symmetry_dict = spglib.get_symmetry_from_database(hall_number)
    #     #rotations = symmetry_dict['rotations'][(symmetry_dict['translations'] == 0).sum(axis=1) == 3]
    #     rotations = spglib.get_symmetry_from_database(hall_number)['rotations']
    #     _,unique_indices = np.unique(ar=rotations,axis=0,return_index=True)
    #     unique_rotations = rotations[sorted(unique_indices)]
    #
    #     # exact (as opposed to np.isclose) conditions on determinant and identity-ness are fine since spglib gives rotation matrices with integer elements
    #     determinants = np.linalg.det(unique_rotations)
    #     # evidently spglib sometimes gives rotations which are not orthogonal matrices, so we need to exclude those
    #     proper_rotations = tuple(R@self.alignment_matrix for R,det in zip(unique_rotations,determinants) if det == 1 and (R@R.T == np.eye(3)).all() and not (R == np.eye(3)).all())
    #     improper_rotations = tuple(R@self.alignment_matrix for R,det in zip(unique_rotations,determinants) if det == -1 and (R@R.T == np.eye(3)).all() and not (R == -np.eye(3)).all())
    #
    #     return proper_rotations,improper_rotations

    def _align_rotations_with_molecule(self, inertia_tensor):
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

        if (
            principal_moments == np.array([0, 0, 0])
        ).all():  # i.e. this is an atomic species
            return np.eye(3)

        sorted_moments, sorted_directions = zip(
            *sorted(zip(principal_moments, principal_directions.T), reverse=True)
        )
        u, v, _ = sorted_directions

        Ru = materia.utils.rotation_matrix_m_to_n(m=u, n=np.array([[0, 0, 1]]).T)
        Rv = materia.utils.rotation_matrix_m_to_n(m=Ru @ v, n=np.array([[0, 1, 0]]).T)
        R = Rv @ Ru

        return R
