import os

import autofit as af
import autolens as al
from test_autolens.simulate.imaging import simulate_util

# Get the relative path to the config files and output folder in our autolens_workspace.
test_path = "{}/../".format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output papth
conf.instance = conf.Config(
    config_path=test_path + "config", output_path=test_path + "output"
)

# It is convenient to specify the lens name as a string, so that if the pipeline is applied to multiple images we \
# don't have to change all of the path entries in the function below.
data_name = "no_lens_source_smooth"
instrument = "euclid"

# Setup the size of the sub-grid and mask used for this precision analysis.
sub_size = 2
inner_radius = 0.0
outer_radius = 3.0

# The pixel scale of the interpolation grid, where a smaller pixel scale gives a higher resolution grid and therefore
# more precise interpolation of the sub-grid deflection angles.
pixel_scales_interp = 0.2

imaging = simulate_util.load_test_imaging(
    data_name=data_name, instrument=instrument, psf_shape_2d=(21, 21)
)

# The phase is passed the mask we setup below using the radii specified above.
mask = al.Mask.circular_annular(
    shape=imaging.shape_2d,
    pixel_scales=imaging.pixel_scales,
    inner_radius=inner_radius,
    outer_radius=outer_radius,
)

# Plot the imaging data and mask.
aplt.Imaging.subplot_imaging(imaging=imaging, mask=mask)

# To perform the analysis, we set up a phase using the 'phase' module (imported as 'ph').
# A phase takes our galaxy models and fits their parameters using a non-linear search (in this case, MultiNest).
phase = al.PhaseImaging(
    phase_name="phase_interp",
    folders=[data_name, instrument + "_" + str(pixel_scales_interp)],
    galaxies=dict(lens=al.GalaxyModel(mass=al.EllipticalPowerLaw)),
    galaxies=dict(source=al.GalaxyModel(light=al.lp.EllipticalSersic)),
    search=af.DynestyStatic(),
    pixel_scales_interp=pixel_scales_interp,
)

phase.search.const_efficiency_mode = True
phase.search.n_live_points = 50
phase.search.facc = 0.5

# We run the phase on the image, print the results and plotters the fit.
result = phase.run(dataset=imaging, mask=mask)
