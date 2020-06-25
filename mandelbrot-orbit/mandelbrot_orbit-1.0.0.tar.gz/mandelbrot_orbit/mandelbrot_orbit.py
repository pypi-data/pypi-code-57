# -*- coding: utf-8 -*-


"""mandelbrot_orbit.mandelbrot_orbit: provides entry point main()."""

__version__ = "1.0.0"

import sys

import matplotlib.pyplot as plt
import mpmath

from mandelbrot_orbit.orbit_calculator import OrbitCalculator


def main():
    print("Executing mandelbrot_orbit version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])

    zx = sys.argv[1]
    zy = sys.argv[2]
    num_iterations = int(sys.argv[3])

    print("Generation of orbit for point (", zx, " , ", zy, ") with ", num_iterations, " iterations ...")

    # Calculate orbit
    c = mpmath.mpc(real=zx, imag=zy)
    orbit_re, orbit_im = OrbitCalculator.generate(c, num_iterations)

    # Format data for plot
    x = range(num_iterations)
    orbit_re_float = list(map(float, orbit_re))
    orbit_im_float = list(map(float, orbit_im))

    # Plot real and imaginary parts
    plt.plot(x, orbit_re_float, color="orange", linewidth=1.5)
    plt.plot(x, orbit_im_float, color="blue", linewidth=1.5)

    # Show grid
    plt.grid(True)

    # Image size
    plt.gcf().set_size_inches(12, 4)

    # x axis
    plt.xlim([0, 100])

    # Save image
    plt.savefig("./mandelbrot_orbit.png", bbox_inches="tight")
