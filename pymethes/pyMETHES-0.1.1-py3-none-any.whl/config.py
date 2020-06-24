#  Copyright (c) 2020 ETH Zurich

"""
Module for the Config class of the simulation.
"""

# Import Packages
import json5
import json
from typing import Union
import scipy.constants as csts

num = Union[int, float]


class Config:
    """
    Configuration class for the Monte-Carlo simulation.

    The configuration can be loaded from, or saved to, json or json5 files.
    Alternatively, it can be provided as, or exported to, a (nested) dictionary.
    The gas number density is not a configuration parameter, but a
    cached property of the Config class, which is computed from the pressure and
    temperature.

    Attributes:
        gases (list): sum formulae of gases
        paths_to_cross_section_files (list): paths to the cross section files in
            txt format
        fractions (list): proportions of the gases in the gas mixture
        max_cross_section_energy (float): maximum cross section energy (eV)

        output_directory (str): path to the output directory

        EN (float): E/N ratio in (Td)
        _pressure (float): gas pressure in Pa
        _temperature (float): gas temperature in K
        _gas_number_density (float): gas number density in m-3

        num_e_initial (int): initial number of electrons
        initial_pos_electrons (list): initial position [x, y, z] of the electrons'
            center of mass
        initial_std_electrons (list): initial broadening of gaussian distributed
            electrons in x, y and z direction

        num_energy_bins (int): number of energy bins to group the electrons for the
            energy distribution
        energy_sharing_factor (float): energy sharing factor for ionization collisions
        isotropic_scattering (bool): scattering: isotropic (true), non-isotropic
            according to Vahedi et al. (false)
        conserve (bool): conservation of the number of electrons
        num_e_max (int): maximum allowed electron number (when it is reached, the
            number of electrons is then conserved until simulation ends)

        w_tol (float): tolerance on the flux drift velocity. simulation ends
            when w_err/w < w_tol
        DN_tol (float): tolerance on the flux diffusion coefficient. simulation ends
            when DN_err/w < DN_tol
        num_col_max (int): maximum number of collisions during the simulation,
            simulation ends when it is reached
    """

    def __init__(self, config: Union[str, dict]):
        """
        Instantiate the config.

        Args:
            config (str, dict): path to a json or json5 config file, or dictionary.
        """

        if isinstance(config, str):
            if config.endswith('.json5'):
                with open(config, "r") as json_file:
                    config = json5.load(json_file)
            elif config.endswith('.json'):
                with open(config, "r") as json_file:
                    config = json.load(json_file)
            else:
                raise ValueError(f"Configuration file '{config}' has invalid extension."
                                 " Extensions '.json' or '.json5' are expected.")

        # gases
        input_gases = config['input_gases']
        self.paths_to_cross_section_files: (str, list) = \
            input_gases['paths_to_cross_section_files']
        self.gases: (str, list) = input_gases['gases']
        self.fractions: (float, list) = input_gases['fractions']
        self.max_cross_section_energy: num = input_gases['max_cross_section_energy']

        # output
        output = config['output']
        self.output_directory: str = output['output_directory']
        self.base_name: str = output['base_name']
        self.save_simulation_pickle: bool = output['save_simulation_pickle']
        self.save_temporal_evolution: bool = output['save_temporal_evolution']
        self.save_swarm_parameters: bool = output['save_swarm_parameters']
        self.save_energy_distribution: bool = output['save_energy_distribution']

        # physical conditions
        physical_conditions = config['physical_conditions']
        self.EN: num = physical_conditions['EN']
        self._pressure: num = physical_conditions['pressure']
        self._temperature: num = physical_conditions['temperature']
        self._gas_number_density = None

        # initial state
        initial_state = config['initial_state']
        self.num_e_initial: int = int(initial_state['num_e_initial'])
        self.initial_pos_electrons: list = initial_state['initial_pos_electrons']
        self.initial_std_electrons: list = initial_state['initial_std_electrons']

        # simulation settings
        simulation = config['simulation_settings']
        self.num_energy_bins: int = simulation['num_energy_bins']
        self.energy_sharing_factor: num = simulation['energy_sharing_factor']
        self.isotropic_scattering: bool = simulation['isotropic_scattering']
        self.conserve: bool = simulation['conserve']
        self.num_e_max: int = int(simulation['num_e_max'])

        # end conditions
        end_conditions = config['end_conditions']
        self.w_tol: float = end_conditions['w_tol']
        self.DN_tol: float = end_conditions['DN_tol']
        self.num_col_max: int = int(end_conditions['num_col_max'])

    @property
    def gas_number_density(self) -> float:
        if self._gas_number_density is None:
            self._gas_number_density = \
                self.pressure / (csts.Boltzmann * self.temperature)
        return self._gas_number_density

    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, value: float):
        """
        Pressure setter. If a new value is set, resets the cache for the gas
        number density.

        :param value: pressure in Pascal
        """
        self._pressure = value
        self._gas_number_density = None

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        """
        Temperature setter. If a new value is set, resets the cache for the gas
        number density.

        :param value: temperature in Kelvin
        """
        self._temperature = value
        self._gas_number_density = None

    def to_dict(self) -> dict:
        """
        Returns the current configuration as a dictionary.

        Returns: dict of configuration
        """

        return {
            'input_gases': {
                'gases': self.gases,
                'paths_to_cross_section_files': self.paths_to_cross_section_files,
                'fractions': self.fractions,
                'max_cross_section_energy': self.max_cross_section_energy,
            },
            'output': {
                'output_directory': self.output_directory,
                'base_name': self.base_name,
                'save_simulation_pickle': self.save_simulation_pickle,
                'save_temporal_evolution': self.save_temporal_evolution,
                'save_swarm_parameters': self.save_swarm_parameters,
                'save_energy_distribution': self.save_energy_distribution,
            },
            'physical_conditions': {
                'EN': self.EN,
                'pressure': self.pressure,
                'temperature': self.temperature,
            },
            'initial_state': {
                'num_e_initial': self.num_e_initial,
                'initial_pos_electrons': self.initial_pos_electrons,
                'initial_std_electrons': self.initial_std_electrons,
            },
            'simulation_settings': {
                'num_energy_bins': self.num_energy_bins,
                'energy_sharing_factor': self.energy_sharing_factor,
                'isotropic_scattering': self.isotropic_scattering,
                'conserve': self.conserve,
                'num_e_max': self.num_e_max,
            },
            'end_conditions': {
                'w_tol': self.w_tol,
                'DN_tol': self.DN_tol,
                'num_col_max': self.num_col_max,
            }
        }

    def save_json5(self, path: str = 'config.json5') -> None:
        """
        Saves the current configuration to a json5 file.

        Args:
            path (str): path including the file name and extension,
                example: 'data/config.json5'
        """

        with open(path, "w") as config_file:
            json5.dump(self.to_dict(), config_file, indent=2)

    def save_json(self, path: str = 'config.json') -> None:
        """
        Saves the current configuration to a json file.

        Args:
            path (str): path including the file name and extension,
                example: 'data/config.json'
        """

        with open(path, "w") as config_file:
            json.dump(self.to_dict(), config_file, indent=2)
