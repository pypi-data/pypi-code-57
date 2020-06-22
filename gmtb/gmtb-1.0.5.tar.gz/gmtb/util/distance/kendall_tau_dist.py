import numpy as np

#import pyximport; pyximport.install()
from gmtb.util.distance.kendall_tau_dist_cy import tau_cy, tau_matrix_cy, try_bucket_cy

# computes the kendall tau distance between rankings when rankings are encoded as index vectors
# each vector is an array r where r[i] is the bucket of value i.
# Example:
# [1], [2,4], [3,5,6] is encoded as [1, 2, 3, 2, 3, 3]
def kendall_tau_dist(r1, r2, penalty=0.5):
    assert(r1.dtype == np.int)
    assert (r2.dtype == np.int)
    return tau_cy(r1,r2,penalty)



def kendall_tau_wm(r1, r2, alpha, penalty=0.5):
    assert(r1.dtype == np.int)
    assert (r2.dtype == np.int)

    r_med = r1
    done = False

    # matrix where disagreements happen
    mat_r1 = np.zeros((len(r1), len(r1)))
    #mat_r2 = tau_matrix(r_med, r2, penalty)
    mat_r2 = tau_matrix_cy(r_med, r2, penalty)

    # current tau
    tau_r1 = 0
    tau_r2 = np.sum(mat_r2)

    # goal tau
    tau_r1_goal = alpha * tau_r2
    tau_r2_goal = (1 - alpha) * tau_r2

    #iter = 0

    # iterate all possible values and try to find a best possible mean
    while (abs(tau_r1 - tau_r1_goal) > 1e-10 or abs(tau_r2 - tau_r2_goal) > 1e-10) and not done:

        #iter = iter + 1
        #print('Iteration %d, %f %f %f %f' % (iter,tau_r1, tau_r1_goal, tau_r2, tau_r2_goal))

        best_r_med = r_med
        best_tau_r1 = tau_r1
        best_tau_r2 = tau_r2
        best_mat_r1 = mat_r1
        best_mat_r2 = mat_r2
        done = True

        disagreeing_values = np.sum(mat_r1 + mat_r2, axis=1) != 0
        for value in range(len(r_med)):
            # try full bucket
            if disagreeing_values[value]:
                for bucket in range(1,max(r_med)+1):
                    # existing bucket, skip if its already in there
                    if (r_med[value] != bucket):
                        #r_med_new, mat_r1_new, mat_r2_new, tau_r1_new, tau_r2_new = try_bucket(r1 ,r2, r_med, mat_r1, mat_r2, value, bucket, penalty, False)
                        r_med_new, mat_r1_new, mat_r2_new, tau_r1_new, tau_r2_new = try_bucket_cy(r1, r2, r_med, mat_r1,
                                                                                                  mat_r2, value, bucket,
                                                                                                  penalty, False)
                        # check if better
                        if abs(tau_r1_new - tau_r1_goal) + abs(tau_r2_new - tau_r2_goal) < abs(best_tau_r1 - tau_r1_goal) + abs(
                                best_tau_r2 - tau_r2_goal):
                            best_r_med = r_med_new
                            best_mat_r1 = mat_r1_new
                            best_mat_r2 = mat_r2_new
                            best_tau_r1 = tau_r1_new
                            best_tau_r2 = tau_r2_new
                            done = False

                    # new bucket
                    #r_med_new, mat_r1_new, mat_r2_new, tau_r1_new, tau_r2_new = try_bucket(r1 ,r2, r_med, mat_r1, mat_r2, value, bucket, penalty, True)
                    r_med_new, mat_r1_new, mat_r2_new, tau_r1_new, tau_r2_new = try_bucket_cy(r1, r2, r_med, mat_r1,
                                                                                              mat_r2, value, bucket,
                                                                                              penalty, True)
                    if abs(tau_r1_new - tau_r1_goal) + abs(tau_r2_new - tau_r2_goal) < abs(best_tau_r1 - tau_r1_goal) + abs(
                            best_tau_r2 - tau_r2_goal):
                        best_r_med = r_med_new
                        best_mat_r1 = mat_r1_new
                        best_mat_r2 = mat_r2_new
                        best_tau_r1 = tau_r1_new
                        best_tau_r2 = tau_r2_new
                        done = False

                r_med = best_r_med
                tau_r1 = best_tau_r1
                tau_r2 = best_tau_r2
                mat_r1 = best_mat_r1
                mat_r2 = best_mat_r2

    return r_med


def tau_matrix(r1, r2, penalty):
    mat = np.zeros((len(r1), len(r1)))

    for i in range(len(r1)):
        for j in range(len(r1)):
            mat[i,j] = (r1[i] < r1[j] and r2[i] > r2[j] or
                         r1[i] > r1[j] and r2[i] < r2[j]) \
                  + penalty * (r1[i] == r1[j] and r2[i] != r2[j] or
                               r1[i] != r1[j] and r2[i] == r2[j])

    return mat


# computes changes after changing the bucket
def try_bucket(r1, r2, r_med, mat_r1, mat_r2, value, bucket_index, penalty, new_bucket):

    # create copyies so we dont change anything important
    r_med_new = r_med.copy()
    mat_r1 = mat_r1.copy()
    mat_r2 = mat_r2.copy()

    # create new array
    if new_bucket:
        # move all values in bucket new_index
        move_idx = r_med_new >= bucket_index
        r_med_new[move_idx] = r_med_new[move_idx] + 1

    # set new index
    r_med_new[value] = bucket_index

    # update matrices
    for i in range(len(r_med_new)):
        mat_r1[value, i] = (r1[value] < r1[i] and r_med_new[value] > r_med_new[i] or
                            r1[value] > r1[i] and r_med_new[value] < r_med_new[i]) \
                            + penalty * (r1[value] == r1[i] and r_med_new[value] != r_med_new[i] or
                               r1[value] != r1[i] and r_med_new[value] == r_med_new[i])
        mat_r1[i, value] =  mat_r1[value, i]

        mat_r2[value, i] = (r2[value] < r2[i] and r_med_new[value] > r_med_new[i] or
                            r2[value] > r2[i] and r_med_new[value] < r_med_new[i]) \
                            + penalty * (r2[value] == r2[i] and r_med_new[value] != r_med_new[i] or
                               r2[value] != r2[i] and r_med_new[value] == r_med_new[i])
        mat_r2[i, value] = mat_r2[i, value]


    # update tau
    tau_r1 = np.sum(mat_r1)
    tau_r2 = np.sum(mat_r2)

    # return everything
    return r_med_new, mat_r1, mat_r2, tau_r1, tau_r2


# convert list of buckets to index vector
def to_index_vector(r):
    # 1 get max index
    # 2 go through each bucket and save index
    raise NotImplementedError


# convert index vector to list of buckets
def to_list(r):
    r_out = []

    for i in range(1, max(r)):
        r_out.append(r[r == i])
