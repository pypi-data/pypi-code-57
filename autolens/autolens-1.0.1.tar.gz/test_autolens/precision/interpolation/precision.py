import numpy as np
from autolens.plot import plotters

# Although we could test_autoarray the deflection angles without using an image (e.al. by just making a grid), we have chosen to
# set this test_autoarray up using an image and mask. This gives run-time numbers that can be easily related to an actual lens
# analysis

sub_size = 2
inner_radius = 0.2
outer_radius = 4.0

print("sub grid size = " + str(sub_size))
print("annular inner mask radius = " + str(inner_radius) + "\n")
print("annular outer mask radius = " + str(outer_radius) + "\n")

for instrument in ["hst_up"]:

    print()

    imaging = simulate_util.load_test_imaging(
        data_name="lens_sie__source_smooth", instrument=instrument, psf_shape_2d=(3, 3)
    )
    mask = al.Mask.circular_annular(
        shape=imaging.shape_2d,
        pixel_scales=imaging.pixel_scales,
        inner_radius=inner_radius,
        outer_radius=outer_radius,
    )
    masked_imaging = al.MaskedImaging(imaging=imaging, mask=mask, sub_size=sub_size)

    print("Deflection angle run times for image type " + instrument + "\n")
    print("Number of points = " + str(masked_imaging.grid.sub_shape_1d) + "\n")

    interpolator = al.GridInterpolate.from_mask_grid_and_pixel_scales_interps(
        mask=masked_imaging.mask, grid=masked_imaging.grid, pixel_scales_interp=0.05
    )

    print(
        "Number of interpolation points = "
        + str(interpolator.grid_interp.sub_shape_1d)
        + "\n"
    )

    ### EllipticalIsothermal ###

    mass_profile = al.EllipticalIsothermal(
        centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.0
    )

    interp_deflections = mass_profile.deflections_from_grid(
        grid=interpolator.grid_interp
    )
    deflections = np.zeros((masked_imaging.grid.sub_shape_1d, 2))
    deflections[:, 0] = interpolator.interpolated_array_from_array_interp(
        array_interp=interp_deflections[:, 0]
    )
    deflections[:, 1] = interpolator.interpolated_array_from_array_interp(
        array_interp=interp_deflections[:, 1]
    )

    true_deflections = mass_profile.deflections_from_grid(grid=masked_imaging.grid)

    true_deflections_y_2d = masked_imaging.grid.array_stored_1d_from_sub_array_1d(
        sub_array_1d=true_deflections[:, 0]
    )
    true_deflections_x_2d = masked_imaging.grid.array_stored_1d_from_sub_array_1d(
        sub_array_1d=true_deflections[:, 1]
    )

    difference_y = deflections[:, 0] - true_deflections[:, 0]
    difference_x = deflections[:, 1] - true_deflections[:, 1]

    print("interpolation y error: ", np.mean(difference_y))
    print("interpolation y uncertainty: ", np.std(difference_y))
    print("interpolation y max error: ", np.max(difference_y))
    print("interpolation x error: ", np.mean(difference_x))
    print("interpolation x uncertainty: ", np.std(difference_x))
    print("interpolation x max error: ", np.max(difference_x))

    difference_y_2d = masked_imaging.grid.array_stored_1d_from_sub_array_1d(
        sub_array_1d=difference_y
    )
    difference_x_2d = masked_imaging.grid.array_stored_1d_from_sub_array_1d(
        sub_array_1d=difference_x
    )

    aplt.Array(array=true_deflections_y_2d)
    aplt.Array(array=difference_y_2d)

    aplt.Array(array=true_deflections_x_2d)
    aplt.Array(array=difference_x_2d)

    # difference_percent_y = (np.abs(difference_y) / np.abs(true_deflections[:,0]))*100.0
    # difference_percent_x = (np.abs(difference_x) / np.abs(true_deflections[:,1]))*100.0
    #
    # print("interpolation y mean percent difference: ", np.mean(difference_percent_y))
    # print("interpolation y std percent difference: ", np.std(difference_percent_y))
    # print("interpolation y max percent difference: ", np.max(difference_percent_y))
    # print("interpolation x mean percent difference: ", np.mean(difference_percent_x))
    # print("interpolation x std percent difference: ", np.std(difference_percent_x))
    # print("interpolation x mean percent difference: ", np.max(difference_percent_x))
    #
    # difference_percent_y_2d = masked_imaging.grid.scaled_array_2d_with_sub_dimensions_from_sub_array_1d(
    #     sub_array_1d=difference_percent_y)
    # difference_percent_x_2d = masked_imaging.grid.scaled_array_2d_with_sub_dimensions_from_sub_array_1d(
    #     sub_array_1d=difference_percent_x)
    #
    # aplt.Array(arrays=difference_percent_y_2d)
    # aplt.Array(arrays=difference_percent_x_2d)
