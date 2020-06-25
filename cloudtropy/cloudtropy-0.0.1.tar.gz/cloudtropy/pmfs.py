import numpy as np
from sklearn.metrics import pairwise_distances


def pmf(X,N=None,d=None,delta_c=None,return_grid=True):
	"""
    Take a cloud X of P points in Q dimensions (i.e., X.shape->(P,Q)) and compute
	a discrete-support probability mass function on a Q-dimensional grid.
	The number of elements of the grid along one dimension is N, is given, or 
	computed from step d.
	delta_c is the euclidean radius under which points of the cloud are 
	associated with the points of the Q-dimensional grid.

    Parameters
    ----------
    X : float, array
        Input array. Rows are points, columns are coordinates.
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
    pmf : ndarray
        The N**Q point array. 
		If True, return the support of the N**Q grid points,
		it returns (grid,pmf)


    See Also
    --------
    Onesto, V., M. Romano, F. Gentile, and F. Amato. 
    "Relating the small world coefficient to the entropy of 2D networks and 
    applications in neuromorphic engineering." 
    Journal of Physics Communications 3, no. 9 (2019): 095011.

    """

	# check data
	if np.isnan(X).any():
	    raise ValueError('No nan cooridats allowed for the poins in the cloud.')
	if X.shape[0]<1:
		raise ValueError('The cloud must contain at least one point.')
	if (d is not None) and (N is not None):
	    raise ValueError('N and d parameters cannot be given at the same time.')
	# if (d is None) and (N is None):
	#     raise ValueError('Either N or d must be given as inputs.')

	# Treating input
	if (d is not None) and (N is None):
		N = np.max( (X.max(axis=1)-X.min(axis=1))/d )
	if (d is None) and (N is None):
	    N=20
	if delta_c is None:
		delta_c = np.max( (X.max(axis=1)-X.min(axis=1)))/N

	# Retrieving parameters of the points cloud
	(N_points,dims) = X.shape
	# N_points = X.shape[0]
	# dims = X.shape[1]

	# Generating grid
	lims = []
	for dim in range(dims):
	    lims.append( (np.min(X[:,dim]),np.max(X[:,dim])) )   
	dim_arrays = []
	for dim in range(dims):
	    if d is not None:
	        dim_arrays.append(np.arange(start=lims[dim][0],stop=lims[dim][1]+d,step=d))
	    elif N is not None:
	        dim_arrays.append(np.linspace(start=lims[dim][0],stop=lims[dim][1],num=N))
	grid = np.meshgrid(*dim_arrays)
	# Creating the points of the grid
	Y = np.vstack(map(np.ravel, grid)).transpose()

	# Pairwise distance between the points of the cloud and the points of the grid
	pd = pairwise_distances(X,Y)

	# Computing the PMF
	flat_pmf = (pd<delta_c).sum(axis=0)
	flat_pmf = flat_pmf/flat_pmf.sum()
	pmf = np.reshape(flat_pmf,newshape=[N for i in range(dims)])

	if return_grid:
		return grid, pmf;
	else:
		return pmf;
