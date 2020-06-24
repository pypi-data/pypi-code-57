#  Copyright (c) 2020 ETH Zurich

"""
Module for the Output class.
"""

# Import Packages
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

# Import modules
from pyMETHES.config import Config
from pyMETHES.electrons import Electrons
from pyMETHES.energy_distribution import TimeAveragedEnergyDistribution
from pyMETHES.transport_data import BulkData, FluxData
from pyMETHES.rate_coefficients import ConvolutedRates, CountedRates
from pyMETHES.temporal_evolution import TimeSeries

np.seterr(all='raise')


class Output:
    """
    The Output class instantiates all output-related classes: TimeSeries,
    TimeAveragedEnergyDistribution, FluxData, BulkData, ConvolutedRates, CountedRates.
    It also provides methods to save or to plot the output data. Finally, it provides
    the check_sst method which test if the swarm is at equilibrium based on the
    evolution of the mean electron energy.

    Attributes:
        config (Config): configuration of the simulation
        version (str): version of pyMETHES as a string
        time_series (TimeSeries): temporal evolution data
        energy_distribution (TimeAveragedEnergyDistribution): energy distribution data
        flux (FluxData): flux transport data
        bulk (BulkData): flux transport data
        rates_conv (ConvolutedRates): convoluted rate coefficients
        rates_count (CountedRates): counted rate coefficients
    """

    def __init__(self, cfg: Config, ver: str, electrons: Electrons):
        """
        Instantiates the Output class.

        Args:
            cfg (Config): configuration of the simulation
            ver (str): version of pyMETHES as a string
            electrons (Electrons): electron data
        """

        self.config = cfg
        self.version = ver

        # temporal evolution of some quantities
        self.time_series = TimeSeries(electrons)

        # energy-related data:
        self.energy_distribution = TimeAveragedEnergyDistribution()

        # flux data
        self.flux = FluxData(self.config.gas_number_density)

        # bulk data
        self.bulk = BulkData(self.config.gas_number_density)

        # rate coefficients calculated by convolution
        self.rates_conv = ConvolutedRates()

        # rate coefficients calculated by counting events
        self.rates_count = CountedRates(cfg.gas_number_density, cfg.conserve)

    def check_sst(self) -> bool:
        """
        Checks if the swarm energy is at equilibrium (steady-state). This is done by
        checking if the mean electron energy has dropped during the last 10% of the
        elapsed time, compared to the period between 80 and 90%.

        Returns: True if equilibrium was reached, False otherwise
        """

        # Intervals need to contain at least 10 elements
        n = round(self.time_series.mean_energy.size / 10)
        # Checks if the interval 80-90 % of energy data is larger
        # than the interval 90-100%
        if n >= 10 and np.mean(self.time_series.mean_energy[-2*n:-n]) >= \
                np.mean(self.time_series.mean_energy[-n:]):
            # store the index, where the sst-data starts
            self.time_series.ind_equ = self.time_series.time.size
            return True
        return False

    def save_temporal_evolution(self, name: str = None) -> None:
        """
        Saves the temporal evolution of the swarm data to a json file.

        Args:
            name: name of the json file created
        """

        if name is None:
            name = '_'.join([self.config.base_name, "temporal_evolution"])

        with open(self.config.output_directory + name + ".json", "w") as output_file:
            json.dump(self.time_series.to_dataframe().to_dict('list'), output_file,
                      indent=2)

    def save_swarm_parameters(self, name: str = None) -> None:
        """
        Saves the final swarm parameters to a json file.

        Args:
            name: name of the json file created
        """

        if self.flux.w_err[2] is not None:

            coefficients = {
                'E/N (Td)': float(self.config.EN),
                'mean energy (eV)': self.energy_distribution.energy_mean,
                'mean energy error (eV)': self.energy_distribution.energy_mean_err,
                'bulk drift velocity (m.s-1)': self.bulk.w[2],
                'bulk drift velocity error (m.s-1)': self.bulk.w_err[2],
                'bulk L diffusion coeff. * N (m-1.s-1)': self.bulk.DN[2],
                'bulk L diffusion coeff. error * N (m-1.s-1)':
                    self.bulk.DN_err[2],
                'bulk T diffusion coeff. * N (m-1.s-1)': self.bulk.DN[0],
                'bulk T diffusion coeff. error * N (m-1.s-1)':
                    self.bulk.DN_err[0],
                'flux drift velocity (m.s-1)': self.flux.w[2],
                'flux drift velocity error (m.s-1)': self.flux.w_err[2],
                'flux L diffusion coeff. * N (m-1.s-1)': self.flux.DN[2],
                'flux L diffusion coeff. error * N (m-1.s-1)':
                    self.flux.DN_err[2],
                'flux T diffusion coeff. * N (m-1.s-1)': self.flux.DN[0],
                'flux T diffusion coeff. error * N (m-1.s-1)':
                    self.flux.DN_err[0],
                'effective ionization rate coeff. (counted) (m3.s-1)':
                    self.rates_count.effective,
                'effective ionization rate coeff. (counted) error (m3.s-1)':
                    self.rates_count.effective_err,
                'ionization rate coeff. (counted) (m3.s-1)':
                    self.rates_count.ionization,
                'ionization rate coeff. (counted) error (m3.s-1)':
                    self.rates_count.ionization_err,
                'attachment rate coeff. (counted) (m3.s-1)':
                    self.rates_count.attachment,
                'attachment rate coeff. (counted) error (m3.s-1)':
                    self.rates_count.attachment_err,
                'effective ionization rate coeff. (convolution) (m3.s-1)':
                    self.rates_conv.effective,
                'ionization rate coeff. (convolution) (m3.s-1)':
                    self.rates_conv.ionization,
                'attachment rate coeff. (convolution) (m3.s-1)':
                    self.rates_conv.attachment,
            }

            if name is None:
                name = '_'.join([self.config.base_name, "swarm_parameters"])

            with open(self.config.output_directory
                      + name + ".json", "w") as output_file:
                json.dump(coefficients, output_file, indent=2)

    def save_energy_distribution(self, name: str = None) -> None:
        """
        Saves the final time-averaged electron energy distribution function and electron
        energy probability function to a json file.

        Args:
            name: name of the json file created
        """

        if self.energy_distribution.eedf is not None:
            energy_distributions = pd.DataFrame({
                'energy (eV)': self.energy_distribution.energy_bin_centers,
                'eedf (eV-1)': self.energy_distribution.eedf,
                'eepf (eV-3/2)': self.energy_distribution.eepf
            }).to_dict('list')

            if name is None:
                name = '_'.join([self.config.base_name, "energy_distribution"])

            with open(self.config.output_directory
                      + name + ".json", "w") as output_file:
                json.dump(energy_distributions, output_file, indent=2)

    @staticmethod
    def plot_sst_line(axes, t_sst) -> None:
        """
        Plots a vertical line at the time instant where equilibrium is reached.

        Args:
            axes: axes to plot the line on
            t_sst: equilibration time
        """

        y_limits = axes.get_ylim()
        axes.plot([t_sst, t_sst], y_limits, 'k-', label='equilibration time')
        axes.set_ylim(y_limits)

    def plot_temporal_evolution(self, show: bool = True,
                                block: bool = True) -> plt.Figure:
        """
        Produces a figure showing the temporal evolution of the swarm. The figure
        contains five subplots showing the number of particles, the mean electron
        energy, the number of collisions, the mean electron position and the
        variance of electron positions.

        Args:
            show (bool): calls plt.show() if True, else does nothing
            block (bool): if show is True, plt.show(block) is called

        Returns: Matplotlib figure object
        """

        data = self.time_series
        simu_time = data.time
        pos_mean = data.mean_position
        pos_variance = data.var_position

        # plot a line to indicate the time when equilibrium is reached
        t_sst = None
        if self.time_series.ind_equ is not None:
            t_sst = data.time[self.time_series.ind_equ]

        fig = plt.figure()
        ax = fig.add_subplot(231)
        ax.plot(simu_time, data.num_electrons - data.num_electrons[0],
                label='n_electrons - n_0', linewidth=3)
        ax.plot(simu_time, data.num_cations, label='n_cations')
        ax.plot(simu_time, data.num_anions, label='n_anions')
        Output.plot_sst_line(ax, t_sst)
        ax.legend()
        ax.set_title('Number of Particles')
        ax.set_ylabel('number of particles')
        ax.set_xlabel('time (s)')
        ax.grid(True)

        ax = fig.add_subplot(232)
        ax.plot(simu_time, data.mean_energy)
        Output.plot_sst_line(ax, t_sst)
        ax.legend()
        ax.set_title("Mean Energy of Electrons")
        ax.set_ylabel('mean electron energy (eV)')
        ax.set_xlabel('time (s)')
        ax.grid(True)

        ax = fig.add_subplot(233)
        ax.plot(simu_time[1:], np.diff(data.num_collisions), label='collisions')
        ax.plot(simu_time[1:], data.num_electrons[1:] - np.diff(data.num_collisions),
                label='null collisions')
        Output.plot_sst_line(ax, t_sst)
        ax.legend()
        ax.set_title('Number of Collisions Per Simulation Step')
        ax.set_ylabel('number of collisions')
        ax.set_xlabel('time (s)')
        ax.grid(True)

        ax = fig.add_subplot(234)
        ax.plot(simu_time, pos_mean[:, 0], label="x")
        ax.plot(simu_time, pos_mean[:, 1], label="y")
        ax.plot(simu_time, pos_mean[:, 2], label="z")
        Output.plot_sst_line(ax, t_sst)
        ax.legend()
        ax.set_title("Mean Position of Electrons")
        ax.set_ylabel('mean position (m)')
        ax.set_xlabel('time (s)')
        ax.grid(True)

        ax = fig.add_subplot(235)
        ax.plot(simu_time, pos_variance[:, 0], label="x")
        ax.plot(simu_time, pos_variance[:, 1], label="y")
        ax.plot(simu_time, pos_variance[:, 2], label="z")
        Output.plot_sst_line(ax, t_sst)
        ax.legend()
        ax.set_title("Variance of Electrons Positions")
        ax.set_ylabel('variance (m$^2$)')
        ax.set_xlabel('time (s)')
        ax.grid(True)

        if show:
            plt.show(block=block)
        return fig

    def plot_energy_distribution(self, show: bool = True,
                                 block: bool = True) -> plt.Figure:
        """
        Produces a figure showing the time-averaged electron energy distribution
        function and electron energy probability function.

        Args:
            show (bool): calls plt.show() if True, else does nothing
            block (bool): if show is True, plt.show(block) is called

        Returns: Matplotlib figure object
        """

        if self.energy_distribution.eedf is not None:
            energy = self.energy_distribution.energy_bin_centers

            fig, ax1 = plt.subplots()
            plt.title("Electron Energy Distribution Function (EEDF) \n"
                      "and Electron Energy Probability Function (EEPF)")
            color = 'tab:blue'
            ax1.plot(energy, self.energy_distribution.eedf, color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.set_ylabel('EEDF (eV$^{-1}$)', color=color)
            ax1.set_xlabel('energy (eV)')
            ax1.grid(True)

            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.plot(energy, self.energy_distribution.eepf, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.set_ylabel('EEPF (eV$^{-3/2}$)', color=color)

            if show:
                plt.show(block=block)
            return fig
