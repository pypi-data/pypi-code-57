import time

import autogalaxy as ag

# Although we could test_autoarray the deflection angles without using an image (e.ag.mp. by just making a grid), we have chosen to
# set this test_autoarray up using an image and mask. This gives run-time numbers that can be easily related to an actual galaxy
# analysis

shape_2d = (301, 301)
pixel_scales = 0.05
sub_size = 4
radius = 4.0
pixel_scales_interp = 0.1

print("sub grid size = " + str(sub_size))
print("circular mask radius = " + str(radius) + "\n")


mask = ag.Mask.circular(
    shape_2d=shape_2d, pixel_scales=pixel_scales, sub_size=sub_size, radius=radius
)

grid = ag.GridInterpolate.from_mask(mask=mask, pixel_scales_interp=pixel_scales_interp)

print("Number of points = " + str(grid.sub_shape_1d) + "\n")
print("Interpolation Pixel Scale = " + str(pixel_scales_interp) + "\n")

### EllipticalIsothermal ###

mass_profile = ag.mp.EllipticalIsothermal(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.0
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalIsothermal time = {}".format(diff))

### SphericalIsothermal ###

mass_profile = ag.mp.SphericalIsothermal(centre=(0.0, 0.0), einstein_radius=1.0)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalIsothermal time = {}".format(diff))

### EllipticalPowerLaw (slope = 1.5) ###

mass_profile = ag.mp.EllipticalPowerLaw(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.0, slope=1.5
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalPowerLaw (slope = 1.5) time = {}".format(diff))

### SphericalPowerLaw (slope = 1.5) ###

mass_profile = ag.mp.SphericalPowerLaw(
    centre=(0.0, 0.0), einstein_radius=1.0, slope=1.5
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalPowerLaw (slope = 1.5) time = {}".format(diff))

### EllipticalPowerLaw (slope = 2.5) ###

mass_profile = ag.mp.EllipticalPowerLaw(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.0, slope=2.5
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalPowerLaw (slope = 2.5) time = {}".format(diff))

### SphericalPowerLaw (slope = 2.5) ###

mass_profile = ag.mp.SphericalPowerLaw(
    centre=(0.0, 0.0), einstein_radius=1.0, slope=2.5
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalPowerLaw (slope = 2.5) time = {}".format(diff))

### EllipticalCoredPowerLaw ###

mass_profile = ag.mp.EllipticalCoredPowerLaw(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    einstein_radius=1.0,
    slope=2.0,
    core_radius=0.1,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalCoredPowerLaw time = {}".format(diff))

### SphericalCoredPowerLaw ###

mass_profile = ag.mp.SphericalCoredPowerLaw(
    centre=(0.0, 0.0), einstein_radius=1.0, slope=2.0, core_radius=0.1
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalCoredPowerLaw time = {}".format(diff))

### EllipticalGeneralizedNFW (inner_slope = 0.5) ###

# mass_profile = ag.mp.EllipticalGeneralizedNFW(centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), kappa_s=0.1,
#                                            scale_radius=10.0, inner_slope=0.5)
#
# start = time.time()
# mass_profile.deflections_from_grid(grid=grid)
# diff = time.time() - start
# print("EllipticalGeneralizedNFW (inner_slope = 1.0) time = {}".format(diff))

### SphericalGeneralizedNFW (inner_slope = 0.5) ###

mass_profile = ag.mp.SphericalGeneralizedNFW(
    centre=(0.0, 0.0), kappa_s=0.1, scale_radius=10.0, inner_slope=0.5
)

# start = time.time()
# mass_profile.deflections_from_grid(grid=grid)
# diff = time.time() - start
# print("SphericalGeneralizedNFW (inner_slope = 1.0) time = {}".format(diff))

### EllipticalNFW ###

mass_profile = ag.mp.EllipticalNFW(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), kappa_s=0.1, scale_radius=10.0
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalNFW time = {}".format(diff))

### SphericalNFW ###

mass_profile = ag.mp.SphericalNFW(centre=(0.0, 0.0), kappa_s=0.1, scale_radius=10.0)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalNFW time = {}".format(diff))

### SphericalNFW ###

mass_profile = ag.mp.SphericalTruncatedNFW(
    centre=(0.0, 0.0), kappa_s=0.1, scale_radius=10.0, truncation_radius=5.0
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalTruncatedNFW time = {}".format(diff))

### EllipticalExponential ###

profile = ag.mp.EllipticalExponential(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    mass_to_light_ratio=1.0,
)

start = time.time()
profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalExponential time = {}".format(diff))

### SphericalExponential ###

profile = ag.mp.SphericalExponential(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0, mass_to_light_ratio=1.0
)

start = time.time()
profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalExponential time = {}".format(diff))

### EllipticalDevVaucouleurs ###

profile = ag.mp.EllipticalDevVaucouleurs(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    mass_to_light_ratio=1.0,
)

start = time.time()
profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalDevVaucouleurs time = {}".format(diff))

### SphericalDevVaucouleurs ###

profile = ag.mp.SphericalDevVaucouleurs(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0, mass_to_light_ratio=1.0
)

start = time.time()
profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalDevVaucouleurs time = {}".format(diff))

### EllipticalSersic ###

mass_profile = ag.mp.EllipticalSersic(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalSersic time = {}".format(diff))

### SphericalSersic ###

mass_profile = ag.mp.SphericalSersic(
    centre=(0.0, 0.0),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalSersic time = {}".format(diff))

### EllipticalSersicRadialGradient (gradient = -1.0) ###

mass_profile = ag.mp.EllipticalSersicRadialGradient(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
    mass_to_light_gradient=-1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalSersicRadialGradient (gradient = -1.0) time = {}".format(diff))

### SphericalersicRadialGradient (gradient = -1.0) ###

mass_profile = ag.mp.SphericalSersicRadialGradient(
    centre=(0.0, 0.0),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
    mass_to_light_gradient=-1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalSersicRadialGradient (gradient = -1.0) time = {}".format(diff))

### EllipticalSersicRadialGradient (gradient = 1.0) ###

mass_profile = ag.mp.EllipticalSersicRadialGradient(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
    mass_to_light_gradient=1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalSersicRadialGradient (gradient = 1.0) time = {}".format(diff))

### SphericalersicRadialGradient (gradient = 1.0) ###

mass_profile = ag.mp.SphericalSersicRadialGradient(
    centre=(0.0, 0.0),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    mass_to_light_ratio=1.0,
    mass_to_light_gradient=1.0,
)

start = time.time()
mass_profile.deflections_from_grid(grid=grid)
diff = time.time() - start
print("SphericalSersicRadialGradient (gradient = 1.0) time = {}".format(diff))

print()
