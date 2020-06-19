#  Copyright (c) 2020 ETH Zurich

"""
Module for the GasMixture class, which aggregates data of different gases.

The GasMixture uses the cross_section module to read cross section data. It stores
linear interpolations of each cross section, as well as the mass ratio,
energy threshold and type of cross section, which are needed for the simulation.
The proportions of the gas mixture should sum up to 1. A common energy_vector for all
cross sections is calculated, as well as the total_cross_section.
"""

# Import Packages
import numpy as np
from lxcat_data_parser import CrossSectionTypes as CST
import scipy.interpolate

# Import modules
from pyMETHES.cross_section import InterpolatedCrossSectionSet

np.seterr(all='raise')


class GasMixture:
    """
    Class representing a gas mixture.

    Attributes:
        cross_sections (ndarray): array of cross section interpolations (from all gases)
        types (ndarray): type of each cross section of each species
        thresholds (ndarray): threshold of each cross section of each species
        mass_ratios (ndarray): mass ratios (repeated for each cross section)
        is_attachment (ndarray): boolean mask for ATTACHMENT cross sections
        is_ionization (ndarray): boolean mask for IONIZATION cross sections
        energy_vector (ndarray): common energy vector, containing all distinct energies
            of all cross sections
        total_cross_section (ndarray): sum of all cross sections of all species,
            linearly interpolated at energy_vector
        number_of_cross_sections (int): total number of cross sections (from all gases)
    """

    def __init__(self, gas_formulas: list, path_to_cross_section_files: list,
                 proportions: list, max_cross_section_energy: float):
        """
        Instantiates a GasMixture.

        Args:
            gas_formulas (list): list of the chemical formulas of the species
            path_to_cross_section_files (list): path to the cross section data of each
                species
            proportions (list): proportion of each species in the mixture
            gases (list): InterpolatedCrossSectionSet of each species
            max_cross_section_energy (float): maximum cross section energy (eV)
            number_of_cross_sections (int): total number of cross sections across all
                species

        Raises:
            ValueError: If the proportions do not sum up to 1
        """

        # check if the sum of proportions is 1
        if not np.isclose(sum(proportions), 1):
            raise ValueError("The sum of the proportions of the gases in the GasMixture"
                             "must be 1, but it is %1.2f" % (sum(proportions)))

        # Create a list with a Gas Object for each gas of the mixture
        gases = [InterpolatedCrossSectionSet(max_cross_section_energy, *args)
                 for args in zip(path_to_cross_section_files, gas_formulas)]

        self.cross_sections = np.array([
            scipy.interpolate.interp1d(x.data['energy'].to_numpy(),
                                       x.data['cross section'].to_numpy() * p,
                                       kind='linear')
            for p, gas in zip(proportions, gases) for x in gas.cross_sections
        ])

        cross_sections = [x for gas in gases for x in gas.cross_sections]
        self.thresholds = np.asarray([x.threshold for x in cross_sections])
        self.mass_ratios = np.asarray([x.mass_ratio for x in cross_sections])
        self.types = [x.type for x in cross_sections]
        types_array = np.asarray(self.types)
        self.is_attachment = types_array == CST.ATTACHMENT
        self.is_ionization = types_array == CST.IONIZATION

        # combine the energy vectors into a total energy vector
        all_energies = np.concatenate([x.data['energy'] for x in cross_sections])
        self.energy_vector = np.unique(all_energies)

        # calculate the total cross section
        self.total_cross_section = \
            np.sum([interp(self.energy_vector) for interp in self.cross_sections],
                   axis=0)

    @property
    def number_of_cross_sections(self) -> int:
        """
        Returns: Total number of cross sections, all gases considered.
        """

        return self.cross_sections.size
