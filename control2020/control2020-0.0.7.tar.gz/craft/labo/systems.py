import control as ct
import control2020 as ct20
import sympy as sp
from typing import Union, Tuple, Dict
import numpy as np

TF = Union[ct.TransferFunction, sp.Expr, float, str]


def normalized_tf(tf: TF) -> ct.TransferFunction:
    if isinstance(tf, ct.TransferFunction):
        return tf
    elif isinstance(tf, str):
        return ct20.core.symbolic_transfer_function(sp.sympify(tf))
    else:
        return ct20.core.symbolic_transfer_function(tf)


class System:
    def __init__(self, g: TF, k: TF = 1, h: TF = 1, in_noise: TF = 0, out_noise: TF = 0):
        self.K: ct.TransferFunction = normalized_tf(k)
        self.G: ct.TransferFunction = normalized_tf(g)
        self.H: ct.TransferFunction = normalized_tf(h)
        self.in_noise: ct.TransferFunction = normalized_tf(in_noise)
        self.out_noise: ct.TransferFunction = normalized_tf(out_noise)

    def open_system(self) -> ct.TransferFunction:
        return self.in_noise + self.K * self.G + self.out_noise

    def full_system(self) -> ct.TransferFunction:
        return ct.feedback(self.open_system(), self.H)

    def step(self, time: list = None) -> Tuple[list, list]:
        t, y = ct.step_response(self.full_system(), time)
        return t, y

    def step_report(self, time: list = None) -> Dict[str, float]:
        return ct.step_info(self.full_system(), time)

    def response_to(self, u: list, time: list = None) -> Tuple[np.float, np.float]:
        t, y = ct.forced_response(self.full_system(), time, u)
        return t, y

    def bode_open(self, omega: list = None) -> Tuple[np.float, np.float, np.float]:
        mag, phase, omega = ct.bode(self.open_system(), omega=omega, dB=True, deg=True, Plot=False)
        return mag, phase, omega

    def bode_close(self, omega: list = None) -> Tuple[list, list, list]:
        mag, phase, omega_returned = ct.bode(self.full_system(), omega=omega, dB=True, deg=True, Plot=False)
        return mag, phase, omega_returned

    def margins_open(self, omega: list = None) -> Tuple[float, float, float, float]:
        gm, pm, wg, wp = ct.margin(self.open_system(), omega)
        return gm, pm, wg, wp

    def update(self, g: TF = None, k: TF = None, h: TF = None, in_noise: TF = None, out_noise: TF = None):
        if g is not None:
            self.G = normalized_tf(g)
        if k is not None:
            self.K = normalized_tf(k)
        if h is not None:
            self.H = normalized_tf(h)
        if in_noise is not None:
            self.in_noise = normalized_tf(in_noise)
        if out_noise is not None:
            self.out_noise = normalized_tf(out_noise)
