import gmtb.dpe.reconstruction
import gmtb.util as util


# wrapper for the reconstruction methods
# returns:
#   rec_obj - the reconstructed object
#   best_value - SOD of the reconstructed object
def reconstruct(object_vector, embedding, object_set, dist_func, weighted_mean_func, rec_type):

    # TODO check input

    # TODO check embedding

    # if only one object: nothing to do
    if len(object_set) == 1:
        return object_set[0], 0

    # do reconstruction
    if rec_type == "linear":
        return gmtb.dpe.reconstruction.linear(object_vector, embedding, object_set, dist_func, weighted_mean_func, 2)

    elif rec_type == "triangular":
        return gmtb.dpe.reconstruction.linear(object_vector, embedding, object_set, dist_func, weighted_mean_func, 3)

    elif rec_type == "linear_recursive":
        return gmtb.dpe.reconstruction.linear_recursive(object_vector, embedding, object_set, dist_func, weighted_mean_func)

    elif rec_type == "triangular_recursive":
        return gmtb.dpe.reconstruction.triangular_recursive(object_vector, embedding, object_set, dist_func, weighted_mean_func)

    elif rec_type == "linear_search_linear_recursive":
        rec_obj, best_val = gmtb.dpe.reconstruction.triangular_recursive(object_vector, embedding, object_set,
                                                                dist_func, weighted_mean_func)
        return util.linear_search(rec_obj, object_set, dist_func, weighted_mean_func)

    else:
        raise ValueError("reconstruct: rec_type not found")

    # TODO: what to do in case of unsuccessfull reconstruction?
