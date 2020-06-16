"""
Reads in a model dump and outputs the relative importance of each feature.
"""
import csv
import argparse
import tempfile
from collections import defaultdict

def compute_features_from_dump(model):
    with open(model, "r") as input:
        reader = csv.reader(input)
        total = 0
        feature_dict = defaultdict(float)
        for line in reader:
            if len(line) < 4:
                continue
            first = line[0]
            begin = first.index('[')
            last = first.index('<')
            feature = first[begin + 1: last]
            gain_text = line[3]
            gain = float(gain_text[5:])
            feature_dict[feature] += gain
            total += gain
    results = sorted(iter(list(feature_dict.items())), key = lambda x: x[1], reverse = True)
    results = [(x[0], x[1] * 100.0 / total) for x in results]
    return results

def compute_feature_importance(xgb_model, row_handler):
    with tempfile.NamedTemporaryFile(delete = False, suffix=".dump") as temp:
        xgb_model.dump_model(row_handler, temp.name)
        results = compute_features_from_dump(temp.name)
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)

    args = parser.parse_args()
    for k,v in compute_features_from_dump(args.model):
        print("%30s: %6.3f%%" % (k, v))
