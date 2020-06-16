import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from sortedcontainers import SortedDict
from deepcinac.utils.display import BREWER_COLORS
from deepcinac.utils.utils import get_continous_time_periods
from deepcinac.utils.cinac_file_utils import CinacFileReader
from datetime import datetime
import os
import yaml
from deepcinac.utils.signal import smooth_convolve
import hdf5storage
from scipy.stats import wilcoxon
from matplotlib.patches import Patch, Circle
from sortedcontainers import SortedDict


def build_spike_nums_dur(spike_nums, peak_nums, traces=None, fluorescence_threshold=None):
    """
    Build a "raster dur", meaning a 2d binary array (n_cells * n_frames) representing when a cell is active
    based on the onset and peak on transients. 
    Args:
        spike_nums: (2d array binary n_cells * n_frames), represent the onsets of cell activations (transients)
        peak_nums: (2d array binary n_cells * n_frames), represent the peaks of cell activations (transients)
        traces: (2d array float n_cells * n_frames) fluorescence traces of the cells
        fluorescence_threshold:  if a peak amplitude is under the threshold, we don't consider i

    Returns:

    """
    n_cells = len(spike_nums)
    n_frames = spike_nums.shape[1]
    spike_nums_dur = np.zeros((n_cells, n_frames), dtype="int8")
    for cell in np.arange(n_cells):
        peaks_index = np.where(peak_nums[cell, :])[0]
        onsets_index = np.where(spike_nums[cell, :])[0]

        for onset_index in onsets_index:
            peaks_after = np.where(peaks_index > onset_index)[0]
            if len(peaks_after) == 0:
                continue
            peaks_after = peaks_index[peaks_after]
            peak_after = peaks_after[0]

            if (traces is not None) and (fluorescence_threshold is not None):
                # if the peak amplitude is under the threshold, we don't consider it
                if traces[cell, peak_after] < fluorescence_threshold[cell]:
                    continue

            spike_nums_dur[cell, onset_index:peak_after + 1] = 1
    return spike_nums_dur


def get_raster_dur_from_traces(traces, fluorescence_threshold=None):
    """
    Allow to build a raster dur based on all putative transient from the fluorescence traces.
    :param traces:(2d array float, n_cells *n_frames) fluorescence traces
    :param fluorescence_threshold: None or otherwise 1xlen(traces) array with for each cell the threshold under which
    we should not take into account a peak and the transient associated. The value is without normalization.
    :return:
    """
    n_cells = traces.shape[0]
    n_times = traces.shape[1]

    for i in np.arange(n_cells):
        if fluorescence_threshold is not None:
            fluorescence_threshold[i] = (fluorescence_threshold[i] - np.mean(traces[i, :])) / np.std(traces[i, :])
        traces[i, :] = (traces[i, :] - np.mean(traces[i, :])) / np.std(traces[i, :])

    spike_nums_all = np.zeros((n_cells, n_times), dtype="int8")
    for cell in np.arange(n_cells):
        onsets = []
        diff_values = np.diff(traces[cell])
        for index, value in enumerate(diff_values):
            if index == (len(diff_values) - 1):
                continue
            if value < 0:
                if diff_values[index + 1] >= 0:
                    onsets.append(index + 1)
        if len(onsets) > 0:
            spike_nums_all[cell, np.array(onsets)] = 1

    peak_nums = np.zeros((n_cells, n_times), dtype="int8")
    for cell in np.arange(n_cells):
        peaks, properties = signal.find_peaks(x=traces[cell])
        peak_nums[cell, peaks] = 1

    spike_nums_dur = build_spike_nums_dur(spike_nums_all, peak_nums,
                                          traces=traces, fluorescence_threshold=fluorescence_threshold)
    return spike_nums_dur


def compute_stats_over_gt(raster_gt, raster_to_evaluate, traces, raster_predictions=None, fluorescence_threshold=None):
    """
    Compute the stats based on raster dur
    :param raster_gt: 1d binary array (n_frames or 2d binary array (n_cells, n_frames), 1 when the cell is active
    :param raster_to_evaluate: same sahpe as raster_t, binary, 1 when a cell is active
    :param traces: (1d or 2d array, same shape as raster_gt), should be smoothed, allows to detect
    :raster_predictions: same shape as raster_gt, but float array, probability that the cell is active at each
    frame. Can be None, if ground_truth is not based
    putative transients
    fluorescence_threshold: if not None, float value representing a low threshold for
        # for transients used for benchmarks (possible transients), transients below the threshold are not considered
    :return: two dicts: first one with stats on frames, the other one with stats on transients
    Frames dict has the following keys (as String):
    TP: True Positive
    FP: False Positive
    FN: False Negative
    TN: True Negative
    sensitivity or TPR: True Positive Rate or Recall
    specificity or TNR: True Negative Rate or Selectivity
    FPR: False Positive Rate or Fall-out
    FNR: False Negative Rate or Miss Rate
    ACC: accuracy
    Prevalence: sum positive conditions / total population (for frames only)
    PPV: Positive Predictive Value or Precision
    FDR: False Discovery Rate
    FOR: False Omission Rate
    NPV: Negative Predictive Value
    LR+: Positive Likelihood ratio
    LR-: Negative likelihood ratio

    transients dict has just the following keys:
    TP
    FN
    sensitivity or TPR: True Positive Rate or Recall
    FNR: False Negative Rate or Miss Rate
    """

    if raster_gt.shape != raster_to_evaluate.shape:
        raise Exception(f"both raster_gt and to_evaluate should have the same shape {raster_gt.shape} vs "
                        f"{raster_to_evaluate.shape}")
    if len(raster_gt.shape) == 1:
        # we transform them in a 2 dimensions array
        raster_gt = raster_gt.reshape(1, raster_gt.shape[0])
        raster_to_evaluate = raster_to_evaluate.reshape(1, raster_to_evaluate.shape[0])
        if raster_predictions is not None:
            raster_predictions = raster_predictions.reshape(1, raster_predictions.shape[0])
        if traces is not None:
            traces = traces.reshape(1, traces.shape[0])

    frames_stat = dict()
    transients_stat = dict()

    n_frames = raster_gt.shape[1]
    n_cells = raster_gt.shape[0]

    # full raster dur represents the raster dur built from all potential onsets and peaks
    full_raster_dur = None
    if traces is not None:
        full_raster_dur = get_raster_dur_from_traces(traces, fluorescence_threshold=fluorescence_threshold)

    # positive means active frame, negative means non-active frames
    # condition is the ground truth
    # predicted is the one computed (RNN, CaiMan etc...)

    tp_frames = 0
    fp_frames = 0
    fn_frames = 0
    tn_frames = 0

    tp_transients = 0
    fn_transients = 0
    fp_transients = 0
    tn_transients = 0

    # will keep values of the predictions of the FN and FP transients and frames
    # for transients will take median predicted value over the transient
    fn_transients_predictions = []
    fp_transients_predictions = []
    tp_transients_predictions = []
    tn_transients_predictions = []
    fn_frames_predictions = []
    fp_frames_predictions = []
    tn_frames_predictions = []
    tp_frames_predictions = []

    proportion_of_frames_detected_in_transients = []

    for cell in np.arange(n_cells):
        raster_dur = raster_gt[cell]
        predicted_raster_dur = raster_to_evaluate[cell]
        if raster_predictions is not None:
            gt_predictions_for_cell = raster_predictions[cell]
        else:
            gt_predictions_for_cell = None
        predicted_positive_frames = np.where(predicted_raster_dur)[0]
        predicted_negative_frames = np.where(predicted_raster_dur == 0)[0]

        tp_frames += len(np.where(raster_dur[predicted_positive_frames] == 1)[0])
        fp_frames += len(np.where(raster_dur[predicted_positive_frames] == 0)[0])
        fn_frames += len(np.where(raster_dur[predicted_negative_frames] == 1)[0])
        tn_frames += len(np.where(raster_dur[predicted_negative_frames] == 0)[0])

        if raster_predictions is not None:
            fp_frames_indices = np.where(raster_dur[gt_predictions_for_cell >= 0.5] == 0)[0]
            fn_frames_indices = np.where(raster_dur[gt_predictions_for_cell < 0.5] == 1)[0]
            tp_frames_indices = np.where(raster_dur[gt_predictions_for_cell >= 0.5] == 1)[0]
            tn_frames_indices = np.where(raster_dur[gt_predictions_for_cell < 0.5] == 0)[0]
            fp_frames_predictions.extend(list(gt_predictions_for_cell[fp_frames_indices]))
            fn_frames_predictions.extend(list(gt_predictions_for_cell[fn_frames_indices]))
            tp_frames_predictions.extend(list(gt_predictions_for_cell[tp_frames_indices]))
            tn_frames_predictions.extend(list(gt_predictions_for_cell[tn_frames_indices]))

        n_fake_transients = 0
        # transients section
        transient_periods = get_continous_time_periods(raster_dur)
        if full_raster_dur is not None:
            full_transient_periods = get_continous_time_periods(full_raster_dur[cell])
            fake_transients_periods = []
            # keeping only the fake ones
            for transient_period in full_transient_periods:
                if np.sum(raster_dur[transient_period[0]:transient_period[1] + 1]) > 0:
                    # it means it's a real transient
                    continue
                fake_transients_periods.append(transient_period)

            n_fake_transients = len(fake_transients_periods)
        # positive condition
        n_transients = len(transient_periods)
        tp = 0
        for transient_period in transient_periods:
            frames = np.arange(transient_period[0], transient_period[1] + 1)
            if np.sum(predicted_raster_dur[frames]) > 0:
                tp += 1
                # keeping only transients with one frame detected
                proportion_of_frames_detected_in_transients.append((np.sum(predicted_raster_dur[frames]) / len(frames))
                                                                   * 100)

            if raster_predictions is not None:
                if np.max(gt_predictions_for_cell[frames]) >= 0.5:
                    # adding the median of the predicted frames in the transient
                    tp_transients_predictions.append(np.max(gt_predictions_for_cell[frames]))
                else:
                    # then if's a FN
                    fn_transients_predictions.append(np.max(gt_predictions_for_cell[frames]))
        tn = 0
        if full_raster_dur is not None:
            for transient_period in fake_transients_periods:
                frames = np.arange(transient_period[0], transient_period[1] + 1)
                if np.sum(predicted_raster_dur[frames]) == 0:
                    tn += 1
                if raster_predictions is not None:
                    if np.max(gt_predictions_for_cell[frames]) < 0.5:
                        # adding the max of the predicted frames in the transient
                        # by max we know how far we are from 0.5
                        tn_transients_predictions.append(np.max(gt_predictions_for_cell[frames]))
                    else:
                        # then if's a FP
                        # taking the max because we want to see how far are we from 0.5
                        fp_transients_predictions.append(np.max(gt_predictions_for_cell[frames]))

        tp_transients += tp
        fn_transients += (n_transients - tp)
        tn_transients += tn
        fp_transients += (n_fake_transients - tn)

    frames_stat["TP"] = tp_frames
    frames_stat["FP"] = fp_frames
    frames_stat["FN"] = fn_frames
    frames_stat["TN"] = tn_frames

    # frames_stat["TPR"] = tp_frames / (tp_frames + fn_frames)
    if (tp_frames + fn_frames) > 0:
        frames_stat["sensitivity"] = tp_frames / (tp_frames + fn_frames)
    else:
        frames_stat["sensitivity"] = 1
    frames_stat["TPR"] = frames_stat["sensitivity"]

    if (tn_frames + fp_frames) > 0:
        frames_stat["specificity"] = tn_frames / (tn_frames + fp_frames)
    else:
        frames_stat["specificity"] = 1
    frames_stat["TNR"] = frames_stat["specificity"]

    if (tp_frames + tn_frames + fp_frames + fn_frames) > 0:
        frames_stat["ACC"] = (tp_frames + tn_frames) / (tp_frames + tn_frames + fp_frames + fn_frames)
    else:
        frames_stat["ACC"] = 1

    if (tp_frames + fp_frames) > 0:
        frames_stat["PPV"] = tp_frames / (tp_frames + fp_frames)
    else:
        frames_stat["PPV"] = 1
    if (tn_frames + fn_frames) > 0:
        frames_stat["NPV"] = tn_frames / (tn_frames + fn_frames)
    else:
        frames_stat["NPV"] = 1

    frames_stat["FNR"] = 1 - frames_stat["TPR"]

    frames_stat["FPR"] = 1 - frames_stat["TNR"]

    if "PPV" in frames_stat:
        frames_stat["FDR"] = 1 - frames_stat["PPV"]

    if "NPV" in frames_stat:
        frames_stat["FOR"] = 1 - frames_stat["NPV"]

    if frames_stat["FPR"] > 0:
        frames_stat["LR+"] = frames_stat["TPR"] / frames_stat["FPR"]
    else:
        frames_stat["LR+"] = 1

    if frames_stat["TNR"] > 0:
        frames_stat["LR-"] = frames_stat["FNR"] / frames_stat["TNR"]
    else:
        frames_stat["LR-"] = 1

    # transients dict
    transients_stat["TP"] = tp_transients
    transients_stat["FN"] = fn_transients
    if traces is not None:
        # print(f"tn_transients {tn_transients}")
        transients_stat["TN"] = tn_transients
        transients_stat["FP"] = fp_transients

    if (tp_transients + fn_transients) > 0:
        transients_stat["sensitivity"] = tp_transients / (tp_transients + fn_transients)
    else:
        transients_stat["sensitivity"] = 1

    # print(f'transients_stat["sensitivity"] {transients_stat["sensitivity"]}')
    transients_stat["TPR"] = transients_stat["sensitivity"]

    if traces is not None:
        if (tn_transients + fp_transients) > 0:
            transients_stat["specificity"] = tn_transients / (tn_transients + fp_transients)
        else:
            transients_stat["specificity"] = 1
        transients_stat["TNR"] = transients_stat["specificity"]

        if (tp_transients + tn_transients + fp_transients + fn_transients) > 0:
            transients_stat["ACC"] = (tp_transients + tn_transients) / \
                                     (tp_transients + tn_transients + fp_transients + fn_transients)
        else:
            transients_stat["ACC"] = 1

        if (tp_transients + fp_transients) > 0:
            transients_stat["PPV"] = tp_transients / (tp_transients + fp_transients)
        else:
            transients_stat["PPV"] = 1
        if (tn_transients + fn_transients) > 0:
            transients_stat["NPV"] = tn_transients / (tn_transients + fn_transients)
        else:
            transients_stat["NPV"] = 1

    transients_stat["FNR"] = 1 - transients_stat["TPR"]

    if raster_predictions is not None:
        predictions_stat = dict()
        predictions_stat["fn_transients_predictions"] = fn_transients_predictions
        predictions_stat["fp_transients_predictions"] = fp_transients_predictions
        predictions_stat["tp_transients_predictions"] = tp_transients_predictions
        predictions_stat["tn_transients_predictions"] = tn_transients_predictions
        predictions_stat["fn_frames_predictions"] = fn_frames_predictions
        predictions_stat["fp_frames_predictions"] = fp_frames_predictions
        predictions_stat["tn_frames_predictions"] = tn_frames_predictions
        predictions_stat["tp_frames_predictions"] = tp_frames_predictions
    else:
        predictions_stat = None

    return frames_stat, transients_stat, predictions_stat, proportion_of_frames_detected_in_transients


class CinacBenchmarks:
    """
    Used to plot benchmarks.
    To do so 4 steps:
    Create an instance of CinacBenchmarks
    Add data using add_inference_to_benchmark()
    Add color for session if you want to using color_by_session()
    then call one the method to plot stats
    """

    def __init__(self, results_path, colors_boxplots=None, verbose=0):
        # key is a session_id (str), value is a 2d binary array (n_cells * n_frames)
        self.ground_truth_dict = dict()
        # key is a session_id (str), value is a 2d array (n_cells * n_frames)
        self.smooth_traces_dict = dict()
        self.verbose = verbose
        self.results_path = results_path

        if colors_boxplots is None:
            self.colors_boxplots = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c',
                                    '#ff7f00', '#cab2d6', '#fdbf6f', '#6a3d9a', '#ffff99', '#b15928', '#ffffd9']
        else:
            self.colors_boxplots = colors_boxplots

        # self.colors_boxplots = self.colors_boxplots[::-1]

        # key is reference_id and value is a boolean, indicating if predictions are available for this inference
        # meaning values that give the probability for the cell to be active at a given frame
        self.are_predictions_for_inference = dict()

        # dict with key the id (str) of the inference method,
        # and value is list of one of 2 array of same shape as ground_truth (1d array), first array is a binary one,
        # 2nd one (optional) is a float one representing the probability (between 0 and 1) for the cell to be active
        self.inferences_to_benchmark_dict = dict()

        # key are the same as inferences_to_benchmark_dict, value is a list of int representing the cell indices
        # to benchmark
        self.cells_to_benchmark_dict = dict()

        # inference id-> session_id -> cell -> value will be a list of dict with results from benchmarks
        self.results_frames_dict = dict()
        self.results_transients_dict = dict()
        # inference id-> session_id-> cell -> value is a list of percentage
        # that represents for each real transient the proportion of frames detected
        self.results_frames_in_transients_pc = dict()
        # inference id-> session_id-> cell -> value will be a dict with results from benchmarks. Each key of the dict
        # each key being a string like "fp_transients_predictions" or "fp_frames_predictions"
        self.results_predictions_dict = dict()
        # inference id-> session_id> value will be a list of dict with results from benchmarks
        self.results_dict_global = dict()

        # key: session_id, value: color
        self.cells_to_color = dict()

    def color_by_session(self, session_id, color):
        """
        Attribute a cell to a color, allowing for example to give to cell of the same
        Args:
            session_id: (str)
            color:

        Returns:

        """
        self.cells_to_color[session_id] = color

    def add_ground_truth(self, session_id, ground_truth, smooth_traces):
        """

        Args:
            session_id:
            ground_truth:
            smooth_traces

        Returns:

        """
        self.ground_truth_dict[session_id] = ground_truth
        self.smooth_traces_dict[session_id] = smooth_traces

    def add_inference_to_benchmark(self, session_id, inference_to_benchmark_id, raster_to_evaluate,
                                   cells_to_benchmark,
                                   raster_predictions=None):
        """

        Args:
            session_id:
            inference_to_benchmark_id:
            raster_to_evaluate:
            raster_predictions:
            cells_to_benchmark:

        Returns:

        """

        if inference_to_benchmark_id not in self.cells_to_benchmark_dict:
            self.cells_to_benchmark_dict[inference_to_benchmark_id] = dict()
        if session_id in self.cells_to_benchmark_dict[inference_to_benchmark_id]:
            print(f"Session {session_id} for {inference_to_benchmark_id} already added to inference_to_benchmark")

        self.cells_to_benchmark_dict[inference_to_benchmark_id][session_id] = cells_to_benchmark
        inference_data = [raster_to_evaluate]
        if raster_predictions is not None:
            inference_data.append(raster_predictions)

        # assuming that if a predictions is available for an inference method, it is for all sessions
        if inference_to_benchmark_id not in self.are_predictions_for_inference:
            self.are_predictions_for_inference[inference_to_benchmark_id] = False
        if raster_predictions is not None:
            self.are_predictions_for_inference[inference_to_benchmark_id] = True

        if inference_to_benchmark_id not in self.inferences_to_benchmark_dict:
            self.inferences_to_benchmark_dict[inference_to_benchmark_id] = dict()
        self.inferences_to_benchmark_dict[inference_to_benchmark_id][session_id] = inference_data

        if inference_to_benchmark_id not in self.results_predictions_dict:
            self.results_predictions_dict[inference_to_benchmark_id] = dict()
        self.results_predictions_dict[inference_to_benchmark_id][session_id] = SortedDict()

        if inference_to_benchmark_id not in self.results_frames_dict:
            self.results_frames_dict[inference_to_benchmark_id] = dict()
        self.results_frames_dict[inference_to_benchmark_id][session_id] = SortedDict()

        if inference_to_benchmark_id not in self.results_transients_dict:
            self.results_transients_dict[inference_to_benchmark_id] = dict()
        self.results_transients_dict[inference_to_benchmark_id][session_id] = SortedDict()

        if inference_to_benchmark_id not in self.results_frames_in_transients_pc:
            self.results_frames_in_transients_pc[inference_to_benchmark_id] = dict()
        self.results_frames_in_transients_pc[inference_to_benchmark_id][session_id] = SortedDict()

    def evaluate_metrics(self):
        """
        Should be called after all inference to benchmark have been added and before generating the plots
        Returns:

        """
        for inference_to_benchmark_id, cell_dict in self.cells_to_benchmark_dict.items():
            for session_id, cells in cell_dict.items():
                for cell in cells:
                    self._evaluate_metrics_on_a_cell(session_id=session_id,
                                                     inference_to_benchmark_id=inference_to_benchmark_id,
                                                     cell=cell)

    def _evaluate_metrics_on_a_cell(self, session_id, inference_to_benchmark_id, cell):
        """

        Args:
            session_id: session from which the activity is recorded
            inference_to_benchmark_id: (str) id of the inference to benchmark
            cell: int

        Returns: a dict with same keys as inferences_to_benchmarks and values...
        """

        if inference_to_benchmark_id not in self.inferences_to_benchmark_dict:
            print(f"evaluate_metrics_on_a_cell: inference {inference_to_benchmark_id} unknown")

        if session_id not in self.inferences_to_benchmark_dict[inference_to_benchmark_id]:
            print(f"evaluate_metrics_on_a_cell: session {session_id} unknown")
            return

        inference_to_benchmark = self.inferences_to_benchmark_dict[inference_to_benchmark_id][session_id]
        # print(f"{session_id} {inference_to_benchmark_id}: n_cells for evaluation {len(inference_to_benchmark[0])}")
        raster_to_evaluate = inference_to_benchmark[0][cell]
        if len(inference_to_benchmark) == 2:
            raster_predictions = inference_to_benchmark[1][cell]
        else:
            raster_predictions = None

        frames_stat, transients_stat, predictions_stat_dict, proportion_of_frames_detected_in_transients = \
            compute_stats_over_gt(raster_gt=self.ground_truth_dict[session_id][cell],
                                  raster_predictions=raster_predictions,
                                  raster_to_evaluate=raster_to_evaluate,
                                  traces=self.smooth_traces_dict[session_id][cell],
                                  fluorescence_threshold=None)

        self.results_predictions_dict[inference_to_benchmark_id][session_id][cell] = predictions_stat_dict
        self.results_frames_dict[inference_to_benchmark_id][session_id][cell] = frames_stat
        self.results_transients_dict[inference_to_benchmark_id][session_id][cell] = transients_stat
        self.results_frames_in_transients_pc[inference_to_benchmark_id][session_id][
            cell] = proportion_of_frames_detected_in_transients

        if self.verbose:
            # frames stats
            print(f"raster {inference_to_benchmark_id}")
            print(f"Frames stat:")
            for k, value in frames_stat.items():
                print(f"{k}: {str(np.round(value, 4))}")
        if self.verbose:
            print(f"###")
            print(f"Transients stat:")
            for k, value in transients_stat.items():
                print(f"{k}: {str(np.round(value, 4))}")
            print("")

    def plot_boxplot_predictions_stat_by_metrics(self, description, time_str=None, colorfull=True,
                                                 white_background=True, for_frames=False,
                                                 save_formats="pdf", dpi=500):
        """
        PLot the boxplot regarding the predictions done by cinac classifiers.
        Args:
            description: (str) will be added to file_name
            time_str: (str) timestamps for file_name, optional
            save_formats:str or list of str (.pdf, .png etc...)
            dpi:

        Returns:

        """

        if len(self.results_predictions_dict) == 0:
            # it means no inference had predictions
            return

        if for_frames:
            type_of_activity_list = ["frames"]
        else:
            type_of_activity_list = ["transients"]
        metrics_to_show_list = ["tp", "tn", "fp", "fn"]

        with_scatter = True

        for inference_id in list(self.results_predictions_dict.keys()):
            # first we check if we have predictions for this inference
            if not self.are_predictions_for_inference[inference_id]:
                continue
            # print(f"Inference {inference_id} in the loop")
            """
            # inference id-> session_id-> cell -> value will be a dict with results from benchmarks. Each key of the dict
        # each key being a string like "fp_transients_predictions" or "fp_frames_predictions"
        self.results_predictions_dict = dict()
            """
            predictions_by_cell_stat = dict()
            predictions_stat = dict()
            # we take just the first data, as it's supposed to be same results for each
            for type_of_activity in type_of_activity_list:
                predictions_by_cell_stat[type_of_activity] = dict()
                predictions_stat[type_of_activity] = dict()
                for metrics_to_show in metrics_to_show_list:
                    predictions_by_cell_stat[type_of_activity][metrics_to_show] = dict()
                    predictions_stat[type_of_activity][metrics_to_show] = []
                    data_pred_dict = self.results_predictions_dict[inference_id]
                    for session_id, session_data_dict in data_pred_dict.items():
                        predictions_by_cell_stat[type_of_activity][metrics_to_show][session_id] = dict()
                        for cell, pred_dict in session_data_dict.items():
                            string_key = metrics_to_show + "_" + type_of_activity + "_" + "predictions"
                            predictions_by_cell_stat[type_of_activity][metrics_to_show][session_id][cell] = \
                                pred_dict[string_key]
                            predictions_stat[type_of_activity][metrics_to_show].extend(pred_dict[string_key])
                            # first one is enough

            for by_cell in [True, False]:
                for type_of_activity in type_of_activity_list:
                    if by_cell:
                        # using the value in metrics_to_show
                        n_box_plots = 0
                        for session_id, session_data_dict in \
                                predictions_by_cell_stat[type_of_activity][metrics_to_show].items():
                            # number of cells in the session
                            n_box_plots += len(session_data_dict)
                        if n_box_plots > 25:
                            # if more than 15 boxplots, we don't plot it
                            continue
                    stat_fig, axes = plt.subplots(nrows=2, ncols=2, squeeze=True,
                                                  gridspec_kw={'height_ratios': [0.5, 0.5],
                                                               'width_ratios': [0.5, 0.5]},
                                                  figsize=(10, 10), dpi=dpi)

                    stat_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'w_pad': 1, 'h_pad': 5})
                    axes = np.ndarray.flatten(axes)
                    fig_patch = stat_fig.patch

                    # rgba = c_map(0)
                    if white_background:
                        face_color = "white"
                        text_color = "black"
                        title_color = "black"
                    else:
                        face_color = "black"
                        text_color = "white"
                        title_color = "red"
                    fig_patch.set_facecolor(face_color)

                    for metrics_index, metrics_to_show in enumerate(metrics_to_show_list):
                        ax = axes[metrics_index]

                        ax.set_facecolor(face_color)

                        ax.set_frame_on(False)
                        box_plot_index_so_far = 0
                        if by_cell:
                            n_box_plots = 0
                            labels = []
                            values_by_prediction = []
                            for session_id, by_cell_dict in \
                                    predictions_by_cell_stat[type_of_activity][metrics_to_show].items():
                                n_box_plots += len(by_cell_dict)
                                for cell_key in by_cell_dict.keys():
                                    labels.append(f"{len(by_cell_dict[cell_key])}")
                                # labels = list(by_cell_dict.keys())
                                values_by_prediction.extend([by_cell_dict[cell_key] for cell_key in
                                                             by_cell_dict.keys()])
                                if with_scatter:
                                    for label_index, cell_key in enumerate(list(by_cell_dict.keys())):
                                        # print(f"scatter {label_index} {cell_key}")
                                        y_pos = by_cell_dict[cell_key]
                                        x_pos = []
                                        for ii in range(len(y_pos)):
                                            # Adding jitter
                                            x_pos.append(
                                                1 + box_plot_index_so_far + ((np.random.random_sample() - 0.5) * 0.7))
                                        if white_background:
                                            edgecolors = "black"
                                        else:
                                            edgecolors = "white"
                                        ax.scatter(x_pos, y_pos,
                                                   color=BREWER_COLORS[box_plot_index_so_far % len(BREWER_COLORS)],
                                                   marker="o",
                                                   edgecolors=edgecolors,
                                                   s=20, zorder=21, alpha=0.4)
                                        box_plot_index_so_far += 1
                        else:
                            n_cells = 0
                            for session_id, by_cell_dict in \
                                    predictions_by_cell_stat[type_of_activity][metrics_to_show].items():
                                n_cells += len(by_cell_dict)
                            labels = [f"{n_cells} cells, "
                                      f"{len(predictions_stat[type_of_activity][metrics_to_show])} {type_of_activity}"]
                            n_box_plots = 1
                            values_by_prediction = [predictions_stat[type_of_activity][metrics_to_show]]

                            if with_scatter:
                                y_pos = predictions_stat[type_of_activity][metrics_to_show]
                                x_pos = []
                                for ii in range(len(y_pos)):
                                    # Adding jitter
                                    x_pos.append(1 + ((np.random.random_sample() - 0.5) * 0.7))
                                if white_background:
                                    edgecolors = "black"
                                else:
                                    edgecolors = "white"
                                ax.scatter(x_pos, y_pos,
                                           color=BREWER_COLORS[0 % len(BREWER_COLORS)],
                                           marker="o",
                                           edgecolors=edgecolors,
                                           s=20, zorder=21, alpha=0.4)

                        outliers = dict(markerfacecolor='white', marker='D')
                        # if not for_frames:
                        #     print(f"plot_boxplots_full_stat: {stat_name}: values_by_prediction {values_by_prediction}")
                        if with_scatter:
                            sym = ''
                        else:
                            sym = '+'

                        # print("stat_by_metrics")
                        # print(f"{metrics_to_show.upper()}: median: {np.round(np.median(values_by_prediction), 3)}, "
                        #       f"25p {np.round(np.percentile(values_by_prediction, 25), 3)}, "
                        #       f"75p {np.round(np.percentile(values_by_prediction, 75), 3)}")

                        bplot = ax.boxplot(values_by_prediction, patch_artist=colorfull,
                                           flierprops=outliers, widths=[0.7] * len(values_by_prediction),
                                           labels=labels, sym=sym, zorder=1)  # whis=[5, 95], sym='+'

                        for element in ['boxes', 'whiskers', 'fliers', 'caps']:
                            if white_background:
                                plt.setp(bplot[element], color="black")
                            else:
                                plt.setp(bplot[element], color="white")

                        for element in ['means', 'medians']:
                            if white_background:
                                plt.setp(bplot[element], color="black")
                            else:
                                plt.setp(bplot[element], color="white")

                        if colorfull:
                            colors = self.colors_boxplots[:n_box_plots]
                            for patch, color in zip(bplot['boxes'], colors):
                                patch.set_facecolor(color)

                        ax.xaxis.set_ticks_position('none')
                        ax.xaxis.label.set_color(text_color)
                        ax.tick_params(axis='x', colors=text_color)
                        if n_box_plots <= 3:
                            ax.xaxis.set_tick_params(labelsize=15)
                        elif n_box_plots <= 6:
                            ax.xaxis.set_tick_params(labelsize=8)
                        else:
                            ax.xaxis.set_tick_params(labelsize=6)
                        ax.yaxis.label.set_color(text_color)
                        ax.tick_params(axis='y', colors=text_color)
                        # ax.set_xticklabels([])
                        # ax.set_yticklabels([])
                        # ax.get_yaxis().set_visible(False)
                        # ax.get_xaxis().set_visible(False)
                        # ax.set_ylabel(f"proportion")
                        # ax.set_xlabel("age")
                        xticks = np.arange(1, n_box_plots + 1)
                        ax.set_xticks(xticks)
                        # sce clusters labels
                        ax.set_xticklabels(labels)
                        # fixing the limits
                        # if stat_name == "sensitivity":
                        #     ax.set_ylim(0, 1)
                        # elif stat_name == "specificity":
                        #     ax.set_ylim(0.85, 1)
                        # elif stat_name == "PPV":
                        #     ax.set_ylim(0, 1)
                        # elif stat_name == "NPV":
                        #     ax.set_ylim(0.6, 1.1)

                        ax.set_title(metrics_to_show.upper(), color=title_color, pad=20, fontsize=30, fontweight='bold')

                    str_details = "and_cells_" if by_cell else ""
                    str_details = str_details + "_" + inference_id
                    if isinstance(save_formats, str):
                        save_formats = [save_formats]
                    if time_str is None:
                        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
                    for save_format in save_formats:
                        stat_fig.savefig(f'{self.results_path}/'
                                         f'{description}_box_plots_predictions_by_metrics_{str_details}_'
                                         f'for_{type_of_activity}'
                                         f'_{time_str}.{save_format}',
                                         format=f"{save_format}",
                                         facecolor=stat_fig.get_facecolor(), edgecolor='none')
                    plt.close()

    def plot_boxplots_full_stat(self, description, time_str=None, for_frames=True, with_cells=False,
                                color_cell_as_boxplot=False,
                                box_plots_labels=None,
                                colorfull=True,
                                white_background=True,
                                stats_to_show=("sensitivity", "specificity", "PPV", "NPV"),
                                title_correspondance=None,
                                alpha_scatter=1., with_cell_number=True,
                                put_metric_as_y_axis_label=False,
                                using_patch_for_legend=False,
                                with_legend=False,
                                save_formats="pdf", dpi=500):
        """

        :param description:
        :param time_str:
        :param for_frames:
        ;param box_plots_labels: if not NOne, list of str, allowing to choose the order of the boxplots.
        The labels should be existing one, otherwise it will crash
        :param with_cells: if True, display a scatter for each cell
        :param save_formats:
        :param title_correspondance: dict or None, keys are the stats to show, and the value is another string
        that will be displayed in the title
        :return:
        """
        result_dict_to_use = self.results_frames_dict
        if not for_frames:
            result_dict_to_use = self.results_transients_dict

        nrows = 2
        height_ratios = [0.5, 0.5]
        ncols = 2
        width_ratios = [0.5, 0.5]
        figsize = (10, 10)
        if len(stats_to_show) == 2:
            nrows = 2
            height_ratios = [0.5, 0.5]
            ncols = 1
            width_ratios = [1]
            figsize = (5, 10)
        if len(stats_to_show) == 1:
            nrows = 1
            height_ratios = [1]
            ncols = 1
            width_ratios = [1]
            figsize = (5, 5)
        stat_fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=True,
                                      gridspec_kw={'height_ratios': height_ratios,
                                                   'width_ratios': width_ratios},
                                      figsize=figsize, dpi=dpi)

        stat_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'w_pad': 1, 'h_pad': 5})
        if isinstance(axes, np.ndarray):
            axes = np.ndarray.flatten(axes)
        else:
            axes = [axes]
        fig_patch = stat_fig.patch

        # rgba = c_map(0)
        if white_background:
            face_color = "white"
            text_color = "black"
            title_color = "black"
        else:
            face_color = "black"
            text_color = "white"
            title_color = "red"
        fig_patch.set_facecolor(face_color)

        for stat_index, stat_name in enumerate(stats_to_show):
            ax = axes[stat_index]
            # n_cells = len(self.results_frames_dict_by_cell)

            ax.set_facecolor(face_color)

            ax.set_frame_on(False)
            n_box_plots = None
            labels = None
            values_by_prediction = None

            n_box_plots = len(result_dict_to_use)
            if box_plots_labels is None:
                labels = list(result_dict_to_use.keys())
            else:
                labels = box_plots_labels
            values_by_prediction = [[] for n in np.arange(n_box_plots)]

            for label_index, label in enumerate(labels):
                session_dict = result_dict_to_use[label]
                for session_id, cells_dict in session_dict.items():
                    for cell_to_display, stat_dict in cells_dict.items():
                        # all label might not have the same cells
                        values_by_prediction[label_index].append(stat_dict[stat_name])
                        if with_cells:
                            # Adding jitter
                            x_pos = 1 + label_index + ((np.random.random_sample() - 0.5) * 0.7)
                            y_pos = stat_dict[stat_name]
                            font_size = 3
                            if white_background:
                                edgecolors = "black"
                            else:
                                edgecolors = "white"
                            if color_cell_as_boxplot:
                                color_cell = self.colors_boxplots[label_index % len(self.colors_boxplots)]
                            elif session_id not in self.cells_to_color:
                                color_cell = BREWER_COLORS[label_index % len(BREWER_COLORS)]
                            else:
                                color_cell = self.cells_to_color[session_id]
                            ax.scatter(x_pos, y_pos,
                                       color=color_cell,
                                       marker="o",
                                       edgecolors=edgecolors,
                                       s=60, zorder=21, alpha=alpha_scatter)
                            if cell_to_display > 999:
                                font_size = 2
                            if with_cell_number:
                                ax.text(x=x_pos, y=y_pos,
                                        s=f"{cell_to_display}", color="black", zorder=22,
                                        ha='center', va="center", fontsize=font_size, fontweight='bold')

            outliers = dict(markerfacecolor='white', marker='D')

            print(f"full_stats for_frames {for_frames}, stat {stat_name}: {description}")
            for label_index, label in enumerate(labels):
                print(f"{label}: median: {np.round(np.median(values_by_prediction[label_index]), 3)}, "
                      f"25p {np.round(np.percentile(values_by_prediction[label_index], 25), 3)}, "
                      f"75p {np.round(np.percentile(values_by_prediction[label_index], 75), 3)}")

            bplot = ax.boxplot(values_by_prediction, patch_artist=colorfull,
                               flierprops=outliers, widths=[0.7] * len(values_by_prediction),
                               labels=labels, sym='', zorder=1)  # whis=[5, 95], sym='+'

            for element in ['boxes', 'whiskers', 'fliers', 'caps']:
                if white_background:
                    plt.setp(bplot[element], color="black")
                else:
                    plt.setp(bplot[element], color="white")

            for element in ['means', 'medians']:
                if white_background:
                    plt.setp(bplot[element], color="black")
                else:
                    plt.setp(bplot[element], color="white")

            if colorfull:
                # supposing there are less box_plots than colors,
                # but most probably there won't be more than 20 boxplots
                colors = self.colors_boxplots[:n_box_plots]
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)

            ax.xaxis.set_ticks_position('none')
            ax.xaxis.label.set_color(text_color)
            ax.tick_params(axis='x', colors=text_color)
            if n_box_plots <= 2:
                ax.xaxis.set_tick_params(labelsize=20)
            elif n_box_plots <= 6:
                ax.xaxis.set_tick_params(labelsize=8)
            else:
                ax.xaxis.set_tick_params(labelsize=2)
            ax.yaxis.label.set_color(text_color)
            ax.tick_params(axis='y', colors=text_color)
            # ax.set_xticklabels([])
            # ax.set_yticklabels([])
            # ax.get_yaxis().set_visible(False)
            # ax.get_xaxis().set_visible(False)
            if put_metric_as_y_axis_label:
                if title_correspondance is not None and stat_name in title_correspondance:
                    ax.set_ylabel(title_correspondance[stat_name] + " (%)")
                else:
                    ax.set_ylabel(stat_name + " (%)")
                ax.yaxis.label.set_size(20)
            else:
                if title_correspondance is not None and stat_name in title_correspondance:
                    ax.set_title(title_correspondance[stat_name], color=title_color, pad=20, fontsize=20)
                else:
                    ax.set_title(stat_name, color=title_color, pad=20, fontsize=20)

            # ax.set_xlabel("age")
            xticks = np.arange(1, n_box_plots + 1)
            ax.set_xticks(xticks)
            ax.set_xticklabels(labels)

            yticks = np.arange(0, 1.2, 0.2)
            ax.set_yticks(yticks)
            ax.set_yticklabels(np.arange(0, 120, 20))
            # fixing the limits
            if stat_name == "sensitivity":
                ax.set_ylim(0, 1.1)
            # elif stat_name == "specificity":
            #     ax.set_ylim(0.85, 1)
            if stat_name == "PPV":
                ax.set_ylim(0, 1.1)
            # elif stat_name == "NPV":
            #     ax.set_ylim(0.6, 1.1)

            # adding legend if cells displayed
            if with_cells and with_legend and (not color_cell_as_boxplot):
                if using_patch_for_legend:
                    legend_elements = []
                    # looking for all session_ids
                    all_session_ids = set()
                    for label_index, label in enumerate(labels):
                        session_dict = result_dict_to_use[label]
                        # session_dict = SortedDict(**session_dict)
                        for session_id, cells_dict in session_dict.items():
                            all_session_ids.add(session_id)
                    all_session_ids = list(all_session_ids)
                    copy_all_session_ids = all_session_ids.copy()
                    try:
                        all_session_ids.sort(key=extract_age)
                    except TypeError:
                        all_session_ids = copy_all_session_ids

                    for session_id in all_session_ids:
                        # print(f"session_id {session_id}")
                        if session_id not in self.cells_to_color:
                            continue
                        color_cell = self.cells_to_color[session_id]
                        # hatch="o",
                        legend_elements.append(Patch(facecolor=color_cell,
                                                     edgecolor='black', label=session_id))

                    # if use_different_shapes_for_stat:
                    #     for cat in np.arange(1, n_categories + 1):
                    #         if cat in banned_categories:
                    #             continue
                    #         legend_elements.append(Line2D([0], [0], marker=param.markers[cat - 1], color="w", lw=0, label="*" * cat,
                    #                                       markerfacecolor='black', markersize=15))
                    #
                    ax.legend(handles=legend_elements)
                else:
                    # using the label put in the scatter
                    ax.legend()

        str_details = "frames"
        if not for_frames:
            str_details = "transients"
        for stat_name in stats_to_show:
            str_details = str_details + f'_{title_correspondance[stat_name]}'
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        if time_str is None:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        for save_format in save_formats:
            stat_fig.savefig(f'{self.results_path}/'
                             f'{description}_box_plots_predictions_{str_details}'
                             f'_{time_str}.{save_format}',
                             format=f"{save_format}",
                             facecolor=stat_fig.get_facecolor(), edgecolor='none')
        plt.close()

    # TODO: update this one
    def plot_boxplots_for_transients_stat(self, description, colorfull=True, time_str=None, save_formats="pdf"):
        stats_to_show = ["sensitivity"]
        colors = ["cornflowerblue", "blue", "steelblue", "red", "orange"]

        stat_fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=True,
                                      gridspec_kw={'height_ratios': [1],
                                                   'width_ratios': [1]},
                                      figsize=(8, 8))

        stat_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'w_pad': 1, 'h_pad': 5})
        # axes = np.ndarray.flatten(axes)
        fig_patch = stat_fig.patch
        # rgba = c_map(0)
        face_color = "black"
        text_color = "white"
        title_color = "red"
        fig_patch.set_facecolor(face_color)

        for stat_index, stat_name in enumerate(stats_to_show):
            ax = axes
            # n_cells = len(self.results_transients_dict_by_cell)

            # now adding as many suplots as need, depending on how many overlap has the cell

            ax.set_facecolor(face_color)
            ax.xaxis.set_ticks_position('none')
            ax.xaxis.label.set_color(text_color)
            ax.tick_params(axis='x', colors=text_color)
            ax.yaxis.label.set_color(text_color)
            ax.tick_params(axis='y', colors=text_color)
            # ax.set_xticklabels([])
            # ax.set_yticklabels([])
            # ax.get_yaxis().set_visible(False)
            # ax.get_xaxis().set_visible(False)

            ax.set_frame_on(False)
            n_box_plots = None
            labels = None
            values_by_prediction = None

            n_box_plots = len(self.results_transients_dict)
            labels = list(self.results_transients_dict.keys())
            values_by_prediction = [[] for n in np.arange(n_box_plots)]
            for label_index, label in enumerate(labels):
                session_dict = self.results_transients_dict[label]
                for session_id, cells_dict in session_dict.items():
                    for cell_to_display, stat_dict in cells_dict.items():
                        values_by_prediction[label_index]. \
                            append(self.results_transients_dict[cell_to_display][label][stat_name])

            bplot = ax.boxplot(values_by_prediction, patch_artist=colorfull,
                               labels=labels, sym='', zorder=1)  # whis=[5, 95], sym='+'

            for element in ['boxes', 'whiskers', 'fliers', 'caps']:
                plt.setp(bplot[element], color="white")

            for element in ['means', 'medians']:
                plt.setp(bplot[element], color="white")  # used to be silver

            if colorfull:
                colors = colors[:n_box_plots]
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)

            # ax.set_ylabel(f"proportion")
            # ax.set_xlabel("age")
            xticks = np.arange(1, n_box_plots + 1)
            ax.set_xticks(xticks)
            # sce clusters labels
            ax.set_xticklabels(labels)

            ax.set_title(stat_name, color=title_color, pad=20)

        if time_str is None:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            stat_fig.savefig(f'{self.results_path}/'
                             f'{description}_box_plots_predictions_transients'
                             f'_{time_str}.{save_format}',
                             format=f"{save_format}",
                             facecolor=stat_fig.get_facecolor(), edgecolor='none')

    def stats_on_performance(self, stats_to_evaluate, data_labels=None, title_correspondance=None, for_frames=False):
        """
        Compare with a wilcoxon test the performance over all pair of labels (methods)
        Args:
            stats_to_evaluate: list of str
            title_correspondance: dict

        Returns:

        """
        print("")
        print("-" * 100)
        print("COMPARING METRICS values FOR EACH LABEL (Wilcoxon signed-rank test)")
        result_dict_to_use = self.results_frames_dict
        if not for_frames:
            result_dict_to_use = self.results_transients_dict

        for stat_name in stats_to_evaluate:
            stat_name_to_display = stat_name
            if (title_correspondance is not None) and (stat_name in title_correspondance):
                stat_name_to_display = title_correspondance[stat_name]
            print(f"## For {stat_name_to_display}:")
            n_labels = len(data_labels)
            if data_labels is None:
                data_labels = list(result_dict_to_use.keys())

            values_by_prediction = [[] for n in np.arange(n_labels)]
            cells_by_prediction = [[] for n in np.arange(n_labels)]

            for label_index, label in enumerate(data_labels):
                session_dict = result_dict_to_use[label]
                for session_id, cells_dict in session_dict.items():
                    for cell_to_display, stat_dict in cells_dict.items():
                        if stat_name == "F1":
                            recall = stat_dict["sensitivity"]
                            precision = stat_dict["PPV"]
                            if (precision + recall) == 0:
                                f1_score = 0
                            else:
                                f1_score = 2 * ((precision * recall) / (precision + recall))
                            values_by_prediction[label_index].append(f1_score)
                        else:
                            # putting metric value for each cell in the list
                            values_by_prediction[label_index].append(stat_dict[stat_name])
                        cells_by_prediction[label_index].append(session_id + "_" + str(cell_to_display))

            for label_index in np.arange(n_labels - 1):
                for label_index_2 in np.arange(1, n_labels):
                    if label_index == label_index_2:
                        continue
                    values = np.array(values_by_prediction[label_index])
                    values_2 = np.array(values_by_prediction[label_index_2])
                    common_cells = np.intersect1d(cells_by_prediction[label_index],
                                                  cells_by_prediction[label_index_2])
                    # common_cells = list(set(cells_by_prediction[label_index]) &
                    #                     set(cells_by_prediction[label_index_2]))
                    # same cells
                    # print(f"{data_labels[label_index]} vs {data_labels[label_index_2]}")
                    # print(f"{len(values)} vs {len(values_2)}")
                    # print(f"{values} vs {values_2}")
                    # print(" ")

                    if (len(values) != len(values_2)) or len(values) != len(common_cells):
                        # we only keep common cells
                        # list of string
                        cells = cells_by_prediction[label_index]
                        cells_2 = cells_by_prediction[label_index_2]

                        values = [values[cells.index(cell)] for cell in common_cells]
                        values_2 = [values_2[cells_2.index(cell)] for cell in common_cells]
                    sum_of_ranks, p_value = wilcoxon(values, values_2)

                    print(f"{data_labels[label_index]} vs {data_labels[label_index_2]}: p = "
                          f"{np.round(p_value, 3)}, T = {np.round(sum_of_ranks, 1)}")

            print("")

        print("-" * 100)
        print("")

    def plot_boxplots_f1_score(self, description, colorfull=False, time_str=None,
                               for_frames=True, with_cells=False,
                               color_cell_as_boxplot=False,
                               box_plots_labels=None,
                               white_background=False,
                               with_legend=False,
                               using_patch_for_legend=True,
                               alpha_scatter=1, with_cell_number=True,
                               put_metric_as_y_axis_label=False,
                               save_formats="pdf", dpi=500):
        """

        :param description:
        :param time_str:
        :param colorfull (bool): if True, the boxplots are filled with color, one different for each
        (based on brewer colors)
        :param white_background: (bool) if True white background, else black background
        :param for_frames:
        :param with_cells: if True, display a scatter for each cell
        :param save_formats:
        :return:
        """
        result_dict_to_use = self.results_frames_dict
        if not for_frames:
            result_dict_to_use = self.results_transients_dict

        stat_fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=True,
                                    gridspec_kw={'height_ratios': [1],
                                                 'width_ratios': [1]},
                                    figsize=(5, 5), dpi=dpi)

        stat_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'w_pad': 1, 'h_pad': 5})
        fig_patch = stat_fig.patch

        # rgba = c_map(0)
        if white_background:
            face_color = "white"
            text_color = "black"
            title_color = "black"
        else:
            face_color = "black"
            text_color = "white"
            title_color = "red"
        fig_patch.set_facecolor(face_color)

        # n_cells = len(self.results_frames_dict_by_cell)

        ax.set_facecolor(face_color)

        ax.set_frame_on(False)

        n_box_plots = len(result_dict_to_use)
        if box_plots_labels is None:
            labels = list(result_dict_to_use.keys())
        else:
            labels = box_plots_labels
        values_by_prediction = [[] for n in np.arange(n_box_plots)]

        for label_index, label in enumerate(labels):
            n_scatter = 0
            session_dict = result_dict_to_use[label]
            for session_id, cells_dict in session_dict.items():
                for cell_to_display, stat_dict in cells_dict.items():
                    n_scatter += 1
                    recall = stat_dict["sensitivity"]
                    precision = stat_dict["PPV"]
                    if (precision + recall) == 0:
                        f1_score = 0
                    else:
                        f1_score = 2 * ((precision * recall) / (precision + recall))
                    values_by_prediction[label_index]. \
                        append(f1_score)
                    if with_cells:
                        # Adding jitter
                        x_pos = 1 + label_index + ((np.random.random_sample() - 0.5) * 0.7)
                        y_pos = f1_score
                        font_size = 3
                        if white_background:
                            edgecolors = "black"
                        else:
                            edgecolors = "white"

                        if color_cell_as_boxplot:
                            color_cell = self.colors_boxplots[label_index % len(self.colors_boxplots)]
                        elif session_id not in self.cells_to_color:
                            color_cell = BREWER_COLORS[label_index % len(BREWER_COLORS)]
                        else:
                            color_cell = self.cells_to_color[session_id]
                        if label_index == 0 and with_legend:
                            ax.scatter(x_pos, y_pos,
                                       color=color_cell,
                                       marker="o",
                                       label=session_id,
                                       edgecolors=edgecolors,
                                       s=60, zorder=21, alpha=alpha_scatter)
                        else:
                            ax.scatter(x_pos, y_pos,
                                       color=color_cell,
                                       marker="o",
                                       edgecolors=edgecolors,
                                       s=60, zorder=21, alpha=alpha_scatter)
                        if with_cell_number:
                            ax.text(x=x_pos, y=y_pos,
                                    s=f"{cell_to_display}", color="black", zorder=22,
                                    ha='center', va="center", fontsize=font_size, fontweight='bold')
            print(f"{n_scatter} cells for {label}")
        outliers = dict(markerfacecolor='white', marker='D')
        print(f"F1 SCORE for_frames {for_frames}: {description}")
        for label_index, label in enumerate(labels):
            print(f"{label}: median: {np.round(np.median(values_by_prediction[label_index]), 3)}, "
                  f"25p {np.round(np.percentile(values_by_prediction[label_index], 25), 3)}, "
                  f"75p {np.round(np.percentile(values_by_prediction[label_index], 75), 3)}")
        bplot = ax.boxplot(values_by_prediction, patch_artist=colorfull,
                           flierprops=outliers, widths=[0.7] * len(values_by_prediction),
                           labels=labels, sym='', zorder=1)  # whis=[5, 95], sym='+'

        for element in ['boxes', 'whiskers', 'fliers', 'caps']:
            if white_background:
                plt.setp(bplot[element], color="black")
            else:
                plt.setp(bplot[element], color="white")

        for element in ['means', 'medians']:
            if white_background:
                plt.setp(bplot[element], color="black")
            else:
                plt.setp(bplot[element], color="white")  # "silver"

        if colorfull:
            colors = self.colors_boxplots[:n_box_plots]
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)

        # adding legend if cells displayed
        if with_cells and with_legend and (not color_cell_as_boxplot):
            if using_patch_for_legend:
                legend_elements = []
                # looking for all session_ids
                all_session_ids = set()
                for label_index, label in enumerate(labels):
                    session_dict = result_dict_to_use[label]
                    # session_dict = SortedDict(**session_dict)
                    for session_id, cells_dict in session_dict.items():
                        all_session_ids.add(session_id)
                all_session_ids = list(all_session_ids)

                all_session_ids.sort(key=extract_age)
                for session_id in all_session_ids:
                    print(f"session_id {session_id}")
                    if session_id not in self.cells_to_color:
                        continue
                    color_cell = self.cells_to_color[session_id]
                    # hatch="o",
                    legend_elements.append(Patch(facecolor=color_cell,
                                                 edgecolor='black', label=session_id))

                # if use_different_shapes_for_stat:
                #     for cat in np.arange(1, n_categories + 1):
                #         if cat in banned_categories:
                #             continue
                #         legend_elements.append(Line2D([0], [0], marker=param.markers[cat - 1], color="w", lw=0, label="*" * cat,
                #                                       markerfacecolor='black', markersize=15))
                #
                ax.legend(handles=legend_elements)
            else:
                # using the label put in the scatter
                ax.legend()

        ax.xaxis.set_ticks_position('none')
        ax.xaxis.label.set_color(text_color)
        ax.tick_params(axis='x', colors=text_color)

        if n_box_plots <= 2:
            ax.xaxis.set_tick_params(labelsize=20)
        elif n_box_plots <= 6:
            ax.xaxis.set_tick_params(labelsize=8)
        else:
            ax.xaxis.set_tick_params(labelsize=2)
        ax.yaxis.label.set_color(text_color)
        ax.tick_params(axis='y', colors=text_color)
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.get_yaxis().set_visible(False)
        # ax.get_xaxis().set_visible(False)
        # ax.set_ylabel(f"proportion")
        # ax.set_xlabel("age")
        xticks = np.arange(1, n_box_plots + 1)
        ax.set_xticks(xticks)
        # sce clusters labels
        ax.set_xticklabels(labels)
        yticks = np.arange(0, 1.2, 0.2)
        ax.set_yticks(yticks)
        ax.set_yticklabels(np.arange(0, 120, 20))
        # fixing the limits
        ax.set_ylim(0, 1.1)

        if put_metric_as_y_axis_label:
            ax.set_ylabel("F1 SCORE" " (%)")
            ax.yaxis.label.set_size(20)
        else:
            ax.set_title("F1 SCORE", color=title_color, pad=20, fontsize=20)

        str_details = "frames"
        if not for_frames:
            str_details = "transients"

        if time_str is None:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            stat_fig.savefig(f'{self.results_path}/'
                             f'{description}_box_plots_f1_score_{str_details}'
                             f'_{time_str}.{save_format}',
                             format=f"{save_format}",
                             facecolor=stat_fig.get_facecolor(), edgecolor='none')
        plt.close()

    def plot_boxplots_proportion_frames_in_transients(self, description, time_str=None,
                                                      colorfull=True,
                                                      white_background=False,
                                                      only_this_key=None,
                                                      with_scatter=True,
                                                      with_cell_text=True,
                                                      alpha_scatter=0.6,
                                                      using_patch_for_legend=False,
                                                      with_legend=False,
                                                      put_metric_as_y_axis_label=True,
                                                      save_formats="pdf", dpi=500):
        """

        :param description:
        :param time_str:
        param only_this_key: (str): key of the label, if not None, then only the boxplot corresponding will be displayed
        :param save_formats:
        :return:
        """
        result_dict_to_use = self.results_frames_in_transients_pc

        stat_fig, ax = plt.subplots(nrows=1, ncols=1, squeeze=True,
                                    gridspec_kw={'height_ratios': [1],
                                                 'width_ratios': [1]},
                                    figsize=(5, 10), dpi=dpi)

        stat_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 1, 'w_pad': 1, 'h_pad': 5})
        fig_patch = stat_fig.patch

        # rgba = c_map(0)
        if white_background:
            face_color = "white"
            text_color = "black"
            title_color = "black"
        else:
            face_color = "black"
            text_color = "white"
            title_color = "red"
        fig_patch.set_facecolor(face_color)

        # n_cells = len(self.results_frames_dict_by_cell)

        ax.set_facecolor(face_color)

        ax.set_frame_on(False)

        if only_this_key and only_this_key in result_dict_to_use:
            n_box_plots = 1
            labels = [only_this_key]
        else:
            n_box_plots = len(result_dict_to_use)
            labels = list(result_dict_to_use.keys())

        values_by_prediction = [[] for n in np.arange(n_box_plots)]

        for label_index, label in enumerate(labels):
            session_dict = result_dict_to_use[label]
            for session_id, cells_dict in session_dict.items():
                for cell_to_display, pourcentages in cells_dict.items():
                    values_by_prediction[label_index].extend(pourcentages)

                    if with_scatter:
                        for pc in pourcentages:
                            # Adding jitter
                            x_pos = 1 + label_index + ((np.random.random_sample() - 0.5) * 0.7)
                            y_pos = pc
                            font_size = 3
                            if white_background:
                                edgecolors = "black"
                            else:
                                edgecolors = "white"
                            if session_id not in self.cells_to_color:
                                color_cell = BREWER_COLORS[label_index % len(BREWER_COLORS)]
                            else:
                                color_cell = self.cells_to_color[session_id]
                            ax.scatter(x_pos, y_pos,
                                       color=color_cell,
                                       marker="o",
                                       edgecolors=edgecolors,
                                       s=60, zorder=21, alpha=alpha_scatter)
                            if cell_to_display > 999:
                                font_size = 2
                            if with_cell_text:
                                ax.text(x=x_pos, y=y_pos,
                                        s=f"{cell_to_display}", color="black", zorder=22,
                                        ha='center', va="center", fontsize=font_size, fontweight='bold')

            if with_legend:
                if using_patch_for_legend:
                    legend_elements = []
                    # looking for all session_ids
                    all_session_ids = set()
                    for label_index, label in enumerate(labels):
                        session_dict = result_dict_to_use[label]
                        # session_dict = SortedDict(**session_dict)
                        for session_id, cells_dict in session_dict.items():
                            all_session_ids.add(session_id)
                    all_session_ids = list(all_session_ids)

                    all_session_ids.sort(key=extract_age)
                    for session_id in all_session_ids:
                        print(f"session_id {session_id}")
                        if session_id not in self.cells_to_color:
                            continue
                        color_cell = self.cells_to_color[session_id]
                        # hatch="o",
                        legend_elements.append(Patch(facecolor=color_cell,
                                                     edgecolor='black', label=session_id))

                    # if use_different_shapes_for_stat:
                    #     for cat in np.arange(1, n_categories + 1):
                    #         if cat in banned_categories:
                    #             continue
                    #         legend_elements.append(Line2D([0], [0], marker=param.markers[cat - 1], color="w", lw=0, label="*" * cat,
                    #                                       markerfacecolor='black', markersize=15))
                    #
                    ax.legend(handles=legend_elements)
                else:
                    # using the label put in the scatter
                    ax.legend()

        outliers = dict(markerfacecolor='white', marker='D')
        print("proportion_frames_in_transients")
        for label_index, label in enumerate(labels):
            print(f"{label}: median: {np.round(np.median(values_by_prediction[label_index]), 3)}, "
                  f"25p {np.round(np.percentile(values_by_prediction[label_index], 25), 3)}, "
                  f"75p {np.round(np.percentile(values_by_prediction[label_index], 75), 3)}")
        bplot = ax.boxplot(values_by_prediction, patch_artist=colorfull,
                           flierprops=outliers, widths=[0.7] * len(values_by_prediction),
                           labels=labels, sym='', zorder=1)  # whis=[5, 95], sym='+'

        for element in ['boxes', 'whiskers', 'fliers', 'caps']:
            if white_background:
                plt.setp(bplot[element], color="black")
            else:
                plt.setp(bplot[element], color="white")

        for element in ['means', 'medians']:
            if white_background:
                plt.setp(bplot[element], color="black")
            else:
                plt.setp(bplot[element], color="white")  # silver

        if colorfull:
            colors = self.colors_boxplots[:n_box_plots]
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)

        if put_metric_as_y_axis_label:
            ax.set_ylabel("Proportion of detected frames (%)")
            ax.yaxis.label.set_size(20)
        else:
            ax.set_title("Proportion of detected frames (%)", color=title_color, pad=20, fontsize=20)

        ax.xaxis.set_ticks_position('none')
        ax.xaxis.label.set_color(text_color)
        ax.tick_params(axis='x', colors=text_color)
        if n_box_plots <= 3:
            ax.xaxis.set_tick_params(labelsize=15)
        elif n_box_plots <= 6:
            ax.xaxis.set_tick_params(labelsize=8)
        else:
            ax.xaxis.set_tick_params(labelsize=2)
        ax.yaxis.label.set_color(text_color)
        ax.tick_params(axis='y', colors=text_color)
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        # ax.get_yaxis().set_visible(False)
        # ax.get_xaxis().set_visible(False)
        # ax.set_ylabel(f"proportion")
        # ax.set_xlabel("age")
        xticks = np.arange(1, n_box_plots + 1)
        ax.set_xticks(xticks)
        # sce clusters labels
        ax.set_xticklabels(labels)
        # fixing the limits
        # ax.set_ylim(0, 100)

        # ax.set_title("", color=title_color, pad=20, fontsize=20)

        str_details = ""
        if only_this_key:
            str_details = "_" + only_this_key
        if time_str is None:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            stat_fig.savefig(f'{self.results_path}/'
                             f'{description}_box_plots_proportion_frames_in_transients{str_details}'
                             f'_{time_str}.{save_format}',
                             format=f"{save_format}",
                             facecolor=stat_fig.get_facecolor(), edgecolor='none')
        plt.close()


def load_data_from_np_or_mat_file(file_name, attr_name=None):
    """
    Load data from a numpy or matlab file (.npz, .npz or .mat)
    Args:
        file_name:
        data_descr: string used to display error message if the file is not in the good format
        attr_name:

    Returns:


    """
    if file_name.endswith(".npy"):
        data = np.load(file_name)
    elif file_name.endswith(".npz"):
        data = np.load(file_name)
        if attr_name not in data:
            raise Exception(f"{attr_name} not available in {file_name}, choices are {list(data.keys())}")
        data = data[attr_name]
    elif file_name.endswith(".mat"):  # .mat
        data = hdf5storage.loadmat(file_name)
        if attr_name not in data:
            raise Exception(f"{attr_name} not available in {file_name}, choices are {list(data.keys())}")
        data = data[attr_name]
    else:
        print("Load_data_from_np_or_mat_file() error: file extension must be .npy, .npz or .mat")
        return

    return data


def bin_raster(spike_nums):
    """
    Take a binary 2d array (n_cell*n_frames) and return a binned version,
    with output shape 2d array (n_cell*n_frames//2)
    Args:
        spike_nums:

    Returns:

    """
    spike_nums_bin = np.zeros((spike_nums.shape[0], spike_nums.shape[1] // 2),
                              dtype="int8")
    for cell in np.arange(spike_nums_bin.shape[0]):
        binned_cell = spike_nums[cell].reshape(-1, 2).mean(axis=1)
        binned_cell[binned_cell > 0] = 1
        spike_nums_bin[cell] = binned_cell.astype("int")

    return spike_nums_bin


def get_raster_dur_spikes_and_traces(spike_nums, traces):
    """
    Take a binary raster (n_cells*n_frames) representing spikes or onsets of transient,
    and based on the smoothed traces, detect putative transients and extend the spikes/onsets
    so that the duration of the rise time of the transient in which they are fully 'active'
    Args:
        spike_nums:
        traces:

    Returns:

    """

    # to work just on onsets/spikes
    # return caiman_spike_nums

    n_cells = traces.shape[0]
    n_times = traces.shape[1]

    for i in np.arange(n_cells):
        traces[i, :] = (traces[i, :] - np.mean(traces[i, :])) / np.std(traces[i, :])

    spike_nums_all = np.zeros((n_cells, n_times), dtype="int8")
    for cell in np.arange(n_cells):
        onsets = []
        diff_values = np.diff(traces[cell])
        for index, value in enumerate(diff_values):
            if index == (len(diff_values) - 1):
                continue
            if value < 0:
                if diff_values[index + 1] >= 0:
                    onsets.append(index + 1)
        if len(onsets) > 0:
            spike_nums_all[cell, np.array(onsets)] = 1

    peak_nums = np.zeros((n_cells, n_times), dtype="int8")
    for cell in np.arange(n_cells):
        peaks, properties = signal.find_peaks(x=traces[cell])
        peak_nums[cell, peaks] = 1

    spike_nums_dur = build_spike_nums_dur(spike_nums_all, peak_nums)

    final_spike_nums_dur = np.zeros((spike_nums_dur.shape[0], spike_nums_dur.shape[1]), dtype="int8")
    for cell in np.arange(n_cells):
        periods = get_continous_time_periods(spike_nums_dur[cell])
        for period in periods:
            if np.sum(spike_nums[cell, period[0]:period[1] + 1]) > 0:
                final_spike_nums_dur[cell, period[0]:period[1] + 1] = 1

    return final_spike_nums_dur


class SessionForBenchmark:
    """
    From a directory content including a yaml config file, will read ground truth + infered data
    """

    def __init__(self, dir_to_explore, inferences_to_benchmark, predictions_keywords_dict,
                 default_predictions_threshold):
        """

        Args:
            dir_to_explore:
            inferences_to_benchmark: list of inference_id, if empty with evaluate all inference, otherwise just those in the list
        """
        self.inferences_to_benchmark = inferences_to_benchmark
        self.dir_to_explore = dir_to_explore
        self.valid = False
        self.session_id = os.path.basename(dir_to_explore)
        self.predictions_keywords_dict = predictions_keywords_dict
        self.default_predictions_threshold = default_predictions_threshold
        self.cells_in_ground_truth = None

        # 2d binary array (n_cells * n_frames)
        self.ground_truth = None
        self.smooth_traces = None
        self.inferences_raster_dict = dict()
        self.cells_by_inference = dict()

        file_names = []

        # look for filenames in the fisrst directory, if we don't break, it will go through all directories
        for (dirpath, dirnames, local_filenames) in os.walk(self.dir_to_explore):
            file_names.extend(local_filenames)
            break

        yaml_file_name = [f for f in file_names if f.endswith(".yaml")]
        if len(yaml_file_name) == 0:
            print(f"SessionForBenchmark: no yaml config file in : {self.dir_to_explore}")
            return
        yaml_file_name = os.path.join(dir_to_explore, yaml_file_name[0])

        file_names = [f for f in file_names if (not f.endswith(".yaml")) and (not f.startswith("."))]

        # reading the yaml file
        with open(yaml_file_name, 'r') as stream:
            yaml_data = yaml.load(stream, Loader=yaml.FullLoader)

        if "groundtruth" not in yaml_data:
            raise Exception(f"No groundtruth given in {yaml_file_name}")

        yaml_keys = list(yaml_data.keys())
        # we want to start by ground_truth
        yaml_keys.remove("groundtruth")
        yaml_keys = ["groundtruth"] + yaml_keys
        for inference_id in yaml_keys:
            inference_data = yaml_data[inference_id]
            if "cells" not in inference_data:
                raise Exception(f"Cells are not indicated for {inference_id} of {yaml_file_name}")
            cells = inference_data["cells"]

            if "file_name" not in inference_data:
                raise Exception(f"No file_name given in inference data {inference_id} of {yaml_file_name}")
            inference_file_name = inference_data["file_name"]

            # we remove the file from the list of filenames
            if inference_file_name in file_names:
                file_names.remove(inference_file_name)

            inference_file_name = os.path.join(dir_to_explore, inference_file_name)

            if inference_id == "groundtruth":
                # then we look at extension to decide how to benchmark it
                if not inference_file_name.endswith("cinac"):
                    raise Exception(f"{os.path.basename(inference_file_name)} format not yet "
                                    f"implemented for ground truth"
                                    f"in {yaml_file_name}")
                self.cells_in_ground_truth = cells
                # so far ground truth file has to be in cinac format
                self.extract_data_from_cinac_file(cinac_file=inference_file_name, cells_to_add=cells,
                                                  for_ground_truth=True, label=None)
                continue
            else:
                if len(self.inferences_to_benchmark) > 0 and (inference_id not in self.inferences_to_benchmark):
                    # this inference is not on the list of inferences to evaluate
                    continue

                if inference_file_name.endswith("cinac"):
                    self.extract_data_from_cinac_file(cinac_file=inference_file_name, cells_to_add=cells,
                                                      for_ground_truth=False, label=inference_id)
                    continue
                if "prediction_threshold" in inference_data:
                    # means the data is issue of predictions from cinac
                    prediction_threshold = inference_data["prediction_threshold"]
                    predictions = load_data_from_np_or_mat_file(file_name=inference_file_name,
                                                                attr_name="predictions")

                    # then we produce the raster dur based on the predictions using threshold the prediction_threshold
                    raster_dur = np.zeros(predictions.shape, dtype="int8")

                    for cell in np.arange(len(predictions)):
                        raster_dur[cell, predictions[cell] >= prediction_threshold] = 1
                    self.inferences_raster_dict[inference_id] = [raster_dur, predictions]
                    self.cells_by_inference[inference_id] = cells
                    continue
                if inference_file_name.endswith("npy") or inference_file_name.endswith("mat") or \
                        inference_file_name.endswith("npz"):
                    # attribute name in the file (for npz or mat files)
                    attr_name = inference_data.get("attr_name", None)
                    # get a 2d array of shape n_cells*n_frames
                    # print(f"inference_file_name {inference_file_name}")
                    inference_neuronal_data = load_data_from_np_or_mat_file(file_name=inference_file_name,
                                                                            attr_name=attr_name)
                    if "to_bin" in inference_data and inference_data['to_bin']:
                        # bining the data, useful for caiman output for exemple
                        inference_neuronal_data = bin_raster(inference_neuronal_data)
                    if "traces_file_name" in inference_data:
                        traces_file_name = inference_data["traces_file_name"]
                        traces_file_name = os.path.join(dir_to_explore, traces_file_name)
                        traces_attr_name = inference_data.get("traces_attr_name", None)
                        traces = load_data_from_np_or_mat_file(file_name=traces_file_name,
                                                               attr_name=traces_attr_name)
                        inference_neuronal_data = get_raster_dur_spikes_and_traces(spike_nums=inference_neuronal_data,
                                                                                   traces=traces)

                    # mapping fiji coord to caiman coord if necessary
                    if "caiman_fiji_mapping" in inference_data:
                        print("caiman_fiji_mapping in inference_data")
                        caiman_fiji_mapping = np.load(
                            os.path.join(dir_to_explore, inference_data["caiman_fiji_mapping"]))
                        caiman_raster_dur = np.zeros((self.ground_truth.shape[0], inference_neuronal_data.shape[1]),
                                                     dtype="int8")
                        cells_mapped = []
                        # print(f"caiman_fiji_mapping {caiman_fiji_mapping}")
                        # caiman_fiji_mapping take a cell index from caiman segmentation
                        # and return a value > 0 if a cell of Fiji matches (the value is the index of this cell in fiji)
                        # -1 otherwise
                        for caiman_cell_index, fiji_cell_index in enumerate(caiman_fiji_mapping):
                            if fiji_cell_index >= 0:
                                # print(f"{inference_id}: Cell {fiji_cell_index} -> {caiman_cell_index}")
                                # using deconvolution value, cell is active if value > 0
                                caiman_raster_dur[fiji_cell_index] = inference_neuronal_data[caiman_cell_index]
                                # print(f"sum spikes: {np.sum(caiman_raster_dur[fiji_cell_index])}")
                                cells_mapped.append(fiji_cell_index)
                        inference_neuronal_data = caiman_raster_dur
                        cells_to_keep = []
                        for cell in cells:
                            if cell not in cells_mapped:  # caiman_fiji_mapping:
                                print(f"Cell {cell} has no match in caiman segmentation")
                            else:
                                cells_to_keep.append(cell)
                        cells = np.array(cells_to_keep)
                    self.inferences_raster_dict[inference_id] = [inference_neuronal_data]
                    self.cells_by_inference[inference_id] = cells
                    continue
                else:
                    print(f"Format of {os.path.basename(inference_file_name)} not supported")

        # then if the list of prediction keywords is not None, we list the files to find some
        if len(predictions_keywords_dict) > 0:
            for pred_keyword, inference_id in predictions_keywords_dict.items():
                for file_name in file_names:
                    if pred_keyword in file_name:
                        inference_file_name = os.path.join(dir_to_explore, file_name)
                        prediction_threshold = default_predictions_threshold
                        predictions = load_data_from_np_or_mat_file(file_name=inference_file_name,
                                                                    attr_name="predictions")

                        # then we produce the raster dur based on the predictions using threshold the prediction_threshold
                        raster_dur = np.zeros(predictions.shape, dtype="int8")

                        for cell in np.arange(len(predictions)):
                            raster_dur[cell, predictions[cell] >= prediction_threshold] = 1
                        self.inferences_raster_dict[inference_id] = [raster_dur, predictions]
                        # we put the same cells as in GT
                        self.cells_by_inference[inference_id] = self.cells_in_ground_truth
                        break

        self.valid = True

    def get_inference_ids(self):
        return list(self.inferences_raster_dict.keys())

    def extract_data_from_cinac_file(self, cinac_file, cells_to_add, for_ground_truth, label=None):
        """
        From a cinac_file,
        Args:
            session_id: str
            cinac_file:
            cells_to_add:
            for_ground_truth: (bool) to set ground truth or add some inference
            label: (str), necessary if for_ground_truth is False, allow to identify the inference

        Returns:

        """

        cinac_file_reader = CinacFileReader(file_name=cinac_file)

        n_cells = cinac_file_reader.get_n_cells()

        n_frames = cinac_file_reader.get_n_frames()

        if n_cells is None:
            raise Exception(f"{os.path.basename(cinac_file)} in {self.session_id} has not the n_cells info")

        if n_frames is None:
            raise Exception(f"{os.path.basename(cinac_file)} in {self.session_id} has not the n_frames info")

        segments = cinac_file_reader.get_all_segments()

        raster_dur = np.zeros((n_cells, n_frames), dtype="int8")

        if for_ground_truth:
            self.smooth_traces = np.zeros((n_cells, n_frames))

        for segment in segments:
            cell = segment[0]
            first_frame = segment[1]
            last_frame = segment[2]
            if cell not in cells_to_add:
                continue
            # then we fill the raster_dur
            raster_dur[cell, first_frame:last_frame + 1] = cinac_file_reader.get_segment_raster_dur(segment=segment)
            # and fluoresence signal, needed for the ground truth in order to find the putative transients
            if for_ground_truth:
                self.smooth_traces[cell, first_frame:last_frame + 1] = cinac_file_reader. \
                    get_segment_smooth_traces(segment=segment)

        if for_ground_truth:
            self.ground_truth = raster_dur
        else:
            self.inferences_raster_dict[label] = [raster_dur]
            self.cells_by_inference[label] = cells_to_add

    def add_it_to_cinac_benchmark(self, cinac_benchmarks):
        cinac_benchmarks.add_ground_truth(session_id=self.session_id, ground_truth=self.ground_truth,
                                          smooth_traces=self.smooth_traces)

        for inference_id, inference_data in self.inferences_raster_dict.items():
            raster_predictions = None
            if len(inference_data) > 1:
                raster_predictions = inference_data[1]
            cinac_benchmarks.add_inference_to_benchmark(session_id=self.session_id,
                                                        inference_to_benchmark_id=inference_id,
                                                        raster_to_evaluate=inference_data[0],
                                                        cells_to_benchmark=self.cells_by_inference[inference_id],
                                                        raster_predictions=raster_predictions)


def do_traces_smoothing(traces):
    # smoothing the trace
    windows = ['hanning', 'hamming', 'bartlett', 'blackman']
    i_w = 1
    window_length = 7  # 11
    for i in np.arange(traces.shape[0]):
        smooth_signal = smooth_convolve(x=traces[i], window_len=window_length,
                                        window=windows[i_w])
        beg = (window_length - 1) // 2
        traces[i] = smooth_signal[beg:-beg]


def benchmark_neuronal_activity_inferences(inferences_dir, results_path, colorfull_boxplots=True,
                                           white_background=False, color_cell_as_boxplot=False,
                                           with_legend=False, put_metric_as_y_axis_label=False,
                                           using_patch_for_legend=True, alpha_scatter=0.6,
                                           plot_proportion_frames_in_transients=False,
                                           with_cells=True, with_cell_number=True,
                                           predictions_stat_by_metrics=False,
                                           save_formats=["png", "eps"]):
    """
    Evaluate the performances of different inferences methods. Every directory in the main
    directory is considered a session with a ground truth and inferences to benchmark
    Args:
        inferences_dir: directory containing other directories, one by session to benchmark
        results_path:
        colorfull_boxplots: if True boxplots are filled with color
        white_background: if True background is white, else it's black
        with_cells: if True display scatter to represent metrics for a cell
        with_cell_number: Displau the cell number in the scatter if with_cells is True
        with_legend: if True, add legens to the F1 score plot

    Returns:

    """

    directories = []
    file_names_in_root = []

    # look for filenames in the fisrst directory, if we don't break, it will go through all directories
    for (dirpath, dirnames, local_filenames) in os.walk(inferences_dir):
        directories.extend(dirnames)
        file_names_in_root.extend(local_filenames)
        break
    if len(directories) == 0:
        print(f"No directories with inferences in {inferences_dir}")
        return

    config_yaml_files = [f for f in file_names_in_root if (not f.startswith(".") and f.endswith(".yaml"))]
    if len(config_yaml_files) == 0:
        print(f"No yaml benchmarks config file in {inferences_dir}")
        return

    # looping over configuration files and evaluate inference with each config
    for config_yaml_file in config_yaml_files:
        sessions_for_benchmark = []
        # first getting the main config yaml
        # list of inference_id, if empty with evaluate all inference, otherwise just those in the list
        inferences_to_benchmark = []
        sessions_to_exclude = []
        # dict that contains as keys a list of keyword allowing to selecting predictions file automatically
        # the value is the inference_id
        predictions_keywords_dict = {}
        default_predictions_threshold = 0.5

        config_yaml_file = os.path.join(inferences_dir, config_yaml_file)
        with open(config_yaml_file, 'r') as stream:
            yaml_data = yaml.load(stream, Loader=yaml.FullLoader)
        inferences_to_benchmark = yaml_data.get("inferences_to_benchmark", [])
        sessions_to_exclude = yaml_data.get("sessions_to_exclude", [])
        predictions_keywords_dict = yaml_data.get("predictions_keywords", {})
        default_predictions_threshold = yaml_data.get("predictions_threshold", 0.5)
        # allows to create a subdirecoty to put the results
        config_id = yaml_data.get("config_id", None)

        if config_id is None:
            config_results_path = results_path
        else:
            # create a directory
            config_results_path = os.path.join(results_path, config_id)
            os.mkdir(config_results_path)

        directories = [os.path.join(inferences_dir, d) for d in directories if not d.startswith(".")]

        inference_ids = []

        for dir_to_explore in directories:
            if os.path.basename(dir_to_explore) in sessions_to_exclude:
                # excluding the session evaluation
                continue

            session_for_benchmark = SessionForBenchmark(dir_to_explore=dir_to_explore,
                                                        inferences_to_benchmark=inferences_to_benchmark,
                                                        predictions_keywords_dict=predictions_keywords_dict,
                                                        default_predictions_threshold=default_predictions_threshold)
            if session_for_benchmark.valid:
                sessions_for_benchmark.append(session_for_benchmark)
                inference_ids.extend(session_for_benchmark.get_inference_ids())

        # making it unique
        inference_ids = set(inference_ids)
        colors_boxplots = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c',
                           '#ff7f00', '#cab2d6', '#fdbf6f', '#6a3d9a', '#ffff99', '#b15928', '#ffffd9']
        cinac_benchmarks = CinacBenchmarks(results_path=config_results_path, colors_boxplots=colors_boxplots)

        description = ""
        for session_index, session_for_benchmark in enumerate(sessions_for_benchmark):
            description = description + session_for_benchmark.session_id + "_"
            session_for_benchmark.add_it_to_cinac_benchmark(cinac_benchmarks=cinac_benchmarks)
            cinac_benchmarks.color_by_session(session_id=session_for_benchmark.session_id,
                                              color=BREWER_COLORS[session_index % len(BREWER_COLORS)])

        cinac_benchmarks.evaluate_metrics()

        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

        # only transients
        for for_frames in [False]:
            if predictions_stat_by_metrics:
                # plot the distribution of the the prediction values for each cell
                cinac_benchmarks.plot_boxplot_predictions_stat_by_metrics(description=description, time_str=time_str,
                                                                          for_frames=for_frames,
                                                                          colorfull=colorfull_boxplots,
                                                                          white_background=white_background,
                                                                          save_formats=save_formats,
                                                                          dpi=500)

            # tp get PPV and Sensitivity in the same figure
            # cinac_benchmarks.plot_boxplots_full_stat(description=description, time_str=time_str,
            #                                          colorfull=colorfull_boxplots,
            #                                          color_cell_as_boxplot=color_cell_as_boxplot,
            #                                          box_plots_labels=inferences_to_benchmark,
            #                                          white_background=white_background,
            #                                          stats_to_show=("sensitivity", "PPV"),
            #                                          title_correspondance={"sensitivity": "Sensitivity",
            #                                                                "PPV": "Precision"},
            #                                          for_frames=for_frames, save_formats=["png"], with_cells=True,
            #                                          alpha_scatter=0.8,
            #                                          dpi=500)

            cinac_benchmarks.stats_on_performance(stats_to_evaluate=["sensitivity", "PPV", "F1"],
                                                  data_labels=inferences_to_benchmark,
                                                  title_correspondance={"PPV": "Precision",
                                                                        "sensitivity": "Sensitivity"})

            cinac_benchmarks.plot_boxplots_full_stat(description=description, time_str=time_str,
                                                     colorfull=colorfull_boxplots,
                                                     color_cell_as_boxplot=color_cell_as_boxplot,
                                                     box_plots_labels=inferences_to_benchmark,
                                                     white_background=white_background,
                                                     stats_to_show=["sensitivity"],
                                                     title_correspondance={"sensitivity": "Sensitivity"},
                                                     for_frames=for_frames, save_formats=save_formats,
                                                     with_cells=with_cells,
                                                     put_metric_as_y_axis_label=put_metric_as_y_axis_label,
                                                     with_cell_number=with_cell_number,
                                                     with_legend=with_legend,
                                                     using_patch_for_legend=using_patch_for_legend,
                                                     alpha_scatter=alpha_scatter,
                                                     dpi=500)

            cinac_benchmarks.plot_boxplots_full_stat(description=description, time_str=time_str,
                                                     colorfull=colorfull_boxplots,
                                                     color_cell_as_boxplot=color_cell_as_boxplot,
                                                     box_plots_labels=inferences_to_benchmark,
                                                     white_background=white_background,
                                                     stats_to_show=["PPV"],
                                                     title_correspondance={"PPV": "Precision"},
                                                     for_frames=for_frames, save_formats=save_formats,
                                                     with_cells=with_cells,
                                                     put_metric_as_y_axis_label=put_metric_as_y_axis_label,
                                                     # with_legend=with_legend,
                                                     # using_patch_for_legend=using_patch_for_legend,
                                                     with_cell_number=with_cell_number,
                                                     alpha_scatter=alpha_scatter,
                                                     dpi=500)

            cinac_benchmarks.plot_boxplots_f1_score(description=description, time_str=time_str,
                                                    colorfull=colorfull_boxplots,
                                                    color_cell_as_boxplot=color_cell_as_boxplot,
                                                    box_plots_labels=inferences_to_benchmark,
                                                    white_background=white_background,
                                                    with_cell_number=with_cell_number,
                                                    # with_legend=with_legend,
                                                    # using_patch_for_legend=using_patch_for_legend,
                                                    alpha_scatter=alpha_scatter,
                                                    for_frames=for_frames, save_formats=save_formats,
                                                    with_cells=with_cells,
                                                    put_metric_as_y_axis_label=put_metric_as_y_axis_label,
                                                    dpi=500)
        if plot_proportion_frames_in_transients:
            cinac_benchmarks.plot_boxplots_proportion_frames_in_transients(description=description,
                                                                           time_str=time_str,
                                                                           only_this_key=None,
                                                                           colorfull=colorfull_boxplots,
                                                                           white_background=white_background,
                                                                           alpha_scatter=alpha_scatter,
                                                                           with_legend=with_legend,
                                                                           using_patch_for_legend=using_patch_for_legend,
                                                                           with_scatter=True,
                                                                           with_cell_text=False,
                                                                           put_metric_as_y_axis_label=put_metric_as_y_axis_label,
                                                                           save_formats=save_formats, dpi=500)
            #
        # for inference_id in inference_ids:
        #     cinac_benchmarks.plot_boxplots_proportion_frames_in_transients(description=description,
        #                                                                    time_str=time_str,
        #                                                                    only_this_key=inference_id,
        #                                                                    colorfull=colorfull_boxplots,
        #                                                                    white_background=white_background,
        #                                                                    with_scatter=True,
        #                                                                    with_cell_text=False,
        #                                                                    save_formats="png", dpi=500)


def extract_age(label):
    try:
        label = label[1:]
        index = label.index("_")
        return int(label[:index])
    except Exception:
        return label
