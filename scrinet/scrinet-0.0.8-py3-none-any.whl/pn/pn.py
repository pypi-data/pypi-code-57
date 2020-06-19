import numpy as np

# Newton gravity constant
# lal.G_SI: 6.67384e-11
G_Newt = 6.67384e-11

# light speed
# lal.C_SI: 299792458.0
c_ls = 299792458.0

# lal.MSUN_SI: 1.9885469549614615e+30
MSUN_SI = 1.9885469549614615e+30

MTSUN_SI = 4.925491025543576e-06

# lal.MRSUN_SI: 1476.6250614046494
MRSUN_SI = 1476.6250614046494

# lal.PC_SI: 3.085677581491367e+16
PC_SI = 3.085677581491367e+16

# lal.GAMMA: 0.5772156649015329
GAMMA = 0.5772156649015329


def Msun_to_sec(M):
    """
    convert mass (in units of solar masses)
    into seconds
    """
#     return M *lal.MSUN_SI* G_Newt / c_ls**3.
    return M * MTSUN_SI


def TaylorT3_phase(t, tc, eta, M, phi0=0, m=2):
    """
    orbital phase, but returns by default the m=2 mode
    equation 3.10a in https://arxiv.org/pdf/0907.0700.pdf

    https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralTaylorT3.c

    https://git.ligo.org/lscsoft/lalsuite/blob/master/lalsimulation/src/LALSimInspiralPNCoefficients.c

    t: time
    tc: coalescence time
    eta: symmetric mass ratio
    M: total mass (Msun)
    phi0: reference orbital phase, default 0
    m: m-mode default = 2
    """

    Msec = Msun_to_sec(M)
    Msec = M

    pi2 = np.pi*np.pi

    c1 = eta/(5.*Msec)

    td = c1 * (tc - t)

#     td = np.sqrt(td**2 + 1)

    theta = td**(-1./8.)  # -1./8. = -0.125

    theta2 = theta*theta
    theta3 = theta2*theta
    theta4 = theta3*theta
    theta5 = theta4*theta
    theta6 = theta5*theta
    theta7 = theta6*theta

    # pre factor
    ftaN = -1. / eta
    # 0PN
    fts1 = 1.
    # 0.5PN = 0 in GR
    # 1PN
    fta2 = 3.715/8.064 + 5.5/9.6 * eta
    # 1.5PN
    fta3 = -3./4. * np.pi
    # 2PN
    fta4 = 9.275495/14.450688 + 2.84875/2.58048 * eta + 1.855/2.048 * eta*eta
    # 2.5PN
    fta5 = (3.8645/2.1504 - 6.5/25.6 * eta) * np.pi
    # 3PN
    fta6 = 83.1032450749357/5.7682522275840 - 5.3/4.0 * pi2 - 10.7/5.6 * GAMMA \
        + (-126.510089885/4.161798144 + 2.255/2.048 * pi2) * eta \
        + 1.54565/18.35008 * eta*eta - 1.179625/1.769472 * eta*eta*eta

    # 3.5PN
    fta7 = (1.88516689/1.73408256 + 4.88825/5.16096 *
            eta - 1.41769/5.16096 * eta*eta) * np.pi

    # 3PN log term
    ftal6 = -10.7/5.6

    # 2.5 PN log term
    ftal5 = np.log(theta)

    full = ftaN/theta5 * (fts1
                          + fta2*theta2
                          + fta3*theta3
                          + fta4*theta4
                          + (fta5*ftal5)*theta5
                          + (fta6 + ftal6*np.log(2.*theta))*theta6
                          + fta7*theta7)

    return m*(phi0 + full)
