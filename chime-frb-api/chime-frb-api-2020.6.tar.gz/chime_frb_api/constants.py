from __future__ import division

###############################################################################
#                             CHIME/FRB CONSTANTS                             #
###############################################################################


#
#  I N C O H E R E N T   B E A M   C O N S T A N T S
#
INCOHERENT_BEAM_RA_ERROR = 1.5  # RA error in degrees
INCOHERENT_BEAM_DEC_ERROR = 90.0  # Dec error in degrees
INCOHERENT_BEAM_X_POSITION = 0.0  # at zenith
INCOHERENT_BEAM_Y_POSITION = 0.0  # at zenith

#
#   D I S P E R S I O N   M E A S U R E   C O N S T A N T
#

# In MHz**2 s / (pc cm^-3)
"""
k_DM = (
    phys_const.elementary_charge ** 2
    / 2
    / phys_const.pi
    / 4
    / phys_const.pi
    / phys_const.epsilon_0
    / phys_const.electron_mass
    / phys_const.speed_of_light
    * (phys_const.parsec / phys_const.centi ** 3)
) / 1e6 ** 2
"""
# Dispersion constant defined for pulsar studies (Manchester & Taylor 1972)
k_DM = 1.0 / 2.41e-4


#
#   C H I M E   I N S T R U M E N T A L   C O N S T A N T S
#

# Sampling frequency, in Hz.
adc_sampling_freq = float(800e6)

# Number of samples in the inital FFT in the F-engine.
fpga_num_samp_fft = 2048
# f-engine parameters for alias sampling in second Nyquist zone.
fpga_num_freq = fpga_num_samp_fft // 2
fpga_freq0_mhz = adc_sampling_freq / 1e6
fpga_delta_freq_mhz = -adc_sampling_freq / 2 / fpga_num_freq / 1e6

# L0 parameters
l0_upchan_factor = 16
l0_num_frames_sample = 8 * 3

# Resulting output data parameters
num_channels = fpga_num_freq * l0_upchan_factor
channel_bandwidth_mhz = adc_sampling_freq / num_channels / 1e6
fpga_frequency_hz = adc_sampling_freq / fpga_num_samp_fft
sampling_time_ms = 1.0 / fpga_frequency_hz * l0_upchan_factor * l0_num_frames_sample

# Physical Telescope (possibly approx)
n_cylinder = 4
n_feed_per_cylinder = 256
n_pol_per_feed = 2
delta_y_feed_m = 0.3048
delta_x_cyl_m = 22.0
telescope_rotation_angle = -0.071  # degrees

# Copied from ch_util.ephemeris (actually pathfinder?)
chime_latitude_deg = 49.32  # degrees
chime_longitude_deg = -119.62  # degrees

# FPGA counts/s for injection snatcher
FPGA_COUNTS_PER_SECOND = 390625
