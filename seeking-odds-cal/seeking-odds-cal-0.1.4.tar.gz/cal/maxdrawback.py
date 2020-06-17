import numpy as np


def maxdrawback(data):
    index_end = np.argmax(np.maximum.accumulate(data) - data)  # end position
    if index_end == 0:
        return 0
    index_beg = np.argmax(data[:index_end])  # begin position
    maxdrawvalue = data[index_end] - data[index_beg]
    maxdrawpercent = maxdrawvalue / data[index_beg] * 100
    return maxdrawpercent


def drawdown_list(data_list):
    """返回列表回撤率"""
    data_list = np.array(data_list)
    maxac = np.zeros(len(data_list))
    max_value = data_list[0]
    maxdrawdown_list = []
    for i in range(0, len(data_list)):  # 遍历数组，当其后一项大于前一项时
        if data_list[i] > max_value:
            max_value = data_list[i]
        maxac[i] = max_value
        if i == 0:
            maxdrawdown_list.append(0)
            continue
        start_idx = np.argmax(data_list[: i + 1])
        maxdrawdown_list.append(
            (data_list[start_idx] - data_list[i]) / data_list[start_idx]
        )

    return maxdrawdown_list
