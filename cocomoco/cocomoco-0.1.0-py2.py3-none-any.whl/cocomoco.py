#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import collections

from dataclasses import dataclass
from typing import Iterator
from typing import List
from typing import Dict
from typing import Optional


class CocomocoError(Exception): pass
class CocomocoRangeError(Exception): CocomocoError
class CocomocoModelUnknownError(Exception): CocomocoError

_CorrectiveFactors = collections.namedtuple('CorrectiveFactors', 'very_low low nominal high very_high extra_high')
_CorrectiveFactorsRely = _CorrectiveFactors(0.75, 0.88, 1.0, 1.15, 1.40, None)
_CorrectiveFactorsData = _CorrectiveFactors(None, 0.94, 1.0, 1.08, 1.16, None)
_CorrectiveFactorsCplx = _CorrectiveFactors(0.70, 0.85, 1.0, 1.15, 1.30, 1.65)
_CorrectiveFactorsTime = _CorrectiveFactors(None, None, 1.0, 1.11, 1.30, 1.66)
_CorrectiveFactorsStor = _CorrectiveFactors(None, None, 1.0, 1.06, 1.21, 1.56)
_CorrectiveFactorsVirt = _CorrectiveFactors(None, 0.87, 1.0, 1.15, 1.30, None)
_CorrectiveFactorsTurn = _CorrectiveFactors(None, 0.87, 1.0, 1.07, 1.15, None)
_CorrectiveFactorsAcap = _CorrectiveFactors(1.46, 1.19, 1.0, 0.86, 0.71, None)
_CorrectiveFactorsAexp = _CorrectiveFactors(1.29, 1.13, 1.0, 0.91, 0.82, None)
_CorrectiveFactorsPcap = _CorrectiveFactors(1.42, 1.17, 1.0, 0.86, 0.70, None)
_CorrectiveFactorsVexp = _CorrectiveFactors(1.21, 1.10, 1.0, 0.90, None, None)
_CorrectiveFactorsLexp = _CorrectiveFactors(1.14, 1.07, 1.0, 0.95, None, None)
_CorrectiveFactorsModp = _CorrectiveFactors(1.24, 1.10, 1.0, 0.91, 0.82, None)
_CorrectiveFactorsTool = _CorrectiveFactors(1.24, 1.10, 1.0, 0.91, 0.83, None)
_CorrectiveFactorsSced = _CorrectiveFactors(1.23, 1.08, 1.0, 1.04, 1.10, None)

@dataclass
class _Model:
    """Base Model

    All models inheriet from this model. It values relfect the organic one.
    """
    name: str = 'undefined'
    effort: float = 2.4
    effort_exponent: float = 1.05
    schedule: float = 2.5
    schedule_exponent: float = 0.38


@dataclass
class Organic(_Model):
    """Organic Model

    Relatively small software teams develop software in a highly familiar,
    in-house environment.  It has a generally stable development environment,
    minimal need for innovative algorithms, and requirements can be relaxed to
    avoid extensive rework.
    """
    name: str = 'Organic'

@dataclass
class Semidetached(_Model):
    """Semidetached Model

    This is an intermediate step between organic and embedded. This is
    generally characterized by reduced flexibility in the requirements.
    """
    name: str = 'Semidetached'
    effort: float = 3.0
    effort_exponent: float = 1.12
    schedule_exponent: float = 0.35

@dataclass
class Embedded(_Model):
    """Embedded Model

    The project must operate within tight (hard-to-meet) constraints, and
    requirements and interface specifications are often non-negotiable. The
    software will be embedded in a complex environment that the software must
    deal with as-is.
    """
    name: str = 'Embedded'
    effort: float = 3.6
    effort_exponent: float = 1.2
    schedule_exponent: float = 0.32


@dataclass
class IntermediateOrganic(_Model):
    name: str = 'Intermediate Organic'
    effort: float = 2.3
    effort_exponent: float = 1.05
    schedule_exponent: float = 0.38

@dataclass
class IntermediateSemidetached(_Model):
    name: str = 'Intermediate Semidetached'
    effort: float = 2.3
    effort: float = 3.0
    effort_exponent: float = 1.12
    schedule_exponent: float = 0.35

@dataclass
class IntermediateEmbedded(_Model):
    name: str = 'Intermediate Embedded'
    effort: float = 2.3
    effort: float = 2.8
    effort_exponent: float = 1.2
    schedule_exponent: float = 0.32


class CocomocoMetric:

    def __init__(self, salary=100000.0):
        self.set_salary(salary)
        self.sloc = None
        self.effort = None
        # time to develop
        self.dtime = None
        self.staff = None
        self.model_name = None
        self.sloc_per_staff_month = None

    @property
    def cost(self):
        if not self.effort:
            return 0.0
        return (self.effort / 12.0) * self.salary

    def set_salary(self, new_salary):
        if new_salary <= 0:
            raise CocomocoRangeError("salary must be larger than 0")
        self.salary = new_salary

    def __str__(self):
        msg  = f'effort:{self.effort:.1f} person-months ({self.effort/12.0:.1f} person-years),'
        msg += f' dtime:{self.dtime:.1f} month, staff:{self.staff:.1f} costs:{self.cost:.2f}'
        msg += f' productivity:{self.sloc_per_staff_month:.0f} sloc_per_staff_month'
        msg += f' model:{self.model_name}'
        return msg


def model_by_name(modelname: str):
    if modelname.lower() == 'organic':
        return Organic()
    elif modelname.lower() == 'semidetached':
        return Semidetached()
    elif modelname.lower() == 'embedded':
        return Embedded()
    else:
        raise CocomocoModelUnknownError(f'unknown model: {modelname}')


def calculate(sloc: int, model=Organic()):
    if sloc <= 0:
        raise CocomocoRangeError("sloc must be larger than 0")
    cm = CocomocoMetric()
    cm.sloc = sloc
    cm.model_name = model.name
    cm.effort = model.effort * math.pow(sloc / 1000.0, model.effort_exponent)
    cm.dtime = model.schedule * math.pow(cm.effort, model.schedule_exponent)
    cm.staff = cm.effort / cm.dtime
    cm.sloc_per_staff_month = sloc / cm.effort
    return cm
