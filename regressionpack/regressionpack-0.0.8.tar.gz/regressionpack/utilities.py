import numpy as np
from typing import Tuple

def _parseAxis(A:np.ndarray, axis:Tuple[int,int]):
    assert all([-A.ndim <= x < A.ndim for x in axis]), "Specified dimension must respect -X.ndim <= ParmDim < X.ndim"
    return tuple([x % A.ndim for x in axis])

def getOrder(A:np.ndarray, axis:Tuple[int,int]=(-2,-1)):

    axis = _parseAxis(A, axis)
    # Define how the axis are to be re-ordered (must put the axis of interest in the last two positions)
    order = tuple([x for x in range(A.ndim) if x not in axis]) + axis

    # Define how to re-order the result at the end
    reorder = list()
    counter = 0
    for i in range(A.ndim):
        if i == axis[0]:
            reorder.append(A.ndim-2)
        elif i == axis[1]:
            reorder.append(A.ndim-1)
        else:
            reorder.append(counter)
            counter += 1

    return order, reorder

def MatMul(A:np.ndarray, B:np.ndarray, axis:Tuple[int,int]=(-2,-1)):
        """
        Computes the matrix product between the chosen two axis. By default, it will
        use the first two. 
        """

        axis = _parseAxis(A, axis)

        # Shortcut if the axis are the last two
        if axis == (A.ndim-2, A.ndim-1):
            return np.matmul(A, B)

        # Find how to reorder these
        order, reorder = getOrder(A, axis)

        # Compute and return the result
        return np.matmul(A.transpose(order), B.transpose(order)).transpose(reorder)

def MatInv(A:np.ndarray, axis:Tuple[int,int]=(-2,-1)):
    """
    Compute the inverse of the matrix on the two axis of interest. 
    By default uses the first two axis
    """

    axis = _parseAxis(A, axis)

    # Shortcut if the axis are the last two
    if axis == (A.ndim-2, A.ndim-1):
        return np.linalg.pinv(A)

    # Find how to reorder these
    order, reorder = getOrder(A, axis)

    # Compute and return the result
    return np.linalg.pinv(A.transpose(order)).transpose(reorder)

def MatDiag(A:np.ndarray, axis:Tuple[int,int]=(-2,-1)):
    """
    Returns the diagonal of the selected two axis. 
    """

    axis = _parseAxis(A, axis)

    assert A.shape[axis[0]] == A.shape[axis[1]], "The two selected axis must have the same size"

    # Shortcut if the axis are the last two
    if axis == (A.ndim-2, A.ndim-1):
        # Create an output array
        shape = list(A.shape)
        shape[-2] = 1
        out = np.zeros(shape)

        # Get the diagonal
        for k in range(A.shape[axis[0]]):
            out[...,0,k] = A[...,k,k]

        return out

    # Find how to reorder these
    order, reorder = getOrder(A, axis)

    # Create an output array
    temp = A.transpose(order)
    shape = list(temp.shape)
    shape[-2] = 1
    out = np.zeros(shape)

    # Get the diagonal
    for k in range(A.shape[axis[0]]):
        out[...,0,k] = temp[...,k,k]

    # Reshape and return
    return out.transpose(reorder)

def MatFlip(A:np.ndarray, axis:Tuple[int,int]=(-2,-1)):
    """
    Flips those two axis in the matrix
    """
    axis = _parseAxis(A, axis)

    order = list(range(A.ndim))
    order[axis[0]] = axis[1]
    order[axis[1]] = axis[0]
    return A.transpose(order)

def MatRemoveDim(A:np.ndarray, axis=int):
    assert A.shape[axis] == 1, 'Can only remove a dimension of size 1'
    order = [x for x in range(A.ndim) if x != axis] + [axis]
    return A.transpose(order)[...,0]

def FFTGuess(x:np.ndarray, y:np.ndarray, axis=-1) -> Tuple[float, float, float, float]:
    """
    Guesses the parameters used for a CosineFit using the Fourier transform. 
    This approach can be limited if more than one frequency is prominent, 
    as it only takes the most prominent one. 

    Only the frequencies below Nyquist will be used for this, also if
    the x vector is not evenly spaced, interpolation will be used. 

    Returns the following parameters:
        amplitude (amp)
        frequency (omega)
        phase shift (phi)
        vertical offset (voff)

    """
    assert x.ndim == 1 and y.ndim == 1, "Only 1D arrays are supported for now. "

    dx = np.diff(x, axis=axis)
    if not np.allclose(dx[0],dx):
        # If the x values are not evenly spaced enough, interpolate
        dx = np.min(dx)
        xi = np.linspace(x.min(), x.max(), (x.max() - x.min())//dx + 1)
        yi = np.interp(xi, x, y)
        
        # Replace with interpolated values
        x, y = xi, yi

    # Perform the fft of the function
    nb = y.shape[axis]
    Y = np.fft.fft(y, axis=axis)[:nb//2] / nb # Normalize by number of points
    Y[1:] *= 2 # Correction when taking only positive frequencies
    A = np.abs(Y) # Amplitude

    # Obtain the frequencies as well
    F = np.fft.fftfreq(nb, (x.max() - x.min())/(nb -1))[:nb//2]

    # Find the most prominent peak after the DC offset
    amp = np.max(A[1:])

    # Find the frequency and phase of that peak
    crit = A == amp
    omega = F[crit][0] * 2*np.pi
    phi = np.angle(Y[crit])[0]

    # Grab the DC offset
    voff = Y[0].real

    # Warn if the most prominent peak is not dominant enough
    totalEnergy = np.sum(A[1:]**2) # without counting the DC offset
    peakEnergy = amp**2

    if peakEnergy/totalEnergy < 0.5:
        print("Warning: the most prominent peak does not account for more than half the energy, the FFTGuess may not be the best one. ")

    return amp, omega, phi, voff