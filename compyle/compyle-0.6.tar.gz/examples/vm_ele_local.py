"""Shows the use of an elementwise operation with the use of local memory but
this memory cannot be passed by the user so has to be allocated by the user in
their code.

This does illustrate how a user can write a lot more sophisticated code on the
GPU using local memory. Note though that this code is obviously only sensible
on the opencl/cuda backends and not on the Cython backend and will not work on
Cython.

"""
import numpy as np
from math import pi
import time

from pysph.cpy.config import get_config
from pysph.cpy.api import declare, annotate
from pysph.cpy.parallel import (Elementwise, LID_0, LDIM_0, GDIM_0,
                                local_barrier)
from pysph.cpy.array import wrap


@annotate(double='xi, yi, xj, yj, gamma', result='doublep')
def point_vortex(xi, yi, xj, yj, gamma, result):
    xij = xi - xj
    yij = yi - yj
    r2ij = xij*xij + yij*yij
    if r2ij < 1e-14:
        result[0] = 0.0
        result[1] = 0.0
    else:
        tmp = gamma/(2.0*pi*r2ij)
        result[0] = -tmp*yij
        result[1] = tmp*xij


@annotate(nv='int', i='int', doublep='x, y, gamma, u, v')
def velocity(i, x, y, gamma, u, v, nv):
    nb = declare('int')
    j, ti, nt, jb = declare('int', 4)
    ti = LID_0
    nt = LDIM_0
    idx = declare('int')
    tmp = declare('matrix(2)')
    uj, vj = declare('double', 2)
    xc = declare('LOCAL_MEM matrix(128)')
    yc = declare('LOCAL_MEM matrix(128)')
    gc = declare('LOCAL_MEM matrix(128)')
    nb = GDIM_0

    if i < nv:
        xi = x[i]
        yi = y[i]
    uj = 0.0
    vj = 0.0
    for jb in range(nb):
        idx = jb*nt + ti
        if idx < nv:
            xc[ti] = x[idx]
            yc[ti] = y[idx]
            gc[ti] = gamma[idx]
        else:
            gc[ti] = 0.0
        local_barrier()

        if i < nv:
            for j in range(nt):
                point_vortex(xi, yi, xc[j], yc[j], gc[j], tmp)
                uj += tmp[0]
                vj += tmp[1]

        local_barrier()

    if i < nv:
        u[i] = uj
        v[i] = vj


def make_vortices(nv, backend):
    x = np.linspace(-1, 1, nv)
    y = x.copy()
    gamma = np.ones(nv)
    u = np.zeros_like(x)
    v = np.zeros_like(x)
    x, y, gamma, u, v = wrap(x, y, gamma, u, v, backend=backend)
    return x, y, gamma, u, v, nv


def run(nv, backend):
    e = Elementwise(velocity, backend=backend)
    args = make_vortices(nv, backend)
    t1 = time.time()
    gs = ((nv + 128 - 1)//128)*128
    print(gs)
    e(*args, range=slice(gs))
    print(time.time() - t1)
    u = args[-3]
    u.pull()
    print(u.data)
    return e, args


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument(
        '-b', '--backend', action='store', dest='backend',
        default='opencl', help='Choose the backend.'
    )
    p.add_argument(
        '--use-double', action='store_true', dest='use_double',
        default=False,  help='Use double precision on the GPU.'
    )
    p.add_argument('-n', action='store', type=int, dest='n',
                   default=10000, help='Number of particles.')
    o = p.parse_args()
    get_config().use_double = o.use_double
    assert o.backend in ['opencl'], "Only OpenCL backend is supported."
    run(o.n, o.backend)
