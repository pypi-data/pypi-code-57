#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from chime_frb_constants.frange import _frange

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

###############################################################################
#   D I S P E R S I O N   M E A S U R E   C O N S T A N T
###############################################################################

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
K_DM = 1.0 / 2.41e-4


###############################################################################
#   C H I M E   I N S T R U M E N T A L   C O N S T A N T S
###############################################################################

# Sampling frequency, in Hz.
ADC_SAMPLING_FREQ = float(800e6)

# Number of samples in the inital FFT in the F-engine.
FPGA_NUM_SAMP_FFT = 2048

# f-engine parameters for alias sampling in second Nyquist zone.
FPGA_NUM_FREQ = FPGA_NUM_SAMP_FFT // 2
FPGA_FREQ0_MHZ = ADC_SAMPLING_FREQ / 1e6
FPGA_DELTA_FREQ_MHZ = -ADC_SAMPLING_FREQ / 2 / FPGA_NUM_FREQ / 1e6

# top of the highest-frequency channel
# (NB the FGPA-channel around 800 MHz is contaminated by aliasing)
FREQ_TOP_MHZ = FPGA_FREQ0_MHZ - FPGA_DELTA_FREQ_MHZ / 2.0
# bottom of the lowest-frequency channel
FREQ_BOTTOM_MHZ = FREQ_TOP_MHZ - ADC_SAMPLING_FREQ / 2.0 / 1e6
# # # bin centres of FPGA channels, in MHz (ordered 800 to 400 MHz)
FPGA_FREQ = list(_frange(FPGA_FREQ0_MHZ, FPGA_FREQ0_MHZ / 2.0, FPGA_DELTA_FREQ_MHZ))

# L0 parameters
L0_UPCHAN_FACTOR = 16
L0_NUM_FRAMES_SAMPLE = 8 * 3

# Resulting output data parameters
NUM_CHANNELS = FPGA_NUM_FREQ * L0_UPCHAN_FACTOR
CHANNEL_BANDWIDTH_MHZ = ADC_SAMPLING_FREQ / NUM_CHANNELS / NUM_CHANNELS
FPGA_FREQUENCY_HZ = ADC_SAMPLING_FREQ / FPGA_NUM_SAMP_FFT
SAMPLING_TIME_S = 1.0 / FPGA_FREQUENCY_HZ * L0_UPCHAN_FACTOR * L0_NUM_FRAMES_SAMPLE
SAMPLING_TIME_MS = SAMPLING_TIME_S * 1e3

FPGA_COUNTS_PER_SAMPLE = int(SAMPLING_TIME_S / 1e3 / (1.0 / FPGA_FREQUENCY_HZ))

# Bin centres of L0 channels, in MHz (ordered 400 to 800 MHz)
FREQ = list(
    _frange(
        FREQ_BOTTOM_MHZ + CHANNEL_BANDWIDTH_MHZ / 2.0,
        FREQ_TOP_MHZ + 1,
        CHANNEL_BANDWIDTH_MHZ,
    )
)

# Physical Telescope (possibly approx)
N_CYLINDER = 4
N_FEED_PER_CYLINDER = 256
N_POL_PER_FEED = 2
DELTA_Y_FEED_M = 0.3048
DELTA_X_CYL_M = 22.0
TELESCOPE_ROTATION_ANGLE = -0.071  # degrees

# Copied from ch_util.ephemeris (actually pathfinder?)
CHIME_LATITUDE_DEG = 49.32  # degrees
CHIME_LONGITUDE_DEG = -119.62  # degrees

# FPGA counts/s for injection snatcher
FPGA_COUNTS_PER_SECOND = 390625
