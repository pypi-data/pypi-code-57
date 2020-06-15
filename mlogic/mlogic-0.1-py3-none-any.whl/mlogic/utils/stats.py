"""
# Statistics functions
"""
import numpy as np
from scipy import stats
from collections import Counter


# 常用函数列举
# 皮尔逊相关系数：np.corrcoef

# def cal_correlation(X,Y):
#     '''计算皮尔逊相关系数'''
#     X = np.sampleay(X)
#     Y = np.sampleay(Y)
#     covariance = np.sum((X-X.mean())*(Y-Y.mean()))/len(X)
#     correlation_coefficients = covariance/(X.std()*Y.std())
#     return correlation_coefficients

# def cal_ttest_statistics(X,Y,critical_value = 2.18):
#     '''独立双样本异方差t统计量计算,默认临界值为2.18'''
#     Xvar = X.var(ddof = 1)      # 样本方差
#     Yvar = Y.var(ddof = 1)      # 样本方差
#     t_statistic = (X.mean() - Y.mean())/np.sqrt(Xvar/len(X) + Yvar/len(Y))      #计算t统计量
#     return t_statistic


##########################假设检验###################################


def ttest(sample1, sample2):
    """双样本学生t检验：计算双变量是否来自拥有相同均值和方差的同一总体"""
    t_statistic, p_value = stats.ttest_ind(sample1, sample2, equal_var=False)
    return p_value


def ftest(samples):
    """
    F检验：又称方差分析，计算多组数据是否来自同一总体
    如果p_value < 0，则说明不是来自同一总体
    """
    f_statistic, p_value = stats.f_oneway(*samples)
    return p_value


def chi2_contingency(category_sample1, category_sample2):
    """
    卡方检验：类别变量的独立性检验
    如果p_value < 0.05，则说明不独立，显著相关
    """
    observed = cross_value(category_sample1, category_sample2)
    chi2, p_value, dof, expctd = stats.chi2_contingency(observed)
    return p_value


def cross_value(category_sample1, category_sample2):
    num_sample1, label_map_row = label_encode(category_sample1)
    num_sample2, label_map_col = label_encode(category_sample2)
    grid = np.zeros((len(label_map_row), len(label_map_col)))
    combines = zip(num_sample1, num_sample2)
    counter = Counter(combines)
    for key in counter:
        row, col = key
        grid[row, col] = counter[key]
    return grid


def label_encode(sample):
    unique_vars = set(sample)
    label_map = dict(zip(unique_vars, range(len(unique_vars))))
    num_sample = [label_map[x] for x in sample]
    return num_sample, label_map


def cal_corrb(value_sample, group_sample):
    """
    计算分类变量与数值变量的相关系数

    Parameters
    ----------
    value_sample:arr_like
        数值变量的样本数据
    group_sample:arr_like
        分类变量的样本数据

    Returns
    -------
    corrb:float
        相关系数
    """
    wss = 0
    bss = 0
    for i in set(group_sample):
        selectvalue = value_sample[group_sample == i]
        # print selectvalue
        wss += ((selectvalue - selectvalue.mean()) ** 2).sum()
        bss += len(selectvalue) * ((selectvalue.mean() - value_sample.mean()) ** 2)
        # print wss,bss
    corrb = bss / (wss + bss)
    return corrb


# Xvar = X.var(ddof = 1)      # 样本方差
# Yvar = Y.var(ddof = 1)      # 样本方差


# def goftest(critical_value = 5.024):
#     '''分类变量的拟合优度计算'''
#     sample = table.values
#     fe = sample.sum(1)[0]*sample.sum(0)*1./sample.sum()    #计算期望值
#     chisq = (np.square(sample[0] - fe)/fe).sum()      #计算卡方统计量
#     if chisq > critical_value:      #和临界值比较,默认是0.05置信的双尾检验
#         print "significance"
#     else:
#         print "no significance"
#     return chisq


def cramerv(table):
    """基于列联表的克莱姆V相关系数"""
    sample = table.values
    sample = sample + 1.0  # 对0的处理
    expvalue = (
        sample.sum(0) * sample.sum(1).reshape(sample.shape[0], 1) / sample.sum()
    )  # 计算期望值

    chisquare = (np.square(sample - expvalue) / expvalue).sum()  # 计算卡方
    # return chisquare,expvalue
    corr = np.sqrt(
        chisquare / (sample.sum() * (min(sample.shape) - 1))
    )  # 根据卡方和自由度计算相关系数
    return corr


def manytocate(data, sample):
    """让数据集与某类别变量进行批量相关系数计算"""
    datalist = []
    for i in range(data.shape[1]):
        if type(data.ix[0, i]) is str:
            table = pd.crosstab(data.ix[:, i], sample)
            corr = cramerv(table)
            corrtype = "cramerv"
        else:
            corr = stats.pearsonr(data.ix[:, i].values, sample)
            corrtype = "corrb"
        datalist.append([corrtype, data.columns[i], round(corr, 2)])
    return pd.DataFrame(datalist, columns=["corrtype", "colname", "corr"])


##########################其他###################################


class anomaly_detection(object):
    """基于四分位的异常值监测"""

    def __init__(self, df, sample):
        self.df = df
        self.sample = sample
        self.nrow, self.ncol = self.sample.shape

    def quartile(self):
        """四分位距"""
        result = []
        for i in range(self.ncol):
            selectedsample = self.sample[:, i]
            q1, q2, q3 = np.percentile(selectedsample.astype("float"), [25, 50, 75])
            up = q3 + 1.5 * (q3 - q1)
            down = q1 - 1.5 * (q3 - q1)
            print(down, up)
            oneresult = (selectedsample > up) | (selectedsample < down)
            result.append(oneresult)
        outputds = self.df.copy()
        outputds["anomaly"] = np.sampleay(result).sum(0)
        return outputds


def pca(nsample):
    """主成分分析"""
    nsample = (nsample - nsample.mean(0)) / nsample.std(0)
    cov = np.cov(nsample, rowvar=0)
    evals, evects = np.linalg.eig(np.mat(cov))  # 计算出特征值和特征向量
    ser = pd.Series(evals)
    ser.sort(ascending=False)
    evects = evects[:, ser.index]  # 根据evals的降序排列evects
    evals = ser.values

    class result(object):
        def __init__(self, evals, evects):
            self.evals = evals
            self.evects = evects
            self.weight = np.round(evals.cumsum() / evals.sum(), 2)
            self.combnum = (self.weight < 0.8).argmin() + 1  # 选择大于累积0.8的最小维度数

        def dimreduce(self):
            return nsample * self.evects[:, : self.combnum]  # 返回降维后的数组

    return result(evals, evects)
