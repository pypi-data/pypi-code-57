import argparse
import csv


def read_predictions(file):
    """
    Read csv with user_id, email and prediction into a hash table
    :param file: (string) Path to a local file.
    :return: predictions, max_val: (dict, float) Return hash table with predictions and rankings along with
    maximum prediction
    """
    predictions = {}
    max_val = 0.0
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row_i, row in enumerate(csv_reader):
            user_id = row[0]
            pred = float(row[2])
            predictions[user_id] = {'pred': pred, 'rank': row_i}
            if pred > max_val:
                max_val = pred
    return predictions, max_val


def compare_predictions(file1, file2):
    """
    Compare predictions from two csv files
    :param file1: (string) Path to file1
    :param file2: (string) Path to file2
    :return:
    """
    results1, max_val1 = read_predictions(file1)
    results2, max_val2 = read_predictions(file2)

    average_norm_diff = 0.0
    average_diff = 0.0
    average_rank_diff = 0.0
    for key in list(results1.keys()):
        pred1 = results1[key]['pred']
        pred2 = results2[key]['pred']

        rank1 = results1[key]['rank']
        rank2 = results2[key]['rank']

        average_norm_diff += abs(pred1/max_val1 - pred2/max_val2)
        average_diff += abs(pred1 - pred2)
        average_rank_diff += abs(rank1 - rank2)
    print("Average difference in normalized predictions: %.4f" % (average_norm_diff / len(results1)))
    print("Average difference in absolute predictions: %.4f" % (average_diff / len(results1)))
    print("Average difference in ranking: %.4f" % (average_rank_diff / len(results1)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('--file1', required=True)
    parser.add_argument('--file2', required=True)

    args = parser.parse_args()

    compare_predictions(args.file1, args.file2)