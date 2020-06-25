#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of the correction scheme for charged point defects
of Kumagai and Oba:

    Y. Kumagai and F. Oba, PRB 89, 195205 (2014)
"""
from copy import copy
import numpy as np
from scipy.spatial.distance import cdist
from spinney.structures.wigner_seitz import WignerSeitzCell
from spinney.defects.madelung import Ewald

def kumagai_sampling_region(cell, atom_coordinates, defect_position):
    """ Given the scaled coordinates of atoms in the supercell,
    returns the indices of the atoms belonging to the sampling region
    as defined in: Y. Kumagai and F. Oba, PRB 89, 195205 (2014)

    Parameters
    ----------
    cell : 2D numpy array
        each row represents the Cartesian coordinates of the primitive
        vectors

    atom_coordinates: 2D numpy array
        each row represents the fractional coordinates of the atoms in the
        supercell

    defect_position : 1D numpa array
        the scaled coordinates of the defect atom in the supercell.
        It will be used to center the supercell

    Returns
    -------
    in_region, sphere_radius : tuple
        :data:`in_region` is a list with the indexes of the atoms
        in the sampling region.

        :data:`sphere_radius` is a float and it is the radius of the
        sphere inscribed in the Wigner-Seitz cell.
    """
    patom_coordinates = atom_coordinates.copy()
    N_0 = len(patom_coordinates)
    patom_coordinates %= 1
    images = {}
    extended_coords = patom_coordinates.copy()
    # extend with PBC
    for i, coord in enumerate(patom_coordinates):
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    new_coord = coord + np.array([x, y, z])
                    extended_coords = np.vstack((extended_coords,
                                                 new_coord))
                    N = len(extended_coords) - 1
                    images[N] = i
    # put the defective atom at the origin of the cell
    # which will be the origin of the wigner-Seitz cell
    extended_coords -= defect_position
    wsc = WignerSeitzCell(cell)
    in_region = []

    sphere_radius = np.min(wsc.face_distances)
    for i, atom in enumerate(extended_coords):
        distance = np.dot(atom, cell)
        distance = np.linalg.norm(distance)
        if (wsc.is_in_cell(atom)) and (distance >= sphere_radius):
            if i >= N_0:
                if images[i] not in in_region:
                    in_region.append(images[i])
            else:
                if i not in in_region:
                    in_region.append(i)
    return in_region, sphere_radius

def map_atoms_pristine_defect(cell, scaled_pos_prist, scaled_pos_defect,
                             dist_tol=0.01):
    """
    Return a mapping between the indexes of the atoms in the pristine
    supercell and those of the atoms in the defective supercell.
    Both supercells have to be the same.

    Parameters
    ----------
    cell : 2D numpy array
        the supercell

    scaled_pos_prist : 2D numpy array
        fractional atomic positions of the pristine system

    scaled_pos_defect : 2D numpy array
        fractional positions of the defective system

        .. warning::

            It is assumed that both pristine and defective system
            have the same cell: :data:`cell`

    dist_tol : float/array of 3 elements
        tolerance value for which 2 distances are considered equal.
        If float, the value will be used to create an array with 3
        elements. Each elements represent the tolerance along the
        corresponding cell parameter. 
        Default value: 1% of the corresponding cell parameter.

    Returns
    -------
    map : 2-ple of 1D arrays

        :data:`map[0]` has the indexes of the pristine system with
        correspective atoms in the defective system

        :data:`map[1]`has the indexes of the defective system
        atoms mapped by :data:`map[0]`
    """
    scaled_pos_prist = scaled_pos_prist.copy()%1
    scaled_pos_defect = scaled_pos_defect.copy()%1

    map_prist = []
    map_def = []
    if isinstance(dist_tol, (int, float)):
        dist_tol = np.full(3, dist_tol)
    for i, coords in enumerate(scaled_pos_prist):
        dist = scaled_pos_defect - coords
        dist -= np.rint(dist)
        dist = np.abs(dist)
        condition = dist < dist_tol
        values = np.where(np.all(condition, axis=1))[0]
        if len(values) > 1:
            raise ValueError('dist_tol too large, decrease it\n'
                             'Current value:{}'.format(dist_tol))
        elif len(values) == 1:
            map_prist.append(i)
            map_def.append(values[0])

    return map_prist, map_def

class KumagaiCorr(Ewald):
    """
    Implementation of the Kumagai correction scheme of:
    PRB 89, 195205 (2014)

    Parameters
    ----------
    cell : 2D numpy array
        cell parameters defective supercell

    positions_defective/positions_pristine : 2D numpy array
        fractional coordinates of the atoms in the **DEFECTIVE** and
        **PRISTINE** supercells of same size and shape.

    defect_position : 1D numpy array
        fractional coordinates of the point defect

    defect_formal_charge : float
        charge of the point defect

    dielectric_constant : 2D numpy array
        the dielectric tensor

    dft_core_potential_def/dft_core_potential_prist : 1D numpy array
        potential at the ionic sites calculated by first-principles for
        **DEFECTIVE** and **PRISTINE** systems, respectively.
        Same atomic ordering as in the corresponding :data:`positions_*` arrays

    direct_cutoff/reciprocal_cutoff/alpha :
        see the :class:`spinney.defects.madelung.Ewald` class

    length_units/energy_units : strings
        the unit of length and energy used for :data:`cell` and
        :data:`dft_core_potential_*`

    tol_dist : float
        rounding tolerance for comparing distances, in units of
        :data:`length_units`

    Attributes
    ----------
    atomic_mapping : 2-ple of 1D arrays
        element [0] has the indexes of the pristine system atoms
        with corresponding atoms in the defective system

        element [1] has the indexes of the defective system mapped by
        :data:`map[0]`. Where :data:`map` is returned by
        :meth:`map_atoms_pristine_defect`

    atoms_in_sampling_region : 2-ple
        the first element contains the indices of the atoms of the pristine
        system in the sampling region, the second element contains the
        corresponding atoms of the defective system

    difference_potential_vs_distance : 2-ple of 1D arrays
        element [0] is an array containing the distances from the point
        defects where the electrostatic core potential has been sampled

        element [1] is the difference of the defective and pristine core
        potentials at the point whose distance from the defect is in
        element [0]

    difference_potential_vs_distance_sampling_region : 2-ple of 1D arrays
        as above, but only the sampling region is considered

    alignment_potential_vs_distance_sampling_region : 2-ple of 1D arrays
        element [0] is an array containing the distances from the defect of
        the sites within the sampling region.

        element [1] is the corresponding alignment potential:
        site potential defect - site potential pristine - ewald potential

    ewald_potential_vs_distance_sampling_region : 2-ple of 1D arrays
        the ewald potential calculated at the sites in the sampling region.
        Structure analogous to
        :attr:`alignment_potential_vs_distance_sampling_region`

    grouped_atom_by_distance : 2-ple
        the first element of the tuple reports the distances from the defect
        The second element is another 2-ple;
        each element of this tuple contains a list of lists.
        Each inner list contains the atomic index of the atoms
        that are at a given distance (within :data:`tol_dist`)
        from the defective site for the pristine and defective supercell.
    """
    def __init__(self, cell, positions_defective, positions_pristine,
                 defect_position, defect_formal_charge,
                 dielectric_constant,
                 dft_core_potential_def, dft_core_potential_prist,
                 direct_cutoff=10, reciprocal_cutoff=1, alpha=None,
                 length_units='Angstrom', energy_units='eV', tol_en=1e-6,
                 min_steps=2, tol_dist=1e-2):
        if not isinstance(positions_defective, np.ndarray):
            raise TypeError('positions_defective must be a Numpy array')
        if not isinstance(positions_pristine, np.ndarray):
            raise TypeError('positions_pristine must be a Numpy array')
        if not isinstance(cell, np.ndarray):
            raise TypeError('cell must be a Numpy array')
        self._atom_positions_def = copy(positions_defective)
        self._atom_positions_prist = copy(positions_pristine)
        self._dft_potential_def = copy(dft_core_potential_def)
        self._dft_potential_prist = copy(dft_core_potential_prist)
        self._tol_dist = tol_dist
        self._dec_tol_dist = int(np.floor(-np.log10(tol_dist)))
        self._original_cell = copy(cell)
        Ewald.__init__(self, cell, defect_position, defect_formal_charge,
                       dielectric_constant, direct_cutoff, reciprocal_cutoff,
                       alpha, length_units, energy_units, tol_en, min_steps)
        # the position of the defect
        self._def_pos = self._positions
        self._atoms_map = map_atoms_pristine_defect(self._original_cell,
                                                    self._atom_positions_prist,
                                                    self._atom_positions_def,
                                                    self._tol_dist)
        # cartesian coordinates pristine system from defect position
        # with PBC and MIC
        pos_prist = copy(self._atom_positions_prist)%1
        pos_defect = copy(self._def_pos)%1

        pos_prist = pos_prist - pos_defect
        pos_prist -= np.rint(pos_prist)
        self._shifted_pos_prist_cart = np.dot(pos_prist,
                                              self._original_cell)
    @property
    def atomic_mapping(self):
        return self._atoms_map

    @property
    def atoms_in_sampling_region(self):
        if not hasattr(self, '_atoms_in_region'):
            self._get_atoms_in_sampling_region()
        return self._atoms_in_region

    @property
    def difference_potential_vs_distance(self):
        """ Pot_def - Pot_pristine """
        if not hasattr(self, '_diff_pot'):
            self._difference_potential_vs_distance()
        return self._diff_pot

    @property
    def difference_potential_vs_distance_sampling_region(self):
        if not hasattr(self, '_difference_pot_vs_dist_sample'):
            self._difference_potential_vs_distance_sampling_region()
        return self._difference_pot_vs_dist_sample

    @property
    def alignment_potential_vs_distance_sampling_region(self):
        if not hasattr(self, '_align_pot_vs_dist_sample'):
            self._alignment_potential_vs_distance_sampling_region()
        return self._align_pot_vs_dist_sample

    @property
    def ewald_potential_vs_distance_sampling_region(self):
        if not hasattr(self, '_ewald_pot_vs_dist_sample'):
            self._alignment_potential_vs_distance_sampling_region()
        return self._ewald_pot_vs_dist_sample

    @property
    def grouped_atom_by_distance(self):
        if not hasattr(self, '_groups_by_distance'):
            self._group_atoms_by_distance()
        return (tuple(self._final_distances), self._groups_by_distance)

    @property
    def grouped_atom_by_distance_sampling_region(self):
        if not hasattr(self, '_groups_by_distance_sample'):
            self._get_atoms_in_sampling_region()

        return (tuple(self._final_distances_sampling),
                self._groups_by_distance_sample)

    @property
    def pc_term(self):
        if not hasattr(self, '_pc_term'):
            self.get_correction_energy()
        return self._pc_term

    @property
    def alignment_term(self):
        if not hasattr(self, '_alignment_term'):
            self.get_potential_alignment()
        return self._alignment_term

    def _group_atoms_by_distance(self):
        mapping = self.atomic_mapping
        pos_prist = copy(self._shifted_pos_prist_cart)

        # consider only atoms in pristine system which are mapped in the
        # defective system; i.e. those which position is not severely affected
        # by the presence of the defect
        distances = np.linalg.norm(pos_prist, axis=1)[mapping[0]]
        distances = np.round(distances, self._dec_tol_dist)
        uniq_distances = tuple(set(distances))
        # group atoms by distance
        groups = [] # each sublist will contain the indices of atoms at
                    # a given distance
        groups_def = [] # same as above but for defective system
        final_dist = []
        for i, dist in enumerate(uniq_distances):
            groups.append([])
            groups_def.append([])
            for j, atom_prist in enumerate(mapping[0]):
                pos = distances[j]
                if abs(pos - dist) <= self._tol_dist:
                    groups[i].append(atom_prist)
                    groups_def[i].append(mapping[1][j])
                    if dist not in final_dist:
                        final_dist.append(dist)
        self._groups_by_distance = (groups, groups_def)
        self._final_distances = copy(final_dist)

    def _difference_potential_vs_distance(self):
        groups, groups_def = self.grouped_atom_by_distance[1]
        prist_pot_vs_dist = self._calculate_potential_vs_distance(
            self._dft_potential_prist,
            groups)
        def_pot_vs_dist = self._calculate_potential_vs_distance(
            self._dft_potential_def,
            groups_def)
        pot_align_vs_dist = def_pot_vs_dist - prist_pot_vs_dist

        self._diff_pot = (self._final_distances, pot_align_vs_dist)

    def _get_atoms_in_sampling_region(self):
        cell = self._original_cell
        # note: the shape of self._def_pos is (1,3)
        ind_prist, rad = kumagai_sampling_region(
            cell,
            self._atom_positions_prist,
            self._def_pos[0])
        self.sphere_radius = rad
        pos_in_region = self._atom_positions_prist[ind_prist]
        pos_prist = copy(self._shifted_pos_prist_cart)

        ind_def = kumagai_sampling_region(
            cell,
            self._atom_positions_def,
            self._def_pos[0])[0]
        pos_def_in_region = self._atom_positions_def[ind_def]

        # the number of atoms in the sampling region and in the map can
        # be different between defective and pristine system
        sample_map = map_atoms_pristine_defect(cell,
                                               pos_in_region,
                                               pos_def_in_region,
                                               self._tol_dist)

        sample_map = (np.array(ind_prist)[sample_map[0]],
                      np.array(ind_def)[sample_map[1]])
        self.atomic_mapping_region = sample_map

        distances = np.linalg.norm(pos_prist, axis=1)[sample_map[0]]
        distances = np.around(distances, self._dec_tol_dist)
        uniq_distances = tuple(set(distances))

        # not all atom in the sampling region will be considered;
        # we calculate the potential only if the atom position does not
        # change noticeably (self._tol_dist) after we add the defect
        groups = []
        groups_def = []
        final_dist = []
        for i, dist in enumerate(uniq_distances):
            groups.append([])
            groups_def.append([])
            for j, atom_prist in enumerate(sample_map[0]):
                pos = distances[j]
                if abs(pos - dist) <= self._tol_dist:
                    groups[i].append(atom_prist)
                    groups_def[i].append(sample_map[1][j])
                    if dist not in final_dist:
                        final_dist.append(dist)
        indices_prist_sampling = [atom for group in groups for atom in group]
        indices_def_sampling = [atom for group in groups_def for atom in group]

        # to speed up the calculations of the Ewald Potential we
        # consider only those atoms in the sampling region
        groups_ew = []
        no = 0
        for i, group in enumerate(groups):
            groups_ew.append([])
            for it in group:
                groups_ew[i].append(no)
                no += 1
        scal_pos_ew = self._atom_positions_prist[indices_prist_sampling]
        self._ewald_pot_data = (scal_pos_ew, groups_ew)

        self._indices_pristine = ind_prist
        self._indices_defective = ind_def
        self._groups_by_distance_sample = (groups, groups_def)
        self._atoms_in_region = (indices_prist_sampling, indices_def_sampling)
        self._final_distances_sampling = copy(final_dist)

    def _difference_potential_vs_distance_sampling_region(self):
        groups, groups_def = self.grouped_atom_by_distance_sampling_region[1]

        prist_pot_vs_dist = self._calculate_potential_vs_distance(
            self._dft_potential_prist,
            groups)
        def_pot_vs_dist = self._calculate_potential_vs_distance(
            self._dft_potential_def,
            groups_def)

        pot_align_vs_dist = def_pot_vs_dist - prist_pot_vs_dist

        final_dist = self._final_distances_sampling
        self._difference_pot_vs_dist_sample = (final_dist, pot_align_vs_dist)

    def _alignment_potential_vs_distance_sampling_region(self):
        dist, pot_diff = self.difference_potential_vs_distance_sampling_region

        sample_atoms, groups_sample = self._ewald_pot_data
        ewald_pot = []
        for atom in sample_atoms:
            ewald_pot.append(self.get_ewald_potential(atom))
        ewald_pot = np.array(ewald_pot)

        ewald_pot_vs_dist = self._calculate_potential_vs_distance(
            ewald_pot,
            groups_sample)
        self._ewald_potential = ewald_pot.copy()
        self._ewald_pot_vs_dist_sample = (dist, ewald_pot_vs_dist)
        self._align_pot_vs_dist_sample = (dist,
                                          pot_diff - ewald_pot_vs_dist)

    def _calculate_potential_vs_distance(self, all_potential, potential_map):
        pot_vs_dist = []
        for i in range(len(potential_map)):
            pp = 0
            n = len(potential_map[i])
            for index in potential_map[i]:
                pp += all_potential[index]
            pot_vs_dist.append(pp/n)
        return np.array(pot_vs_dist)

    def _calculate_alignment_term(self):
        if not hasattr(self, '_groups_by_distance_sample'):
            self._difference_potential_vs_distance_sampling_region()
        g_atoms = self._groups_by_distance_sample[0]
        g_align_pot = self.alignment_potential_vs_distance_sampling_region[1]
        av_pot = 0
        n = 0
        for atoms, pot in zip(g_atoms, g_align_pot):
            multi = len(atoms)
            term = pot*multi
            av_pot += term
            n += multi
        return av_pot/n

    def get_potential_alignment(self, option=0):
        if option == 0:
            align = self._calculate_alignment_term()
        elif option == 1:
            align = self.alignment_potential_vs_distance_sampling_region[1]
            align = align.mean()
        else:
            raise ValueError('Option number can only be 0, 1')
        self._alignment_term = align
        return align

    def get_correction_energy(self):
        pc_corr = -self.get_madelung_energy()
        self._pc_term = pc_corr
        return pc_corr

    def get_net_correction_energy(self):
        e1 = self.get_correction_energy()
        e2 = -self._charges[0]*self.get_potential_alignment()
        return e1+e2
