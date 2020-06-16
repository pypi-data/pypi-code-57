from collections import Counter
import numpy as np


def to_categorical_list(input_list):
    result = [0] * len(input_list)
    keys = {}
    for idx, el in enumerate(input_list):
        if el in keys:
            result[idx] = keys[el]
        else:
            keys[el] = len(keys)
            result[idx] = keys[el]
    return result, keys


def to_categorical_list_2d(input_list, num_of_sort=-1):
    num_list, keys = to_categorical_list(input_list)
    if num_of_sort <= 0:
        result = np.zeros(shape=(len(input_list), len(keys)))
    else:
        result = np.zeros(shape=(len(input_list), num_of_sort))
    for i in range(len(input_list)):
        result[i][num_list[i]] = 1
    return result.astype(int), keys


def change_categorical_pandas(input_pandas, categorize=None):
    num_object = 0
    num_other = 0
    strange_dict = {}
    key_result = {}
    for col_name, col_contents in input_pandas.iteritems():
        tp = col_contents.dtype
        if tp != float and tp != int:
            try:
                tmp = col_contents.astype(float)
                input_pandas[col_name] = tmp
            except ValueError:
                if tp == object:
                    num_object += 1
                else:
                    num_other += 1
                strange_dict[col_name] = Counter(col_contents)
    print("number of object column\t", num_object)
    print("number of other column\t", num_other)
    while True:
        if categorize is not None:
            var = "y"
        else:
            print("The number of columns which are not int or float :", len(strange_dict))
            print("Do you want to inspect?")
            print("y : yes / n : no / s : list of columns name")
            var = input()
        if var == "y":
            for key, value in strange_dict.items():
                while True:
                    if categorize is not None:
                        var = "1"
                    else:
                        print(key, "\t: number of sort : ", len(value))
                        var = input("categorize(1) / want to see(2) / Don't do anything(3) : ")
                    if var == "1":
                        result3, my_keys = to_categorical_list(input_pandas[key])
                        input_pandas[key] = result3
                        key_result[key] = my_keys
                        break
                    elif var == "2":
                        print(value)
                    elif var == "3":
                        break
                    else:
                        print("Press one of three options (1,2,3)")
            break
        elif var == "n":
            break
        elif var == "s":
            print(strange_dict.keys())
        else:
            print("Press one of three options (y, n, s)")
    return key_result


def row_slice(mode: int, total_length: int, split_length: int, num_of_result: int = -1,
              stride: int = -1) -> list:
    """

    Args:
        mode: 0 or 1. Mode 0 uses num_of_result, and mode 1 uses stride.
        total_length: Total length of data which you want to divide from.
        split_length: Length of row which you want to split into.
        num_of_result: The Number of result. It's valid only when mode == 0.
        stride: The stride which will be used to split the data.

    Returns:
        list: list of start points

    """
    if mode == 0:
        assert total_length >= split_length, "Too big length"
        assert num_of_result > 0, "Wrong number_of_row_data : num_of_result should be integer larger then 1."
        if num_of_result == 1:
            return [round((total_length - split_length) / 2)]
        x = (total_length - num_of_result * split_length) / (num_of_result - 1)
        starting_pts = [round(k * (split_length + x)) for k in range(num_of_result)]
        assert len(starting_pts) == len(set(starting_pts)), "Too many number_of_row_data : duplicate row made"
        return starting_pts
    if mode == 1:
        assert total_length >= split_length, "Too big length"
        assert stride > 0, "stride should be larger than 0"
        starting_pts = list(range(total_length))[:-split_length + 1:stride]
        return starting_pts


def confusion_matrix(y_true: list, y_pred: list, num_of_sort: int = None, normalize_axis: int = None) -> np.array:
    if len(y_true) != len(y_pred):
        raise ValueError("the length of y_true should be the same as the length of y_pred")
    for el1, el2 in zip(y_true, y_pred):
        if el1 < 0 or el2 < 0:
            raise ValueError("element of list should be positive integer")
    maximum_plus_1 = max(np.max(y_true), np.max(y_pred)) + 1
    if num_of_sort is None:
        result = np.zeros(shape=(maximum_plus_1, maximum_plus_1)).astype(int)
    else:
        if num_of_sort < maximum_plus_1:
            raise ValueError("num_of_sort < maximum + 1")
        result = np.zeros(shape=(num_of_sort, num_of_sort)).astype(int)
    for i in range(len(y_true)):
        result[y_true[i], y_pred[i]] += 1
    length_of_result = len(result)

    if normalize_axis is None:
        return result
    elif normalize_axis is 0:
        result = result.astype(float)
        for i in range(length_of_result):
            row_sum = np.sum(result[i])
            if row_sum != 0:
                result[i] = result[i] / row_sum
        return result
    elif normalize_axis is 1:
        result = result.astype(float)
        for i in range(length_of_result):
            column_sum = np.sum(result[:, i])
            if column_sum != 0:
                result[:, i] = result[:, i] / column_sum
        return result
    else:
        raise ValueError("normalize_axis should be either 0 or 1")


def plot_confusion_matrix(confusion_matrix_input, labels=None, vmin=None, vmax=None, cmap=None, center=None,
                          robust=False, annot=None, fmt='.2g', annot_kws=None, linewidths=0, linecolor='white',
                          cbar=True, cbar_kws=None, cbar_ax=None, square=False, xticklabels='auto', yticklabels='auto',
                          mask=None, ax=None):
    import seaborn as sn
    if labels is None:
        return sn.heatmap(confusion_matrix_input, vmin, vmax, cmap, center, robust, annot, fmt, annot_kws, linewidths,
                          linecolor, cbar, cbar_kws, cbar_ax, square, xticklabels, yticklabels, mask, ax)
    else:
        return sn.heatmap(confusion_matrix_input, vmin, vmax, cmap, center, robust, annot, fmt, annot_kws, linewidths,
                          linecolor, cbar, cbar_kws, cbar_ax, square, labels, labels, mask, ax)


def get_accuracy(y_pred: list, y_true: list) -> float:
    """
    Generate accuracy from the two inputs.
    Args:
        y_pred: prediction list or numpy array.
                It can be 2 dimensional or 1 dimensional list of integer
        y_true: true list or numpy array.
                It can be 2 dimensional or 1 dimensional list of integer

    Returns: accuracy from the inputs.

    """
    y_pred = np.array(y_pred)
    y_true = np.array(y_true)
    if len(y_pred.shape) == 2:
        y_pred = np.argmax(y_pred, axis=1)
    if len(y_true.shape) == 2:
        y_true = np.argmax(y_true, axis=1)
    return float(len(np.where(y_pred == y_true)[0])) / float(len(y_pred))
