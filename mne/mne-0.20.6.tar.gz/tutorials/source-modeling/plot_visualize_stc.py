"""
.. _tut_viz_stcs:

Visualize source time courses
=============================

This tutorial focuses on visualization of stcs.

.. contents:: Table of Contents
   :local:

Surface Source Estimates
------------------------
First, we get the paths for the evoked data and the time courses (stcs).
"""

import os

import mne
from mne.datasets import sample
from mne.minimum_norm import apply_inverse, read_inverse_operator
from mne import read_evokeds

data_path = sample.data_path()
sample_dir = os.path.join(data_path, 'MEG', 'sample')
subjects_dir = os.path.join(data_path, 'subjects')

fname_evoked = data_path + '/MEG/sample/sample_audvis-ave.fif'
fname_stc = os.path.join(sample_dir, 'sample_audvis-meg')

###############################################################################
# Then, we read the stc from file
stc = mne.read_source_estimate(fname_stc, subject='sample')

###############################################################################
# This is a :class:`SourceEstimate <mne.SourceEstimate>` object
print(stc)

###############################################################################
# The SourceEstimate object is in fact a *surface* source estimate. MNE also
# supports volume-based source estimates but more on that later.
#
# We can plot the source estimate using the
# :func:`stc.plot <mne.SourceEstimate.plot>` just as in other MNE
# objects. Note that for this visualization to work, you must have ``mayavi``
# and ``pysurfer`` installed on your machine.
initial_time = 0.1
brain = stc.plot(subjects_dir=subjects_dir, initial_time=initial_time,
                 clim=dict(kind='value', pos_lims=[3, 6, 9]),
                 time_viewer=True)

###############################################################################
#
# Note that here we used ``initial_time=0.1``, but we can also browse through
# time using ``time_viewer=True``.
#
# In case ``mayavi`` is not available, we also offer a ``matplotlib``
# backend. Here we use verbose='error' to ignore a warning that not all
# vertices were used in plotting.
mpl_fig = stc.plot(subjects_dir=subjects_dir, initial_time=initial_time,
                   backend='matplotlib', verbose='error')

###############################################################################
#
# Volume Source Estimates
# -----------------------
# We can also visualize volume source estimates (used for deep structures).
#
# Let us load the sensor-level evoked data. We select the MEG channels
# to keep things simple.
evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
evoked.pick_types(meg=True, eeg=False)

###############################################################################
# Then, we can load the precomputed inverse operator from a file.
fname_inv = data_path + '/MEG/sample/sample_audvis-meg-vol-7-meg-inv.fif'
inv = read_inverse_operator(fname_inv)
src = inv['src']

###############################################################################
# The source estimate is computed using the inverse operator and the
# sensor-space data.
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
stc = apply_inverse(evoked, inv, lambda2, method)
stc.crop(0.0, 0.2)

###############################################################################
# This time, we have a different container
# (:class:`VolSourceEstimate <mne.VolSourceEstimate>`) for the source time
# course.
print(stc)

###############################################################################
# This too comes with a convenient plot method.
stc.plot(src, subject='sample', subjects_dir=subjects_dir)

###############################################################################
# For this visualization, ``nilearn`` must be installed.
# This visualization is interactive. Click on any of the anatomical slices
# to explore the time series. Clicking on any time point will bring up the
# corresponding anatomical map.
#
# We could visualize the source estimate on a glass brain. Unlike the previous
# visualization, a glass brain does not show us one slice but what we would
# see if the brain was transparent like glass.
stc.plot(src, subject='sample', subjects_dir=subjects_dir, mode='glass_brain')

###############################################################################
# Vector Source Estimates
# -----------------------
# If we choose to use ``pick_ori='vector'`` in
# :func:`apply_inverse <mne.minimum_norm.apply_inverse>`
fname_inv = data_path + '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'

inv = read_inverse_operator(fname_inv)
stc = apply_inverse(evoked, inv, lambda2, 'dSPM', pick_ori='vector')
stc.plot(subject='sample', subjects_dir=subjects_dir,
         initial_time=initial_time)

###############################################################################
# Dipole fits
# -----------
# For computing a dipole fit, we need to load the noise covariance, the BEM
# solution, and the coregistration transformation files. Note that for the
# other methods, these were already used to generate the inverse operator.
fname_cov = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-cov.fif')
fname_bem = os.path.join(subjects_dir, 'sample', 'bem',
                         'sample-5120-bem-sol.fif')
fname_trans = os.path.join(data_path, 'MEG', 'sample',
                           'sample_audvis_raw-trans.fif')

##############################################################################
# Dipoles are fit independently for each time point, so let us crop our time
# series to visualize the dipole fit for the time point of interest.
evoked.crop(0.1, 0.1)
dip = mne.fit_dipole(evoked, fname_cov, fname_bem, fname_trans)[0]

##############################################################################
# Finally, we can visualize the dipole.
dip.plot_locations(fname_trans, 'sample', subjects_dir)
