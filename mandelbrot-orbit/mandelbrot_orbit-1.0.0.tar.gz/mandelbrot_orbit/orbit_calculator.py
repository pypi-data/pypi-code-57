import mpmath


class OrbitCalculator:

    @staticmethod
    def generate(c, num_iterations=200):
        orbit_re = []
        orbit_im = []
        z = mpmath.mpc(real='0.0', imag='0.0')
        for _ in range(num_iterations):
            z = mpmath.fadd(mpmath.fmul(z, z), c)
            orbit_re.append(mpmath.nstr(mpmath.re(z)))
            orbit_im.append(mpmath.nstr(mpmath.im(z)))
        return [orbit_re, orbit_im]
