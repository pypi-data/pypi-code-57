import time

import autogalaxy as ag
import autogalaxy as ag

# Although we could test_autoarray the image without using an image (e.ag.lp. by just making a grid), we have chosen to
# set this test_autoarray up using an image and mask. This gives run-time numbers that can be easily related to an actual galaxy
# analysis

shape_2d = (301, 301)
pixel_scales = 0.05
sub_size = 4
radius = 3.0

print("sub grid size = " + str(sub_size))
print("circular mask radius = " + str(radius) + "\n")

mask = ag.Mask.circular(
    shape_2d=shape_2d, pixel_scales=pixel_scales, sub_size=sub_size, radius=radius
)

grid = ag.Grid.from_mask(mask=mask)

print("Number of grid points = " + str(grid.sub_shape_1d) + "\n")

### EllipticalGaussian ###

light_profile = ag.lp.EllipticalGaussian(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), sigma=1.0
)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalGaussian time = {}".format(diff))

### SphericalGaussian ###

light_profile = ag.lp.SphericalGaussian(centre=(0.0, 0.0), sigma=1.0)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("SphericalGaussian time = {}".format(diff))

### EllipticalExponential ###

profile = ag.lp.EllipticalExponential(
    centre=(0.0, 0.0),
    elliptical_comps=(0.111111, 0.0),
    intensity=1.0,
    effective_radius=1.0,
)

start = time.time()
profile.image_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalExponential time = {}".format(diff))

### SphericalExponential ###

profile = ag.lp.SphericalExponential(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0
)

start = time.time()
profile.image_from_grid(grid=grid)
diff = time.time() - start
print("SphericalExponential time = {}".format(diff))

### EllipticalDevVaucouleurs ###

profile = ag.lp.EllipticalDevVaucouleurs(
    centre=(0.0, 0.0),
    elliptical_comps=(0.111111, 0.0),
    intensity=1.0,
    effective_radius=1.0,
)

start = time.time()
profile.image_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalDevVaucouleurs time = {}".format(diff))

### SphericalDevVaucouleurs ###

profile = ag.lp.SphericalDevVaucouleurs(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0
)

start = time.time()
profile.image_from_grid(grid=grid)
diff = time.time() - start
print("SphericalDevVaucouleurs time = {}".format(diff))

### EllipticalSersic ###

light_profile = ag.lp.EllipticalSersic(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalSersic time = {}".format(diff))

### SphericalSersic ###

light_profile = ag.lp.SphericalSersic(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0, sersic_index=2.5
)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("SphericalSersic time = {}".format(diff))

### EllipticalCoreSersic ###

light_profile = ag.lp.EllipticalCoreSersic(
    centre=(0.0, 0.0),
    elliptical_comps=(0.0, 0.1),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    radius_break=0.01,
    intensity_break=0.05,
    gamma=0.25,
    alpha=3.0,
)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("EllipticalCoreSersic time = {}".format(diff))

### SphericalCoreSersic ###

light_profile = ag.lp.SphericalCoreSersic(
    centre=(0.0, 0.0),
    intensity=1.0,
    effective_radius=1.0,
    sersic_index=2.5,
    radius_break=0.01,
    intensity_break=0.05,
    gamma=0.25,
    alpha=3.0,
)

start = time.time()
light_profile.image_from_grid(grid=grid)
diff = time.time() - start
print("SphericalCoreSersic time = {}".format(diff))

print()
