class RadialBasisFunction2D:
    def __init__(self, x_min, x_max, y_min, y_max, x_dim, y_dim, sigma):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.n_dim = x_dim * y_dim
        self.sigma = sigma

        xlist = np.linspace(x_min, x_max, x_dim)
        ylist = np.linspace(y_min, y_max, y_dim)
        XX, YY = np.meshgrid(xlist, ylist)

        self.XX = XX
        self.YY = YY

        self.x_mu = XX.flatten()
        self.y_mu = YY.flatten()



    def transform(self, A):
        X_mu = np.broadcast_to(self.x_mu, (A.shape[0], self.n_dim))
        Y_mu = np.broadcast_to(self.y_mu, (A.shape[0], self.n_dim))
        X = np.broadcast_to(data[:,0].reshape(-1,1), (A.shape[0], self.n_dim))
        Y = np.broadcast_to(data[:,1].reshape(-1,1), (A.shape[0], self.n_dim))

        distance = ((X - X_mu)**2+((Y - Y_mu)**2))
        return np.exp(-distance/2*self.sigma)

    def inverse_transform(self, A):
        index = np.argmax(transformed_data, axis=1)
        result = []
        for idx in index:
            i, j = self._1d_index_to_2d_index(idx)
            result.append([self.XX[i][j], self.YY[i][j]])

        return np.array(result)

    def _1d_index_to_2d_index(self, index):
        i = index // self.x_dim;
        j = index % self.y_dim;

        return i, j
