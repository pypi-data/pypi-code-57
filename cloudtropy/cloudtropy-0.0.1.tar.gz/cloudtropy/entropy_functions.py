import numpy as np
from scipy.stats import entropy as entpy
from .pmfs import pmf

def testfunc():
    return 1;

def entropy(X,base=2,N=None,d=None,delta_c=None):
    """
    Take a cloud X of P points in Q dimensions (i.e., X.shape->(P,Q)) and compute
    the entropy of a  discrete-support probability mass function on a Q-dimensional grid.
    The number of elements of the grid along one dimension is N, is given, or 
    computed from step d.
    delta_c is the euclidean radius under which points of the cloud are 
    associated with the points of the Q-dimensional grid.

    Parameters
    ----------
    X : float, array
        Input array. Rows are points, columns are coordinates.
    base : float, default=2
    	The base for the logarithm of the entropy
    N : int, optional (N (x)or d must be given)
        Number of elements of the grid along one dimension.
    d : float, optional (N (x)or d must be given)
        Step between the elements of the grid along one dimension.
    delta_c : float, optional
        Euclidean radius under which points of the cloud are 
    	associated with the points of the Q-dimensional grid.
    	If not given, computed as the greatest width divided by N.
    return_grid : bool, default=True
        If True, return the support of the N**Q grid points.

    Returns
    -------
    e : float
    The entropy of the computed PMF.

    See Also
    --------
    Onesto, V., M. Romano, F. Gentile, and F. Amato. 
    "Relating the small world coefficient to the entropy of 2D networks and 
    applications in neuromorphic engineering." 
    Journal of Physics Communications 3, no. 9 (2019): 095011.
    """

    p = pmf(X,N=N,d=d,delta_c=delta_c,return_grid=False)
    return entpy(np.ravel(p),base=base);
