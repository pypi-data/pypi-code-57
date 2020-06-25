import collections
import csv
import json
import os

import csv_stats


def item_to_tensor(col_name, stats, item):
    """Use stats[col_name] to tranform the item.

    Args:
      col_name: csv column name
      stats: dict of stats for all columns
      item: str value of the csv cell.

    Returns:
      converted cell as int / float. 
    """
    assert col_name in stats
    stat = stats[col_name]

    if stat['type'] == 'str':
        for idx, kv in enumerate(stat['str_stats']):
            if kv[0] == item:
                return idx
        return len(stat['str_stats'])
    elif stat['type'] == 'float':
        return (float(item) - stat['float_stats']['avg']) / stat['float_stats']['std']
    else:
        return (float(item) - stat['int_stats']['avg']) / stat['int_stats']['std']
            

def read_csv(fn, label_col, stats):
    """Convert data in csv to tensordict.

    Args:
      fn: name of the csv file
      label_col: column name of the label
      stats: Stats of the columns

    Returns:
      cols, tensor_dict, num_records tuple
      tensor_dict contains column name as key, list of float/int as value.
    """
    cols = []
    tensor_dict = collections.defaultdict(list)
    num_records = 0
    with open(fn) as inp:
        reader = csv.reader(inp)
        header = True
        for row in reader:
            if header:
                cols.extend(row)
                header = False
            else:
                label_found = False
                for idx, item in enumerate(row):
                    col_name = cols[idx]
                    if col_name == label_col:
                        tensor_dict[col_name].append(int(item))
                        label_found = True
                    else:
                        tensor_dict[col_name].append(
                            item_to_tensor(col_name, stats, item) * 1.0)
                num_records += 1
                if not label_found:
                    tensor_dict[label_col].append(0)

    return cols, tensor_dict, num_records


def csv_to_dataset(csv_fn, label_col, train_stats=None):
    if not train_stats:
        csvstats = csv_stats.CSVStats(csv_fn, label_col='outcome')
        train_stats = csvstats.getAllStats(verbose=True)

    cols, tensor_dict, num_records = read_csv(
        fn=csv_fn, label_col='outcome', stats=train_stats)

    train_dataset = []
    for idx in range(num_records):
        label = tensor_dict['outcome'][idx]
        one_record = []
        for col in cols:
            if col == 'outcome':
                continue
            one_record.append(tensor_dict[col][idx])
        train_dataset.append((one_record, label))

    return train_stats, train_dataset
