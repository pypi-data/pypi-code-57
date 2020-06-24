#  Copyright (c) 2020 ETH Zurich

"""
Module for the Simulation class.
"""

# Import Packages
import pickle
import numpy as np
import os
from typing import Union

# Import modules
from pyMETHES.__about__ import __version__
from pyMETHES.config import Config
from pyMETHES.monte_carlo import MonteCarlo
from pyMETHES.gas_mixture import GasMixture
from pyMETHES.electrons import Electrons
from pyMETHES.output import Output


class Simulation:
    """
    Main class of the pyMETHES simulation tool.

    The Simulation can be initialized providing the path to a configuration file, or
    a configuration dictionary. A different configuration can be applied at later stages
    using the apply_config method. A single simulation can be run with the run method,
    a series of simulation with the run_series method.

    Attributes:
        config (Config): configuration of the simulation
        mc (MonteCarlo): Monte-Carlo methods
        gas_mixture (GasMixture): GasMixture object containing the cross section data
        electric_field (float): electric field strength (V.m-1)
        electrons (Electrons): electron related data
        output (Output): output data of the simulation
    """

    version = f"pyMETHES version {__version__}\n"

    def __init__(self, config: Union[str, dict]):
        """
        Instantiates a Simulation.

        Args:
            config (str, dict): path to a json or json5 config file, or dictionary.
        """

        self.config = None
        self.mc = None
        self.gas_mixture = None
        self.electric_field = None
        self.electrons = None
        self.output = None
        self.apply_config(config)

    def apply_config(self, config: Union[str, dict] = None) -> None:
        """
        Applies the config to (re-)initialize all attributes of Simulation.

        Args:
            config (str, dict): path to a json or json5 config file, or dictionary
                containing the configuration for the simulation
        """

        if config is not None:
            self.config = Config(config)

        # creates the output directory if it does not already exist
        if not os.path.isdir(self.config.output_directory):
            os.mkdir(self.config.output_directory)

        self.mc = MonteCarlo(self.config)

        self.gas_mixture = GasMixture(self.config.gases,
                                      self.config.paths_to_cross_section_files,
                                      self.config.fractions,
                                      self.config.max_cross_section_energy)

        # Electric field strength in the z direction
        self.electric_field = self.config.EN * 1e-21 * self.config.gas_number_density

        self.electrons = Electrons(self.config.num_e_initial,
                                   self.config.initial_pos_electrons,
                                   self.config.initial_std_electrons,
                                   self.electric_field)

        self.output = Output(self.config, self.version, self.electrons)

    def run(self) -> None:
        """
        Runs the simulation, until one of the end conditions is fulfilled.
        """

        self.mc.calculate_max_coll_freq(self.gas_mixture)
        while not self.end_simulation():
            self.advance_one_step()
            self.print_step_info()
        self.calculate_final_output()
        self.save()

    def run_series(self, param: str, values: np.ndarray) -> None:
        """
        Runs a series of simulations.

        Args:
            param (str): name of the configuration parameter to be varied
            values (ndarray): list of values of the configuration parameter for the
                different simulations
        """

        base_name = self.config.base_name
        cfg_dict = self.config.to_dict()

        category = [cat for cat in cfg_dict.keys() if param in cfg_dict[cat].keys()]
        if not category:
            raise ValueError(f"{param} is not a valid configuration parameter name.")
        else:
            category = category[0]

        digits = len(str(values.size))
        for i, val in enumerate(values):
            cfg_dict['output']['base_name'] = base_name + f"_{i:0{digits}}"
            cfg_dict[category][param] = val
            self.apply_config(cfg_dict)
            self.run()

    def save(self) -> None:
        """
        Save the data specified in the configuration: pickle file of the simulation,
        temporal evolution of the swarm, swarm parameters, electron energy distribution.
        """

        if self.config.save_simulation_pickle:
            self.save_pickle()
        if self.config.save_temporal_evolution:
            self.output.save_temporal_evolution()
        if self.config.save_swarm_parameters:
            self.output.save_swarm_parameters()
        if self.config.save_energy_distribution:
            self.output.save_energy_distribution()

    def save_pickle(self, name: str = None) -> None:
        """
        Save the MonteCarlo class instance to a pickle file.

        Args:
            name: name of the pickle file created
        """

        if name is None:
            name = '_'.join([self.config.base_name, "simulation"])

        with open(self.config.output_directory + name + ".pickle", "wb") as pickle_file:
            pickle.dump(self, pickle_file)

    def advance_one_step(self) -> None:
        """
        Advances the simulation by one time step.
        """

        dt = self.mc.determine_timestep(self.electrons.max_velocity_norm,
                                        self.electrons.max_acceleration_norm)
        self.mc.determine_collisions(self.gas_mixture, self.electrons.velocity_norm,
                                     self.electrons.energy)
        pos, vel, nc, ni, na = self.mc.perform_collisions(self.gas_mixture,
                                                          self.electrons.position,
                                                          self.electrons.velocity,
                                                          self.electrons.energy)
        self.electrons.apply_scatter(pos, vel, self.electric_field)
        self.electrons.free_flight(dt)
        self.collect_output_data(dt, nc, ni, na)

    def collect_output_data(self, dt, nc, ni, na):
        """
        Collects and store current data for the simulation output.

        Args:
            dt (float): duration of the current time-step (s)
            nc (int): number of collisions during the current time-step
            ni (int): number of cations produced during the current time-step
            na (int): number of anions produced during the current time-step
        """

        self.output.time_series.append_data(self.electrons, dt, nc, ni, na)
        if self.output.time_series.ind_equ is None:
            if self.output.check_sst():
                # when equilibrium is reached, generate fixed energy bins to start
                # averaging the eedf over time:
                self.output.energy_distribution.generate_bins(
                    self.config.num_energy_bins,
                    self.electrons.max_energy
                )
        else:
            # updates the time-averaged energy distribution of electrons
            self.output.energy_distribution.collect_histogram(
                self.electrons.energy)
            # calculates the flux data (end condition for the simulation)
            self.output.flux.calculate_data(self.output.time_series)

    def calculate_final_output(self) -> None:
        """
        Calculates the final output data at the end of the simulation.
        """

        if self.output.time_series.ind_equ is not None:
            self.output.flux.calculate_data(self.output.time_series)
            self.output.bulk.calculate_data(self.output.time_series)
            self.output.energy_distribution.calculate_distribution(
                self.output.time_series.mean_energy[self.output.time_series.ind_equ:])
            self.output.rates_conv.calculate_data(self.gas_mixture,
                                                  self.output.energy_distribution)
            self.output.rates_count.calculate_data(self.output.time_series)

    def print_step_info(self) -> None:
        """
        Prints information on the current simulation step: mean electron energy,
        relative error of the flux drift velocity in z direction, and relative error
        of the flux diffusion coefficient (maximum of x, y, z directions).
        """

        info = f"Mean energy: {self.electrons.mean_energy:6.2f} eV."
        try:
            rel_err_w = self.output.flux.w_err[2] / self.output.flux.w[2]
            rel_err_d = np.max(self.output.flux.DN_err / self.output.flux.DN)
            info += (f" Error of w: {100 * rel_err_w:5.2f}%."
                     f" Error of DN: {100 * rel_err_d:5.2f}%.")
        except FloatingPointError:
            pass
        print(info)

    def end_simulation(self) -> bool:
        """
        Check end conditions for the simulation.

        Returns: True if simulation is finished, False otherwise.
        """

        end = False
        if not self.config.conserve:
            if self.electrons.num_e <= 0:
                end = True
                print('Simulation ended: number of electrons is zero')
            if self.electrons.num_e >= self.config.num_e_max:
                self.config.conserve = True
                print('Maximum number of electrons reached. Conserving the number '
                      'of electrons for the rest of the simulation.')

        # condition on the convergence of flux w and flux DN
        if not np.isnan(self.output.flux.DN_err[2]):
            w = self.output.flux.w
            w_err = self.output.flux.w_err
            DN = self.output.flux.DN
            DN_err = self.output.flux.DN_err
            if w_err[2] <= w[2] * self.config.w_tol \
                    and all(DN_err <= DN * self.config.DN_tol):
                end = True
                print("Simulation ended."
                      f" Error of w < {100 * self.config.w_tol:5.3}%."
                      f" Error of DN < {100 * self.config.DN_tol:5.3}%.")

        if self.output.time_series.num_collisions[-1] >= self.config.num_col_max:
            end = True
            print('Simulation ended: maximum number of collisions reached')

        return end
