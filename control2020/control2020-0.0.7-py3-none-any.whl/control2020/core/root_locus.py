import numpy as np
import sympy as sp
import control as ct
from matplotlib import pyplot as plt
from typing import Tuple, Union, List
from control2020 import core


def plot_root_locus(g: Union[sp.Expr, ct.TransferFunction], ki: float = 0, kf: float = 5e3,
                    points: int = 500, k_space: str = "lin", print_critical: bool = False,
                    critical_tolerance: float = 0.01) -> plt.Line2D:
    """
    Plot a medium fidelity Root Locus of your G, K and H transfer functions
    :param g: Your plant transfer function
    :param ki: Gain range start (default: 0)
    :param kf: Gain range end (default: 5000)
    :param points: Fine Grain or measured points of your Gain range (default: 500)
    :param k_space: Your kind of space generated for your Gain range
    :param print_critical: If you want to print Critical Gain (pass for imag axis)
    :param critical_tolerance: The minimal threshold distance to imag axis
    :return: A Plot Line2D object, ready to show
    """
    # s = sp.var("s")

    if isinstance(g, ct.TransferFunction):
        sys = g
    else:
        sys = core.symbolic_transfer_function(g)

    # plt.title(f"Root locus of $G={sp.latex(g)}$", fontsize='x-large')
    plt.xlabel("$Real\\ Axis\\ [s^{-1}]$")
    plt.ylabel("$Imaginary\\ Axis\\ [s^{-1}]$")

    if k_space == "lin":
        range_space = np.linspace(ki, kf, points)
    elif k_space == "log":
        range_space = np.logspace(ki, kf, points)
    else:
        raise BaseException("invalid space, use \"lin\" o \"log\"")

    paths, gains = ct.root_locus(sys, kvect=range_space, Plot=False)

    for i, gain in enumerate(gains):
        points = paths[i]
        for point in points:
            if print_critical and abs(point.real) < critical_tolerance:
                print("Critical gain K = %.3f at %.3f + %.3fi" % (gain, point.real, point.imag))

    plt.axvline(0, color='k')
    plt.axhline(0, color='k')
    plt.grid()

    plt.plot(np.real(paths), np.imag(paths))

    n_poles = sys.pole()
    n_zeros = sys.zero()

    plt.plot(np.real(n_poles), np.imag(n_poles), "kx")

    return plt.plot(np.real(n_zeros), np.imag(n_zeros), "ko")


def find_points_in_root_locus(g: sp.Expr, find: Union[List[float], List[complex]], k: sp.Expr = sp.var("K"),
                              h: sp.Expr = 1,
                              tolerance: float = 0.01, ki: float = 0, kf: float = 50, points: int = int(1e3),
                              print_founds: bool = False) -> List[Tuple[float, complex]]:
    """
    Find points near a some path of your root locus space
    :param g: Your plant transfer function
    :param find: Your point or list of points to search
    :param k: Your gain (or compensator) transfer function
    :param h: Your feedback transfer function
    :param tolerance: The minimal threshold distance to your searched points
    :param ki: Gain range start (default: 0)
    :param kf: Gain range end (default: 5000)
    :param points: Fine Grain or measured points of your Gain range (default: 500)
    :param print_founds: If you want to print your founded points
    :return: a list of pairs (Gain, point)
    """
    if find is None:
        find = []
    eq = core.extract_characteristic_equation(k, g, h)
    s = sp.var("s")

    founds: List[Tuple[float, complex]] = []

    for current_gain in np.linspace(ki, kf, points):
        p = sp.Poly(sp.expand(eq.subs(sp.var("K"), current_gain)), s)
        all_coeffs = list(p.all_coeffs())
        num_polynomial = np.poly1d(all_coeffs)
        points = list(np.roots(num_polynomial))
        for i, point in enumerate(points):
            for to_find in find:
                real_error = np.abs(to_find.real - point.real)
                imag_error = np.abs(to_find.imag - point.imag)
                if real_error < tolerance and imag_error < tolerance:
                    if print_founds:
                        e = float(np.mean([real_error, imag_error]))
                        print("K = %.3f at %.3f + %.3fi | e = %.3f" % (current_gain, point.real, point.imag, e))
                    founds.append((current_gain, point))
    return founds
