import collections
import csv
import json
import numpy as np
import os
import scipy.stats


def genStats(items):
    """Given a list of str, generate stats.

    Args:
      items: list of str for a csv column.
    
    Returns:
      json dict of stat.
    """
    maybe_float = True
    maybe_int = True

    text_count = collections.defaultdict(int)
    float_vals = []
    int_vals = []
    text_vals = []
    for i in items:
        if maybe_float:
            try:
                float_val = float(i)
                float_vals.append(float_val)
            except Exception:
                # it is not a float
                maybe_float = False
                maybe_int = False
        if maybe_float and maybe_int:
            try:
                int_val = int(i)
                if int_val != float_val:
                    maybe_int = False
                else:
                    int_vals.append(int_val)
            except Exception:
                maybe_int = False
        text_vals.append(i)    
        text_count[i] += 1

    # sort text by counts
    text_counts = sorted(text_count.items(), key=lambda kv: kv[1], reverse=True)
    
    stats = {}
    if maybe_int:
        np_vals = np.array(int_vals)
        stats['type'] = 'int'
        stats['int_stats'] = {
            'avg': np.average(np_vals),
            'std': np.std(np_vals)
        }
        stats['raw'] = int_vals
    elif maybe_float:
        np_vals = np.array(float_vals)
        stats['type'] = 'float'
        stats['float_stats'] = {
            'avg': np.average(np_vals),
            'std': np.std(np_vals)
        }
        stats['raw'] = float_vals
    else:
        stats['type'] = 'str'
        stats['raw'] = text_vals
        stats['str_stats'] = text_counts

    return stats


def textToId(feature_stats):
    assert feature_stats['type'] == 'str'
    text_counts = feature_stats['str_stats']
    lookup = {}
    for idx, kv in enumerate(text_counts):
        lookup[kv[0]] = idx
    ids = []
    for text in feature_stats['raw']:
        ids.append(lookup[text])
    return ids


def getVals(feature_stats):
    if feature_stats['type'] == 'str':
        return textToId(feature_stats)
    return feature_stats['raw']
                       
    
def getCorr(feature_stats, label_stats):
    vals = np.array(getVals(feature_stats))
    labels = np.array(getVals(label_stats))
    return scipy.stats.pearsonr(vals, labels)


class CSVStats:
    """Read csv and gather stats for all columns."""
    def __init__(self, input_csv, label_col, save=False, stats_dir=None):
        self._input_csv = input_csv
        self._label_col = label_col
        self._save = save
        self._stats_dir = stats_dir
        if save:
            assert self._stats_dir
            

    def getAllStats(self, verbose=False):
        """Get stats for all columns.

        Args:
          output: set to print the stats.

        Returns:
          stats dict that contains stat for all columns.
        """
        cols = []
        data = collections.defaultdict(list)

        all_stats = {}

        with open(self._input_csv) as inp:
            reader = csv.reader(inp)
            header = True
            for row in reader:
                if header:
                    cols.extend(row)
                    header = False
                else:
                    for idx, item in enumerate(row):
                        data[cols[idx]].append(item)

        label_stats = genStats(data[self._label_col])

        for col in cols:
            stats = genStats(data[col])
            stats['corr'] = getCorr(stats, label_stats)
            if self._save:
                with open(os.path.join(self._stats_dir, col + '.json'), 'w') as out_f:
                    json.dump(stats, out_f)
            if verbose:
                stats_output = stats.copy()
                del stats_output['raw']
                print(col, stats_output)
            all_stats[col] = stats

        return all_stats
    
