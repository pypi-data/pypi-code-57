import control as ct
import numpy as np
import sympy as sp
from control2020 import core
from typing import Union


def pid_with_root_placing(g: Union[sp.Expr, ct.TransferFunction],
                          po: float, ts: float, report: bool = False) -> ct.TransferFunction:
    """
    Function to create a PID controller based on root locus method,
    the controller is the form: Kc*(s+b)^2/s equivalent to Kp + Ki/s + Kd*s
    ---
    design params example
    ts = 11.5  # 11.5 seg
    po = 0.5  # 0.5%
    :param g: Your plant transfer function
    :param po: Percentage Overshoot
    :param ts: Time Settling
    :param report: If you want to print a report step by step
    :return: a TransferFunction controller
    """
    s = sp.var("s")

    if isinstance(g, ct.TransferFunction):
        sys = g
    else:
        sys = core.symbolic_transfer_function(g)

    psi, wn = core.from_quality_to_psi_wn(po, ts)
    if report:
        print("psi=%.2f | wn=%.2f\n" % (psi, wn))

    pds = core.construct_poles(psi, wn)

    pd = pds[0]  # util pole in the (Re-, Im+) plane
    if report:
        print("desired pole: %.2f + %.2fi" % (pd.real, pd.imag))

    # finding b with the angle condition
    poles_angles = []
    for pole in [*ct.pole(sys), 0]:  # for each pole and added the pole generated for the PID integrator
        angle = np.angle(pd - pole) * 180 / np.pi
        if angle < 0:
            angle = 360 + angle
        poles_angles.append(angle)

    zeros_angles = []
    for zero in ct.zero(sys):  # for each pole
        angle = np.angle(pd - zero) * 180 / np.pi
        if angle < 0:
            angle = 360 + angle
        zeros_angles.append(angle)

    b_angle = -180 - (sum(zeros_angles) - sum(poles_angles))
    b_angle = b_angle / 2  # because a == b in the PID controller form

    if report:
        print("positioned pole angle: %.2f" % b_angle)

    dist = pd.imag / np.tan(b_angle * np.pi / 180)
    b = pd.real - dist  # finally, we have b

    if report:
        print("found 'b' constant = %.2f" % b)
        print("a = b, then a = %.2f too" % b)

    # finding Kc with module condition
    poles_dists = []
    for pole in [*ct.pole(sys), 0]:  # for each pole and added the pole generated for the PID integrator
        poles_dists.append(np.abs(pd - pole))

    zeros_dists = []
    for zero in [*ct.zero(sys), b, b]:  # for each pole added with our new zeros (from PID) calculated before
        zeros_dists.append(np.abs(pd - zero))

    k = sys.num[0][0][-1]  # assuming the basic form of a SISO system
    kc = np.prod(poles_dists) / k / np.prod(zeros_dists)

    if report:
        print("found 'kc' constant = %.2f" % kc)

    # defining PID constants
    kp = -2 * kc * b
    ki = kc * b ** 2
    kd = kc

    if report:
        print("controller = %.2f * (s+%.2f)^2 / s" % (kc, b))
        print("pid form = %.2f + %.2f/s + %.2f*s" % (kp, ki, kd))

    c = kp + ki/s + kd*s
    pid = core.symbolic_transfer_function(c)

    return pid
