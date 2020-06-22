import numpy as np
from gmtb.util import pdist
import networkx as nx


def ewm_get_pairs(dist_mat):
    # cost matrix: negative distance and Diagonal is infinity
    #cost_matrix = -dist_mat
    #np.fill_diagonal(cost_matrix,np.inf)
    #assignment = munkres(cost_matrix).nonzero()

    g = nx.from_numpy_matrix(dist_mat)
    pairs = nx.max_weight_matching(g)

    return pairs


def ewm(dataset, dist_func, weighted_mean_func, verbose=False):
    # EWM calculates the generalized median of objects using an evolutionary weighted mean approach
    # Published in "Evolutionary Weighted Mean Based Framework for Generalized Median Computation with
    # Application to Strings"
    # by Lucas Franek and Xiaoyi Jiang
    #
    # Parameters:
    #   dataset             - Cell array of objects.
    #   dist_func           - Function handle @(o1,o2). Distance function between objects o1 and o2. Objects are
    #                         single cells from dataset
    #   weighted_mean_func  - Function handle @(o1,o2,alpha). Weighted mean function between objects. o1, o2 are
    #                         single cells, alpha is a float
    #                         between 0 and 1.
    #
    # Returns:
    #   best_object         - Resulting best object according to best_crit
    #   best_crit_value     - Sum of Distance of the best object

    # check if there is only one object
    if len(dataset) == 1:
        return dataset[0], 0

    # initialize sets. Copy to not change anything
    original_set = dataset.copy()
    dataset = dataset.copy()
    crit_values = np.sum(pdist(dataset,dist_func),axis=1).tolist()
    last_best_crit = np.inf  # max because min will be found later

    # ********************************* Parameters ********************************* #
    w = 3
    max_iter = 20
    n_max = min(20,2*len(dataset))

    # ********************************* BEGIN ITERATION ********************************* #
    iteration = 0
    stop = False
    stop_again = False

    while iteration  < max_iter and ~stop:

        iteration = iteration+1
        resSOD = []
        n = len(dataset)

        # compute Matrix of distances / similarities
        dist_mat = pdist(dataset,dist_func)

        # get pairs of objects
        pairs = ewm_get_pairs(dist_mat)

        # ********* iterate over pairs of objects *********
        for (x,y) in pairs:

            ## find best alpha for the weighted mean using linear search
            #search_crit = @(alpha) best_crit(original_set, weighted_mean_func(dataset{pairs(i,1)}, dataset{pairs(i,2)}, alpha));
            #options.TolX = last_best_crit * 0.001;
            #[alpha, ~] = fminbnd(search_crit,0,1,options);

            # use this alpha to calculate a result
            #dataset{n+i} = weighted_mean_func(dataset{pairs(i,1)}, dataset{pairs(i,2)}, alpha);
            #crit_values(n+i) = best_crit(original_set,dataset{n+i});

            ## use equidistant alphas
            for step in range(1,w+1):
                alpha = step/(1+w)
                new_obj = weighted_mean_func(dataset[x], dataset[y], alpha)
                dataset.append(new_obj)
                crit_values.append(np.sum(pdist(set1=original_set,set2=[new_obj],func=dist_func)))

        ## ********* delete from result set *********

        idx = np.argsort(crit_values)

        max_length = min(len(dataset),n_max)

        dataset = [dataset[i] for i in idx[:max_length]]
        crit_values = [crit_values[i] for i in idx[:max_length]]


        ## stopping criterium: no change for 2 iterations
        if abs(last_best_crit - crit_values[0]) <= 1e-10:
            if stop_again:
                stop = True
            else:
                stop_again = True

        else:
            last_best_crit = crit_values[0]
            stop_again = False



    # ********************************* END ITERATION ********************************* #
    if verbose:
        print('EWM terminated after %d / %d iterations' % (iteration, max_iter))

    return dataset[0], crit_values[0]