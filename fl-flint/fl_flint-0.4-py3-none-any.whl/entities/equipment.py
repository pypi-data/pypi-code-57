"""
Copyright (C) 2016, 2017, 2020 biqqles.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from . import Entity


class Equipment(Entity):
    # volume: float  # volume of one unit in ship's cargo bay
    pass


class Commodity(Equipment):
    decay_per_second: int


class Mountable(Equipment):
    mass: int


class ExternalMountable(Mountable):
    hit_pts: int


class Power(Mountable):
    capacity: int
    charge_rate: int
    thrust_capacity: int
    thrust_charge_rate: int


class Gun(Equipment):
    hit_pts: int
    mass: int
    power_usage: int
    muzzle_velocity: int


class Engine(Equipment):
    pass


class Thruster(Mountable):
    pass


class Munition(Equipment):
    pass
