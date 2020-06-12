#!/usr/bin/env python3
from caproto.server import (pvproperty, PVGroup, SubGroup,
                            ioc_arg_parser, run)
import numpy as np
import time
import functools
import math
import contextvars

internal_process = contextvars.ContextVar('internal_process',
                                          default=False)


def no_reentry(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        if internal_process.get():
            return
        try:
            internal_process.set(True)
            return (await func(*args, **kwargs))
        finally:
            internal_process.set(False)

    return inner


def _arrayify(func):
    @functools.wraps(func)
    def inner(*args):
        return func(*(np.asarray(a) for a in args))
    return inner


class _JitterDetector(PVGroup):
    det = pvproperty(value=0, dtype=float, read_only=True)

    @det.getter
    async def det(self, instance):
        return (await self._read(instance))

    mtr = pvproperty(value=0, dtype=float, precision=3, record='ai')
    exp = pvproperty(value=1, dtype=float)
    vel = pvproperty(value=1, dtype=float)

    mtr_tick_rate = pvproperty(value=10, dtype=float, units='Hz')

    @exp.putter
    async def exp(self, instance, value):
        value = np.clip(value, a_min=0, a_max=None)
        return value

    @mtr.startup
    async def mtr(self, instance, async_lib):
        instance.ev = async_lib.library.Event()
        instance.async_lib = async_lib

    @mtr.putter
    @no_reentry
    async def mtr(self, instance, value):
        # "tick" at 10Hz
        dwell = 1 / self.mtr_tick_rate.value

        disp = (value - instance.value)
        # compute the total movement time based an velocity
        total_time = abs(disp / self.vel.value)
        # compute how many steps, should come up short as there will
        # be a final write of the return value outside of this call
        N = int(total_time // dwell)

        for j in range(N):
            # hide a possible divide by 0
            step_size = disp / N
            await instance.write(instance.value + step_size)
            await instance.async_lib.library.sleep(dwell)

        return value


class PinHole(_JitterDetector):
    async def _read(self, instance):
        sigma = 5
        center = 0
        c = - 1 / (2 * sigma * sigma)

        @_arrayify
        def jitter_read(m, e, intensity):
            N = (self.parent.N_per_I_per_s * intensity * e *
                 np.exp(c * (m - center)**2))
            return np.random.poisson(N)

        return jitter_read(self.mtr.value,
                           self.exp.value,
                           self.parent.current.value)


class Edge(_JitterDetector):
    async def _read(self, instance):
        sigma = 2.5
        center = 5
        c = 1 / sigma

        @_arrayify
        def jitter_read(m, e, intensity):
            s = math.erfc(c * (-m + center)) / 2
            N = (self.parent.N_per_I_per_s * intensity * e * s)
            return np.random.poisson(N)

        return jitter_read(self.mtr.value,
                           self.exp.value,
                           self.parent.current.value)


class Slit(_JitterDetector):
    async def _read(self, instance):
        sigma = 2.5
        center = 7.5
        c = 1 / sigma

        @_arrayify
        def jitter_read(m, e, intensity):
            s = (math.erfc(c * (m - center)) -
                 math.erfc(c * (m + center))) / 2

            N = (self.parent.N_per_I_per_s * intensity * e * s)
            return np.random.poisson(N)

        return jitter_read(self.mtr.value,
                           self.exp.value,
                           self.parent.current.value)


class MovingDot(PVGroup):
    N = 480
    M = 640

    sigmax = 50
    sigmay = 25

    background = 1000

    Xcen = Ycen = 0

    det = pvproperty(value=[0] * N * M,
                     dtype=float,
                     read_only=True)

    @det.getter
    async def det(self, instance):
        N = self.N
        M = self.M
        back = np.random.poisson(self.background, (N, M))
        if not self.shutter_open.value:
            await self.img_sum.write([back.sum()])
            return back.ravel()
        x = self.mtrx.value
        y = self.mtry.value

        Y, X = np.ogrid[:N, :M]

        X = X - M / 2 + x
        Y = Y - N / 2 + y

        X /= self.sigmax
        Y /= self.sigmay

        dot = np.exp(-(X**2 + Y**2) / 2) * np.exp(- (x**2 + y**2) / 100**2)

        I = self.parent.current.value  # noqa
        e = self.exp.value
        measured = (self.parent.N_per_I_per_s * dot * e * I)
        ret = (back + np.random.poisson(measured))
        await self.img_sum.write([ret.sum()])
        return ret.ravel()

    img_sum = pvproperty(value=0, read_only=True, dtype=float)
    mtrx = pvproperty(value=0, dtype=float)
    mtry = pvproperty(value=0, dtype=float)

    exp = pvproperty(value=1, dtype=float)

    @exp.putter
    async def exp(self, instance, value):
        value = np.clip(value, a_min=0, a_max=None)
        return value

    shutter_open = pvproperty(value=1, dtype=int)

    ArraySizeY_RBV = pvproperty(value=N, dtype=int,
                                read_only=True)
    ArraySizeX_RBV = pvproperty(value=M, dtype=int,
                                read_only=True)
    ArraySize_RBV = pvproperty(value=[N, M], dtype=int,
                               read_only=True)


class MiniBeamline(PVGroup):
    """
    A collection of detectors coupled to motors and an oscillating beam current
    """

    N_per_I_per_s = 200

    current = pvproperty(value=500, dtype=float, read_only=True)

    @current.scan(period=0.1)
    async def current(self, instance, async_lib):
        current = 500 + 25 * np.sin(time.monotonic() * (2 * np.pi) / 4)
        await instance.write(value=current)

    ph = SubGroup(PinHole)
    edge = SubGroup(Edge)
    slit = SubGroup(Slit)

    dot = SubGroup(MovingDot)


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='mini:',
        desc=('An IOC that provides a simulated pinhole, edge and slit '
              'with coupled with a shared global current that oscillates '
              'in time.'))

    ioc = MiniBeamline(**ioc_options)
    run(ioc.pvdb, **run_options)
