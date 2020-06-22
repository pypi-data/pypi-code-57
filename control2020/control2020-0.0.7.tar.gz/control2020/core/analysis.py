import numpy as np
import sympy as sp
import control as ct
import math
from typing import Tuple, Union, List, Dict
from control2020 import core


def step_report(sys: Union[ct.TransferFunction, sp.Expr], output: bool = True) -> Dict[str, float]:
    """
    Return a step report from your system in a symbolic or polynomial form (TransferFunction or Symbolic)
    :param sys: your system
    :param output: If you want to print your output to stdout
    :return: a dict with props: RiseTime, SettlingTime, SettlingMin, SettlingMax, Overshoot, Undershoot, Peak, PeakTime, SteadyStateValue
    """
    if type(sys) is ct.TransferFunction:
        tf = sys
    else:
        tf = core.symbolic_transfer_function(sys)

    info = ct.step_info(tf)

    if output:
        print("Rise Time: %.3f" % info["RiseTime"])
        print("Settling Time: %.3f" % info["SettlingTime"])
        print("Settling Min: %.3f" % info["SettlingMin"])
        print("Settling Max: %.3f" % info["SettlingMax"])
        print("Overshoot: %.3f" % info["Overshoot"])
        print("Undershoot: %.3f" % info["Undershoot"])
        print("Peak: %.3f" % info["Peak"])
        print("Peak time: %.3f" % info["PeakTime"])
        print("Steady State Value: %.3f" % info["SteadyStateValue"])

    return info


def construct_poles(psi: float, wn: float) -> Tuple[complex, complex]:
    """
    Create two conjugated poles with the form: -psi*wn + 1j*wn*sqrt(1 - psi ** 2)
    :param psi: Your expected damping factor
    :param wn: Your expected natural frequency from your poles
    :return: a pair of complex (or not) poles
    """
    i_part = wn * math.sqrt(1 - psi ** 2)

    p1: complex = -psi * wn + 1j * i_part
    p2: complex = -psi * wn - 1j * i_part

    return p1, p2


def from_quality_to_psi_wn(po: float, ts: float) -> Tuple[float, float]:
    """
    Generate your damping and frequency from quality constraints: PO and Ts
    :param po: Percentage Overshoot
    :param ts: Time settling
    :return: psi, wn
    """
    po_log = math.log(po / 100) ** 2
    psi = math.sqrt(po_log / (np.pi ** 2 + po_log))
    wn = 4 / psi / ts

    return psi, wn


def gain_to_poles(g: sp.Expr, gain: float, k: sp.Expr = sp.var("K"), h: sp.Expr = 1, pole: int = -1) -> Union[List[complex], complex]:
    """
    Return poles from a gain value
    :param g: Your plant transfer function
    :param gain: Your gain value (K)
    :param k: Your gain (or compensator) transfer function
    :param h: Your feedback transfer function
    :param pole:
    :return:
    """
    equation = core.extract_characteristic_equation(k, g, h)

    s = sp.var("s")
    p = sp.Poly(sp.expand(equation.subs(sp.var("K"), gain)), s)

    num_polynomial = np.poly1d(p.all_coeffs())
    poles = list(np.roots(num_polynomial))

    if pole >= 0:
        if pole > len(poles):
            raise BaseException(f"invalid index of pole, you have only {len(poles)} poles")

        return poles[pole]

    return poles


def pole_to_psi_wn(pole: Union[complex, float]) -> Tuple[float, float]:
    """
    Convert a pole to quality params: psi and wn
    :param pole: Your pole
    :return: psi, wn
    """
    psi, wn = sp.var("psi w_n")

    pole = complex(pole)

    # p1 = psi*wn +/- j*wn*sqrt(1-psi^2)
    eq1 = sp.Eq(-psi * wn, pole.real)
    eq2 = sp.Eq(wn * sp.sqrt(1 - psi ** 2), pole.imag)

    result = sp.solve([eq1, eq2], (psi, wn))

    if len(result) < 2:
        psi_v, wn_v = result[0]
    else:
        psi_v, wn_v = result[1]

    return float(psi_v), float(wn_v)


def point_report(point: Union[complex, float], output: bool = True) -> Tuple[float, float, float]:
    """
    Return a basic report of a complex point in the Root Plane (Complex Plane)
    :param point: A complex point
    :param output: If you want to print the output to stdout
    :return: po, psi, wn
    """
    psi, wn = pole_to_psi_wn(point)
    po = 100 * np.exp(-psi * np.pi / np.sqrt(1 - psi ** 2))

    if output:
        print("Pole: %.3f + %.3fi" % (point.real, point.imag))
        print("Overshoot (%%): %.0f" % po)
        print("Damping: %.3f" % psi)
        print("Frequency (rad/s): %.3f" % wn)

    return po, psi, wn


