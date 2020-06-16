"""
Bootstrap AUC confidence intervals.

Example:

python calc.py --input al_data_both_smooth.csv --group model --prediction score --label leased --iterations 10

"""
import argparse
import csv
import sklearn.metrics
import numpy as np

from collections import defaultdict

parser = argparse.ArgumentParser(description='Bootstrap AUC confidence intervals')
parser.add_argument('--input', type=str, required=True, help='Input filename')
parser.add_argument('--group', type=str, required=True, nargs='+', help='Columns to concatenate to construct group name')
parser.add_argument('--prediction', type=str, required=True, help='Column name of prediction')
parser.add_argument('--label', type=str, required=True, help='Column name of label')
parser.add_argument('--iterations', type=int, default=1000, help='Number of bootstrap iterations')
parser.add_argument('--filter_groups', type=str, nargs='+', help='Filter to id set available for all specified groups')
parser.add_argument('--filter_id', type=str, nargs='+', help='Columns to concatenate to construct id filtering.')
args = parser.parse_args()

group_predictions = defaultdict(list)
group_labels = defaultdict(list)
group_ids = defaultdict(list)

with open(args.input) as f:
    reader = csv.reader(f)
    header = next(reader)

    group_index_list = [header.index(i) for i in args.group]
    prediction_index = header.index(args.prediction)
    label_index = header.index(args.label)
    id_index_list = [header.index(i) for i in args.filter_id] if args.filter_id else None

    predictions = []
    labels = []
    for row in reader:
        group = ':'.join([row[i] for i in group_index_list])
        if row[prediction_index] == '':
            # TODO: What is this?
            continue
        group_predictions[group].append(float(row[prediction_index]))
        group_labels[group].append(int(row[label_index]))
        if id_index_list:
            id_str = ':'.join([row[i] for i in id_index_list])
            group_ids[group].append(id_str)

if args.filter_groups:
    print("Filtering to ids shared by all of %s..." % ' '.join(args.filter_groups))
    shared_ids = set(group_ids[args.filter_groups[0]])
    for group in args.filter_groups[1:]:
        shared_ids.intersection_update(group_ids[group])
    print("Filtered to %d ids." % len(shared_ids))
    for group in sorted(group_predictions.keys()):
        indexes = np.array([i for i in range(len(group_ids[group])) if group_ids[group][i] in shared_ids])
        group_predictions[group] = [group_predictions[group][x] for x in indexes]
        group_labels[group] = [group_labels[group][x] for x in indexes]
        group_ids[group] = [group_ids[group][x] for x in indexes]

print("Bootstrapping 90%% intervals with %d iterations..." % args.iterations)
for name in sorted(group_predictions.keys()):
    labels = np.array(group_labels[name])
    predictions = np.array(group_predictions[name])

    if args.filter_groups and name not in args.filter_groups:
        continue

    rate_list = []
    auc_list = []
    logloss_list = []
    for iteration in range(args.iterations):
        # Re-sample with replacement
        which = np.random.choice(len(predictions), len(predictions))
        rate_list.append(np.mean(labels[which]))
        try:
            auc_list.append(sklearn.metrics.roc_auc_score(labels[which], predictions[which]))
        except ValueError:
            auc_list.append(0.5)

        pred = predictions[which]
        logloss_list.append(sklearn.metrics.log_loss(labels[which], np.array([np.subtract(1, pred), pred]).T))

    rate_list = sorted(rate_list)
    auc_list = sorted(auc_list)
    logloss_list = sorted(logloss_list)
    print(("%s samples:%6d rate:%.3f [%.3f .. %.3f] auc:%.3f [%.3f .. %.3f] logloss:%.3f [%.3f .. %.3f]" % (
                    name,
                    len(predictions),
                    np.mean(rate_list),
                    rate_list[args.iterations * 5 / 100],
                    rate_list[args.iterations * 94 / 100],
                    np.mean(auc_list),
                    auc_list[args.iterations * 5 / 100],
                    auc_list[args.iterations * 94 / 100],
                    np.mean(logloss_list),
                    logloss_list[args.iterations * 5 / 100],
                    logloss_list[args.iterations * 94 / 100])))
