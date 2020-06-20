"""
Mapping functions to warp camera image
"""
import numpy as np

def _newtons_real(x, y):
    return x + (2.0*x**2)/(3.0*(x**2 + y**2)**2) - (2.0*x**5)/(3.0*(x**2 + y**2)**2) - (2.0*y**2)/(3.0*(x**2 + y**2)**2) - (4.0*x**3 * y**2)/(3.0*(x**2 + y**2)**2) - (2.0*x*y**4)/(3.0*(x**2 + y**2)**2)

def _newtons_imag(x, y):
    return y - (4.0*x*y)/(3.0*(x**2 + y**2)**2) - (2.0*y*x**4)/(3.0*(x**2 + y**2)**2) - (4.0*x**2 * y**3)/(3.0*(x**2 + y**2)**2) - (2.0*y**5)/(3.0*(x**2 + y**2)**2)

def _newtons_v2_real(x, y):
    return x - np.sin(2.0*x)/(np.cos(2*x) + np.cosh(2*y))

def _newtons_v2_imag(x, y):
    return y - np.sinh(2.0*y)/(np.cos(2.0*x) + np.cosh(2.0*y))

def _newtons_v3_real(x, y):
    return (2.0*np.sinh(x)*np.cosh(x)*np.cos(y)*np.cos(y))/(np.cos(2*y) - np.cosh(2*x)) - (2*np.sinh(x)*np.cos(y))/(np.cos(2*y) - np.cosh(2*x)) + (2*np.sinh(x)*np.cosh(x)*np.sin(y)*np.sin(y))/(np.cos(2*y) - np.cosh(2*x)) + x

def _newtons_v3_imag(x, y):
    return -(2*np.cosh(x)*np.cosh(x)*np.sin(y)*np.cos(y))/(np.cos(2*y) - np.cosh(2*x)) + (2*np.cosh(x)*np.sin(y))/(np.cos(2*y) - np.cosh(2*x)) + (2*np.sinh(x)*np.sinh(x)*np.sin(y)*np.cos(y))/(np.cos(2*y) - np.cosh(2*x)) + y

def _newtons_v4_real(x, y):
    return x/(2*(x**2 + y**2)) + y/(2*(x**2 + y**2)) + x/2 + y/2

def _newtons_v4_imag(x, y):
    return x/(2*(x**2 + y**2)) - y/(2*(x**2 + y**2)) - x/2 + y/2

def _newtons_v5_real(x, y):
    arg = np.arctan2(x,y)
    return -(0.336*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) + (0.252*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) - (0.252*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) - (0.336*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) - (0.672*y*y*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) + (0.504*y*y*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) - (0.504*y*y*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) - (0.672*y*y*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) + x + (0.336*np.exp(3*arg)*np.cos(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.336*(y**4)*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) + (0.252*(y**4)*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.252*np.exp(3*arg)*np.sin(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.252*(y**4)*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.336*(y**4)*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2)

def _newtons_v5_imag(x, y):
    arg = np.arctan2(x,y)
    return (0.252*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) + (0.336*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) - (0.336*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) + (0.252*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*(x**4))/(x*x + y*y)**(3/2) + (0.504*y*y*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) + (0.672*y*y*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) - (0.672*y*y*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) + (0.504*y*y*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y))*x*x)/(x*x + y*y)**(3/2) + y - (0.252*np.exp(3*arg)*np.cos(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) + (0.252*(y**4)*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.cos(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) + (0.336*(y**4)*np.cos(4*arg + (3/2)*np.log(x*x + y*y))*np.sin(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.336*np.exp(3*arg)*np.sin(3*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) - (0.336*(y**4)*np.cos(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2) + (0.252*(y**4)*np.sin(3*arg + (3/2)*np.log(x*x + y*y))*np.sin(4*arg + (3/2)*np.log(x*x + y*y)))/(x*x + y*y)**(3/2)


def mandelbrot(height, width):
    """
    Function to apply one iteration of the transform:
    z_next = z^2 + c
    
    where c are pixels in the webcam. Note: pixel rows/cols position are
    shifted to fit the "interesting" areas of the map:
    real: [-2, 1]
    imag: [-1, 1]
    """

    h,w = (height, width)
    xscale = 3.0
    yscale = 3.0
    xshift = 1.5
    yshift = 1.5

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = x**2 - y**2
    # Imaginary part
    rows = 2*x*y
    # rows = np.roll(rows,150,0)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)

def newtons(height, width):
    """
    Newton's Fractal fixed as p = z^3 -1 and a=2
    """

    h,w = (height, width)
    xscale = 6.0
    yscale = 4.0
    xshift = 3.0
    yshift = 1.5

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = _newtons_real(x, y)
    # Imaginary part
    rows = _newtons_imag(x, y)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)

def newtons_v2(height, width):
    """
    Newton's Fractal fixed as p = sin(z) and a=1
    """

    h,w = (height, width)
    xscale = 4.0
    yscale = 2.0
    xshift = 2.0
    yshift = 1.0

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = _newtons_v2_real(x, y)
    # Imaginary part
    rows = _newtons_v2_imag(x, y)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)

def newtons_v3(height, width):
    """
    Newton's Fractal with p = cosh(z) - 1
    """

    h,w = (height, width)
    xscale = 10.0
    yscale = 10.0
    xshift = 5.0
    yshift = 5.0

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = _newtons_v3_real(x, y)
    # Imaginary part
    rows = _newtons_v3_imag(x, y)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)

def newtons_v4(height, width):
    """
    Newton's Fractal with p = z^2 - 1, a = 1+i
    """

    h,w = (height, width)
    xscale = 5.0
    yscale = 5.0
    xshift = 2.5
    yshift = 2.5

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = _newtons_v4_real(x, y)
    # Imaginary part
    rows = _newtons_v4_imag(x, y)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)

def newtons_v5(height, width):
    """
    Newton's Fractal with p = z^(4+3i) - 1, a = 2.1
    """

    h,w = (height, width)
    xscale = 5.0
    yscale = 4.0
    xshift = 1.0
    yshift = 0.0

    rows,cols = np.mgrid[0:h, 0:w]
    # Shift to interesting area
    x = xscale * (cols/w) - xshift
    y = yscale * (rows/h) - yshift
    # Real part
    cols = _newtons_v5_real(x, y)
    # Imaginary part
    rows = _newtons_v5_imag(x, y)

    # Shift back to image coords
    rows = h*(rows + yshift)/yscale
    cols = w*(cols + xshift)/xscale

    return (rows, cols)