"""
Example usage:
net, results = cross_validate.run(dataset, net_function)
"""

import bytegain.nn_tools.auc_plot as auc_plot

def run(dataset, create_net, batches, runs = 5):
    auc_sum = 0
    aucs = []
    test_results = []
    for run in range(runs):
        net = create_net(dataset);
        aucs.append(net.train(batches, 4000))
        test_results.extend(net.get_sorted_test_labels());
        if run < runs - 1:
            dataset.repartition()
    auc_plot.sort_results(test_results)
    auc = auc_plot.compute_auc(test_results)
    print("Total Auc: %5.3f %s" % (auc, str([("%5.3f" % a) for a in aucs])))

    return net, test_results
