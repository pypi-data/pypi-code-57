import numpy as np
import gmtb.util as util
from gmtb.util.distance.euclidean_dist import euclidean_dist

# code base from SOM Toolbox 2.1


def potency_curve(v0, vn, l):
    return v0 * np.power(vn/v0, np.arange(0, l, 1) / l)


def cca(data, num_dim, projection=None, epochs=1000, dist_mat=None, alpha0=0.5, lambda0=None):

    # CCA Projects data vectors using Curvilinear Component Analysis.
    # P = cca(D, projection, epochs, [Dist], [alpha0], [lambda0])
    #
    # P = cca(D, 2, 10); % projects the given data to a plane
    # P = cca(D, pcaproj(D, 2), 5); % same, but with PCA initialization
    # P = cca(D, 2, 10, Dist); % same, but the given distance matrix is used
    #
    # Input and output arguments([] 's are optional):
    # D          (matrix) the data matrix, size dlen x dim
    #            (struct) data or map struct
    # projection (scalar) output dimension
    #            (matrix) size dlen x odim, the initial projection
    # epochs     (scalar) training length
    # [Dist]     (matrix) pairwise distance matrix, size dlen x dlen.
    #                     If the distances in the input space should
    #                     be calculated otherwise than as euclidian
    #                     distances, the distance from each vector
    #                     to each other vector can be given here,
    #                     size dlen x dlen.For example PDIST
    #                     function can be used to calculate the
    #                     distances: Dist = squareform(pdist(D, 'mahal'));
    # [alpha0]   (scalar) initial step size, 0.5 by default
    # [lambda0]  (scalar) initial radius of influence, 3 * max(std(D)) by default
    #
    # Output:
    # projection (matrix) size dlen x odim, the projections
    #
    # Unknown values(NaN's) in the data: projections of vectors with
    # unknown components tend to drift towards the center of the
    # projection distribution.Projections of totally unknown vectors are
    # set to unknown(NaN).
    #
    # See also SAMMON, PCAPROJ.

    # Reference: Demartines, P., Herault, J., "Curvilinear Component
    #      Analysis: a Self - Organizing Neural Network for Nonlinear
    #      Mapping of Data Sets", IEEE Transactions on Neural Networks,
    #      vol 8, no 1, 1997, pp.148-154.

    # Contributed to SOM Toolbox 2.0, February 2nd, 2000 by Juha Vesanto
    # Copyright (c) by Juha Vesanto
    # http://www.cis.hut.fi/projects/somtoolbox/

    #juuso 171297 040100


    # input data
    noc = np.shape(data)[0]

    me = np.mean(data, axis=1)
    st = np.std(data, axis=1)

    #initial projection
    if projection is None:
        projection = (2 * np.random.rand(noc, num_dim) - 1) * st[0:num_dim] + me[0: num_dim]

    else:
        # replace unknown projections with known values
        inds = np.where(np.isnan(projection))
        projection[inds] = np.random.rand(np.shape(inds))

    # training length
    train_len = epochs * noc

    # random sample order
    # rand('state', sum(100 * clock)); % % TODO: FIX
    sample_inds = np.ceil(noc * np.random.rand(train_len)).astype(np.int64)-1 # -1 because index is from -0 to noc-1

    # mutual distances
    if dist_mat is None or np.alltrue(np.isnan(dist_mat)):
        # fprintf(2, 'computing mutual distances\r');
        #TODO compute euclidean distances
        raise NotImplementedError("Only with Distance matrix so far")
    else:
        # if there is a distance matrix
        if np.shape(dist_mat)[0] != noc:
            raise ValueError('Mutual distance matrix size and data set size do not match')


    # alpha and lambda
    alpha = potency_curve(alpha0, alpha0 / 100, train_len)

    if lambda0 is None:
        lambda0 = np.max(st) * 3

    lambdas = potency_curve(lambda0, 0.01, train_len)


    # ------------------- Action ------------------------

    k = 0 #fprintf(2, 'iterating: %d / %d epochs\r', k, epochs);

    for i in range(train_len):
        ind = sample_inds[i]  # sample index
        dx = dist_mat[:, ind]  # mutual distances in input space
        known = np.nonzero(np.logical_not(np.isnan(dx)))  # known distances

        if np.size(known) > 0:
            # sample vector's projection
            y = projection[ind, :]

            # distances in output space
            Dy = np.squeeze(projection[known, :] - y)
            dy = np.sqrt(np.sum(np.power(Dy,2),axis=1))

            # relative effect
            dy[dy == 0] = 1  # to get rid of div - by - zero's
            fy = np.exp(-dy / lambdas[i]) * (dx[known] / dy - 1)

            # Note that the function F here is e ^ (-dy /lambda))
            # instead of the bubble function 1(lambda -dy) used in the
            # paper.

            # Note that here a simplification has been made: the derivatives of the
            # F function have been ignored in calculating the gradient of error
            # function w.r.t.to changes in dy.

            # update
            projection[known, :] = np.squeeze(projection[known, :]) + alpha[i] * fy[:, np.newaxis] * Dy


        # track
        if np.remainder(i, noc) == 0:
            k = k + 1  # fprintf(2, 'iterating: %d / %d epochs\r', k, epochs);


    # -----------  Clear up -------------

    # calculate error
    # c_error = cca_error(P, Mdist, lambda (train_len));
    # fprintf(2, '%d iterations, error %f          \n', epochs, c_error);

    # set projections of totally unknown vectors as unknown
    unknown = np.sum(np.isnan(data), axis=1) == num_dim
    projection[unknown, :] = np.NaN

    return projection
