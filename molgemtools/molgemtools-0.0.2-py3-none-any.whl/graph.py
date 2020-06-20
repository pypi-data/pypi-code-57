"""Tools for working with chemical graphs.
"""


import numpy as np


class Graph:
    """The `Graph` class contains some methods for working with
    chemical graphs.

    Parameters
    ----------
    adj_list : list of list of int

    See Also
    --------
    molgemtools.geom.Geom.adjacency
    """

    def __init__(self, adj_list):
        self.adj_list = adj_list
        self.n = len(self.adj_list)
        adj_items = []
        for inner_list in self.adj_list:
            if type(inner_list) != list:
                raise Exception("adj_list should contain lists of integers.")
            adj_items = adj_items + inner_list
        for i in adj_items:
            if i < 0:
                raise Exception("An atomic index should not be negative.")
        for i in range(self.n):
            for j in self.adj_list[i]:
                if i not in self.adj_list[j]:
                    raise Exception("adj_list is invalid.")

    def adjmat(self):
        """Calculates the adjacency matrix.

        Returns
        -------
        adj_array : ndarray

        Examples
        --------
        Creating the adjacency matrix of alanine from its adjacency
        list.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> for item in adj_list:
        ...     print(item)
        [1, 3, 4]
        [0, 2, 6, 7]
        [1, 8, 9]
        [0, 5]
        [0]
        [3]
        [1]
        [1, 10, 11, 12]
        [2]
        [2]
        [7]
        [7]
        [7]
        >>> adj_array = mgr.Graph(adj_list).adjmat()
        >>> for item in adj_array:
        ...     print(item)
        [0. 1. 0. 1. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
        [1. 0. 1. 0. 0. 0. 1. 1. 0. 0. 0. 0. 0.]
        [0. 1. 0. 0. 0. 0. 0. 0. 1. 1. 0. 0. 0.]
        [1. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
        [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 1. 1. 1.]
        [0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
        [0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
        """
        adj_array = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in self.adj_list[i]:
                adj_array[i][j] = 1.0
        return adj_array

    def distmat(self):
        """Calculates the distance matrix.

        Returns
        -------
        dist_array : ndarray

        See Also
        --------
        molgemtools.graph.Graph.adjmat

        Notes
        -----
        The calculation of the distance matrix is based upon the
        Floyd-Warshall algorithm.

        References
        ----------
        .. [Floyd1962] R. W. Floyd; Algorithm 97: shortest path.,
            Communications of the ACM, Vol. 5, No. 6, 1962, 345.

        Examples
        --------
        The distance matrix of alanine.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> dist_array = mgr.Graph(adj_list).distmat()
        >>> for item in dist_array:
        ...     print(item)
        [0. 1. 2. 1. 1. 2. 2. 2. 3. 3. 3. 3. 3.]
        [1. 0. 1. 2. 2. 3. 1. 1. 2. 2. 2. 2. 2.]
        [2. 1. 0. 3. 3. 4. 2. 2. 1. 1. 3. 3. 3.]
        [1. 2. 3. 0. 2. 1. 3. 3. 4. 4. 4. 4. 4.]
        [1. 2. 3. 2. 0. 3. 3. 3. 4. 4. 4. 4. 4.]
        [2. 3. 4. 1. 3. 0. 4. 4. 5. 5. 5. 5. 5.]
        [2. 1. 2. 3. 3. 4. 0. 2. 3. 3. 3. 3. 3.]
        [2. 1. 2. 3. 3. 4. 2. 0. 3. 3. 1. 1. 1.]
        [3. 2. 1. 4. 4. 5. 3. 3. 0. 2. 4. 4. 4.]
        [3. 2. 1. 4. 4. 5. 3. 3. 2. 0. 4. 4. 4.]
        [3. 2. 3. 4. 4. 5. 3. 1. 4. 4. 0. 2. 2.]
        [3. 2. 3. 4. 4. 5. 3. 1. 4. 4. 2. 0. 2.]
        [3. 2. 3. 4. 4. 5. 3. 1. 4. 4. 2. 2. 0.]
        """
        dist_array = self.adjmat()
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                if dist_array[i][j] == 0.0:
                    dist_array[i][j] = np.inf
                    dist_array[j][i] = np.inf
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist_array[i][j] > dist_array[i][k] + dist_array[k][j]:
                        dist_array[i][j] = dist_array[i][k] + dist_array[k][j]
        return dist_array

    def vertex(self):
        """Calculates the vertex degree vector.

        Returns
        -------
        vertex_array : ndarray

        See Also
        --------
        molgemtools.graph.Graph.adjmat

        Examples
        --------
        The vertex degree vector of alanine.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> vertex_array = mgr.Graph(adj_list).vertex()
        >>> for item in vertex_array:
        ...     print(item)
        3.0
        4.0
        3.0
        2.0
        1.0
        1.0
        1.0
        4.0
        1.0
        1.0
        1.0
        1.0
        1.0
        """
        vertex_array = sum(self.adjmat())
        return vertex_array

    def distsum(self):
        """Calculates the distance-sums vector.

        Returns
        -------
        distsum_array : ndarray

        See Also
        --------
        molgemtools.graph.Graph.distmat

        Examples
        --------
        The distance-sums vector of alanine.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> distsum_array = mgr.Graph(adj_list).distsum()
        >>> for item in distsum_array:
        ...     print(item)
        26.0
        21.0
        28.0
        35.0
        37.0
        46.0
        32.0
        26.0
        39.0
        39.0
        37.0
        37.0
        37.0
        """
        distsum_array = sum(self.distmat())
        return distsum_array

    def laplacian(self):
        """Calculates the Laplacian matrix.

        Returns
        -------
        laplacian_array : ndarray

        References
        ----------
        .. [Anderson1985] W. N. Anderson Jr.; T. D. Morley;
            Eigenvalues of the Laplacian of a graph, Linear and
            Multilinear Algebra, 18:2, 1985, 141-145.

        Examples
        --------
        The Laplacian matrix of alanine.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> laplacian_array = mgr.Graph(adj_list).laplacian()
        >>> for item in laplacian_array:
        ...     print(item)
        [ 3. -1.  0. -1. -1.  0.  0.  0.  0.  0.  0.  0.  0.]
        [-1.  4. -1.  0.  0.  0. -1. -1.  0.  0.  0.  0.  0.]
        [ 0. -1.  3.  0.  0.  0.  0.  0. -1. -1.  0.  0.  0.]
        [-1.  0.  0.  2.  0. -1.  0.  0.  0.  0.  0.  0.  0.]
        [-1.  0.  0.  0.  1.  0.  0.  0.  0.  0.  0.  0.  0.]
        [ 0.  0.  0. -1.  0.  1.  0.  0.  0.  0.  0.  0.  0.]
        [ 0. -1.  0.  0.  0.  0.  1.  0.  0.  0.  0.  0.  0.]
        [ 0. -1.  0.  0.  0.  0.  0.  4.  0.  0. -1. -1. -1.]
        [ 0.  0. -1.  0.  0.  0.  0.  0.  1.  0.  0.  0.  0.]
        [ 0.  0. -1.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.]
        [ 0.  0.  0.  0.  0.  0.  0. -1.  0.  0.  1.  0.  0.]
        [ 0.  0.  0.  0.  0.  0.  0. -1.  0.  0.  0.  1.  0.]
        [ 0.  0.  0.  0.  0.  0.  0. -1.  0.  0.  0.  0.  1.]
        """
        laplacian_array = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in self.adj_list[i]:
                laplacian_array[i][j] = -1.0
        vertex_array = self.vertex()
        for i in range(self.n):
            laplacian_array[i][i] = vertex_array[i]
        return laplacian_array

    def components(self, pz=10):
        """Calculates the number of the connected components.

        Parameters
        ----------
        pz : int or float, optional
            A number less than 10 to the negative power of `pz`
            considered 0.

        Returns
        -------
        c : int

        See Also
        --------
        molgemtools.graph.Graph.laplacian

        Notes
        -----
        The multiplicity of the 0 eigenvalue of the Laplacian matrix
        of the graph equals the number of the connected components.

        Examples
        --------
        The number of connected components of the graph of alanine.

        >>> import molgemtools.geom as mg
        >>> import molgemtools.graph as mgr
        >>> x_dict = mg.open_xyz('data/alanine/conformers/ala_1.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> c = mgr.Graph(adj_list).components()
        >>> c
        1

        Calculating the number of connected components of the graph
        created from `water_molecules.xyz`.

        >>> x_dict = mg.open_xyz('data/water_molecules.xyz')
        >>> adj_list = mg.Geom(x_dict).adjacency()
        >>> c = mgr.Graph(adj_list).components()
        >>> c
        5
        """
        eig_list = np.linalg.eig(self.laplacian())[0]
        c = 0
        for i in eig_list:
            if round(abs(i), pz) == 0.0:
                c = c + 1
        return c


if __name__ == "__main__":
    import os
    import doctest


    os.chdir(os.path.dirname(__file__))
    doctest.testmod()
    print("Doctest of molgemtools.graph...")
