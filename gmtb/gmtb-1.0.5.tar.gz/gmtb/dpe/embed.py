import gmtb.dpe.embedding
from gmtb.util import pdist
import numpy as np
import sklearn.manifold


def embed(object_set, embedding_type, num_dim, dist_func, dist_mat = None):

    # check input
    num_dim = round(num_dim)

    # do embedding
    if embedding_type == "fastmap":
        #TODO: testing
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        emb = gmtb.dpe.embedding.fastmap(dist_mat.copy(), num_dim)

    elif embedding_type == "metricmap":
        emb = gmtb.dpe.embedding.metricmap(object_set,dist_func,num_dim,dist_mat)

    elif embedding_type == "sparsemap":
        emb = gmtb.dpe.embedding.sparsemap(object_set,dist_func,num_dim,dist_mat)

    elif embedding_type == "mds":
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        mds = sklearn.manifold.MDS(n_components=num_dim,metric=False,dissimilarity='precomputed')
        emb = mds.fit_transform(dist_mat)

    elif embedding_type == "sammon":
        # TODO: remove duplicates
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        emb, _ = gmtb.dpe.embedding.sammon(dist_mat, num_dim, inputdist='distance', init='random', display=0)

    elif embedding_type == "cca":
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        emb = gmtb.dpe.embedding.cca(dist_mat, num_dim, dist_mat=dist_mat)

    elif embedding_type == "t-sne":
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        tsne = sklearn.manifold.TSNE(n_components=num_dim,metric='precomputed',method='exact')
        emb = tsne.fit_transform(dist_mat)

    #TODO: Isomap,LLE from sklearn.manifold?

    elif embedding_type == "prototype":
        if dist_mat is None:
            dist_mat = pdist(object_set, dist_func)
        emb = gmtb.dpe.embedding.prototype(dist_mat, num_dim)

    else:
        raise NotImplementedError("Embedding Method not implemented")

    return emb

