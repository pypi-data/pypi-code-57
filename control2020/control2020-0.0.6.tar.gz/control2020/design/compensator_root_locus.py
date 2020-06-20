import numpy as np
import control as ct
import sympy as sp
from control2020 import core
from typing import Union, Tuple


def lead_compensator_with_root_placing(g: Union[sp.Expr, ct.TransferFunction], po: float, ts: float,
                                       compensator_zero: float = -1, auto_tune: bool = False,
                                       tune_range: Tuple[float, float] = (-1, 1), tune_values: int = 100,
                                       report: bool = False) -> ct.TransferFunction:
    """
    This function construct a lead compensator based on root locus placing
    :param g: Your plant transfer function
    :param po: Percentage Overshoot
    :param ts: Time Settling
    :param compensator_zero: Fixed zero for the compensator (must be negative)
    :param auto_tune: If you want to execute a simple algorithm to find near optimal zero based on your params
    :param tune_range: Tuple with two relative bounds for the tuner (default: (-4, 4))
    :param tune_values: Total of values to search
    :param report: If you want to print a report of the design construction
    :return: a TransferFunction controller
    """

    s = sp.var("s")

    if isinstance(g, ct.TransferFunction):
        sys = g
    else:
        sys = core.symbolic_transfer_function(g)

    psi, wn = core.from_quality_to_psi_wn(po, ts)
    if report:
        print("psi= %.2f | wn= %.2f" % (psi, wn))

    d_poles = core.construct_poles(psi, wn)

    if report:
        print("desired poles:")
        for d_p in d_poles:
            print("%.2f + %.2fi" % (d_p.real, d_p.imag))

    pd = d_poles[0]

    poles_angles = []
    for pole in sys.pole():
        angle = np.angle(pd - pole) * 180 / np.pi
        if angle < 0:
            angle = 360 - angle
        poles_angles.append(angle)

    zeros_angles = []
    for zero in sys.zero():
        angle = np.angle(pd - zero) * 180 / np.pi
        if angle < 0:
            angle = 360 - angle
        zeros_angles.append(angle)

    plant_angle = sum(zeros_angles) - sum(poles_angles)

    compensator_angle = -180 - plant_angle

    if report:
        print("compensator expected angle= %.2f" % compensator_angle)

    # compensator_zero:  # fixed value for your compensator
    fixed_zero = compensator_zero
    if auto_tune:  # simple algorithm to search the best near zero
        if report:
            print("---")
            print("auto tuning zero compensator in range (%.2f, %.2f) with %d steps" %
                  (compensator_zero + tune_range[0], compensator_zero + tune_range[1], tune_values))
            print("expected - ts: %.2f | po: %.2f" % (ts, po))
        errors: [float] = []
        zero_tests = np.linspace(compensator_zero + tune_range[0], compensator_zero + tune_range[1], tune_values)
        for i, z in enumerate(zero_tests):
            try:
                z_angle = np.angle(pd - z) * 180 / np.pi
                p_angle = z_angle - compensator_angle
                d_pole = pd.imag / np.tan(p_angle * np.pi / 180)
                p = pd.real - d_pole
                g_t = core.symbolic_transfer_function((s - z) / (s - p))
                g_t_pd_e = g_t.horner(pd)[0][0]  # expecting a siso model
                sys_pd_e = sys.horner(pd)[0][0]  # expecting a siso model
                kc = 1 / np.abs(g_t_pd_e) / np.abs(sys_pd_e)
                comp = kc * g_t
                f_sys = ct.feedback(comp * sys)
                step_report = ct.step_info(f_sys)
                g_ts = step_report["SettlingTime"]
                g_po = step_report["Overshoot"]
                if report:
                    print("step %d) zero: %.6f |  ts: %.2f | po: %.2f" % (i, z, g_ts, g_po))
                err = .4 * (po - g_po) ** 2 + .6 * (ts - g_ts) ** 2  # compute quadratic error
                errors.append(err)
            except:
                errors.append(np.inf)
                continue
        fixed_zero = zero_tests[np.argmin(errors)]
        if report:
            print("---")

    compensator_zero_angle = np.angle(pd - fixed_zero) * 180 / np.pi

    if report:
        print("fixed zero= %.6f | angle= %.2fdeg" % (fixed_zero, compensator_zero_angle))

    # angle condition
    pole_angle = compensator_zero_angle - compensator_angle  # calculated value for your compensator
    dist_pole = pd.imag / np.tan(pole_angle * np.pi / 180)

    compensator_pole = pd.real - dist_pole

    if report:
        print("calculated pole= %.2f + %.2fi | angle= %.2fdeg" % (
            compensator_pole.real, compensator_pole.imag, pole_angle))

    # finally we can to calculate the kc of our controller

    # module condition
    g1 = (s - fixed_zero) / (s - compensator_pole)
    g1_sys = core.symbolic_transfer_function(g1)

    g1_pd_evaluated = g1_sys.horner(pd)[0][0]  # expecting a siso model
    sys_pd_evaluated = sys.horner(pd)[0][0]  # expecting a siso model

    kc = 1 / np.abs(g1_pd_evaluated) / np.abs(sys_pd_evaluated)

    if report:
        print("found 'kc' constant = %.2f" % kc)

    final_compensator = kc * g1_sys

    return final_compensator
