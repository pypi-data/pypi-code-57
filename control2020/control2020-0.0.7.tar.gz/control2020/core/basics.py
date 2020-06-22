import sympy as sp
import control as ct
from typing import Union


def symbolic_transfer_function(eq: Union[sp.Expr, int, float]) -> ct.TransferFunction:
    """
    Transform a symbolic equation to a transfer function (sympy -> control)
    :param eq: your symbolic sympy based equation
    :return: a control Transfer Function class
    """
    s = sp.var('s')
    try:
        if eq.is_real:
            pass
    except:
        if not isinstance(eq, float) and not isinstance(eq, int):
            used_symbols = [str(sym) for sym in eq.free_symbols]
            if not len(used_symbols) == 1 or "s" not in used_symbols:
                raise Exception("invalid equation, please use correct transfer function equation (e.g. 1/(s**2+3))")

    n, d = sp.fraction(sp.factor(eq))

    num = sp.Poly(sp.expand(n), s).all_coeffs()
    den = sp.Poly(sp.expand(d), s).all_coeffs()

    num: [float] = [float(v) for v in num]
    den: [float] = [float(v) for v in den]

    return ct.TransferFunction(num, den)


def extract_characteristic_equation(g: sp.Expr, k: sp.Expr = sp.var("K"), h: Union[sp.Expr, float] = 1) -> sp.Expr:
    """
    Extract the characteristic equation form from a set of G, K and H system blocks
    The characteristic equation have the form: 1 + K*G*H = 0
    :param g: Your plant transfer function
    :param k: Your gain (or compensator) transfer function
    :param h: Your feedback transfer function
    :return: a symbolic expresion that contains your characteristic equation
    """
    eq = sp.factor(sp.simplify(1 + k * g * h))
    num, _ = sp.fraction(eq)
    return sp.expand(num)  # == 0

