import pyFC
import matplotlib.pyplot as pl

kmin = 20
nx = 512
ny = 512
nz = 512
sigma = 30
do_density = True
do_velocity = True


if do_density:
    cube = pyFC.LogNormalFractalCube(nx, ny, nz, kmin=kmin)
    cube.gen_cube()
    cube.write_cube(fname='density.flt', prec='single')

    pyFC.plot_field_stats(cube, 'log')
    pl.gcf().savefig('lnfc_stats.png', dpi=300, bbox_inches='tight')

if do_velocity:
    for i in range(3):
        cube = pyFC.GaussianFractalCube(nx, ny, nz, kmin=kmin, mean=0, sigma=sigma)
        cube.gen_cube()
        cube.write_cube(fname=f'velocity{i+1}.flt', prec='single')
