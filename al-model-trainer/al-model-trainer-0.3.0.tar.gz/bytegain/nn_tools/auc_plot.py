"""
Plots AUC for binary classifier
"""

import numpy
import numpy.ma
import matplotlib
import sys
import csv
import random
from scipy.stats import binom
from sklearn import metrics
from enum import Enum
import json
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def create_total_pos(results):
    """Returns a list of cumulative fraction of positive examples.
    The lengt of the list is max(1, number of negative examples)"""
    length = len(results)
    #total_pos = numpy.zeros([length], dtype=numpy.float)
    total_pos = [0.0]
    for i in range(0, length):
        pos = results[i]['label']
        if pos:
            total_pos[-1] += 1
        else:
            total_pos.append(total_pos[-1])
    pos_count = total_pos[-1]
    if length == 0 or pos_count == 0:
        raise Exception("WARNING: bad data for results,total_pos: %d %d"% (length, pos_count))

    total_pos = numpy.array(total_pos)
    total_pos /= pos_count
    return total_pos

def compute_auc(results):
    y_true = [result['label'] for result in results]
    y_pred = [result['probability'] for result in results]
    # y_pred_label = [1 if result['probability'] > 0.5 else 0 for result in results]
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    return metrics.auc(fpr, tpr)

def compute_avgpr(results):
    y_true = [result['label'] for result in results]
    y_pred = [result['probability'] for result in results]
    return metrics.average_precision_score(y_true, y_pred, average='macro', pos_label=1, sample_weight=None)

def compute_metrics(results, threshold=0.5):
    y_true = [result['label'] for result in results]
    y_pred = [result['probability'] for result in results]
    y_pred_label = [1 if result['probability'] > threshold else 0 for result in results]

    metrs = {
        'precision': metrics.precision_score(y_true, y_pred_label),
        'recall': metrics.recall_score(y_true, y_pred_label),
        'accuracy': metrics.accuracy_score(y_true, y_pred_label)
    }

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    metrs['auc'] = metrics.auc(fpr, tpr)
    # Find fpr and tpr for a given threshold
    thresholds = thresholds.tolist()
    index = binary_search_reverse(thresholds, threshold)
    metrs['false_positive_rate'], metrs['true_positive_rate'] = fpr[index], tpr[index]

    # All metrics are numpy floats - convert them to python float
    for key, value in list(metrs.items()):
        metrs[key] = value.item()

    conf_mtr = metrics.confusion_matrix(y_true, y_pred_label)
    metrs['confusion_mtr'] = numpy.ndarray.tolist(conf_mtr)
    return metrs

def f_beta_DLMavg(results, beta = 10.):
    DML_percentile_threshold_probs=numpy.array([0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
       0.      , 0.      , 0.      , 0.      , 0.402825, 0.003687,
       0.003746, 0.00376 , 0.003645, 0.003678, 0.003759, 0.003719,
       0.003748, 0.003817, 0.003933, 0.003818, 0.003895, 0.003837,
       0.003955, 0.003887, 0.003946, 0.004022, 0.004067, 0.00413 ,
       0.004172, 0.004195, 0.00427 , 0.004361, 0.004027, 0.004638,
       0.004199, 0.004423, 0.004721, 0.004675, 0.004576, 0.004782,
       0.004783, 0.004899, 0.004948, 0.005073, 0.004973, 0.005121,
       0.005178, 0.005303, 0.005236, 0.005507, 0.005454, 0.005642,
       0.00556 , 0.005712, 0.005857, 0.005961, 0.005962, 0.006164,
       0.006051, 0.006261, 0.006179, 0.006486, 0.006486, 0.006648,
       0.006605, 0.006878, 0.006806, 0.006984, 0.006837, 0.007116,
       0.007016, 0.007083, 0.007754, 0.007751, 0.008233, 0.007815,
       0.008068, 0.008309, 0.007567, 0.007302, 0.007548, 0.007272,
       0.00729 , 0.008005, 0.007244, 0.006954, 0.00716 , 0.007044,
       0.007023, 0.006936, 0.006849, 0.007081, 0.007206, 0.00756 ,
       0.007932, 0.008628, 0.010169, 0.011799, 0.077819])
    sort_results_asc(results)
    fb_sum=0
    y_true = [result['label'] for result in results]
    length_res = len(results)
    for j,result in enumerate(results):
        result['perc'] = j/length_res
    for i,frac in enumerate(numpy.arange(0.0,1.01,0.01)):
        y_pred_label = [1 if result['perc']  > frac else 0 for result in results]
        fb = metrics.fbeta_score(y_true, y_pred_label, beta)
        fb_sum += fb*DML_percentile_threshold_probs[i]
    return fb_sum


def compute_TPFN_Thresholds(results, minority_class_proportion = False, sample_size = 200000):
    print('total results size: ', len(results))
    if minority_class_proportion:
        #sample_size = min(len(results),sample_size)
        result_pos = [result for result in results if result['label'] >0.99]
        result_neg = [result for result in results if result['label'] <0.99]
        try:
            print('positive results size: ', len(result_pos))
            print('negative results size: ', len(result_neg))
            print('minority class fraction: ', minority_class_proportion)
            print('desired sample size: ', sample_size)
            result_pos_sample = random.sample(result_pos, min(len(result_pos),int(minority_class_proportion*sample_size)))
            print('pos sampling ok')
            result_neg_sample = random.sample(result_neg, min(int(1.0*len(result_pos_sample)/(minority_class_proportion) - 1.0*len(result_pos_sample)),len(result_neg)))
            print('neg sampling ok')
            results = result_pos_sample + result_neg_sample
        except:
            print('uh oh, sample size is trying to be bigger than results')
        
    sort_results_asc(results)
    y_true = [result['label'] for result in results]
    len_results = len(y_true)
    y_pred = [result['probability'] for result in results]
    y_true = numpy.array(y_true)
    y_pred =numpy.array(y_pred)
    metrics_list = []
    TP_list = []
    FP_list = []
    TN_list = []
    FN_list = []
    TP=0
    FP=0
    TN = 0
    FN = 0
    for ind,threshold in enumerate(y_pred):
        if y_true[ind]==1:
            FN+=1
        else:
            TN+=1
        if y_true[len_results - ind-1]==1:
            TP+=1
        else:
            FP+=1
        FN_list.append(FN)
        TN_list.append(TN)
        FP_list.append(FP)
        TP_list.append(TP)
    metrics_list = [['threshold','TN','FN','TP','FP']] + numpy.array([y_pred, TN_list, FN_list, TP_list[::-1], FP_list[::-1]]).T.tolist()
    return metrics_list

def net_revenue(obs_revenue,TP,FN,FP,value_TP,value_FP): 
    return obs_revenue*(1- FN/TP - (value_FP/value_TP)*(FP/TP))

def compute_revenue_voltage(results, minority_class_proportion = False, sample_size = 35000):
    DLM_list = [0.      , 0.      , 0.      , 0.      , 0.      , 0.      ,
       0.      , 0.      , 0.      , 0.      , 0.402825, 0.003687,
       0.003746, 0.00376 , 0.003645, 0.003678, 0.003759, 0.003719,
       0.003748, 0.003817, 0.003933, 0.003818, 0.003895, 0.003837,
       0.003955, 0.003887, 0.003946, 0.004022, 0.004067, 0.00413 ,
       0.004172, 0.004195, 0.00427 , 0.004361, 0.004027, 0.004638,
       0.004199, 0.004423, 0.004721, 0.004675, 0.004576, 0.004782,
       0.004783, 0.004899, 0.004948, 0.005073, 0.004973, 0.005121,
       0.005178, 0.005303, 0.005236, 0.005507, 0.005454, 0.005642,
       0.00556 , 0.005712, 0.005857, 0.005961, 0.005962, 0.006164,
       0.006051, 0.006261, 0.006179, 0.006486, 0.006486, 0.006648,
       0.006605, 0.006878, 0.006806, 0.006984, 0.006837, 0.007116,
       0.007016, 0.007083, 0.007754, 0.007751, 0.008233, 0.007815,
       0.008068, 0.008309, 0.007567, 0.007302, 0.007548, 0.007272,
       0.00729 , 0.008005, 0.007244, 0.006954, 0.00716 , 0.007044,
       0.007023, 0.006936, 0.006849, 0.007081, 0.007206, 0.00756 ,
       0.007932, 0.008628, 0.010169, 0.011799, 0.077819]
    print('total results size: ', len(results))
    if minority_class_proportion:
        result_pos = [result for result in results if result['label'] >0.99]
        result_neg = [result for result in results if result['label'] <0.99]
        try:
            result_pos_sample = random.sample(result_pos, min(len(result_pos),int(minority_class_proportion*sample_size)))
            result_neg_sample = random.sample(result_neg, min(int(1.0*len(result_pos_sample)/(minority_class_proportion) - 1.0*len(result_pos_sample)),len(result_neg)))
            results = result_pos_sample + result_neg_sample
        except:
            print('uh oh, sample size is trying to be bigger than results')
        
    sort_results_asc(results)
    y_true = [result['label'] for result in results]
    len_results = len(y_true)
    y_pred = [result['probability'] for result in results]
    y_true = numpy.array(y_true)
    y_pred =numpy.array(y_pred)
    metrics_list = []
    TP_list = []
    FP_list = []
    TN_list = []
    FN_list = []
    perc_list = []
    TP=0
    FP=0
    TN = 0
    FN = 0
    for ind,threshold in enumerate(y_pred):
        if y_true[ind]==1:
            FN+=1
        else:
            TN+=1
        if y_true[len_results - ind-1]==1:
            TP+=1
        else:
            FP+=1
        FN_list.append(FN)
        TN_list.append(TN)
        FP_list.append(FP)
        TP_list.append(TP)
        perc_list.append(ind/len_results)
    TP_list=TP_list[::-1]
    FP_list=FP_list[::-1]
    metric_dict = {}
    metric_dict['eTN'] = 0
    metric_dict['eTP'] = 0
    metric_dict['eFN'] = 0
    metric_dict['eFP'] = 0
    perc_index_list = numpy.searchsorted(perc_list, numpy.arange(0.0001,1.001,0.01).tolist(), side='left')-1
    for i,perc_index in enumerate(perc_index_list):
        metric_dict['eTN'] += (TN_list[perc_index]*DLM_list[i])
        metric_dict['eTP'] += (TP_list[perc_index]*DLM_list[i])
        metric_dict['eFN'] += (FN_list[perc_index]*DLM_list[i])
        metric_dict['eFP'] += (FP_list[perc_index]*DLM_list[i])
    return net_revenue(100,metric_dict['eTP'],metric_dict['eFN'],metric_dict['eFP'],350,1)

def binarysearch(sequence, value):
    lo, hi = 0, len(sequence) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sequence[mid] < value:
            lo = mid + 1
        elif value < sequence[mid]:
            hi = mid - 1
        else:
            return mid
    return None

# Binary search in a reversely sorted array/list 'a' for the index of the element closest in value to 'x'
def binary_search_reverse(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        mid_element = a[mid]
        if mid_element > x:
            lo = mid+1
        else:
            hi = mid
    return lo

def sort_results(results):
    results.sort(key=lambda v: v['probability'], reverse=True)

def sort_results_asc(results):
    results.sort(key=lambda v: v['probability'], reverse=False)

"""
Computes actual & predicted values for each "bucket" in the sorted
result list.
bucket_fractions is an array of floats, where each value represents
the fraction of results to use for that bucket.
bucket_fractions should sum to <1 (the remainder is used for the last bucket)
"""


def get_buckets(results, bucket_fractions):
    count = len(results)
    # Last bucket is "remainer"
    bucket_count = len(bucket_fractions) + 1
    breakpoints = [0] * bucket_count
    fraction_sum = 0.0
    for i in range(len(bucket_fractions)):
        fraction_sum += bucket_fractions[i]
        breakpoints[i] = int(fraction_sum * count)

    breakpoints[len(bucket_fractions)] = count
    actual = []
    predicted = []
    confidence = []
    prev_end = 0
    for i in range(bucket_count):
        bucket_size = breakpoints[i] - prev_end
        pred_sum = 0.0
        actual_sum = 0.0
        for j in range(prev_end, breakpoints[i]):
            pred_sum += results[j]['probability']
            if results[j]['label']:
                actual_sum += 1.0

        actual_val = actual_sum / bucket_size
        actual.append(actual_val)
        predicted.append(pred_sum / bucket_size)
        conf = binom.interval(0.95, bucket_size, actual_val)
        confidence.append(conf[1] / bucket_size - actual_val)
        prev_end = breakpoints[i]

    return actual, predicted, confidence

def save_predictions(results, filename="true_and_pred.csv"):
    true_pred_list = [['event_id','prob_predict','true_outcome']]
    length = len(results)
    sort_results_asc(results)
    for i in range(length):
        pred = results[i]['probability']
        if results[i]['label']:
            true_outcome = 1.0
        else:
            true_outcome = 0.0
        event_id = results[i]['id']
        true_pred_list += [[event_id, pred, true_outcome]]
    with open(filename, "w", newline="") as g:
            writer = csv.writer(g)
            writer.writerows(true_pred_list) 


def plot_predicted_vs_actual(filename, results, smoothing=500):
    print("Plot datapoints: %d Smoothing: %d" % (len(results), smoothing))
    length = len(results)
    preds = []
    leases = []
    np_lease = numpy.zeros([length])
    np_prob = numpy.zeros([length])
    for i in range(length):
        np_prob[i] = results[i]['probability']
        if results[i]['label']:
            np_lease[i] = 1.0

    for i in range(length - smoothing):
        leases.append(numpy.ma.average(np_lease[i:i + smoothing]))
        preds.append(numpy.ma.average(np_prob[i:i + smoothing]))
    do_plot_predicted_vs_actual(filename, preds, leases)


def do_plot_predicted_vs_actual(filename, predictions, actual, x_values, use_percent=True, x_axis_label=None, y_axis_label=None):
    length = len(predictions)
    assert length > 1
    # print "input length: %d" % length
    plt.clf()
    if use_percent:
        predictions = [x * 100 for x in predictions]
        actual = [x * 100 for x in actual]

    max_val = max([predictions[0], actual[0], predictions[-1], actual[-1]]) * 1.1
    plt.subplots_adjust(left=0.1, right=0.97, top=0.98, bottom=0.09, wspace=0.0, hspace=0.0)
    # print ("length: %s" % str(length + (length / 10 - 1)))
    xrange = numpy.arange(0, 11)
    xrange = xrange * (length) / 10.0
    # print "predictions: %s" % str(predictions)
    plt.xticks(xrange)
    ax = plt.gca()
    if use_percent:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3d%%" % (float(x) * 100 / (length))))
    else:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3.1f" % (float(x) / (length))))
    ax.set_ylim([0, max_val])
    ax.set_autoscale_on(False)
    plt.grid(b=True, which='major', axis='y', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    lines = []
    if x_axis_label != None:
        plt.xlabel(x_axis_label)

    if y_axis_label != None:
        plt.ylabel(y_axis_label)
    # Reverse x values so plot goes Up & to the Right.
    x_values = [length - x for x in x_values]
    line, = plt.plot(x_values, predictions, "b-", linewidth=1, antialiased=True, label="predictions")
    lines.append(line)
    if actual != None:
        # plot_x = numpy.arange(0, length, length / float(len(actual)))
        line, = plt.plot(x_values, actual, "g-", linewidth=1, antialiased=True, label="actual")
        lines.append(line)
    plt.legend(handles=lines)
    plt.savefig(filename, dpi=300)


def get_predicted_vs_actual(results, points=None, min_positive_per_point = 100):
    length = len(results)

    # Compute the minimum # of samples per point.
    # We want 1000 positive (or negative if they are rarer) examples per point.
    actual = 0
    for j in range(0, length):
        if results[j]['label']:
            actual += 1.0

    if actual < min_positive_per_point * 3:
        min_positive_per_point = actual / 3

    if points is not None:
        delta = float(length)/points
        stop_points = [int(i * delta) - 1 for i in range(1, points+1)]
    else:
        stop_points = []

    min_distance = length / 100
    actual_points = []
    pred_points = []
    ece = 0.0  # Expected calibration error
    x_values = []
    last_point = 0
    pred = 0.0
    actual = 0.0
    # Compute positive rate in top 10% bucket
    actual_ten_percent = 0.0
    count_ten_percent = int(len(results)*0.1)
    for i, point in enumerate(results):
        pred += results[i]['probability']
        if results[i]['label']:
            if i < count_ten_percent:
                actual_ten_percent += 1.0
            actual += 1.0

        if (((actual > min_positive_per_point and i - last_point > min_distance) or i == len(results) - 1) and points is None) or i in stop_points:
            count = i - last_point + 1
            accuracy = actual / count  # accuracy
            confidence = pred / count  # confidence
            ece += count * abs(accuracy - confidence)

            # Hack so end points are 0%/100%
            x_values.append( float(i) if i == len(results) -1 else float(last_point))
            actual_points.append(accuracy)
            pred_points.append(confidence)
            last_point = i
            actual = 0.0
            pred = 0.0

    ece = ece / length

    print("Positive rate in top 10 percent: %s " % (actual_ten_percent/count_ten_percent))

    x_values = [(x * len(x_values)) / length for x in x_values]
    # print "Expected Calibration Error: %.4f." % ece
    return ece, pred_points, actual_points, x_values


def plot_predicted_vs_actual2(filename, results, points=None, use_percent=True, x_axis_label=None, y_axis_label=None):
    ece, pred_points, actual_points, x_values = get_predicted_vs_actual(results, points)
    do_plot_predicted_vs_actual(filename, pred_points, actual_points, x_values, use_percent, x_axis_label, y_axis_label)
    return ece


class PlotType(Enum):
    percent = 'percent'
    odds_ratio = 'odds_ratio'
    percent_of_total = 'percent_of_total'

    def __str__(self):
        return self.value

def plot_by_segment(filename, results, y_axis_label = None, title = None, plot_type = PlotType.percent_of_total,
                    buckets = None):
    """

    :param filename: Image file to create
    :param results: Sorted result set
    :param y_axis_label: Graph label for y Axis
    :param title: Plot title
    :return: sums: Ratio/percentage of positive events in each bucket
    """
    if buckets == None:
        buckets = (0.2, 0.2, 0.2, 0.2, 0.2)
    plt.clf()
    fig, ax = plt.subplots()
    labels = ('Very High', 'High', 'Med', 'Low', 'Lowest')
    labels = labels[0:len(buckets)]
    labels_perc = []
    for i in range(len(buckets)):
        labels_perc.append(labels[i]+'\n'+str(int(buckets[i]*100))+'%')
    buckets = numpy.array(buckets)
    cumsum = numpy.cumsum(buckets)
    length = len(results)
    y_pos = numpy.arange(len(labels))
    sums = []
    current_count = 0.0
    current_sum = 0.0
    target =  cumsum[0] * length
    total_positive = 0.0
    for example in results:
        if example['label']:
            total_positive +=1

    if total_positive == 0.0:
        raise Exception("No positive results")

    print("Plot type: %s           " % plot_type)
    if plot_type == PlotType.odds_ratio:
        total = 0
        for result in results:
            if result['label']:
                total += 1
        average = total / float(length)
        multiplier = 1.0 / average
    elif plot_type == PlotType.percent:
        multiplier = 100
    elif plot_type == PlotType.percent_of_total:
        multiplier = 100
    else:
        raise Exception("Unknown plot_type: %s %s" % (plot_type, type(plot_type)))

    for i in range(length):
        current_count += 1
        if results[i]['label']:
            current_sum += 1
        if i <= target and (i+1) > target or i == length - 1:
            if plot_type == PlotType.percent_of_total:
                sums.append(current_sum / total_positive * multiplier)
            else:
                sums.append(current_sum / current_count * multiplier)

            current_sum = 0.0
            current_count = 0.0
            if len(sums) < len(buckets):
                target = cumsum[len(sums)] * length

    plt.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.13, wspace=0.0, hspace=0.0)
    bars = plt.bar(y_pos, sums, align='center', alpha=0.5)
    for bar in bars:
        height = bar.get_height()
        bottom, top = ax.get_ylim()
        yrange = (top - bottom)
        if height > bottom + yrange * 0.8:
            print_height = height - yrange * 0.06
        else:
            print_height = height + yrange * 0.03
        ax.text(bar.get_x() + bar.get_width()/2., print_height,
                ('%.1f%%' % height) if plot_type in (PlotType.percent_of_total, PlotType.percent) else ("%4.2fx" % height),
                ha='center', va='bottom')

    plt.xticks(y_pos, labels_perc)
    plt.xlabel("User Segment (Best to Worst)")
    # plt.ylabel(y_axis_label)
    if plot_type == PlotType.odds_ratio:
        plt.ylabel("Purchase odds vs average user")
    elif plot_type == PlotType.percent_of_total:
        plt.ylabel("Percent of total positive samples")
    else:
        plt.ylabel("Percent positive in segment")

    if title:
        plt.title(title)
    plt.savefig(filename, dpi=300)
    return sums


def plot_auc(filename, results, results2=None, results3=None, x_label=None, y_label=None,
             labels=None):
    plt.clf()
    total_pos = create_total_pos(results)
    length = len(total_pos)
    if results2 != None:
        total_pos2 = create_total_pos(results2)
    if results3 != None:
        total_pos3 = create_total_pos(results3)

    if x_label == None and y_label == None:
        plt.subplots_adjust(left=0.05, right=0.98, top=0.97, bottom=0.08, wspace=0.0, hspace=0.0)
    else:
        plt.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.09, wspace=0.0, hspace=0.0)

    xticks = numpy.arange(length + 0.001, step=length / 10.0)
    plt.xticks(xticks)
    plt.yticks(numpy.arange(0, 1, step=0.1))
    ax = plt.gca()
    ax.set_autoscale_on(False)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: "%3.1f" % (float(x) / length)))
    plt.grid(b=True, which='major', axis='y', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    plt.grid(b=True, which='major', axis='x', color='0.3', linestyle='-', alpha=0.3, linewidth=0.3)
    plt.plot([0, length - 1], [0, 1], "r-", linewidth=0.2, antialiased=True)

    if y_label:
        ax.set_ylabel(y_label)

    if x_label:
        ax.set_xlabel(x_label)

    plt.plot(total_pos, "b-", linewidth=0.5, antialiased=True, label=labels[0] if labels else None)
    if results2 != None:
        plot_x = numpy.arange(0, length, length / float(len(total_pos2)))
        plt.plot(plot_x, total_pos2, "g-", linewidth=0.5, antialiased=True, label=labels[1] if labels else None)
    if results3 != None:
        plot_x = numpy.arange(0, length, length / float(len(total_pos3)))
        plt.plot(plot_x, total_pos3, "k-", linewidth=0.5, antialiased=True, label=labels[2] if labels else None)

    if labels:
        plt.legend(loc='upper left')
    plt.savefig(filename, dpi=300)
