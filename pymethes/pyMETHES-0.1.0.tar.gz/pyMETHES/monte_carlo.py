#  Copyright (c) 2020 ETH Zurich

"""
Module for the MonteCarlo class.

The MonteCarlo class implements all random-number based methods to simulate the motion
of electrons. The simulation time-step is determined with the null collision technique
(calculate_max_coll_freq creates a lookup table for the choice of the
trial collision frequency, determine_timestep calculates the time-step based on the
current maximum electron energy and acceleration). The collision processes are randomly
chosen based on the collision frequency of each process. The scattering angles are
randomly chosen with either an isotropic or an anisotropic model.
"""

# Import Packages
import numpy as np
import numpy.linalg as linalg
import scipy.constants as csts
import scipy.interpolate
from typing import Tuple

# Import modules
import pyMETHES.utils as utils
from pyMETHES.__about__ import __version__
from pyMETHES.config import Config
from pyMETHES.gas_mixture import GasMixture

np.seterr(all='raise')


class MonteCarlo:
    """
    Class implementing all random-number based simulation methods

    Attributes:
        config (Config): configuration of the simulation
        trial_coll_freq (float): trial collision frequency for the null collision
            technique
        max_coll_freq (interp1d): cumulative maximum of the collision frequency as a
            function of the electron energy
        max_coll_period (ndarray): array inversely proportional to the cumulative
            maximum of the collision frequency
        max_coll_period_squared (ndarray): array inversely proportional to the square
            of the cumulative maximum of the collision frequency
        collision_by_electron (ndarray): array of collision index for each electron
            (starting at 0), an index equal to the number of cross sections indicates
            a null collision
    """

    version = f"pyMETHES version {__version__}\n"

    def __init__(self, cfg: Config):
        """
        Instantiates the MonteCarlo class.

        Args:
            cfg (Config): configuration of the simulation
        """

        self.config = cfg

        # trial collision frequency
        self.trial_coll_freq = None
        # data for the calculation of the trial collision frequency
        self.max_coll_freq = None
        self.max_coll_period = None
        self.max_coll_period_squared = None

        # vector of which collision which electron undergoes
        self.collision_by_electron = None

    def calculate_max_coll_freq(self, gas_mixture: GasMixture):
        """
        Calculates the maximum collision frequency in the given gas mixture.

        Args:
            gas_mixture (GasMixture): gas mixture
        """

        gas_density = self.config.gas_number_density
        velocity = utils.velocity_from_energy(gas_mixture.energy_vector)
        freq = gas_density * velocity * gas_mixture.total_cross_section
        # replace zero value to avoid divide by zero:
        freq[0] = freq[1]
        # take cumulative maximum of the collision frequency (make it monotonous)
        freq = np.maximum.accumulate(freq)
        self.max_coll_freq = scipy.interpolate.interp1d(gas_mixture.energy_vector,
                                                        freq,
                                                        kind='linear')
        self.max_coll_period = \
            0.5 * csts.electron_mass / csts.elementary_charge / freq
        self.max_coll_period_squared = \
            0.5 * csts.electron_mass / csts.elementary_charge / freq ** 2

    def determine_timestep(self, max_velocity: float, max_acceleration: float) -> float:
        """
        Determine the duration of the next time-step in the simulation with the
        null-collision technique.

        Args:
            max_velocity (float): current maximum electron velocity
            max_acceleration (float): current maximum electron acceleration

        Returns: time-step duration (s)
        """

        # Draw random number
        s = - np.log(np.random.random())
        # Calculate energy after step (worst case: max_velocity + max_acceleration * dt)
        max_energy = utils.energy_from_velocity(max_velocity)
        freq = self.max_coll_freq.y
        de = 2 * max_velocity * max_acceleration * s * self.max_coll_period \
            + max_acceleration ** 2 * s ** 2 * self.max_coll_period_squared
        # Clip energy after step to maximum energy
        e_end = np.clip(max_energy + de, a_min=None,
                        a_max=self.config.max_cross_section_energy)
        # Find trial collision frequency that fulfills the condition
        ok_frequencies = freq[self.max_coll_freq(e_end) <= freq]
        # Take the first (= smallest) frequency that fulfills the condition
        self.trial_coll_freq = 1.01 * ok_frequencies[0]
        # Calculate the time-step
        dt = s/self.trial_coll_freq
        return dt

    def determine_collisions(self, gas_mixture: GasMixture,
                             velocity_norm: np.ndarray,
                             energy: np.ndarray) -> None:
        """
        Calculates the collision frequencies for all electrons with all cross sections,
        and chooses a collision type via a random number.

        Args:
            gas_mixture (GasMixture): cross section data
            velocity_norm (ndarray): norm of the velocity of each electron
            energy (ndarray): energy of each electron
        """

        # calculate the coll frequency for each cross section and each electron
        collision_matrix = np.array([
            self.config.gas_number_density * interp(energy) * velocity_norm
            / self.trial_coll_freq for interp in gas_mixture.cross_sections])

        rand_vector = np.random.rand(1, energy.size)
        rand_matrix = np.repeat(rand_vector, collision_matrix.shape[0], axis=0)
        coll_matrix_cum = np.cumsum(collision_matrix, axis=0)
        self.collision_by_electron = np.sum(rand_matrix > coll_matrix_cum, axis=0)

    def perform_collisions(
            self, gas_mixture: GasMixture, position: np.ndarray, velocity: np.ndarray,
            energy: np.ndarray) -> Tuple[np.ndarray, np.ndarray, int, int, int]:
        """
        Calculates the electrons positions (created/removed) and velocities (scattered)
        after the collisions listed in the collision_by_electron array.

        Args:
            gas_mixture (GasMixture): cross section data
            position (ndarray): coordinates (x,y,z) of each electron (m)
            velocity (ndarray): velocity of each electron in (x,y,z) directions (m.s-1)
            energy (ndarray): energy of each electron (eV)

        Returns: the new position and velocity of electrons, the number of collisions,
            cations and anions produced
        """

        null_collisions = \
            self.collision_by_electron >= gas_mixture.number_of_cross_sections

        # set aside electrons which did not collide (null collision)
        null_coll_p = position[:, null_collisions]
        null_coll_v = velocity[:, null_collisions]

        is_collision = np.logical_not(null_collisions)
        collisions = self.collision_by_electron[is_collision]
        n_coll = collisions.size
        pos = position[:, is_collision]
        vel = velocity[:, is_collision]
        ener = energy[is_collision]

        # count attached electrons
        attachment_collisions = gas_mixture.is_attachment[collisions]
        n_att = np.count_nonzero(attachment_collisions)

        # remove attached electrons by excluding them
        is_collision = np.logical_not(attachment_collisions)
        collisions = collisions[is_collision]
        pos = pos[:, is_collision]
        vel = vel[:, is_collision]
        ener = ener[is_collision]

        # calculate the new velocity direction after scattering
        v_scattered_hat, cos_chi = MonteCarlo.unit_scattered_velocity(
            ener, vel, self.config.isotropic_scattering)

        # Calculate the losses and the remaining energy
        mass_ratios = gas_mixture.mass_ratios[collisions]
        ionization_collisions = gas_mixture.is_ionization[collisions]
        thresholds = gas_mixture.thresholds[collisions]
        sharing = np.ones(thresholds.shape)
        sharing[ionization_collisions] *= self.config.energy_sharing_factor
        losses = thresholds + ener * mass_ratios * (1 - cos_chi)
        energy_after_coll = np.maximum(ener - losses, 0)

        # Calculate the new velocity
        v_scattered = \
            v_scattered_hat * utils.velocity_from_energy(
                energy_after_coll * sharing)

        # Add electrons produced by ionization
        new_e_pos = pos[:, ionization_collisions]
        new_e_energy = energy_after_coll[ionization_collisions] \
            * (1 - self.config.energy_sharing_factor)
        new_e_velocity = \
            MonteCarlo.unit_scattered_velocity(ener[ionization_collisions],
                                               vel[:, ionization_collisions], True)[0] \
            * utils.velocity_from_energy(new_e_energy)
        n_ion = new_e_energy.size

        pos_end = np.hstack([null_coll_p, pos, new_e_pos])
        vel_end = np.hstack([null_coll_v, v_scattered, new_e_velocity])

        if self.config.conserve:
            ne_ini = position.shape[1]
            ne_end = pos_end.shape[1]
            if ne_end > ne_ini:
                # delete some random electrons to compensate for the increased number
                indexes_to_keep = np.random.permutation(ne_end)[:ne_ini]
                pos_end = pos_end[:, indexes_to_keep]
                vel_end = vel_end[:, indexes_to_keep]
            elif ne_end < ne_ini:
                # duplicate some random electrons to compensate for the decreased number
                n_duplicates = ne_ini - ne_end
                # stack if required, to draw enough duplicates
                n_stacks = int(np.ceil(n_duplicates/ne_end))
                indexes_to_duplicate = np.concatenate(
                    [np.random.permutation(ne_end) for _ in range(n_stacks)]
                )[:n_duplicates]
                pos_end = np.hstack([pos_end, pos_end[:, indexes_to_duplicate]])
                vel_end = np.hstack([vel_end, vel_end[:, indexes_to_duplicate]])

        return pos_end, vel_end, n_coll, n_ion, n_att

    @staticmethod
    def unit_scattered_velocity(energy: np.ndarray, velocity: np.ndarray,
                                iso: bool) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates the new direction of the velocity vector after scattering.

        Args:
            energy (ndarray): energy of each electron (eV)
            velocity (ndarray): velocity of each electron in (x,y,z) directions before
                the collision (m.s-1)
            iso (bool): isotropic scattering (True) or anisotropic scattering (False)

        Returns: normed velocities after collisions, cosine of polar scattering angle
        """

        cos_chi, sin_chi, cos_phi, sin_phi = MonteCarlo.scattering_angles(energy, iso)

        # Normalize the velocity
        v_hat = velocity / linalg.norm(velocity, axis=0, keepdims=True)

        # unit vector in x direction
        e_x = np.zeros_like(velocity)
        e_x[0, :] = 1

        # calculate theta (angle between v_hat and e_x)
        theta = np.arccos(v_hat[0, :])
        sin_theta = np.sin(theta)

        # calculate the direction of the new velocity, see Vahedi 1995 equation (11)
        v_new_dir = \
            v_hat * cos_chi \
            + np.cross(v_hat, e_x, axis=0) * sin_chi * sin_phi / sin_theta \
            + np.cross(v_hat, np.cross(e_x, v_hat, axis=0), axis=0) \
            * sin_chi * cos_phi / sin_theta

        return v_new_dir, cos_chi

    @staticmethod
    def scattering_angles(energy: np.ndarray, iso: bool
                          ) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
        """
        Generates values for the polar (chi) and azimuthal (phi)
        isotropic or anisotropic scattering angles according to Vahedi (1995).

        Args:
            energy: array of electron energies
            iso: isotropic scattering or not

        Returns: 4 arrays cos(chi), sin(chi), cos(phi), sin(phi)
        """

        # choose scattering angle phi
        phi = 2 * np.pi * np.random.random(energy.size)
        sin_phi = np.sin(phi)
        cos_phi = np.cos(phi)

        # choose scattering angle chi
        if iso:
            cos_chi = 1 - 2 * np.random.random(energy.size)
        else:
            cos_chi = (2 + energy
                       - 2 * (1 + energy) ** np.random.random(energy.size)) / energy

        sin_chi = np.sqrt(1 - cos_chi ** 2)

        return cos_chi, sin_chi, cos_phi, sin_phi
