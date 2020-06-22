import gmtb.dpe


def compute_median(object_set, dist_func, weighted_mean_func, emb_type, num_dim, rec_type):

    emb = gmtb.dpe.embed(object_set, emb_type, num_dim, dist_func)
    median_vector = gmtb.dpe.compute_median_vector(emb)
    median, sod = gmtb.dpe.reconstruct(median_vector, emb, object_set, dist_func, weighted_mean_func, rec_type)

    return median, sod
